# Zero YT — Production Pipeline
## From written script to published video — the exact toolchain

> **Goal:** 1 long-form + 3 shorts per batch day (Sunday)
> **Total time per batch day:** ~4 hours
> **Tools:** ElevenLabs + Zero avatar + InVideo AI (or CapCut) + TubeBuddy + Later.com

---

## The 7-Stage Pipeline

```
┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐
│ 1. SCRIPT│──▶│ 2. VOICE │──▶│ 3. B-ROLL│──▶│ 4. EDIT  │──▶│ 5. THUMB │──▶│ 6. SEO   │──▶│ 7. UPLOAD│
└──────────┘   └──────────┘   └──────────┘   └──────────┘   └──────────┘   └──────────┘   └──────────┘
   written     ElevenLabs     Zero avatar      CapCut /      fal.ai /      TubeBuddy       YouTube +
   in repo     Orlando        + InVideo AI     InVideo AI    Figma         + Later.com     social dist
```

---

## STAGE 1 — Script (already done)

All scripts live in:
- `zero-yt/scripts/zero-quickfire-intro.md`
- `zero-yt/scripts/long-form/*.md`
- `zero-yt/scripts/shorts/*.md`

**Before rendering audio, final pass:**
- Read it OUT LOUD once. If anything trips your tongue, rewrite it.
- Count laughs — each long-form needs MINIMUM 5 laugh moments.
- Count receipts — each long-form needs MINIMUM 3 specific numbers.
- Confirm the CTA is in there 2x (soft mid-video + hard at end).

---

## STAGE 2 — Voice (ElevenLabs)

### Setup (one-time)
- ElevenLabs account: `edwin@soulhustleai.com`
- Voice: **Orlando** — `4t8HWMowRF0NaJl0r9MS`
- Settings (LOCKED — never change):
  - Stability: **0.42**
  - Similarity boost: **0.9**
  - Style exaggeration: **0.52**
  - Speaker boost: ON

### Render process
1. Open ElevenLabs Studio → new project
2. Paste the script (one block per natural paragraph)
3. Preview each block — re-roll any that mispronounce "SoulHustleAI" or numbers
4. Export as **MP3 128kbps** (upgrade to WAV for editing)
5. Save as `zero-yt/assets/audio/long-01.mp3`, `long-02.mp3`, etc.

### Pronunciation hacks (use these in scripts)
| If ElevenLabs mispronounces... | Write it as... |
|--------------------------------|----------------|
| SoulHustleAI | Soul Hustle A.I. |
| VAPI | V.A.P.I. |
| Twilio | Twill-io |
| n8n | n-eight-n |
| ROI | R.O.I. |
| 929-236-1567 | nine-two-nine, two-three-six, one-five-six-seven |
| $1,497 | fourteen ninety-seven |

### Batch render time
- Long-form (6-7 min): ~15 min render + 10 min review
- Short (30-45s): ~3 min render + 2 min review

---

## STAGE 3 — B-roll / Visuals

### Zero avatar (static)
- **Source of truth:** `zero_avatar_url` in Supabase `system_config`
- **Local backup:** `brand/avatar/zero_social_avatar.svg`
- **Never** use a random stock character. Always Zero.

### Zero avatar (animated — for intros/outros)
Use one of these tools to animate the static JPEG:
- **D-ID** (easiest, realistic lip sync)
- **HeyGen** (higher quality, subscription required)
- **fal.ai** (for Midjourney-style stylized motion)

Prompt for animated Zero:
```
Animate this character: slight head nod, subtle visor glint animation,
minimal mouth movement for voiceover sync, gold particle aura around
head, 5-second loop, black background, no body movement below neck
```

### Screen recordings (for Video 03 live build)
- **OBS Studio**, 1920x1080, 60fps
- Hide any sensitive info (API keys, account names) with a gold square
- Add subtle cursor click SFX (free Freesound.org "click" pack)
- Zoom in on the important action every 10 seconds

### Charts + data visualizations
- **Figma** — build a chart template once, reuse forever
- Gold bars on black background
- Cinzel font for labels
- Animate reveals in CapCut/InVideo

### Midjourney prompts for b-roll
```
1. "Bloomberg terminal with gold text overlay, dark room, dramatic lighting, luxury fintech aesthetic --ar 16:9 --s 300"
2. "Abstract gold particles swirling around a dark orb, infinity symbol, black background, cinematic --ar 16:9"
3. "Dollar bills floating out of a glowing gold compass, dark room, luxury --ar 16:9 --s 250"
4. "NYC rooftop at night with gold city lights, cinematic wide shot, Blade Runner aesthetic --ar 16:9 --s 300"
```

---

## STAGE 4 — Edit

### Tool: CapCut (free) or InVideo AI (paid — faster)

