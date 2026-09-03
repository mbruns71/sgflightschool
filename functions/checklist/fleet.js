/**
 * /checklist/fleet — the shared checklist for every device.
 *
 * GET  ?head=1   cheap poll: {rev, published, note, aircraft}
 * GET            full pull:  {rev, published, note, db}
 * POST {action:"publish", token, db, note}
 *
 * Reading is open — the checklist is not a secret, and a device with no
 * credential must still be able to pull the current one. Publishing requires
 * a valid unlock token from /checklist/auth, so whoever holds the Setup
 * password can push, which is the rule the school asked for.
 *
 * The signing key is the same KV entry /checklist/auth uses, so a token
 * issued there verifies here.
 *
 * Bindings: ENQUIRIES (KV), keys under "checklist:".
 */

const KEY = "checklist:fleet";
const MAX_BYTES = 2 * 1024 * 1024;   // a checklist is tens of KB; this is a sanity bound

function json(status, body) {
  return new Response(JSON.stringify(body), {
    status,
    headers: { "content-type": "application/json; charset=utf-8", "cache-control": "no-store" },
  });
}

const enc = new TextEncoder();
const unb64 = (s) => Uint8Array.from(atob(s), (c) => c.charCodeAt(0));
const b64 = (buf) => btoa(String.fromCharCode(...new Uint8Array(buf)));

async function signKey(env) {
  let raw = await env.ENQUIRIES.get("checklist:signkey");
  if (!raw) {
    raw = b64(crypto.getRandomValues(new Uint8Array(32)));
    await env.ENQUIRIES.put("checklist:signkey", raw);
  }
  return crypto.subtle.importKey("raw", unb64(raw), { name: "HMAC", hash: "SHA-256" }, false, ["sign", "verify"]);
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

/** Cheap content hash (FNV-1a), so a device can tell "same content" from
 *  "different content" without comparing the whole checklist. */
function fingerprint(str) {
  let h = 0x811c9dc5;
  for (let i = 0; i < str.length; i++) {
    h ^= str.charCodeAt(i);
    h = (h + (h << 1) + (h << 4) + (h << 7) + (h << 8) + (h << 24)) >>> 0;
  }
  return h.toString(16);
}

/** Summary so a device can describe the update without pulling all of it. */
function summarise(db) {
  try {
    return (db.list || []).map((a) => String(a.tail || "?")).slice(0, 12);
  } catch (e) {
    return [];
  }
}

export async function onRequestGet({ request, env }) {
  try {
    if (!env.ENQUIRIES) return json(503, { error: "unconfigured" });
    const raw = await env.ENQUIRIES.get(KEY);
    if (!raw) return json(200, { rev: 0 });
    const rec = JSON.parse(raw);
    if (new URL(request.url).searchParams.get("head")) {
      return json(200, { rev: rec.rev, published: rec.published, note: rec.note, aircraft: rec.aircraft, fingerprint: rec.fingerprint });
    }
    return json(200, rec);
  } catch (err) {
    console.log("fleet get error: " + (err && err.stack ? err.stack : err));
    return json(500, { error: "Could not read the shared checklist." });
  }
}

export async function onRequestPost({ request, env }) {
  try {
    if (!env.ENQUIRIES) return json(503, { error: "unconfigured" });

    let body;
    try { body = await request.json(); } catch (e) { return json(400, { error: "bad request" }); }
    if (body.action !== "publish") return json(400, { error: "unknown action" });

    if (!(await tokenValid(env, body.token))) {
      return json(401, { error: "Setup is locked, or the unlock has expired. Unlock Setup and try again." });
    }
    if (!body.db || !Array.isArray(body.db.list) || !body.db.list.length) {
      return json(400, { error: "Nothing to publish." });
    }

    const payload = JSON.stringify(body.db);
    if (payload.length > MAX_BYTES) return json(413, { error: "That checklist is too large to publish." });

    // The revision is the publish time, NOT previous + 1.
    //
    // KV is eventually consistent and caches reads at the edge for ~60s, so a
    // read-modify-write here silently collided: two publishes a few seconds
    // apart both read the same stale record, both wrote the same revision, and
    // the second one's edits became invisible to any device that had already
    // taken the first (the client only accepts rev > its own). A timestamp is
    // monotonic and needs no read, so the race cannot happen.
    const rev = Date.now();

    const rec = {
      rev,
      published: new Date(rev).toISOString(),
      note: typeof body.note === "string" ? body.note.slice(0, 200) : "",
      aircraft: summarise(body.db),
      fingerprint: fingerprint(payload),
      db: body.db,
    };
    await env.ENQUIRIES.put(KEY, JSON.stringify(rec));
    return json(200, { ok: true, rev, published: rec.published, fingerprint: rec.fingerprint });
  } catch (err) {
    console.log("fleet publish error: " + (err && err.stack ? err.stack : err));
    return json(500, { error: "The server could not publish that right now." });
  }
}
