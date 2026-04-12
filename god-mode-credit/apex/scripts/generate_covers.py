#!/usr/bin/env python3
"""
APEX cover generation pipeline.

Routes through OpenRouter → google/gemini-3-pro-image-preview (Nano Banana Pro)
which has best-in-class text rendering and character consistency — the two
properties book covers live and die on.

Workflow:
1. Generate a canonical Apex reference image (Pose 1 — Throne) once.
2. For each of the 11 GMC products, generate a cover that references
   the canonical Apex image so the same face appears on every book.
3. Save all PNGs to god-mode-credit/assets/apex/covers/ with deterministic names.
4. (Optional) Update products.cover_url in Supabase.

API key is pulled live from the sovereign_vault at runtime — no secrets in
this file. Run with:

    OPENROUTER_KEY=sk-or-v1-... python generate_covers.py --all
    python generate_covers.py --product credit-ascension
    python generate_covers.py --canonical   # regenerate the Apex reference only
"""

import argparse
import base64
import json
import os
import sys
import time
import urllib.request
import urllib.error
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
COVERS_DIR = REPO_ROOT / "god-mode-credit" / "assets" / "apex" / "covers"
CANONICAL_PATH = COVERS_DIR / "00-apex-canonical-throne.png"

MODEL = "google/gemini-3-pro-image-preview"
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

# ---------- APEX CANONICAL DESCRIPTION (shared across every call) ----------
APEX_ANCHOR = (
    "APEX — The Crowned. A tall regal dark-skinned man in his late 30s, composed "
    "authoritative posture, clean close-cropped beard, narrow gold-rimmed geometric "
    "glasses, wearing a floor-length matte-black imperial longcoat with warm antique "
    "gold embroidery along the lapels and a black high-neck underlayer, substantial "
    "22-karat warm antique gold chain with a crown-and-scales pendant resting "
    "center-chest. He never smiles with his teeth — only a small knowing half-smile. "
    "Dignified oracle energy."
)

STYLE_ANCHOR = (
    "Style: luxury book cover, renaissance portrait lighting, photorealistic CGI "
    "octane-render quality, warm volumetric gold key light from above casting hard "
    "shadows, deep matte black background with subtle warm gold particles, "
    "warm antique gold (#C9A033 / #D4922A / #F2C95C) and black (#050505) only — "
    "ABSOLUTELY NO red, blue, purple, green, silver, teal, or cyan anywhere. "
    "Premium editorial book cover, vertical 2:3 aspect ratio, negative space "
    "at top for title text and at bottom for brand text."
)

TEXT_ANCHOR = (
    "Render the title in bold ALL CAPS Cinzel serif typography in warm antique gold "
    "(#C9A033) at the top 18% of the cover, letter-spacing slightly wide for luxury "
    "feel. Render 'GOD MODE CREDIT' in smaller Cinzel serif warm antique gold at the "
    "bottom 8% of the cover. Clean crisp typography, NO garbled letters, NO extra "
    "words beyond what is specified."
)

