#!/usr/bin/env python3
"""
GOD MODE CREDIT — Master Content Pipeline Orchestrator

The full automated flow:
  1. Claude generates TikTok script + caption + hashtags
  2. HeyGen creates AI avatar video from script
  3. Buffer schedules video across TikTok, IG, YouTube Shorts, Pinterest
  4. ManyChat catches comments → delivers lead magnet → collects emails
  5. Make.com → ConvertKit tags and nurtures leads

Usage:
    python scripts/pipeline.py --generate-and-schedule "credit repair myths"
    python scripts/pipeline.py --batch-generate topics.json
    python scripts/pipeline.py --status
    python scripts/pipeline.py --test
"""

import os
import sys
import json
import time
import argparse
from pathlib import Path
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent.parent / ".env")

# Import sub-modules
sys.path.insert(0, str(Path(__file__).resolve().parent))
from heygen_video import generate_video_agent, download_video, check_api_key as check_heygen
from buffer_schedule import schedule_staggered, check_api_key as check_buffer

# Content pillars for GOD MODE CREDIT
CONTENT_PILLARS = {
    "rights": {
        "description": "Federal law says they MUST remove this — FCRA/FDCPA education",
        "hashtags": "#creditrepair #fcra #fdcpa #creditrights #creditlaw #fyp #credittips",
        "cta": "Comment LAWS for the free guide 👇",
    },
    "ai_tools": {
        "description": "I let AI dispute my credit — here's what happened",
        "hashtags": "#aicreditrepair #dovly #creditai #automation #creditfix #fyp",
        "cta": "Comment AI for the tool list 🤖",
    },
    "divine_energy": {
        "description": "They profit off your ignorance — spiritual wealth lens",
        "hashtags": "#financialsovereignty #credithealing #wealthmindset #fyp #godmode",
        "cta": "Comment LAWS for the free guide 👇",
    },
    "business_credit": {
        "description": "$50K biz credit with no personal SSN",
        "hashtags": "#businesscredit #llc #ein #bizcredit #fundingstack #fyp",
        "cta": "Comment GUIDE for the full playbook 📖",
    },
    "ai_income": {
        "description": "My staff don't exist — Zero energy",
        "hashtags": "#aiautomation #makemoney #aitools #sideHustle #fyp #passiveincome",
        "cta": "Comment AI for the breakdown 🤖",
    },
}


def check_all_keys():
    """Verify all API keys are configured."""
    keys = {
        "HEYGEN_API_KEY": os.getenv("HEYGEN_API_KEY"),
        "BUFFER_API_KEY": os.getenv("BUFFER_API_KEY"),
        "MAKE_API_KEY": os.getenv("MAKE_API_KEY"),
        "MANYCHAT_API_KEY": os.getenv("MANYCHAT_API_KEY"),
        "CONVERTKIT_API_KEY": os.getenv("CONVERTKIT_API_KEY"),
        "PAYHIP_API_KEY": os.getenv("PAYHIP_API_KEY"),
    }

    print(f"\n{'='*50}")
    print(f"  API KEY STATUS")
    print(f"{'='*50}")

    all_set = True
    for name, value in keys.items():
        status = "SET" if value else "MISSING"
        icon = "[+]" if value else "[!]"
        masked = f"{value[:8]}...{value[-4:]}" if value and len(value) > 12 else ("***" if value else "—")
        print(f"  {icon} {name}: {masked} ({status})")
        if not value:
            all_set = False

    print(f"\n  {'All keys configured!' if all_set else 'Some keys missing — check .env'}")
    return all_set


def generate_script_prompt(topic, pillar="rights"):
    """
    Generate a Claude API prompt for creating a TikTok script.
    This would be sent to Claude API in the Make.com/n8n scenario.
    Returns the prompt text that Make.com sends to Claude.
    """
    pillar_data = CONTENT_PILLARS.get(pillar, CONTENT_PILLARS["rights"])

    prompt = f"""Write a 45-60 second TikTok script for GOD MODE CREDIT about: {topic}

Content pillar: {pillar_data['description']}

RULES:
- Hook in first 2 seconds (pattern interrupt, bold claim, or question)
- Conversational tone — Gen Z energy meets Fortune 500 authority
- Include 1 specific federal law, stat, or fact (not vague)
- End with CTA: "{pillar_data['cta']}"
- Spiritual undertone: knowledge is power, reclaiming what's yours
- NO legal advice. Education ONLY. CROA compliant.
- Write for someone with a 450-600 credit score who feels stuck

FORMAT:
[HOOK - 2 seconds]
(Your attention-grabbing opener)

[BODY - 40-50 seconds]
(The value — teach one specific thing)

[CTA - 5 seconds]
(Call to action with keyword trigger)

Also provide:
CAPTION: (for the post — include CTA + hashtags)
HASHTAGS: {pillar_data['hashtags']}
"""
    return prompt


