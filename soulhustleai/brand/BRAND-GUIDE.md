# SoulHustleAI — Brand Guide
## Single source of truth for the logo, Zero, and visual system

> **Status:** Live. All new SHAI assets MUST match this guide.
> **Source of record:** this file + `/brand/` SVGs + `system_config.pomelli_brand_dna_profiles` + `system_config.youtube_zero_strategy`
> **Updated:** 2026-04-13

---

## 1. The Story In One Sentence

**Soul meets hustle. Tech makes it infinite.**

The logo is a Möbius-style "Infinite S" — a gold arc (SOUL) and a silver arc (HUSTLE) weaving through a central gold compass. The compass is the AI — the thing that makes the cycle never end.

---

## 2. Palette (LOCKED)

| Role | Hex | Use |
|------|-----|-----|
| **Background black** | `#050505` | Every background. Never true black (`#000`). |
| **Primary gold** | `#C9A033` | Logo, CTAs, Zero accents. |
| **Gold highlight** | `#F2C95C` | Hover states, glows, top of gradients. |
| **Gold shadow** | `#8A6A1E` | Bottom of gradients, depth. |
| **Silver (hustle)** | `#BDBDBD` → `#5A5A5A` | Hustle arc only. Never use on text. |
| **Teal accent** | `#14B8A6` | "AI" in wordmark, Zero's signature color. |
| **Teal bright** | `#2DD4BF` | Hover states for teal CTAs. |
| **Text primary** | `#F5F2E8` | Body text on black. |
| **Text muted** | `#8a8577` | Metadata, subtitles. |
| **NEVER** | red of any kind, pure `#FFFFFF`, pure `#000000`, blue |

Gradient definition (use consistently):
```
gold:   #F7DB7A → #F2C95C → #C9A033 → #8A6A1E
silver: #F5F5F5 → #BDBDBD → #5A5A5A
teal:   #2DD4BF → #0F766E
```

---

## 3. Fonts (LOCKED)

| Role | Family | Fallback | Where |
|------|--------|----------|-------|
| Display / headlines | **Cinzel** (600/700) | Georgia, serif | Logo, H1, section titles |
| UI / body | **Space Grotesk** (400/500/600) | Inter, system-ui | Site UI, buttons, body |
| Mono / data | **DM Mono** / JetBrains Mono (400/500) | Courier New | Code, metrics, taglines |
| Editorial pull quote | Cormorant Garamond (italic 400) | Georgia italic | Long-form quotes only |

Use `@import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@600;700&family=Space+Grotesk:wght@400;500;600;700&family=DM+Mono:wght@400;500&display=swap')`

---

## 4. Logo Files — When To Use Which

| File | Size | Use For |
|------|------|---------|
| `logo/shai_infinite_s_v3_master.svg` | 1200x1200 | Master reference. Keynote / pitch decks / posters. |
| `logo/shai_icon_only.svg` | 512x512 | App icon, favicon, social profile pic, tiny sizes. |
| `logo/shai_horizontal_lockup.svg` | 1600x400 | Email headers, website nav, YouTube banner. |
| `logo/shai_logo_v1.svg` | 600x200 | LEGACY. Only use for continuity with pre-v3 assets. |
| `logo/zero_email_header.svg` | 240x64 | Outbound email header (keep for email lineage). |

