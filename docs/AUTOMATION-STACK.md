# Full Automation Stack — Hands-Off System

> Goal: Days 1-30 Edwin builds. Days 31-60 machine takes over. Day 90+ Edwin monitors and collects. 1-2 hrs/week max.
> **Updated: March 19, 2026 — All API keys configured. Scripts built.**

---

## API KEYS STATUS (all configured in `.env`)

| Service | Key Status | Script |
|---------|-----------|--------|
| **HeyGen** | CONFIGURED | `scripts/heygen_video.py` |
| **Buffer** | CONFIGURED | `scripts/buffer_schedule.py` |
| **Make.com** | CONFIGURED | `scripts/make_webhooks.py` |
| **ManyChat** | CONFIGURED | `scripts/manychat_setup.py` |
| **ConvertKit (Kit)** | CONFIGURED | (via Make.com webhook) |
| **Payhip** | CONFIGURED | (via Make.com webhook) |

**Master orchestrator:** `scripts/pipeline.py`

---

## Content Creation Pipeline

```
Claude API (scripts/captions/ebooks)
    → HeyGen (AI avatar video — 9:16 vertical, auto-generated)
    → Buffer (schedule to TikTok + IG + YouTube Shorts + Pinterest)
    → OpusClip (optional: 1 long video → 10 Reels/Shorts)
```

### Content Batch Process
1. `python scripts/pipeline.py --batch-prompts` → generates 21 Claude API prompts
2. Claude API generates scripts (via Make.com scenario or manual)
3. `python scripts/heygen_video.py --batch scripts/tiktok_scripts/` → AI avatar videos
4. `python scripts/buffer_schedule.py --batch output/videos/ --captions captions.json` → scheduled
5. Edwin reviews once monthly

---

## Sales & Delivery Pipeline

```
TikTok/IG traffic
    → Stan Store (bio link, one-tap checkout)
    → Payhip (PDF auto-delivery + affiliate tracking)
    → ConvertKit (14-day welcome + sell sequence)
    → Make.com (Payhip → ConvertKit → tags buyers → triggers sequences)
```

---

## Lead Capture Pipeline

```
Content goes viral
    → ManyChat DM bot ("Comment LAWS and I'll send it")
    → Auto-delivers lead magnet PDF
    → Warms prospect to paid products
    → ConvertKit email sequence takes over
```

---

## Client Automation Pipeline (SoulHustleAI)

```
Lead comes in (website/referral)
    → Voiceflow AI chatbot (qualifies, answers FAQs 24/7)
    → Twilio SMS follow-up (when 10DLC approved)
    → Make.com orchestrates workflows
    → Notion CRM tracks everything
    → Square processes payments
```

---

## Analytics Layer

| Tool | Purpose |
|------|---------|
| Metricool | Unified social analytics dashboard |
| TikTok Creative Center | Trending content research (check BEFORE writing scripts) |
| Exploding Topics | Topic forecasting 3-6 months ahead |

---

## Platform Details

### HeyGen (AI Avatar Video)
- **Plan:** Pro API ($99/mo)
- **Why:** Script → finished 9:16 video in one API call. No filming needed.
- **Script:** `python scripts/heygen_video.py --list-avatars` to pick your avatar
- **API Key:** Configured in `.env`

### Buffer (Social Scheduling — replacing Later.com)
- **Plan:** Pro
- **Why:** API access for automated scheduling. Supports TikTok, IG, YT, Pinterest.
- **Script:** `python scripts/buffer_schedule.py --list-profiles` to see connected accounts
- **Stagger posting:** TikTok first, IG +2hrs, YouTube +4hrs, Pinterest +6hrs
- **API Key:** Configured in `.env`

### ConvertKit (Kit)
- **Plan:** Free (up to 10K subscribers)
- **Sequences:** 14-day welcome + sell sequence (to be written)

### ManyChat
- **Platforms:** TikTok DMs + Instagram DMs
- **Trigger:** Comment keyword → auto-deliver lead magnet → warm to products
- **Script:** `python scripts/manychat_setup.py --setup-guide` for full DM flow setup
- **Keywords:** LAWS, GUIDE, AI, CREDIT, FREE
- **API Key:** Configured in `.env`

### Make.com (Automation Orchestrator)
- **Script:** `python scripts/make_webhooks.py --setup-payhip-pipeline` for full setup guide
- **Key scenario:** Payhip purchase webhook → ConvertKit tag + email sequence
- **API Key:** Configured in `.env`

### Digistore24 — Three Plays
1. **LIST** our products → 3,000+ active affiliates promote at no cost
2. **PROMOTE** compatible products as affiliate to our warmed list (Keystone Investors Club, Project Serenity, Crypto Quantum Leap)
3. **STUDY + SUPERSEDE** their funnels (Tube Mastery, Passive Income 2.0, Perpetual Income 365)

### Make.com → n8n Migration
- **Current:** Make.com (paid per operation)
- **Future:** Self-hosted n8n on Mac Mini
- **Benefit:** Unlimited runs, zero monthly cost, full control
- **Trigger:** When Mac Mini arrives

---

## VSL Rule
Every Payhip product page needs a **60-second video sales letter**:
- ElevenLabs + Zero voice + script
- Done in one hour per product
- Non-negotiable for conversion

---

## Content Strategy

### Platforms
TikTok (primary), Instagram Reels, YouTube Shorts, X
3-5 posts/day using Later.com batch scheduling

### 5 Content Pillars
1. **Rights** — "Federal law says they MUST remove this" — FCRA/FDCPA education = viral
2. **AI Tools** — "I let AI dispute my credit — here's what happened" — screen demos
3. **Divine Energy** — "They profit off your ignorance" — spiritual wealth lens = loyal tribe
4. **Business Credit** — "$50K biz credit with no personal SSN" — high purchase intent
5. **AI Income** — "My staff don't exist" — Zero energy, SH.AI brand content

---

## Quick Start Commands

```bash
# Install dependencies
pip install -r scripts/requirements.txt

# Check all API keys are configured
python scripts/pipeline.py --check-keys

# Generate 21 TikTok script prompts (all 5 pillars)
python scripts/pipeline.py --batch-prompts

# List available HeyGen avatars
python scripts/heygen_video.py --list-avatars

# Generate a video from a script
python scripts/heygen_video.py --script "Your script text" --title "Video Title"

# List connected Buffer profiles
python scripts/buffer_schedule.py --list-profiles

# Schedule a post across all platforms (staggered)
python scripts/buffer_schedule.py --post "Caption text" --video-url URL --stagger

# View ManyChat setup guide
python scripts/manychat_setup.py --setup-guide

# View Make.com Payhip→ConvertKit pipeline guide
python scripts/make_webhooks.py --setup-payhip-pipeline

# Full pipeline status
python scripts/pipeline.py --status
```
