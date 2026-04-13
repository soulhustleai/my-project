"""
Top-level speak() dispatcher.

Usage:
    from voice_router import speak
    audio = speak(ceo="apex", text="Ascend.")

The router:
    1. Looks up the CEO in the registry (Supabase ceo_brains)
    2. Selects the backend from ceo.voice_backend
    3. Dispatches to the backend with ceo.voice_id
    4. (Optional) Post-processes via services/voxcpm/postprocess.py so the
       output includes CEO psychoacoustic profile + sonic logo tail
    5. Returns audio bytes (mp3 by default)

Post-processing is ON by default. Disable with VOICE_ROUTER_POSTPROCESS=0
for raw backend output (useful for debugging the TTS backend in isolation).

Falls back to ElevenLabs Miles if the requested CEO has no configured
voice yet — prevents runtime errors while the empire migrates to VoxCPM.
"""

from __future__ import annotations

import os
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Optional

from .backends import BACKENDS, TTSBackend
from .registry import get_ceo, list_ceos as _list_ceos, refresh_registry

# Fallback voice — Miles on ElevenLabs (matches ceo_brains APEX row)
FALLBACK_BACKEND = "elevenlabs"
FALLBACK_VOICE_ID = "pQh9V7vKVWKF3pBFDSc5"  # Miles
FALLBACK_CEO_FOR_POSTPROCESS = "APEX"       # default profile when the caller has no CEO

POSTPROCESS_ENABLED = os.environ.get("VOICE_ROUTER_POSTPROCESS", "1") == "1"
# Default path resolution:
#   __file__ = services/voice-router/src/voice_router/router.py
#   parents[0] voice_router    parents[1] src
#   parents[2] voice-router    parents[3] services
#   parents[4] my-project (repo root)
# Post-processor lives at services/voxcpm/postprocess.py
POSTPROCESS_SCRIPT = os.environ.get(
    "VOICE_ROUTER_POSTPROCESS_SCRIPT",
    str(Path(__file__).resolve().parents[4] / "services" / "voxcpm" / "postprocess.py"),
)

_BACKEND_CACHE: dict[str, TTSBackend] = {}


def _postprocess_bytes(raw_audio: bytes, ceo: str, fmt: str = "mp3") -> bytes:
    """Run the raw TTS bytes through the CEO's psychoacoustic post-processor.

    Shells out to services/voxcpm/postprocess.py (same machine). If the script
    is not available or post-processing is disabled, returns the raw bytes
    unchanged so the pipeline is graceful when deployed without the VoxCPM
    container.
    """
    if not POSTPROCESS_ENABLED:
        return raw_audio

    script = Path(POSTPROCESS_SCRIPT)
    if not script.exists():
        # Silent fallback — log once per process and keep going
        print(
            f"[voice_router] WARN: postprocess script not found at {script}, "
            "returning raw TTS bytes.",
            file=sys.stderr,
        )
        return raw_audio

    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        in_path = tmp_path / f"in.{fmt}"
        out_path = tmp_path / f"out.{fmt}"
        in_path.write_bytes(raw_audio)
        try:
            result = subprocess.run(
                [
                    sys.executable, str(script),
                    "--ceo", ceo,
                    "--input", str(in_path),
                    "--output", str(out_path),
                    "--format", fmt,
                ],
                capture_output=True,
                text=True,
                timeout=120,
            )
        except subprocess.TimeoutExpired:
            print("[voice_router] WARN: postprocess timed out, returning raw bytes.", file=sys.stderr)
            return raw_audio
        if result.returncode != 0:
            print(
                f"[voice_router] WARN: postprocess failed rc={result.returncode}: "
                f"{result.stderr.strip()[:300]}. Returning raw bytes.",
                file=sys.stderr,
            )
            return raw_audio
        return out_path.read_bytes()


def _get_backend(name: str) -> TTSBackend:
    if name not in _BACKEND_CACHE:
        cls = BACKENDS.get(name)
        if cls is None:
            raise ValueError(f"Unknown voice backend '{name}'. Valid: {sorted(BACKENDS.keys())}")
        _BACKEND_CACHE[name] = cls()
    return _BACKEND_CACHE[name]


def speak_bytes(
    *,
    ceo: Optional[str] = None,
    text: str,
    backend: Optional[str] = None,
    voice_id: Optional[str] = None,
    format: str = "mp3",
    postprocess: Optional[bool] = None,
) -> bytes:
    """Generate audio for the given text.

    Resolution order for backend + voice_id:
        1. Explicit kwargs (backend, voice_id)
        2. CEO row in the registry
        3. Global fallback (ElevenLabs Miles)

    Post-processing (CEO psychoacoustic profile + sonic logo tail) is applied
    by default. Pass postprocess=False for raw TTS bytes.
    """
    # --- backend + voice_id resolution ---
    if backend and voice_id:
        raw = _get_backend(backend).tts(voice_id, text, format=format)
        ceo_for_pp = ceo or FALLBACK_CEO_FOR_POSTPROCESS
    elif ceo:
        row = get_ceo(ceo)
        if row is None:
            raise KeyError(
                f"CEO '{ceo}' not found in registry. Run refresh_registry() after migrations."
            )
        bk = backend or row.voice_backend or FALLBACK_BACKEND
        vid = voice_id or row.voice_id
        if not vid:
            print(
                f"[voice_router] WARN: {ceo!r} has no voice_id configured — using fallback Miles.",
                file=sys.stderr,
            )
            bk, vid = FALLBACK_BACKEND, FALLBACK_VOICE_ID
        raw = _get_backend(bk).tts(vid, text, format=format)
        ceo_for_pp = ceo
    else:
        raw = _get_backend(FALLBACK_BACKEND).tts(FALLBACK_VOICE_ID, text, format=format)
        ceo_for_pp = FALLBACK_CEO_FOR_POSTPROCESS

    # --- post-processing ---
    do_pp = POSTPROCESS_ENABLED if postprocess is None else postprocess
    if do_pp:
        return _postprocess_bytes(raw, ceo_for_pp, fmt=format)
    return raw


def speak(*, ceo: Optional[str] = None, text: str, out_path: Optional[str] = None, **kwargs) -> str:
    """Convenience wrapper that writes the audio to disk.

    Returns the output path.
    """
    data = speak_bytes(ceo=ceo, text=text, **kwargs)
    if out_path is None:
        fmt = kwargs.get("format", "mp3")
        out_path = f"/tmp/voice_{(ceo or 'fallback').lower()}.{fmt}"
    with open(out_path, "wb") as f:
        f.write(data)
    return out_path


def list_ceos():
    return _list_ceos()


def health() -> dict:
    """Report the health of every configured backend."""
    return {name: cls().health() for name, cls in BACKENDS.items()}
