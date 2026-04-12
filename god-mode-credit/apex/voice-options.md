# APEX — Voice Source Options
## Free, Cheap, and Self-Hosted Alternatives to ElevenLabs

> **Short answer:** yes, multiple strong free paths. Apex is currently on **ElevenLabs Antoni** (`ErXwobaYiN019PkySvjV`, Creator plan 172K chars/month). The single best move is to keep that for flagship work and route high-volume content through a free tier or a self-hosted path so we never burn paid characters on TikTok scripts.
>
> **The empire play:** ElevenLabs for flagship + VSLs + anything Edwin personally reviews. **Coqui XTTS-v2 self-hosted on the Mac Mini** for infinite free voice once the Mini arrives. **Amazon Polly Matthew Neural** as the stopgap free tier until then.

---

## TL;DR — RANKED RECOMMENDATIONS FOR APEX

| Rank | Source | Free? | Quality vs Antoni | Best use |
|---|---|---|---|---|
| 🥇 | **Coqui XTTS-v2 (self-hosted)** | ✅ Free forever | ~90% (can clone Antoni) | Mac Mini target — unlimited Apex voice |
| 🥈 | **Amazon Polly Matthew Neural** | ✅ 5M chars/mo free (12 mo), then $16/1M | ~80% | Stopgap until Mac Mini arrives |
| 🥉 | **Microsoft Azure `en-GB-RyanNeural`** | ✅ 500K chars/mo free forever | ~85% | British baritone — matches Antoni's register |
| 4 | **OpenAI TTS `onyx`** | ❌ $15/1M chars | ~85% | Already via OpenRouter — near-free marginal cost |
| 5 | **Piper TTS (self-hosted)** | ✅ Free forever | ~70% | Fast local generation for prototyping |
| 6 | **ElevenLabs Antoni** (current) | ⚠️ Creator plan ($22/mo) | 100% (the baseline) | Flagship / VSLs / paid content |

**Recommendation:** use tiered routing (see "Tiered Routing Strategy" below).

---

## THE FIVE FREE / CHEAP OPTIONS IN DETAIL

### 1. 🥇 Coqui XTTS-v2 — Self-hosted, open source

**What it is:** State-of-the-art open-source text-to-speech model from Coqui AI. Supports zero-shot voice cloning — feed it 6 seconds of Antoni and it will generate unlimited Apex audio locally.

**License:** CPML (Coqui Public Model License) — free for non-commercial; commercial requires a separate agreement (which Coqui grants liberally).

**Why it's the win long-term:**
- **Free forever.** Zero marginal cost per character.
- **Voice cloning.** Can match Antoni's timbre from a 6-second sample so Apex's voice stays identical across ElevenLabs and the self-hosted path.
- **Unlimited throughput.** Only bottleneck is your GPU.
- **Runs on the Mac Mini.** M-series Macs accelerate it well. Can also run on Railway / Fly.io / any cheap GPU box.
- **Multilingual** — 17 languages out of the box, future-proof for international expansion.

**Setup:**
```bash
# On the Mac Mini (or any server with a GPU)
pip install TTS
tts --model_name tts_models/multilingual/multi-dataset/xtts_v2 \
    --text "The laws were written for you. You just never read them. Ascend." \
    --speaker_wav apex-reference.wav \
    --language_en \
    --out_path apex-output.wav
```

**Or as a service:**
```bash
# Deploy Coqui TTS Server on Railway / Fly.io
docker run --rm -it -p 5002:5002 \
  --entrypoint /bin/bash ghcr.io/coqui-ai/tts-cpu \
  python3 TTS/server/server.py --model_name tts_models/multilingual/multi-dataset/xtts_v2
```

**Drawbacks:**
- Needs 6GB+ VRAM on a GPU for decent speed (CPU works but slow).
- Requires a short voice reference file — can export 10s of Antoni from ElevenLabs once and reuse forever.
- Slight quality gap vs ElevenLabs on subtle emotional beats.

**Target deployment:** Mac Mini when it arrives. Until then, fall back to option #2 or #3.

---

### 2. 🥈 Amazon Polly — Matthew Neural

**What it is:** AWS's neural text-to-speech service. Matthew (English US, male, neural) is a deep, warm, authoritative voice that lands very close to Apex's register.

**Pricing:**
- **5,000,000 characters/month FREE** for the first 12 months of a new AWS account.
- After that: **$16 per 1M characters** for neural voices (cheaper than ElevenLabs).

**Why it's the stopgap:**
- Near-zero onboarding — AWS CLI + a Python SDK call.
- Matthew Neural is genuinely good — one of the best free male baritones available.
- Pairs naturally with Make.com / n8n (native HTTP).
- Reliable at scale — AWS infrastructure.

