"""
VoxCPM2 FastAPI Server — Godfident Empire TTS

A minimal, production-grade HTTP wrapper around VoxCPM2 that matches the
voice router's expected contract. Reference audio files live on disk in
/app/references (mounted from the host) so clones are reused across requests
without re-uploading.

Endpoints:
  GET  /health                  → liveness probe
  GET  /voices                  → list available voice references on disk
  POST /voices                  → upload a new reference (multipart form)
  POST /tts                     → generate audio: {voice, text} → audio/wav

Environment:
  VOXCPM_MODEL_ID     HuggingFace model id (default: openbmb/VoxCPM2)
  VOXCPM_REF_DIR      References directory (default: /app/references)
  VOXCPM_DENOISER     "1" to enable the built-in denoiser (default: "0")
  VOXCPM_API_KEY      Optional bearer token; if set, all /tts and /voices
                      POST endpoints require Authorization: Bearer <token>

The contract is deliberately close to ElevenLabs' TTS shape so swapping
backends in the voice router is a one-line change.
"""

from __future__ import annotations

import io
import os
import tempfile
from pathlib import Path
from typing import Optional

import soundfile as sf
from fastapi import FastAPI, Header, HTTPException, UploadFile, File, Form
from fastapi.responses import Response, JSONResponse
from pydantic import BaseModel, Field

MODEL_ID = os.environ.get("VOXCPM_MODEL_ID", "openbmb/VoxCPM2")
REF_DIR = Path(os.environ.get("VOXCPM_REF_DIR", "/app/references"))
USE_DENOISER = os.environ.get("VOXCPM_DENOISER", "0") == "1"
API_KEY = os.environ.get("VOXCPM_API_KEY")

REF_DIR.mkdir(parents=True, exist_ok=True)

app = FastAPI(title="VoxCPM2 Empire TTS", version="1.0.0")

# Lazy model handle — loaded on first /tts call so the container boots fast
# even when the model is ~4 GB. Subsequent calls reuse the loaded instance.
_model = None
_sample_rate = 48000


def _load_model():
    global _model, _sample_rate
    if _model is not None:
        return _model
    try:
        from voxcpm import VoxCPM
    except ImportError as e:
        raise RuntimeError(f"voxcpm not installed: {e}")
    _model = VoxCPM.from_pretrained(MODEL_ID, load_denoiser=USE_DENOISER)
    # The sample rate property lives on the underlying tts_model
    try:
        _sample_rate = _model.tts_model.sample_rate  # type: ignore[attr-defined]
    except Exception:
        _sample_rate = 48000
    return _model


def _auth_or_raise(authorization: Optional[str]) -> None:
    if not API_KEY:
        return
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing bearer token")
    token = authorization.split(" ", 1)[1].strip()
    if token != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid bearer token")


class TTSRequest(BaseModel):
    voice: str = Field(..., description="Voice reference name (filename stem in /app/references, e.g. 'miles')")
    text: str = Field(..., min_length=1, max_length=10_000)
    format: str = Field("wav", description="'wav' or 'mp3'")


@app.get("/health")
def health():
    return {
        "status": "ok",
        "model_id": MODEL_ID,
        "model_loaded": _model is not None,
        "references_dir": str(REF_DIR),
        "denoiser": USE_DENOISER,
        "sample_rate": _sample_rate if _model is not None else None,
    }


@app.get("/voices")
def list_voices():
    """List available voice references on disk."""
    refs = []
    for p in sorted(REF_DIR.glob("*")):
        if p.is_file() and p.suffix.lower() in {".wav", ".mp3", ".flac", ".ogg", ".m4a"}:
            refs.append({
                "name": p.stem,
                "filename": p.name,
                "size_bytes": p.stat().st_size,
            })
    return {"voices": refs}


@app.post("/voices")
async def upload_voice(
    name: str = Form(..., description="Voice name (used as filename stem)"),
    file: UploadFile = File(..., description="Reference audio (3-10 seconds, clean, single speaker)"),
    authorization: Optional[str] = Header(None),
):
    _auth_or_raise(authorization)
    safe_name = "".join(c for c in name if c.isalnum() or c in "-_").lower()
    if not safe_name:
        raise HTTPException(status_code=400, detail="Invalid voice name")
    suffix = Path(file.filename or "ref.wav").suffix.lower() or ".wav"
    if suffix not in {".wav", ".mp3", ".flac", ".ogg", ".m4a"}:
        raise HTTPException(status_code=400, detail=f"Unsupported extension {suffix}")
    out = REF_DIR / f"{safe_name}{suffix}"
    data = await file.read()
    out.write_bytes(data)
    return {"name": safe_name, "filename": out.name, "size_bytes": len(data)}


@app.post("/tts")
def tts(req: TTSRequest, authorization: Optional[str] = Header(None)):
    _auth_or_raise(authorization)

    # Resolve reference audio path — accept bare name or file name
    candidates = [
        REF_DIR / req.voice,
        *(REF_DIR / f"{req.voice}{ext}" for ext in (".wav", ".mp3", ".flac", ".ogg", ".m4a")),
    ]
    ref_path = next((p for p in candidates if p.exists()), None)
    if ref_path is None:
        raise HTTPException(
            status_code=404,
            detail=f"Voice '{req.voice}' not found in {REF_DIR}. Upload it via POST /voices first.",
        )

    model = _load_model()
    try:
        wav = model.generate(text=req.text, reference_wav_path=str(ref_path))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"VoxCPM generation failed: {e}")

    buf = io.BytesIO()
    out_format = req.format.lower()
    if out_format == "wav":
        sf.write(buf, wav, _sample_rate, format="WAV")
        media_type = "audio/wav"
    elif out_format == "mp3":
        # soundfile doesn't do mp3 natively in all builds; write wav then convert via ffmpeg
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp_wav:
            sf.write(tmp_wav.name, wav, _sample_rate, format="WAV")
            tmp_mp3 = tmp_wav.name.replace(".wav", ".mp3")
        rc = os.system(f"ffmpeg -y -loglevel error -i {tmp_wav.name} -b:a 192k {tmp_mp3}")
        if rc != 0:
            raise HTTPException(status_code=500, detail="mp3 encode failed")
        buf = io.BytesIO(Path(tmp_mp3).read_bytes())
        Path(tmp_wav.name).unlink(missing_ok=True)
        Path(tmp_mp3).unlink(missing_ok=True)
        media_type = "audio/mpeg"
    else:
        raise HTTPException(status_code=400, detail=f"Unsupported format '{req.format}'")

    return Response(content=buf.getvalue(), media_type=media_type)
