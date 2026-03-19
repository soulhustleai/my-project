# Founder Action Protocol

## Purpose

Define the exact format for every unavoidable founder action. Every escalation must be brain-dead simple, pre-completed as much as possible, and take the minimum possible time.

---

## Standard Format

Every founder escalation MUST use this exact format:

```
═══════════════════════════════════════════
FOUNDER ACTION REQUIRED
═══════════════════════════════════════════

WHY: [One sentence — why this can't be automated]

TIME REQUIRED: [Estimated minutes]

WHAT SYSTEM ALREADY COMPLETED:
- [bullet list of everything the system already did]

WHERE TO GO: [exact URL, app, or location]

EXACT STEPS:
1. [click-by-click instructions]
2. [with exact field names]
3. [and exact values]

EXACT FIELDS/VALUES:
- Field: Value
- Field: Value

EXACT TEXT TO PASTE:
[copy-paste ready text if applicable]

HOW TO VERIFY COMPLETION:
[what the founder should see after completing the action]

WHAT HAPPENS NEXT AUTOMATICALLY:
[what the system will do once this action is done]

═══════════════════════════════════════════
```

---

## Rules

1. **Never say "manual step required" without the full block above**
2. **Pre-complete everything possible** — if 90% of the work can be done before the founder touches it, do it
3. **Reduce decisions to zero** — the founder confirms, not decides
4. **One action per block** — don't bundle multiple actions
5. **Time estimate is mandatory** — founder must know if this is 2 minutes or 20
6. **"What happens next automatically" is mandatory** — founder must know the system resumes

---

## Anticipated Founder Actions

### Category 1: Business Setup (One-Time)

#### FA-001: Register LLC
```
═══════════════════════════════════════════
FOUNDER ACTION REQUIRED
═══════════════════════════════════════════

WHY: LLC registration requires personal identity verification and payment.

TIME REQUIRED: 15-20 minutes

WHAT SYSTEM ALREADY COMPLETED:
- Recommended entity type: Florida LLC (single member)
- Recommended name options: [3 name suggestions]
- Prepared Articles of Organization draft
- Identified filing portal

WHERE TO GO: https://dos.fl.gov/sunbiz/start-business/efile/

EXACT STEPS:
1. Click "File Florida LLC — Articles of Organization"
2. Enter LLC name: [recommended name]
3. Enter registered agent info: [your name + address]
4. Enter member/manager info: [your name]
5. Pay filing fee: $125
6. Save confirmation number

EXACT FIELDS/VALUES:
- LLC Name: [recommended]
- Registered Agent: [Edwin's name]
- Address: [Edwin's address]
- Effective Date: [today's date]
- Annual Report Month: [recommendation]

HOW TO VERIFY COMPLETION:
- You receive a confirmation email from Sunbiz
- Filing number appears on Sunbiz search within 24 hours

WHAT HAPPENS NEXT AUTOMATICALLY:
- System updates business entity info in config
- Outreach templates updated with business name
- Next action: FA-002 (Business bank account)
═══════════════════════════════════════════
```

#### FA-002: Open Business Bank Account
#### FA-003: Get Business Phone Number (or use existing Twilio)
#### FA-004: Set Up Business Email Domain
#### FA-005: Create Simple Website/Landing Page

### Category 2: Recurring Operations

#### FA-010: Review and Approve Claim Packet Before Filing
```
═══════════════════════════════════════════
FOUNDER ACTION REQUIRED
═══════════════════════════════════════════

WHY: Final human review before filing legal claim with county.

TIME REQUIRED: 5-10 minutes

WHAT SYSTEM ALREADY COMPLETED:
- Claim packet generated with all required documents
- All claimant documents collected and verified
- County-specific form filled with case data
- Cover letter drafted
- Packet organized in filing order

WHERE TO GO: Dashboard → Cases → [Case ID] → Documents tab

EXACT STEPS:
1. Open claim packet PDF
2. Verify claimant name matches on all documents
3. Verify case number is correct on all forms
4. Verify surplus amount matches county records
5. Confirm notarization is present where required
6. Click "Approve for Filing"

HOW TO VERIFY COMPLETION:
- Case status changes to "APPROVED_FOR_FILING"
- System shows green checkmark

WHAT HAPPENS NEXT AUTOMATICALLY:
- System prints and mails claim packet via Lob
- Tracking number logged
- Follow-up reminder set for 30 days
- Case status moves to FILED
═══════════════════════════════════════════
```

#### FA-011: Make Phone Call to High-Value Lead
```
═══════════════════════════════════════════
FOUNDER ACTION REQUIRED
═══════════════════════════════════════════

WHY: Leads with >$10K surplus convert better with a personal call.

TIME REQUIRED: 5-15 minutes

WHAT SYSTEM ALREADY COMPLETED:
- Lead qualified and scored (score: [X]/25)
- Contact info verified: [phone number]
- Two mail pieces sent (Day 1 and Day 12)
- One SMS sent (Day 5) — [delivered/read status]
- Call script prepared below
- Case summary prepared

WHERE TO GO: Call [phone number]

CASE SUMMARY:
- Claimant: [Name]
- Property: [Address]
- County: [County], FL
- Surplus: ~$[Amount]
- Case #: [Number]
- Mail sent: [dates]
- SMS response: [none/details]

CALL SCRIPT:
"Hi [First Name], this is [Your Name] with [Business Name].
I sent you a letter recently about surplus funds from the sale
of your property at [short address]. The county is holding
approximately $[amount] that belongs to you. Were you able
to review that letter?

[If yes → proceed with pitch]
[If no → brief summary, offer to resend]
[If skeptical → 'I completely understand. You can verify by
calling the [County] Clerk at [phone]. Would you like that number?']"

HOW TO VERIFY COMPLETION:
- Log call result in dashboard: Connected/Voicemail/No Answer/Interested/Declined

WHAT HAPPENS NEXT AUTOMATICALLY:
- If "Interested" → System sends intake form link via SMS + email
- If "Voicemail" → System schedules callback in 2 days
- If "Declined" → Lead marked as declined, outreach stops
- If "No Answer" → System schedules retry in 3 days
═══════════════════════════════════════════
```

#### FA-012: Submit Claim via County Portal (Manual)
#### FA-013: Deposit and Disburse Recovery Check
#### FA-014: Handle Complex Case Escalation (Attorney Referral)

### Category 3: Periodic Reviews

#### FA-020: Weekly Pipeline Review (10 min)
#### FA-021: Monthly Performance Review (15 min)
#### FA-022: Quarterly Strategy Review (30 min)

---

## Escalation Priority Levels

| Level | Definition | Notification | Max Wait |
|-------|-----------|-------------|----------|
| **P1 — URGENT** | Revenue at risk, legal deadline | SMS + Dashboard alert | Same day |
| **P2 — ACTION** | Normal workflow step needs founder | Dashboard + daily digest | 48 hours |
| **P3 — REVIEW** | Optional review, non-blocking | Weekly digest | 1 week |
| **P4 — INFO** | FYI only, no action needed | Dashboard only | N/A |

---

## Dependency Map

```
docs/founder-action-protocol.md
  ↓ feeds
templates/founder-actions/          (template files for each FA type)
services/notifications/             (escalation triggers and routing)
apps/dashboard/                     (founder action queue UI)
workflows/founder-escalation-flow.md
```
