#!/usr/bin/env python3
"""
SoulHustleAI — Logo Generator
Automatically generates logo variants using the first available image-gen API
(fal.ai → Replicate → HuggingFace → OpenArt).

Run once an API key is added to Supabase system_config:
    fal_ai_api_key, replicate_api_token, huggingface_token, openart_api_key

Usage:
    export SUPABASE_URL=...
    export SUPABASE_SERVICE_KEY=...
    pip install supabase httpx
    python logo_generate.py

Output:
    soulhustleai/brand/logo/generated/<tool>_<timestamp>_<n>.png
"""
import os
import sys
import time
import pathlib
from typing import Optional

try:
    from supabase import create_client
    import httpx
except ImportError:
    print("Install deps: pip install supabase httpx")
    sys.exit(1)

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT_DIR = REPO_ROOT / "brand" / "logo" / "generated"
OUT_DIR.mkdir(parents=True, exist_ok=True)

SUPABASE_URL = os.environ.get("SUPABASE_URL", "https://pjkurxtvvtxbpfearqhd.supabase.co")
SUPABASE_SERVICE_KEY = os.environ["SUPABASE_SERVICE_KEY"]
supa = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)

# The master prompt — matches PROMPT-PACK.md Prompt 1 style
MASTER_PROMPT = """Luxury fintech logo design, vertical square composition, pure black background #050505,
central emblem of a gold astrolabe compass with a glowing 4-point navigation star at its heart,
two flowing ribbon arcs forming an infinite S shape weaving through the compass — one arc in
rich gold #C9A033 with soft highlight #F2C95C labeled SOUL, the other in polished platinum silver
labeled HUSTLE, both arcs end in subtle arrow points, faint astrolabe tick marks radiating around
the compass, subtle Bloomberg-terminal grid background at 8% opacity, cinematic rim lighting,
premium editorial quality, symmetric and balanced, clean vector aesthetic, luxury financial
brand identity, minimal and unforgettable, 8k detail, NO red, NO text, NO typography"""

NEGATIVE_PROMPT = "red, text, typography, watermark, signature, low quality, blurry, saas, generic, cartoon, 3d"


def get_key(name: str) -> Optional[str]:
    """Fetch an API key from Supabase system_config."""
    try:
        r = supa.table("system_config").select("value").eq("key", name).maybe_single().execute()
        if r and r.data:
            v = r.data["value"]
            return v.strip('"') if isinstance(v, str) else v
    except Exception:
        pass
    return None


def save_image(data: bytes, tool: str, n: int) -> pathlib.Path:
    ts = time.strftime("%Y%m%d-%H%M%S")
    path = OUT_DIR / f"{tool}_{ts}_{n:02d}.png"
    path.write_bytes(data)
    print(f"  ✓ {path.relative_to(REPO_ROOT)} ({len(data) // 1024}KB)")
    return path


# ==================== PROVIDERS ====================

def generate_via_fal(api_key: str, n: int = 4) -> int:
    """Fal.ai Flux Pro — fastest, highest quality."""
    print("🎨 fal.ai Flux Pro")
    url = "https://fal.run/fal-ai/flux-pro/v1.1"
    saved = 0
    with httpx.Client(timeout=120) as client:
        for i in range(n):
            r = client.post(
                url,
                headers={"Authorization": f"Key {api_key}"},
                json={
                    "prompt": MASTER_PROMPT,
                    "image_size": "square_hd",
                    "num_inference_steps": 28,
                    "guidance_scale": 3.5,
                    "enable_safety_checker": False,
                    "output_format": "png",
                },
            )
            if r.status_code != 200:
                print(f"  ✗ {r.status_code}: {r.text[:200]}")
                continue
            image_url = r.json()["images"][0]["url"]
            img = client.get(image_url).content
            save_image(img, "fal_flux_pro", i + 1)
            saved += 1
            time.sleep(1)
    return saved


