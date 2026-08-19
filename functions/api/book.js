/**
 * POST /api/book — booking enquiry handler.
 *
 * Runs as a Cloudflare Pages Function. Deliberately fail-safe: a submission is
 * persisted first and email is sent best-effort, so a mail misconfiguration can
 * never lose an enquiry. If persistence is also unavailable the submission is
 * written to the log (visible via `wrangler pages deployment tail`) and the
 * visitor still gets a success response with the phone number.
 *
 * Bindings (all optional — the handler degrades rather than erroring):
 *   ENQUIRIES  KV namespace   durable store for every submission
 *   SEND_EMAIL Email binding  Cloudflare Email Service (public beta)
 *   RESEND_API_KEY  secret    used instead of SEND_EMAIL if present
 */

const TO = "info@sgflightschool.com";

// Sends from a SUBDOMAIN, not the root domain. The root's MX and SPF belong to
// Microsoft 365; putting a second mail provider's MX/SPF there would risk the
// school's actual email. send.sgflightschool.com keeps Resend fully isolated,
// and still aligns for DMARC because relaxed alignment matches the org domain.
const FROM = "website@send.sgflightschool.com";
const PHONE = "(406) 609-6798";

const FIELDS = ["name", "phone", "email", "interest", "when", "notes"];
const LIMITS = { name: 120, phone: 40, email: 160, interest: 80, when: 200, notes: 2000 };

function json(status, body) {
  return new Response(JSON.stringify(body), {
    status,
    headers: {
      "content-type": "application/json; charset=utf-8",
      "cache-control": "no-store",
    },
  });
}

function clean(v, max) {
  if (typeof v !== "string") return "";
  // Strip control characters, collapse whitespace, cap length. Written with
  // explicit escapes so the class can't be mangled by an editor or diff.
  return v.replace(/[\x00-\x1F\x7F]/g, " ").replace(/\s+/g, " ").trim().slice(0, max);
}

function validate(data) {
  const errors = {};
  if (!data.name || data.name.length < 2) errors.name = "Please tell us your name.";
  const digits = (data.phone || "").replace(/\D/g, "");
  if (digits.length < 10) errors.phone = "Please enter a phone number we can reach you on.";
  if (data.email && !/^[^@\s]+@[^@\s.]+\.[^@\s]{2,}$/.test(data.email)) {
    errors.email = "That email address doesn't look right.";
  }
  return errors;
}

async function persist(env, record) {
  if (!env.ENQUIRIES) return false;
  // Key sorts newest-last and is unique per submission.
  const key = `enquiry:${record.received_at}:${record.id}`;
  await env.ENQUIRIES.put(key, JSON.stringify(record), {
    expirationTtl: 60 * 60 * 24 * 365 * 2, // keep two years
  });
  return true;
}

/**
 * Simple per-IP rate limit, backed by KV.
 *
 * Needed because the confirmation email lets a visitor cause mail to be sent to
 * an address they typed — without a cap that is a way to pester a third party
 * using this domain's reputation. Fails OPEN: if KV is unavailable a genuine
 * enquiry still gets through, which matters more than perfect enforcement.
 */
const RATE_MAX = 5;
const RATE_WINDOW_S = 3600;

async function rateLimited(env, ip) {
  if (!env.ENQUIRIES || !ip) return false;
  const key = `rl:${ip}`;
  try {
    const n = parseInt((await env.ENQUIRIES.get(key)) || "0", 10);
    if (n >= RATE_MAX) return true;
    await env.ENQUIRIES.put(key, String(n + 1), { expirationTtl: RATE_WINDOW_S });
    return false;
  } catch {
    return false;
  }
}

