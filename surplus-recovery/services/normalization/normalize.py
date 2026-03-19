"""
Normalization Service

Deduplicates, validates, and normalizes raw_records into opportunities.

Trigger: After record ingestion completes
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from packages.config.config import config
from packages.utils.supabase_client import get_supabase, log_audit
from packages.utils.logger import get_logger

logger = get_logger("normalization")


def normalize_name(name: str | None) -> str | None:
    """Standardize a person/entity name."""
    if not name:
        return None
    # Remove extra whitespace
    name = re.sub(r'\s+', ' ', name.strip())
    # Title case for person names (not entities)
    if not _is_entity(name):
        name = name.title()
    return name


def normalize_address(address: str | None) -> str | None:
    """Standardize a property address."""
    if not address:
        return None
    address = re.sub(r'\s+', ' ', address.strip())
    # Common abbreviation standardization
    replacements = {
        r'\bSt\b': 'Street', r'\bAve\b': 'Avenue', r'\bBlvd\b': 'Boulevard',
        r'\bDr\b': 'Drive', r'\bLn\b': 'Lane', r'\bCt\b': 'Court',
        r'\bRd\b': 'Road', r'\bPl\b': 'Place', r'\bCir\b': 'Circle',
    }
    for pattern, replacement in replacements.items():
        address = re.sub(pattern, replacement, address, flags=re.IGNORECASE)
    return address.title()


def _is_entity(name: str) -> bool:
    """Check if name is a legal entity rather than a person."""
    entities = ['llc', 'inc', 'corp', 'trust', 'estate', 'bank',
                'association', 'company', 'limited', 'partnership']
    return any(e in name.lower() for e in entities)


def normalize_pending():
    """Process all unprocessed raw_records into opportunities."""
    supabase = get_supabase()

    # Get raw records that haven't been normalized yet
    # (raw records not linked to any opportunity)
    result = supabase.rpc("get_unnormalized_records").execute()

    # Fallback: simple query if RPC not set up
    if not result.data:
        result = (supabase.table("raw_records")
                  .select("*")
                  .eq("parse_status", "parsed")
                  .execute())

    records = result.data or []
    logger.info(f"Normalizing {len(records)} records")

    created = 0
    skipped_dup = 0
    skipped_invalid = 0

    for record in records:
        county = _get_county_state(record, supabase)
        if not county:
            skipped_invalid += 1
            continue

        case_number = record.get("case_number", "").strip()
        surplus_amount = record.get("surplus_amount")

        # Validate
        if not case_number:
            skipped_invalid += 1
            continue
        if not surplus_amount or float(surplus_amount) < config.min_surplus_amount:
            skipped_invalid += 1
            continue

        # Check for duplicate
        county_name = county["county"]
        state_name = county["state"]
        existing = (supabase.table("opportunities")
                    .select("id")
                    .eq("county", county_name)
                    .eq("state", state_name)
                    .eq("case_number", case_number)
                    .execute())

        if existing.data:
            skipped_dup += 1
            continue

        # Create opportunity
        opp = {
            "raw_record_id": record["id"],
            "source_id": record["source_id"],
            "county": county_name,
            "state": state_name,
            "case_number": case_number,
            "property_address": normalize_address(record.get("property_address")),
            "owner_name": normalize_name(record.get("owner_name")),
            "surplus_amount": float(surplus_amount),
            "sale_date": record.get("sale_date"),
            "sale_type": record.get("sale_type", "foreclosure"),
            "status": "new",
        }

        result = supabase.table("opportunities").insert(opp).execute()
        if result.data:
            log_audit(supabase, "opportunities", result.data[0]["id"],
                      "create", "system:normalization", new_value=opp)
            created += 1

    logger.info(f"Normalization complete: {created} created, {skipped_dup} duplicates, {skipped_invalid} invalid")


def _get_county_state(record: dict, supabase) -> dict | None:
    """Get county/state info from the source."""
    source_id = record.get("source_id")
    if not source_id:
        return None
    result = (supabase.table("county_sources")
              .select("county, state")
              .eq("id", source_id)
              .single()
              .execute())
    return result.data


if __name__ == "__main__":
    normalize_pending()
