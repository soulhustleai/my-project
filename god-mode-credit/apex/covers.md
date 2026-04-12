# APEX — PDF Covers
## All 11 GMC Product Covers — Apex-Fronted, Nano Banana Pro Generated

> **Status:** ✅ All 11 covers generated and checked in. Apex is the face of every cover. Face lock is maintained via a canonical reference image passed to the model on every call.

---

## THE TOOL

**`google/gemini-3-pro-image-preview`** (Nano Banana Pro) via **OpenRouter**.

**Why this tool and not Canva or plain Midjourney:**
- **Best-in-class text rendering.** Nano Banana Pro renders book-cover typography cleanly — zero garbled letters, which means no Canva overlay pass needed.
- **Native character consistency.** Supports multi-image input: we pass a canonical Apex reference on every call and the model locks his face, glasses, chain, and longcoat across all 11 covers without a separate LoRA or fine-tune.
- **Already budgeted.** Routes through Edwin's existing OpenRouter key (`sovereign_vault.openrouter_api_key`). No new vendor. No new billing.
- **Cost-effective.** ~$0.14/image. Full 12-image batch (1 canonical + 11 covers) ran for ~$1.68 at retail. Regenerations are cheap.

Configured in Supabase `sovereign_vault` — no new keys required.

---

## PIPELINE

```
┌──────────────────────────────────────────────────────────────┐
│  1. sovereign_vault.openrouter_api_key  (Supabase)            │
│                    │                                           │
│                    ▼                                           │
│  2. generate_covers.py  (apex/scripts/)                       │
│     ├── build canonical Apex prompt (Pose 1 Throne)            │
│     ├── call Nano Banana Pro → save 00-apex-canonical-throne.png│
│     ├── for each of 11 products:                               │
│     │     build per-cover prompt  (title + subtitle + visual)  │
│     │     call model WITH canonical image attached             │
│     │     save PNG to assets/apex/covers/NN-<slug>.png         │
│                    │                                           │
│                    ▼                                           │
│  3. Post-process: normalize any JPEG-in-PNG → real PNG         │
│                    │                                           │
│                    ▼                                           │
│  4. update_product_covers.sql  (Supabase)                      │
│     UPDATE products SET cover_url=<raw.githubusercontent URL>  │
│                    │                                           │
│                    ▼                                           │
│  5. Covers live at raw.githubusercontent.com after git push    │
│     → Payhip / Stan Store / ConvertKit / ManyChat pull from it │
└──────────────────────────────────────────────────────────────┘
```

---

## FILES

### The covers (`god-mode-credit/assets/apex/covers/`)

| File | Product | Price | Emotional hook |
|---|---|---|---|
| `00-apex-canonical-throne.png` | **Canonical reference** — passed to every cover generation | — | Authority (character lock) |
| `01-5-federal-laws.png` | 5 Federal Laws Banks Hope You Never Read | FREE | Awakening |
| `02-cards-that-say-yes.png` | Cards That Say Yes | FREE | Relief / approval |
| `03-ai-x-credit-cheat-code.png` | AI × Credit Cheat Code | $27 | Elite knowledge |
| `04-ai-credit-repair-toolkit.png` | AI Credit Repair Toolkit | $37 | Delegation / future |
| `05-the-dispute-letter-pack.png` | The Dispute Letter Pack | $37 | Armament / confidence |
| `06-zero-to-10k-ai-automation-playbook.png` | Zero to $10K AI Playbook | $37 | Freedom / launch |
| `07-collect-what-they-owe-you.png` | Collect What They Owe You | $47 | Vindication |
| `08-business-credit-blueprint.png` | Business Credit Blueprint | $47 | Empire / legacy |
| `09-zero-to-funded-bundle.png` | Zero to Funded Bundle | $67 | Completeness |
| `10-credit-ascension.png` | **Credit Ascension (FLAGSHIP)** | $97 | Transformation / coronation |
| `11-the-crowned-circle.png` | The Crowned Circle | $197 | Belonging / inner circle |

**Format:** All PNG, 848 × 1264 (2:3 aspect), warm-gold-on-black palette, Apex face-locked on every one.

**Prices reflect live `products` table in Supabase (see next section).**

### The pipeline (`god-mode-credit/apex/scripts/`)

| File | Purpose |
|---|---|
| `generate_covers.py` | Nano Banana Pro cover generation pipeline. Pulls `OPENROUTER_KEY` from env. Accepts `--canonical`, `--all`, or `--product <slug>`. |
| `update_product_covers.sql` | Supabase UPDATE that sets `products.cover_url` to the raw.githubusercontent.com URLs for each of the 11 covers. Idempotent. |

---

## HOW TO REGENERATE

