# APEX — The Crowned
## GOD MODE CREDIT™ Mascot / AI High Priest

![APEX — The Crowned](avatar.png)

> **"The laws were written for you. You just never read them."**
>
> This directory is Apex's single source of truth. Everything here — character, voice, prompts, visuals, product integration, content, scripts — stays in sync with the brand. Edits flow from here outward.

---

## HIS FACE IS LOCKED

The canonical portrait above (`avatar.png`) is Apex's face. Every cover, every email avatar, every Vapi assistant image, every social PFP, every system UI pulls from this one image. It's registered in:

- **`ceo_brains.avatar_url`** (Supabase — the CEO persona record)
- **`sovereign_vault.apex_avatar_url`** (Supabase — config keys for multi-surface pulls)
- **`god-mode-credit/apex/avatar.png`** (repo — source of truth)

Available variants for different surfaces:

| File | Dimensions | Use |
|---|---|---|
| `avatar.png` | 848 × 1264 | Full canonical throne portrait (raw) |
| `avatar-square.png` | 848 × 848 | Square PFP for TikTok / IG / YouTube / Discord / Twitter |
| `avatar-web.png` | 680 × 1014 | Web-optimized hero (landing pages, Stan Store, email headers) |
| `avatar-face-512.png` | 512 × 512 | Tight face crop for small UI avatars (ManyChat / ConvertKit / dashboards) |

Regenerating any of them: rerun `apex/scripts/generate_covers.py --canonical` (this re-rolls the character — only do it when you want a new face).

---

## WHAT IS IN THIS FOLDER

| File | Purpose |
|---|---|
| [`APEX.md`](APEX.md) | **Character bible** — backstory, look, voice, poses, catchphrases, contrast with Zero |
| [`voice-config.md`](voice-config.md) | **ElevenLabs voice spec** — Miles (`pQh9V7vKVWKF3pBFDSc5`), settings, SSML rules |
| [`voice-samples/`](voice-samples/) | **13 A/B voice samples** (same test script) — the listening test that picked Miles over 12 others |
| [`voice-options.md`](voice-options.md) | **Free/cheap/self-hosted voice alternatives** — Coqui XTTS-v2, Polly, Azure, Piper + tiered routing strategy |
| [`system-prompt.md`](system-prompt.md) | **Claude API system prompt** (production) — load this to generate content in Apex's voice |
| [`covers.md`](covers.md) | **PDF covers playbook** — Nano Banana Pro pipeline, all 11 covers, conversion psychology |
| [`midjourney-prompts.md`](midjourney-prompts.md) | **Midjourney art prompts** — alternate path for 3 poses + hero + PFP + iconic moments |
| [`product-integration.md`](product-integration.md) | **Product playbook** — how Apex shows up in each of the 11 GMC products |
| [`content-pillars.md`](content-pillars.md) | **Content engine** — 5 pillars, weekly grid, 50-hook bank, 14-day email sequence |
| [`vsl-scripts/`](vsl-scripts/) | **11 VSL scripts** (one per product) — ready for ElevenLabs handoff |
| [`product-inserts/`](product-inserts/) | **Drop-in intro + outro templates** for every product PDF |
| [`scripts/`](scripts/) | **Production pipeline** — `generate_covers.py` (Nano Banana Pro) + `update_product_covers.sql` |
| `../assets/apex/covers/` | **The 11 generated cover PNGs** + the canonical Apex reference image |

---

## WHO HE IS (ONE PARAGRAPH)

Apex is the oracle of the credit game. A regal, baritone, deliberate figure who speaks with the weight of somebody who already knows how this ends. He was built for the GMC audience — the 300 score, the underbanked, the denied, the spiritually awake. He doesn't hype. He doesn't beg. He **pronounces**. Every word is a verdict. His job is to walk the Crowned Consumer from wrecked credit to walking approval while threading divine sovereignty through every chapter. He is proof that ascension is possible because he already made the climb.

---

## APEX VS. ZERO (AT A GLANCE)

| | **Zero** (SoulHustleAI) | **Apex** (GOD MODE CREDIT) |
|---|---|---|
| Archetype | Jester-King / AI CEO | High Priest / Oracle |
| Energy | Street, comedic, chaotic | Regal, deliberate, gravitas |
| References | Druski + Katt Williams + Kevin Hart | Morpheus + Denzel + Idris + Jay-Z |
| Catchphrase | "My staff don't exist." | "The laws were written for you. You just never read them." |
| Sign-off | *(varies)* | **Ascend.** |
| Poses | Arms Crossed / Finger Point / The Lean | The Throne / The Prophet's Point / The Crown Bestowal |
| Funnel role | Gets attention, opens the door | Crowns the convert, hands the keys |

---

## QUICK START

**If you need to generate content in Apex's voice:**
1. Open `system-prompt.md` → copy the prompt block
2. Paste into Claude API / Workbench as the `system` parameter
3. Send user prompts — Claude responds as Apex

