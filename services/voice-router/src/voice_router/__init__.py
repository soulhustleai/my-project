"""
voice_router — Godfident Empire TTS backend abstraction.

A single entry point (`speak()`) that looks up a CEO in Supabase ceo_brains,
reads their voice_backend + voice_id + voice_reference_url, and dispatches
to the correct TTS provider. Lets us cut over from ElevenLabs → VoxCPM2 by
flipping `voice_backend` in one row without touching any calling code.

Usage:
    from voice_router import speak

    mp3_bytes = speak(
        ceo="apex",
        text="The laws were written for you. You just never read them. Ascend.",
    )
    # bytes are audio/mpeg (or audio/wav if format='wav')

Backends:
    - elevenlabs  → ElevenLabs REST API (legacy/flagship)
    - voxcpm      → Self-hosted VoxCPM2 on the VPS (default target)
    - vapi_tts    → Pass-through to a pre-configured Vapi assistant (phone calls)

Config resolution order (first wins):
    1. Explicit kwargs to speak()
    2. Supabase ceo_brains row
    3. Environment variables (VOXCPM_URL, ELEVENLABS_API_KEY, etc)
    4. Hardcoded fallback to ElevenLabs Miles

Secrets are pulled from sovereign_vault at module load time via the
bundled `_vault_client` helper.
"""

from .router import speak, speak_bytes, list_ceos, refresh_registry
from .backends import ElevenLabsBackend, VoxCPMBackend
from .registry import CEOVoice

__version__ = "1.0.0"
__all__ = [
    "speak",
    "speak_bytes",
    "list_ceos",
    "refresh_registry",
    "ElevenLabsBackend",
    "VoxCPMBackend",
    "CEOVoice",
]
