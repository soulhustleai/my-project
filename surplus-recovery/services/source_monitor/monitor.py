"""
Source Monitor Service

Checks county surplus list sources for new data.
Downloads files and stores them for ingestion.

Trigger: Cron (every 24 hours) or manual
"""
import asyncio
import hashlib
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from packages.config.config import config
from packages.utils.supabase_client import get_supabase, log_audit
from packages.utils.logger import get_logger

logger = get_logger("source-monitor")

DOWNLOAD_DIR = Path(__file__).parent / "downloads"
DOWNLOAD_DIR.mkdir(exist_ok=True)


async def check_source(source: dict) -> dict | None:
    """
    Check a single county source for new data.
    Returns download info if new data found, None otherwise.
    """
    from playwright.async_api import async_playwright

    source_id = source["id"]
    parser_id = source["parser_id"]
    source_url = source["source_url"]

    logger.info(f"Checking source: {source['county']}, {source['state']} ({parser_id})")

    try:
        # Import source-specific scraper
        scraper = _get_scraper(parser_id)

        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()

            # Source-specific navigation and download
            file_path = await scraper.download(page, source, DOWNLOAD_DIR)

            await browser.close()

        if not file_path or not os.path.exists(file_path):
            logger.warning(f"No file downloaded for {parser_id}")
            return None

        # Check if this file is new (compare hash)
        file_hash = _hash_file(file_path)

        return {
            "source_id": source_id,
            "file_path": str(file_path),
            "file_hash": file_hash,
            "file_size_bytes": os.path.getsize(file_path),
        }

    except Exception as e:
        logger.error(f"Error checking source {parser_id}: {e}")
        raise


def _get_scraper(parser_id: str):
    """Dynamically load source-specific scraper module."""
    scrapers = {
        "broward_fl_foreclosure_pdf": "services.source_monitor.sources.broward_fl",
        "palm_beach_fl_foreclosure_pdf": "services.source_monitor.sources.palm_beach_fl",
        "hillsborough_fl_foreclosure_pdf": "services.source_monitor.sources.hillsborough_fl",
    }
    module_path = scrapers.get(parser_id)
    if not module_path:
        raise ValueError(f"Unknown parser_id: {parser_id}")

    import importlib
    return importlib.import_module(module_path)


def _hash_file(file_path: str) -> str:
    """SHA256 hash of a file."""
    sha256 = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            sha256.update(chunk)
    return sha256.hexdigest()


async def run():
    """Main entry point — check all active sources."""
    supabase = get_supabase()

    # Get all active sources
    result = supabase.table("county_sources").select("*").eq("is_active", True).execute()
    sources = result.data

    if not sources:
        logger.info("No active sources configured")
        return

    logger.info(f"Checking {len(sources)} active sources")

    for source in sources:
        retries = 3
        for attempt in range(retries):
            try:
                download_info = await check_source(source)

                if download_info:
                    # Check if we already have this file (by hash)
                    existing = (supabase.table("raw_downloads")
                                .select("id")
                                .eq("source_id", source["id"])
                                .eq("file_hash", download_info["file_hash"])
                                .execute())

                    if existing.data:
                        logger.info(f"File already processed for {source['parser_id']}")
                    else:
                        # Save download record
                        supabase.table("raw_downloads").insert({
                            **download_info,
                            "download_status": "success",
                        }).execute()
                        logger.info(f"New download saved for {source['parser_id']}")

                # Update source check timestamp
                supabase.table("county_sources").update({
                    "last_checked_at": datetime.now(timezone.utc).isoformat(),
                    "last_success_at": datetime.now(timezone.utc).isoformat(),
                    "consecutive_failures": 0,
                }).eq("id", source["id"]).execute()

                log_audit(supabase, "county_sources", source["id"],
                          "check_succeeded", "system:source-monitor")
                break  # Success — exit retry loop

            except Exception as e:
                logger.error(f"Attempt {attempt + 1}/{retries} failed for {source['county']}: {e}")
                if attempt == retries - 1:
                    # All retries exhausted
                    failures = source.get("consecutive_failures", 0) + 1
                    supabase.table("county_sources").update({
                        "last_checked_at": datetime.now(timezone.utc).isoformat(),
                        "consecutive_failures": failures,
                    }).eq("id", source["id"]).execute()

                    log_audit(supabase, "county_sources", source["id"],
                              "check_failed", "system:source-monitor",
                              new_value={"error": str(e), "consecutive_failures": failures})

                    # Alert if 3+ consecutive failures
                    if failures >= 3:
                        supabase.table("notifications").insert({
                            "type": "alert",
                            "priority": "p2_action",
                            "title": f"Source failing: {source['county']}, {source['state']}",
                            "body": f"Source {source['parser_id']} has failed {failures} consecutive times. Last error: {str(e)[:200]}",
                            "related_entity_type": "county_sources",
                            "related_entity_id": source["id"],
                        }).execute()
                else:
                    await asyncio.sleep(2 ** attempt)  # Exponential backoff

    logger.info("Source monitor run complete")


if __name__ == "__main__":
    asyncio.run(run())
