#!/usr/bin/env bash
# =============================================================================
# VoxCPM2 — one-shot VPS installer
# =============================================================================
# Installs everything VoxCPM needs on a fresh Ubuntu 22.04 VPS with an NVIDIA
# GPU, builds the Empire TTS container, and starts it as a systemd-managed
# service that survives reboots.
#
# Usage (on the VPS):
#   curl -fsSL https://raw.githubusercontent.com/soulhustleai/my-project/main/services/voxcpm/install.sh | sudo bash
#
# Or pull the repo first and run locally:
#   sudo bash services/voxcpm/install.sh
#
# What it does:
#   1. Verifies NVIDIA driver + nvidia-smi work
#   2. Installs Docker + Docker Compose plugin if missing
#   3. Installs nvidia-container-toolkit if missing
#   4. Creates /opt/voxcpm/{references,cache} directories
#   5. Generates a random VOXCPM_API_KEY and writes /opt/voxcpm/.env
#   6. Builds the voxcpm-empire image
#   7. Installs and starts a systemd unit wrapping docker compose
#   8. Prints the API key and health check command
#
# Requires: root / sudo.
# =============================================================================

set -euo pipefail

GREEN='\033[0;32m'; YELLOW='\033[1;33m'; RED='\033[0;31m'; NC='\033[0m'
log()  { echo -e "${GREEN}[voxcpm-install]${NC} $*"; }
warn() { echo -e "${YELLOW}[voxcpm-install]${NC} $*"; }
die()  { echo -e "${RED}[voxcpm-install]${NC} $*" >&2; exit 1; }

[[ $EUID -eq 0 ]] || die "Run as root (sudo bash install.sh)"

log "Step 1/8  Checking GPU"
if ! command -v nvidia-smi &>/dev/null; then
  die "nvidia-smi not found. Install the NVIDIA driver for your GPU first."
fi
nvidia-smi --query-gpu=name,driver_version,memory.total --format=csv,noheader

log "Step 2/8  Installing Docker (if missing)"
if ! command -v docker &>/dev/null; then
  apt-get update
  apt-get install -y ca-certificates curl gnupg
  install -m 0755 -d /etc/apt/keyrings
  curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
  chmod a+r /etc/apt/keyrings/docker.asc
  echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] \
    https://download.docker.com/linux/ubuntu $(. /etc/os-release && echo $VERSION_CODENAME) stable" \
    | tee /etc/apt/sources.list.d/docker.list > /dev/null
  apt-get update
  apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
  systemctl enable --now docker
fi
docker version --format 'Docker {{.Server.Version}}'

log "Step 3/8  Installing nvidia-container-toolkit (if missing)"
if ! dpkg -l | grep -q nvidia-container-toolkit; then
  curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg
  curl -fsSL https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list \
    | sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' \
    | tee /etc/apt/sources.list.d/nvidia-container-toolkit.list
  apt-get update
  apt-get install -y nvidia-container-toolkit
  nvidia-ctk runtime configure --runtime=docker
  systemctl restart docker
fi

log "Step 4/8  Creating /opt/voxcpm directory tree"
mkdir -p /opt/voxcpm/{references,cache,app}
chmod 755 /opt/voxcpm

log "Step 5/8  Generating API key and .env"
if [[ ! -f /opt/voxcpm/.env ]]; then
  API_KEY="voxcpm_$(tr -dc 'a-zA-Z0-9' </dev/urandom | head -c 40)"
  cat > /opt/voxcpm/.env <<EOF
VOXCPM_MODEL_ID=openbmb/VoxCPM2
VOXCPM_DENOISER=0
VOXCPM_API_KEY=${API_KEY}
EOF
  chmod 600 /opt/voxcpm/.env
  log "Generated VOXCPM_API_KEY — save this into sovereign_vault.voxcpm_api_key:"
  echo "    ${API_KEY}"
else
  warn "/opt/voxcpm/.env exists — keeping existing VOXCPM_API_KEY"
fi

log "Step 6/8  Copying service files to /opt/voxcpm/app"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cp "$SCRIPT_DIR/Dockerfile"         /opt/voxcpm/app/
cp "$SCRIPT_DIR/server.py"          /opt/voxcpm/app/
cp "$SCRIPT_DIR/docker-compose.yml" /opt/voxcpm/app/

log "Step 7/8  Building voxcpm-empire image (this can take 10-20 minutes on first run)"
cd /opt/voxcpm/app
docker compose --env-file /opt/voxcpm/.env build

log "Step 8/8  Installing systemd unit + starting service"
cat > /etc/systemd/system/voxcpm-empire.service <<'EOF'
[Unit]
Description=VoxCPM2 Empire TTS (Godfident)
Requires=docker.service
After=docker.service network-online.target
Wants=network-online.target

[Service]
Type=simple
Restart=always
RestartSec=10
WorkingDirectory=/opt/voxcpm/app
EnvironmentFile=/opt/voxcpm/.env
ExecStart=/usr/bin/docker compose --env-file /opt/voxcpm/.env up
ExecStop=/usr/bin/docker compose --env-file /opt/voxcpm/.env down

[Install]
WantedBy=multi-user.target
EOF
systemctl daemon-reload
systemctl enable --now voxcpm-empire.service
sleep 3

log "Done."
echo ""
echo "Health check:"
echo "  curl http://localhost:8000/health"
echo ""
echo "Upload a voice reference:"
echo "  curl -X POST -H \"Authorization: Bearer \$VOXCPM_API_KEY\" \\"
echo "       -F name=miles -F file=@/path/to/miles-reference.wav \\"
echo "       http://localhost:8000/voices"
echo ""
echo "Generate a sample:"
echo "  curl -X POST -H \"Authorization: Bearer \$VOXCPM_API_KEY\" \\"
echo "       -H \"Content-Type: application/json\" \\"
echo "       -d '{\"voice\":\"miles\",\"text\":\"Ascend.\"}' \\"
echo "       --output sample.wav \\"
echo "       http://localhost:8000/tts"
echo ""
log "Service status: systemctl status voxcpm-empire"
log "Service logs:   journalctl -u voxcpm-empire -f"
