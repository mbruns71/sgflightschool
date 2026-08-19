#!/bin/bash
# Migration checkpoint verifier for sgflightschool.com.
# Run at each phase. Green = expected, red = needs attention.
D=sgflightschool.com
G="\033[32m"; R="\033[31m"; Y="\033[33m"; N="\033[0m"

pass(){ printf "  ${G}PASS${N}  %s\n" "$1"; }
fail(){ printf "  ${R}FAIL${N}  %s\n" "$1"; }
warn(){ printf "  ${Y}WARN${N}  %s\n" "$1"; }

echo
echo "=============================================="
echo " sgflightschool.com — migration check"
echo " $(date)"
echo "=============================================="

echo
echo "-- Nameservers --"
NS=$(dig $D NS +short | sort | tr '\n' ' ')
echo "  current: $NS"
if echo "$NS" | grep -q "ns.cloudflare.com"; then
  pass "on Cloudflare nameservers"
  ON_CF=1
elif echo "$NS" | grep -q "squarespacedns"; then
  warn "still on Squarespace nameservers (expected before Phase 1 step 5)"
  ON_CF=0
else
  fail "unrecognized nameservers"
  ON_CF=0
fi

echo
echo "-- Website --"
A=$(dig $D A +short | sort | tr '\n' ' ')
echo "  apex A: $A"
WWW=$(dig www.$D CNAME +short)
echo "  www CNAME: ${WWW:-none}"
CODE=$(curl -sL -o /dev/null -w "%{http_code}" --max-time 15 https://www.$D)
[ "$CODE" = "200" ] && pass "https://www.$D returns 200" || fail "https://www.$D returned $CODE"
REDIR=$(curl -sI --max-time 15 https://$D | awk '/^[Ll]ocation:/{print $2}' | tr -d '\r')
[ -n "$REDIR" ] && pass "apex redirects to $REDIR" || warn "apex did not redirect"

echo
echo "-- Email (the records that must never break) --"
MX=$(dig $D MX +short)
if echo "$MX" | grep -q "mail.protection.outlook.com"; then
  pass "MX -> $MX"
else
  fail "MX missing or wrong: ${MX:-none}"
fi

SPF=$(dig $D TXT +short | grep "v=spf1")
if echo "$SPF" | grep -q "secureserver.net"; then
  pass "SPF present: $SPF"
else
  fail "SPF missing or changed: ${SPF:-none}"
fi

MSV=$(dig $D TXT +short | grep -i "onmicrosoft.com")
if [ -n "$MSV" ]; then
  pass "M365 domain verification TXT present"
else
  fail "M365 verification TXT missing: expected NETORGFT17174974.onmicrosoft.com"
fi

echo
echo "-- Email hardening (added during Phase 1) --"
DMARC=$(dig _dmarc.$D TXT +short)
if [ -n "$DMARC" ]; then pass "DMARC: $DMARC"; else warn "no DMARC record yet"; fi

AD=$(dig autodiscover.$D CNAME +short)
if [ -n "$AD" ]; then pass "autodiscover -> $AD"; else warn "no autodiscover CNAME yet"; fi

for s in selector1 selector2; do
  K=$(dig $s._domainkey.$D CNAME +short)
  if [ -n "$K" ]; then pass "DKIM $s -> $K"; else warn "no DKIM $s CNAME yet"; fi
done

echo
echo "-- Registrar --"
REG=$(whois $D 2>/dev/null | grep -i "^   Registrar:" | head -1 | sed 's/^[^:]*: *//')
echo "  registrar: ${REG:-unknown}"
if whois $D 2>/dev/null | grep -qi "clientTransferProhibited"; then
  warn "transfer lock ON (must be off to start Phase 2)"
else
  pass "transfer lock off"
fi
EXP=$(whois $D 2>/dev/null | grep -i "Registry Expiry Date" | head -1 | sed 's/^[^:]*: *//')
echo "  expires: ${EXP:-unknown}"

echo
echo "=============================================="
echo
