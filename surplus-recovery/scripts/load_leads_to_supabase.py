"""
Load parsed surplus fund leads into Supabase.
Run this AFTER tables have been created via setup_supabase.sql.

Usage: python scripts/load_leads_to_supabase.py
"""
import json
import os
import sys
import requests
from pathlib import Path
from datetime import datetime

# Load env
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
try:
    from dotenv import load_dotenv
    load_dotenv(Path(__file__).resolve().parents[1] / '.env')
except ImportError:
    pass

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_KEY")
DATA_DIR = Path(__file__).resolve().parents[1] / "data"


def supabase_post(table: str, data: list[dict]) -> tuple[int, str]:
    """Insert rows into a Supabase table via REST API."""
    url = f"{SUPABASE_URL}/rest/v1/{table}"
    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/json",
        "Prefer": "return=minimal",
    }
    resp = requests.post(url, json=data, headers=headers, timeout=30)
    return resp.status_code, resp.text


def supabase_get(table: str, params: dict = None) -> list:
    """Query a Supabase table via REST API."""
    url = f"{SUPABASE_URL}/rest/v1/{table}"
    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
    }
    resp = requests.get(url, headers=headers, params=params or {}, timeout=30)
    if resp.status_code == 200:
        return resp.json()
    return []


def load_leads():
    """Load all parsed leads into the opportunities table."""
    if not SUPABASE_URL or not SUPABASE_KEY:
        print("ERROR: Set SUPABASE_URL and SUPABASE_SERVICE_KEY in .env")
        return

    # Check if tables exist
    status_code, _ = requests.get(
        f"{SUPABASE_URL}/rest/v1/opportunities?limit=0",
        headers={"apikey": SUPABASE_KEY, "Authorization": f"Bearer {SUPABASE_KEY}"},
        timeout=10,
    ).status_code, ""
    # Fix: just check the response
    resp = requests.get(
        f"{SUPABASE_URL}/rest/v1/opportunities?limit=0",
        headers={"apikey": SUPABASE_KEY, "Authorization": f"Bearer {SUPABASE_KEY}"},
        timeout=10,
    )
    if resp.status_code != 200:
        print("ERROR: 'opportunities' table doesn't exist yet.")
        print("Run the SQL from scripts/setup_supabase.sql in Supabase SQL Editor first.")
        return

    # Load leads
    leads_file = DATA_DIR / "all_leads_pipeline.json"
    if not leads_file.exists():
        print("ERROR: No leads file found. Run the scrapers first.")
        return

    leads = json.load(open(leads_file))
    print(f"Loaded {len(leads)} leads from {leads_file.name}")

    # Check existing to avoid duplicates
    existing = supabase_get("opportunities", {"select": "case_number,county,state"})
    existing_keys = {(r["county"], r["state"], r["case_number"]) for r in existing}
    print(f"Already in database: {len(existing_keys)} opportunities")

    new_leads = [l for l in leads if (l["county"], l["state"], l["case_number"]) not in existing_keys]
    print(f"New leads to insert: {len(new_leads)}")

    if not new_leads:
        print("Nothing to insert. All leads already in database.")
        return

    # Also create claimant records for leads with names
    claimants_inserted = 0
    opportunities_inserted = 0
    batch_size = 50

    for i in range(0, len(new_leads), batch_size):
        batch = new_leads[i:i + batch_size]
        rows = []
        for lead in batch:
            # Parse sale_date
            sale_date = None
            if lead.get("sale_date"):
                try:
                    for fmt in ("%m/%d/%Y", "%Y-%m-%d"):
                        try:
                            sale_date = datetime.strptime(lead["sale_date"], fmt).strftime("%Y-%m-%d")
                            break
                        except ValueError:
                            continue
                except Exception:
                    pass

            row = {
                "county": lead["county"],
                "state": lead["state"],
                "case_number": lead["case_number"],
                "owner_name": lead.get("owner_name"),
                "surplus_amount": lead["surplus_amount"],
                "sale_date": sale_date,
                "sale_type": lead.get("sale_type", "tax_deed_overage"),
                "property_address": lead.get("property_address"),
                "status": "new",
            }
            rows.append(row)

        code, text = supabase_post("opportunities", rows)
        if code in (200, 201):
            opportunities_inserted += len(rows)
            print(f"  Inserted batch {i // batch_size + 1}: {len(rows)} opportunities")
        else:
            print(f"  ERROR batch {i // batch_size + 1}: HTTP {code} - {text[:200]}")

    # Insert claimants for leads with name + address
    claimant_batch = []
    for lead in new_leads:
        if lead.get("owner_name") and lead.get("owner_address"):
            parts = lead["owner_address"].split(",")
            claimant = {
                "full_name": lead["owner_name"],
                "current_address_line1": parts[0].strip() if parts else None,
                "current_city": parts[1].strip() if len(parts) > 1 else None,
                "current_state": parts[2].strip().split()[0] if len(parts) > 2 else None,
                "current_zip": parts[2].strip().split()[1] if len(parts) > 2 and len(parts[2].strip().split()) > 1 else None,
            }
            claimant_batch.append(claimant)

    if claimant_batch:
        code, text = supabase_post("claimants", claimant_batch)
        if code in (200, 201):
            claimants_inserted = len(claimant_batch)
            print(f"  Inserted {claimants_inserted} claimants with addresses")
        else:
            print(f"  Claimant insert error: HTTP {code} - {text[:200]}")

    print(f"\nDone: {opportunities_inserted} opportunities, {claimants_inserted} claimants inserted")
    print(f"Total value loaded: ${sum(l['surplus_amount'] for l in new_leads):,.2f}")


if __name__ == "__main__":
    load_leads()
