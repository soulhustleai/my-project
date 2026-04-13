"""
Registry — pulls the CEO voice roster from Supabase ceo_brains.

The registry is loaded once at module import and cached for `CACHE_TTL`
seconds. Call `refresh_registry()` to force a reload (useful after
migrations or voice changes).

The Supabase client reads credentials from sovereign_vault via the
service-role key (already in the vault). For local development you can
set `CEO_REGISTRY_JSON` to a path and it will load from there instead.
"""

from __future__ import annotations

import json
import os
import time
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Dict, List, Optional

CACHE_TTL = int(os.environ.get("CEO_REGISTRY_TTL", "300"))


@dataclass
class CEOVoice:
    name: str                                   # "APEX", "ZERO", etc
    business: Optional[str]                     # "GOD MODE CREDIT"
    voice_backend: str                          # "elevenlabs" | "voxcpm" | "vapi_tts"
    voice_id: Optional[str]                     # backend-specific voice identifier
    voice_reference_url: Optional[str] = None   # for VoxCPM cloning references
    voice_status: str = "pending"
    avatar_url: Optional[str] = None

    def to_dict(self) -> Dict:
        return asdict(self)


_CACHE: Dict[str, CEOVoice] = {}
_CACHED_AT: float = 0.0


def _load_from_supabase() -> Dict[str, CEOVoice]:
    """Load the registry via the Supabase REST API using the service role key."""
    try:
        import requests
    except ImportError as e:
        raise RuntimeError(f"voice_router requires `requests`: {e}")

    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_SERVICE_ROLE_KEY") or os.environ.get("SUPABASE_ANON_KEY")
    if not url or not key:
        raise RuntimeError(
            "SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY must be set. "
            "Retrieve them from sovereign_vault at startup."
        )

    resp = requests.get(
        f"{url}/rest/v1/ceo_brains",
        headers={"apikey": key, "Authorization": f"Bearer {key}"},
        params={
            "select": "name,business,voice_backend,voice_id,voice_reference_url,voice_status,avatar_url,active",
            "active": "eq.true",
        },
        timeout=15,
    )
    resp.raise_for_status()
    rows = resp.json()
    return {r["name"].upper(): CEOVoice(**{k: v for k, v in r.items() if k != "active"}) for r in rows}


def _load_from_json_file(path: str) -> Dict[str, CEOVoice]:
    data = json.loads(Path(path).read_text())
    return {r["name"].upper(): CEOVoice(**r) for r in data}


def _load() -> Dict[str, CEOVoice]:
    path = os.environ.get("CEO_REGISTRY_JSON")
    if path:
        return _load_from_json_file(path)
    return _load_from_supabase()


def refresh_registry() -> Dict[str, CEOVoice]:
    global _CACHE, _CACHED_AT
    _CACHE = _load()
    _CACHED_AT = time.time()
    return _CACHE


def get_registry() -> Dict[str, CEOVoice]:
    global _CACHE, _CACHED_AT
    if not _CACHE or (time.time() - _CACHED_AT) > CACHE_TTL:
        refresh_registry()
    return _CACHE


def list_ceos() -> List[CEOVoice]:
    return list(get_registry().values())


def get_ceo(name: str) -> Optional[CEOVoice]:
    return get_registry().get(name.upper())
