# SG Flight School — website prototype

A fast static rebuild of sgflightschool.com, ready to deploy to Cloudflare Pages.

## Look at it

**Easiest:** open `preview-standalone/index.html` in a browser and click around.
No server needed.

**Live-reloading local server:**

```bash
python3 "/Users/mikebruns/Projects/sgflightschool/serve.py"
```

Then visit http://localhost:8788 — this rebuilds first and serves with the same
clean URLs and redirects Cloudflare Pages will use.

## Edit it

All copy lives in `content.py`, one dict per page. Site-wide details (phone,
address, booking links) live in `siteconfig.py`. Shared header, footer, nav and
structured data live in `build.py`.

After any edit:

```bash
python3 build.py && python3 make_standalone.py
```

## Layout

| Path | What |
|---|---|
| `siteconfig.py` | Phone, address, booking URLs — **edit before launch** |
| `content.py` | Page copy |
| `build.py` | Template, nav, footer, JSON-LD → writes `site/` |
| `make_standalone.py` | Writes `preview-standalone/` for offline review |
| `serve.py` | Local preview server on :8788 |
| `site/` | **Deploy this directory** |
| `site/_redirects` | Old Squarespace URLs → new ones |
| `site/_headers` | Security headers, asset caching |
| `CLOUDFLARE-MIGRATION.md` | DNS + registrar migration runbook |

## Before launch

**Address — done.** `4800 E Falcon Dr, Hangar 120, Mesa, AZ 85215`, live on every
page and in the LocalBusiness structured data.

**Phone — works, but swap it before launch.** The site currently publishes
`(406) 609-6798`. That's a Montana area code on a Mesa flight school, which reads
as out-of-town to local callers. Get a **480** number (the East Valley area code)
and forward it to the 406.

Change `phone_display` and `phone_href` in `siteconfig.py` — nothing else needs
touching. Do this *before* the site goes live and before creating a Google
Business Profile, so the number never has to change once it's cited around the web.

### Getting a 480 number

| Option | Cost | Notes |
|---|---|---|
| **Google Voice** (personal) | Free | Pick a 480 number, forward to the 406. Free US calls/texts, voicemail transcription. Fine for a small operation; personal-use terms. |
| **Google Voice for Workspace** | ~$10/user/mo | Same thing under business terms. Requires Google Workspace, which you don't have — you're on Microsoft 365. |
| **Microsoft Teams Phone** | ~$8/user/mo + calling plan | Already integrated with your M365 tenant. Most consolidated, but the most setup. |
| **Grasshopper** | ~$14/mo | Purpose-built for small business. Business hours, greetings, no per-user fees. |
| **Quo (was OpenPhone)** | ~$15/user/mo | Best if instructors ever share an inbox. Overkill for one line. |

Start with Google Voice. It costs nothing, gets you a 480 number today, and
porting out later is straightforward if you outgrow it.

### Also worth doing

Set up a **Google Business Profile** for the Hangar 120 address. For a local
flight school this likely drives more calls than the website itself — it's what
puts you in the map results for "flight school near me" and "flight training
Mesa." Use the exact same name, address and phone as the site.

## Booking form — live, with email notifications working

`/book` is live. Every submission is stored in Cloudflare KV **and** emailed to
`info@sgflightschool.com` via Resend, with the enquirer's address as Reply-To so
replying goes straight back to them.

Verified end-to-end 2026-08-17: a live submission recorded
`email_status: "sent via resend"`.

### How it's wired

| Piece | Where |
|---|---|
| Form + client JS | `/book`, `site/assets/js/book.js` |
| Handler | `functions/api/book.js` (must stay at project root, **not** in `site/`) |
| Durable store | KV namespace `ENQUIRIES`, bound in `wrangler.toml` |
| Email | Resend, sending from `website@send.sgflightschool.com` |
| API key | Pages secret `RESEND_API_KEY` (never in the repo) |

**Sending uses the `send.sgflightschool.com` subdomain deliberately.** The root
domain's MX and SPF belong to Microsoft 365 — putting a second mail provider's
records there would risk the school's actual email. DMARC still aligns because
relaxed alignment matches the parent domain.

### Read enquiries any time

```bash
cd "/Users/mikebruns/Projects/sgflightschool" && npx wrangler kv key list --binding ENQUIRIES --remote
```

Then read one by its key:

```bash
npx wrangler kv key get "<key from the list>" --binding ENQUIRIES --remote
```

### If email ever stops working

