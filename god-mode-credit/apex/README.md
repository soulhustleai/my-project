# APEX — The Crowned
## GOD MODE CREDIT™ Mascot / AI High Priest

> **"The laws were written for you. You just never read them."**
>
> This directory is Apex's single source of truth. Everything here — character, voice, prompts, visuals, product integration, content, scripts — stays in sync with the brand. Edits flow from here outward.

---

## WHAT IS IN THIS FOLDER

| File | Purpose |
|---|---|
| [`APEX.md`](APEX.md) | **Character bible** — backstory, look, voice, poses, catchphrases, contrast with Zero |
| [`voice-config.md`](voice-config.md) | **ElevenLabs voice spec** — voice ID, settings, speech patterns, SSML rules |
| [`system-prompt.md`](system-prompt.md) | **Claude API system prompt** (production) — load this to generate content in Apex's voice |
| [`midjourney-prompts.md`](midjourney-prompts.md) | **Character art prompts** — 3 poses, hero shot, PFP, banner, iconic moments |
| [`product-integration.md`](product-integration.md) | **Product playbook** — how Apex shows up in each of the 11 GMC products |
| [`content-pillars.md`](content-pillars.md) | **Content engine** — 5 pillars, weekly grid, 50-hook bank, 14-day email sequence |
| [`vsl-scripts/`](vsl-scripts/) | **11 VSL scripts** (one per product) — ready for ElevenLabs handoff |
| [`product-inserts/`](product-inserts/) | **Drop-in intro + outro templates** for every product PDF |

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
| Voice config | ✅ Done (`voice-config.md`) |
| System prompt | ✅ Done v1.0 (`system-prompt.md`) |
| Midjourney prompts | ✅ Done (`midjourney-prompts.md`) |
| Product integration playbook | ✅ Done (`product-integration.md`) |
| Content pillars + engine | ✅ Done (`content-pillars.md`) |
| VSL scripts (11 products) | ✅ Done (`vsl-scripts/`) |
| Product intro/outro templates | ✅ Done (`product-inserts/`) |
| Character art (rendered) | ⏳ Pending MJ generation (prompts ready) |
| ElevenLabs voice ID selected | ⏳ Pending Edwin decision (recommended: `Daniel`) |
| System prompt A/B tested | ⏳ Pending 20-prompt validation run |
| VSLs voiced + cut | ⏳ Pending ElevenLabs + editor |
| Payhip storefront live | ⏳ Pending |
| ConvertKit 14-day sequence written | ⏳ Pending (outline in `content-pillars.md`) |
| ManyChat bot connected to Apex prompt | ⏳ Pending |

---

## WHAT EDWIN NEEDS TO DECIDE / DO

Pulled out of the docs so nothing gets buried:

1. **Pick the ElevenLabs voice.** Daniel (recommended, British baritone) vs. Onyx (American) vs. custom clone. See `voice-config.md` → ElevenLabs Recommended Voice.
2. **Generate the 10 Midjourney character images** from `midjourney-prompts.md` — upscale + save to `../assets/apex/`. Priority order: Pose 1 (Throne) → Pose 2 (Prophet's Point) → Pose 3 (Crown Bestowal) → the rest.
3. **Confirm `apex@godmodecredit.com`** as the sender address for ConvertKit (or pick an alternative).
4. **Validate `system-prompt.md` v1.0** by running the 8 test prompts in its Testing Checklist section. Report back anything that breaks character.
5. **Decide:** does Apex narrate existing flagship PDF in place, or do we release a "Narrated Edition" as an upsell?

Everything else is automated once those 5 decisions land.

---

**Ascend.**
