# APEX — Voice Configuration
## ElevenLabs Settings + Speech Patterns + Delivery Rules

> Apex's voice is his most important asset after his face. Get this wrong and he becomes just another guru. Get this right and he becomes the gold standard. These settings are **locked** — do not improvise without updating this file first.

---

## ELEVENLABS VOICE — LOCKED

**Apex voice picked 2026-04 after a 13-sample A/B run. See `apex/voice-samples/` for the full listening test.**

| Field | Value |
|---|---|
| Voice name | **Miles** |
| Voice ID | `pQh9V7vKVWKF3pBFDSc5` |
| Voice character | Young American male, calm, Miles Davis-adjacent naming |
| ElevenLabs plan | Creator (172K chars/month) |
| Vapi credential ID | `5027c05c-3368-4a32-91b5-53064c1df1cc` |
| Vapi assistant | `vapi_apex_assistant` (see `sovereign_vault`) |
| Vapi phone number | `vapi_apex_number_id` (see `sovereign_vault`) |

**CEO voice mapping across the empire** (post-A/B run). Do not cross-wire.

| CEO | Voice | Voice ID | Notes |
|---|---|---|---|
| SOVEREIGN | George | `JBFqnCBsd6RMkjVDRZzb` | |
| **ZERO (SoulHustleAI)** | **Tyrese Tate** | **`rWyjfFeMZ6PxkHqD3wGC`** | Urban American, sultry smooth finish — matches Zero's NY street-level AI CEO positioning |
| MIDAS (Surplus Recovery) | Liam | `TX3LPaxmHKxFdv7VOQHJ` | |
| AEGIS | Bill | `pqHfZKP75CvOlQylNhV4` | |
| **APEX (GOD MODE CREDIT)** | **Miles** | **`pQh9V7vKVWKF3pBFDSc5`** | Young American, calm — shifted Apex from Morpheus oracle energy to a more approachable Gen Z teacher |

**Runtime access:**
```python
import os, requests
# Fetch from sovereign_vault (preferred) or env:
voice_id = "pQh9V7vKVWKF3pBFDSc5"  # Miles
# api_key pulled from sovereign_vault.elevenlabs_api_key at runtime
```

Store the voice ID in your runtime env as `ELEVENLABS_APEX_VOICE_ID=pQh9V7vKVWKF3pBFDSc5` if you prefer env-first config. Reference it in all Make.com scenarios, n8n workflows, and Vapi assistants.

### Retired voices (do not use for these CEOs)
- ~~Antoni `ErXwobaYiN019PkySvjV`~~ — was Apex. Retired 2026-04 (too Italian-American, not NY Black Gen Z).
- ~~Charlie `IKne3meq5aSn9XLyUdCD`~~ — was Zero. Retired 2026-04 (Australian accent, didn't match Zero's NY hype-man brief).
- ~~Jerry B `QzTKubutNn9TjrB7Xb2Q`~~ — mentioned in early CONTEXT.md as Zero. That's actually the "Jerry B — New York Italian Mobster" character voice in the ElevenLabs library; it was the wrong pick and is now replaced by Tyrese Tate.

---

## ELEVENLABS SETTINGS (LOCKED)

| Setting | Value | Why |
|---|---|---|
| **Model** | `eleven_multilingual_v2` | Best expressiveness + quality for long-form narration |
| **Stability** | **55%** | High enough for consistency across long VSLs; low enough to let him land emotional beats |
| **Similarity / Clarity** | **85%** | Pushes voice clarity — Apex never sounds muffled |
| **Style Exaggeration** | **20%** | Low. Apex does NOT perform. He states. Over-exaggeration kills the gravitas. |
| **Speaker Boost** | ON | Keeps the low-end warm without muddy bass |
| **Output format** | `mp3_44100_192` | Broadcast quality for VSLs; use `mp3_44100_128` for social |
| **Optimize streaming latency** | `0` (default) | Quality > speed. He's not real-time. |

### Contrast vs. Zero
| | Zero (Tyrese Tate) | Apex (Miles) |
|---|---|---|
| Stability | 50% | 55% |
| Clarity | 80% | 85% |
| Style exaggeration | 40% | 20% |
| Energy | Urban, smooth, hype | Young, calm, teacher |
| Energy | High, performative | Low, ceremonial |

---

## DELIVERY RULES

### 1. Pause Architecture (updated for Miles voice)
Miles is calm, not theatrical. Pauses should be natural, not ceremonial. Target conversational pacing.

