"""
Hillsborough County, FL — Surplus Funds Source Scraper

Status: NEEDS_VALIDATION
"""
from pathlib import Path


async def download(page, source: dict, download_dir: Path) -> str | None:
    """
    Navigate to Hillsborough County Clerk surplus funds page and download the latest list.

    TODO: Validate actual URL and navigation after visiting:
    https://www.hillsclerk.com
    Look for: "Registry Funds" or "Surplus Funds" section
    """
    raise NotImplementedError(
        "Hillsborough County scraper needs validation. "
        "Visit the clerk website, identify the surplus list page, "
        "and update this scraper with actual navigation steps."
    )
