"""
Seed County Sources

Populates the county_sources table with initial Florida county configurations.
Run after setup_supabase.sql.

Usage: python scripts/seed_sources.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from packages.utils.supabase_client import get_supabase
from packages.utils.logger import get_logger

logger = get_logger("seed-sources")

INITIAL_SOURCES = [
    {
        "county": "Broward",
        "state": "FL",
        "source_type": "foreclosure_surplus",
        "source_url": "https://www.browardclerk.org",  # NEEDS VALIDATION
        "data_format": "pdf",
        "parser_id": "broward_fl_foreclosure_pdf",
        "check_frequency_hours": 24,
        "is_active": False,  # Disabled until scraper is validated
        "scraper_config": {
            "notes": "Navigate to surplus/registry funds page, download latest PDF"
        },
        "parser_config": {
            "expected_columns": ["case_number", "property_address", "defendant_name", "surplus_amount", "sale_date"],
        },
        "notes": "NEEDS VALIDATION — confirm URL, navigation, and PDF format",
    },
    {
        "county": "Palm Beach",
        "state": "FL",
        "source_type": "foreclosure_surplus",
        "source_url": "https://www.mypalmbeachclerk.com",  # NEEDS VALIDATION
        "data_format": "pdf",
        "parser_id": "palm_beach_fl_foreclosure_pdf",
        "check_frequency_hours": 24,
        "is_active": False,
        "scraper_config": {
            "notes": "Navigate to surplus/registry funds page"
        },
        "parser_config": {
            "expected_columns": ["case_number", "property_address", "defendant_name", "surplus_amount"],
        },
        "notes": "NEEDS VALIDATION",
    },
    {
        "county": "Hillsborough",
        "state": "FL",
        "source_type": "foreclosure_surplus",
        "source_url": "https://www.hillsclerk.com",  # NEEDS VALIDATION
        "data_format": "pdf",
        "parser_id": "hillsborough_fl_foreclosure_pdf",
        "check_frequency_hours": 24,
        "is_active": False,
        "scraper_config": {
            "notes": "Navigate to registry funds page"
        },
        "parser_config": {
            "expected_columns": ["case_number", "defendant_name", "surplus_amount", "sale_date"],
        },
        "notes": "NEEDS VALIDATION",
    },
]


def seed():
    supabase = get_supabase()

    for source in INITIAL_SOURCES:
        # Check if already exists
        existing = (supabase.table("county_sources")
                    .select("id")
                    .eq("county", source["county"])
                    .eq("state", source["state"])
                    .eq("source_type", source["source_type"])
                    .execute())

        if existing.data:
            logger.info(f"Source already exists: {source['county']}, {source['state']}")
            continue

        supabase.table("county_sources").insert(source).execute()
        logger.info(f"Seeded source: {source['county']}, {source['state']} ({source['source_type']})")

    logger.info("Seeding complete")


if __name__ == "__main__":
    seed()
