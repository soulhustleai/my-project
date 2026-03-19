#!/usr/bin/env python3
"""
Make.com Automation Manager — GOD MODE CREDIT
Manages scenarios and webhooks for the Payhip → ConvertKit pipeline.

Usage:
    python scripts/make_webhooks.py --list-scenarios
    python scripts/make_webhooks.py --list-webhooks
    python scripts/make_webhooks.py --setup-payhip-pipeline
    python scripts/make_webhooks.py --test-webhook <webhook_url>
"""

import os
import sys
import json
import argparse
import requests
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent.parent / ".env")

API_KEY = os.getenv("MAKE_API_KEY")

# Make.com API — try multiple regions (US, EU)
REGIONS = ["us1", "us2", "eu1", "eu2"]
BASE_URL = None  # Set after discovering region

HEADERS = {
    "Authorization": f"Token {API_KEY}",
    "Content-Type": "application/json",
}

# ConvertKit integration
CONVERTKIT_API_KEY = os.getenv("CONVERTKIT_API_KEY")
CONVERTKIT_API_SECRET = os.getenv("CONVERTKIT_API_SECRET")
PAYHIP_API_KEY = os.getenv("PAYHIP_API_KEY")


def check_api_key():
    if not API_KEY:
        print("[ERROR] MAKE_API_KEY not set in .env file")
        sys.exit(1)


def discover_region():
    """Find which Make.com region this API key belongs to."""
    global BASE_URL
    for region in REGIONS:
        url = f"https://{region}.make.com/api/v2/users/me"
        try:
            resp = requests.get(url, headers=HEADERS, timeout=10)
            if resp.status_code == 200:
                BASE_URL = f"https://{region}.make.com/api/v2"
                user = resp.json()
                print(f"[MAKE] Region: {region}")
                print(f"[MAKE] User: {user.get('name', 'Unknown')}")
                print(f"[MAKE] Org: {user.get('organizationId', 'N/A')}")
                return user
        except requests.exceptions.RequestException:
            continue

    print("[ERROR] Could not connect to Make.com API. Check your API key.")
    sys.exit(1)


def list_scenarios():
    """List all scenarios in your Make.com account."""
    user = discover_region()
    org_id = user.get("organizationId")

    resp = requests.get(
        f"{BASE_URL}/scenarios",
        headers=HEADERS,
        params={"organizationId": org_id} if org_id else {},
    )
    resp.raise_for_status()
    scenarios = resp.json().get("scenarios", [])

    print(f"\n{'='*60}")
    print(f"  SCENARIOS ({len(scenarios)} total)")
    print(f"{'='*60}")
    for s in scenarios:
        print(f"  ID: {s['id']}")
        print(f"  Name: {s.get('name', 'Untitled')}")
        print(f"  Active: {s.get('isEnabled', False)}")
        print(f"  Last run: {s.get('lastRun', 'Never')}")
        print(f"  ---")
    return scenarios


def list_webhooks():
    """List all webhooks."""
    discover_region()

    resp = requests.get(f"{BASE_URL}/hooks", headers=HEADERS)
    resp.raise_for_status()
    hooks = resp.json().get("hooks", [])

    print(f"\n{'='*60}")
    print(f"  WEBHOOKS ({len(hooks)} total)")
    print(f"{'='*60}")
    for h in hooks:
        print(f"  ID: {h['id']}")
        print(f"  Name: {h.get('name', 'Untitled')}")
        print(f"  URL: {h.get('url', 'N/A')}")
        print(f"  Active: {h.get('enabled', False)}")
        print(f"  ---")
    return hooks


