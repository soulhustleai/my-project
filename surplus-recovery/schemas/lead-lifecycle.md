# Lead Lifecycle — State Machine

## Opportunity States

```
┌──────┐     ┌───────────┐     ┌───────────┐     ┌─────────────┐
│ NEW  │────▶│ QUALIFIED │────▶│ ENRICHING │────▶│ CONTACTABLE │
└──────┘     └───────────┘     └───────────┘     └──────┬──────┘
                  │                   │                   │
                  ▼                   ▼                   ▼
            DISQUALIFIED      ENRICHMENT_FAILED    ┌───────────────┐
                                                   │OUTREACH_ACTIVE│
                                                   └──────┬────────┘
                                                          │
                                    ┌─────────────────────┼──────────────┐
                                    ▼                     ▼              ▼
                              RESPONDED              UNRESPONSIVE   DO_NOT_CONTACT
                                    │
                              ┌─────┼─────┐
                              ▼           ▼
                         INTERESTED    DECLINED
                              │
                              ▼
                        INTAKE_PENDING
                              │
                              ▼
                           SIGNED ──────────▶ (moves to cases table)
```

## Transitions

| From | To | Trigger | Automated? |
|------|----|---------|-----------|
| NEW | QUALIFIED | Score > threshold, amount > $1,000 | Yes |
| NEW | DISQUALIFIED | Score below threshold or amount < $1,000 | Yes |
| QUALIFIED | ENRICHING | Enrichment job started | Yes |
| ENRICHING | CONTACTABLE | Contact info found | Yes |
| ENRICHING | ENRICHMENT_FAILED | No contact info after all providers | Yes |
| CONTACTABLE | OUTREACH_ACTIVE | First outreach sent | Yes |
| OUTREACH_ACTIVE | RESPONDED | Claimant replied (any channel) | Yes (detection) |
| OUTREACH_ACTIVE | UNRESPONSIVE | 30 days, all touches complete, no response | Yes |
| OUTREACH_ACTIVE | DO_NOT_CONTACT | Claimant requests no contact | Yes |
| RESPONDED | INTERESTED | Claimant expresses interest | Manual classification |
| RESPONDED | DECLINED | Claimant declines | Manual classification |
| INTERESTED | INTAKE_PENDING | Intake form sent | Yes |
| INTAKE_PENDING | SIGNED | Agreement signed + intake complete | Yes (form submission) |

---

## Case States (Post-Signing)

```
SIGNED → DOCS_COLLECTING → DOCS_COMPLETE → CLAIM_PREP →
  → READY_TO_FILE → FILED → ACKNOWLEDGED → UNDER_REVIEW →
  → APPROVED → DISBURSEMENT_PENDING → DISBURSED →
  → FEE_COLLECTED → CLIENT_PAID → CLOSED

Side states:
  DENIED → APPEAL → (re-enters UNDER_REVIEW or CLOSED)
  STALLED → ESCALATED → (re-enters tracking or CLOSED)
```

| From | To | Trigger | Automated? |
|------|----|---------|-----------|
| SIGNED | DOCS_COLLECTING | Case created, docs needed | Yes |
| DOCS_COLLECTING | DOCS_COMPLETE | All required docs received | Yes (checklist) |
| DOCS_COMPLETE | CLAIM_PREP | Doc generation starts | Yes |
| CLAIM_PREP | READY_TO_FILE | Claim packet generated | Yes |
| READY_TO_FILE | FILED | Founder approves, packet mailed | Founder review → auto-mail |
| FILED | ACKNOWLEDGED | County confirms receipt | Manual (check portal/mail) |
| ACKNOWLEDGED | UNDER_REVIEW | Standard progression | Manual |
| UNDER_REVIEW | APPROVED | County approves claim | Manual (check portal/mail) |
| APPROVED | DISBURSEMENT_PENDING | Waiting for check/wire | Manual |
| DISBURSEMENT_PENDING | DISBURSED | Funds received | Founder confirms |
| DISBURSED | FEE_COLLECTED | Fee deducted | Founder action |
| FEE_COLLECTED | CLIENT_PAID | Client portion sent | Founder action |
| CLIENT_PAID | CLOSED | Case complete | Yes |
| UNDER_REVIEW | DENIED | Claim denied | Manual |
| DENIED | APPEAL | Founder decides to appeal | Founder decision |
| Any | STALLED | No status change in 90 days | Yes (automated detection) |
| STALLED | ESCALATED | Founder investigates | Founder action |

---

## State Change Rules

1. Every state change is logged in `audit_log`
2. State can only move forward or to a terminal state (no backwards)
3. Exception: DENIED → APPEAL allows re-entry to UNDER_REVIEW
4. Exception: STALLED → ESCALATED can re-enter any active state
5. Terminal states: CLOSED, DISQUALIFIED, UNRESPONSIVE, DECLINED, DO_NOT_CONTACT
