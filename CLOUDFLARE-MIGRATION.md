# sgflightschool.com → Cloudflare Migration Runbook

**Prepared 2026-08-16. Phases 1 and 2 COMPLETED 2026-08-16.**

## Completion record

| | Before | After |
|---|---|---|
| Registrar | GoDaddy | **Cloudflare, Inc.** (IANA 1910) |
| Expiry | 2027-08-16 | **2028-08-16** |
| Nameservers | Squarespace / NS1 | **hal.ns.cloudflare.com, journey.ns.cloudflare.com** |
| Website | Squarespace | Squarespace (unchanged, cert intact) |
| Email | M365, SPF only | M365, **SPF + DKIM + DMARC all passing** |

Verified end-to-end 2026-08-16: live message from `info@sgflightschool.com` to an
external Gmail account returned `SPF: PASS`, `DKIM: PASS with domain
sgflightschool.com`, `DMARC: PASS`.

### Things that went wrong, and why

- **Cloudflare's scan imported all 5 web records orange-clouded (proxied).** Left
  that way, Squarespace's TLS cert validation would have broken on cutover. All
  were forced to DNS-only before the nameserver switch.
- **The DKIM CNAME targets were initially wrong.** Microsoft moved from the legacy
  `<tenant>.onmicrosoft.com` pattern to `q-v1.dkim.mail.microsoft`. Always take the
  values from the Defender portal; never derive them.
- **The Defender portal displayed "undefined" for both selectors.** Cosmetic bug —
  the keys were published and signing correctly. Verify with `dig`, not the UI.
- **The first transfer attempt was auto-rejected in 72 seconds** with "express
  written objection." Cause was GoDaddy **Domain Protection**, which is separate
  from the registry transfer lock and must be downgraded to None. It lives in the
  Protection Plan column of the Domain Portfolio list, not in Domain Settings.

### Remaining

- Re-lock the domain at Cloudflare (Cloudflare does not auto-lock post-transfer)
- Turn off GoDaddy auto-renew **on the domain only** — Microsoft 365 stays with
  GoDaddy and must keep renewing to preserve the two mailboxes
- Tighten DMARC from `p=none` to `p=quarantine` after 2–4 weeks of clean reports

---

The original runbook follows. Phases 1 and 2 are done; Phase 3 is optional.

---

## Starting state

| Item | Current |
|---|---|
| Registrar | GoDaddy (expires 2027-08-16) |
| DNS | Squarespace (`ns01–04.squarespacedns.com`) |
| Website | Squarespace |
| Email | Microsoft 365, billed through GoDaddy (tenant `NETORGFT17174974.onmicrosoft.com`) |

### Complete current zone — all 5 record sets

| Type | Name | Value | Purpose |
|---|---|---|---|
| A | `@` | `198.185.159.144` | Squarespace |
| A | `@` | `198.185.159.145` | Squarespace |
| A | `@` | `198.49.23.144` | Squarespace |
| A | `@` | `198.49.23.145` | Squarespace |
| CNAME | `www` | `ext-sq.squarespace.com` | Squarespace |
| MX | `@` | `sgflightschool-com.mail.protection.outlook.com` (priority 0) | **Email — do not lose** |
| TXT | `@` | `NETORGFT17174974.onmicrosoft.com` | M365 domain verification |
| TXT | `@` | `v=spf1 include:secureserver.net -all` | SPF |

> The SPF record is correct as-is. `secureserver.net` chains through to
> `spf.protection.outlook.com`, so Microsoft 365 mail passes SPF. Don't "fix" it.

---

## Phase 1 — Move DNS to Cloudflare

**Risk: this is the step that can break email.** Verify the MX and both TXT records
before changing nameservers.

1. In Cloudflare, **Add a site** → `sgflightschool.com` → **Free** plan.
   Cloudflare scans the existing zone and imports what it finds.

2. **Verify all 8 records above imported correctly.** Add anything missing by hand.
   Pay particular attention to the MX record and both TXT records.

3. **Set every record to "DNS only" (grey cloud), not proxied (orange cloud).**

   This matters. While the site is hosted on Squarespace, Squarespace issues and
   renews its own TLS certificate. Proxying through Cloudflare blocks that
   validation and causes certificate failures and redirect loops. Grey-cloud
   everything for now.

4. **Add the three missing email records** (see next section).

5. Cloudflare shows you two assigned nameservers, e.g. `xxx.ns.cloudflare.com`.
   In **GoDaddy → Domain Settings → Nameservers → Change**, replace all
   Squarespace nameservers with the two Cloudflare ones.

6. Wait for Cloudflare to report the zone **Active** (usually 15 minutes to a few
   hours; the registry TTL is what governs).

