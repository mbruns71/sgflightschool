#!/usr/bin/env python3
"""
Populate the Cloudflare zone for sgflightschool.com.

Reads a scoped API token from ~/.sgfs-cf-token (never printed, never logged).

Safe by design:
  * Defaults to a dry run. Nothing changes without --apply.
  * While the domain's nameservers still point at Squarespace, the Cloudflare
    zone is not authoritative, so populating it cannot affect live traffic.
  * Never deletes records. It creates what's missing and updates what differs.

Usage:
    python3 apply-dns.py            # dry run — show the plan
    python3 apply-dns.py --apply    # make the changes
"""
import json
import os
import sys
import urllib.error
import urllib.request

DOMAIN = "sgflightschool.com"
TOKEN_FILE = os.path.expanduser("~/.sgfs-cf-token")
API = "https://api.cloudflare.com/client/v4"

# Desired zone. proxied=False everywhere: Squarespace issues its own TLS cert,
# and proxying breaks their validation until we move to Cloudflare Pages.
DESIRED = [
    # (type, name, content, extra)
    ("A", "@", "198.185.159.144", {"proxied": False}),
    ("A", "@", "198.185.159.145", {"proxied": False}),
    ("A", "@", "198.49.23.144", {"proxied": False}),
    ("A", "@", "198.49.23.145", {"proxied": False}),
    ("CNAME", "www", "ext-sq.squarespace.com", {"proxied": False}),
    ("MX", "@", "sgflightschool-com.mail.protection.outlook.com", {"priority": 0}),
    ("TXT", "@", "NETORGFT17174974.onmicrosoft.com", {}),
    ("TXT", "@", "v=spf1 include:secureserver.net -all", {}),
    # --- email hardening, new ---
    ("TXT", "_dmarc",
     "v=DMARC1; p=none; rua=mailto:info@sgflightschool.com; fo=1", {}),
    ("CNAME", "autodiscover", "autodiscover.outlook.com", {"proxied": False}),
    # DKIM targets as issued by the Microsoft Defender portal on 2026-08-16.
    # Microsoft now uses the q-v1.dkim.mail.microsoft host, NOT the older
    # <tenant>.onmicrosoft.com pattern. Always take these from the portal.
    ("CNAME", "selector1._domainkey",
     "selector1-sgflightschool-com._domainkey.NETORGFT17174974.q-v1.dkim.mail.microsoft",
     {"proxied": False}),
    ("CNAME", "selector2._domainkey",
     "selector2-sgflightschool-com._domainkey.NETORGFT17174974.q-v1.dkim.mail.microsoft",
     {"proxied": False}),
]


def token():
    if not os.path.exists(TOKEN_FILE):
        sys.exit(
            f"No token at {TOKEN_FILE}.\n"
            "Create one (Zone:Read + DNS:Edit, scoped to this zone only), then:\n"
            "  read -rs CF_TOKEN && printf '%s' \"$CF_TOKEN\" > ~/.sgfs-cf-token "
            "&& chmod 600 ~/.sgfs-cf-token && unset CF_TOKEN"
        )
    with open(TOKEN_FILE) as f:
        t = f.read().strip()
    if not t:
        sys.exit(f"{TOKEN_FILE} is empty.")
    return t


def call(method, path, body=None, tok=None):
    req = urllib.request.Request(
        API + path,
        method=method,
        data=json.dumps(body).encode() if body is not None else None,
        headers={
            "Authorization": f"Bearer {tok}",
            "Content-Type": "application/json",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        payload = e.read().decode()
        # Never echo the token; surface only Cloudflare's own error text.
        try:
            errs = json.loads(payload).get("errors", [])
            msg = "; ".join(f"{x.get('code')}: {x.get('message')}" for x in errs)
        except Exception:
            msg = payload[:300]
        sys.exit(f"Cloudflare API error {e.code} on {method} {path}\n  {msg}")


def fqdn(name):
    return DOMAIN if name == "@" else f"{name}.{DOMAIN}"


def main():
    apply = "--apply" in sys.argv
    tok = token()

    zones = call("GET", f"/zones?name={DOMAIN}", tok=tok)["result"]
    if not zones:
        sys.exit(
            f"Zone {DOMAIN} not found on this account.\n"
            "Add the site in the Cloudflare dashboard first (Add a site -> Free)."
        )
    z = zones[0]
    zid = z["id"]

    print(f"Zone:   {DOMAIN}")
    print(f"Status: {z['status']}")
    ns = z.get("name_servers") or []
    if ns:
        print("Cloudflare assigned nameservers:")
        for n in ns:
            print(f"  {n}")
    print()

    existing = call("GET", f"/zones/{zid}/dns_records?per_page=200", tok=tok)["result"]

    creates, updates, oks = [], [], []
    for rtype, name, content, extra in DESIRED:
        target = fqdn(name)
        match = None
        for r in existing:
            if r["type"] != rtype or r["name"] != target:
                continue
            # For multi-value sets (A, MX, TXT) match on content; for CNAME the
            # name is unique so match on name alone.
            if rtype == "CNAME" or r["content"].strip('"') == content:
                match = r
                break

        payload = {"type": rtype, "name": target, "content": content, "ttl": 1}
        payload.update(extra)

        if match is None:
            creates.append((rtype, target, content, payload))
        else:
            differs = (
                match["content"].strip('"') != content
                or ("proxied" in extra and match.get("proxied") != extra["proxied"])
                or ("priority" in extra and match.get("priority") != extra["priority"])
            )
            if differs:
                updates.append((rtype, target, content, match["id"], payload,
                                match["content"], match.get("proxied")))
            else:
                oks.append((rtype, target, content))

    for rtype, target, content in oks:
        print(f"  OK      {rtype:6} {target:45} {content[:60]}")
    for rtype, target, content, _p in creates:
        print(f"  CREATE  {rtype:6} {target:45} {content[:60]}")
    for rtype, target, content, _i, _p, old, oldprox in updates:
        old = old.strip('"')
        if old != content:
            what = f"{old[:38]} -> {content[:38]}"
        elif oldprox:
            what = f"{content[:34]}  [ORANGE -> grey: un-proxy]"
        else:
            what = content[:60]
        print(f"  UPDATE  {rtype:6} {target:45} {what}")

    # Warn about anything present that we didn't ask for — never auto-delete.
    wanted = {(t, fqdn(n)) for t, n, _c, _e in DESIRED}
    extras = [r for r in existing if (r["type"], r["name"]) not in wanted]
    if extras:
        print("\n  Records in the zone that are not in the migration plan")
        print("  (left untouched — review them yourself):")
        for r in extras:
            print(f"    {r['type']:6} {r['name']:45} {str(r['content'])[:60]}")

    print()
    if not creates and not updates:
        print("Zone already matches the plan. Nothing to do.")
        return

    if not apply:
        print(f"DRY RUN — {len(creates)} to create, {len(updates)} to update.")
        print("Re-run with --apply to make these changes.")
        return

    for rtype, target, content, payload in creates:
        call("POST", f"/zones/{zid}/dns_records", payload, tok=tok)
        print(f"  created {rtype} {target}")
    for rtype, target, content, rid, payload, _o, _op in updates:
        call("PUT", f"/zones/{zid}/dns_records/{rid}", payload, tok=tok)
        print(f"  updated {rtype} {target}")

    print("\nDone. Verify with: ./verify-dns.sh")
    print("Nameservers are still at Squarespace — nothing is live yet.")


if __name__ == "__main__":
    main()
