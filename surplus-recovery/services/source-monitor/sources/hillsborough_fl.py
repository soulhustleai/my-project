"""
Hillsborough County, FL — Foreclosure Auction Results Scraper

VALIDATED APPROACH (March 2026):
Hillsborough does NOT publish a simple surplus funds list.
Must request "Statement of Registry Funds" per case, or monitor auctions.

Data Sources:
  - Foreclosure auctions: https://hillsborough.realforeclose.com
  - Clerk website: https://www.hillsclerk.com
  - Circuit Civil: https://www.hillsclerk.com/Court-Services/Circuit-Civil
  - Unclaimed funds: https://www.hillsclerk.com/records-and-reports/unclaimed-funds
  - Case search: HOVER (Hillsborough Online Viewing of Electronic Records)
  - Tax Collector: https://www.hillstaxfl.gov/taxes/tax-certificate/tax-deeds/

Contact: 813-276-8100
Address: 800 E. Twiggs Street, Room 101, Tampa, FL 33602

Status: VALIDATED — URLs confirmed, scraper logic needs implementation
"""
import json
from pathlib import Path
from datetime import datetime


async def download(page, source: dict, download_dir: Path) -> str | None:
    """
    Scrape Hillsborough County foreclosure auction results.

    Strategy:
      1. Navigate to hillsborough.realforeclose.com
      2. View completed auction results
      3. Extract: case number, property address, sale price
      4. Cross-reference via HOVER for surplus amounts

    Note: Auction sales M-F at 10 AM online.
    """
    auction_url = "https://hillsborough.realforeclose.com"

    await page.goto(auction_url, wait_until="networkidle", timeout=30000)

    results = []

    # TODO: Implement scraping after testing live site

    if not results:
        return None

    file_name = f"hillsborough_fl_auctions_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    file_path = download_dir / file_name
    with open(file_path, "w") as f:
        json.dump(results, f, indent=2)

    return str(file_path)


async def download_unclaimed_funds(page, download_dir: Path) -> str | None:
    """
    Check Hillsborough County unclaimed funds page.

    Source: https://www.hillsclerk.com/records-and-reports/unclaimed-funds
    These are outstanding checks and deposits, separate from foreclosure surplus.
    """
    url = "https://www.hillsclerk.com/records-and-reports/unclaimed-funds"
    await page.goto(url, wait_until="networkidle", timeout=30000)

    # TODO: Check if there's a downloadable list here
    return None
