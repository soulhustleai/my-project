"""
Lob API client for sending physical mail.

Lob handles: address verification, printing, mailing, delivery tracking.
"""
from packages.config.config import config
from packages.utils.logger import get_logger

logger = get_logger("lob-client")


def send_letter(
    to_name: str,
    to_address: dict,
    from_name: str,
    from_address: dict,
    html_content: str,
    description: str = "",
) -> str | None:
    """
    Send a letter via Lob API.

    Args:
        to_name: Recipient name
        to_address: dict with line1, city, state, zip
        from_name: Sender name (business)
        from_address: dict with line1, city, state, zip
        html_content: HTML content for the letter
        description: Internal description

    Returns:
        Lob letter ID, or None on failure
    """
    import requests

    if not config.lob_api_key:
        logger.error("No Lob API key configured")
        return None

    api_url = "https://api.lob.com/v1/letters"

    payload = {
        "description": description[:255],
        "to": {
            "name": to_name,
            "address_line1": to_address.get("line1", ""),
            "address_line2": to_address.get("line2", ""),
            "address_city": to_address.get("city", ""),
            "address_state": to_address.get("state", ""),
            "address_zip": to_address.get("zip", ""),
        },
        "from": {
            "name": from_name,
            "address_line1": from_address.get("line1", ""),
            "address_city": from_address.get("city", ""),
            "address_state": from_address.get("state", ""),
            "address_zip": from_address.get("zip", ""),
        },
        "file": html_content,
        "color": False,
        "mail_type": "usps_first_class",
    }

    # Use test key in test mode
    auth = (config.lob_api_key, "")

    try:
        resp = requests.post(api_url, json=payload, auth=auth, timeout=30)
        if resp.status_code in (200, 201):
            data = resp.json()
            letter_id = data.get("id")
            logger.info(f"Letter sent via Lob: {letter_id}")
            return letter_id
        else:
            logger.error(f"Lob API error: {resp.status_code} — {resp.text[:300]}")
            return None
    except Exception as e:
        logger.error(f"Lob API request failed: {e}")
        return None


def verify_address(address: dict) -> dict | None:
    """
    Verify a US address via Lob.

    Returns verified address dict or None if undeliverable.
    """
    import requests

    if not config.lob_api_key:
        return None

    try:
        resp = requests.post(
            "https://api.lob.com/v1/us_verifications",
            json={
                "primary_line": address.get("line1", ""),
                "secondary_line": address.get("line2", ""),
                "city": address.get("city", ""),
                "state": address.get("state", ""),
                "zip_code": address.get("zip", ""),
            },
            auth=(config.lob_api_key, ""),
            timeout=15,
        )
        if resp.status_code == 200:
            data = resp.json()
            if data.get("deliverability") in ("deliverable", "deliverable_missing_unit"):
                return {
                    "line1": data.get("primary_line"),
                    "line2": data.get("secondary_line"),
                    "city": data.get("components", {}).get("city"),
                    "state": data.get("components", {}).get("state"),
                    "zip": data.get("components", {}).get("zip_code"),
                }
        return None
    except Exception as e:
        logger.error(f"Lob address verification failed: {e}")
        return None
