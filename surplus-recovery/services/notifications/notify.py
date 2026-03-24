"""
Notifications Service

Sends alerts to the founder via SMS and email when critical events occur.
Reads from the notifications table and sends via configured channels.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from packages.config.config import config
from packages.utils.supabase_client import get_supabase
from packages.utils.logger import get_logger
from services.outreach_engine.twilio_client import send_sms
from services.outreach_engine.email_client import send_email

logger = get_logger("notifications")

# Priority → notification channels
PRIORITY_CHANNELS = {
    "p1_urgent": ["sms", "email"],
    "p2_action": ["sms", "email"],
    "p3_review": ["email"],
    "p4_info": [],  # In-app only
}


def send_pending_notifications():
    """Process and send all unread notifications."""
    supabase = get_supabase()

    notifications = (supabase.table("notifications")
                     .select("*")
                     .eq("is_read", False)
                     .order("created_at", desc=False)
                     .limit(50)
                     .execute()).data or []

    if not notifications:
        logger.info("No pending notifications")
        return

    logger.info(f"Processing {len(notifications)} notifications")

    for notif in notifications:
        channels = PRIORITY_CHANNELS.get(notif["priority"], [])
        sent_via = []

        if "sms" in channels and config.business_phone:
            body = f"[MIDAS {notif['priority'].upper()}]\n{notif['title']}\n\n{notif['body'][:300]}"
            result = send_sms(to_phone=config.business_phone, body=body)
            if result:
                sent_via.append("sms")

        if "email" in channels and config.business_email:
            subject = f"[MIDAS] {notif['title']}"
            body_html = f"<h2>{notif['title']}</h2><p>{notif['body'].replace(chr(10), '<br>')}</p>"
            result = send_email(
                to_email=config.business_email,
                subject=subject,
                body_html=body_html,
            )
            if result:
                sent_via.append("email")

        # Mark as read and record sent channels
        supabase.table("notifications").update({
            "is_read": True,
            "sent_via": sent_via,
        }).eq("id", notif["id"]).execute()

        logger.info(f"Notification {notif['id']} sent via: {sent_via or ['in-app only']}")


def create_notification(
    title: str,
    body: str,
    priority: str = "p3_review",
    notif_type: str = "info",
    entity_type: str = None,
    entity_id: str = None,
):
    """Create a notification and optionally send immediately."""
    supabase = get_supabase()

    notif = supabase.table("notifications").insert({
        "type": notif_type,
        "priority": priority,
        "title": title,
        "body": body,
        "related_entity_type": entity_type,
        "related_entity_id": entity_id,
    }).execute()

    # P1 notifications get sent immediately
    if priority == "p1_urgent":
        send_pending_notifications()

    return notif.data


if __name__ == "__main__":
    send_pending_notifications()