Each stored record carries an `email_status` field — `sent via resend` or
`FAILED: <reason>`. Check it before assuming a lead was delivered:

```bash
npx wrangler kv key get "<key>" --binding ENQUIRIES --remote
```

The visitor always sees success, by design, so this field is the only way to tell
a delivered notification from a silently failed one.

To rotate the Resend key:

```bash
npx wrangler pages secret put RESEND_API_KEY --project-name=sgflightschool
```

### Two emails go out per submission

| Email | To | Reply-To | When |
|---|---|---|---|
| Notification | `info@sgflightschool.com` | the enquirer | always |
| Confirmation | the enquirer | `info@sgflightschool.com` | only if they gave an email |

Email is **optional** on the form (phone is the required field), so roughly some
share of enquiries won't get a confirmation. That's intentional — requiring an
email address would cost you submissions from people who'd rather just be called.

Each record stores both outcomes: `email_status` and `confirmation_status`.

To edit the confirmation wording, see `confirmationText()` in
`functions/api/book.js`.

### Rate limit

The confirmation email means a visitor can cause mail to be sent to an address
they typed, so submissions are capped at **5 per IP per hour**, counted in KV.
Over the limit returns HTTP 429 telling them to call instead.

It **fails open**: if KV is unavailable the limit is skipped rather than blocking
a genuine enquiry. Counters are stored as `rl:<ip>` and expire after an hour —
delete one to reset it:

```bash
npx wrangler kv key delete "rl:<ip>" --binding ENQUIRIES --remote
```

### The phone number is duplicated — the build guards it

`functions/api/book.js` can't import `siteconfig.py`, so `PHONE` and `TO` are
hardcoded there. `build.py` compares them against siteconfig and **fails the
build** if they drift, so changing the phone number in one place can't leave the
emails quoting the old one. When you switch to the 480 number, update both.

### How the form fails safely

1. Submission is **stored in KV first**, before any email is attempted
2. Email is **best-effort** — a mail failure is logged but never shown to the visitor
3. If both KV and email fail, the full submission is written to the log
   (`npx wrangler pages deployment tail`) and the visitor is told to call

A misconfiguration can therefore never silently lose a lead.

## Deploying to Cloudflare Pages

Wrangler is installed. Deploy the `site/` directory:

```bash
cd "/Users/mikebruns/Projects/sgflightschool" && npx wrangler pages deploy
```

Config now lives in `wrangler.toml` (project name, output dir, KV binding), so no
flags are needed. Needs a
Cloudflare API token with **Account → Cloudflare Pages → Edit**, either via
`wrangler login` or `CLOUDFLARE_API_TOKEN`.

No build step runs on Cloudflare — the HTML is pre-built and committed, so what
you deploy is exactly what you tested. `_headers` and `_redirects` are picked up
automatically.

**Go live only after the 480 number is in.** Adding the custom domain in Pages
rewrites the apex A records and `www` CNAME away from Squarespace — that's the
real cutover. Once on Pages, proxying (orange cloud) becomes correct.

## What changed from the Squarespace site

- Homepage HTML went from **1.19 MB → 12 KB**
- Every page has a meta description (there were none)
- Instructors moved from `/new-page` → `/instructors`
- The blank `/fleet-tracker` page is gone, redirected to `/aircraft`
- Added LocalBusiness, Course, HowTo and Person structured data
- Location (Falcon Field, Mesa AZ) now appears on every page — it was previously
  mentioned only in passing on the homepage
- Aircraft rates, the $199 discovery flight price, and booking links surfaced
  throughout instead of buried
- The homepage hero photo is now the Superstitions/Salt River aerial; the old one
  was a coastline that isn't in Arizona
- **New FAQ page** with 10 questions and FAQPage structured data, including a
  transparent cost breakdown. This is the page most likely to win search traffic —
  "how much does it cost to learn to fly" is what people actually type

## Owner review needed on the FAQ

The cost figures are estimates built from your published rates plus typical
third-party costs. Read them and correct anything you disagree with — they're in
`FAQ_DATA` in `content.py`:

- Total estimate of **$14,000–16,000** for a PPL, assuming ~60 aircraft hours and
  ~45 instruction hours
- **$800–1,200** quoted for a Phoenix-area DPE checkride fee
- **~$175** for the FAA written test
- **$300–500** for self-paced online ground school

Questions deliberately *not* answered, because I have no basis for them — add them
if you want them covered: financing options, VA/GI Bill eligibility, cancellation
and no-show policy, whether you accept international students, and minimum age you
personally take on as students.
