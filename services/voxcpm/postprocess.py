#!/usr/bin/env python3
"""
Godfident Empire — Voice Post-Processing Pipeline

Takes a raw TTS render (from VoxCPM, ElevenLabs, or any file on disk) and
applies the CEO's locked psychoacoustic profile, then crossfades into the
CEO's sonic logo tail. Output is a fully-branded asset ready to ship.

The filter chain (per CEO):
  1. High-pass (clean subsonic rumble)
  2. Parametric EQ bands (proximity boost, mid-cut, presence, airband)
  3. Compression (per-profile ratio + attack/release)
  4. Reverb via aecho (pre-delay, decay, wet level)
  5. Loudness normalization to target LUFS (EBU R128 / Apple Podcast standard)
  6. Crossfade 500ms into the CEO sonic logo tail
  7. Final loudness pass on the concatenated asset

Every stage is pure ffmpeg — no external processing libraries. Runs on any
machine with ffmpeg installed (including the VPS).

Usage:
    python3 postprocess.py --ceo apex --input raw.mp3 --output branded.mp3
    python3 postprocess.py --ceo zero --input raw.wav --output branded.wav --format wav
    python3 postprocess.py --ceo apex --input raw.mp3  # output defaults to <stem>-<ceo>-branded.mp3

Called automatically by services/voice-router when configured — see
voice_router/router.py for the hook.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path
from typing import Optional

# Add this directory to path for local import
sys.path.insert(0, str(Path(__file__).resolve().parent))

from voice_profiles import VoiceProfile, get as get_profile  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parents[2]
LOGOS_DIR = REPO_ROOT / "god-mode-credit" / "apex" / "voice-samples" / "sonic-logos"


def _eq_filter_string(profile: VoiceProfile) -> str:
    """Build an ffmpeg EQ filter chain string from the profile's EQ bands."""
    parts: list[str] = []
    for band in profile.eq_bands:
        if band.filter_type == "highpass":
            parts.append(f"highpass=f={band.freq_hz:.0f}")
        elif band.filter_type == "lowpass":
            parts.append(f"lowpass=f={band.freq_hz:.0f}")
        elif band.filter_type == "peak":
            # equalizer f=F t=q w=Q g=G
            parts.append(
                f"equalizer=f={band.freq_hz:.0f}:t=q:w={band.q:.2f}:g={band.gain_db:.2f}"
            )
        elif band.filter_type == "lowshelf":
            parts.append(
                f"bass=frequency={band.freq_hz:.0f}:gain={band.gain_db:.2f}"
            )
        elif band.filter_type == "highshelf":
            parts.append(
                f"treble=frequency={band.freq_hz:.0f}:gain={band.gain_db:.2f}"
            )
    return ",".join(parts)


def _compressor_filter(profile: VoiceProfile) -> str:
    """Build the ffmpeg acompressor filter string.

    Note: ffmpeg acompressor expects:
      - threshold: linear amplitude (0 to 1), NOT dB
      - attack/release: in milliseconds (NOT seconds)
      - makeup: linear factor in [1, 64] (1.0 = unity gain)
    """
    c = profile.compression
    if c is None:
        return ""
    threshold_lin = max(0.00097563, min(1.0, 10 ** (c.threshold_db / 20)))
    makeup_lin = max(1.0, min(64.0, 10 ** (c.makeup_gain_db / 20)))
    return (
        f"acompressor=threshold={threshold_lin:.4f}"
        f":ratio={c.ratio:.2f}"
        f":attack={c.attack_ms:.2f}"
        f":release={c.release_ms:.2f}"
        f":makeup={makeup_lin:.3f}"
    )


def _reverb_filter(profile: VoiceProfile) -> str:
    """Build the ffmpeg aecho-based reverb approximation."""
    r = profile.reverb
    if r is None:
        return ""
    # aecho=in_gain:out_gain:delays:decays
    # Use 3 taps at fractions of the decay time for a denser tail
    tap1 = r.predelay_ms
    tap2 = int(r.predelay_ms + r.decay_s * 400)
    tap3 = int(r.predelay_ms + r.decay_s * 800)
    delays = f"{tap1}|{tap2}|{tap3}"
    # Convert wet_db to linear gain (inverse dB)
    wet_lin = 10 ** (r.wet_db / 20)
    decays = f"{wet_lin:.3f}|{wet_lin * 0.6:.3f}|{wet_lin * 0.35:.3f}"
    return f"aecho=0.8:0.9:{delays}:{decays}"


