"""
Outreach Engine

Manages multi-channel outreach sequences for contactable leads.

Trigger: Opportunities with status='contactable'
         Cron for scheduled follow-ups
"""
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from packages.config.config import config
from packages.utils.supabase_client import get_supabase, log_audit
from packages.utils.logger import get_logger
from services.outreach_engine.template_loader import render_template, render_mail_html
from services.outreach_engine.lob_client import send_letter, verify_address
from services.outreach_engine.twilio_client import send_sms, format_phone
from services.outreach_engine.email_client import send_email

logger = get_logger("outreach-engine")

# Outreach sequence definition
SEQUENCE = [
    {"step": 1, "day": 0,  "channel": "mail",  "template": "mail_letter_1",    "auto": True},
    {"step": 2, "day": 5,  "channel": "sms",   "template": "sms_followup_1",   "auto": True},
    {"step": 3, "day": 8,  "channel": "email", "template": "email_followup_1", "auto": True},
    {"step": 4, "day": 12, "channel": "mail",  "template": "mail_letter_2",    "auto": True},
    {"step": 5, "day": 16, "channel": "sms",   "template": "sms_followup_2",   "auto": True},
    {"step": 6, "day": 21, "channel": "phone", "template": "phone_script_1",   "auto": False},
    {"step": 7, "day": 30, "channel": "mail",  "template": "mail_final",       "auto": True},
]


def start_outreach(opp_id: str):
    """Initialize outreach for a contactable opportunity."""
    supabase = get_supabase()

    opp = (supabase.table("opportunities")
           .select("*, claimants(*)")
           .eq("id", opp_id)
           .single()
           .execute()).data

    if not opp or not opp.get("claimants"):
        logger.error(f"Opportunity or claimant not found: {opp_id}")
        return

    claimant = opp["claimants"]

    if claimant.get("do_not_contact"):
        logger.info(f"Claimant is do-not-contact, skipping: {opp_id}")
        return

    # Update status
    supabase.table("opportunities").update({
        "status": "outreach_active",
    }).eq("id", opp_id).execute()

    # Send step 1 (direct mail)
    _send_step(opp, claimant, SEQUENCE[0], supabase)


def process_scheduled():
    """Process all scheduled outreach steps that are due."""
    supabase = get_supabase()

    # Get all outreach_active opportunities
    result = (supabase.table("opportunities")
              .select("*, claimants(*)")
              .eq("status", "outreach_active")
              .execute())

    for opp in (result.data or []):
        claimant = opp.get("claimants")
        if not claimant or claimant.get("do_not_contact"):
            continue

        # Get outreach history
        events = (supabase.table("outreach_events")
                  .select("sequence_step, created_at")
                  .eq("opportunity_id", opp["id"])
                  .eq("direction", "outbound")
                  .order("sequence_step", desc=True)
                  .limit(1)
                  .execute())

        last_step = events.data[0]["sequence_step"] if events.data else 0
        first_event = (supabase.table("outreach_events")
                       .select("created_at")
                       .eq("opportunity_id", opp["id"])
                       .eq("sequence_step", 1)
                       .limit(1)
                       .execute())

        if not first_event.data:
            continue

        outreach_start = datetime.fromisoformat(first_event.data[0]["created_at"].replace("Z", "+00:00"))

        # Find next step
        for step in SEQUENCE:
            if step["step"] <= last_step:
                continue

            due_date = outreach_start + timedelta(days=step["day"])
            if datetime.now(timezone.utc) >= due_date:
                _send_step(opp, claimant, step, supabase)
                break  # One step per run per opportunity

        # Check if sequence complete
        if last_step >= len(SEQUENCE):
            supabase.table("opportunities").update({
                "status": "unresponsive",
            }).eq("id", opp["id"]).execute()


def _send_step(opp: dict, claimant: dict, step: dict, supabase):
    """Execute a single outreach step."""
    channel = step["channel"]
    template_id = step["template"]

    # Check channel availability
    if channel == "sms" and not claimant.get("phone_primary"):
        logger.info(f"No phone for SMS step {step['step']}, skipping")
        return
    if channel == "email" and not claimant.get("email"):
        logger.info(f"No email for step {step['step']}, skipping")
        return
    if channel == "phone" and float(opp.get("surplus_amount", 0)) < config.min_surplus_for_phone:
        logger.info(f"Surplus below phone threshold for step {step['step']}, skipping")
        return

    # Non-automated steps create founder actions
    if not step["auto"]:
        _create_phone_action(opp, claimant, supabase)
        return

    # Send via appropriate channel
    content_preview = ""
    external_id = None

    if channel == "mail":
        external_id = _send_mail(opp, claimant, template_id)
        content_preview = f"Letter sent to {claimant.get('current_address_line1', 'address')}"
    elif channel == "sms":
        external_id = _send_sms(opp, claimant, template_id)
        content_preview = f"SMS to {claimant.get('phone_primary', 'phone')}"
    elif channel == "email":
        external_id = _send_email(opp, claimant, template_id)
        content_preview = f"Email to {claimant.get('email', 'email')}"

    # Log outreach event
    supabase.table("outreach_events").insert({
        "opportunity_id": opp["id"],
        "claimant_id": claimant["id"],
        "channel": channel,
        "direction": "outbound",
        "event_type": "sent",
        "template_id": template_id,
        "content_preview": content_preview[:200],
        "external_id": external_id,
        "sequence_step": step["step"],
    }).execute()

    logger.info(f"Sent step {step['step']} ({channel}) for opportunity {opp['id']}")


