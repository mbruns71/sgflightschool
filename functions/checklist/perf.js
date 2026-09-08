/**
 * /checklist/perf — POH performance page images, per aircraft.
 *
 * GET  ?aircraft=<id>&page=<id>          -> the image bytes
 * POST {action:"put",   token, aircraft, page, type, data}   data is base64, no prefix
 * POST {action:"prune", token, aircraft, keep:[pageIds]}      delete this aircraft's pages not in keep
 *
 * Reading is open, like the checklist itself: a device with no credential
 * must still be able to pull the pages. Writing requires an unlock token
 * from /checklist/auth, so whoever holds the Setup password can publish.
 *
 * Images are stored as binary KV values with the content type in metadata,
 * keyed checklist:perf:<aircraft>:<page>. Page ids are unique per upload,
 * so a cached image can never go stale.
 */

const PREFIX = "checklist:perf:";
const MAX_BYTES = 2 * 1024 * 1024;
const ID = /^[A-Za-z0-9_-]{1,64}$/;

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

export async function onRequestGet({ request, env }) {
  try {
    if (!env.ENQUIRIES) return json(503, { error: "unconfigured" });
    const u = new URL(request.url);
    const aircraft = u.searchParams.get("aircraft") || "", page = u.searchParams.get("page") || "";
    if (!ID.test(aircraft) || !ID.test(page)) return json(400, { error: "bad id" });

    const hit = await env.ENQUIRIES.getWithMetadata(PREFIX + aircraft + ":" + page, { type: "arrayBuffer" });
    if (!hit || !hit.value) return json(404, { error: "no such page" });
    return new Response(hit.value, {
      status: 200,
      headers: {
        "content-type": (hit.metadata && hit.metadata.type) || "image/jpeg",
        // ids are unique per upload, so this can never serve a stale page
        "cache-control": "public, max-age=604800",
      },
    });
  } catch (err) {
    console.log("perf get error: " + (err && err.stack ? err.stack : err));
    return json(500, { error: "Could not read that page." });
  }
}

export async function onRequestPost({ request, env }) {
  try {
    if (!env.ENQUIRIES) return json(503, { error: "unconfigured" });
    let body;
    try { body = await request.json(); } catch (e) { return json(400, { error: "bad request" }); }

    if (!(await tokenValid(env, body.token))) {
      return json(401, { error: "Setup is locked, or the unlock has expired. Unlock Setup and try again." });
    }
    if (!ID.test(body.aircraft || "")) return json(400, { error: "bad aircraft id" });

    if (body.action === "put") {
      if (!ID.test(body.page || "")) return json(400, { error: "bad page id" });
      if (typeof body.data !== "string" || !body.data) return json(400, { error: "no image" });
      let bytes;
      try { bytes = unb64(body.data); } catch (e) { return json(400, { error: "image is not valid base64" }); }
      if (bytes.length > MAX_BYTES) return json(413, { error: "That page is too large. Pages are limited to 2 MB." });
      const type = /^image\/(jpeg|png|webp)$/.test(body.type || "") ? body.type : "image/jpeg";
      await env.ENQUIRIES.put(PREFIX + body.aircraft + ":" + body.page, bytes, { metadata: { type } });
      return json(200, { ok: true, bytes: bytes.length });
    }

    if (body.action === "prune") {
      const keep = new Set(Array.isArray(body.keep) ? body.keep.filter((k) => ID.test(k)) : []);
      const listed = await env.ENQUIRIES.list({ prefix: PREFIX + body.aircraft + ":" });
      let removed = 0;
      for (const k of listed.keys) {
        const page = k.name.slice((PREFIX + body.aircraft + ":").length);
        if (!keep.has(page)) { await env.ENQUIRIES.delete(k.name); removed++; }
      }
      return json(200, { ok: true, removed });
    }

    return json(400, { error: "unknown action" });
  } catch (err) {
    console.log("perf post error: " + (err && err.stack ? err.stack : err));
    return json(500, { error: "The server could not store that right now." });
  }
}