function confirmationText(r) {
  return [
    `Hi ${r.name.split(" ")[0]},`,
    ``,
    `Thanks for getting in touch with SG Flight School — we've got your request`,
    `and we'll come back to you shortly, usually the same day.`,
    ``,
    `If you'd rather not wait, just call us on ${PHONE}. Happy to answer`,
    `questions before you commit to anything.`,
    ``,
    `WHAT YOU SENT US`,
    `  Interested in: ${r.interest || "(not specified)"}`,
    `  Phone:         ${r.phone}`,
    r.when ? `  Availability:  ${r.when}` : null,
    r.notes ? `  Notes:         ${r.notes}` : null,
    ``,
    `WHAT HAPPENS NEXT`,
    `  1. We'll reply with a couple of times that fit your schedule.`,
    `  2. We handle the booking — there's nothing for you to sign up for.`,
    `  3. You turn up and fly. Bring nothing; wear sunglasses if you have them.`,
    ``,
    `A discovery flight is $199, takes about an hour including the ground`,
    `briefing, and you'll be flying the airplane yourself with an instructor`,
    `beside you. No experience or medical certificate needed.`,
    ``,
    `Wondering what full training costs or how long it takes? We answer both`,
    `honestly here: https://www.sgflightschool.com/faq`,
    ``,
    `See you at Falcon Field,`,
    `SG Flight School`,
    `4800 E Falcon Dr, Hangar 120, Mesa, AZ 85215`,
    `Falcon Field Airport (KFFZ)`,
    `${PHONE} | info@sgflightschool.com`,
    ``,
    `--`,
    `You're getting this because you submitted a booking request at`,
    `sgflightschool.com. If that wasn't you, please ignore this email — nothing`,
    `has been booked and we won't contact you again.`,
  ]
    .filter((l) => l !== null)
    .join("\n");
}

function asText(r) {
  return [
    `New enquiry from sgflightschool.com`,
    ``,
    `Name:      ${r.name}`,
    `Phone:     ${r.phone}`,
    `Email:     ${r.email || "(not given)"}`,
    `Interest:  ${r.interest || "(not given)"}`,
    `Available: ${r.when || "(not given)"}`,
    ``,
    `Notes:`,
    r.notes || "(none)",
    ``,
    `---`,
    `Received: ${r.received_at}`,
    `Ref:      ${r.id}`,
  ].join("\n");
}

async function notify(env, record) {
  const subject = `Discovery flight enquiry — ${record.name}`;
  const text = asText(record);

  if (env.RESEND_API_KEY) {
    const res = await fetch("https://api.resend.com/emails", {
      method: "POST",
      headers: {
        authorization: `Bearer ${env.RESEND_API_KEY}`,
        "content-type": "application/json",
      },
      body: JSON.stringify({
        from: `SG Flight School <${FROM}>`,
        to: [TO],
        reply_to: record.email || undefined,
        subject,
        text,
      }),
    });
    if (!res.ok) throw new Error(`resend ${res.status}: ${await res.text()}`);
    return "resend";
  }

  if (env.SEND_EMAIL) {
    await env.SEND_EMAIL.send({
      to: [{ email: TO }],
      from: { email: FROM, name: "SG Flight School website" },
      replyTo: record.email ? { email: record.email } : undefined,
      subject,
      text,
    });
    return "cloudflare";
  }

  throw new Error("no email binding configured");
}

/**
 * Confirmation to the person who submitted, so they know it landed.
 * Reply-To is the school's real inbox, so replying reaches a human.
 */
async function confirm(env, record) {
  if (!record.email) return "skipped — no email given";

  const payload = {
    from: `SG Flight School <${FROM}>`,
    to: [record.email],
    reply_to: TO,
    subject: "Thanks — we've got your request | SG Flight School",
    text: confirmationText(record),
  };

  if (env.RESEND_API_KEY) {
    const res = await fetch("https://api.resend.com/emails", {
      method: "POST",
      headers: {
        authorization: `Bearer ${env.RESEND_API_KEY}`,
        "content-type": "application/json",
      },
      body: JSON.stringify(payload),
    });
    if (!res.ok) throw new Error(`resend ${res.status}: ${await res.text()}`);
    return "sent via resend";
  }

  if (env.SEND_EMAIL) {
    await env.SEND_EMAIL.send({
      to: [{ email: record.email }],
      from: { email: FROM, name: "SG Flight School" },
      replyTo: { email: TO },
      subject: payload.subject,
      text: payload.text,
    });
    return "sent via cloudflare";
  }

  throw new Error("no email binding configured");
}