7. **Verify before moving on:**

   ```bash
   dig sgflightschool.com NS +short && dig sgflightschool.com MX +short && dig www.sgflightschool.com CNAME +short
   ```

   Then send a test email *to* `info@sgflightschool.com` from an outside account
   and confirm it arrives, and send one *from* it and confirm delivery.

---

## Email records to add while you're in there

Your domain currently has **no DMARC record**, which means anyone can spoof
`@sgflightschool.com` and receiving servers have no instruction on what to do
about it. Add these in Cloudflare DNS:

| Type | Name | Value |
|---|---|---|
| TXT | `_dmarc` | `v=DMARC1; p=none; rua=mailto:info@sgflightschool.com; fo=1` |
| CNAME | `autodiscover` | `autodiscover.outlook.com` |
| CNAME | `selector1._domainkey` | `selector1-sgflightschool-com._domainkey.NETORGFT17174974.onmicrosoft.com` |
| CNAME | `selector2._domainkey` | `selector2-sgflightschool-com._domainkey.NETORGFT17174974.onmicrosoft.com` |

Notes:

- **DMARC** starts at `p=none`, which only monitors — it changes nothing about
  delivery. Run it for 2–4 weeks, read the reports, then tighten to
  `p=quarantine` and eventually `p=reject`.
- **DKIM**: the two `selector` CNAMEs follow Microsoft's standard naming pattern.
  Confirm the exact target hostnames in **Microsoft 365 Defender → Policies →
  Email authentication → DKIM** before adding, then enable signing for the domain
  there. DKIM does nothing until you flip it on in that portal.
- **autodiscover** speeds up Outlook client setup on desktop and mobile.

---

## Phase 2 — Transfer the registrar to Cloudflare

Only after Phase 1 shows **Active**. Cloudflare Registrar requires the domain to
already use Cloudflare DNS.

Eligibility is fine: the domain was created 2024-08-15, well past the 60-day
minimum, and hasn't been transferred recently.

1. **GoDaddy → Domain Settings:**
   - Turn **off** the domain lock (`clientTransferProhibited` is currently set).
   - Request the **authorization / EPP code** — GoDaddy emails it to the registrant.
2. **Cloudflare → Domain Registration → Transfer Domains**, select
   `sgflightschool.com`, paste the auth code, and pay for one year (~$10 at cost).
3. Approve the confirmation email. You can accelerate by approving the transfer
   from GoDaddy's side rather than waiting out the 5-day auto-approval.
4. The one year you pay **adds to** the existing expiry: 2027-08-16 → 2028-08-16.

### What the transfer does *not* affect

- **Your Microsoft 365 email keeps working.** It's a separate GoDaddy
  subscription, not part of the domain registration, and it does not cancel when
  the domain moves. Your mailboxes, billing, and admin portal stay where they are.
- Nothing about the website — DNS already points wherever you set it in Phase 1.

### What it does change

- GoDaddy's "Domain Connect" auto-DNS management stops applying. Irrelevant once
  DNS lives at Cloudflare, but worth knowing: if you later add a service that
  offers "connect automatically with GoDaddy," you'll add its records manually
  in Cloudflare instead.
- WHOIS privacy is included free at Cloudflare.

---

## Phase 3 — Optional: move hosting to Cloudflare Pages

Only if you decide to retire Squarespace after reviewing the prototype in
`preview-standalone/`.

1. Push this project to a Git repo (or use `wrangler pages deploy site`).
2. Cloudflare → **Workers & Pages → Create → Pages**. Build output directory:
   `site`. No build command needed — the HTML is pre-built and committed.
3. Deploy first to the free `*.pages.dev` URL and click through every page.
4. When satisfied, add the custom domain in Pages for both `sgflightschool.com`
   and `www.sgflightschool.com`. Cloudflare replaces the Squarespace A/CNAME
   records automatically and issues certificates.
5. **Then** you can turn the orange cloud on — with Pages, proxying is correct.
6. Cancel Squarespace only after the new site has served live traffic for a few
   days. Keep the Squarespace export as a backup.

Redirects from the old URLs are already configured in `site/_redirects`
(`/home` → `/`, `/new-page` → `/instructors`, `/fleet-tracker` → `/aircraft`).

---

## Rollback

At any point in Phase 1, revert by setting the GoDaddy nameservers back to:

```
ns01.squarespacedns.com
ns02.squarespacedns.com
ns03.squarespacedns.com
ns04.squarespacedns.com
```

Propagation takes up to a few hours. Phase 2 is harder to reverse — a registrar
transfer can't be undone for 60 days — so be confident DNS and email are healthy
before starting it.