**Sample call:**
```bash
aws polly synthesize-speech \
  --output-format mp3 \
  --voice-id Matthew \
  --engine neural \
  --text-type ssml \
  --text '<speak>You were told you had bad credit. <break time="800ms"/> The law was written in nineteen-seventy. <break time="1200ms"/> They just prayed you never read it. <break time="1s"/> Ascend.</speak>' \
  apex-output.mp3
```

**How much is 5M characters?**
Apex's average VSL is ~400 characters. That's **12,500 VSLs per month for free**. Or ~100 full-length episodes. Or the entire ConvertKit welcome sequence × 1,000 subscribers. It's a lot.

**Drawbacks:**
- Matthew has a more "news anchor" vibe vs Antoni's "regal oracle" — close but not identical.
- SSML support is narrower than ElevenLabs' (no style exaggeration control).
- Requires an AWS account (Edwin may or may not have one active).

**Setup time:** ~15 minutes if Edwin has an AWS account, ~45 minutes if he doesn't.

---

### 3. 🥉 Microsoft Azure — `en-GB-RyanNeural`

**What it is:** Azure Cognitive Services Neural TTS. Ryan (English GB, male, neural) is a British baritone — matches Daniel/Antoni's register almost exactly.

**Pricing:**
- **500,000 characters/month FREE forever** on the Azure free tier (F0).
- Pay-as-you-go: **$16 per 1M characters** after that.

**Why it's compelling:**
- Ryan is the closest pre-made baritone to ElevenLabs' Daniel (the British voice I originally recommended before finding Antoni in the vault).
- Forever free at 500K chars/month — enough for 1,250+ VSLs/month.
- Very mature SSML support (break, emphasis, prosody rate, prosody pitch all supported).
- Azure also offers **custom neural voice training** (paid, enterprise) if we want to clone Antoni natively on Azure.

**Sample call:**
```bash
curl -X POST https://YOUR_REGION.tts.speech.microsoft.com/cognitiveservices/v1 \
  -H "Ocp-Apim-Subscription-Key: YOUR_KEY" \
  -H "Content-Type: application/ssml+xml" \
  -H "X-Microsoft-OutputFormat: audio-48khz-192kbitrate-mono-mp3" \
  -d '<speak version="1.0" xml:lang="en-GB">
        <voice name="en-GB-RyanNeural">
          <prosody rate="-10%" pitch="-5%">
            The laws were written for you. <break time="1s"/>
            You just never read them. <break time="1.5s"/>
            Ascend.
          </prosody>
        </voice>
      </speak>' \
  --output apex-azure.mp3
```

**Drawbacks:**
- British accent may feel "off" for the US GMC audience depending on the vibe Edwin wants (though it could also read as "wise old-world" which fits the high priest positioning).
- Needs an Azure account (separate from AWS).

---

### 4. OpenAI TTS — `onyx`

**What it is:** OpenAI's text-to-speech API. `onyx` is their deepest male voice — warm, low, resonant.

