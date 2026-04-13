# Zero YT — Channel Setup
## One-time configuration — do this once, set it and forget it

> **Time required:** ~30 minutes
> **Prereqs:** Google account (use `soulhustleai@gmail.com`), Canva or Figma for banner

---

## 1. Create The Channel

1. Go to https://youtube.com → sign in with `soulhustleai@gmail.com`
2. Click your avatar → **Create a channel**
3. Choose **Use a custom name** → `SoulHustleAI`
4. Grab the handle: **@SoulHustleAI** (backup: @ZeroCEO if taken)
5. URL will be: `youtube.com/@SoulHustleAI`

---

## 2. Channel Branding

### Profile picture (800x800px, <4MB, PNG)
Use the Zero avatar: circular gold visor head, black hoodie collar visible.
Midjourney prompt:
```
portrait of Zero the AI CEO, reflective gold visor covering eyes,
black hoodie, gold Cuban link chain, solid black background,
highly detailed, cinematic lighting, centered square crop,
luxury fintech aesthetic --ar 1:1 --style raw --s 250
```

### Banner (2560x1440px, safe zone 1546x423px)
**Concept:** Black background, Zero silhouette on right 1/3, gold script text on left 2/3.

**Layout spec:**
- Background: pure `#050505`
- Left 60%: Headline "MY STAFF DON'T EXIST." in Cinzel Bold 180px, color `#F2C95C`
- Subheadline (under main): "Custom AI automation for businesses done growing the hard way." in Barlow Light 56px, `#8a8577`
- Right 40%: Full-body Zero in the Arms Crossed pose, gold visor reflecting faint website UI
- Bottom bar (full width): horizontal gold line `#C9A033` 2px + social icons
- Subtle radial gold glow behind Zero (opacity 20%)

**Midjourney prompt for Zero body shot:**
```
full body shot of Zero the AI CEO, arms crossed confident pose,
black designer hoodie under navy blazer, reflective gold visor
covering eyes, solid gold Cuban link chain, black backdrop,
luxury fintech vibe, Bloomberg terminal glow reflecting off visor,
cinematic lighting, centered composition --ar 16:9 --style raw --s 300
```

### Channel avatar watermark (for subscribe button overlay — 150x150px)
A compressed circular version of the profile picture.

---

## 3. Channel "About" Section

### Description (copy-paste verbatim)
```
My staff don't exist.

I'm Zero — the AI CEO of SoulHustleAI. I answer every call, qualify every lead,
book every job, and close every follow-up for service businesses tired of leaking
money to missed calls, dead follow-up, and no-show automation.

This channel shows you exactly how I do it.

  → Real case studies from real clients (Eli recovered $11K/mo)
  → The 5 automations that print money in service businesses
  → BOSSMoves framework: lead gen → conversion → fulfillment → ascension
  → Behind the scenes of running a business without humans

🎯 Work with me → soulhustleai.com/apply.html
📞 Call me direct → (929) 236-1567  (I'm an AI — I pick up in 2 rings, 24/7)

Powered by SoulHustleAI — a Typically Not Lifestyle LLC brand.
```

### Links to add
1. **Website:** https://soulhustleai.com
2. **Apply:** https://soulhustleai.com/apply.html
3. **ROI Calculator:** https://soulhustleai.com/roi-calculator.html
4. **Instagram:** @soulhustleai
5. **TikTok:** @soulhustleai
6. **Phone (custom link):** tel:+19292361567 label "Call Zero"

### Contact email
`hello@soulhustleai.com` (public business inquiries)

### Keywords / tags
```
ai automation, service business, zero ai, soulhustleai, faceless youtube,
ai receptionist, missed call text back, twilio, vapi, make.com, n8n,
bossmoves, ai for small business, ai sales, b2b automation
```

---

## 4. Upload Defaults

Go to YouTube Studio → Settings → Upload defaults:

### Default description (auto-fills on every upload)
```
Work with Zero → soulhustleai.com/apply.html
Call Zero direct → (929) 236-1567  (live 24/7)
Free ROI check → soulhustleai.com/roi-calculator.html

━━━━━━━━━━━━━━━━━━━
Zero is the AI CEO of SoulHustleAI. He runs sales, support, and
automation for service businesses doing $100K–$10M/year.

SoulHustleAI — Typically Not Lifestyle LLC
#ai #automation #zero #soulhustleai #smallbusiness
```

### Default tags
```
ai automation, zero ai ceo, soulhustleai, service business, ai for small business,
missed call text back, ai receptionist, automated follow up, bossmoves framework,
n8n, make.com, vapi, twilio, business automation
```

### Default category
`Science & Technology` or `Education` (test both — Education usually indexes better for education-style scripts)

### Default visibility
`Private` (you review before every publish)

### Default license
`Standard YouTube License`

---

## 5. Playlists (create these now — they boost watch time)

1. **Case Studies** — "Real clients. Real numbers. Real receipts."
2. **The 5 Automations** — "The stack that prints money for service businesses."
3. **BOSSMoves Framework** — "Lead gen → conversion → fulfillment → ascension."
4. **Zero's Audits** — "Live audits of real businesses. Unfiltered."
5. **Behind The AI** — "How a faceless AI character runs a 6-figure agency."

---

## 6. YouTube Shorts Shelf

Enable shorts shelf on channel homepage: YT Studio → Customization → Layout → Add section → Shorts.

---

## 7. Monetization (future — after 1K subs + 4K watch hours)

- Apply for YouTube Partner Program when eligible
- Prioritize **memberships** over AdSense — higher LTV
- Add memberships at $4.99/mo with perks: behind-the-scenes audits, early Zero voice previews

---

## 8. Analytics Tracking

### UTM links in every description
```
https://soulhustleai.com/apply.html?utm_source=youtube&utm_medium=video&utm_campaign={{video_slug}}
```

Pipe UTMs into PostHog + Supabase `leads.source` column for attribution tracking.

### Weekly check (every Monday 9am ET)
- Top 3 videos by watch time → double down on format
- Bottom 3 → pull + retitle or unlist
- CTR on thumbnails → anything <4% gets a new thumbnail

---

## ✓ Channel setup complete when:
- [x] Handle claimed
- [x] Avatar uploaded
- [x] Banner uploaded
- [x] About section filled
- [x] Links added
- [x] Upload defaults set
- [x] 5 playlists created
- [x] Shorts shelf enabled

Next → `PRODUCTION-PIPELINE.md`
