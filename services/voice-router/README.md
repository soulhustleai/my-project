# voice-router

> Godfident Empire TTS backend abstraction. **One call, any backend, every CEO.**

Lets any service in the empire generate audio for any CEO without caring whether the voice is coming from ElevenLabs, self-hosted VoxCPM2, or a Vapi assistant. The routing decision lives in Supabase `ceo_brains.voice_backend` — flip it from `elevenlabs` to `voxcpm` in one row and the next call switches backends with no code change.

## Install

```bash
# From the repo root
pip install -e services/voice-router
```

## Usage

```python
from voice_router import speak, speak_bytes, list_ceos, refresh_registry

# One-liner: generate audio for a CEO and save to disk
path = speak(ceo="apex", text="The laws were written for you. You just never read them. Ascend.")
print(f"Audio saved to {path}")

# Or get raw bytes
mp3_bytes = speak_bytes(ceo="zero", text="My staff don't exist.")

# Force a specific backend (bypasses the registry)
speak(ceo="apex", text="...", backend="voxcpm")

# List configured CEOs
for ceo in list_ceos():
    print(ceo.name, ceo.voice_backend, ceo.voice_id, ceo.voice_status)

# After a DB migration, reload
refresh_registry()
```

## Environment

The router pulls secrets from env vars at runtime. Populate these at service
startup from `sovereign_vault`:

| Var | Source in vault | Used by |
|---|---|---|
| `SUPABASE_URL` | `sovereign_vault.supabase_url` | registry loader |
| `SUPABASE_SERVICE_ROLE_KEY` | `sovereign_vault.supabase_service_role_key` | registry loader |
| `ELEVENLABS_API_KEY` | `sovereign_vault.elevenlabs_api_key` | ElevenLabs backend |
| `VOXCPM_URL` | `sovereign_vault.voxcpm_url` | VoxCPM backend |
| `VOXCPM_API_KEY` | `sovereign_vault.voxcpm_api_key` | VoxCPM backend |
| `CEO_REGISTRY_TTL` | (optional, default 300s) | cache lifetime |

### Local dev override

Set `CEO_REGISTRY_JSON=/path/to/registry.json` to skip Supabase and load the
roster from a JSON file. Format:

```json
[
  {"name": "APEX", "business": "GOD MODE CREDIT", "voice_backend": "voxcpm",
   "voice_id": "apex-miles-ref", "voice_reference_url": "...", "voice_status": "live",
   "avatar_url": "..."}
]
```

## Backends

| Backend | Implementation | When used |
|---|---|---|
| `elevenlabs` | `ElevenLabsBackend` — REST API, locked Apex settings (Stability 55 / Clarity 85 / Style 20 / Boost ON) | Fallback + legacy |
| `voxcpm` | `VoxCPMBackend` — HTTP client for self-hosted VoxCPM2 server (see `services/voxcpm`) | Target production backend |
| `vapi_tts` | `VapiTTSBackend` — placeholder; Vapi handles voice internally for phone calls | Phone assistants only |

## Adding a new CEO voice

1. Drop a 3-10 second reference audio clip into `god-mode-credit/apex/voice-samples/references/<ceo>-<voice_name>.wav`
2. Commit + push
3. Upload to the VoxCPM server: `curl -X POST -H "Authorization: Bearer $VOXCPM_API_KEY" -F name=<ceo>-<voice_name> -F file=@<path> $VOXCPM_URL/voices`
4. Update the row:
   ```sql
   UPDATE ceo_brains SET
     voice_backend = 'voxcpm',
     voice_id = '<ceo>-<voice_name>',
     voice_reference_url = 'https://raw.githubusercontent.com/.../references/<ceo>-<voice_name>.wav',
     voice_status = 'live',
     updated_at = NOW()
   WHERE UPPER(name) = 'CEO_NAME';
   ```
5. Call `voice_router.refresh_registry()` in running services (or wait up to `CEO_REGISTRY_TTL` seconds)

## Rollback path

If VoxCPM2 has an outage, every call fails open to ElevenLabs with Miles'
voice via the hardcoded fallback in `router.py`. To force the whole empire
back onto ElevenLabs temporarily:

```sql
UPDATE ceo_brains SET voice_backend = 'elevenlabs' WHERE voice_backend = 'voxcpm';
```

Then `refresh_registry()` in-process or restart the services.

---

**Ascend.**
