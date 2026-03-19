#!/usr/bin/env python3
"""
Buffer Social Media Scheduler — GOD MODE CREDIT
Schedules video posts across TikTok, IG Reels, YouTube Shorts, Pinterest.

Usage:
    python scripts/buffer_schedule.py --list-profiles
    python scripts/buffer_schedule.py --post "Caption here" --video output/videos/video.mp4
    python scripts/buffer_schedule.py --batch output/videos/ --captions scripts/captions.json
"""

import os
import sys
import json
import argparse
import requests
from pathlib import Path
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent.parent / ".env")

API_KEY = os.getenv("BUFFER_API_KEY")
BASE_URL = "https://api.bufferapp.com/1"

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
}

# Posting schedule: stagger across platforms for max reach
# TikTok = immediate, IG = +2hrs, YouTube = +4hrs, Pinterest = +6hrs
PLATFORM_STAGGER_HOURS = {
    "tiktok": 0,
    "instagram": 2,
    "youtube": 4,
    "pinterest": 6,
}


def check_api_key():
    if not API_KEY:
        print("[ERROR] BUFFER_API_KEY not set in .env file")
        sys.exit(1)


def get_user():
    """Get authenticated user info."""
    resp = requests.get(f"{BASE_URL}/user.json", headers=HEADERS)
    resp.raise_for_status()
    user = resp.json()
    print(f"[BUFFER] Authenticated as: {user.get('name', 'Unknown')}")
    return user


def list_profiles():
    """List all connected social media profiles."""
    resp = requests.get(f"{BASE_URL}/profiles.json", headers=HEADERS)
    resp.raise_for_status()
    profiles = resp.json()

    print(f"\n{'='*60}")
    print(f"  CONNECTED PROFILES ({len(profiles)} total)")
    print(f"{'='*60}")
    for p in profiles:
        print(f"  ID: {p['id']}")
        print(f"  Service: {p.get('service', 'N/A')}")
        print(f"  Name: {p.get('formatted_username', p.get('service_username', 'N/A'))}")
        print(f"  Type: {p.get('service_type', 'N/A')}")
        print(f"  ---")
    return profiles


def get_profiles_by_platform():
    """Get profile IDs grouped by platform."""
    resp = requests.get(f"{BASE_URL}/profiles.json", headers=HEADERS)
    resp.raise_for_status()
    profiles = resp.json()

    by_platform = {}
    for p in profiles:
        service = p.get("service", "").lower()
        by_platform.setdefault(service, []).append(p["id"])
    return by_platform


def create_post(profile_ids, text, media_url=None, scheduled_at=None):
    """
    Create a Buffer post (queued or scheduled).

    Args:
        profile_ids: List of Buffer profile IDs to post to
        text: Post caption/text
        media_url: URL to video/image (must be publicly accessible)
        scheduled_at: ISO datetime string for scheduling, or None for queue
    """
    payload = {
        "text": text,
        "profile_ids[]": profile_ids,
        "shorten": True,
    }

    if media_url:
        payload["media[video]"] = media_url

    if scheduled_at:
        payload["scheduled_at"] = scheduled_at
    else:
        payload["now"] = False  # Add to queue

    resp = requests.post(
        f"{BASE_URL}/updates/create.json",
        headers=HEADERS,
        data=payload,
    )
    resp.raise_for_status()
    result = resp.json()

    if result.get("success"):
        print(f"[BUFFER] Post created successfully")
        for update in result.get("updates", []):
            print(f"  Profile: {update.get('profile_id')}")
            print(f"  Status: {update.get('status')}")
            if update.get("due_at"):
                print(f"  Scheduled: {datetime.fromtimestamp(update['due_at'])}")
    else:
        print(f"[BUFFER] Post failed: {result.get('message', 'Unknown error')}")

    return result