export async function onRequestPost({ request, env }) {
  let data = {};
  try {
    const ct = request.headers.get("content-type") || "";
    if (ct.includes("application/json")) {
      const raw = await request.json();
      for (const f of FIELDS) data[f] = clean(raw[f], LIMITS[f]);
      data.website = clean(raw.website, 100);
    } else {
      const form = await request.formData();
      for (const f of FIELDS) data[f] = clean(form.get(f), LIMITS[f]);
      data.website = clean(form.get("website"), 100);
    }
  } catch {
    return json(400, { ok: false, error: "Could not read that submission." });
  }

  // Honeypot filled → almost certainly a bot. Accept silently so it doesn't retry.
  if (data.website) return json(200, { ok: true });

  const errors = validate(data);
  if (Object.keys(errors).length) return json(422, { ok: false, errors });

  const ip = request.headers.get("cf-connecting-ip") || "";
  if (await rateLimited(env, ip)) {
    return json(429, {
      ok: false,
      error:
        `That's several requests in a short time. If something isn't working, ` +
        `please call ${PHONE} and we'll sort it out directly.`,
    });
  }

  const record = {
    id: crypto.randomUUID().slice(0, 8),
    received_at: new Date().toISOString(),
    ...FIELDS.reduce((o, f) => ((o[f] = data[f]), o), {}),
    ip_country: request.headers.get("cf-ipcountry") || "",
    user_agent: (request.headers.get("user-agent") || "").slice(0, 200),
  };

  // Persist FIRST so the enquiry is captured even if email hangs or fails.
  let stored = false;
  try {
    stored = await persist(env, record);
  } catch (e) {
    console.error("persist failed:", e.message);
  }

  let sent = null;
  let emailError = null;
  try {
    sent = await notify(env, record);
  } catch (e) {
    emailError = e.message;
    console.error("email failed:", e.message);
  }

  // Confirmation to the visitor. Entirely best-effort: if this fails the school
  // has still been notified, which is the part that actually matters.
  let confirmStatus = null;
  try {
    confirmStatus = await confirm(env, record);
  } catch (e) {
    confirmStatus = `FAILED: ${e.message}`;
    console.error("confirmation failed:", e.message);
  }

  // Record the delivery outcomes alongside the enquiry. Without this there is no
  // way to tell a delivered notification from a silently failed one — the
  // visitor sees success either way, by design.
  if (stored) {
    try {
      record.email_status = sent ? `sent via ${sent}` : `FAILED: ${emailError}`;
      record.confirmation_status = confirmStatus;
      await persist(env, record);
    } catch (e) {
      console.error("status update failed:", e.message);
    }
  }

  // Nothing worked — make sure the submission is at least in the log, and tell
  // the visitor to call rather than pretending we received it cleanly.
  if (!stored && !sent) {
    console.error("UNDELIVERED ENQUIRY (no KV, no email):", JSON.stringify(record));
    return json(200, {
      ok: true,
      degraded: true,
      ref: record.id,
      message:
        `Thanks — we've got your details. If you don't hear from us within a day, ` +
        `please call ${PHONE} to be safe.`,
    });
  }

  return json(200, {
    ok: true,
    ref: record.id,
    message:
      "Thanks — we've got it. We'll be in touch shortly, usually the same day. " +
      `If you'd rather not wait, call ${PHONE}.`,
  });
}

// A GET here means someone navigated to the endpoint directly.
export async function onRequestGet() {
  return Response.redirect("https://www.sgflightschool.com/book", 302);
}