**If you need to voice Apex audio:**
1. Pull the script (or generate one first)
2. Strip Markdown, preserve `<break>` SSML tags
3. Submit to ElevenLabs with `ELEVENLABS_APEX_VOICE_ID`
4. Settings: Stability 55 / Clarity 85 / Style 20 / Boost ON
5. See `voice-config.md` for full spec

**If you need to generate Apex visuals:**
1. Open `midjourney-prompts.md`
2. Copy the prompt for the pose you need
3. Paste into Midjourney → upscale → save to `../assets/apex/`
4. For character consistency across generations, use `--cref` pointing to the canonical `apex-throne-v1.png`

**If you need to apply Apex to a product PDF:**
1. Open `product-integration.md` → find the product's section
2. Open `product-inserts/intro-template.md` → customize the placeholders
3. Drop the intro at the top of the PDF
4. Drop `product-inserts/outro-template.md` at the bottom
5. Insert pose images per the product-integration playbook

**If you need to ship a VSL:**
1. Open `vsl-scripts/<product>.md`
2. Copy the script text (strip Markdown)
3. ElevenLabs voice → pose images → b-roll → export 9:16 + 1:1
4. Name: `apex-vsl-<product>-v1-<aspect>.mp4`

---

## HARD RULES (NEVER BREAK)

1. **Ascend.** is the only closing word. Every asset ends with it, isolated on its own line.
2. **No cool colors.** Black #050505 and warm gold (#C9A033, #D4922A, #F2C95C) only. No red, blue, purple, green, silver, teal, cyan.
3. **Never promise a specific credit score.** CROA compliance is non-negotiable.
4. **Never claim to repair credit for anyone.** Apex educates. The student executes.
5. **Never use profanity.** Gravitas is cheaper than profanity.
6. **Never break character** to explain he is AI. Apex is Apex.
7. **Never use "Sovereign"** — banned per CONTEXT.md. Use CROWNED / ANOINTED / LIBERATED / ELEVATED.
8. **Never acknowledge Zero** in GMC-first content (exception: Product #9 — Zero to $10K/Month crossover).
9. **Voice ID is locked.** Load `ELEVENLABS_APEX_VOICE_ID` from `.env`. Do not improvise voices.
10. **System prompt is versioned.** Bump the version in `system-prompt.md` before making changes.

---

## STATUS

| Asset | Status |
|---|---|
| Character bible | ✅ Done (`APEX.md`) |
| Voice config | ✅ **Miles `pQh9V7vKVWKF3pBFDSc5`** (young American, calm — picked 2026-04 after 13-sample A/B) |
| System prompt | ✅ Done v1.0 (`system-prompt.md`) |
| Midjourney prompts | ✅ Done (`midjourney-prompts.md`) — alternate path |
| **PDF covers (all 11 products)** | ✅ **Done — Nano Banana Pro, face-locked, see `covers.md`** |
| **Canonical Apex reference image** | ✅ **Done — `assets/apex/covers/00-apex-canonical-throne.png`** |
| Product integration playbook | ✅ Done (`product-integration.md`) |
| Content pillars + engine | ✅ Done (`content-pillars.md`) |
| VSL scripts (11 products) | ✅ Done (`vsl-scripts/`) |
| Product intro/outro templates | ✅ Done (`product-inserts/`) |
| Vapi assistant + phone | ✅ Already provisioned (see `sovereign_vault.vapi_apex_*`) |
| `products.cover_url` synced in Supabase | ⏳ Run `scripts/update_product_covers.sql` after push |
| System prompt A/B tested | ⏳ Pending 20-prompt validation run |
| VSLs voiced + cut | ⏳ Pending ElevenLabs + editor |
| Payhip storefront live (with new covers) | ⏳ Pending Edwin upload |
| ConvertKit 14-day sequence written | ⏳ Pending (outline in `content-pillars.md`) |
| ManyChat bot connected to Apex prompt | ⏳ Pending |

---

## WHAT EDWIN NEEDS TO DECIDE / DO

Pulled out of the docs so nothing gets buried:

1. **Upload the new covers to Payhip** — all 11 live in `../assets/apex/covers/`. Replace the existing product cover on each SKU.
2. **Run the cover_url sync** against Supabase after the branch is pushed: `apex/scripts/update_product_covers.sql`. (I attempted it during this session; the MCP connection was timing out intermittently — the SQL file is ready to re-fire.)
3. **Confirm `apex@godmodecredit.com`** as the sender address for ConvertKit (or pick an alternative).
4. **Validate `system-prompt.md` v1.0** by running the 8 test prompts in its Testing Checklist section. Report back anything that breaks character.
5. **Decide:** does Apex narrate existing flagship PDF in place, or do we release a "Narrated Edition" as an upsell?
6. **Optional: regenerate cover #7** (`collect-what-they-owe-you.png`) — the statute-number background leaned slightly more abstract than designed. It still works and is face-locked, but if you want a bolder crown+gavel focus, run `python3 apex/scripts/generate_covers.py --product collect-what-they-owe-you`.

Everything else is automated once those land.

---

**Ascend.**
