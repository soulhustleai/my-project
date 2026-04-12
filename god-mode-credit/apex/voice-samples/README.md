# APEX — Voice Samples
## Listen Before You Lock

> All samples speak the **same test script** so you can A/B them fairly:
>
> *"You were told you had bad credit. The law was written in nineteen seventy. They just prayed you'd never read it. Fifteen U.S.C. sixteen eighty one, section six eleven. The Fair Credit Reporting Act. The laws were written for you. You just never read them. Ascend."*
>
> All generated at ElevenLabs Multilingual v2 with Stability 55 / Clarity 85 / Style 20 / Speaker Boost ON — the locked Apex voice settings.

---

## 🎯 THE BRIEF

Edwin's voice criteria:
- ✅ **American** accent (not British)
- ✅ **New York** vibe
- ✅ **Gen Z** energy (younger than current Antoni)
- ✅ **Sounds Black**

Ranked by how well each candidate hits all 4 criteria.

---

## 🥇 TIER S — Most Likely To Win (explicit matches)

These voices are tagged or described as Black + American + urban/NY + young. Start here.

| Rank | Voice | File | Description | Voice ID |
|---|---|---|---|---|
| 1 | **Jamal — Expressive and Confident** | `apex-sample-jamal-urban-street.mp3` | "Urban American male with a street accent. Great for drama and passion." | `Ybqj6CIlqb6M85s9Bl4n` |
| 2 | **Jamahal — Young, Vibrant, Natural** | `apex-sample-jamahal-young-urban.mp3` | "A stylish, young urban male perfect for chill podcasts and natural conversation." | `DTKMou8ccj1ZaWGBiotd` |
| 3 | **Young Jamal** | `apex-sample-young-jamal.mp3` | "Young Black African American voice. Perfect for casual conversation and social media." | `6OzrBCQf8cjERkYgzSg8` |
| 4 | **Darryl — Deep and Confident** | `apex-sample-darryl-young-raspy.mp3` | "Young Raspy, confident, Black Male voice. Great for Narration." | `h8LZpYr8y3VBz0q2x0LP` |
| 5 | **Tyrese Tate — Warm, Smooth, Husky** | `apex-sample-tyrese-tate-smooth.mp3` | "Urban American male with a sultry smooth finish. Ideal for content." | `rWyjfFeMZ6PxkHqD3wGC` |
| 6 | **Carter — Charismatic and Relatable** | `apex-sample-carter-ny-street-smart.mp3` | "Charismatic New York male voice with a laid-back, street-smart character." | `GorLj2SsI4u2JqL58gAA` |
| 7 | **Jon Paul — Charismatic and Flowy** | `apex-sample-jon-paul-charismatic.mp3` | "Black African American male voice (30's), Great for narrative & fiction." | `rdDUoCO1RjwdMmNjmhHV` |

---

## 🥈 TIER A — Also Worth Hearing

Strong pre-made voices from the personal account. Ethnicity not explicitly labeled but worth comparing.

| Voice | File | Description | Voice ID |
|---|---|---|---|
| **Erik / Alexander — Deep High Energy Urban Authority** | `apex-sample-erik-urban-authority.mp3` | "Deep, bold, high energy with confident promotional drive. Strong urban authority." | `dYcHQ0F5ki90WgfHiRL8` |
| **DJ Marathon** | `apex-sample-dj-marathon.mp3` | "American New York adult male with a raspy, scratchy, rough, or smooth voice." | `9pKX7TwfPxl7p2PNZQ1B` |
| **Donovan** | `apex-sample-donovan.mp3` | American middle-aged male, confident, conversational. | `DMyrgzQFny3JI1Y1paM5` |
| **Miles** | `apex-sample-miles.mp3` | Young American male, calm (Miles Davis-adjacent naming). | `pQh9V7vKVWKF3pBFDSc5` |
| **Orlando — Bold & Steady** | `apex-sample-orlando.mp3` | "Deep, bold, versatile Black male voice with slightly raspy tone." | `4t8HWMowRF0NaJl0r9MS` |

---

## 🎭 CURRENT BASELINE

| Voice | File | Why it's here | Voice ID |
|---|---|---|---|
| **Antoni** | `apex-sample-antoni.mp3` | The voice currently locked in `sovereign_vault.elevenlabs_api_key` and `ceo_brains.voice_id` for APEX. Italian-American baritone — NOT NY Black Gen Z. This is what we're replacing. | `ErXwobaYiN019PkySvjV` |

---

## HOW TO LISTEN

```bash
# From the repo root
cd god-mode-credit/apex/voice-samples

# Play a single sample (macOS)
afplay apex-sample-jamal-urban-street.mp3

# Play a single sample (Linux)
mpg123 apex-sample-jamal-urban-street.mp3

# Play them all back-to-back in ranked order
for f in \
  apex-sample-jamal-urban-street.mp3 \
  apex-sample-jamahal-young-urban.mp3 \
  apex-sample-young-jamal.mp3 \
  apex-sample-darryl-young-raspy.mp3 \
  apex-sample-tyrese-tate-smooth.mp3 \
  apex-sample-carter-ny-street-smart.mp3 \
  apex-sample-jon-paul-charismatic.mp3; do
  echo "=== $f ==="
  afplay "$f"
done
```

**Or**, GitHub will stream the .mp3 files directly from the raw URL once this branch is pushed. Click any file in the GitHub UI → hit the ▶ button.

---

## REGENERATE A SAMPLE

```bash
# Same settings, different text
python3 generate_sample.py \
  Ybqj6CIlqb6M85s9Bl4n \
  apex-sample-jamal-v2.mp3 \
  "Custom test line. Ascend."

# The script uses sovereign_vault.elevenlabs_api_key (hardcoded in the file for now)
# and Multilingual v2 with locked Apex voice settings.
```

---

## AFTER YOU PICK

Once Edwin picks the winner:

1. **Update `sovereign_vault`** → re-key `elevenlabs_apex_voice_id` to the chosen voice ID.
2. **Update `ceo_brains.voice_id`** for APEX (via `apex/scripts/apex_supabase_sync.sql`).
3. **Update `apex/voice-config.md`** → swap the "Antoni" block for the winning voice.
4. **Clone the voice into Coqui XTTS-v2 on the VPS** (see `apex/vps-voice-deployment.md`) so the same voice runs unlimited locally.
5. **Regenerate all 11 VSL scripts with the new voice** → save over `apex/vsl-scripts/*-audio.mp3`.

---

## BONUS: IF NONE OF THESE WIN

If none of the 13 samples hit the exact vibe, the play is:
1. **Find a real-world voice reference** Edwin likes — a YouTuber, podcaster, rapper (spoken interview, not rapping), actor, or speaker. Download 1-3 minutes of clean audio.
2. **Clone it via ElevenLabs Instant Voice Cloning** (Creator plan supports it — Edwin is on Creator per sovereign_vault).
3. **Then also feed the same reference into Coqui XTTS-v2 on the VPS** for the unlimited-throughput path.

Good reference candidates for "NY Black Gen Z authority":
- Jay-Z speaking in interviews (not rapping) — "Wisdom. Calm. Authority."
- Ty Dolla $ign in podcast mode
- Denzel in Training Day monologues (older, but the register works)
- Michael B. Jordan in press interviews
- Kendrick Lamar in spoken interviews
- Jidenna (speaking register — elegant gentleman energy)
- NLE Choppa in motivational mode
- D Smoke (educator energy + hip hop)
- Killer Mike in Run The Jewels interviews

**The best reference for Apex specifically is probably Killer Mike or D Smoke** — both have the "street-smart teacher" energy Apex needs.

---

**Ascend.**
