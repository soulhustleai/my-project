#!/usr/bin/env python3
"""
ManyChat DM Automation Manager — GOD MODE CREDIT
Manages subscriber data and DM flows via ManyChat API.

Usage:
    python scripts/manychat_setup.py --get-info
    python scripts/manychat_setup.py --list-tags
    python scripts/manychat_setup.py --create-tag "gmc_lead"
    python scripts/manychat_setup.py --list-flows
    python scripts/manychat_setup.py --setup-guide
"""

import os
import sys
import json
import argparse
import requests
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent.parent / ".env")

API_KEY = os.getenv("MANYCHAT_API_KEY")
BASE_URL = "https://api.manychat.com/fb"

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
}


def check_api_key():
    if not API_KEY:
        print("[ERROR] MANYCHAT_API_KEY not set in .env file")
        sys.exit(1)


def get_page_info():
    """Get connected page info."""
    resp = requests.get(f"{BASE_URL}/page/getInfo", headers=HEADERS)
    resp.raise_for_status()
    data = resp.json().get("data", {})
    print(f"\n[MANYCHAT] Connected Page:")
    print(f"  Name: {data.get('name', 'N/A')}")
    print(f"  ID: {data.get('id', 'N/A')}")
    print(f"  Category: {data.get('category', 'N/A')}")
    return data


def list_tags():
    """List all tags in your ManyChat account."""
    resp = requests.get(f"{BASE_URL}/page/getTags", headers=HEADERS)
    resp.raise_for_status()
    tags = resp.json().get("data", [])

    print(f"\n{'='*50}")
    print(f"  TAGS ({len(tags)} total)")
    print(f"{'='*50}")
    for tag in tags:
        print(f"  ID: {tag['id']} | Name: {tag['name']}")
    return tags


def create_tag(tag_name):
    """Create a new tag."""
    resp = requests.post(
        f"{BASE_URL}/page/createTag",
        headers=HEADERS,
        json={"name": tag_name},
    )
    resp.raise_for_status()
    data = resp.json()
    if data.get("status") == "success":
        print(f"[MANYCHAT] Tag created: {tag_name} (ID: {data.get('data', {}).get('id')})")
    else:
        print(f"[MANYCHAT] Failed: {data}")
    return data


def list_custom_fields():
    """List custom fields (for storing email, product purchased, etc.)."""
    resp = requests.get(f"{BASE_URL}/page/getCustomFields", headers=HEADERS)
    resp.raise_for_status()
    fields = resp.json().get("data", [])

    print(f"\n{'='*50}")
    print(f"  CUSTOM FIELDS ({len(fields)} total)")
    print(f"{'='*50}")
    for f in fields:
        print(f"  ID: {f['id']} | Name: {f['name']} | Type: {f.get('type', 'N/A')}")
    return fields


def list_flows():
    """List all automation flows."""
    resp = requests.get(f"{BASE_URL}/page/getFlows", headers=HEADERS)
    resp.raise_for_status()
    flows = resp.json().get("data", [])

    print(f"\n{'='*50}")
    print(f"  FLOWS ({len(flows)} total)")
    print(f"{'='*50}")
    for fl in flows:
        print(f"  ID: {fl.get('id', 'N/A')}")
        print(f"  Name: {fl.get('name', 'Untitled')}")
        print(f"  Status: {'Active' if fl.get('is_active') else 'Inactive'}")
        print(f"  ---")
    return flows


def setup_required_tags():
    """Create all tags needed for the GOD MODE CREDIT pipeline."""
    required_tags = [
        "gmc_lead",           # Downloaded lead magnet
        "gmc_prospect",       # Engaged (opened emails, clicked)
        "gmc_buyer",          # Any paid purchase
        "gmc_flagship",       # Bought Credit Ascension ($47)
        "gmc_biz_credit",     # Bought Business Credit Blueprint
        "gmc_crowned_circle", # Active membership
        "tiktok_lead",        # Came from TikTok
        "instagram_lead",     # Came from Instagram
        "keyword_laws",       # Triggered by "LAWS" keyword
        "keyword_guide",      # Triggered by "GUIDE" keyword
        "keyword_credit",     # Triggered by "CREDIT" keyword
    ]

    print(f"\n[MANYCHAT] Creating {len(required_tags)} tags for GOD MODE CREDIT pipeline...")
    for tag_name in required_tags:
        try:
            create_tag(tag_name)
        except requests.exceptions.HTTPError as e:
            if "already exists" in str(e.response.text).lower():
                print(f"  [SKIP] Tag '{tag_name}' already exists")
            else:
                print(f"  [ERROR] Tag '{tag_name}': {e}")


