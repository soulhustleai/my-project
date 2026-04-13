# syntax=docker/dockerfile:1.6
# ============================================================================
# VoxCPM2 — Godfident Empire TTS Server
# ============================================================================
# Base: NVIDIA CUDA 12.4 runtime on Ubuntu 22.04. This image is the deployable
# artifact for the VPS: GPU-accelerated VoxCPM2 inference with a FastAPI HTTP
# wrapper so the voice router can call it like any other TTS backend.
#
# Expected host: Ubuntu 22.04+ with:
#   - NVIDIA GPU (8GB+ VRAM)
#   - NVIDIA driver ≥ 550
#   - nvidia-container-toolkit installed
#
# Build:
#   docker build -t voxcpm-empire:latest services/voxcpm
#
# Run:
#   docker run --gpus all -p 8000:8000 \
#     -v /opt/voxcpm/references:/app/references \
#     -v /opt/voxcpm/cache:/root/.cache \
#     -e VOXCPM_MODEL_ID=openbmb/VoxCPM2 \
#     voxcpm-empire:latest
#
# Health check:
#   curl http://localhost:8000/health
# ============================================================================

FROM nvidia/cuda:12.4.1-cudnn-runtime-ubuntu22.04

ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    HF_HOME=/root/.cache/huggingface \
    TRANSFORMERS_CACHE=/root/.cache/huggingface

RUN apt-get update && apt-get install -y --no-install-recommends \
      python3.11 python3.11-venv python3-pip \
      ffmpeg libsndfile1 git curl ca-certificates \
    && rm -rf /var/lib/apt/lists/* \
    && ln -sf /usr/bin/python3.11 /usr/local/bin/python \
    && ln -sf /usr/bin/python3.11 /usr/local/bin/python3

WORKDIR /app

# Install PyTorch matched to CUDA 12.4 first (voxcpm depends on torch >= 2.5)
RUN python -m pip install --upgrade pip setuptools wheel \
 && python -m pip install \
      torch==2.5.1 torchaudio==2.5.1 \
      --index-url https://download.pytorch.org/whl/cu124

# Core TTS + API deps
RUN python -m pip install \
      voxcpm \
      fastapi \
      "uvicorn[standard]" \
      soundfile \
      pydantic \
      python-multipart \
      requests

# Optional: install the high-throughput serving engine if it's available on PyPI.
# Safe to fail during build — the FastAPI wrapper works without it.
RUN python -m pip install nano-vllm-voxcpm || echo "nano-vllm-voxcpm not on PyPI yet, falling back to stock voxcpm"

# Copy the FastAPI wrapper
COPY server.py /app/server.py

# Pre-create reference directory
RUN mkdir -p /app/references /root/.cache/huggingface

# Pre-download the model at build time (optional; comment out if building on
# a machine without GPU — then model downloads lazily on first call)
# RUN python -c "from voxcpm import VoxCPM; VoxCPM.from_pretrained('openbmb/VoxCPM2', load_denoiser=False)"

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=10s --start-period=120s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1

CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1"]