### Logo Rules
- ✅ Always on `#050505` or near-black
- ✅ Always keep the compass core visible (it's the "AI")
- ✅ Keep 15% clear space around the icon minimum
- ❌ No recoloring the gold (that's the brand DNA)
- ❌ No horizontal stretching
- ❌ No drop shadows on flat surfaces (the logo has its own glow)
- ❌ No emboss, bevel, or 3D effects

---

## 5. Zero — The Character

### Visual (canonical)
> "Dark-skinned Black man, powerful build, gold reflective visor bar across
> eyes, thick gold Cuban link chain, black oversized hoodie under black
> tailored blazer, gold particle aura, NYC energy."

### Title
**Zero, C.E.O. of Soul Hustle A.I. — Godfident Collective**

### Voice
- **ElevenLabs Orlando** — `4t8HWMowRF0NaJl0r9MS`
- Settings: stability `0.42`, similarity_boost `0.9`, style `0.52`
- Character: deep, bold, Brooklyn CEO cadence

### Personality
> "The ghost in the machine. Never sleeps, never misses, never forgets.
> Speaks with calm authority. Not a tech bro — a strategic operator.
> Luxury consultant energy meets street-smart hustle."

### Catchphrases (canon — use these verbatim)
- "My staff don't exist."
- "We don't build funnels. We deploy revenue infrastructure."
- "Your business has a pulse. We make it unstoppable."
- "Same leads. Better systems."
- "That's not a marketing problem. That's a systems problem."
- "Ship it."
- "Automate or die."
- "Clients don't wait."
- "Systems over motivation."
- "While you was hiring, I was automating. Respectfully."

### Never
- Never hype
- Never shout
- Never beg
- Never use stock footage
- Never corporate speak
- Never "maybe" / "probably" / "soon"

---

## 6. Zero's Avatar — Canonical Source

### Live (scraped from YT channel — already published)
URL: `https://yt3.googleusercontent.com/hwQsGJPyGpXo7uImg_WtWe_acjMvsTfSkn9A46D4xuOPJaiGZb50k-xI_6L81uTRCzfdMPtG=s400-c`

Stored in `system_config`:
- `zero_avatar_url` — full URL above
- `zero_avatar_b64` — full JPEG base64 (backup)
- `zero_avatar_svg_b64` — simplified SVG mark (saved to `/brand/avatar/zero_avatar_mark.svg`)

### Vector fallback
`/brand/avatar/zero_social_avatar.svg` — 800x800 visor-bars SVG (use when the real JPEG can't render)

### Character generation prompt (Midjourney / fal.ai)
```
portrait of Zero, dark-skinned Black man, powerful build, gold
reflective visor bar across eyes glowing faintly, thick gold
Cuban link chain, black oversized hoodie under black tailored
blazer, gold particle aura around head, NYC rooftop at night
in background, luxury fintech aesthetic, Bloomberg terminal
reflections in visor, photorealistic, cinematic key light from
above, dramatic shadow, --ar 1:1 --style raw --s 300
```

**Consistency rule:** Every Zero image across every platform MUST use the published JPEG OR be a new generation with the above prompt. No rando visor dudes.

---

## 7. Design Motifs

### Use these recurring motifs on any new SHAI asset:
1. **Gold ring + tick marks** (astrolabe / compass)
2. **Diagonal slash of gold light** (the "signal" — Zero's response time)
3. **Bloomberg terminal grid background** (subtle 1px gold at 6% opacity)
4. **Corner registration marks** (cinematic framing — see `shai_infinite_s_v3_master.svg`)
5. **4-point gold star** (the compass core — use as bullet points / loading state)

### Avoid
- Swooshy generic SaaS gradients
- Emoji
- Stock photos of handshakes, skyscrapers, arrows
- Isometric illustrations
- Neumorphism

---

## 8. Tone Of Voice

**Street philosopher meets automation genius. Confident, direct, never corporate.
Speaks like someone who already solved the problem.**

Rule of thumb: if your sentence could be written by a LinkedIn thought leader, rewrite it.

### Words we use
revenue infrastructure · speed to lead · dead database · the system · the stack · the mark · ghost in the machine · pulse · unstoppable · ship · deploy

### Words we don't
leverage · synergy · solution · empower · journey · ecosystem · platform · disruption · game-changer · optimize

---

## 9. Brand Health Audit (monthly)

Every first Monday of the month, walk the repo + live sites:
- [ ] Logo used correctly everywhere? (check all .html in repo)
- [ ] Palette consistent? (no rogue blues or reds)
- [ ] Zero's avatar identical across platforms?
- [ ] Fonts loading correctly? (check fallback chain)
- [ ] Tone check on the 5 newest pieces of copy
- [ ] Update this file if anything changes

---

**The brand is a compounding asset. Treat it like one.**