### Long-form edit structure
1. **Import** the ElevenLabs audio → audio track
2. **Slice** the audio at every natural pause (creates "cards")
3. **Drop** b-roll / charts / Zero avatar on video track 1
4. **Add** gold text overlays on video track 2 using the Cinzel font (or Georgia as fallback)
5. **Add** subtle background music on audio track 2 (lofi beat, -18dB)
6. **Add** cursor/chart SFX on audio track 3
7. **Export:** 1920x1080, H.264, 30fps, 8Mbps bitrate

### Shorts edit structure
1. Import the short audio (~45s)
2. Drop the Zero avatar as the background layer (full-screen 1080x1920)
3. Add the script as captions (CapCut auto-caption feature, manually edit)
4. Gold hook text at the top, bold Cinzel
5. Subtle gold Bloomberg grid overlay at 10% opacity
6. Export: **1080x1920, 30fps, 45s max**

### Editing time
- Long-form (6-7 min): ~90 minutes
- Short (30-45s): ~15 minutes

---

## STAGE 5 — Thumbnails

### Tool: Figma (template-driven)

### Long-form thumbnail template
- 1280x720px
- Left 60%: Zero avatar with a specific emotion (smirk / raised eyebrow / dead stare)
- Right 40%: headline in Cinzel Bold, gold `#F2C95C`, 110px
- One teal accent element (arrow, circle, stat callout)
- Bloomberg grid background
- Optional: ONE red circle around a stat (thumbnail only — never in video)

### Shorts thumbnail
- Auto-select from first frame — make sure the first frame is hook text
- 1080x1920 first-frame = 2 words in huge Cinzel

### CTR target
- Long-form: 8%+ is good, 12%+ is great
- Anything under 4% → retire the thumbnail, retry

---

## STAGE 6 — SEO

### Tool: TubeBuddy or VidIQ (browser extension)

### For each video:
1. **Title:** `[Shocking Stat] + [Solution] + [For Who]`
   - ✅ "I Did The Math. Your Service Business Is Leaking $18,500/mo."
   - ❌ "How to Automate Your Business"
2. **Description:** paste from the script's upload description block
3. **Tags:** use TubeBuddy's keyword explorer for 10-15 relevant tags
4. **End screen:** link to the next video + subscribe
5. **Cards:** link to `soulhustleai.com/apply.html`
6. **Chapters:** add timestamps from the script

### SEO target keywords (prioritize these)
- ai receptionist for small business
- missed call text back
- service business automation
- vapi tutorial
- n8n real world
- make.com vs n8n

---

## STAGE 7 — Upload & Distribution

### Primary: YouTube
- Upload as **Unlisted** first
- Let the processing finish (usually 2–5 min for HD)
- Preview everything once
- Change to **Public**
- Post in the Community tab within 1 hour

### Cross-platform distribution (one video → 12 pieces of content)

| Platform | Format | Source material |
|----------|--------|-----------------|
| YouTube long-form | 6–8 min horizontal | Master edit |
| YouTube Shorts | 45s vertical | 3 cuts from long-form |
| TikTok | 45s vertical | Same 3 cuts |
| Instagram Reels | 45s vertical | Same 3 cuts |
| IG Feed post | Static gold quote card | 1 killer line from script |
| LinkedIn post | 800-word essay | Summary of video |
| Twitter/X thread | 8-tweet thread | Key numbers + 1 clip |
| Newsletter section | 300-word TLDR | With CTA link |

### Scheduling tool: **Later.com** (Starter, $18/mo)
- Batch upload every Sunday
- Schedule across Tue/Thu/Sat for long-form
- Schedule daily M–F for shorts
- Set Zero's avatar + brand colors in Later profile

---

## Weekly Cadence (steady state — after launch)

| Day | Task |
|-----|------|
| Sunday 10am–2pm | **BATCH DAY** — render audio, edit 1 long-form + 5 shorts, upload to Later |
| Monday 9am | Later.com auto-publishes first short |
| Tuesday 12pm | Later.com auto-publishes long-form #1 + short #2 |
| Wednesday 9am | Short #3 |
| Thursday 12pm | Long-form #2 (second long-form per week) |
| Friday 9am | Short #4 |
| Saturday 12pm | Short #5 + community poll post |

---

## Quality Gate (before publishing anything)

- [ ] Audio has no awkward pauses or robot pronunciations
- [ ] Zero avatar is the canonical one (not a random AI generation)
- [ ] Thumbnail CTR-tested (A/B via TubeBuddy if possible)
- [ ] Title includes 1 specific number
- [ ] Description has phone, apply link, ROI calc link
- [ ] Timestamps added
- [ ] Tags filled
- [ ] End screen + cards set
- [ ] Community post scheduled
- [ ] UTM params in all outgoing links

If any of these are missing → DO NOT publish. Fix it.

---

**This pipeline runs on rails once it's dialed in. Sunday batch → whole week published.**
