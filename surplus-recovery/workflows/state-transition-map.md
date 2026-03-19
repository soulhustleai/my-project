# State Transition Map

## Complete State Machine Reference

This is the single source of truth for all valid state transitions across the system.

---

## Opportunity States

```
Valid transitions:
  new              → qualified, disqualified
  qualified        → enriching
  enriching        → contactable, enrichment_failed
  enrichment_failed → enriching (retry), disqualified
  contactable      → outreach_active
  outreach_active  → responded, unresponsive, do_not_contact
  responded        → interested, declined
  interested       → intake_pending
  intake_pending   → signed
  signed           → (record moves to cases table)

Terminal states: disqualified, unresponsive, declined, do_not_contact
```

## Case States

```
Valid transitions:
  signed                → docs_collecting
  docs_collecting       → docs_complete, stalled
  docs_complete         → claim_prep
  claim_prep            → ready_to_file
  ready_to_file         → filed
  filed                 → acknowledged, stalled
  acknowledged          → under_review
  under_review          → approved, denied, stalled
  approved              → disbursement_pending
  disbursement_pending  → disbursed
  disbursed             → fee_collected
  fee_collected         → client_paid
  client_paid           → closed
  denied                → appeal, closed
  appeal                → under_review, closed
  stalled               → escalated
  escalated             → (any active state), closed

Terminal states: closed
```

---

## Transition Validation Function

```python
VALID_OPPORTUNITY_TRANSITIONS = {
    'new': ['qualified', 'disqualified'],
    'qualified': ['enriching'],
    'enriching': ['contactable', 'enrichment_failed'],
    'enrichment_failed': ['enriching', 'disqualified'],
    'contactable': ['outreach_active'],
    'outreach_active': ['responded', 'unresponsive', 'do_not_contact'],
    'responded': ['interested', 'declined'],
    'interested': ['intake_pending'],
    'intake_pending': ['signed'],
}

VALID_CASE_TRANSITIONS = {
    'signed': ['docs_collecting'],
    'docs_collecting': ['docs_complete', 'stalled'],
    'docs_complete': ['claim_prep'],
    'claim_prep': ['ready_to_file'],
    'ready_to_file': ['filed'],
    'filed': ['acknowledged', 'stalled'],
    'acknowledged': ['under_review'],
    'under_review': ['approved', 'denied', 'stalled'],
    'approved': ['disbursement_pending'],
    'disbursement_pending': ['disbursed'],
    'disbursed': ['fee_collected'],
    'fee_collected': ['client_paid'],
    'client_paid': ['closed'],
    'denied': ['appeal', 'closed'],
    'appeal': ['under_review', 'closed'],
    'stalled': ['escalated'],
    'escalated': ['docs_collecting', 'docs_complete', 'claim_prep',
                  'ready_to_file', 'filed', 'acknowledged',
                  'under_review', 'closed'],
}

def validate_transition(entity_type, current_state, new_state):
    transitions = (VALID_OPPORTUNITY_TRANSITIONS if entity_type == 'opportunity'
                   else VALID_CASE_TRANSITIONS)
    valid = transitions.get(current_state, [])
    if new_state not in valid:
        raise ValueError(f"Invalid transition: {current_state} → {new_state}")
    return True
```

---

## Every transition triggers:
1. `audit_log` entry (old_value, new_value, actor, timestamp)
2. `updated_at` timestamp on the entity
3. Relevant downstream workflow (if any)
4. Notification (if priority threshold met)