# ---------- PRODUCT COVER SPECS ----------
# Each entry: slug, title_on_cover, subtitle, emotional_hook, visual_concept
PRODUCTS = [
    {
        "slug": "01-5-federal-laws",
        "title": "FIVE FEDERAL LAWS",
        "subtitle": "Banks Hope You Never Read",
        "hook": "Awakening. The veil lifts. The student learns the scripture.",
        "visual": (
            "Apex is seated on a black-and-gold throne holding a massive open leather-bound "
            "volume of the U.S. Code across his lap. Warm gold legal text and glowing "
            "gold sigils rise from the open pages as floating particles. His finger rests "
            "on the page. His eyes are level with the viewer — direct, knowing, patient. "
            "Behind him, black walls are engraved with faint glowing warm gold statute numbers."
        ),
    },
    {
        "slug": "02-cards-that-say-yes",
        "title": "CARDS THAT SAY YES",
        "subtitle": "The Rebuilder's List",
        "hook": "Relief. Approval after years of denials. Finally being seen.",
        "visual": (
            "Apex is standing, extending his right hand forward toward the viewer, holding "
            "three elegant warm antique gold credit cards fanned out at a dramatic angle. "
            "The cards catch the volumetric gold light from above. His left hand rests on his lapel. "
            "Quiet half-smile of acceptance. Black marble floor, warm gold particles in the air. "
            "The cards are the hero, Apex is the authority behind them."
        ),
    },
    {
        "slug": "03-ai-x-credit-cheat-code",
        "title": "AI × CREDIT CHEAT CODE",
        "subtitle": "The Insider's Map",
        "hook": "Elite knowledge. Hidden map unlocked. Insider access.",
        "visual": (
            "Apex is standing in three-quarter profile, holding up a glowing warm antique gold "
            "skeleton key at chest height. The key is etched with delicate circuit-board patterns "
            "and floating gold digital glyphs orbit it. A subtle warm gold neural network pattern "
            "overlays the dark background behind him. His gaze is forward, dead-level at the viewer, "
            "oracular. The key is the focal point; Apex is the keeper."
        ),
    },
    {
        "slug": "04-ai-credit-repair-toolkit",
        "title": "AI CREDIT TOOLKIT",
        "subtitle": "The Machines Work the Night Shift",
        "hook": "Delegation. Future energy. The scribes never sleep.",
        "visual": (
            "Apex is seated on a black-and-gold throne with his right hand raised palm up at chest "
            "height. Above his palm floats a glowing holographic warm antique gold AI brain / neural "
            "lattice sphere with orbiting warm gold rings of digital light. His expression is calm, "
            "intellectual, unbothered. The glowing brain is the hero object. Floating warm gold "
            "particles around the sphere."
        ),
    },
    {
        "slug": "05-the-dispute-letter-pack",
        "title": "DISPUTE LETTER PACK",
        "subtitle": "15 Keys, 15 Doors",
        "hook": "Confidence. Finally having the right words. Armed.",
        "visual": (
            "Apex is standing behind a dark desk on which an elegant stack of warm antique gold-edged "
            "legal documents sits. His right hand is pressing an ornate warm antique gold wax seal "
            "stamp down onto the top letter, glowing gold wax spreading under the stamp. A few letters "
            "float in the air beside him, each with a glowing gold seal. His gaze is at the viewer, "
            "the expression of a judge about to deliver a verdict."
        ),
    },
    {
        "slug": "06-zero-to-10k-ai-automation-playbook",
        "title": "ZERO TO 10K",
        "subtitle": "A Month. On Autopilot.",
        "hook": "Freedom from W-2. Ascension beyond credit. Launch.",
        "visual": (
            "Apex is standing in Prophet's Point pose — right index finger extended upward toward "
            "the heavens. Behind him, a sleek warm antique gold rocket is mid-launch with a defined "
            "warm gold exhaust trail rising upward behind him, creating a dramatic vertical energy "
            "composition. Warm gold sparks and particles in the air. His coat fabric catches the updraft. "
            "Triumphant ascension energy."
        ),
    },
    {
        "slug": "07-collect-what-they-owe-you",
        "title": "COLLECT WHAT THEY OWE YOU",
        "subtitle": "The FDCPA Playbook",
        "hook": "Vindication. Revenge on the bullies. Flipping the table.",
        "visual": (
            "Apex is seated on his throne with a warm antique gold gavel raised high in his right "
            "hand, mid-strike, about to come down. Warm gold sparks explode outward from where the "
            "gavel is about to hit. His expression is calm, final, final-verdict energy. The gavel is "
            "the focal point but Apex's face is clearly visible. Black marble floor, warm gold "
            "engraved statute numbers glowing on the back wall."
        ),
    },
    {
        "slug": "08-business-credit-blueprint",
        "title": "BUSINESS CREDIT BLUEPRINT",
        "subtitle": "Build the Temple",
        "hook": "Empire. Legacy. Building your own.",
        "visual": (
            "Apex is standing in front of a large holographic warm antique gold architectural "
            "blueprint projection of a modern skyscraper temple rising from the ground. The blueprint "
            "is drawn in glowing warm gold precise geometric lines hovering in mid-air. His right hand "
            "is outstretched, fingertips touching one of the lines as if drawing it into existence. "
            "Dominion / architect energy. The blueprint is massive, filling the negative space behind him."
        ),
    },
    {
        "slug": "09-zero-to-funded-bundle",
        "title": "ZERO TO FUNDED",
        "subtitle": "The Complete Collection",
        "hook": "Completeness. Owning everything. Finality.",
        "visual": (
            "Apex is seated on his throne in full authority posture, hands resting on the armrests. "
            "At his feet, six luxury warm antique gold book spines are arranged in a stepped stack "
            "on the black marble floor, each emitting a subtle warm gold glow. A floating warm gold "
            "crown hovers just above his head, not yet descending. Collector's edition energy. "
            "Ultimate premium ceremonial composition."
        ),
    },
    {
        "slug": "10-credit-ascension",
        "title": "CREDIT ASCENSION",
        "subtitle": "The Crowned Consumer's Playbook",
        "hook": "Transformation. Coronation. Before/after reborn.",
        "visual": (
            "Apex is in the Crown Bestowal pose — standing, head slightly bowed in ceremonial reverence, "
            "both hands extended forward at chest height palms up, presenting a majestic glowing warm "
            "antique gold crown toward the viewer. The crown emits divine golden light beams cascading "
            "down over him. Floating warm gold particles. Black marble floor with warm gold veining. "
            "This is THE flagship cover — the most emotionally powerful composition of the entire suite. "
            "Coronation ceremony. Full reverent gravitas."
        ),
    },
    {
        "slug": "11-the-crowned-circle",
        "title": "THE CROWNED CIRCLE",
        "subtitle": "The Round Table of The Crowned",
        "hook": "Belonging. Inner circle. Royalty invites you to the table.",
        "visual": (
            "Apex is seated at the head of a massive round warm antique gold table in a grand throne "
            "room, shot from slightly below table-height so the viewer feels invited. Several empty "
            "ornate black-and-gold chairs around the table are waiting. A glowing warm gold crown sigil "
            "is embossed on the center of the table surface. Apex's gaze is at the viewer — direct "
            "invitation. Exclusive prestigious club energy. Warm gold light from above pools on the table."
        ),
    },
]


