# VoxCPM2 Migration Plan
## ElevenLabs → Self-Hosted VoxCPM2 on the VPS

> **⚠️ DO NOT CANCEL ELEVENLABS UNTIL PHASE 5 VALIDATION PASSES.** We run both in parallel for ~24-48 hours while we validate VoxCPM quality. One slip and every CEO loses their voice. Cancel only after the health check + 3 production renders come back clean.

---

## WHY

- **Cost:** ElevenLabs Creator is $22/mo + usage. VoxCPM2 self-hosted is **free forever** after the VPS is already paid for (Edwin confirmed: 24/7 VPS already running).
- **Throughput:** Creator plan = 172K chars/month. VoxCPM on an 8GB GPU = **unlimited** (hard-capped only by real-time factor, ~10 seconds of audio per second of compute).
- **Control:** Voice cloning happens on Edwin's own hardware. No third-party sees the reference audio.
- **Character authenticity:** ElevenLabs pre-made voices skew white/European. VoxCPM clones from reference clips → every CEO sounds like their actual personality, no substitutions.

---

## PHASES

### PHASE 0 — Prep (complete ✅)

- [x] Research VoxCPM2 install + licensing
- [x] Build `services/voxcpm/` deployment scaffold (Dockerfile + FastAPI + install script + systemd unit)
- [x] Build `services/voice-router/` TTS backend abstraction
- [x] Extend `ceo_brains` schema: `voice_backend`, `voice_reference_url`, `voice_status`
- [x] Write `docs/CEO-VOICE-MATRIX.md` with personality → reference mapping for all 12 CEOs

### PHASE 1 — VPS install (requires Edwin to provide SSH access)

- [ ] Add VPS credentials to `sovereign_vault`:
  - `vps_host` (IP or hostname)
  - `vps_user` (usually `root` or `ubuntu`)
  - `vps_ssh_key` (private key, or `vps_ssh_password`)
  - `vps_provider` (hetzner / contabo / digital ocean / etc)
- [ ] Run `services/voxcpm/install.sh` on the VPS as root:
  ```bash
  ssh $VPS_USER@$VPS_HOST 'sudo bash -s' < services/voxcpm/install.sh
  ```
- [ ] Verify GPU + health check:
  ```bash
  ssh $VPS_USER@$VPS_HOST 'nvidia-smi && curl -s http://localhost:8000/health'
  ```
- [ ] Copy the generated `VOXCPM_API_KEY` from the install log and store in `sovereign_vault.voxcpm_api_key`
- [ ] Store `sovereign_vault.voxcpm_url` = `http://<vps_host>:8000` (or behind a reverse proxy with HTTPS — recommended)

### PHASE 2 — Voice reference collection

- [ ] For each CEO in `docs/CEO-VOICE-MATRIX.md`, Edwin records or sources a 3-10 second reference clip:
  - SOVEREIGN: Edwin records 30 seconds of himself reading the Sovereign mission
  - APEX + ZERO: generate 10 seconds with their existing ElevenLabs voice (we already have them locked) and use those as the VoxCPM reference — this preserves Miles + Tyrese Tate exactly across backends
  - The other 7 CEOs: Edwin picks from the candidate list in the matrix or provides his own reference URLs
  - ELI: Edwin decides Option A (consent + real voice) or Option B (proxy) — see matrix
- [ ] Drop each clip at `god-mode-credit/apex/voice-samples/references/<suggested-name>.wav`
- [ ] Commit + push

### PHASE 3 — Upload references to VoxCPM server

- [ ] For each reference:
  ```bash
  curl -X POST \
       -H "Authorization: Bearer $VOXCPM_API_KEY" \
       -F name=<suggested-name> \
       -F file=@god-mode-credit/apex/voice-samples/references/<suggested-name>.wav \
       $VOXCPM_URL/voices
  ```
- [ ] Verify with `curl $VOXCPM_URL/voices` — should list all uploaded refs

### PHASE 4 — Flip `ceo_brains` rows to VoxCPM backend (one CEO at a time)

```sql
-- Example for APEX:
UPDATE ceo_brains SET
  voice_backend = 'voxcpm',
  voice_id = 'apex-miles',
  voice_reference_url = 'https://raw.githubusercontent.com/soulhustleai/my-project/main/god-mode-credit/apex/voice-samples/references/apex-miles.wav',
  voice_status = 'cloned',
  updated_at = NOW()
WHERE UPPER(name) = 'APEX';
```

Order: **APEX → ZERO → SOVEREIGN → CERBERUS → AEGIS → MIDAS → CLOSER → HUNTER → KEEPER → BUILDER → VEGA → ELI**

(Start with APEX + ZERO because we can A/B them against the existing ElevenLabs renders — if VoxCPM's Miles clone doesn't match ElevenLabs Miles, we catch it early before the other clones go live.)

