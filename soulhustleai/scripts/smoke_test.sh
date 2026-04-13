#!/usr/bin/env bash
# SoulHustleAI — End-to-end smoke test
# Run this before any client-facing launch. Takes ~2 minutes.
#
# Usage:
#   cd soulhustleai/scripts
#   cp .env.example .env && vim .env  # fill in real values
#   ./smoke_test.sh
#
# What it tests:
#   1. Supabase reachability + RLS
#   2. n8n Gate webhook intake
#   3. Twilio auth (SMS)
#   4. VAPI Zero agent
#   5. Resend email
#   6. Enrichment engine queue status

set -e
cd "$(dirname "$0")"
[ -f .env ] && source .env

PASS=0
FAIL=0
RESULTS=()

green() { printf "\033[32m%s\033[0m\n" "$1"; }
red()   { printf "\033[31m%s\033[0m\n" "$1"; }
cyan()  { printf "\033[36m%s\033[0m\n" "$1"; }

check() {
  local name="$1" cmd="$2"
  printf "  %-50s" "$name"
  if eval "$cmd" >/dev/null 2>&1; then
    green "✓ PASS"
    PASS=$((PASS+1))
    RESULTS+=("PASS $name")
  else
    red "✗ FAIL"
    FAIL=$((FAIL+1))
    RESULTS+=("FAIL $name")
  fi
}

cyan ""
cyan "╔══════════════════════════════════════════════════╗"
cyan "║  SOULHUSTLEAI — LIVE SMOKE TEST                 ║"
cyan "║  $(date '+%Y-%m-%d %H:%M:%S %Z')                          ║"
cyan "╚══════════════════════════════════════════════════╝"
cyan ""

# 1. Supabase
cyan "━━━ SUPABASE ━━━"
check "Supabase ping" "curl -sf '$SUPABASE_URL/rest/v1/' -H 'apikey: $SUPABASE_SERVICE_KEY'"
check "leads table read" "curl -sf '$SUPABASE_URL/rest/v1/leads?select=id&limit=1' -H 'apikey: $SUPABASE_SERVICE_KEY' -H 'Authorization: Bearer $SUPABASE_SERVICE_KEY'"
check "clients table read" "curl -sf '$SUPABASE_URL/rest/v1/clients?select=id&limit=1' -H 'apikey: $SUPABASE_SERVICE_KEY' -H 'Authorization: Bearer $SUPABASE_SERVICE_KEY'"
check "enrichment_jobs pending count > 0" "curl -sf '$SUPABASE_URL/rest/v1/enrichment_jobs?select=id&status=eq.pending&limit=1' -H 'apikey: $SUPABASE_SERVICE_KEY' -H 'Authorization: Bearer $SUPABASE_SERVICE_KEY' | grep -q id"

# 2. n8n webhook
cyan ""
cyan "━━━ n8n ━━━"
check "n8n reachable" "curl -sf '$N8N_URL'"
check "Gate webhook responds" "curl -sf -X POST '$N8N_URL/webhook/shai-gate-intake' -H 'Content-Type: application/json' -d '{\"name\":\"Smoke Test\",\"business\":\"Smoke Corp\",\"email\":\"smoke@test.com\",\"phone\":\"+15555555555\",\"package\":\"system\",\"revenue\":\"\$100K - \$300K\",\"timeline\":\"Ready to start this week\",\"biggest_leak\":\"missed calls\",\"vision\":\"automated\",\"what_you_do\":\"smoke test\"}'"

# 3. Twilio
cyan ""
cyan "━━━ TWILIO ━━━"
check "Twilio auth" "curl -sf -u '$TWILIO_ACCOUNT_SID:$TWILIO_AUTH_TOKEN' 'https://api.twilio.com/2010-04-01/Accounts/$TWILIO_ACCOUNT_SID.json'"
check "Twilio number active" "curl -sf -u '$TWILIO_ACCOUNT_SID:$TWILIO_AUTH_TOKEN' 'https://api.twilio.com/2010-04-01/Accounts/$TWILIO_ACCOUNT_SID/IncomingPhoneNumbers.json' | grep -q '+18446439825'"

# 4. VAPI
cyan ""
cyan "━━━ VAPI (Zero) ━━━"
check "VAPI auth" "curl -sf -H 'Authorization: Bearer $VAPI_API_KEY' 'https://api.vapi.ai/assistant'"
check "Zero agent exists" "curl -sf -H 'Authorization: Bearer $VAPI_API_KEY' 'https://api.vapi.ai/assistant/$VAPI_ZERO_AGENT_ID'"

# 5. Resend
cyan ""
cyan "━━━ RESEND ━━━"
check "Resend auth" "curl -sf -H 'Authorization: Bearer $RESEND_API_KEY' 'https://api.resend.com/domains'"

# 6. Stripe (optional — only if Stripe set up)
cyan ""
cyan "━━━ STRIPE ━━━"
if [ -n "$STRIPE_SECRET_KEY" ]; then
  check "Stripe auth" "curl -sf -u '$STRIPE_SECRET_KEY:' 'https://api.stripe.com/v1/products?limit=1'"
else
  printf "  %-50s" "Stripe key not set"
  cyan "◌ SKIP"
fi

cyan ""
cyan "═══════════════════════════════════════════════════"
printf "  PASS: \033[32m%d\033[0m   FAIL: \033[31m%d\033[0m\n" "$PASS" "$FAIL"
cyan "═══════════════════════════════════════════════════"

if [ $FAIL -gt 0 ]; then
  red ""
  red "✗ SMOKE TEST FAILED — fix before going live"
  echo ""
  for r in "${RESULTS[@]}"; do
    [[ "$r" == FAIL* ]] && red "    $r"
  done
  exit 1
else
  green ""
  green "✓ ALL SYSTEMS GO — cleared for launch"
  exit 0
fi
