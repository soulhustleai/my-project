# Claim Preparation Flow

## Trigger
Case status = 'docs_complete'

## Flow

```
START (docs_complete case)
  │
  ├─ 1. IDENTIFY COUNTY REQUIREMENTS
  │   ├─ Look up county in filing_templates registry
  │   ├─ Get list of required documents:
  │   │   ├─ Claim form / motion (county-specific)
  │   │   ├─ Cover letter
  │   │   ├─ Contingency agreement copy
  │   │   ├─ Claimant ID copy
  │   │   ├─ Notarized affidavit of claim
  │   │   ├─ Power of Attorney (if required)
  │   │   ├─ W-9 (if required)
  │   │   ├─ Proof of ownership / connection (deed, court record)
  │   │   └─ Any county-specific supplemental forms
  │   └─ Update case status → 'claim_prep'
  │
  ├─ 2. GENERATE DOCUMENTS
  │   ├─ For each required template:
  │   │   ├─ Load template
  │   │   ├─ Merge case data + claimant data
  │   │   ├─ Generate PDF
  │   │   └─ Save to documents table (status: 'generated')
  │   └─ Log generation in audit_log
  │
  ├─ 3. ASSEMBLE PACKET
  │   ├─ Combine in filing order:
  │   │   1. Cover letter
  │   │   2. Claim form / motion
  │   │   3. Signed agreement
  │   │   4. Notarized affidavit
  │   │   5. ID copy
  │   │   6. POA (if applicable)
  │   │   7. W-9 (if applicable)
  │   │   8. Supporting docs
  │   ├─ Generate combined PDF (claim_packet)
  │   └─ Save to documents table (doc_type: 'claim_packet')
  │
  ├─ 4. VALIDATION CHECKLIST
  │   ├─ Automated checks:
  │   │   ├─ [ ] Case number matches on all docs
  │   │   ├─ [ ] Claimant name matches on all docs
  │   │   ├─ [ ] Surplus amount referenced correctly
  │   │   ├─ [ ] All required docs present
  │   │   ├─ [ ] Signatures present where needed
  │   │   ├─ [ ] Notarization present where needed
  │   │   ├─ [ ] Filing address / method identified
  │   │   └─ [ ] No blank required fields
  │   ├─ If all checks pass → status: 'ready_to_file'
  │   └─ If any fail → flag specific issue, request correction
  │
  └─ 5. FOUNDER REVIEW
      ├─ Create FOUNDER ACTION: FA-010 (Review Claim Packet)
      ├─ Founder reviews packet (5-10 min)
      ├─ If approved → trigger submission-flow.md
      └─ If issues found → correct and re-generate
```

## County Filing Template Registry

```python
FILING_TEMPLATES = {
    'Broward_FL_foreclosure': {
        'required_docs': ['claim_form', 'cover_letter', 'affidavit', 'id_copy', 'agreement'],
        'claim_form_template': 'broward_fl_surplus_claim.md',
        'filing_method': 'mail',
        'filing_address': '201 SE 6th St, Fort Lauderdale, FL 33301',
        'attn': 'Clerk of Courts - Surplus Funds',
        'notes': 'Include self-addressed stamped envelope for receipt confirmation'
    },
    'Palm Beach_FL_foreclosure': {
        'required_docs': ['claim_form', 'cover_letter', 'affidavit', 'id_copy', 'agreement'],
        'claim_form_template': 'palm_beach_fl_surplus_claim.md',
        'filing_method': 'mail',
        'filing_address': '205 N Dixie Hwy, West Palm Beach, FL 33401',
        'attn': 'Clerk & Comptroller - Surplus Funds',
        'notes': ''
    },
    'Hillsborough_FL_foreclosure': {
        'required_docs': ['claim_form', 'cover_letter', 'affidavit', 'id_copy', 'agreement'],
        'claim_form_template': 'hillsborough_fl_surplus_claim.md',
        'filing_method': 'mail',
        'filing_address': '800 E Twiggs St, Tampa, FL 33602',
        'attn': 'Clerk of Courts - Registry Funds',
        'notes': ''
    }
}
```
