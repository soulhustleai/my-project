"""
PDF Parser — extracts structured records from county surplus list PDFs.

Uses pdfplumber for well-structured PDFs.
Falls back to Claude API for messy/scanned PDFs.
"""
import re
from datetime import date
from typing import Optional

from packages.shared_types.types import SurplusRecord
from packages.utils.logger import get_logger

logger = get_logger("pdf-parser")


def parse_pdf(file_path: str, source: dict) -> list[SurplusRecord]:
    """
    Parse a surplus list PDF into structured records.

    Args:
        file_path: Path to the PDF file
        source: county_sources record with parser_config

    Returns:
        List of parsed SurplusRecord objects
    """
    import pdfplumber

    parser_config = source.get("parser_config", {})
    county = source["county"]
    state = source["state"]
    sale_type = "foreclosure" if "foreclosure" in source["source_type"] else "tax_deed"

    records = []

    try:
        with pdfplumber.open(file_path) as pdf:
            for page_num, page in enumerate(pdf.pages):
                tables = page.extract_tables()

                if not tables:
                    # No tables found — try Claude API fallback
                    logger.warning(f"No tables on page {page_num + 1}, trying text extraction")
                    text = page.extract_text()
                    if text:
                        page_records = _parse_text_fallback(text, county, state, sale_type)
                        records.extend(page_records)
                    continue

                for table in tables:
                    if not table or len(table) < 2:
                        continue

                    # Try to identify column mapping from header row
                    header = table[0] if table[0] else []
                    col_map = _identify_columns(header, parser_config)

                    for row in table[1:]:
                        if not row or all(cell is None or str(cell).strip() == "" for cell in row):
                            continue

                        record = _row_to_record(row, col_map, county, state, sale_type)
                        if record:
                            records.append(record)

    except Exception as e:
        logger.error(f"PDF parsing failed: {e}")
        # Try Claude API as ultimate fallback
        records = _claude_parse_fallback(file_path, county, state, sale_type)

    logger.info(f"Parsed {len(records)} records from {file_path}")
    return records


def _identify_columns(header: list, parser_config: dict) -> dict:
    """Map column indices to field names based on header text."""
    col_map = {}
    header_lower = [str(h).lower().strip() if h else "" for h in header]

    # Common column name patterns
    patterns = {
        "case_number": ["case", "case no", "case number", "case #", "docket"],
        "property_address": ["address", "property", "property address", "location"],
        "owner_name": ["name", "defendant", "owner", "party", "former owner"],
        "surplus_amount": ["surplus", "amount", "excess", "overage", "balance", "funds"],
        "sale_date": ["date", "sale date", "auction date"],
    }

    for field, keywords in patterns.items():
        for i, h in enumerate(header_lower):
            if any(kw in h for kw in keywords):
                col_map[field] = i
                break

    return col_map


def _row_to_record(row: list, col_map: dict, county: str, state: str, sale_type: str) -> Optional[SurplusRecord]:
    """Convert a table row to a SurplusRecord."""
    try:
        case_number = _get_cell(row, col_map.get("case_number"))
        property_address = _get_cell(row, col_map.get("property_address"))
        owner_name = _get_cell(row, col_map.get("owner_name"))
        surplus_str = _get_cell(row, col_map.get("surplus_amount"))
        date_str = _get_cell(row, col_map.get("sale_date"))

        surplus_amount = _parse_amount(surplus_str) if surplus_str else 0.0
        sale_date = _parse_date(date_str) if date_str else None

        if not case_number and not owner_name:
            return None

        if surplus_amount <= 0:
            return None

        return SurplusRecord(
            case_number=case_number or "",
            property_address=property_address,
            owner_name=owner_name,
            surplus_amount=surplus_amount,
            sale_date=sale_date,
            sale_type=sale_type,
            county=county,
            state=state,
            raw_data={
                "row": [str(c) for c in row],
                "col_map": col_map,
            },
        )
    except Exception as e:
        logger.warning(f"Failed to parse row: {e}")
        return None


def _get_cell(row: list, index: Optional[int]) -> Optional[str]:
    """Safely get a cell value from a row."""
    if index is None or index >= len(row):
        return None
    val = row[index]
    return str(val).strip() if val else None


def _parse_amount(amount_str: str) -> float:
    """Parse dollar amount string to float."""
    cleaned = re.sub(r"[^\d.]", "", amount_str)
    try:
        return float(cleaned)
    except ValueError:
        return 0.0


def _parse_date(date_str: str) -> Optional[date]:
    """Parse date string to date object."""
    from datetime import datetime
    formats = ["%m/%d/%Y", "%m/%d/%y", "%Y-%m-%d", "%m-%d-%Y"]
    for fmt in formats:
        try:
            return datetime.strptime(date_str.strip(), fmt).date()
        except ValueError:
            continue
    return None


def _parse_text_fallback(text: str, county: str, state: str, sale_type: str) -> list[SurplusRecord]:
    """Attempt to parse free text when no tables are found."""
    # Simple pattern matching for common formats
    # This is a basic fallback — Claude API is better for complex text
    logger.info("Using text fallback parser")
    return []  # Placeholder — implement pattern matching as needed


def _claude_parse_fallback(file_path: str, county: str, state: str, sale_type: str) -> list[SurplusRecord]:
    """Use Claude API to parse a difficult PDF."""
    from packages.config.config import config
    import anthropic

    if not config.anthropic_api_key:
        logger.error("No Anthropic API key — cannot use Claude fallback")
        return []

    logger.info(f"Using Claude API to parse {file_path}")

    client = anthropic.Anthropic(api_key=config.anthropic_api_key)

    # Read PDF as base64 for vision
    import base64
    with open(file_path, "rb") as f:
        pdf_data = base64.standard_b64encode(f.read()).decode("utf-8")

    prompt = f"""Extract all surplus fund records from this PDF document.
For each record, extract:
- case_number
- property_address
- owner_name (defendant/former owner)
- surplus_amount (as a number, no $ sign)
- sale_date (as YYYY-MM-DD)

County: {county}, State: {state}, Sale type: {sale_type}

Return as JSON array of objects. Only include records with a surplus amount > 0.
If you cannot parse the document, return an empty array []."""

    try:
        response = client.messages.create(
            model=config.claude_model_parse,
            max_tokens=4096,
            messages=[{
                "role": "user",
                "content": [
                    {"type": "document", "source": {"type": "base64", "media_type": "application/pdf", "data": pdf_data}},
                    {"type": "text", "text": prompt}
                ]
            }]
        )

        import json
        text = response.content[0].text
        # Extract JSON from response
        json_match = re.search(r'\[.*\]', text, re.DOTALL)
        if json_match:
            parsed = json.loads(json_match.group())
            return [
                SurplusRecord(
                    case_number=r.get("case_number", ""),
                    property_address=r.get("property_address"),
                    owner_name=r.get("owner_name"),
                    surplus_amount=float(r.get("surplus_amount", 0)),
                    sale_date=_parse_date(r["sale_date"]) if r.get("sale_date") else None,
                    sale_type=sale_type,
                    county=county,
                    state=state,
                    raw_data=r,
                )
                for r in parsed
                if float(r.get("surplus_amount", 0)) > 0
            ]
    except Exception as e:
        logger.error(f"Claude parse fallback failed: {e}")

    return []
