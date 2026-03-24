"""
Email client for outreach.

Uses SMTP for sending emails. Supports SendGrid, Gmail, or any SMTP provider.
Falls back to logging if not configured.
"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from packages.config.config import config
from packages.utils.logger import get_logger

logger = get_logger("email-client")


def send_email(to_email: str, subject: str, body_html: str, body_text: str = "") -> str | None:
    """
    Send an email via SMTP.

    Args:
        to_email: Recipient email address
        subject: Email subject line
        body_html: HTML body content
        body_text: Plain text fallback (auto-generated from HTML if empty)

    Returns:
        Message ID string, or None on failure
    """
    smtp_host = config.smtp_host
    smtp_port = config.smtp_port
    smtp_user = config.smtp_user
    smtp_pass = config.smtp_pass
    from_email = config.business_email

    if not all([smtp_host, smtp_user, smtp_pass, from_email]):
        logger.error("SMTP not configured — cannot send email")
        return None

    if not body_text:
        # Strip HTML tags for plain text fallback
        import re
        body_text = re.sub(r"<[^>]+>", "", body_html)
        body_text = re.sub(r"\n\s*\n", "\n\n", body_text).strip()

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = f"{config.business_name} <{from_email}>"
    msg["To"] = to_email
    msg["Reply-To"] = from_email

    msg.attach(MIMEText(body_text, "plain"))
    msg.attach(MIMEText(body_html, "html"))

    try:
        if smtp_port == 465:
            server = smtplib.SMTP_SSL(smtp_host, smtp_port, timeout=30)
        else:
            server = smtplib.SMTP(smtp_host, smtp_port, timeout=30)
            server.starttls()

        server.login(smtp_user, smtp_pass)
        result = server.send_message(msg)
        server.quit()

        message_id = msg.get("Message-ID", "sent")
        logger.info(f"Email sent to {to_email}: {message_id}")
        return message_id

    except Exception as e:
        logger.error(f"Email send failed: {e}")
        return None