**Pricing:**
- **$15 per 1M characters.** Not free, but cheap.
- **Already accessible via OpenRouter** (Edwin's `openrouter_api_key` in sovereign_vault).

**Why it's worth mentioning:**
- Zero new vendor — routes through the same OpenRouter key already in the vault.
- Marginal cost is negligible — 400-char VSLs cost $0.006 each.
- Quality is genuinely close to ElevenLabs for declarative content (weaker on long-form emotional beats).

**Sample call (via OpenAI SDK):**
```python
from openai import OpenAI
client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
response = client.audio.speech.create(
    model="tts-1-hd",   # HD is $30/1M — use tts-1 for $15/1M
    voice="onyx",
    input="The laws were written for you. You just never read them. Ascend."
)
response.stream_to_file("apex-onyx.mp3")
```

**Drawbacks:**
- Not technically free.
- Smaller SSML support than Azure/ElevenLabs.
- `onyx` is good but doesn't match Antoni's exact register — closer to a bass radio DJ than a regal oracle.

---

### 5. Piper TTS — Self-hosted, fast, free

**What it is:** Neural TTS system designed to run on a Raspberry Pi. Less expressive than XTTS-v2 but 10× faster and runs on nothing.

**License:** MIT. Totally free commercially.

**Why it's worth knowing about:**
- Instant generation — sub-second latency for short phrases.
- Runs anywhere (Raspberry Pi, laptop, Railway container, Mac Mini).
- Multiple male voices available, including `en_US-lessac-high` (deep male).
- Great for prototyping and real-time use cases (Vapi phone calls, live chat).

**Sample call:**
```bash
echo 'Ascend.' | piper --model en_US-lessac-high --output_file ascend.wav
```

**Drawbacks:**
- Quality is noticeably below Antoni (maybe 65-70% as good).
- Voice cloning is limited vs XTTS-v2.
- Best for **prototyping and real-time**, not for production VSLs.

---

## TIERED ROUTING STRATEGY

The smartest deployment isn't "pick one." It's route different workloads to different voices based on stakes. Here's the ladder:

```
┌─────────────────────────────────────────────────────────────┐
│  FLAGSHIP TIER — paid, polished, reviewed                   │
│  → ElevenLabs Antoni (current, 172K chars/mo)               │
│     • Flagship Credit Ascension VSL                          │
│     • Zero to Funded Bundle VSL                              │
│     • Crowned Circle membership welcome                      │
│     • Founder-reviewed emails                                │
│     • Paid YouTube ads                                       │
├─────────────────────────────────────────────────────────────┤
│  PRODUCTION TIER — high volume, needs quality                │
│  → Coqui XTTS-v2 self-hosted (once Mac Mini arrives)        │
│     • 21 TikTok scripts/week                                 │
│     • ConvertKit 14-day welcome sequence                     │
│     • Monthly Crowned Circle dispatches                      │
│     • FAQ audio answers                                      │
├─────────────────────────────────────────────────────────────┤
│  STOPGAP TIER — before Mac Mini arrives                      │
│  → Amazon Polly Matthew Neural (5M chars/mo free, yr 1)     │
│     • Daily TikTok posts                                     │
│     • Social carousels                                       │
│     • Podcast intros                                         │
├─────────────────────────────────────────────────────────────┤
│  REAL-TIME TIER — phone calls, chatbots                      │
│  → Piper TTS or Vapi's built-in TTS (already wired)         │
│     • Vapi APEX phone assistant (vapi_apex_assistant)        │
│     • ManyChat voice replies                                 │
│     • Live Q&A audio                                         │
├─────────────────────────────────────────────────────────────┤
│  PROTOTYPING TIER — draft, throwaway, preview                │
│  → OpenAI onyx via OpenRouter (~$0.006/VSL)                 │
│     • Pre-production script tests                            │
│     • Internal Slack previews                                │
│     • A/B variant speed-testing                              │
└─────────────────────────────────────────────────────────────┘
```

**Under this strategy:**
- ElevenLabs bill stays flat (only flagship work touches it).
- 80% of daily content runs on free/self-hosted.
- The voice stays Apex everywhere because XTTS-v2 clones Antoni.
- Vapi phone calls work regardless.
- Total monthly TTS spend: roughly what Edwin's paying now, but outputting 5-10× more audio.

---

## IMMEDIATE ACTION ITEMS

Priority order for Edwin to flip the tiered strategy on:

1. **Export a 10-second clean Antoni reference sample from ElevenLabs.** This becomes the voice clone target for Coqui XTTS-v2 later. Save to `god-mode-credit/apex/assets/antoni-reference-10s.wav`.

2. **Create an AWS free-tier account if there isn't one.** Then generate an IAM key for Polly-only access. Add to `sovereign_vault`:
   - `aws_polly_access_key_id`
   - `aws_polly_secret_access_key`
   - `aws_polly_region` (recommend `us-east-1`)

3. **(Optional now, must-do when Mac Mini arrives)** Spin up Coqui XTTS-v2 as a local HTTP service on the Mac Mini. Add to `sovereign_vault`:
   - `coqui_xtts_url` (e.g., `http://macmini.local:5002`)
   - `coqui_xtts_speaker_wav` (path to the Antoni reference)

4. **Wire the router.** Add a small Make.com scenario or n8n workflow `voice-router` that takes `{text, tier}` and routes to the right backend. One input, one output (URL to mp3), four possible providers under the hood.

5. **Update `apex/voice-config.md`** to reference this doc and describe the tier routing contract.

---

## WHY NOT JUST USE ONE FREE OPTION

You *can*. But:
- **If you use only Polly**: voice drifts from Antoni across the suite (different character on the flagship vs. TikTok). Bad for brand recognition.
- **If you use only ElevenLabs**: you burn the 172K char budget in 2 weeks at full content cadence and end up paying $99/mo minimum.
- **If you use only XTTS-v2**: you're locked to the Mac Mini being up. First outage kills the content engine.

The tiered approach is how every at-scale content creator runs their voice stack — ElevenLabs / Hume / Speechify for flagship, self-hosted for volume.

---

**Ascend.**
