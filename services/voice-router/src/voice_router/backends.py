"""
TTS backends — a thin, swappable interface for each provider.

Every backend implements:
    tts(voice_id, text, *, format="mp3", **kwargs) -> bytes

`voice_id` is whatever the backend expects:
    - ElevenLabs: the voice ID (e.g. "pQh9V7vKVWKF3pBFDSc5")
    - VoxCPM:     the reference voice name (e.g. "apex-miles-ref")
    - Vapi:       the assistant ID

Backends are stateless. Credentials come from environment variables
(populated at startup from sovereign_vault).
"""

from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from typing import Optional


class TTSBackend:
    name: str = "abstract"

    def tts(self, voice_id: str, text: str, *, format: str = "mp3", **kwargs) -> bytes:
        raise NotImplementedError

    def health(self) -> dict:
        return {"backend": self.name, "ok": False, "reason": "not implemented"}


class ElevenLabsBackend(TTSBackend):
    """ElevenLabs REST API — matches the locked Apex voice settings."""

    name = "elevenlabs"

    def __init__(
        self,
        api_key: Optional[str] = None,
        model_id: str = "eleven_multilingual_v2",
        stability: float = 0.55,
        similarity_boost: float = 0.85,
        style: float = 0.20,
        use_speaker_boost: bool = True,
    ):
        self.api_key = api_key or os.environ.get("ELEVENLABS_API_KEY")
        self.model_id = model_id
        self.settings = {
            "stability": stability,
            "similarity_boost": similarity_boost,
            "style": style,
            "use_speaker_boost": use_speaker_boost,
        }

    def tts(self, voice_id: str, text: str, *, format: str = "mp3", **kwargs) -> bytes:
        if not self.api_key:
            raise RuntimeError("ELEVENLABS_API_KEY not set")
        body = json.dumps({
            "text": text,
            "model_id": self.model_id,
            "voice_settings": self.settings,
        }).encode()
        req = urllib.request.Request(
            f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}",
            data=body,
            headers={
                "xi-api-key": self.api_key,
                "Content-Type": "application/json",
                "Accept": "audio/mpeg",
            },
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=120) as resp:
            return resp.read()

    def health(self) -> dict:
        return {
            "backend": self.name,
            "ok": bool(self.api_key),
            "reason": None if self.api_key else "ELEVENLABS_API_KEY missing",
        }


class VoxCPMBackend(TTSBackend):
    """Self-hosted VoxCPM2 server (see services/voxcpm)."""

    name = "voxcpm"

    def __init__(self, base_url: Optional[str] = None, api_key: Optional[str] = None):
        self.base_url = (base_url or os.environ.get("VOXCPM_URL", "http://localhost:8000")).rstrip("/")
        self.api_key = api_key or os.environ.get("VOXCPM_API_KEY")

    def _headers(self) -> dict:
        h = {"Content-Type": "application/json"}
        if self.api_key:
            h["Authorization"] = f"Bearer {self.api_key}"
        return h

    def tts(self, voice_id: str, text: str, *, format: str = "mp3", **kwargs) -> bytes:
        body = json.dumps({"voice": voice_id, "text": text, "format": format}).encode()
        req = urllib.request.Request(
            f"{self.base_url}/tts",
            data=body,
            headers=self._headers(),
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=300) as resp:
            return resp.read()

    def health(self) -> dict:
        try:
            with urllib.request.urlopen(f"{self.base_url}/health", timeout=5) as resp:
                data = json.loads(resp.read())
            return {"backend": self.name, "ok": True, **data}
        except Exception as e:
            return {"backend": self.name, "ok": False, "reason": str(e)}


class VapiTTSBackend(TTSBackend):
    """Placeholder for Vapi phone assistants (already wired in sovereign_vault).

    Vapi handles TTS internally for phone calls; this backend exists so the
    router can route non-phone text to a Vapi assistant's configured voice
    as a last resort.
    """

    name = "vapi_tts"

    def tts(self, voice_id: str, text: str, *, format: str = "mp3", **kwargs) -> bytes:
        raise NotImplementedError(
            "Vapi does not expose a standalone TTS endpoint. Use ElevenLabs or VoxCPM "
            "for non-phone audio; Vapi handles voice on its own assistant runtime."
        )


# Backend registry — wire-up happens in router.py
BACKENDS = {
    "elevenlabs": ElevenLabsBackend,
    "voxcpm": VoxCPMBackend,
    "vapi_tts": VapiTTSBackend,
}