def generate_via_replicate(api_key: str, n: int = 4) -> int:
    """Replicate — many models, Flux works well."""
    print("🎨 Replicate Flux Pro")
    url = "https://api.replicate.com/v1/predictions"
    saved = 0
    with httpx.Client(timeout=240) as client:
        for i in range(n):
            r = client.post(
                url,
                headers={
                    "Authorization": f"Token {api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "version": "black-forest-labs/flux-1.1-pro",
                    "input": {
                        "prompt": MASTER_PROMPT,
                        "aspect_ratio": "1:1",
                        "output_format": "png",
                        "output_quality": 100,
                    },
                },
            )
            if r.status_code != 201:
                print(f"  ✗ {r.status_code}: {r.text[:200]}")
                continue
            pred_id = r.json()["id"]
            # Poll
            for _ in range(60):
                poll = client.get(f"{url}/{pred_id}", headers={"Authorization": f"Token {api_key}"})
                status = poll.json().get("status")
                if status == "succeeded":
                    img_url = poll.json()["output"]
                    if isinstance(img_url, list):
                        img_url = img_url[0]
                    img = client.get(img_url).content
                    save_image(img, "replicate_flux", i + 1)
                    saved += 1
                    break
                if status == "failed":
                    print(f"  ✗ prediction failed")
                    break
                time.sleep(2)
    return saved


def generate_via_huggingface(api_key: str, n: int = 4) -> int:
    """HuggingFace Inference API — free tier available."""
    print("🎨 HuggingFace (FLUX.1-schnell)")
    url = "https://api-inference.huggingface.co/models/black-forest-labs/FLUX.1-schnell"
    saved = 0
    with httpx.Client(timeout=180) as client:
        for i in range(n):
            r = client.post(
                url,
                headers={"Authorization": f"Bearer {api_key}"},
                json={
                    "inputs": MASTER_PROMPT,
                    "parameters": {"negative_prompt": NEGATIVE_PROMPT},
                },
            )
            if r.status_code == 503:
                # Model loading — wait and retry
                print("  … model warming up, waiting 30s")
                time.sleep(30)
                continue
            if r.status_code != 200:
                print(f"  ✗ {r.status_code}: {r.text[:200]}")
                continue
            save_image(r.content, "hf_flux_schnell", i + 1)
            saved += 1
            time.sleep(2)
    return saved


# ==================== MAIN ====================

def main():
    print("═══ SHAI LOGO GENERATOR ═══\n")

    # Try each provider in priority order
    providers = [
        ("fal_ai_api_key",      generate_via_fal),
        ("replicate_api_token", generate_via_replicate),
        ("huggingface_token",   generate_via_huggingface),
    ]

    for key_name, fn in providers:
        key = get_key(key_name)
        if key:
            print(f"Using {key_name}\n")
            saved = fn(key, n=4)
            print(f"\n✓ Generated {saved} variants → {OUT_DIR}")
            if saved > 0:
                return
        else:
            print(f"· {key_name} not found in system_config")

    print("""
╔══════════════════════════════════════════════════════╗
║  NO IMAGE-GEN API KEY FOUND IN SUPABASE             ║
╠══════════════════════════════════════════════════════╣
║  Add one of these keys to continue:                  ║
║                                                      ║
║    • fal_ai_api_key       (recommended — fastest)    ║
║    • replicate_api_token  (many models)              ║
║    • huggingface_token    (free tier available)      ║
║                                                      ║
║  SQL:                                                ║
║    INSERT INTO system_config (key, value)            ║
║    VALUES ('fal_ai_api_key', '"YOUR_KEY"')           ║
║    ON CONFLICT (key) DO UPDATE                       ║
║    SET value = EXCLUDED.value;                       ║
║                                                      ║
║  Then re-run: python logo_generate.py                ║
╚══════════════════════════════════════════════════════╝

In the meantime → paste prompts from
  soulhustleai/brand/logo/PROMPT-PACK.md
into Higgsfield, OpenArt, or Midjourney manually.
""")


if __name__ == "__main__":
    main()
