"""
Supabase client — single shared instance for all services.
"""
from typing import Optional
from supabase import create_client, Client
from packages.config.config import config

_client: Optional[Client] = None


def get_supabase() -> Client:
    """Get the cached Supabase client instance (singleton)."""
    global _client
    if _client is not None:
        return _client
    if not config.supabase_url or not config.supabase_key:
        raise ValueError("SUPABASE_URL and SUPABASE_SERVICE_KEY must be set")
    _client = create_client(config.supabase_url, config.supabase_key)
    return _client


def log_audit(
    supabase: Client,
    entity_type: str,
    entity_id: str,
    action: str,
    actor: str = "system",
    old_value: Optional[dict] = None,
    new_value: Optional[dict] = None,
):
    """Write an entry to the audit log. Failures are logged, not raised."""
    try:
        supabase.table("audit_log").insert({
            "entity_type": entity_type,
            "entity_id": entity_id,
            "action": action,
            "actor": actor,
            "old_value": old_value,
            "new_value": new_value,
        }).execute()
    except Exception:
        import logging
        logging.getLogger("audit").warning(
            f"Failed to log audit: {entity_type}/{entity_id}/{action}",
            exc_info=True,
        )
