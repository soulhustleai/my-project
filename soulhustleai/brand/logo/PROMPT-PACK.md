# SoulHustleAI Logo — AI Generation Prompt Pack
## Paste-ready prompts for Higgsfield, OpenArt, Flux, Midjourney, Seedance

> **Why this file exists:** Hand-coded SVGs (what's currently in `/brand/logo/`)
> are placeholders. The REAL v3 logo should come from one of the image-gen tools
> in the SHAI tech stack. This file contains ready-to-paste prompts for each tool.
> **Reference image:** Edwin's v2 concept shared on 2026-04-13 (gold + silver
> arcs forming an infinite S through a central gold compass).

---

## 🎯 THE CORE CONCEPT (the story behind every prompt)

> Soul meets hustle. Tech makes it infinite.
>
> A **Möbius-style Infinite S** rendered as two ribbons:
> - A **gold arc** representing SOUL sweeps from the top-left through a
>   central compass, exiting bottom-right.
> - A **silver/platinum arc** representing HUSTLE mirrors that path,
>   entering from top-right, sweeping down through the same compass,
>   exiting bottom-left.
> - They weave through a **central gold compass emblem** with a
>   4-point star at its heart — the "AI node" — the point where
>   soul and hustle become infinite.
>
> Palette: black `#050505`, gold `#C9A033` + `#F2C95C`, platinum silver,
> accent teal `#14B8A6`. NO RED. Luxury fintech meets street hustle.
> Bloomberg terminal aesthetic with gold accents.

---

## PROMPT 1 — HIGGSFIELD AI (text → image, cinematic image model)

**Use case:** Master 1:1 logo mark for brand identity, pitch decks, profile pics.
**Access:** https://higgsfield.ai (Edwin's account)
**Settings:** 1:1 aspect ratio, image mode (not video), high quality.

```
Luxury fintech logo design, vertical composition, pure black background #050505,
central emblem of a gold astrolabe compass with a glowing 4-point star at its
heart, two flowing ribbon arcs forming an infinite S shape weaving through the
compass — one arc in rich gold #C9A033 with soft highlight #F2C95C labeled
"SOUL", the other in polished platinum silver labeled "HUSTLE", both arcs end
in subtle arrow points, faint astrolabe tick marks radiating around the compass,
subtle Bloomberg-terminal grid background at 8% opacity, cinematic rim lighting,
premium editorial quality, symmetric and balanced, clean vector aesthetic,
luxury financial brand identity, minimal and unforgettable, 8k detail,
NO red, NO text, NO typography
```

**Negative prompt:**
```
red, blue, stock photo, generic saas, flat gradient, emoji, illustration,
3d render, cartoon, anime, watermark, signature, text, letters, logo text
```

---

## PROMPT 2 — OPENART.AI (Flux model)

**Use case:** High-detail logo mark generation, character-consistent across variants.
**Access:** https://openart.ai (Edwin's account)
**Recommended model:** **Flux 1.1 Pro** or **Flux Dev**

```
SoulHustleAI logo, square 1:1 composition, jet black background,
central gold astrolabe compass with glowing 4-point navigation star at its core,
radiant gold glow around the compass center, two ribbon-like arcs weaving
through the compass forming a Möbius infinity S — the top arc rich metallic gold
gradient (#F7DB7A to #C9A033), the bottom arc polished platinum silver
(#F5F5F5 to #5A5A5A), small arrow points at the arc ends suggesting
continuous flow, delicate astrolabe tick marks around the outer ring,
subtle radial grid pattern in gold at 10% opacity, cinematic rim light from
above, luxury fintech brand identity, premium editorial look, symmetric
Bloomberg-terminal aesthetic, vector art style, clean minimal composition,
8k sharp detail, no red, no text, no typography, centered
```

**Reference image:** upload Edwin's v2 concept (`soulhustleai-infinite-s-v2.png`)
as a reference image with **~40% influence weight** to preserve the layout.

---

## PROMPT 3 — MIDJOURNEY V6 / V7