def schedule_staggered(text, video_url=None, base_time=None):
    """
    Schedule the same post across all platforms with staggered timing.
    TikTok first, then IG +2hrs, YouTube +4hrs, Pinterest +6hrs.
    """
    if base_time is None:
        base_time = datetime.utcnow() + timedelta(hours=1)  # 1hr from now

    profiles_by_platform = get_profiles_by_platform()
    results = []

    for platform, offset_hours in PLATFORM_STAGGER_HOURS.items():
        profile_ids = profiles_by_platform.get(platform, [])
        if not profile_ids:
            print(f"[BUFFER] No {platform} profile connected — skipping")
            continue

        scheduled_at = (base_time + timedelta(hours=offset_hours)).isoformat() + "Z"
        print(f"\n[BUFFER] Scheduling {platform} for {scheduled_at}")

        result = create_post(
            profile_ids=profile_ids,
            text=text,
            media_url=video_url,
            scheduled_at=scheduled_at,
        )
        results.append({"platform": platform, "result": result})

    return results


def batch_schedule(videos_dir, captions_file, start_date=None, posts_per_day=3):
    """
    Batch schedule multiple videos with captions.

    captions.json format:
    [
        {"video": "script_01.mp4", "caption": "Federal law says...", "hashtags": "#credit #fyp"},
        {"video": "script_02.mp4", "caption": "Nobody told you...", "hashtags": "#creditrepair"},
    ]
    """
    videos_path = Path(videos_dir)
    with open(captions_file) as f:
        captions = json.load(f)

    if start_date:
        current_date = datetime.fromisoformat(start_date)
    else:
        current_date = datetime.utcnow() + timedelta(days=1)  # Start tomorrow

    # Best posting times (EST converted to UTC)
    # 7am EST, 12pm EST, 6pm EST = 12pm UTC, 5pm UTC, 11pm UTC
    post_times = [
        timedelta(hours=12),  # 7am EST
        timedelta(hours=17),  # 12pm EST
        timedelta(hours=23),  # 6pm EST
    ]

    post_index = 0
    results = []

    for caption_data in captions:
        video_file = caption_data.get("video", "")
        caption = caption_data.get("caption", "")
        hashtags = caption_data.get("hashtags", "")
        full_text = f"{caption}\n\n{hashtags}" if hashtags else caption

        video_path = videos_path / video_file
        video_url = caption_data.get("video_url")  # Use if hosted publicly

        time_slot = post_times[post_index % len(post_times)]
        base_time = datetime.combine(current_date.date(), datetime.min.time()) + time_slot

        print(f"\n{'='*50}")
        print(f"[BATCH] Video: {video_file}")
        print(f"[BATCH] Date: {base_time.date()} | Slot: {post_index % posts_per_day + 1}/{posts_per_day}")

        result = schedule_staggered(
            text=full_text,
            video_url=video_url,
            base_time=base_time,
        )
        results.append({"video": video_file, "scheduled": str(base_time), "result": result})

        post_index += 1
        if post_index % posts_per_day == 0:
            current_date += timedelta(days=1)

    # Save schedule manifest
    manifest_path = Path("output/schedules") / f"schedule_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    with open(manifest_path, "w") as f:
        json.dump(results, f, indent=2, default=str)
    print(f"\n[BATCH] Schedule manifest saved: {manifest_path}")
    return results


def main():
    check_api_key()

    parser = argparse.ArgumentParser(description="Buffer Scheduler for GOD MODE CREDIT")
    parser.add_argument("--list-profiles", action="store_true", help="List connected profiles")
    parser.add_argument("--post", type=str, help="Caption text for single post")
    parser.add_argument("--video-url", type=str, help="Public URL to video file")
    parser.add_argument("--schedule-at", type=str, help="ISO datetime for scheduling")
    parser.add_argument("--stagger", action="store_true", help="Stagger post across platforms")
    parser.add_argument("--batch", type=str, help="Videos directory for batch scheduling")
    parser.add_argument("--captions", type=str, help="Captions JSON file for batch scheduling")
    parser.add_argument("--start-date", type=str, help="Start date for batch (YYYY-MM-DD)")
    parser.add_argument("--posts-per-day", type=int, default=3, help="Posts per day (default: 3)")

    args = parser.parse_args()

    if args.list_profiles:
        get_user()
        list_profiles()
    elif args.batch and args.captions:
        batch_schedule(args.batch, args.captions, args.start_date, args.posts_per_day)
    elif args.post:
        if args.stagger:
            schedule_staggered(args.post, video_url=args.video_url)
        else:
            profiles = get_profiles_by_platform()
            all_ids = [pid for pids in profiles.values() for pid in pids]
            create_post(all_ids, args.post, media_url=args.video_url, scheduled_at=args.schedule_at)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