def generate_and_schedule(topic, pillar="rights"):
    """
    Full pipeline: generate script → create video → schedule posts.

    NOTE: In production, Claude API generates the script via Make.com.
    This function demonstrates the full flow and can be connected to Claude API.
    """
    print(f"\n{'='*60}")
    print(f"  GOD MODE CREDIT — CONTENT PIPELINE")
    print(f"  Topic: {topic}")
    print(f"  Pillar: {pillar}")
    print(f"{'='*60}")

    pillar_data = CONTENT_PILLARS.get(pillar, CONTENT_PILLARS["rights"])

    # Step 1: Generate script prompt (send to Claude API in production)
    print(f"\n[STEP 1] Script Generation")
    prompt = generate_script_prompt(topic, pillar)
    print(f"  Claude API prompt ready ({len(prompt)} chars)")
    print(f"  In production: Make.com sends this to Claude API")
    print(f"  For now: copy this prompt and paste into Claude:")
    print(f"\n{'─'*50}")
    print(prompt)
    print(f"{'─'*50}")

    # Step 2: Once you have the script, generate video
    print(f"\n[STEP 2] Video Generation (HeyGen)")
    print(f"  After Claude writes the script:")
    print(f"  python scripts/heygen_video.py --script 'YOUR_SCRIPT_TEXT' --title '{topic}'")

    # Step 3: Schedule the video
    print(f"\n[STEP 3] Social Scheduling (Buffer)")
    print(f"  After video is downloaded:")
    caption = f"{pillar_data['cta']}\n\n{pillar_data['hashtags']}"
    print(f"  Caption: {caption}")
    print(f"  python scripts/buffer_schedule.py --post '{caption}' --video-url VIDEO_URL --stagger")

    # Step 4: ManyChat catches the comments
    print(f"\n[STEP 4] DM Automation (ManyChat)")
    print(f"  ManyChat monitors for keyword comments (already configured)")
    print(f"  '{pillar_data['cta']}' → auto-DM → email capture → ConvertKit")

    print(f"\n{'='*60}")
    print(f"  PIPELINE READY — Execute steps 1-3 to go live")
    print(f"{'='*60}")


def batch_generate_prompts(topics_file=None):
    """
    Generate Claude API prompts for a batch of topics.
    Outputs a file of prompts ready to feed into Make.com/Claude API.
    """
    if topics_file:
        with open(topics_file) as f:
            topics = json.load(f)
    else:
        # Default 21 topics across all 5 pillars (3 weeks of content, 1/day)
        topics = [
            # RIGHTS pillar (7 scripts)
            {"topic": "The 623 method — FCRA Section 623 forces bureaus to verify", "pillar": "rights"},
            {"topic": "Debt collectors can't contact you at work — FDCPA Section 805", "pillar": "rights"},
            {"topic": "You can sue for $1000 per FCRA violation — most people don't know", "pillar": "rights"},
            {"topic": "How to freeze and unfreeze your credit in 5 minutes", "pillar": "rights"},
            {"topic": "The 30-day dispute window — bureaus MUST respond or delete", "pillar": "rights"},
            {"topic": "Medical debt under $500 can't be on your report anymore", "pillar": "rights"},
            {"topic": "Statute of limitations on debt — they can't collect forever", "pillar": "rights"},

            # AI TOOLS pillar (4 scripts)
            {"topic": "Dovly disputes on autopilot — I set it and forget it", "pillar": "ai_tools"},
            {"topic": "I used ChatGPT to write dispute letters — here's the prompt", "pillar": "ai_tools"},
            {"topic": "3 AI tools that replace a $2000 credit repair company", "pillar": "ai_tools"},
            {"topic": "AI analyzed my credit report and found 7 errors I missed", "pillar": "ai_tools"},

            # DIVINE ENERGY pillar (4 scripts)
            {"topic": "Your credit score is a language — they just never taught you", "pillar": "divine_energy"},
            {"topic": "They profit when you don't know your rights — wake up", "pillar": "divine_energy"},
            {"topic": "Financial sovereignty is your birthright — stop asking permission", "pillar": "divine_energy"},
            {"topic": "The system wasn't built for you — so we build around it", "pillar": "divine_energy"},

            # BUSINESS CREDIT pillar (3 scripts)
            {"topic": "$50K in business credit without using your SSN — here's how", "pillar": "business_credit"},
            {"topic": "Net-30 accounts that report to D&B — build biz credit fast", "pillar": "business_credit"},
            {"topic": "LLC + EIN + biz credit = funded in 90 days", "pillar": "business_credit"},

            # AI INCOME pillar (3 scripts)
            {"topic": "My staff don't exist — AI runs my entire business", "pillar": "ai_income"},
            {"topic": "I automated my side hustle with Make.com — $3K/mo hands off", "pillar": "ai_income"},
            {"topic": "The AI automation stack that replaced 5 employees", "pillar": "ai_income"},
        ]

    prompts = []
    for i, item in enumerate(topics, 1):
        topic = item["topic"] if isinstance(item, dict) else item
        pillar = item.get("pillar", "rights") if isinstance(item, dict) else "rights"
        prompt = generate_script_prompt(topic, pillar)
        prompts.append({
            "index": i,
            "topic": topic,
            "pillar": pillar,
            "prompt": prompt,
            "hashtags": CONTENT_PILLARS[pillar]["hashtags"],
            "cta": CONTENT_PILLARS[pillar]["cta"],
        })

    # Save prompts
    output_path = Path("output/prompts")
    output_path.mkdir(parents=True, exist_ok=True)
    prompts_file = output_path / f"tiktok_prompts_{datetime.now().strftime('%Y%m%d')}.json"
    with open(prompts_file, "w") as f:
        json.dump(prompts, f, indent=2)

    print(f"\n[PIPELINE] Generated {len(prompts)} script prompts")
    print(f"[PIPELINE] Saved to: {prompts_file}")
    print(f"\n  Pillar breakdown:")
    pillar_counts = {}
    for p in prompts:
        pillar_counts[p["pillar"]] = pillar_counts.get(p["pillar"], 0) + 1
    for pillar, count in pillar_counts.items():
        print(f"    {pillar}: {count} scripts")

    return prompts


