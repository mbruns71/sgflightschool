#!/usr/bin/env python3
"""
Add the three Resend DNS records for send.sgflightschool.com.

Everything lands on SUBDOMAINS. The root domain's MX (Microsoft 365) and SPF are
never touched — this script refuses to write anything at the apex, and verifies
the root mail records are unchanged before and after.

Reads a Cloudflare API token (Zone:Read + DNS:Edit) from ~/.sgfs-cf-token.

    python3 apply-resend-dns.py           # dry run
    python3 apply-resend-dns.py --apply
"""
import json
import os
import subprocess
import sys
import urllib.error
import urllib.request

DOMAIN = "sgflightschool.com"
TOKEN_FILE = os.path.expanduser("~/.sgfs-cf-token")
API = "https://api.cloudflare.com/client/v4"

DKIM = (
    "p=MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDjojLxnaT2vuYui27z3S5Vrr3nyq3tZtB8"
    "wg0JONVhbSlMLyo6YmwKWOpBQNPqHGV3J1A6HPuAvzzArZTtaLKFpy41rBKbuwRx3Qoj3TKj/"
    "uXGbZ7lYa9GeC0302YMvTncEeHg+zFL2sQtyMUQARk6eJQox+MLdEYh4uppvZ06MQIDAQAB"
)

# (type, name relative to zone, content, extra)
RECORDS = [
    ("TXT", "resend._domainkey.send", DKIM, {}),
    ("MX", "send.send", "feedback-smtp.us-east-1.amazonses.com", {"priority": 10}),
    ("TXT", "send.send", "v=spf1 include:amazonses.com ~all", {}),
]

# Guard: these must be identical before and after.
PROTECTED = {
    "MX @": "sgflightschool-com.mail.protection.outlook.com",
    "TXT @ spf": "v=spf1 include:secureserver.net -all",
}


def dig(name, rtype):
    out = subprocess.run(
        ["dig", "+short", name, rtype], capture_output=True, text=True
    ).stdout
    return [l.strip() for l in out.splitlines() if l.strip()]


def snapshot_root():
    mx = " ".join(dig(DOMAIN, "MX"))
    spf = " ".join(x for x in dig(DOMAIN, "TXT") if "spf1" in x)
    return {"MX @": mx, "TXT @ spf": spf}


def check_root(before=None):
    now = snapshot_root()
    ok = True
    for k, expected in PROTECTED.items():
        if expected not in now[k]:
            print(f"  !! ROOT {k} UNEXPECTED: {now[k]!r}")
            ok = False
    if before and before != now:
        print("  !! ROOT MAIL RECORDS CHANGED")
        print(f"     before: {before}")
        print(f"     after:  {now}")
        ok = False
    return ok, now


def token():
    if not os.path.exists(TOKEN_FILE):
        sys.exit(
            f"No token at {TOKEN_FILE}.\n"
            "Create one (Zone:Read + DNS:Edit, scoped to sgflightschool.com), then:\n"
            "  read -rs T && printf '%s' \"$T\" > ~/.sgfs-cf-token "
            "&& chmod 600 ~/.sgfs-cf-token && unset T"
        )
    t = open(TOKEN_FILE).read().strip()
    if not t:
        sys.exit(f"{TOKEN_FILE} is empty.")
    return t


def call(method, path, body=None, tok=None):
    req = urllib.request.Request(
        API + path,
        method=method,
        data=json.dumps(body).encode() if body is not None else None,
        headers={"Authorization": f"Bearer {tok}", "Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        try:
            errs = json.loads(e.read()).get("errors", [])
            msg = "; ".join(f"{x.get('code')}: {x.get('message')}" for x in errs)
        except Exception:
            msg = f"HTTP {e.code}"
        sys.exit(f"Cloudflare API error on {method} {path}\n  {msg}")


def main():
    apply = "--apply" in sys.argv
    tok = token()

    print("=== root mail records before ===")
    ok, before = check_root()
    for k, v in before.items():
        print(f"  {k}: {v}")
    if not ok:
        sys.exit("Refusing to continue — root mail records are not as expected.")
    print()

    zid = call("GET", f"/zones?name={DOMAIN}", tok=tok)["result"][0]["id"]
    existing = call("GET", f"/zones/{zid}/dns_records?per_page=200", tok=tok)["result"]

    plan = []
    for rtype, name, content, extra in RECORDS:
        fqdn = f"{name}.{DOMAIN}"
        # Hard guard: never write at the apex.
        if fqdn == DOMAIN or name in ("@", ""):
            sys.exit(f"Refusing to write an apex record: {rtype} {fqdn}")
        match = next(
            (
                r
                for r in existing
                if r["type"] == rtype
                and r["name"] == fqdn
                and (rtype != "TXT" or r["content"].strip('"')[:24] == content[:24])
            ),
            None,
        )
        plan.append((rtype, fqdn, content, extra, match))

    for rtype, fqdn, content, extra, match in plan:
        action = "OK    " if match and match["content"].strip('"') == content else (
            "UPDATE" if match else "CREATE"
        )
        print(f"  {action} {rtype:4} {fqdn:44} {content[:46]}")

    todo = [p for p in plan if not (p[4] and p[4]["content"].strip('"') == p[2])]
    print()
    if not todo:
        print("Zone already matches. Nothing to do.")
    elif not apply:
        print(f"DRY RUN — {len(todo)} record(s) to write. Re-run with --apply.")
        return
    else:
        for rtype, fqdn, content, extra, match in todo:
            payload = {"type": rtype, "name": fqdn, "content": content, "ttl": 1}
            payload.update(extra)
            if match:
                call("PUT", f"/zones/{zid}/dns_records/{match['id']}", payload, tok=tok)
                print(f"  updated {rtype} {fqdn}")
            else:
                call("POST", f"/zones/{zid}/dns_records", payload, tok=tok)
                print(f"  created {rtype} {fqdn}")

    print("\n=== root mail records after ===")
    ok, _ = check_root(before)
    print("  unchanged — Microsoft 365 mail is safe" if ok else "  PROBLEM, see above")


if __name__ == "__main__":
    main()
