"""
Run the SQL schema against Supabase to create all tables.
Uses the Supabase Management API (via postgrest) to execute SQL.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from packages.config.config import config
from supabase import create_client


def run_setup():
    """Execute setup SQL against Supabase."""
    supabase = create_client(config.supabase_url, config.supabase_key)

    sql_path = Path(__file__).parent / "setup_supabase.sql"
    sql = sql_path.read_text()

    # Split into individual statements and execute
    # Remove comments and empty lines
    statements = []
    current = []
    in_function = False

    for line in sql.split('\n'):
        stripped = line.strip()

        # Track function/trigger blocks (they contain semicolons inside)
        if 'CREATE OR REPLACE FUNCTION' in line or 'CREATE TRIGGER' in line:
            in_function = True

        if stripped.startswith('--') and not in_function:
            continue

        current.append(line)

        if stripped.endswith(';') and not in_function:
            stmt = '\n'.join(current).strip()
            if stmt and stmt != ';':
                statements.append(stmt)
            current = []
        elif in_function and stripped == '$$ LANGUAGE plpgsql;':
            stmt = '\n'.join(current).strip()
            if stmt:
                statements.append(stmt)
            current = []
            in_function = False
        elif in_function and stripped.endswith(';') and 'EXECUTE FUNCTION' in stripped:
            stmt = '\n'.join(current).strip()
            if stmt:
                statements.append(stmt)
            current = []
            in_function = False

    # Handle any remaining content
    if current:
        stmt = '\n'.join(current).strip()
        if stmt and stmt != ';':
            statements.append(stmt)

    print(f"Found {len(statements)} SQL statements to execute")

    success = 0
    errors = 0

    for i, stmt in enumerate(statements):
        # Get first meaningful line for description
        desc = stmt.split('\n')[0][:80]
        try:
            result = supabase.rpc('exec_sql', {'query': stmt}).execute()
            print(f"  [{i+1}/{len(statements)}] OK: {desc}")
            success += 1
        except Exception as e:
            # Try direct postgrest approach
            try:
                supabase.postgrest.session.headers.update({
                    "Content-Type": "application/json",
                    "Prefer": "return=minimal"
                })
                # Use the REST API to run raw SQL isn't directly supported
                # Fall back to reporting the statement for manual execution
                print(f"  [{i+1}/{len(statements)}] NEEDS MANUAL: {desc}")
                print(f"    Error: {str(e)[:100]}")
                errors += 1
            except Exception as e2:
                print(f"  [{i+1}/{len(statements)}] FAIL: {desc}")
                print(f"    Error: {str(e2)[:100]}")
                errors += 1

    print(f"\nDone: {success} succeeded, {errors} need manual execution")

    if errors > 0:
        print("\n" + "="*60)
        print("SOME STATEMENTS NEED MANUAL EXECUTION")
        print("="*60)
        print("Supabase REST API doesn't support raw DDL statements.")
        print("Copy the SQL from scripts/setup_supabase.sql and paste it")
        print("into the Supabase SQL Editor at:")
        print(f"  {config.supabase_url.replace('.supabase.co', '')}")
        print("  → SQL Editor → New Query → Paste → Run")
        print("="*60)


if __name__ == "__main__":
    run_setup()
