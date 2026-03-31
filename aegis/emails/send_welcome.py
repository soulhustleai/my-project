"""
AEGIS Auto-Response Email — Sends personalized white-glove email instantly after form submission.
Triggered by n8n when a new lead is inserted into aegis_leads.

Personalization:
- First name
- Contact method preference (text vs call)
- Personalized tip based on their situation (who needs coverage, priority)
"""
import json
import os
from urllib.request import Request, urlopen
from urllib.parse import quote

RESEND_API_KEY = os.getenv('RESEND_API_KEY', '')
FROM_EMAIL = 'Adam Andrade <adam@soulhustleai.com>'  # Update when domain email is configured
FALLBACK_FROM = 'Adam Andrade <Deandradehealthadvisor@gmail.com>'

# Personalized tips based on the lead's situation
TIPS = {
    'Just me': "If you're self-employed or between jobs, you may qualify for a Special Enrollment Period. That means you can get covered right now — even outside open enrollment.",
    'Me + spouse': "Couples often save significantly by comparing individual plans vs. employer plans. I'll look at both angles for you.",
    'Me + family': "Family plans can vary by thousands of dollars between carriers. The right plan depends on your kids' ages and your doctors — I'll map it all out.",
    'My child(ren)': "Children's health coverage has some of the best options available, especially through CHIP programs. I'll find what fits your budget.",
    'Low monthly cost': "Many people overpay because they don't know about subsidies they qualify for. I'll check if you're eligible — it could cut your premium in half.",
    'Low deductible': "A lower deductible means less out-of-pocket when you need care. I'll find plans where the math actually works in your favor.",
    'Keep my doctors': "Keeping your doctors is priority one. I'll check which plans include your providers before recommending anything.",
    'Prescription coverage': "Drug coverage varies wildly between plans. I'll make sure your medications are covered at the lowest tier possible.",
    'Best overall': "I'll compare every angle — premium, deductible, network, prescriptions — and show you the plan that gives you the most value.",
}


def build_email_html(lead):
    """Build personalized email HTML from template."""
    template_path = os.path.join(os.path.dirname(__file__), 'welcome-lead.html')

    with open(template_path, 'r') as f:
        html = f.read()

    first_name = lead.get('first_name', 'there')

    # Parse metadata for personalization
    metadata = {}
    try:
        metadata = json.loads(lead.get('metadata', '{}'))
    except:
        pass

    who = metadata.get('who', 'Just me')
    priority = metadata.get('priority', 'Best overall')
    prefer_text = metadata.get('prefer_text', True)

    # Contact method
    contact_method = "I'll send you a text" if prefer_text else "I'll give you a call"

    # Pick the most relevant tip
    tip = TIPS.get(who, TIPS.get(priority, TIPS['Best overall']))

    # Replace placeholders
    html = html.replace('{{FIRST_NAME}}', first_name)
    html = html.replace('{{CONTACT_METHOD}}', contact_method)
    html = html.replace('{{PERSONALIZED_TIP}}', tip)

    return html


def send_welcome_email(lead):
    """Send the personalized welcome email via Resend API."""
    email = lead.get('email', '')
    if not email or '@' not in email:
        print(f'  No valid email for {lead.get("first_name", "?")}')
        return False

    first_name = lead.get('first_name', 'there')
    html = build_email_html(lead)

    # Subject line — personalized and specific
    subject = f"{first_name}, your coverage options are being reviewed"

    # Send via Resend API
    api_key = RESEND_API_KEY
    from_addr = FROM_EMAIL if 'soulhustleai.com' in FROM_EMAIL else FALLBACK_FROM

    if not api_key:
        print(f'  No Resend API key — email NOT sent to {email}')
        print(f'  Subject: {subject}')
        # Fallback: try sending via Gmail SMTP through n8n
        return send_via_gmail_fallback(email, subject, html, first_name)

    payload = json.dumps({
        'from': from_addr,
        'to': [email],
        'subject': subject,
        'html': html,
        'reply_to': 'Deandradehealthadvisor@gmail.com',
    }).encode()

    req = Request('https://api.resend.com/emails', data=payload, headers={
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json',
    })

    try:
        resp = urlopen(req)
        data = json.loads(resp.read().decode())
        print(f'  Email sent to {email}: {data.get("id", "?")}')
        return True
    except Exception as e:
        print(f'  Resend error: {e}')
        return False


def send_via_gmail_fallback(to_email, subject, html, first_name):
    """Fallback: Use SMTP to send through Gmail."""
    import smtplib
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart

    gmail_user = os.getenv('GMAIL_USER', 'soulhustleai@gmail.com')
    gmail_pass = os.getenv('GMAIL_APP_PASSWORD', '')

    if not gmail_pass:
        print(f'  No Gmail app password — cannot send fallback email')
        return False

    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = f'Adam Andrade <{gmail_user}>'
    msg['To'] = to_email
    msg['Reply-To'] = 'Deandradehealthadvisor@gmail.com'

    # Plain text version
    plain = f"Hey {first_name} — I got your info and I'm reviewing your coverage options right now. I'll reach out within a few hours. Can't wait? Call me directly: (407) 561-2878. — Adam Andrade, State Health Advisor"

    msg.attach(MIMEText(plain, 'plain'))
    msg.attach(MIMEText(html, 'html'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(gmail_user, gmail_pass)
        server.send_message(msg)
        server.quit()
        print(f'  Gmail fallback sent to {to_email}')
        return True
    except Exception as e:
        print(f'  Gmail error: {e}')
        return False


# Entry point for n8n or direct call
if __name__ == '__main__':
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == 'test':
        test_lead = {
            'first_name': 'Jessica',
            'email': 'test@example.com',
            'metadata': json.dumps({
                'who': 'Me + family',
                'priority': 'Low monthly cost',
                'prefer_text': True,
            })
        }

        html = build_email_html(test_lead)
        print(f'Email HTML generated: {len(html)} chars')
        print(f'First 200 chars:\n{html[:200]}')

        # Don't actually send in test mode
        print('\nTest mode — email NOT sent. Set RESEND_API_KEY to send.')
    else:
        # Read lead from stdin (for n8n webhook)
        lead_json = sys.stdin.read()
        lead = json.loads(lead_json)
        send_welcome_email(lead)