def print_payhip_pipeline_guide():
    """
    Print step-by-step guide for setting up the Payhip → ConvertKit pipeline in Make.com.
    Make.com scenarios are best built visually, so this outputs the exact config to use.
    """
    print(f"""
{'='*70}
  PAYHIP → CONVERTKIT PIPELINE — Make.com Setup Guide
{'='*70}

  This pipeline auto-tags buyers in ConvertKit when they purchase on Payhip.
  Build this as a Make.com scenario (visual builder):

  ┌─────────────────────────────────────────────────────────────────┐
  │  SCENARIO: "Payhip Purchase → ConvertKit Tag + Sequence"       │
  │                                                                 │
  │  TRIGGER: Webhook (Custom)                                     │
  │  ├─ Name: "Payhip Purchase Webhook"                            │
  │  ├─ Paste this webhook URL into Payhip Settings → Webhooks     │
  │  └─ Events: paid, subscription.created                         │
  │                                                                 │
  │  MODULE 2: Router (split by product)                            │
  │  ├─ Route 1: product_name contains "Lead Magnet"               │
  │  │   └─ ConvertKit: Add subscriber                             │
  │  │       ├─ Email: {{{{webhook.email}}}}                       │
  │  │       ├─ Tag: "lead_magnet"                                 │
  │  │       └─ Sequence: "14-Day Welcome"                         │
  │  │                                                              │
  │  ├─ Route 2: product_name contains "Credit Ascension"          │
  │  │   └─ ConvertKit: Add subscriber + tag                       │
  │  │       ├─ Email: {{{{webhook.email}}}}                       │
  │  │       ├─ Tags: ["buyer", "flagship"]                        │
  │  │       └─ Sequence: "Buyer Nurture"                          │
  │  │                                                              │
  │  ├─ Route 3: product_name contains "Business Credit"           │
  │  │   └─ ConvertKit: Add subscriber + tag                       │
  │  │       ├─ Email: {{{{webhook.email}}}}                       │
  │  │       ├─ Tags: ["buyer", "biz_credit"]                      │
  │  │       └─ Sequence: "Ascension Sequence"                     │
  │  │                                                              │
  │  └─ Route 4: Default (any other product)                       │
  │      └─ ConvertKit: Add subscriber + tag                       │
  │          ├─ Email: {{{{webhook.email}}}}                       │
  │          └─ Tags: ["buyer"]                                    │
  │                                                                 │
  │  MODULE 3 (all routes): Google Sheets → Log sale               │
  │  ├─ Spreadsheet: "GOD MODE CREDIT Sales Log"                   │
  │  ├─ Row: date, email, product, amount, source                 │
  │  └─ (Optional — great for tracking)                            │
  └─────────────────────────────────────────────────────────────────┘

  YOUR API KEYS (already in .env):
  ─────────────────────────────────
  Make.com API:    {API_KEY[:12]}...
  ConvertKit V4:   {CONVERTKIT_API_KEY[:12] if CONVERTKIT_API_KEY else 'NOT SET'}...
  ConvertKit V3:   {CONVERTKIT_API_SECRET[:12] if CONVERTKIT_API_SECRET else 'NOT SET'}...
  Payhip:          {PAYHIP_API_KEY[:12] if PAYHIP_API_KEY else 'NOT SET'}...

  PAYHIP WEBHOOK PAYLOAD FORMAT:
  ─────────────────────────────────
  {{
    "event": "paid",
    "email": "customer@email.com",
    "product_name": "Credit Ascension",
    "amount": 4700,           // <-- cents! $47 = 4700
    "currency": "USD",
    "transaction_id": "abc123",
    "affiliate": null
  }}

  Note: Payhip amounts are in CENTS (4700 = $47.00).
  Payhip webhook signature: HMAC-SHA256 (verify in Make.com for security).

  CONVERTKIT TAG STRATEGY:
  ─────────────────────────
  lead_magnet   → Downloaded free PDF
  prospect      → Engaged with emails (opened 3+)
  buyer         → Any paid purchase
  flagship      → Bought Credit Ascension ($47)
  biz_credit    → Bought Business Credit Blueprint ($97)
  ascension     → Bought Zero to $10K bridge product ($97)
  crowned       → Active Crowned Circle member ($37/mo)

  STEP-BY-STEP:
  1. Log into Make.com → Create New Scenario
  2. Add Webhooks → Custom Webhook trigger
  3. Copy the webhook URL Make gives you
  4. Go to Payhip → Settings → Webhooks → Paste the URL
  5. Select events: "paid" and "subscription.created"
  6. Back in Make.com: Add Router module
  7. Add ConvertKit modules to each route (use API key above)
  8. Turn on the scenario
  9. Test with a $0 test product on Payhip

{'='*70}
""")


def print_manychat_webhook_guide():
    """Guide for connecting ManyChat to Make.com via webhook."""
    manychat_key = os.getenv("MANYCHAT_API_KEY", "NOT SET")
    print(f"""
{'='*70}
  MANYCHAT → MAKE.COM → CONVERTKIT — Webhook Bridge
{'='*70}

  When ManyChat captures a lead via DM, send their email to ConvertKit
  through Make.com.

  ManyChat API Key: {manychat_key[:15] if manychat_key != 'NOT SET' else 'NOT SET'}...

  FLOW:
  1. TikTok user comments "LAWS" on your video
  2. ManyChat auto-DMs them the lead magnet link
  3. ManyChat collects their email via DM conversation
  4. ManyChat sends webhook to Make.com with email
  5. Make.com adds subscriber to ConvertKit with tag "lead_magnet"

  MANYCHAT SETUP:
  ─────────────────
  1. Log into ManyChat → Automation → New Flow
  2. Trigger: TikTok Comment → Keyword "LAWS"
  3. Action 1: Send Message → "Here's your free guide: [Payhip link]"
  4. Action 2: Ask for Email → "Drop your email and I'll send the full PDF"
  5. Action 3: External Request → POST to Make.com webhook URL
     Body: {{"email": "{{{{email}}}}", "source": "tiktok_dm", "keyword": "LAWS"}}
  6. Make.com receives → adds to ConvertKit with "lead_magnet" tag

  MANYCHAT DM SEQUENCES TO BUILD:
  ────────────────────────────────
  Sequence 1: "LAWS" → Lead Magnet Delivery
    - Trigger: Comment "LAWS" / "CREDIT" / "FREE"
    - DM: Delivers lead magnet link
    - Collects email → Make.com → ConvertKit

  Sequence 2: "GUIDE" → Flagship Pitch
    - Trigger: Comment "GUIDE" / "EBOOK" / "PLAYBOOK"
    - DM: Teaser about Credit Ascension → link to $47 product

  Sequence 3: Post-Purchase Follow-Up
    - Trigger: Make.com webhook (after Payhip purchase)
    - DM: "Thanks for buying! Here's a bonus tip..."
    - Upsells to next product in ladder

{'='*70}
""")


def main():
    check_api_key()

    parser = argparse.ArgumentParser(description="Make.com Manager for GOD MODE CREDIT")
    parser.add_argument("--list-scenarios", action="store_true", help="List all scenarios")
    parser.add_argument("--list-webhooks", action="store_true", help="List all webhooks")
    parser.add_argument("--setup-payhip-pipeline", action="store_true",
                       help="Print Payhip → ConvertKit pipeline setup guide")
    parser.add_argument("--setup-manychat-bridge", action="store_true",
                       help="Print ManyChat → Make.com → ConvertKit setup guide")

    args = parser.parse_args()

    if args.list_scenarios:
        list_scenarios()
    elif args.list_webhooks:
        list_webhooks()
    elif args.setup_payhip_pipeline:
        print_payhip_pipeline_guide()
    elif args.setup_manychat_bridge:
        print_manychat_webhook_guide()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