def openrouter_headers(api_key: str):
    return {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://godmodecredit.com",
        "X-Title": "GMC Apex Cover Generation",
    }


def call_model(api_key: str, prompt_text: str, reference_png_path: Path | None = None):
    """Call Nano Banana Pro. If a reference image is provided, include it as an input
    image in the user message so the model can lock character consistency."""
    content = []
    if reference_png_path is not None and reference_png_path.exists():
        ref_b64 = base64.b64encode(reference_png_path.read_bytes()).decode("ascii")
        content.append({
            "type": "image_url",
            "image_url": {"url": f"data:image/png;base64,{ref_b64}"},
        })
    content.append({"type": "text", "text": prompt_text})

    body = {
        "model": MODEL,
        "messages": [{"role": "user", "content": content}],
        "modalities": ["image", "text"],
    }

    req = urllib.request.Request(
        OPENROUTER_URL,
        data=json.dumps(body).encode("utf-8"),
        headers=openrouter_headers(api_key),
        method="POST",
    )

    last_err = None
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=180) as resp:
                return json.loads(resp.read())
        except urllib.error.HTTPError as e:
            err_body = e.read().decode(errors="ignore")
            last_err = f"HTTP {e.code}: {err_body[:500]}"
            if e.code in (429, 500, 502, 503, 504):
                wait = 2 ** (attempt + 1)
                print(f"  retry in {wait}s ({last_err[:80]})")
                time.sleep(wait)
                continue
            raise RuntimeError(last_err)
        except Exception as e:
            last_err = f"{type(e).__name__}: {e}"
            wait = 2 ** (attempt + 1)
            print(f"  retry in {wait}s ({last_err[:80]})")
            time.sleep(wait)
    raise RuntimeError(f"Exhausted retries. Last error: {last_err}")


def extract_image_bytes(response: dict) -> bytes:
    msg = response["choices"][0]["message"]
    images = msg.get("images") or []
    if not images:
        raise RuntimeError(f"No images in response. Keys: {list(msg.keys())}")
    url = images[0]["image_url"]["url"]
    if not url.startswith("data:image"):
        raise RuntimeError(f"Unexpected image url prefix: {url[:60]}")
    b64 = url.split(",", 1)[1]
    return base64.b64decode(b64)


