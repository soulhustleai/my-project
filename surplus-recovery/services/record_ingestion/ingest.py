"""
Record Ingestion Service

Parses downloaded files (PDF, HTML) into structured raw_records.

Trigger: New raw_downloads entries with status='success'
"""
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from packages.config.config import config
from packages.utils.supabase_client import get_supabase, log_audit
from packages.utils.logger import get_logger
from services.record_ingestion.parsers.pdf_parser import parse_pdf
from packages.shared_types.types import SurplusRecord

logger = get_logger("record-ingestion")


def ingest_download(download_id: str):
    """Process a single raw_download entry."""
    supabase = get_supabase()

    # Get download record
    download = (supabase.table("raw_downloads")
                .select("*, county_sources(*)")
                .eq("id", download_id)
                .single()
                .execute()).data

    if not download:
        logger.error(f"Download not found: {download_id}")
        return

    source = download["county_sources"]
    file_path = download["file_path"]
    data_format = source["data_format"]

    logger.info(f"Ingesting {file_path} (format: {data_format})")

    try:
        if data_format == "pdf":
            records = parse_pdf(file_path, source)
        elif data_format == "html_table":
            from services.record_ingestion.parsers.html_parser import parse_html
            records = parse_html(file_path, source)
        else:
            logger.error(f"Unsupported format: {data_format}")
            return

        logger.info(f"Parsed {len(records)} records from {file_path}")

        # Batch insert raw records (chunks of 100 to avoid payload limits)
        batch = []
        for record in records:
            batch.append({
                "download_id": download_id,
                "source_id": source["id"],
                "raw_data": record.raw_data,
                "case_number": record.case_number,
                "property_address": record.property_address,
                "owner_name": record.owner_name,
                "surplus_amount": float(record.surplus_amount) if record.surplus_amount else None,
                "sale_date": record.sale_date.isoformat() if record.sale_date else None,
                "sale_type": record.sale_type,
                "parse_status": "parsed",
            })
            if len(batch) >= 100:
                supabase.table("raw_records").insert(batch).execute()
                batch = []
        if batch:
            supabase.table("raw_records").insert(batch).execute()

        # Mark download as processed
        supabase.table("raw_downloads").update({
            "download_status": "processed",
            "processed_at": datetime.now(timezone.utc).isoformat(),
        }).eq("id", download_id).execute()

        log_audit(supabase, "raw_downloads", download_id, "processed",
                  "system:record-ingestion",
                  new_value={"records_parsed": len(records)})

    except Exception as e:
        logger.error(f"Ingestion failed for {download_id}: {e}")
        supabase.table("raw_downloads").update({
            "download_status": "failed",
            "error_message": str(e)[:500],
        }).eq("id", download_id).execute()


def ingest_pending():
    """Process all pending downloads."""
    supabase = get_supabase()

    pending = (supabase.table("raw_downloads")
               .select("id")
               .eq("download_status", "success")
               .execute()).data

    logger.info(f"Found {len(pending)} pending downloads")

    for download in pending:
        ingest_download(download["id"])

    logger.info("Ingestion run complete")


if __name__ == "__main__":
    ingest_pending()
