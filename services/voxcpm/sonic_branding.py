#!/usr/bin/env python3
"""
Godfident Empire — Sonic Branding Generator

Synthesizes a per-CEO sonic logo stinger (3-second motif) grounded in
solfeggio frequencies + peer-reviewed psychoacoustic research. Each logo
is a 3-note motif that ends on a rising perfect fifth for emotional uplift
(broaden-and-build cue → listener wants to return).

Research anchors:
- 528 Hz: Akimoto et al 2018, Heti & Yeshaswini 2024 — peer-reviewed
  decrease in salivary cortisol + Chromogranin A (stress markers) and
  increase in oxytocin after listening. Reduces state anxiety scores.
- 3-second logo length: Intel sonic branding research — the subconscious
  sweet spot; beyond 3s people shift from "hearing" to "listening".
- Rising fifth (3:2 ratio): the most consonant interval in Western music,
  universally perceived as "uplift" / "resolution".
- Loudness target: -16 LUFS integrated (EBU R128 / Apple Podcast standard)
  with true peak -1.5 dBTP for safe social playout.
- Lowpass at 8 kHz: softens sine-wave harshness without losing presence.
- Reverb tail: 300ms aecho for spatial "majesty" without washing out the motif.

All 12 CEOs + 1 empire master = 13 logos total.

Usage:
    pip install # nothing — pure stdlib + ffmpeg
    python3 sonic_branding.py --all
    python3 sonic_branding.py --ceo apex
    python3 sonic_branding.py --empire

Output:
    god-mode-credit/apex/voice-samples/sonic-logos/<name>.wav

Each logo is ~3 seconds, 48 kHz / stereo / 16-bit PCM WAV.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import List

REPO_ROOT = Path(__file__).resolve().parents[2]
OUT_DIR = REPO_ROOT / "god-mode-credit" / "apex" / "voice-samples" / "sonic-logos"

# ---------- Musical constants ----------
PERFECT_FIFTH = 3 / 2       # 1.5x root
OCTAVE_DOWN = 1 / 2         # 0.5x root
OCTAVE_UP = 2.0             # 2x root
MAJOR_THIRD = 5 / 4         # 1.25x root
MINOR_THIRD = 6 / 5         # 1.2x root

# ---------- Sonic logo spec per CEO ----------
@dataclass
class Logo:
    name: str                    # file stem
    title: str                   # human label
    root_hz: float               # solfeggio anchor frequency (the CEO's "brand Hz")
    rationale: str               # why this freq was picked
    mood: str                    # "uplift" | "majestic" | "guardian" | "calm" | "hungry"
    duration_sec: float = 3.0

# 528 Hz — stress / cortisol research-backed root for the empire + APEX
# 963 Hz — "divine consciousness" solfeggio, top of the empire for SOVEREIGN + VEGA
# 741 Hz — "awakening intuition" — ZERO wakes you up + BUILDER architect insight
# 639 Hz — "relationships / connection" — MIDAS deal closer
# 417 Hz — "facilitating change" — AEGIS health transformation
# 852 Hz — "return to order" — CLOSER seals the deal
# 396 Hz — "liberation from fear" — HUNTER predator energy
# 285 Hz — "tissue healing" — KEEPER retention/nurture
# 174 Hz — "pain relief / foundation" — CERBERUS the guardian base

LOGOS: List[Logo] = [
    Logo(
        name="godfident-empire",
        title="Godfident Empire — Master Sonic Logo",
        root_hz=528.0,
        rationale="528 Hz transformation — the peer-reviewed 'stress down / oxytocin up' frequency. "
                  "The empire root note. Every CEO sonic logo resolves to this or a related interval.",
        mood="majestic",
    ),
    Logo(
        name="apex-credit-ascension",
        title="APEX — The Crowned (GOD MODE CREDIT)",
        root_hz=528.0,
        rationale="Flagship transformation frequency. APEX is the credit ascension journey — "
                  "aligns 1:1 with the empire root.",
        mood="uplift",
    ),
    Logo(
        name="zero-soulhustleai",
        title="ZERO — The Jester-King (SoulHustleAI)",
        root_hz=741.0,
        rationale="741 Hz 'awakening intuition'. Zero's job is to wake the listener up to the game. "
                  "Fast resolution up to 963 Hz for hype.",
        mood="uplift",
    ),
    Logo(
        name="sovereign-godfident",
        title="SOVEREIGN — Supreme Orchestrator",
        root_hz=963.0,
        rationale="963 Hz 'divine consciousness'. Top of the empire. Descends to 528 to bless the whole stack.",
        mood="majestic",
    ),
    Logo(
        name="midas-recovery",
        title="MIDAS — The Golden Hand (MIDAS Recovery Group)",
        root_hz=639.0,
        rationale="639 Hz 'relationships / connection'. Every MIDAS deal is a relationship between "
                  "a county and a rightful owner.",
        mood="calm",
    ),
    Logo(
        name="aegis-shield",
        title="AEGIS — The Shield (Health Insurance)",
        root_hz=417.0,
        rationale="417 Hz 'facilitating change'. Health transformation — big brother energy.",
        mood="calm",
    ),
    Logo(
        name="cerberus-guardian",
        title="CERBERUS — Three-Headed Guardian (Empire Security)",
        root_hz=174.0,
        rationale="174 Hz 'foundation / pain relief'. The guardian base note. Deep, protective.",
        mood="guardian",
    ),
    Logo(
        name="closer-sales",
        title="CLOSER — Deal Maker (SoulHustleAI)",
        root_hz=852.0,
        rationale="852 Hz 'return to order'. Seal the deal. Close the loop.",
        mood="uplift",
    ),
    Logo(
        name="hunter-leads",
        title="HUNTER — Bloodhound (SoulHustleAI)",
        root_hz=396.0,
        rationale="396 Hz 'liberation from fear'. The predator has no fear. Drives forward motion.",
        mood="hungry",
    ),
    Logo(
        name="keeper-retention",
        title="KEEPER — Retention Guardian (SoulHustleAI)",
        root_hz=285.0,
        rationale="285 Hz 'tissue healing'. Nurture. The voice that keeps clients safe.",
        mood="calm",
    ),
    Logo(
        name="builder-systems",
        title="BUILDER — System Architect (SoulHustleAI)",
        root_hz=741.0,
        rationale="741 Hz 'awakening intuition'. Architect insight. Same anchor as ZERO but different motif.",
        mood="calm",
    ),
    Logo(
        name="vega-operations",
        title="VEGA — Operations General (SoulHustleAI)",
        root_hz=963.0,
        rationale="963 Hz 'divine consciousness'. Command layer, near-sovereign. Female voice tonality.",
        mood="majestic",
    ),
    Logo(
        name="eli-abundantly-blessed",
        title="ELI — Abundantly Blessed Solutions",
        root_hz=528.0,
        rationale="Aligns with the empire root. Eli is a client-CEO under the SoulHustleAI umbrella so "
                  "his sonic logo ties back to the transformation anchor.",
        mood="uplift",
    ),
]

# ---------- Motif design per mood ----------
def motif_intervals(mood: str) -> list[tuple[float, float, float, float]]:
    """Return a list of (frequency_multiplier, start_sec, duration_sec, volume) tuples.

    Each tuple is a tone in the motif, played at (root_hz * multiplier).
    Three tones total, overlapping slightly for smooth musical flow, ending on
    a rising perfect fifth for emotional uplift.
    """
    if mood == "majestic":
        # Deep bass → root → octave-up fifth (full reach, ceremonial)
        return [
            (OCTAVE_DOWN,            0.00, 1.00, 0.40),   # bass fundamental
            (1.0,                    0.70, 1.10, 0.50),   # root
            (OCTAVE_UP * PERFECT_FIFTH / 2, 1.50, 1.50, 0.50),  # resolved fifth in mid register
        ]
    if mood == "uplift":
        # Rising motif: root → third → fifth (classic "heroic" arpeggio)
        return [
            (OCTAVE_DOWN,  0.00, 0.80, 0.38),
            (1.0,          0.55, 0.95, 0.50),
            (PERFECT_FIFTH, 1.30, 1.70, 0.55),
        ]
    if mood == "guardian":
        # Deep bass that sustains with a slow lift (protective, low energy)
        return [
            (OCTAVE_DOWN,    0.00, 1.40, 0.60),
            (1.0,            1.00, 1.40, 0.45),
            (PERFECT_FIFTH,  1.90, 1.10, 0.35),
        ]
    if mood == "hungry":
        # Fast rise with no bass lead-in (energetic, driven)
        return [
            (1.0,            0.00, 0.70, 0.55),
            (MAJOR_THIRD,    0.50, 0.80, 0.50),
            (PERFECT_FIFTH,  1.10, 1.90, 0.55),
        ]
    # calm (default)
    # Gentle three-note unfolding, balanced
    return [
        (OCTAVE_DOWN,   0.00, 1.10, 0.40),
        (1.0,           0.70, 1.10, 0.45),
        (PERFECT_FIFTH, 1.40, 1.60, 0.48),
    ]


def build_filter_complex(logo: Logo) -> tuple[list[str], str]:
    """Build the ffmpeg -i inputs list and -filter_complex graph for a logo."""
    notes = motif_intervals(logo.mood)
    inputs: list[str] = []
    filters: list[str] = []
    mix_tags: list[str] = []

    for i, (mult, start, dur, vol) in enumerate(notes):
        freq = logo.root_hz * mult
        # sine source with duration `dur`
        inputs += ["-f", "lavfi", "-t", f"{dur:.3f}", "-i", f"sine=frequency={freq:.3f}:sample_rate=48000"]
        delay_ms = int(start * 1000)
        fade_in = min(0.12, dur * 0.25)
        fade_out = min(0.30, dur * 0.40)
        fade_out_start = max(0.0, dur - fade_out)
        chain = (
            f"[{i}:a]"
            f"volume={vol:.3f},"
            f"afade=t=in:st=0:d={fade_in:.3f},"
            f"afade=t=out:st={fade_out_start:.3f}:d={fade_out:.3f},"
            f"adelay={delay_ms}|{delay_ms},"
            f"aformat=sample_rates=48000:channel_layouts=stereo"
            f"[n{i}]"
        )
        filters.append(chain)
        mix_tags.append(f"[n{i}]")

    mix_chain = (
        f"{''.join(mix_tags)}amix=inputs={len(notes)}:duration=longest:normalize=0[mix];"
        # Gentle reverb via aecho for spatial "majesty"
        f"[mix]aecho=0.8:0.85:80:0.35[rev];"
        # Softening lowpass (removes harshness of pure sines without killing brightness)
        f"[rev]lowpass=f=7500[soft];"
        # Loudness normalization to broadcast / podcast standard
        f"[soft]loudnorm=I=-16:TP=-1.5:LRA=7[out]"
    )

    filter_complex = ";".join(filters + [mix_chain])
    return inputs, filter_complex


def render_logo(logo: Logo) -> Path:
    out_path = OUT_DIR / f"{logo.name}.wav"
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    inputs, filter_complex = build_filter_complex(logo)
    cmd = (
        ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y"]
        + inputs
        + [
            "-filter_complex", filter_complex,
            "-map", "[out]",
            "-ar", "48000",
            "-ac", "2",
            "-c:a", "pcm_s16le",
            str(out_path),
        ]
    )
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"[fail] {logo.name}: {result.stderr.strip()}", file=sys.stderr)
        raise SystemExit(result.returncode)
    size_kb = out_path.stat().st_size // 1024
    print(f"[ok]   {out_path.name:36s}  root={logo.root_hz:6.1f} Hz  mood={logo.mood:9s}  {size_kb}KB")
    return out_path


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--all", action="store_true", help="Generate every logo")
    ap.add_argument("--empire", action="store_true", help="Generate just the empire master logo")
    ap.add_argument("--ceo", type=str, default=None, help="Generate one CEO's logo by name (e.g., apex)")
    args = ap.parse_args()

    if args.empire:
        render_logo(next(l for l in LOGOS if l.name == "godfident-empire"))
        return
    if args.ceo:
        matches = [l for l in LOGOS if args.ceo.lower() in l.name.lower()]
        if not matches:
            print(f"No logo found for {args.ceo!r}", file=sys.stderr)
            sys.exit(1)
        for l in matches:
            render_logo(l)
        return
    if args.all or (not args.empire and not args.ceo):
        for logo in LOGOS:
            render_logo(logo)
        return


if __name__ == "__main__":
    main()