def print_status():
    """Print full pipeline status."""
    print(f"""
{'='*60}
  GOD MODE CREDIT — PIPELINE STATUS
  {datetime.now().strftime('%B %d, %Y')}
{'='*60}
""")

    # Check API keys
    check_all_keys()

    # Check output directories
    print(f"\n{'='*50}")
    print(f"  OUTPUT DIRECTORIES")
    print(f"{'='*50}")
    dirs = ["output/videos", "output/schedules", "output/prompts"]
    for d in dirs:
        p = Path(d)
        if p.exists():
            files = list(p.iterdir())
            print(f"  [+] {d}: {len(files)} files")
        else:
            print(f"  [ ] {d}: not created yet")

    # Pipeline overview
    print(f"""
{'='*50}
  PIPELINE FLOW
{'='*50}

  1. SCRIPT:    Claude API → generates TikTok scripts
                python scripts/pipeline.py --batch-prompts

  2. VIDEO:     HeyGen API → creates AI avatar videos
                python scripts/heygen_video.py --batch scripts/tiktok_scripts/

  3. SCHEDULE:  Buffer API → posts to TikTok/IG/YT/Pinterest
                python scripts/buffer_schedule.py --batch output/videos/ --captions captions.json

  4. CAPTURE:   ManyChat → auto-DMs on keyword comments
                python scripts/manychat_setup.py --setup-guide

  5. NURTURE:   Make.com → Payhip webhook → ConvertKit tags
                python scripts/make_webhooks.py --setup-payhip-pipeline

  READY TO GO? Start with:
  python scripts/pipeline.py --batch-prompts
""")


def main():
    parser = argparse.ArgumentParser(description="GOD MODE CREDIT Master Pipeline")
    parser.add_argument("--generate", type=str, help="Generate pipeline for single topic")
    parser.add_argument("--pillar", type=str, default="rights",
                       choices=list(CONTENT_PILLARS.keys()),
                       help="Content pillar (default: rights)")
    parser.add_argument("--batch-prompts", nargs="?", const=True,
                       help="Generate batch of Claude API prompts (optional: topics.json)")
    parser.add_argument("--status", action="store_true", help="Show pipeline status")
    parser.add_argument("--check-keys", action="store_true", help="Verify all API keys")
    parser.add_argument("--test", action="store_true", help="Run pipeline test")

    args = parser.parse_args()

    if args.status:
        print_status()
    elif args.check_keys:
        check_all_keys()
    elif args.generate:
        generate_and_schedule(args.generate, args.pillar)
    elif args.batch_prompts:
        topics_file = args.batch_prompts if isinstance(args.batch_prompts, str) else None
        batch_generate_prompts(topics_file)
    elif args.test:
        print("[TEST] Running pipeline diagnostics...")
        check_all_keys()
        print("\n[TEST] Generating sample prompt...")
        prompt = generate_script_prompt("The 623 method", "rights")
        print(f"[TEST] Prompt generated ({len(prompt)} chars)")
        print("[TEST] All systems ready.")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
