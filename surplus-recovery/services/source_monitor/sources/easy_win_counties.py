"""
Easy-Win Florida Counties — Published Surplus Fund Lists

These counties publish downloadable surplus/unclaimed fund lists directly.
Much simpler than the big-3 auction-monitoring approach.

RECOMMENDED: Start with these for immediate leads while building
the auction-monitoring pipeline for Broward/Palm Beach/Hillsborough.

Status: URLs validated via web search, scraper logic needs implementation
"""
import json
from pathlib import Path
from datetime import datetime


# Counties with published surplus lists (confirmed URLs)
EASY_WIN_SOURCES = {
    "brevard_fl_tax_deed": {
        "county": "Brevard",
        "state": "FL",
        "url": "https://www.brevardclerk.us/tax-deed-surplus",
        "type": "tax_deed_overage",
        "format": "html_table",
        "notes": "Online list of tax deed surplus. Also has unclaimed funds at /unclaimed-funds",
    },
    "sumter_fl_surplus": {
        "county": "Sumter",
        "state": "FL",
        "url": "https://www.sumterclerk.com/surplus-funds-list",
        "type": "foreclosure_surplus",
        "format": "pdf",
        "notes": "PDF lists of both foreclosure and tax deed surplus",
    },
    "polk_fl_surplus": {
        "county": "Polk",
        "state": "FL",
        "url": "https://www.polkclerkfl.gov/280/Surplus-Funds-List",
        "type": "foreclosure_surplus",
        "format": "html_table",
        "notes": "Published surplus funds list",
    },
    "lee_fl_tax_deed": {
        "county": "Lee",
        "state": "FL",
        "url": "https://www.leeclerk.org/departments/courts/property-sales/tax-deed-sales/tax-deed-reports",
        "type": "tax_deed_overage",
        "format": "pdf",
        "notes": "Tax deed reports including overbids",
    },
    "pasco_fl_tax_deed": {
        "county": "Pasco",
        "state": "FL",
        "url": "https://www.pascoclerk.com/839/Tax-Deed-Surplus",
        "type": "tax_deed_overage",
        "format": "html_table",
        "notes": "Tax deed surplus list published online",
    },
}


async def download_brevard(page, download_dir: Path) -> str | None:
    """Scrape Brevard County tax deed surplus list."""
    url = EASY_WIN_SOURCES["brevard_fl_tax_deed"]["url"]
    await page.goto(url, wait_until="networkidle", timeout=30000)

    # TODO: Extract table data from the page
    # Brevard publishes surplus info directly as an HTML table/list
    # Parse with BeautifulSoup after saving page content

    content = await page.content()
    file_name = f"brevard_fl_surplus_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
    file_path = download_dir / file_name
    with open(file_path, "w") as f:
        f.write(content)

    return str(file_path)


async def download_sumter(page, download_dir: Path) -> str | None:
    """Download Sumter County surplus funds list PDF."""
    url = EASY_WIN_SOURCES["sumter_fl_surplus"]["url"]
    await page.goto(url, wait_until="networkidle", timeout=30000)

    # TODO: Find and download PDF links on the page
    # Sumter publishes both foreclosure and tax deed surplus as PDFs

    return None


async def download_polk(page, download_dir: Path) -> str | None:
    """Scrape Polk County surplus funds list."""
    url = EASY_WIN_SOURCES["polk_fl_surplus"]["url"]
    await page.goto(url, wait_until="networkidle", timeout=30000)

    content = await page.content()
    file_name = f"polk_fl_surplus_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
    file_path = download_dir / file_name
    with open(file_path, "w") as f:
        f.write(content)

    return str(file_path)
