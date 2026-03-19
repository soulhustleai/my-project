"""
Twilio client for SMS outreach.
"""
from packages.config.config import config
from packages.utils.logger import get_logger

logger = get_logger("twilio-client")


def send_sms(to_phone: str, body: str) -> str | None:
    """
    Send an SMS via Twilio.

    Args:
        to_phone: Recipient phone number (E.164 format)
        body: Message body (include opt-out language)

    Returns:
        Twilio message SID, or None on failure
    """
    if not all([config.twilio_account_sid, config.twilio_auth_token, config.twilio_phone_number]):
        logger.error("Twilio credentials not configured")
        return None

    from twilio.rest import Client

    try:
        client = Client(config.twilio_account_sid, config.twilio_auth_token)
        message = client.messages.create(
            body=body,
            from_=config.twilio_phone_number,
            to=to_phone,
        )
        logger.info(f"SMS sent: {message.sid}")
        return message.sid
    except Exception as e:
        logger.error(f"Twilio SMS failed: {e}")
        return None


def format_phone(phone: str) -> str:
    """Ensure phone is in E.164 format (+1XXXXXXXXXX)."""
    import re
    digits = re.sub(r'\D', '', phone)
    if len(digits) == 10:
        return f"+1{digits}"
    if len(digits) == 11 and digits.startswith("1"):
        return f"+{digits}"
    return phone  # Return as-is if can't parse
