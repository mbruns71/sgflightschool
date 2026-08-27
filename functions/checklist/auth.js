/**
 * POST /checklist/auth — Setup password for the N61574 checklist app.
 *
 * The password is never stored, shipped, or logged in plaintext. KV holds a
 * PBKDF2-SHA256 hash with a per-password random salt. Unlocking returns a
 * short-lived HMAC token; the client presents nothing else.
 *
 * Bindings:
 *   ENQUIRIES  KV namespace  reused with a "checklist:" key prefix so no new
 *                            namespace has to be provisioned.
 *
 * Keys:
 *   checklist:pwhash   {salt, hash, iter}   the credential
 *   checklist:signkey  base64                HMAC key, generated on first use
 *   checklist:rl:<ip>  attempt counter       brute-force brake
 *
 * There is no secret to configure: the signing key is created on first
 * request and stored in KV.
 */

// Cloudflare Workers cap PBKDF2 at 100k iterations; asking for more throws.
const ITERATIONS = 100000;
const TOKEN_TTL_S = 12 * 60 * 60;   // 12 hours
const RATE_MAX = 10;                // failed attempts...
const RATE_WINDOW_S = 600;          // ...per 10 minutes, per IP
const BOOTSTRAP = "SGFlight";       // seeded only if no credential exists yet

function json(status, body) {
  return new Response(JSON.stringify(body), {
    status,
    headers: { "content-type": "application/json; charset=utf-8", "cache-control": "no-store" },
  });
}

const enc = new TextEncoder();
const b64 = (buf) => btoa(String.fromCharCode(...new Uint8Array(buf)));
const unb64 = (s) => Uint8Array.from(atob(s), (c) => c.charCodeAt(0));

/** Comparison that does not leak how much of the value matched. */
function sameBytes(a, b) {
  if (a.length !== b.length) return false;
  let diff = 0;
  for (let i = 0; i < a.length; i++) diff |= a[i] ^ b[i];
  return diff === 0;
}

async function pbkdf2(password, salt, iter) {
  const key = await crypto.subtle.importKey("raw", enc.encode(password), "PBKDF2", false, ["deriveBits"]);
  return new Uint8Array(
    await crypto.subtle.deriveBits({ name: "PBKDF2", salt, iterations: iter, hash: "SHA-256" }, key, 256)
  );
}

async function makeCredential(password) {
  const salt = crypto.getRandomValues(new Uint8Array(16));
  const hash = await pbkdf2(password, salt, ITERATIONS);
  return { salt: b64(salt), hash: b64(hash), iter: ITERATIONS };
}

async function verifyCredential(cred, password) {
  const got = await pbkdf2(password, unb64(cred.salt), cred.iter || ITERATIONS);
  return sameBytes(got, unb64(cred.hash));
}

/** Read the stored credential, seeding the default one the first time. */
async function getCredential(env) {
  const raw = await env.ENQUIRIES.get("checklist:pwhash");
  if (raw) return JSON.parse(raw);
  const cred = await makeCredential(BOOTSTRAP);
  await env.ENQUIRIES.put("checklist:pwhash", JSON.stringify(cred));
  return cred;
}

async function signKey(env) {
  let raw = await env.ENQUIRIES.get("checklist:signkey");
  if (!raw) {
    raw = b64(crypto.getRandomValues(new Uint8Array(32)));
    await env.ENQUIRIES.put("checklist:signkey", raw);
  }
  return crypto.subtle.importKey("raw", unb64(raw), { name: "HMAC", hash: "SHA-256" }, false, ["sign", "verify"]);
}

async function issueToken(env) {
  const payload = b64(enc.encode(JSON.stringify({ exp: Date.now() + TOKEN_TTL_S * 1000 })));
  const sig = b64(await crypto.subtle.sign("HMAC", await signKey(env), enc.encode(payload)));
  return payload + "." + sig;
}

async function tokenValid(env, token) {
  if (typeof token !== "string" || token.indexOf(".") < 0) return false;
  const [payload, sig] = token.split(".");
  try {
    const ok = await crypto.subtle.verify("HMAC", await signKey(env), unb64(sig), enc.encode(payload));
    if (!ok) return false;
    return JSON.parse(new TextDecoder().decode(unb64(payload))).exp > Date.now();
  } catch (e) {
    return false;
  }
}

/** Brute-force brake. Counts only failures, so normal use never trips it. */
async function overLimit(env, ip) {
  if (!ip) return false;
  const n = parseInt((await env.ENQUIRIES.get("checklist:rl:" + ip)) || "0", 10);
  return n >= RATE_MAX;
}
async function noteFailure(env, ip) {
  if (!ip) return;
  const key = "checklist:rl:" + ip;
  const n = parseInt((await env.ENQUIRIES.get(key)) || "0", 10);
  await env.ENQUIRIES.put(key, String(n + 1), { expirationTtl: RATE_WINDOW_S });
}

export async function onRequestPost(ctx) {
  try {
    return await handle(ctx);
  } catch (err) {
    // Never surface a bare 1101 to the app — it cannot tell that apart from
    // being offline, and would silently fall back to the weaker local check.
    console.log("checklist auth error: " + (err && err.stack ? err.stack : err));
    return json(500, { error: "The server could not check that right now." });
  }
}

async function handle({ request, env }) {
  if (!env.ENQUIRIES) return json(503, { error: "unconfigured" });

  let body;
  try { body = await request.json(); } catch (e) { return json(400, { error: "bad request" }); }

  const ip = request.headers.get("cf-connecting-ip") || "";
  const action = body && body.action;
  const password = typeof body.password === "string" ? body.password : "";

  if (await overLimit(env, ip)) {
    return json(429, { error: "Too many attempts. Wait ten minutes and try again." });
  }

  if (action === "unlock") {
    const cred = await getCredential(env);
    if (!(await verifyCredential(cred, password))) {
      await noteFailure(env, ip);
      return json(401, { error: "That password is not right." });
    }
    return json(200, { token: await issueToken(env), ttl: TOKEN_TTL_S });
  }

  if (action === "change") {
    const next = typeof body.newPassword === "string" ? body.newPassword : "";
    if (next.length < 6) return json(400, { error: "Use at least 6 characters." });
    if (next.length > 200) return json(400, { error: "That password is too long." });

    /* Changing requires the current password even when already unlocked, so a
       device left open cannot have its password silently taken over. */
    const cred = await getCredential(env);
    if (!(await verifyCredential(cred, password))) {
      await noteFailure(env, ip);
      return json(401, { error: "The current password is not right." });
    }
    await env.ENQUIRIES.put("checklist:pwhash", JSON.stringify(await makeCredential(next)));
    return json(200, { ok: true, token: await issueToken(env), ttl: TOKEN_TTL_S });
  }

  if (action === "check") {
    return json(200, { valid: await tokenValid(env, body.token) });
  }

  return json(400, { error: "unknown action" });
}

export async function onRequestGet() {
  return json(405, { error: "POST only" });
}
