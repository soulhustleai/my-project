"""
Create all Supabase tables using the PostgREST HTTP API.
Since Supabase REST doesn't support raw DDL, we'll use the
Supabase Management API / direct postgres connection approach.

Actually, the simplest reliable way: use requests to call
the Supabase SQL endpoint (available via the Dashboard API).
"""
import os
import sys
import requests
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parents[1] / '.env')

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_KEY")


def run_sql(sql: str) -> dict:
    """Execute SQL via Supabase's pg_net/rpc or direct REST."""
    # Use the Supabase REST API's rpc endpoint
    url = f"{SUPABASE_URL}/rest/v1/rpc/exec_sql"
    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/json",
    }
    resp = requests.post(url, json={"query": sql}, headers=headers, timeout=30)
    return resp.status_code, resp.text


def test_connection():
    """Test that we can connect to Supabase."""
    url = f"{SUPABASE_URL}/rest/v1/"
    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
    }
    try:
        resp = requests.get(url, headers=headers, timeout=10)
        print(f"Connection test: HTTP {resp.status_code}")
        if resp.status_code == 200:
            print("Connected to Supabase successfully!")
            return True
        else:
            print(f"Response: {resp.text[:200]}")
            return False
    except Exception as e:
        print(f"Connection failed: {e}")
        return False


def create_tables_via_rest():
    """
    Since Supabase REST API doesn't support DDL directly,
    we'll create tables using the Supabase client library's
    built-in SQL execution... but since that's broken in this env,
    we'll use a workaround: create a postgres function first,
    or just verify the connection works and output instructions.
    """
    print("="*60)
    print("SUPABASE DATABASE SETUP")
    print("="*60)
    print()

    if not SUPABASE_URL or not SUPABASE_KEY:
        print("ERROR: SUPABASE_URL and SUPABASE_SERVICE_KEY not set in .env")
        return False

    print(f"Project URL: {SUPABASE_URL}")
    print(f"API Key: {SUPABASE_KEY[:20]}...")
    print()

    # Test connection
    if not test_connection():
        print("Cannot connect to Supabase. Check your URL and API key.")
        return False

    # Try to check if tables exist by querying them
    tables_to_check = [
        "county_sources", "raw_downloads", "raw_records",
        "claimants", "opportunities", "outreach_events",
        "cases", "documents", "notifications", "audit_log"
    ]

    existing = []
    missing = []

    for table in tables_to_check:
        url = f"{SUPABASE_URL}/rest/v1/{table}?limit=0"
        headers = {
            "apikey": SUPABASE_KEY,
            "Authorization": f"Bearer {SUPABASE_KEY}",
        }
        resp = requests.get(url, headers=headers, timeout=10)
        if resp.status_code == 200:
            existing.append(table)
        else:
            missing.append(table)

    print(f"\nExisting tables: {len(existing)}")
    for t in existing:
        print(f"  ✓ {t}")

    print(f"\nMissing tables: {len(missing)}")
    for t in missing:
        print(f"  ✗ {t}")

    if missing:
        print("\n" + "="*60)
        print("ACTION NEEDED: Create missing tables")
        print("="*60)
        print()
        print("The SQL schema file is ready. To create the tables:")
        print()
        print(f"1. Open your Supabase dashboard:")
        print(f"   https://supabase.com/dashboard/project/{SUPABASE_URL.split('//')[1].split('.')[0]}")
        print()
        print("2. Click 'SQL Editor' in the left sidebar")
        print()
        print("3. Click '+ New Query'")
        print()
        print("4. Copy ALL contents of this file:")
        print(f"   {Path(__file__).parent / 'setup_supabase.sql'}")
        print()
        print("5. Paste into the SQL editor and click 'Run'")
        print()
        print("6. Run this script again to verify all tables were created")
        print("="*60)
        return False
    else:
        print("\n✓ All tables exist! Database is ready.")
        return True


if __name__ == "__main__":
    create_tables_via_rest()
