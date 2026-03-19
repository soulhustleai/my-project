"""
Claimant Enrichment Service

Skip traces qualified opportunities to find claimant contact info.

Trigger: Opportunities with status='qualified' and score >= threshold
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from packages.config.config import config
from packages.utils.supabase_client import get_supabase, log_audit
from packages.utils.logger import get_logger

logger = get_logger("claimant-enrichment")


def enrich_with_pdl(name: str, address: str | None) -> dict | None:
    """
    Look up a person using People Data Labs API.

    Returns dict with: current_address, phone, email, dob, confidence
    """
    if not config.pdl_api_key:
        logger.warning("No PDL API key configured")
        return None

    import requests

    params = {
        "name": name,
        "pretty": True,
    }
    if address:
        params["address_line_1"] = address

    headers = {"X-Api-Key": config.pdl_api_key}

    try:
        resp = requests.get(
            "https://api.peopledatalabs.com/v5/person/enrich",
            params=params,
            headers=headers,
            timeout=15,
        )

        if resp.status_code == 200:
            data = resp.json()
            if data.get("status") == 200 and data.get("data"):
                person = data["data"]
                primary_address = None
                if person.get("street_addresses"):
                    addr = person["street_addresses"][0]
                    primary_address = {
                        "line1": addr.get("street_address"),
                        "city": addr.get("locality"),
                        "state": addr.get("region"),
                        "zip": addr.get("postal_code"),
                    }

                return {
                    "first_name": person.get("first_name"),
                    "last_name": person.get("last_name"),
                    "phone": person.get("mobile_phone") or (person.get("phone_numbers", [None])[0] if person.get("phone_numbers") else None),
                    "email": person.get("work_email") or person.get("personal_emails", [None])[0] if person.get("personal_emails") else None,
                    "address": primary_address,
                    "dob": person.get("birth_date"),
                    "confidence": data.get("likelihood", 0),
                }
        elif resp.status_code == 404:
            return None
        else:
            logger.warning(f"PDL API error: {resp.status_code}")
            return None

    except Exception as e:
        logger.error(f"PDL API request failed: {e}")
        return None


def enrich_opportunity(opp_id: str):
    """Enrich a single opportunity's claimant."""
    supabase = get_supabase()

    opp = (supabase.table("opportunities")
           .select("*")
           .eq("id", opp_id)
           .single()
           .execute()).data

    if not opp:
        logger.error(f"Opportunity not found: {opp_id}")
        return

    owner_name = opp.get("owner_name")
    property_address = opp.get("property_address")

    if not owner_name:
        supabase.table("opportunities").update({
            "status": "enrichment_failed",
        }).eq("id", opp_id).execute()
        return

    # Update status to enriching
    supabase.table("opportunities").update({
        "status": "enriching",
    }).eq("id", opp_id).execute()

    # Try PDL
    result = enrich_with_pdl(owner_name, property_address)

    if result:
        # Create claimant record
        claimant_data = {
            "full_name": owner_name,
            "first_name": result.get("first_name"),
            "last_name": result.get("last_name"),
            "phone_primary": result.get("phone"),
            "email": result.get("email"),
            "date_of_birth": result.get("dob"),
            "former_address": property_address,
            "enrichment_source": "pdl",
            "enrichment_confidence": min(result.get("confidence", 0) / 10, 1.0),
        }

        if result.get("address"):
            addr = result["address"]
            claimant_data.update({
                "current_address_line1": addr.get("line1"),
                "current_city": addr.get("city"),
                "current_state": addr.get("state"),
                "current_zip": addr.get("zip"),
            })

        claimant_result = supabase.table("claimants").insert(claimant_data).execute()
        claimant_id = claimant_result.data[0]["id"]

        # Determine contactability
        has_address = bool(claimant_data.get("current_address_line1"))
        has_phone = bool(claimant_data.get("phone_primary"))
        has_email = bool(claimant_data.get("email"))

        if has_address or has_phone:
            new_status = "contactable"
        else:
            new_status = "enrichment_failed"

        supabase.table("opportunities").update({
            "status": new_status,
            "claimant_id": claimant_id,
        }).eq("id", opp_id).execute()

        log_audit(supabase, "opportunities", opp_id, "status_change",
                  "system:claimant-enrichment",
                  old_value={"status": "enriching"},
                  new_value={"status": new_status, "claimant_id": claimant_id})
    else:
        # Enrichment failed
        supabase.table("opportunities").update({
            "status": "enrichment_failed",
        }).eq("id", opp_id).execute()

        log_audit(supabase, "opportunities", opp_id, "status_change",
                  "system:claimant-enrichment",
                  old_value={"status": "enriching"},
                  new_value={"status": "enrichment_failed"})


def enrich_pending():
    """Enrich all qualified opportunities up to daily limit."""
    supabase = get_supabase()

    result = (supabase.table("opportunities")
              .select("id, score")
              .eq("status", "qualified")
              .order("score", desc=True)
              .limit(config.max_enrichments_per_day)
              .execute())

    opportunities = result.data or []
    logger.info(f"Enriching {len(opportunities)} opportunities")

    for opp in opportunities:
        enrich_opportunity(opp["id"])

    logger.info("Enrichment run complete")


if __name__ == "__main__":
    enrich_pending()
