#!/usr/bin/env python3
"""
HeyGen AI Avatar Video Generator — GOD MODE CREDIT
Generates vertical (9:16) AI avatar videos from scripts.
Uses HeyGen Video Agent API for fully automated video creation.

Usage:
    python scripts/heygen_video.py --script "Your script text here"
    python scripts/heygen_video.py --file scripts/tiktok_scripts/script_01.txt
    python scripts/heygen_video.py --batch scripts/tiktok_scripts/
"""

import os
import sys
import json
import time
import argparse
import requests
from pathlib import Path
from dotenv import load_dotenv

# Load .env from project root
load_dotenv(Path(__file__).resolve().parent.parent / ".env")

API_KEY = os.getenv("HEYGEN_API_KEY")
BASE_URL = "https://api.heygen.com"

# Default settings for GOD MODE CREDIT content
DEFAULTS = {
    "aspect_ratio": "9:16",          # Vertical for TikTok/Reels/Shorts
    "avatar_id": None,               # Set after browsing available avatars
    "voice_id": None,                # Set after browsing available voices
    "background_color": "#050505",   # GOD MODE CREDIT black
    "output_dir": "output/videos",
}

HEADERS = {
    "X-Api-Key": API_KEY,
    "Content-Type": "application/json",
}


def check_api_key():
    if not API_KEY:
        print("[ERROR] HEYGEN_API_KEY not set in .env file")
        sys.exit(1)


def list_avatars():
    """List all available avatars to pick one for GOD MODE CREDIT."""
    resp = requests.get(f"{BASE_URL}/v2/avatars", headers=HEADERS)
    resp.raise_for_status()
    data = resp.json()
    avatars = data.get("data", {}).get("avatars", [])
    print(f"\n{'='*60}")
    print(f"  AVAILABLE AVATARS ({len(avatars)} total)")
    print(f"{'='*60}")
    for av in avatars[:30]:  # Show first 30
        print(f"  ID: {av['avatar_id']}")
        print(f"  Name: {av.get('avatar_name', 'N/A')}")
        print(f"  Gender: {av.get('gender', 'N/A')}")
        print(f"  ---")
    return avatars


def list_voices():
    """List available voices."""
    resp = requests.get(f"{BASE_URL}/v2/voices", headers=HEADERS)
    resp.raise_for_status()
    data = resp.json()
    voices = data.get("data", {}).get("voices", [])
    print(f"\n{'='*60}")
    print(f"  AVAILABLE VOICES ({len(voices)} total)")
    print(f"{'='*60}")
    for v in voices[:30]:
        print(f"  ID: {v['voice_id']}")
        print(f"  Name: {v.get('display_name', v.get('name', 'N/A'))}")
        print(f"  Language: {v.get('language', 'N/A')}")
        print(f"  ---")
    return voices


def generate_video_agent(script_text, title="GOD MODE CREDIT"):
    """
    Use HeyGen Video Agent (newest API) — one POST, fully assembled video.
    This is the simplest path: script in, finished video out.
    """
    payload = {
        "video_inputs": [{
            "character": {
                "type": "avatar",
                "avatar_id": DEFAULTS["avatar_id"] or "default",
                "avatar_style": "normal",
            },
            "voice": {
                "type": "text",
                "input_text": script_text,
                "voice_id": DEFAULTS["voice_id"] or "default",
            },
            "background": {
                "type": "color",
                "value": DEFAULTS["background_color"],
            },
        }],
        "dimension": {
            "width": 1080,
            "height": 1920,
        },
        "aspect_ratio": None,  # Using explicit dimensions instead
        "title": title,
    }

    print(f"\n[HEYGEN] Generating video: '{title}'")
    print(f"[HEYGEN] Script length: {len(script_text)} chars")

    resp = requests.post(
        f"{BASE_URL}/v2/video/generate",
        headers=HEADERS,
        json=payload,
    )
    resp.raise_for_status()
    data = resp.json()

    video_id = data.get("data", {}).get("video_id")
    if not video_id:
        print(f"[ERROR] No video_id returned: {data}")
        return None

    print(f"[HEYGEN] Video ID: {video_id}")
    print(f"[HEYGEN] Polling for completion...")

    return poll_video(video_id)