**Use case:** Stylized variants, thumbnail shots, moodboards.
**Access:** Discord Midjourney (Edwin's account)

```
luxury fintech logo identity for SoulHustleAI automation agency,
central gold astrolabe compass with glowing 4-point star, two flowing
ribbon arcs forming a vertical infinite S around the compass, top arc
gold soul energy, bottom arc silver hustle energy, faint tick marks,
radial gold glow, pure black background, Bloomberg terminal aesthetic,
minimal vector art, premium editorial quality, symmetric composition,
no red no text --ar 1:1 --style raw --s 500 --q 2
```

Variants to try in parallel:
- Replace `--style raw` with `--style cute` for softer feel
- Add `--chaos 15` for more variant diversity
- Add `--weird 25` for edgier interpretations

---

## PROMPT 4 — FLUX PRO (via fal.ai, Replicate, or direct HF)

**Use case:** Pure vector-looking mark, best for clean logo output.
**Access:** https://fal.ai/models/fal-ai/flux/pro OR https://replicate.com

```
vector logo design, SoulHustleAI, luxury black and gold brand identity,
central gold compass emblem with 4-point star, two curved ribbons forming
an infinite S, gold ribbon (soul) and silver ribbon (hustle), astrolabe
tick marks, Bloomberg terminal background, premium minimal aesthetic,
flat vector style, 1:1 square, no text, no typography, no red
```

**Fal.ai settings:**
- Image size: 1024x1024
- Num inference steps: 28
- Guidance scale: 3.5
- Output format: PNG

---

## PROMPT 5 — STABLE DIFFUSION XL (open-source, HuggingFace)

**Use case:** Local/free runs, batch variation generation.
**Access:** https://huggingface.co/spaces/stabilityai/stable-diffusion-xl

```
luxury logo design, soulhustleai automation agency, central gold compass
emblem with glowing 4-point star, two ribbon arcs forming a möbius infinite
S, gold ribbon on top, silver ribbon on bottom, black background, bloomberg
terminal aesthetic, premium fintech brand identity, minimal vector art,
symmetric 1:1 square composition, cinematic lighting, 8k detail, no text
```

**Negative:** `red, text, typography, watermark, signature, low quality, blurry, saas, generic`

---

## PROMPT 6 — GOOGLE IMAGEN 3 (via Vertex AI or Gemini)

**Use case:** Highest text-compliance if you want the wordmark IN the image.
**Access:** https://gemini.google.com or Vertex AI

```
Professional luxury brand logo for SoulHustleAI, a premium AI automation
agency. Central element: a gold compass emblem with a glowing 4-point star.
Two flowing arcs forming a Möbius infinity S — one rich gold labeled 'SOUL',
one polished silver labeled 'HUSTLE'. Below: the wordmark 'SoulHustleAI' in
elegant Cinzel serif font — 'Soul' in gold, 'Hustle' in white, 'AI' in teal.
Subtitle 'AUTOMATION AGENCY' in small spaced caps. Pure black background.
Luxury fintech aesthetic. Bloomberg terminal grid subtle in background.
Minimal, memorable, symmetric. Square 1:1 composition. No red.
```

---

## 🎬 BONUS — SEEDANCE 2.0 (for animated logo reveal)

**Use case:** 5-second animated logo intro for YouTube/website hero.
**Access:** via fal.ai — https://fal.ai/seedance-2.0
**Input:** the best still image from Prompts 1-6 above

```
Seedance text-to-video input:
"The SoulHustleAI logo materializes: first the central gold compass
emerges from darkness, tick marks rotating into place with a subtle
gold glow. The 4-point star ignites at the core, emitting a warm
pulse. Then two ribbons — gold from top-left, silver from bottom-right
— sweep in and weave through the compass, forming a Möbius infinity S.
Final hold: the completed logo with the wordmark fading in below.
5 seconds, luxury fintech aesthetic, cinematic, 2K resolution,
black background, no sound."
```

---

## 📋 GENERATION WORKFLOW (tonight)

1. **Pick a tool** you have easy access to (Higgsfield or OpenArt are fastest)
2. **Paste Prompt 1** (or the one matching your tool)
3. **Generate 4–8 variants** (most tools let you batch)
4. **Download the top 2**
5. **Drop them in this repo** at `brand/logo/generated/`
6. **Tell me which one wins** and I'll:
   - Trace it to SVG if needed
   - Build the horizontal lockup, icon variants, and color variations
   - Update the command-center dashboard + website with the new logo
   - Regenerate all 5 thumbnails for the YT scripts

---

## 🔑 ALTERNATIVE — Give me API keys, I'll call the tools directly

If you want me to fully automate this without you clicking anything:

Drop ONE of these into `system_config` and I'll write a Python script that
generates + saves variants automatically:

- `fal_ai_api_key` → I'll call fal.ai's Flux/Seedance endpoints directly
- `openart_api_key` → I'll call OpenArt
- `higgsfield_api_key` → I'll call Higgsfield
- `huggingface_token` → I'll call Flux via HF Inference API (free tier available)
- `replicate_api_token` → I'll call Replicate (Flux, SDXL, many models)

Command to add:
```sql
INSERT INTO system_config (key, value)
VALUES ('fal_ai_api_key', '"YOUR_KEY_HERE"')
ON CONFLICT (key) DO UPDATE SET value = EXCLUDED.value;
```

Once it's in place, run `soulhustleai/scripts/logo_generate.py` and you'll
get a fresh set of logo PNGs in `/brand/logo/generated/` within 60 seconds.

---

## ⚠️ WHAT'S CURRENTLY IN THE REPO

The files in `/brand/logo/`:
- `shai_infinite_s_v3_master.svg` — **placeholder**, hand-coded, readable but not
  production-final. Keep for now, replace when a real generation lands.
- `shai_icon_only.svg` — **placeholder**
- `shai_horizontal_lockup.svg` — **usable as-is**, wordmark renders clean
- `shai_logo_v1.svg` — **legacy v1**, pre-Infinite-S (the Z mark), clean
- `zero_email_header.svg` — **usable**, separate email-specific header

**The horizontal lockup and v1 are the most polished right now.**
**Everything else is scaffolding until the real generation lands.**
