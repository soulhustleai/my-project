# 🔥 TONIGHT — Zero YT Launch Runbook
## Step-by-step from zero subs to first video live

> **Time budget:** 3.5 hours end-to-end
> **Prereqs:** Google account, ElevenLabs account, Canva/Figma, CapCut, Later.com (optional)
> **Goal by midnight:** First long-form video + 3 shorts live on the channel

---

## PHASE 0 — Verify the existing channel (5 min)

Per `system_config.youtube_zero_strategy`, the channel already exists:
- **Channel ID:** `UCp7STnqCNZSzikFLmkv7ZLg`
- **Name:** SoulHustleAI
- **URL:** `youtube.com/channel/UCp7STnqCNZSzikFLmkv7ZLg`

**Check:**
- [ ] Can you log into this channel? (YT Studio access)
- [ ] Is the handle `@SoulHustleAI` claimed?
- [ ] Is the published Zero avatar still the one at `zero_avatar_url` in Supabase?

If the channel is locked or you lost access → create new @SoulHustleAI handle and follow `CHANNEL-SETUP.md` from the top.

---

## PHASE 1 — Apply the v3 brand (30 min)

Upload the upgraded Infinite S logo everywhere:

1. **Profile picture:** export `brand/logo/shai_icon_only.svg` to a 800x800 PNG → upload to YT Studio → Customization → Branding → Picture
2. **Banner:** open `brand/logo/shai_horizontal_lockup.svg` in a 2560x1440 Figma frame → add Zero avatar on the right → export PNG → upload
3. **Video watermark:** use the icon-only variant, 150x150px → YT Studio → Customization → Branding → Video watermark → "End of video"
4. **About page:** paste the description from `CHANNEL-SETUP.md`
5. **Links:** add the 6 links from `CHANNEL-SETUP.md`

**Checkpoint:** the channel page looks like the v3 brand, not the v1 brand.

---

## PHASE 2 — Render Zero's voice (40 min)

Open ElevenLabs Studio.

Render these audio files (in this order):

1. **Intro v1** — from `zero-yt/scripts/zero-quickfire-intro.md` → save as `assets/audio/intro-v1.mp3`
2. **Outro v1** — same file → save as `assets/audio/outro-v1.mp3`
3. **Video 01 (origin)** — paste script in sections → save as `assets/audio/long-01.mp3`
4. **Shorts 01–03** — batch-render these three → save as `assets/audio/short-01.mp3` / `02.mp3` / `03.mp3`

Settings reminder: Orlando `4t8HWMowRF0NaJl0r9MS`, stability 0.42, similarity 0.9, style 0.52.

**Checkpoint:** 6 audio files in `assets/audio/`. Listen to each one. Re-roll any robotic sections.

---

## PHASE 3 — Build the Zero avatar animation (20 min)

Pick ONE of these paths:

### Path A — Static avatar (FASTEST, ship tonight)
- Use `brand/avatar/zero_social_avatar.svg` as a 1920x1080 static background
- Subtle zoom-in animation in CapCut (keyframe scale 1.00 → 1.04 over 6 min)
- Done

### Path B — Animated avatar (BETTER, ~40 min extra)
- Go to D-ID.com
- Upload the real Zero JPEG from `zero_avatar_url`
- Paste the `intro-v1.mp3` audio
- Let D-ID animate the lip sync
- Export the 5-second intro
- Repeat for outro

For tonight → **Path A.** You can upgrade to Path B in week 2.

---

## PHASE 4 — Edit Video 01 (60 min)

Open CapCut.

1. **New project:** 1920x1080, 30fps
2. **Import:** `long-01.mp3` from ElevenLabs
3. **Background:** static Zero avatar SVG (exported PNG) on video track 1
4. **Text overlays:** every major stat from the script appears in gold Cinzel, matching the shot list
5. **Cut-ins:** every 30–45 seconds, add a b-roll clip or chart to break up the static
6. **Outro:** append `outro-v1.mp3` + the SHAI v3 logo PNG
7. **Music:** low-BPM lofi beat, -18dB
8. **Export:** 1920x1080, H.264, 8Mbps

