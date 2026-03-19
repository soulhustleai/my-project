"""
Palm Beach County, FL — Surplus Funds Source Scraper

Status: NEEDS_VALIDATION
"""
from pathlib import Path


async def download(page, source: dict, download_dir: Path) -> str | None:
    """
    Navigate to Palm Beach County Clerk surplus funds page and download the latest list.

    TODO: Validate actual URL and navigation after visiting:
    https://www.mypalmbeachclerk.com
    Look for: "Registry of Court" or "Surplus Funds" section
    """
    raise NotImplementedError(
        "Palm Beach County scraper needs validation. "
        "Visit the clerk website, identify the surplus list page, "
        "and update this scraper with actual navigation steps."
    )
