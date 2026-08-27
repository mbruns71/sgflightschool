# N61574 Checklist app — release process

Live at **https://www.sgflightschool.com/checklist/**

## How offline + update checking works

The app registers a service worker that caches itself, so it opens with no
signal. Nothing updates silently: when the device has a connection the app
fetches `version.json` and compares it to the `APP_VERSION` baked into
`index.html`. If they differ it shows an amber banner with **Update now**.
A checklist must never change itself while someone is flying it.

Service workers need HTTPS. A `file://` copy works offline but can never
check for updates — the About tab says so explicitly when it detects one.

## Publishing an update

1. Edit `index.html` in this folder.
2. Bump the version string in **three** places — they must match exactly:
   - `index.html`  -> `var APP_VERSION = "YYYY.MM.DD-N";`
   - `dist/sw.js`  -> `var VERSION = "YYYY.MM.DD-N";`  (changes the cache name)
   - `dist/version.json` -> `"version": "YYYY.MM.DD-N"` plus a short `notes` line
3. Copy into the site and deploy:

   cp index.html dist/
   cp dist/index.html dist/sw.js dist/manifest.webmanifest dist/version.json \
      dist/icon-*.png ../sgflightschool/site/checklist/
   cd ../sgflightschool && npx wrangler pages deploy site --project-name=sgflightschool

If `sw.js` is byte-identical to the deployed copy the browser will not install
a new worker — that is why its VERSION constant must change too.

## Why the cache headers matter

`site/_headers` sets `Cache-Control: no-cache` on `sw.js`, `version.json`,
`index.html` and the manifest. Without that, Cloudflare would serve a stale
`version.json` from the edge and iPads would never learn an update exists.
The icons are cached for a week; they rarely change.

## Checking it worked

- Open https://www.sgflightschool.com/checklist/ -> Setup -> About.
  "This copy" and "Latest published" should match.
- To prove offline: load it once, enable Airplane Mode, force-quit, reopen.

## Pilot install instructions (iPhone / iPad)

1. Open https://www.sgflightschool.com/checklist/ in Safari (must be Safari).
2. Share -> Add to Home Screen.
3. Launch from the home screen icon. It runs full screen and works with no signal.
4. Set Settings -> Display & Brightness -> Auto-Lock -> Never before flying.

Home-screen web apps are exempt from Safari's 7-day storage eviction, so
saved aircraft and edits persist. Export from Setup -> Backup anyway.

## Setup password

Setup is gated. The credential is **never stored or shipped in plaintext**.

- `functions/checklist/auth.js` is a Cloudflare Pages Function at
  `/checklist/auth`. It keeps a PBKDF2-SHA256 hash (150k iterations, random
  16-byte salt) in the existing `ENQUIRIES` KV namespace under a
  `checklist:` key prefix, so no new namespace is needed.
- Unlocking posts the password, gets back an HMAC-signed 12-hour token.
  The HMAC signing key is generated on first request and stored in KV, so
  there is no secret to configure.
- Failed attempts are rate limited to 10 per 10 minutes per IP.
- The default password is `SGFlight`, seeded on first use from the
  `BOOTSTRAP` constant in the Function. That constant is server-side and is
  never sent to a browser, but it does sit in this repo — change the
  password once from Setup and only the hash exists thereafter.

Change it in the app: **Setup -> About -> Setup password**. The current
password is always required, so a device left unlocked cannot have its
password silently taken over. A change applies to every device.

### Offline

Verifying against the server needs a connection. Because the whole point of
this app is working with no signal, a successful online unlock also caches a
PBKDF2 hash of the password on the device, and that is used to check the
password when offline. It is weaker than the server check — it lives on the
device and could be tampered with — but it still requires knowing the
password, and the server stays authoritative whenever there is a connection.

Changing the password always requires a connection.

The unlock lasts the browsing session only. Force-quitting re-locks it, and
Setup -> About has a "Lock setup" button.