def poll_video(video_id, max_wait=600, interval=15):
    """Poll until video is ready (typically 2-5 minutes)."""
    elapsed = 0
    while elapsed < max_wait:
        resp = requests.get(
            f"{BASE_URL}/v1/video_status.get",
            headers=HEADERS,
            params={"video_id": video_id},
        )
        resp.raise_for_status()
        data = resp.json()["data"]
        status = data.get("status")

        if status == "completed":
            video_url = data.get("video_url")
            print(f"\n[HEYGEN] Video READY: {video_url}")
            return {
                "video_id": video_id,
                "video_url": video_url,
                "status": "completed",
            }
        elif status == "failed":
            error = data.get("error", "Unknown error")
            print(f"\n[HEYGEN] Video FAILED: {error}")
            return {"video_id": video_id, "status": "failed", "error": error}

        print(f"[HEYGEN] Status: {status} ({elapsed}s elapsed)")
        time.sleep(interval)
        elapsed += interval

    print(f"\n[HEYGEN] Timed out after {max_wait}s")
    return {"video_id": video_id, "status": "timeout"}


def download_video(video_url, filename):
    """Download completed video to output directory."""
    output_dir = Path(DEFAULTS["output_dir"])
    output_dir.mkdir(parents=True, exist_ok=True)
    filepath = output_dir / filename

    print(f"[HEYGEN] Downloading to {filepath}...")
    resp = requests.get(video_url, stream=True)
    resp.raise_for_status()
    with open(filepath, "wb") as f:
        for chunk in resp.iter_content(chunk_size=8192):
            f.write(chunk)
    print(f"[HEYGEN] Saved: {filepath}")
    return str(filepath)


def batch_generate(scripts_dir):
    """Generate videos from all .txt files in a directory."""
    scripts_path = Path(scripts_dir)
    results = []
    for script_file in sorted(scripts_path.glob("*.txt")):
        script_text = script_file.read_text().strip()
        title = script_file.stem.replace("_", " ").title()
        result = generate_video_agent(script_text, title=title)
        if result and result["status"] == "completed":
            download_video(
                result["video_url"],
                f"{script_file.stem}.mp4"
            )
        results.append({"file": script_file.name, **result} if result else {"file": script_file.name, "status": "error"})
        time.sleep(2)  # Rate limit buffer

    # Save results manifest
    manifest_path = Path(DEFAULTS["output_dir"]) / "batch_manifest.json"
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    with open(manifest_path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\n[HEYGEN] Batch complete. Manifest: {manifest_path}")
    return results


def main():
    check_api_key()

    parser = argparse.ArgumentParser(description="HeyGen Video Generator for GOD MODE CREDIT")
    parser.add_argument("--script", type=str, help="Script text to generate video from")
    parser.add_argument("--file", type=str, help="Path to script .txt file")
    parser.add_argument("--batch", type=str, help="Directory of .txt script files")
    parser.add_argument("--list-avatars", action="store_true", help="List available avatars")
    parser.add_argument("--list-voices", action="store_true", help="List available voices")
    parser.add_argument("--avatar-id", type=str, help="Override avatar ID")
    parser.add_argument("--voice-id", type=str, help="Override voice ID")
    parser.add_argument("--title", type=str, default="GOD MODE CREDIT", help="Video title")

    args = parser.parse_args()

    if args.avatar_id:
        DEFAULTS["avatar_id"] = args.avatar_id
    if args.voice_id:
        DEFAULTS["voice_id"] = args.voice_id

    if args.list_avatars:
        list_avatars()
    elif args.list_voices:
        list_voices()
    elif args.batch:
        batch_generate(args.batch)
    elif args.file:
        script_text = Path(args.file).read_text().strip()
        result = generate_video_agent(script_text, title=args.title)
        if result and result["status"] == "completed":
            safe_title = args.title.lower().replace(" ", "_")
            download_video(result["video_url"], f"{safe_title}.mp4")
    elif args.script:
        result = generate_video_agent(args.script, title=args.title)
        if result and result["status"] == "completed":
            safe_title = args.title.lower().replace(" ", "_")
            download_video(result["video_url"], f"{safe_title}.mp4")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
