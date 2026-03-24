"""
Direct PostgreSQL setup — creates all MIDAS tables via database connection.

Usage:
    python scripts/setup_db_direct.py

Requires SUPABASE_DB_URL in .env (find in Supabase → Settings → Database → Connection string → URI)
Example: postgresql://postgres.[ref]:[password]@aws-0-us-east-1.pooler.supabase.com:6543/postgres
"""
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from dotenv import load_dotenv
load_dotenv()


def get_db_url() -> str:
    """Get the direct PostgreSQL connection URL."""
    db_url = os.getenv("SUPABASE_DB_URL", "")
    if not db_url:
        # Try to construct from Supabase URL
        supabase_url = os.getenv("SUPABASE_URL", "")
        if supabase_url:
            # Extract project ref from URL
            ref = supabase_url.replace("https://", "").split(".")[0]
            password = os.getenv("SUPABASE_DB_PASSWORD", "")
            if password:
                db_url = f"postgresql://postgres.{ref}:{password}@aws-0-us-east-1.pooler.supabase.com:6543/postgres"
    return db_url


def setup_tables():
    """Create all tables using the SQL schema file."""
    try:
        import psycopg2
    except ImportError:
        print("psycopg2 not installed. Installing...")
        os.system(f"{sys.executable} -m pip install psycopg2-binary")
        import psycopg2

    db_url = get_db_url()
    if not db_url:
        print("\n❌ SUPABASE_DB_URL not set in .env")
        print("\nTo find it:")
        print("1. Go to your Supabase project dashboard")
        print("2. Settings → Database → Connection string → URI")
        print("3. Copy the URI and add to .env as SUPABASE_DB_URL=...")
        print("\nAlternatively, set SUPABASE_DB_PASSWORD in .env and we'll construct the URL.")
        sys.exit(1)

    # Read the SQL file
    sql_path = Path(__file__).parent / "setup_supabase.sql"
    if not sql_path.exists():
        print(f"❌ SQL file not found: {sql_path}")
        sys.exit(1)

    sql = sql_path.read_text()

    print(f"Connecting to database...")
    try:
        conn = psycopg2.connect(db_url)
        conn.autocommit = True
        cursor = conn.cursor()

        print("Running schema setup...")
        cursor.execute(sql)

        print("\n✅ All 10 tables created successfully!")
        print("Tables: county_sources, raw_downloads, raw_records, claimants,")
        print("        opportunities, outreach_events, cases, documents,")
        print("        notifications, audit_log")

        # Verify tables
        cursor.execute("""
            SELECT table_name FROM information_schema.tables
            WHERE table_schema = 'public'
            AND table_type = 'BASE TABLE'
            ORDER BY table_name;
        """)
        tables = [row[0] for row in cursor.fetchall()]
        print(f"\nVerified {len(tables)} tables in database: {', '.join(tables)}")

        cursor.close()
        conn.close()

    except psycopg2.OperationalError as e:
        print(f"\n❌ Connection failed: {e}")
        print("\nCheck your SUPABASE_DB_URL — make sure the password is correct.")
        sys.exit(1)
    except psycopg2.errors.DuplicateTable:
        print("\n✅ Tables already exist (no changes needed)")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    setup_tables()