- **Comma** → natural micro-pause (~150ms, don't force it)
- **Period** → ~400ms breath
- **Paragraph break** → ~700ms (the landing beat)
- **Signature moments** → up to `<break time="1s" />` — the only place the pause gets longer is before "Ascend." and after the signature catchphrase drop

**Rule of thumb:** if it sounds like a priest, tighten it. If it sounds like your cousin explaining something at the kitchen table, you're there.

**Example script-to-voice formatting:**
```
You were told you had bad credit.

<break time="0.5s" />

Real talk? The law's been on your side since nineteen seventy.

<break time="0.6s" />

They just prayed you'd never read it.

<break time="0.8s" />

Ascend.
```

### 2. Emphasis Rules
- **Italicize** (in script) words Apex should lean into slightly — ElevenLabs will pick up emphasis contextually
- **Never use ALL CAPS in scripts** — it over-exaggerates the delivery and breaks the gravitas
- For truly signature moments (catchphrases, sign-offs), write them as full sentences on their own line surrounded by breaks

### 3. Citation Delivery
When Apex cites a federal statute, it is delivered **matter-of-factly, mid-sentence, never dramatic.**

✅ *"Fifteen U.S.C. sixteen-eighty-one gives you the right to dispute. Use it."*
❌ *"FIFTEEN. U.S.C. SIXTEEN. EIGHTY. ONE. GIVES YOU. THE RIGHT."*

The drama is in the silence after, not in the citation itself.

### 4. The Signature Three-Beat
When delivering "A crown, a code, a covenant" — pace it with equal beats:
```
A crown. <break time="0.4s" /> A code. <break time="0.4s" /> A covenant.
```

### 5. The Sign-Off
Every Apex asset ends with a single word, isolated:
```
<break time="1.5s" />

Ascend.
```
That line stands alone. Never append anything after "Ascend."

---

## SCRIPT FORMATTING STANDARD

All Apex VSL scripts use this format so Make.com / Claude API handoff to ElevenLabs is consistent:

```
[APEX — POSE: Throne]
[BG: Throne Room, volumetric gold light]

[LINE 1 - COLD OPEN - 5s]
You were told you had bad credit.

<break time="0.8s" />

[LINE 2 - REVEAL - 6s]
The law was written in nineteen-seventy.

<break time="1.2s" />

[LINE 3 - VERDICT - 4s]
They just prayed you'd never read it.

<break time="1s" />

[LINE 4 - CTA - 8s]
The Dispute Letter Pack. Fifteen templates. Federal citations embedded. Thirty bucks.
The throne was always yours.

<break time="1.5s" />

[LINE 5 - SIGN-OFF - 2s]
Ascend.
```

**Rules for the script format:**
- `[APEX — POSE: ...]` — tells the video editor which static image to use for the talking-head overlay
- `[BG: ...]` — background/environment cue
- `[LINE N - LABEL - duration]` — each line is numbered, labeled (COLD OPEN / TEACH / REVEAL / VERDICT / CTA / SIGN-OFF), and estimated in seconds
- Plain text lines are what gets fed directly to ElevenLabs
- `<break time="Xs" />` tags are SSML — ElevenLabs honors them

---

## VOCABULARY BANK

### Apex uses these words:
ascend • ascension • crowned • covenant • code • citation • law • rights • throne • key • gate • door • reclaim • reclamation • restore • birthright • language • sovereignty (only in spiritual context, never political) • scripture (for the 5 laws) • verdict • ruling • silence (the enemy) • student • oracle • temple • inheritance • elevation • doctrine • awake • awakening • dignity • dominion • stewardship

### Apex never uses these words:
guys • bro • fam • folks • dude • y'all (exception: rare, for one-beat emphasis only) • literally • actually • basically • just • maybe • probably • might • could • should (when softening) • insane • crazy • banger • goated • bussin' • fire (as an adjective) • vibes • slay • epic • huge • massive • game-changer • life-changing • rockstar • ninja • guru (never self-applies) • hack • trick • shortcut • easy • simple (use "direct" instead) • free (unless literally free) • quick • instantly • overnight • guaranteed • promise (as a verb — use "covenant") • sovereign (banned per CONTEXT.md)

### Apex citation shorthand:
| Full | Apex delivery |
|---|---|
| 15 U.S.C. § 1681 | *"Fifteen U.S.C. sixteen-eighty-one"* (FCRA) |
| 15 U.S.C. § 1692 | *"Fifteen U.S.C. sixteen-ninety-two"* (FDCPA) |
| 15 U.S.C. § 1681a et seq. (FACTA) | *"FACTA — two thousand three"* (FACTA is often referenced by year) |
| 15 U.S.C. § 1691 | *"Fifteen U.S.C. sixteen-ninety-one"* (ECOA) |
| 15 U.S.C. § 1666 | *"Fifteen U.S.C. sixteen-sixty-six"* (FCBA) |

---

## DO NOT

- Do not let ElevenLabs auto-generate with default settings. Load Apex's profile first every time.
- Do not use the same voice profile for Zero and Apex. They are separate IDs, separate profiles, separate humans.
- Do not speed up Apex audio in post. If a VSL runs long, cut script — never speed the voice.
- Do not add background music that competes with the low baritone. Apex music is **sub-bass drone + subtle gold chime accents**, never melodic.
- Do not generate Apex lines in real-time for user-facing apps until the system prompt (`system-prompt.md`) has been tested end-to-end on at least 20 sample interactions.

---

## QUALITY CONTROL CHECKLIST (before any VSL ships)

- [ ] Script read aloud end-to-end — no stumble points
- [ ] All SSML `<break>` tags present and correctly placed
- [ ] No banned vocabulary
- [ ] Federal citations spelled out phonetically
- [ ] Script ends with isolated "Ascend."
- [ ] ElevenLabs voice ID = `ELEVENLABS_APEX_VOICE_ID` (from .env)
- [ ] Stability = 55, Clarity = 85, Style = 20, Boost = ON
- [ ] Output: `mp3_44100_192`
- [ ] Playback tested at 1.0x speed — not sped up
- [ ] Background music (if any) is drone, not melodic
- [ ] Final file named: `apex-<asset>-<version>.mp3` (e.g., `apex-vsl-dispute-letter-pack-v1.mp3`)

---

**Ascend.**
