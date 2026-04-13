#!/usr/bin/env python3
"""
SoulHustleAI — Manually fire enrichment for all pending jobs.

This is the emergency "run it NOW" script. It directly calls each enrichment
API source for every pending enrichment_job and writes results back to Supabase.

Usage:
    pip install supabase httpx python-dotenv
    export SUPABASE_URL=...
    export SUPABASE_SERVICE_KEY=...
    export HUNTER_IO_API_KEY=...
    export APOLLO_API_KEY=...
    export NUMVERIFY_API_KEY=...
    python fire_enrichment.py
"""
import os
import sys
import time
import json
from typing import Any

try:
    from supabase import create_client
    import httpx
except ImportError:
    print("Install deps: pip install supabase httpx")
    sys.exit(1)

SUPABASE_URL = os.environ["SUPABASE_URL"]
SUPABASE_SERVICE_KEY = os.environ["SUPABASE_SERVICE_KEY"]
HUNTER_IO_API_KEY = os.environ.get("HUNTER_IO_API_KEY")
APOLLO_API_KEY = os.environ.get("APOLLO_API_KEY")
NUMVERIFY_API_KEY = os.environ.get("NUMVERIFY_API_KEY")

supa = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)


def enrich_via_hunter(name: str) -> dict[str, Any]:
    """Domain search via hunter.io to find emails associated with a company."""
    if not HUNTER_IO_API_KEY or not name:
        return {}
    domain_guess = name.lower().replace(" ", "").replace("&", "and").replace(",", "")[:30] + ".com"
    url = f"https://api.hunter.io/v2/domain-search?domain={domain_guess}&api_key={HUNTER_IO_API_KEY}"
    try:
        r = httpx.get(url, timeout=15)
        return r.json().get("data", {}) if r.status_code == 200 else {}
    except Exception as e:
        print(f"  hunter error: {e}")
        return {}


def enrich_via_numverify(phone: str) -> dict[str, Any]:
    """Phone number validation + carrier lookup."""
    if not NUMVERIFY_API_KEY or not phone:
        return {}
    clean = "".join(c for c in phone if c.isdigit())
    url = f"http://apilayer.net/api/validate?access_key={NUMVERIFY_API_KEY}&number={clean}&country_code=US"
    try:
        r = httpx.get(url, timeout=15)
        return r.json() if r.status_code == 200 else {}
    except Exception as e:
        print(f"  numverify error: {e}")
        return {}


def enrich_via_apollo(name: str) -> dict[str, Any]:
    """Apollo organization enrichment."""
    if not APOLLO_API_KEY or not name:
        return {}
    url = "https://api.apollo.io/v1/organizations/enrich"
    try:
        r = httpx.get(url, params={"q_organization_name": name}, headers={"X-Api-Key": APOLLO_API_KEY}, timeout=20)
        return r.json().get("organization", {}) if r.status_code == 200 else {}
    except Exception as e:
        print(f"  apollo error: {e}")
        return {}


def process_job(job: dict) -> None:
    job_id = job["id"]
    contact = job.get("enriched_contacts") or {}
    name = contact.get("input_name", "")
    phone = contact.get("input_phone", "")
    contact_id = job["contact_id"]

    print(f"\n▶ {name} ({phone})")

    # Mark running
    supa.table("enrichment_jobs").update({"status": "running", "started_at": "now()"}).eq("id", job_id).execute()

    attempted = []
    succeeded = []
    merged = {}

    # Hunter.io
    attempted.append("hunter_io")
    hunter_data = enrich_via_hunter(name)
    if hunter_data:
        succeeded.append("hunter_io")
        merged["hunter"] = hunter_data
        print(f"  ✓ hunter — {len(hunter_data.get('emails', []))} emails found")

    # Apollo
    attempted.append("apollo")
    apollo_data = enrich_via_apollo(name)
    if apollo_data:
        succeeded.append("apollo")
        merged["apollo"] = apollo_data
        print(f"  ✓ apollo — {apollo_data.get('website_url', 'no web')}")

    # Numverify
    attempted.append("numverify")
    nv_data = enrich_via_numverify(phone)
    if nv_data and nv_data.get("valid"):
        succeeded.append("numverify")
        merged["numverify"] = nv_data
        print(f"  ✓ numverify — {nv_data.get('carrier', 'unknown')} / {nv_data.get('line_type', 'unknown')}")

    # Extract email if found
    discovered_email = None
    if hunter_data and hunter_data.get("emails"):
        discovered_email = hunter_data["emails"][0].get("value")

    # Update enriched_contacts
    update_contact = {
        "enrichment_data": merged,
        "last_enriched_at": "now()",
        "enrichment_count": 1,
        "confidence_score": min(1.0, len(succeeded) / 3.0),
    }
    if discovered_email:
        update_contact["email_primary"] = discovered_email
    supa.table("enriched_contacts").update(update_contact).eq("id", contact_id).execute()

    # Mark job complete
    supa.table("enrichment_jobs").update({
        "status": "completed",
        "sources_attempted": attempted,
        "sources_succeeded": succeeded,
        "completed_at": "now()",
    }).eq("id", job_id).execute()

    # Also update the source lead (if we can find it)
    source_lead_id = (contact.get("enrichment_data") or {}).get("source_lead_id")
    if source_lead_id:
        lead_update = {"status": "enriched", "updated_at": "now()"}
        if discovered_email:
            lead_update["email"] = discovered_email
        supa.table("leads").update(lead_update).eq("id", source_lead_id).execute()
        print(f"  ✓ lead {source_lead_id[:8]} → enriched")

    time.sleep(1.5)  # rate limit


def main():
    print("═══ SHAI ENRICHMENT FIRE ═══")
    result = supa.table("enrichment_jobs").select(
        "id, contact_id, status, enriched_contacts(input_name, input_phone, input_email, enrichment_data)"
    ).eq("status", "pending").order("created_at").limit(50).execute()

    jobs = result.data or []
    print(f"Found {len(jobs)} pending jobs.\n")

    if not jobs:
        print("✓ Queue empty.")
        return

    for i, job in enumerate(jobs, 1):
        print(f"[{i}/{len(jobs)}]", end=" ")
        try:
            process_job(job)
        except Exception as e:
            print(f"  ✗ ERROR: {e}")
            supa.table("enrichment_jobs").update({"status": "failed", "sources_failed": {"error": str(e)}}).eq("id", job["id"]).execute()

    print("\n═══ COMPLETE ═══")


if __name__ == "__main__":
    main()
