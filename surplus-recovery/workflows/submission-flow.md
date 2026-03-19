# Submission Flow

## Trigger
Case status = 'ready_to_file' AND founder has approved

## Flow

```
START (approved claim packet)
  │
  ├─ 1. DETERMINE SUBMISSION METHOD
  │   ├─ Check county filing template:
  │   │   ├─ 'mail' → automated via Lob
  │   │   ├─ 'portal' → founder action (manual upload)
  │   │   └─ 'in_person' → founder action (physical delivery)
  │   └─ Route accordingly
  │
  ├─ 2A. MAIL SUBMISSION (Automated)
  │   ├─ Send claim packet via Lob:
  │   │   ├─ Multi-page document print + mail
  │   │   ├─ Certified mail with return receipt (recommended)
  │   │   └─ Track delivery via Lob webhook
  │   ├─ On success:
  │   │   ├─ Update case status → 'filed'
  │   │   ├─ Record claim_filed_at timestamp
  │   │   ├─ Record tracking number
  │   │   └─ Set follow-up reminder (30 days)
  │   └─ On failure:
  │       ├─ Retry once
  │       └─ If still fails → escalate to founder (manual mail)
  │
  ├─ 2B. PORTAL SUBMISSION (Founder Action)
  │   ├─ Create FOUNDER ACTION: FA-012
  │   │   ├─ Portal URL
  │   │   ├─ Login credentials (if applicable)
  │   │   ├─ Step-by-step upload instructions
  │   │   ├─ Files to upload (linked from documents table)
  │   │   └─ Confirmation screenshot request
  │   ├─ Founder completes → marks action done
  │   └─ System updates case status → 'filed'
  │
  ├─ 2C. IN-PERSON SUBMISSION (Founder Action)
  │   ├─ Create FOUNDER ACTION with:
  │   │   ├─ Courthouse/office address
  │   │   ├─ Hours of operation
  │   │   ├─ What to bring (printed packet)
  │   │   ├─ Who to ask for
  │   │   └─ What to get as confirmation (stamped copy, receipt)
  │   ├─ Founder completes → marks action done
  │   └─ System updates case status → 'filed'
  │
  └─ 3. POST-SUBMISSION
      ├─ Send confirmation to claimant:
      │   ├─ SMS: "Your claim has been filed with [County]. We'll keep you updated."
      │   └─ Email: Same message with tracking details
      ├─ Schedule case tracking check (30 days)
      ├─ Log in audit_log
      └─ Update pipeline dashboard
```

## Cost Per Submission (Mail via Lob)
- Multi-page print + certified mail: ~$5-10 per packet
- Return receipt: ~$3 additional
- Total: ~$8-13 per submission
