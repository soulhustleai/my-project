#!/usr/bin/env python3
"""
Generate an Apex voice sample via ElevenLabs.

Pulls the API key from the ELEVENLABS_API_KEY env var. Retrieve it from
sovereign_vault at runtime:

    export ELEVENLABS_API_KEY=$(psql $DATABASE_URL -t -c \
      "SELECT key_value FROM sovereign_vault \
       WHERE key_name='elevenlabs_api_key' AND is_active=true")

Usage:
    python3 generate_sample.py <voice_id> <output.mp3> [text]
"""

import os
import sys
import json
import urllib.request
import urllib.error

DEFAULT_TEXT = (
    "You were told you had bad credit. "
    "The law was written in nineteen seventy. "
    "They just prayed you'd never read it. "
    "Fifteen U.S.C. sixteen eighty one, section six eleven. "
    "The Fair Credit Reporting Act. "
    "The laws were written for you. You just never read them. "
    "Ascend."
)

# Locked Apex voice settings — matches apex/voice-config.md
APEX_VOICE_SETTINGS = {
    "stability": 0.55,
    "similarity_boost": 0.85,
    "style": 0.20,
    "use_speaker_boost": True,
}


def main():
    if len(sys.argv) < 3:
        print(__doc__, file=sys.stderr)
        sys.exit(1)

    voice_id = sys.argv[1]
    out_path = sys.argv[2]
    text = sys.argv[3] if len(sys.argv) > 3 else DEFAULT_TEXT

    api_key = os.environ.get("ELEVENLABS_API_KEY")
    if not api_key:
        print("ERROR: ELEVENLABS_API_KEY env var not set.", file=sys.stderr)
        print("Get it from sovereign_vault.elevenlabs_api_key", file=sys.stderr)
        sys.exit(2)

    body = json.dumps({
        "text": text,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": APEX_VOICE_SETTINGS,
    }).encode()

    req = urllib.request.Request(
        f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}",
        data=body,
        headers={
            "xi-api-key": api_key,
            "Content-Type": "application/json",
            "Accept": "audio/mpeg",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            data = resp.read()
        with open(out_path, "wb") as f:
            f.write(data)
        print(f"OK  {out_path}  {len(data):,} bytes  voice={voice_id}")
    except urllib.error.HTTPError as e:
        print(f"ERR {e.code}: {e.read().decode()[:500]}", file=sys.stderr)
        sys.exit(3)
    except Exception as e:
        print(f"ERR {type(e).__name__}: {e}", file=sys.stderr)
        sys.exit(4)


if __name__ == "__main__":
    main()