def _send_mail(opp: dict, claimant: dict, template_id: str) -> str | None:
    """Send a letter via Lob API."""
    html_content = render_mail_html(template_id, opp, claimant)
    if not html_content:
        logger.error(f"Failed to render mail template: {template_id}")
        return None

    # Parse business address for Lob from_address
    addr = config.business_address or ""
    from_address = {"line1": addr, "city": "", "state": "", "zip": ""}

    to_address = {
        "line1": claimant.get("current_address_line1", ""),
        "line2": claimant.get("current_address_line2", ""),
        "city": claimant.get("current_city", claimant.get("current_address_city", "")),
        "state": claimant.get("current_state", claimant.get("current_address_state", "")),
        "zip": claimant.get("current_zip", claimant.get("current_address_zip", "")),
    }

    # Verify recipient address before sending
    verified = verify_address(to_address)
    if verified:
        to_address = verified
    else:
        logger.warning(f"Address verification failed for {claimant.get('full_name')}, sending anyway")

    letter_id = send_letter(
        to_name=claimant.get("full_name", "Current Resident"),
        to_address=to_address,
        from_name=config.business_name or "Surplus Recovery Services",
        from_address=from_address,
        html_content=html_content,
        description=f"MIDAS {template_id} — {opp.get('county')} {opp.get('case_number', '')}",
    )

    return letter_id


def _send_sms(opp: dict, claimant: dict, template_id: str) -> str | None:
    """Send SMS via Twilio."""
    body = render_template(template_id, opp, claimant)
    if not body:
        logger.error(f"Failed to render SMS template: {template_id}")
        return None

    phone = claimant.get("phone_primary", "")
    if not phone:
        logger.warning(f"No phone number for claimant {claimant.get('id')}")
        return None

    formatted_phone = format_phone(phone)
    return send_sms(to_phone=formatted_phone, body=body)


def _send_email(opp: dict, claimant: dict, template_id: str) -> str | None:
    """Send email via SMTP."""
    content = render_template(template_id, opp, claimant)
    if not content:
        logger.error(f"Failed to render email template: {template_id}")
        return None

    to_email = claimant.get("email", "")
    if not to_email:
        logger.warning(f"No email for claimant {claimant.get('id')}")
        return None

    # Extract subject from template (first line starting with $)
    subject = f"${float(opp.get('surplus_amount', 0)):,.2f} in surplus funds from {opp.get('property_address', 'your property')}"

    # Convert to simple HTML
    import re
    html_lines = []
    for line in content.split("\n"):
        line = line.strip()
        if line.startswith("# ") or line.startswith("## "):
            continue  # Skip markdown headers
        line = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", line)
        if line:
            html_lines.append(f"<p>{line}</p>")
        else:
            html_lines.append("<br>")

    body_html = "\n".join(html_lines)

    return send_email(
        to_email=to_email,
        subject=subject,
        body_html=body_html,
    )


def _create_phone_action(opp: dict, claimant: dict, supabase):
    """Create a founder action for a phone call."""
    supabase.table("notifications").insert({
        "type": "founder_action",
        "priority": "p2_action",
        "title": f"Call {claimant.get('full_name')} — ${opp.get('surplus_amount')} surplus",
        "body": (
            f"High-value lead ready for phone call.\n"
            f"Name: {claimant.get('full_name')}\n"
            f"Phone: {claimant.get('phone_primary')}\n"
            f"Property: {opp.get('property_address')}\n"
            f"Surplus: ${opp.get('surplus_amount')}\n"
            f"County: {opp.get('county')}, {opp.get('state')}"
        ),
        "related_entity_type": "opportunities",
        "related_entity_id": opp["id"],
    }).execute()


def start_new_outreach():
    """Start outreach for all contactable opportunities."""
    supabase = get_supabase()

    result = (supabase.table("opportunities")
              .select("id")
              .eq("status", "contactable")
              .execute())

    for opp in (result.data or []):
        start_outreach(opp["id"])


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--new", action="store_true", help="Start outreach for new contactable leads")
    parser.add_argument("--scheduled", action="store_true", help="Process scheduled follow-ups")
    args = parser.parse_args()

    if args.new:
        start_new_outreach()
    if args.scheduled:
        process_scheduled()
    if not args.new and not args.scheduled:
        start_new_outreach()
        process_scheduled()
