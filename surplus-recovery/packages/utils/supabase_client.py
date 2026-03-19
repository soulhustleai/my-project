"""
Supabase client — single shared instance for all services.
"""
from supabase import create_client, Client
from packages.config.config import config


def get_supabase() -> Client:
    """Get the Supabase client instance."""
    if not config.supabase_url or not config.supabase_key:
        raise ValueError("SUPABASE_URL and SUPABASE_SERVICE_KEY must be set")
    return create_client(config.supabase_url, config.supabase_key)


def log_audit(
    supabase: Client,
    entity_type: str,
    entity_id: str,
    action: str,
    actor: str = "system",
    old_value: dict = None,
    new_value: dict = None,
):
    """Write an entry to the audit log."""
    supabase.table("audit_log").insert({
        "entity_type": entity_type,
        "entity_id": entity_id,
        "action": action,
        "actor": actor,
        "old_value": old_value,
        "new_value": new_value,
    }).execute()
