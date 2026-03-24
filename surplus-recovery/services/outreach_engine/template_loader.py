"""
Template loader — loads outreach templates and substitutes merge fields.
"""
import re
from pathlib import Path
from packages.config.config import config
from packages.utils.logger import get_logger

logger = get_logger("template-loader")

TEMPLATE_DIR = Path(__file__).resolve().parents[2] / "templates" / "outreach"

# County clerk phone numbers for verification
CLERK_PHONES = {
    "Broward": "(954) 831-6565",
    "Palm Beach": "(561) 355-2996",
    "Hillsborough": "(813) 276-8100",
    "Brevard": "(321) 637-5413",
    "Sumter": "(352) 569-6600",
}


def load_template(template_id: str) -> str:
    """Load a template file by ID and return its content."""
    # Try common extensions
    for ext in [".md", ".txt", ".html"]:
        path = TEMPLATE_DIR / f"{template_id}{ext}"
        if path.exists():
            content = path.read_text()
            # For markdown mail templates, extract just the letter content (after "## Letter Content")
            if ext == ".md" and "## Letter Content" in content:
                content = content.split("## Letter Content\n", 1)[1].strip()
            elif ext == ".md" and "## Body" in content:
                content = content.split("## Body\n", 1)[1].strip()
            return content

    logger.error(f"Template not found: {template_id}")
    return ""


def merge_fields(template: str, opp: dict, claimant: dict) -> str:
    """Replace all {{field}} merge tags with actual values."""
    # Build the merge dictionary
    full_name = claimant.get("full_name", "")
    first_name = full_name.split()[0] if full_name else "Homeowner"

    # Build full address string (handle both column naming conventions)
    addr_parts = [
        claimant.get("current_address_line1", ""),
        claimant.get("current_city", claimant.get("current_address_city", "")),
        claimant.get("current_state", claimant.get("current_address_state", "")),
        claimant.get("current_zip", claimant.get("current_address_zip", "")),
    ]
    claimant_address = ", ".join(p for p in addr_parts if p)

    # Short property address (just street)
    property_address = opp.get("property_address", "your former property")
    property_short = property_address.split(",")[0] if property_address else "your former property"

    county = opp.get("county", "")

    fields = {
        "claimant_name": full_name,
        "claimant_first_name": first_name,
        "claimant_address": claimant_address,
        "property_address": property_address,
        "property_short_address": property_short,
        "county": county,
        "state": opp.get("state", "FL"),
        "case_number": opp.get("case_number", ""),
        "surplus_amount": f"{float(opp.get('surplus_amount', 0)):,.2f}",
        "clerk_phone": CLERK_PHONES.get(county, "(see county website)"),
        "date": __import__("datetime").date.today().strftime("%B %d, %Y"),
        "business_name": config.business_name or "Surplus Recovery Services",
        "business_phone": config.business_phone,
        "business_email": config.business_email,
        "business_website": config.business_website,
        "business_address": config.business_address,
        "sender_name": config.business_name or "Surplus Recovery Services",
    }

    result = template
    for key, value in fields.items():
        result = result.replace("{{" + key + "}}", str(value))

    # Warn about any unresolved merge fields
    unresolved = re.findall(r"\{\{(\w+)\}\}", result)
    if unresolved:
        logger.warning(f"Unresolved merge fields: {unresolved}")

    return result


def render_template(template_id: str, opp: dict, claimant: dict) -> str:
    """Load a template and apply merge fields. Returns ready-to-send content."""
    raw = load_template(template_id)
    if not raw:
        return ""
    return merge_fields(raw, opp, claimant)


def render_mail_html(template_id: str, opp: dict, claimant: dict) -> str:
    """Render a mail template as HTML suitable for Lob API."""
    content = render_template(template_id, opp, claimant)
    if not content:
        return ""

    # Convert markdown-style content to simple HTML for Lob
    lines = content.split("\n")
    html_lines = []
    for line in lines:
        line = line.strip()
        if not line:
            html_lines.append("<br>")
            continue
        # Bold
        line = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", line)
        # List items
        if line.startswith("- "):
            line = f"<li>{line[2:]}</li>"
        html_lines.append(f"<p>{line}</p>")

    body = "\n".join(html_lines)

    return f"""<html>
<head>
<meta charset="UTF-8">
<style>
body {{ font-family: Georgia, serif; font-size: 12pt; line-height: 1.6; color: #1a1a1a; margin: 1in; }}
p {{ margin: 0 0 6pt 0; }}
strong {{ font-weight: bold; }}
li {{ margin-left: 20px; }}
</style>
</head>
<body>
{body}
</body>
</html>"""