**Checkpoint:** one MP4, ~6:45 runtime, no dead air, Zero's voice clear.

---

## PHASE 5 — Edit Shorts 01, 02, 03 (45 min)

For each short (15 min each):
1. **New project:** 1080x1920, 30fps
2. **Background:** Zero avatar PNG, zoomed in
3. **Captions:** CapCut auto-caption, manually edit typos
4. **Hook text:** big Cinzel gold at the top
5. **Music:** same lofi beat, lower volume
6. **Export:** 1080x1920, max 45 seconds

**Checkpoint:** 3 MP4 shorts ready.

---

## PHASE 6 — Thumbnails (20 min)

Open Figma → create a 1280x720 frame.

**Video 01 thumbnail:**
- Left 60%: Zero avatar (smirk, visor glint)
- Right 40%: "STAFF DON'T EXIST" in Cinzel gold + "$11,400 →" in teal
- Bloomberg grid background
- Red circle around "$11,400" (only place red is allowed)
- Export: 1280x720 PNG, <2MB

---

## PHASE 7 — Upload (30 min)

### Video 01 (long-form)
1. YT Studio → Upload
2. Paste the **title** from `scripts/long-form/01-my-staff-dont-exist.md`
3. Paste the **description** from the same file (replace UTM placeholders with actual link)
4. Upload the thumbnail
5. Add **tags** from default upload settings
6. Add **timestamps** from the script
7. Set **end screen** → link to Video 02
8. Set **cards** → link to `apply.html`
9. Set **Playlist** → "Case Studies"
10. Publish as **Unlisted** first

### Shorts 01–03
1. Upload each short
2. Title = the hook line from each short script
3. Description = 2 lines + link to main channel
4. Publish as **Public** (shorts ship raw)

---

## PHASE 8 — Announce (15 min)

Once Video 01 is live:

1. Change visibility from Unlisted → **Public**
2. Pin a comment: **"📞 Call Zero at 929-236-1567 — he'll audit your business live. Free. 4 minutes. Or apply at soulhustleai.com/apply.html"**
3. Text Eli + Adam the YT link: "First video is up. Would mean the world if you watched + commented."
4. Post to IG Story with a "new video" sticker
5. Post to LinkedIn with a short text TLDR + YT link
6. Post in community tab: "Zero YT is LIVE. This is the start."

---

## PHASE 9 — Tomorrow morning monitoring (5 min)

Check first-hour metrics:
- [ ] Views (target: 50+ in first 2 hours from warm audience)
- [ ] Watch time % (target: >50% avg retention)
- [ ] Click-through on thumbnail (target: >5% CTR)
- [ ] Click-through to apply.html (check `leads.source` in Supabase for `utm_source=youtube`)

If anything's broken — the thumbnail, the audio, the title — **fix it within 6 hours.** After 24 hours YT locks in the algo assessment.

---

## Fallback Plan (if you can't ship tonight)

**Minimum viable launch (ship ONLY these):**
1. Brand refresh (Phase 1)
2. Video 01 with static avatar (Phases 2, 4, 6, 7)
3. Upload as Public

Shorts + socials + thumbnails can ship Monday morning. But DO NOT skip the long-form Video 01 — that's the channel's north star video. Everything else amplifies it.

---

## Phase-by-phase time budget

| Phase | Task | Time |
|-------|------|------|
| 0 | Verify channel | 5 min |
| 1 | Apply brand | 30 min |
| 2 | Render voice | 40 min |
| 3 | Zero avatar animation (Path A) | 20 min |
| 4 | Edit Video 01 | 60 min |
| 5 | Edit 3 shorts | 45 min |
| 6 | Thumbnails | 20 min |
| 7 | Upload | 30 min |
| 8 | Announce | 15 min |
| **Total** | | **~3h 45m** |

---

**This is the runbook. Execute top to bottom. Don't improvise.**

When Video 01 is live → update `STATE.md` with the live URL.
