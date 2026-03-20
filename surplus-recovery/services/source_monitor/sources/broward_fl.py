"""
Broward County, FL — Foreclosure Auction Results Scraper

VALIDATED APPROACH (March 2026):
Broward does NOT publish a simple surplus funds list.
Instead, we monitor foreclosure auction results on realforeclose.com
and cross-reference with clerk case search for surplus amounts.

Data Sources:
  - Foreclosure auctions: https://broward.realforeclose.com
  - Tax deed overbids: https://broward.deedauction.net/reports/total_sales
  - Tax deed historical: https://www.broward.org/RecordsTaxesTreasury/TaxesFees/Pages/Overbid.aspx
  - Case lookup: Broward Clerk online records search
  - Property appraiser: https://web.bcpa.net/BcpaClient/

Status: VALIDATED — URLs confirmed, scraper logic needs implementation
"""
import json
from pathlib import Path
from datetime import datetime


async def download(page, source: dict, download_dir: Path) -> str | None:
    """
    Scrape Broward County foreclosure auction results from realforeclose.com.

    Strategy:
      1. Navigate to broward.realforeclose.com
      2. View completed/past auction results
      3. Extract: case number, property address, sale price, plaintiff bid
      4. Save as JSON for downstream processing

    The surplus calculation happens in normalization:
      surplus = sale_price - judgment_amount (looked up from case)

    Returns:
        Path to saved results file, or None if no new data
    """
    auction_url = "https://broward.realforeclose.com"

    await page.goto(auction_url, wait_until="networkidle", timeout=30000)

    # NOTE: realforeclose.com may require registration to view full results.
    # The site uses dynamic content loading. Steps below are a framework
    # that needs to be tested against the live site.

    # Approach 1: Scrape the auction calendar for completed sales
    # Look for "Auction Results" or calendar showing past dates

    # Approach 2: Use the tax deed overbid reports as a secondary source
    # These are available at broward.deedauction.net

    results = []

    # TODO: Implement actual scraping after testing against live site
    # Expected data per result:
    # {
    #     "case_number": "CACE-XX-XXXXXX",
    #     "property_address": "123 Main St, Fort Lauderdale, FL",
    #     "sale_price": 285000.00,
    #     "plaintiff_bid": 210000.00,  # judgment amount
    #     "sale_date": "2026-03-15",
    #     "status": "sold_to_third_party",  # only these have surplus
    # }

    if not results:
        return None

    # Save results as JSON
    file_name = f"broward_fl_auctions_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    file_path = download_dir / file_name
    with open(file_path, "w") as f:
        json.dump(results, f, indent=2)

    return str(file_path)


async def download_tax_deed_overbids(page, download_dir: Path) -> str | None:
    """
    Download Broward County tax deed overbid results.

    Source: https://broward.deedauction.net/reports/total_sales
    Also: https://www.broward.org/RecordsTaxesTreasury/TaxesFees/Pages/Overbid.aspx
    """
    overbid_url = "https://broward.deedauction.net/reports/total_sales"

    await page.goto(overbid_url, wait_until="networkidle", timeout=30000)

    # TODO: Implement after testing against live site
    # This page shows past tax deed sale results with overbid amounts
    # May require login to download full data
    # Filter by year to get recent results

    return None
