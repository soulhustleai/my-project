"""
Opportunity Scoring Engine

Scores all new opportunities using the scoring model.
See schemas/opportunity-scoring-model.md for full specification.

Trigger: After normalization completes
"""
import sys
from datetime import date, datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from packages.config.config import config
from packages.utils.supabase_client import get_supabase, log_audit
from packages.utils.logger import get_logger

logger = get_logger("opportunity-engine")

# County-specific scores (pre-configured)
COUNTY_FILING_EASE = {
    "Broward_FL": 7, "Palm Beach_FL": 7, "Hillsborough_FL": 8,
    "Cuyahoga_OH": 9, "Franklin_OH": 9, "Hamilton_OH": 8,
    "Maricopa_AZ": 8, "Pima_AZ": 7,
}

COUNTY_COMPETITION = {
    "Broward_FL": 4, "Palm Beach_FL": 5, "Hillsborough_FL": 7,
    "Cuyahoga_OH": 8, "Franklin_OH": 9, "Hamilton_OH": 8,
    "Maricopa_AZ": 6, "Pima_AZ": 8,
}


def score_amount(surplus_amount: float) -> float:
    if surplus_amount >= 50000: return 40
    if surplus_amount >= 25000: return 35
    if surplus_amount >= 15000: return 30
    if surplus_amount >= 10000: return 25
    if surplus_amount >= 5000: return 20
    if surplus_amount >= 3000: return 12
    if surplus_amount >= 1000: return 5
    return 0


def score_recency(sale_date: date | None) -> float:
    if not sale_date:
        return 10  # Unknown date — assume moderate
    days_ago = (date.today() - sale_date).days
    if days_ago <= 30: return 20
    if days_ago <= 90: return 18
    if days_ago <= 180: return 15
    if days_ago <= 365: return 10
    if days_ago <= 730: return 5
    return 2


def score_identifiability(owner_name: str | None) -> float:
    if not owner_name:
        return 0
    name = owner_name.strip()
    entities = ['llc', 'inc', 'corp', 'trust', 'estate', 'bank', 'association']
    if any(e in name.lower() for e in entities):
        return 5
    if ' ' in name and len(name.split()) >= 2:
        return 20
    return 8


def score_opportunity(opp: dict) -> float:
    county_key = f"{opp['county']}_{opp['state']}"

    # Parse sale_date string to date object (Supabase returns ISO strings)
    sale_date_raw = opp.get("sale_date")
    sale_date = None
    if sale_date_raw:
        try:
            sale_date = date.fromisoformat(str(sale_date_raw)[:10])
        except (ValueError, TypeError):
            pass

    return (
        score_amount(float(opp.get("surplus_amount", 0)))
        + score_recency(sale_date)
        + score_identifiability(opp.get("owner_name"))
        + COUNTY_FILING_EASE.get(county_key, 5)
        + COUNTY_COMPETITION.get(county_key, 5)
    )


def score_pending():
    """Score all opportunities with status='new' (paginated)."""
    supabase = get_supabase()

    # Paginate to handle >1000 records
    page_size = 1000
    offset = 0
    total_scored = 0

    while True:
        result = (supabase.table("opportunities")
                  .select("*")
                  .eq("status", "new")
                  .range(offset, offset + page_size - 1)
                  .execute())

        opportunities = result.data or []
        if not opportunities:
            break

        logger.info(f"Scoring batch of {len(opportunities)} opportunities (offset {offset})")

        for opp in opportunities:
            try:
                score = score_opportunity(opp)
            except Exception as e:
                logger.warning(f"Scoring failed for {opp.get('id')}: {e}")
                continue

            new_status = "qualified" if score >= config.min_score_to_enrich else "disqualified"

            supabase.table("opportunities").update({
                "score": score,
                "status": new_status,
                "disqualification_reason": "Score below threshold" if new_status == "disqualified" else None,
            }).eq("id", opp["id"]).execute()

            log_audit(supabase, "opportunities", opp["id"],
                      "status_change", "system:opportunity-engine",
                      old_value={"status": "new", "score": None},
                      new_value={"status": new_status, "score": score})
            total_scored += 1

        if len(opportunities) < page_size:
            break
        offset += page_size

    logger.info(f"Scoring complete: {total_scored} opportunities scored")


if __name__ == "__main__":
    score_pending()