def print_setup_guide():
    """Print the complete ManyChat setup guide for GOD MODE CREDIT."""
    print(f"""
{'='*70}
  MANYCHAT DM AUTOMATION — GOD MODE CREDIT Setup Guide
{'='*70}

  OVERVIEW:
  Someone comments a keyword on TikTok/IG → ManyChat auto-DMs them →
  Collects email → Sends to ConvertKit via Make.com → Nurture sequence

  ═══════════════════════════════════════════════════════════════
  FLOW 1: "LAWS" KEYWORD → LEAD MAGNET DELIVERY
  ═══════════════════════════════════════════════════════════════

  TRIGGER: User comments "LAWS" (or "LAW", "FEDERAL", "FREE")

  Message 1 (immediate):
  ───────────────────────
  "You already know something most people never figure out 👑

  Here's the guide — 5 Federal Laws Banks Hope You Never Read:
  [PAYHIP LINK TO FREE LEAD MAGNET]

  This isn't just information. It's ammunition.
  Federal law is on YOUR side. Most people just don't know how to use it."

  Message 2 (+30 seconds):
  ─────────────────────────
  "Real talk — want me to send you the full breakdown straight
  to your inbox? Drop your email below and I'll send it over 📧"

  [COLLECT EMAIL via User Input]

  Message 3 (after email collected):
  ────────────────────────────────────
  "Locked in 🔒 Check your inbox.

  While you're here — if you want the FULL system
  (dispute letters, secret lenders list, AI tools, 90-day plan)...

  Credit Ascension has everything: [PAYHIP $47 LINK]

  No pressure. The free guide alone is powerful. But if you want
  to go from 300 to 750+... that's what Ascension is for."

  ACTION: POST email to Make.com webhook
  → Make.com → ConvertKit (tag: lead_magnet, tiktok_lead)

  ═══════════════════════════════════════════════════════════════
  FLOW 2: "GUIDE" KEYWORD → FLAGSHIP PITCH
  ═══════════════════════════════════════════════════════════════

  TRIGGER: User comments "GUIDE" (or "EBOOK", "PLAYBOOK", "BOOK")

  Message 1:
  ──────────
  "Credit Ascension — the full playbook 👑

  ✓ 5 federal laws that delete negative items
  ✓ Secret lenders list (30+ with bureau pull data)
  ✓ AI tools that automate disputes
  ✓ Business credit blueprint (no SSN needed)
  ✓ 90-day step-by-step plan

  Get it here: [PAYHIP $47 LINK]

  This is the system. Not a tip. Not a hack. The whole thing."

  ═══════════════════════════════════════════════════════════════
  FLOW 3: "AI" KEYWORD → AI TOOLS PITCH
  ═══════════════════════════════════════════════════════════════

  TRIGGER: User comments "AI" (or "TOOLS", "AUTOMATE")

  Message 1:
  ──────────
  "The AI Credit Cheat Code — nobody else is teaching this 🤖

  I mapped AI tools to EVERY step of credit repair:
  ✓ Dovly — auto-disputes on autopilot
  ✓ Dispute AI — generates letters in seconds
  ✓ ChatGPT — custom prompts for bureau responses
  ✓ Claude — analyzes your credit report for errors

  The full system: [PAYHIP $67 LINK]"

  ═══════════════════════════════════════════════════════════════
  SETUP STEPS IN MANYCHAT:
  ═══════════════════════════════════════════════════════════════

  1. Connect your TikTok Business Account
     └─ ManyChat → Settings → Channels → TikTok → Connect
     └─ REQUIRES Business TikTok account (not Creator/Personal)
     └─ NOT available in UK/EU (TikTok restriction)

  2. Connect Instagram (optional, recommended)
     └─ ManyChat → Settings → Channels → Instagram → Connect

  3. Create Tags (run: python scripts/manychat_setup.py --create-tags)

  4. Create Custom Fields:
     └─ "email" (text) — for email collection
     └─ "product_interest" (text) — for segmentation
     └─ "source_platform" (text) — tiktok or instagram

  5. Build Flow 1 ("LAWS" keyword):
     └─ Automation → New Flow → TikTok Comment Trigger
     └─ Keyword: LAWS, LAW, FEDERAL, FREE
     └─ Add messages as outlined above
     └─ Add User Input block to collect email
     └─ Add External Request to POST to Make.com webhook

  6. Build Flow 2 ("GUIDE" keyword):
     └─ Same structure, different messages

  7. Test: Comment "LAWS" on your own TikTok video

  ═══════════════════════════════════════════════════════════════
  MANYCHAT → MAKE.COM WEBHOOK FORMAT:
  ═══════════════════════════════════════════════════════════════

  POST [Make.com webhook URL]
  Content-Type: application/json

  {{
    "email": "{{{{email}}}}",
    "first_name": "{{{{first_name}}}}",
    "source": "tiktok_dm",
    "keyword": "LAWS",
    "manychat_id": "{{{{subscriber_id}}}}",
    "tags": ["lead_magnet", "tiktok_lead"]
  }}

{'='*70}
""")


def main():
    check_api_key()

    parser = argparse.ArgumentParser(description="ManyChat Manager for GOD MODE CREDIT")
    parser.add_argument("--get-info", action="store_true", help="Get connected page info")
    parser.add_argument("--list-tags", action="store_true", help="List all tags")
    parser.add_argument("--create-tag", type=str, help="Create a new tag")
    parser.add_argument("--create-tags", action="store_true", help="Create all required GMC tags")
    parser.add_argument("--list-fields", action="store_true", help="List custom fields")
    parser.add_argument("--list-flows", action="store_true", help="List automation flows")
    parser.add_argument("--setup-guide", action="store_true", help="Print full setup guide")

    args = parser.parse_args()

    if args.get_info:
        get_page_info()
    elif args.list_tags:
        list_tags()
    elif args.create_tag:
        create_tag(args.create_tag)
    elif args.create_tags:
        setup_required_tags()
    elif args.list_fields:
        list_custom_fields()
    elif args.list_flows:
        list_flows()
    elif args.setup_guide:
        print_setup_guide()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
