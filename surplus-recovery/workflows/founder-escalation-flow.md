# Founder Escalation Flow

## Trigger
Any service determines a founder action is required

## Flow

```
START (escalation event)
  │
  ├─ 1. CLASSIFY PRIORITY
  │   ├─ P1 (URGENT): Revenue at risk, legal deadline, system critical error
  │   ├─ P2 (ACTION): Normal workflow needs founder input
  │   ├─ P3 (REVIEW): Optional review, non-blocking
  │   └─ P4 (INFO): FYI only
  │
  ├─ 2. GENERATE FOUNDER ACTION BLOCK
  │   ├─ Use standard format from founder-action-protocol.md
  │   ├─ Pre-complete everything possible
  │   ├─ Include exact steps, fields, values, text to paste
  │   └─ Estimate time required
  │
  ├─ 3. CREATE NOTIFICATION
  │   ├─ Insert into notifications table
  │   ├─ Link to related entity (opportunity, case, claimant)
  │   └─ Set priority level
  │
  ├─ 4. DELIVER NOTIFICATION
  │   ├─ P1 → SMS immediately + dashboard + email
  │   ├─ P2 → Dashboard + daily digest email
  │   ├─ P3 → Weekly digest email + dashboard
  │   └─ P4 → Dashboard only
  │
  ├─ 5. WAIT FOR FOUNDER ACTION
  │   ├─ Dashboard shows pending actions queue
  │   ├─ Founder completes action → marks as done
  │   └─ System detects completion → resumes workflow
  │
  └─ 6. TIMEOUT HANDLING
      ├─ P1: Re-send after 4 hours if not actioned
      ├─ P2: Re-send after 48 hours
      ├─ P3: Re-send after 7 days
      └─ P4: No follow-up
```

## Common Escalation Triggers

| Source Service | Trigger | Priority | Action Type |
|---------------|---------|----------|-------------|
| outreach-engine | High-value lead needs phone call | P2 | FA-011 |
| document-engine | Claim packet ready for review | P2 | FA-010 |
| submission-engine | Portal submission required | P2 | FA-012 |
| case-tracker | Claim stalled 90+ days | P2 | FA-follow-up-call |
| case-tracker | Funds disbursed | P1 | FA-013 (deposit) |
| source-monitor | 3 consecutive failures | P2 | Check county site |
| record-ingestion | Parse failure spike | P3 | Review format change |
| Any | System critical error | P1 | Investigate |
