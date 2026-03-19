"""
Broward County, FL — Surplus Funds Source Scraper

IMPORTANT: Source URL and navigation steps need validation.
This is a scaffold — actual selectors must be confirmed against the live site.

Status: NEEDS_VALIDATION
"""
from pathlib import Path
from datetime import datetime


async def download(page, source: dict, download_dir: Path) -> str | None:
    """
    Navigate to Broward County Clerk surplus funds page and download the latest list.

    Args:
        page: Playwright page object
        source: county_sources record
        download_dir: directory to save downloaded files

    Returns:
        Path to downloaded file, or None if no new file found
    """
    source_url = source["source_url"]

    # TODO: Validate actual URL and navigation steps
    # The Broward County Clerk website structure needs to be confirmed.
    # Expected flow:
    #   1. Navigate to clerk website
    #   2. Find "Surplus Funds" or "Registry of Court" section
    #   3. Download the latest surplus funds list PDF
    #
    # Placeholder implementation:

    await page.goto(source_url, wait_until="networkidle", timeout=30000)

    # TODO: Replace with actual navigation steps after site validation
    # Example navigation (MUST BE UPDATED):
    #
    # # Navigate to surplus funds section
    # await page.click('a:text("Court Records")')
    # await page.click('a:text("Surplus Funds")')
    #
    # # Find latest PDF link
    # pdf_link = await page.query_selector('a[href$=".pdf"]')
    # if not pdf_link:
    #     return None
    #
    # # Download the PDF
    # async with page.expect_download() as download_info:
    #     await pdf_link.click()
    # download = await download_info.value
    #
    # file_name = f"broward_fl_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    # file_path = download_dir / file_name
    # await download.save_as(str(file_path))
    # return str(file_path)

    raise NotImplementedError(
        "Broward County scraper needs validation. "
        "Visit the clerk website, identify the surplus list page, "
        "and update this scraper with actual navigation steps."
    )
