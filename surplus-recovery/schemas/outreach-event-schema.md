# Outreach Event Schema

## Purpose

Track every outreach touchpoint across all channels for every lead. Enables sequence management, compliance auditing, and conversion analysis.

---

## Event Types

| Channel | Direction | Event Types |
|---------|-----------|-------------|
| mail | outbound | sent, delivered, returned |
| sms | outbound | sent, delivered, failed |
| sms | inbound | received, opted_out |
| email | outbound | sent, delivered, opened, clicked, bounced |
| email | inbound | replied |
| phone | outbound | called, connected, voicemail, no_answer |
| phone | inbound | received, missed |

---

## Sequence Definition

```python
OUTREACH_SEQUENCE = [
    {"step": 1, "day": 0,  "channel": "mail",  "template": "mail_letter_1",    "auto": True},
    {"step": 2, "day": 5,  "channel": "sms",   "template": "sms_followup_1",   "auto": True},
    {"step": 3, "day": 8,  "channel": "email", "template": "email_followup_1", "auto": True, "requires": "email"},
    {"step": 4, "day": 12, "channel": "mail",  "template": "mail_letter_2",    "auto": True},
    {"step": 5, "day": 16, "channel": "sms",   "template": "sms_followup_2",   "auto": True},
    {"step": 6, "day": 21, "channel": "phone", "template": "phone_script_1",   "auto": False, "min_amount": 10000},
    {"step": 7, "day": 30, "channel": "mail",  "template": "mail_final",       "auto": True},
]
```

### Sequence Rules
- Sequence starts when opportunity status → OUTREACH_ACTIVE
- If claimant responds at any step → pause sequence, move to RESPONDED
- If claimant opts out → stop all outreach, mark DO_NOT_CONTACT
- Phone step only triggers for leads with surplus > $10K
- Phone step creates a founder action (not automated)
- After step 7 with no response → mark UNRESPONSIVE

---

## Compliance Fields

```python
class OutreachComplianceData:
    tcpa_consent: bool               # Did claimant consent to calls/texts?
    opt_out_requested: bool          # Has claimant requested no contact?
    opt_out_at: datetime             # When was opt-out recorded?
    do_not_call_checked: bool        # Was DNC list checked before calling?
    outreach_hours_compliant: bool   # Was outreach sent during legal hours?
    state_specific_disclosures: bool # Were required disclosures included?
```

### Compliance Rules
- SMS: Include opt-out language ("Reply STOP to opt out") in every message
- Phone: No calls before 8 AM or after 9 PM local time
- Mail: Include business address and phone on every letter
- Email: Include unsubscribe link, physical address (CAN-SPAM)
- All channels: Stop immediately on opt-out, log the event

---

## Metrics Derived from Events

| Metric | Query |
|--------|-------|
| Mail delivery rate | delivered / sent (mail) |
| SMS delivery rate | delivered / sent (sms) |
| Email open rate | opened / delivered (email) |
| Response rate | (inbound events) / (outbound sent events) |
| Opt-out rate | opted_out / total contacted |
| Avg touches to response | avg(sequence_step) for RESPONDED leads |
| Channel conversion | responses by channel / sends by channel |
| Cost per outreach | total channel cost / sends |
