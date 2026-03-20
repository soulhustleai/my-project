"""
HTML Parser — extracts structured records from HTML table pages.

Used when county sources publish surplus data as HTML tables.
"""
from packages.shared_types.types import SurplusRecord
from packages.utils.logger import get_logger

logger = get_logger("html-parser")


def parse_html(file_path: str, source: dict) -> list[SurplusRecord]:
    """
    Parse an HTML file containing surplus list data.

    Args:
        file_path: Path to saved HTML file
        source: county_sources record

    Returns:
        List of SurplusRecord objects
    """
    from bs4 import BeautifulSoup

    county = source["county"]
    state = source["state"]
    sale_type = "foreclosure" if "foreclosure" in source["source_type"] else "tax_deed"

    with open(file_path, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f.read(), "html.parser")

    records = []
    tables = soup.find_all("table")

    for table in tables:
        rows = table.find_all("tr")
        if len(rows) < 2:
            continue

        # Extract header
        header_cells = rows[0].find_all(["th", "td"])
        header = [cell.get_text(strip=True).lower() for cell in header_cells]

        # Map columns (reuse logic from pdf_parser)
        from services.record_ingestion.parsers.pdf_parser import (
            _identify_columns, _row_to_record
        )
        col_map = _identify_columns(header, source.get("parser_config", {}))

        # Extract data rows
        for row in rows[1:]:
            cells = row.find_all("td")
            cell_values = [cell.get_text(strip=True) for cell in cells]

            record = _row_to_record(cell_values, col_map, county, state, sale_type)
            if record:
                records.append(record)

    logger.info(f"Parsed {len(records)} records from HTML")
    return records