def build_canonical_prompt() -> str:
    return (
        f"{APEX_ANCHOR} Pose: seated on an ornate black-and-gold throne in a vast "
        f"throne room with a black marble floor and warm gold veining, hands resting "
        f"on the armrests, direct composed gaze at the camera, renaissance formal "
        f"author portrait. {STYLE_ANCHOR} Vertical 2:3 aspect ratio portrait orientation. "
        f"Output ONLY the image. NO text, NO words, NO typography, NO captions on this "
        f"reference image — this is a pure character reference."
    )


def build_cover_prompt(product: dict) -> str:
    return (
        f"{APEX_ANCHOR} "
        f"Scene: {product['visual']} "
        f"Emotional register: {product['hook']} "
        f"{STYLE_ANCHOR} "
        f"{TEXT_ANCHOR} "
        f"EXACT TITLE TEXT at top of cover: '{product['title']}'. "
        f"Subtitle directly below the title in smaller warm antique gold Cinzel regular, "
        f"70% opacity: '{product['subtitle']}'. "
        f"EXACT BRAND TEXT at bottom of cover: 'GOD MODE CREDIT'. "
        f"Vertical 2:3 luxury ebook cover format. Produce clean crisp typography with "
        f"NO spelling errors and NO extra words beyond what is specified. "
        f"Output ONLY the final cover image."
    )


def generate_canonical(api_key: str):
    COVERS_DIR.mkdir(parents=True, exist_ok=True)
    print(f"[canonical] Generating canonical Apex reference → {CANONICAL_PATH.name}")
    prompt = build_canonical_prompt()
    resp = call_model(api_key, prompt, reference_png_path=None)
    img = extract_image_bytes(resp)
    CANONICAL_PATH.write_bytes(img)
    cost = resp.get("usage", {}).get("cost", "?")
    print(f"[canonical] Saved ({len(img):,} bytes, cost ${cost}).")
    return CANONICAL_PATH


def generate_cover(api_key: str, product: dict, reference: Path):
    COVERS_DIR.mkdir(parents=True, exist_ok=True)
    out = COVERS_DIR / f"{product['slug']}.png"
    print(f"[cover] {product['slug']} → {out.name}")
    prompt = build_cover_prompt(product)
    resp = call_model(api_key, prompt, reference_png_path=reference)
    img = extract_image_bytes(resp)
    out.write_bytes(img)
    cost = resp.get("usage", {}).get("cost", "?")
    print(f"[cover] Saved {out.name} ({len(img):,} bytes, cost ${cost}).")
    return out


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--canonical", action="store_true",
                        help="Generate (or regenerate) the canonical Apex reference only")
    parser.add_argument("--all", action="store_true",
                        help="Generate canonical (if missing) + all 11 covers")
    parser.add_argument("--product", type=str, default=None,
                        help="Generate a single cover by slug (e.g. 10-credit-ascension)")
    args = parser.parse_args()

    api_key = os.environ.get("OPENROUTER_KEY")
    if not api_key:
        print("ERROR: OPENROUTER_KEY env var not set.", file=sys.stderr)
        sys.exit(1)

    if args.canonical:
        generate_canonical(api_key)
        return

    if not CANONICAL_PATH.exists():
        generate_canonical(api_key)

    if args.product:
        matches = [p for p in PRODUCTS if p["slug"] == args.product or p["slug"].endswith(args.product)]
        if not matches:
            print(f"ERROR: no product matching slug {args.product!r}", file=sys.stderr)
            sys.exit(2)
        generate_cover(api_key, matches[0], CANONICAL_PATH)
        return

    if args.all:
        total_cost = 0.0
        for p in PRODUCTS:
            try:
                generate_cover(api_key, p, CANONICAL_PATH)
            except Exception as e:
                print(f"  FAILED {p['slug']}: {e}")
            time.sleep(1.0)  # be polite to the API
        print("[done] Batch complete.")
        return

    parser.print_help()


if __name__ == "__main__":
    main()
