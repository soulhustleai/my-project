"""
Top-level speak() dispatcher.

Usage:
    from voice_router import speak
    audio = speak(ceo="apex", text="Ascend.")

The router:
    1. Looks up the CEO in the registry (Supabase ceo_brains)
    2. Selects the backend from ceo.voice_backend
    3. Dispatches to the backend with ceo.voice_id
    4. Returns audio bytes (mp3 by default)

Falls back to ElevenLabs Miles if the requested CEO has no configured
voice yet — prevents runtime errors while the empire migrates to VoxCPM.
"""

from __future__ import annotations

from typing import Optional

from .backends import BACKENDS, TTSBackend
from .registry import get_ceo, list_ceos as _list_ceos, refresh_registry

# Fallback voice — Miles on ElevenLabs (matches ceo_brains APEX row)
FALLBACK_BACKEND = "elevenlabs"
FALLBACK_VOICE_ID = "pQh9V7vKVWKF3pBFDSc5"  # Miles

_BACKEND_CACHE: dict[str, TTSBackend] = {}


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
) -> bytes:
    """Generate audio for the given text.

    Resolution order for backend + voice_id:
        1. Explicit kwargs (backend, voice_id)
        2. CEO row in the registry
        3. Global fallback (ElevenLabs Miles)
    """
    if backend and voice_id:
        return _get_backend(backend).tts(voice_id, text, format=format)

    if ceo:
        row = get_ceo(ceo)
        if row is None:
            raise KeyError(f"CEO '{ceo}' not found in registry. Run refresh_registry() after migrations.")
        bk = backend or row.voice_backend or FALLBACK_BACKEND
        vid = voice_id or row.voice_id
        if not vid:
            # CEO has no voice yet — use the fallback but log it
            import sys
            print(
                f"[voice_router] WARN: {ceo!r} has no voice_id configured — using fallback Miles.",
                file=sys.stderr,
            )
            bk, vid = FALLBACK_BACKEND, FALLBACK_VOICE_ID
        return _get_backend(bk).tts(vid, text, format=format)

    # Raw fallback
    return _get_backend(FALLBACK_BACKEND).tts(FALLBACK_VOICE_ID, text, format=format)


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