def _loudnorm_filter(profile: VoiceProfile) -> str:
    """Build the ffmpeg loudnorm filter string."""
    return (
        f"loudnorm=I={profile.lufs_target:.1f}"
        f":TP={profile.true_peak_db:.1f}"
        f":LRA=7"
    )


def build_voice_filter_chain(profile: VoiceProfile) -> str:
    """Build the full audio filter chain for the voice body (before logo tail)."""
    stages: list[str] = []
    eq = _eq_filter_string(profile)
    if eq:
        stages.append(eq)
    comp = _compressor_filter(profile)
    if comp:
        stages.append(comp)
    rev = _reverb_filter(profile)
    if rev:
        stages.append(rev)
    stages.append(_loudnorm_filter(profile))
    return ",".join(stages)


def process(
    input_path: Path,
    output_path: Path,
    ceo: str,
    fmt: str = "mp3",
    append_logo: bool = True,
    verbose: bool = False,
) -> Path:
    """Apply the CEO profile to `input_path`, append sonic logo, write to `output_path`."""
    profile = get_profile(ceo)
    filter_chain = build_voice_filter_chain(profile)

    if not append_logo or not profile.sonic_logo:
        # Simple single-stage: voice body only
        cmd = [
            "ffmpeg", "-hide_banner", "-y",
            "-i", str(input_path),
            "-af", filter_chain,
            "-ar", "48000",
            "-ac", "2",
        ]
        if fmt == "mp3":
            cmd += ["-c:a", "libmp3lame", "-b:a", "192k"]
        else:
            cmd += ["-c:a", "pcm_s16le"]
        cmd += [str(output_path)]
        if verbose:
            print("ffmpeg:", " ".join(cmd))
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            raise RuntimeError(f"ffmpeg failed: {result.stderr.strip()}")
        return output_path

    # Two-stage: voice body -> concat with logo tail (500ms crossfade)
    logo_path = LOGOS_DIR / f"{profile.sonic_logo}.wav"
    if not logo_path.exists():
        raise FileNotFoundError(f"Sonic logo not found: {logo_path}")

    # filter_complex: filter voice body, then acrossfade with the logo
    filter_complex = (
        f"[0:a]{filter_chain}[voice];"
        f"[voice][1:a]acrossfade=d=0.5:c1=tri:c2=tri,"
        f"loudnorm=I={profile.lufs_target:.1f}:TP={profile.true_peak_db:.1f}:LRA=9[out]"
    )

    cmd = [
        "ffmpeg", "-hide_banner", "-y",
        "-i", str(input_path),
        "-i", str(logo_path),
        "-filter_complex", filter_complex,
        "-map", "[out]",
        "-ar", "48000",
        "-ac", "2",
    ]
    if fmt == "mp3":
        cmd += ["-c:a", "libmp3lame", "-b:a", "192k"]
    else:
        cmd += ["-c:a", "pcm_s16le"]
    cmd += [str(output_path)]

    if verbose:
        print("ffmpeg:", " ".join(cmd))
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"ffmpeg failed: {result.stderr.strip()[:800]}")
    return output_path


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ceo", required=True, help="CEO name (e.g. apex, zero, sovereign)")
    ap.add_argument("--input", required=True, help="Input audio file")
    ap.add_argument("--output", default=None, help="Output file (default: <stem>-<ceo>-branded.<ext>)")
    ap.add_argument("--format", default="mp3", choices=["mp3", "wav"])
    ap.add_argument("--no-logo", action="store_true", help="Skip appending the sonic logo tail")
    ap.add_argument("--verbose", "-v", action="store_true")
    args = ap.parse_args()

    input_path = Path(args.input).resolve()
    if not input_path.exists():
        print(f"Input not found: {input_path}", file=sys.stderr)
        sys.exit(1)

    if args.output:
        output_path = Path(args.output).resolve()
    else:
        stem = input_path.stem
        output_path = input_path.parent / f"{stem}-{args.ceo.lower()}-branded.{args.format}"

    try:
        process(
            input_path=input_path,
            output_path=output_path,
            ceo=args.ceo,
            fmt=args.format,
            append_logo=not args.no_logo,
            verbose=args.verbose,
        )
    except Exception as e:
        print(f"ERR: {e}", file=sys.stderr)
        sys.exit(2)

    size_kb = output_path.stat().st_size // 1024
    print(f"OK  {output_path}  {size_kb}KB")


if __name__ == "__main__":
    main()
