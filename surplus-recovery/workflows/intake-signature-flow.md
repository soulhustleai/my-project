# Intake & Signature Flow

## Trigger
Opportunity status = 'interested' (claimant expressed interest in proceeding)

## Flow

```
START (interested claimant)
  │
  ├─ 1. SEND INTAKE LINK
  │   ├─ Generate unique Jotform link with pre-filled fields:
  │   │   ├─ Claimant name
  │   │   ├─ Property address
  │   │   ├─ County + case number
  │   │   ├─ Estimated surplus amount
  │   │   └─ Fee percentage
  │   ├─ Send link via SMS + email
  │   ├─ Update opportunity status → 'intake_pending'
  │   └─ Log in audit_log
  │
  ├─ 2. CLAIMANT COMPLETES FORM
  │   │
  │   │  Form collects:
  │   │  ├─ Full legal name (as on government ID)
  │   │  ├─ Date of birth
  │   │  ├─ Current mailing address
  │   │  ├─ Phone number
  │   │  ├─ Email address
  │   │  ├─ Government ID upload (photo of driver's license or passport)
  │   │  ├─ Relationship to property (owner / heir / spouse / other)
  │   │  ├─ If heir: death certificate upload
  │   │  ├─ E-signature on contingency fee agreement
  │   │  └─ Acknowledgment of terms
  │   │
  │   ├─ Jotform webhook fires → Supabase
  │   ├─ Create case record (status: 'signed')
  │   ├─ Store uploaded docs in documents table
  │   ├─ Send confirmation SMS + email to claimant
  │   └─ Notify founder (P4 info)
  │
  ├─ 3. FORM INCOMPLETE? → AUTO FOLLOW-UP
  │   ├─ If form started but not submitted:
  │   │   ├─ Day 1: SMS reminder with link
  │   │   ├─ Day 3: Email reminder
  │   │   └─ Day 7: Final SMS ("We still need your info to proceed")
  │   ├─ If still incomplete after 14 days → founder action (phone call)
  │   └─ If 30 days no completion → status: 'stalled'
  │
  ├─ 4. DOCUMENT VERIFICATION
  │   ├─ System checks:
  │   │   ├─ [ ] ID uploaded (readable)
  │   │   ├─ [ ] Agreement signed
  │   │   ├─ [ ] Name on ID matches agreement
  │   │   ├─ [ ] Address provided
  │   │   └─ [ ] Relationship to property stated
  │   ├─ If all checks pass → status: 'docs_collecting'
  │   └─ If missing items → send specific request to claimant
  │
  ├─ 5. NOTARIZATION
  │   ├─ Determine if county requires notarized affidavit (most do)
  │   ├─ If yes:
  │   │   ├─ Option A: Remote Online Notarization (RON)
  │   │   │   ├─ Send RON link (Notarize.com, NotaryCam, etc.)
  │   │   │   └─ Claimant completes online (15 min, ~$25)
  │   │   ├─ Option B: In-person notary
  │   │   │   ├─ Provide list of nearby UPS Stores / banks with notary
  │   │   │   └─ Send pre-filled affidavit for claimant to bring
  │   │   └─ Follow up until notarization complete
  │   ├─ If notarized doc received → update document status
  │   └─ All docs complete → case status: 'docs_complete'
  │
  └─ 6. HANDOFF TO CLAIM PREP
      ├─ Case status: 'docs_complete'
      ├─ Triggers claim-prep-flow.md
      └─ Log in audit_log
```

## Founder Escalations in This Flow
- Claimant wants to discuss on phone before signing → FA-011 (phone call)
- Form incomplete after 14 days → FA reminder
- Complex situation (heir, entity, multiple claimants) → FA review

## Required Templates
- Contingency fee agreement (see templates/documents/contingency_agreement.md)
- Notarized affidavit template
- Confirmation SMS
- Confirmation email
- Reminder sequences (SMS + email)