### PHASE 5 — Validation (THE CRITICAL GATE)

For each CEO after Phase 4:

- [ ] Render a test line via the voice router:
  ```python
  from voice_router import speak, refresh_registry
  refresh_registry()
  speak(ceo="apex", text="The laws were written for you. You just never read them. Ascend.", out_path="test-apex-voxcpm.wav")
  ```
- [ ] Side-by-side listen: VoxCPM render vs the ElevenLabs original in `voice-samples/apex-sample-miles.mp3`
- [ ] Edwin gives thumbs up or thumbs down
- [ ] Mark `voice_status = 'validated'` in `ceo_brains` on thumbs up
- [ ] On thumbs down: try a different reference clip, or adjust the `VOXCPM_DENOISER` flag, or pick a different voice from the candidate list

**All 12 must pass before Phase 6.**

### PHASE 6 — Rollout to production (existing content pipelines)

- [ ] Update Make.com scenarios that call ElevenLabs → point them at the voice router HTTP wrapper instead
- [ ] Update n8n workflows that call ElevenLabs → same
- [ ] Update Vapi assistants' TTS config where applicable (Vapi has its own TTS, but for non-phone call assets, flip to voice router)
- [ ] Regenerate all 11 GMC VSLs with the new Apex clone → save over `apex/voice-samples/apex-vsl-*-v2.mp3`
- [ ] Mark all CEOs `voice_status = 'live'`

### PHASE 7 — Monitor for 24-48 hours

- [ ] Watch `journalctl -u voxcpm-empire -f` on the VPS for any errors
- [ ] Generate a handful of ad-hoc renders via the voice router to confirm latency is acceptable
- [ ] Spot-check that all CEO assets (emails, TikTok, VSLs) are using the new voice
- [ ] Verify GPU memory is stable, no OOM crashes
- [ ] Verify the VPS hasn't restarted / systemd unit stays healthy

### PHASE 8 — Cancel ElevenLabs (ONLY AFTER PHASE 7 PASSES)

**This is the destructive action. Edwin runs this himself after confirming everything above.**

- [ ] Log into ElevenLabs → Subscription → **Pause** first (not cancel)
- [ ] Wait 24 hours with ElevenLabs paused — verify the empire still runs on VoxCPM alone
- [ ] If all green: go back to ElevenLabs → **Cancel subscription**
- [ ] Update `sovereign_vault.elevenlabs_api_key` → set `is_active = false`
- [ ] Update `apex/voice-config.md` → note ElevenLabs is historical; point all live config at VoxCPM

---

## ROLLBACK PLAN (if something breaks mid-migration)

One SQL statement flips the entire empire back to ElevenLabs:

```sql
UPDATE ceo_brains SET voice_backend = 'elevenlabs' WHERE voice_backend = 'voxcpm';
```

Then call `voice_router.refresh_registry()` in running services (or restart them). Because the router keeps the old ElevenLabs `voice_id`s (Miles for APEX, Tyrese Tate for ZERO, etc) in git history, reverting means pulling the pre-migration `ceo_brains` row back — which the consolidated sync SQL file also has as a fallback.

**If the VPS goes down entirely:**

The voice router's hardcoded fallback in `router.py` will auto-route to **ElevenLabs Miles** when any CEO's backend fails. So VPS outages degrade to "every CEO sounds like Apex temporarily" instead of "every CEO is silent." That's intentional.

---

## COST COMPARISON (post-migration)

| Line item | Before | After |
|---|---|---|
| ElevenLabs Creator | $22/mo | $0 |
| ElevenLabs usage overage | variable | $0 |
| VPS (already paid) | $X/mo | $X/mo (unchanged) |
| Storage for references (Supabase) | $0 | $0 |
| **Marginal TTS cost** | ~$22-50/mo | **$0** |

Savings compound as the content engine scales. At 1000+ VSLs/month we'd blow past the Creator cap and get charged per character on ElevenLabs — VoxCPM is flat $0.

---

## FILES TOUCHED BY THIS MIGRATION

- `services/voxcpm/Dockerfile` — container image
- `services/voxcpm/server.py` — FastAPI HTTP wrapper
- `services/voxcpm/docker-compose.yml` — one-command deploy
- `services/voxcpm/install.sh` — VPS installer script
- `services/voice-router/` — Python package for TTS dispatch
- `docs/CEO-VOICE-MATRIX.md` — personality → voice reference for all 12 CEOs
- `god-mode-credit/apex/voice-config.md` — update after Phase 8 completes
- `god-mode-credit/apex/voxcpm-migration.md` — this file
- `god-mode-credit/apex/scripts/apex_supabase_sync.sql` — schema additions + CEO voice backend seeds
- `sovereign_vault` (Supabase) — new keys: `voxcpm_url`, `voxcpm_api_key`, `vps_host`, `vps_user`, `vps_ssh_key`

---

**Ascend.**