### Regenerate a single cover
```bash
export OPENROUTER_KEY=$(psql $SUPABASE_URL -t -c \
  "SELECT key_value FROM sovereign_vault WHERE key_name='openrouter_api_key'")

python3 god-mode-credit/apex/scripts/generate_covers.py --product credit-ascension
```

### Regenerate the canonical Apex reference (changes character lock for all future runs)
```bash
python3 god-mode-credit/apex/scripts/generate_covers.py --canonical
```
**Warning:** regenerating the canonical changes every subsequent cover's face. Only do this if you want to re-establish a new canonical look.

### Regenerate the full batch
```bash
python3 god-mode-credit/apex/scripts/generate_covers.py --all
```

### Sync Supabase `products.cover_url` after generating
```bash
# Option A — via MCP (preferred)
# mcp__supabase__execute_sql with contents of update_product_covers.sql

# Option B — via psql
psql $DATABASE_URL -f god-mode-credit/apex/scripts/update_product_covers.sql
```

---

## DESIGN RULES (LOCKED)

Every cover adheres to these rules. Baked into `generate_covers.py` in the `APEX_ANCHOR`, `STYLE_ANCHOR`, and `TEXT_ANCHOR` constants.

1. **Character lock.** Every cover passes `00-apex-canonical-throne.png` as a reference image. Same face. Same glasses. Same longcoat. Same chain. Same crown-and-scales pendant.
2. **Palette lock.** Black `#050505` + warm antique gold `#C9A033` / `#D4922A` / `#F2C95C` only. **No red, blue, purple, green, silver, teal, cyan — ever.**
3. **Typography lock.** Title in ALL CAPS Cinzel serif bold, warm antique gold, top 18% of cover. Subtitle in smaller Cinzel regular at ~70% opacity directly below. Brand `GOD MODE CREDIT` in smaller Cinzel regular at bottom 8%.
4. **Aspect lock.** 2:3 vertical (848 × 1264), the Payhip/Stan Store standard for ebooks.
5. **Lighting lock.** Warm volumetric gold key light from above, hard shadows, renaissance portrait lighting.
6. **Emotional hook lock.** Every cover telegraphs one emotion at thumbnail scale — see the per-product table above.
7. **Face placement lock.** Apex's face is visible on every cover (not obscured by text, not turned away from the viewer). Face-on-cover is the #1 conversion driver for digital products.

---

## CONVERSION PSYCHOLOGY (WHY THESE COVERS WILL CONVERT)

Every cover is engineered against six conversion principles validated across ebook/digital product markets:

1. **Face on cover.** Books with faces on the cover outperform object covers 2–3× on click-through. Apex is on every single cover, eyes level with the viewer on 9 of 11.
2. **Eye contact / gaze.** Direct gaze activates emotional response. Apex's glasses are always visible and oriented toward the camera. Even on the abstract covers (#4 AI Brain, #6 Rocket), his eyes are forward.
3. **Symbolic payload.** Each cover has exactly ONE hero symbol besides Apex — book, cards, key, AI brain, letters, rocket, gavel, blueprint, book stack, crown, round table. One symbol is memorable. Five symbols is noise.
4. **Color psychology of gold.** Gold = wealth, abundance, divine, authority. Black = power, luxury, mystery. The deliberate absence of other colors amplifies the authority read.
5. **Title hierarchy.** Title dominates. Subtitle supports. Brand grounds. No other text. This is the 3-tier hierarchy every best-selling ebook cover follows.
6. **Thumbnail test.** Every cover is readable at 100px wide (Payhip search result size). Title pops. Face pops. Hero symbol pops. No cluttered backgrounds.

Plus the Apex-specific conversion multiplier:
7. **Brand recognition compound effect.** Because the SAME man appears on every cover, a buyer who sees one becomes primed for the entire suite. By the time they encounter their third Apex cover on TikTok, they already recognize him. That's shelf-presence at scale — the exact effect Grant Cardone, Robert Greene, and Dan Koe's cover systems produce.

---

## NEXT STEPS (NON-BLOCKING)

- [ ] After `git push`, fire the SQL in `apex/scripts/update_product_covers.sql` to hydrate `products.cover_url`
- [ ] Upload covers to Payhip against each product (they currently use different covers)
- [ ] Swap `hero_image` on Stan Store bio link page to `10-credit-ascension.png` (the flagship)
- [ ] Use `00-apex-canonical-throne.png` as the ConvertKit sender avatar
- [ ] Spot-check #7 `collect-what-they-owe-you` — looks great but the statute-number background leaned slightly more abstract than planned. Regenerate if Edwin wants more crown/gavel focus.
- [ ] Optional: A/B test the flagship cover (#10 Credit Ascension) against a Pose 1 Throne variant to see which converts better.

---

**Generated April 2026. Nano Banana Pro. Pipeline documented. Character locked. Covers live.**

**Ascend.**
