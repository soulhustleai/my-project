# Outreach Flow

## Trigger
Opportunity status = 'contactable' with linked claimant

## Flow

```
START (contactable opportunity)
  │
  ├─ 1. INITIALIZE SEQUENCE
  │   ├─ Create outreach plan based on OUTREACH_SEQUENCE config
  │   ├─ Determine available channels:
  │   │   ├─ Mail: requires valid address (always attempt)
  │   │   ├─ SMS: requires verified phone
  │   │   ├─ Email: requires email
  │   │   └─ Phone: requires phone + surplus > $10K
  │   ├─ Update opportunity status → 'outreach_active'
  │   └─ Log in audit_log
  │
  ├─ 2. STEP 1: DIRECT MAIL (Day 0)
  │   ├─ Generate letter from template (mail_letter_1)
  │   │   ├─ Merge fields: claimant name, property address, county, case number, surplus amount
  │   │   ├─ Include: business info, phone, website, verification instructions
  │   │   └─ Validate all merge fields populated
  │   ├─ Send via Lob API
  │   │   ├─ Address verification (Lob does this automatically)
  │   │   ├─ On success → create outreach_event (type: 'sent')
  │   │   └─ On failure → log error, try alternate address if available
  │   └─ Track Lob delivery webhook → update event (type: 'delivered' or 'returned')
  │
  ├─ 3. STEP 2: SMS FOLLOW-UP (Day 5)
  │   ├─ Check: claimant has phone + not opted out
  │   ├─ Check: no response received yet
  │   ├─ Generate SMS from template (sms_followup_1)
  │   ├─ Send via Twilio
  │   │   ├─ Include STOP opt-out language
  │   │   ├─ Respect TCPA hours (8 AM - 9 PM local)
  │   │   └─ On success → create outreach_event
  │   └─ Monitor inbound: Twilio webhook → outreach_event (direction: 'inbound')
  │
  ├─ 4. STEP 3: EMAIL (Day 8)
  │   ├─ Check: claimant has email + not opted out + not responded
  │   ├─ Generate email from template (email_followup_1)
  │   ├─ Send via Smartlead or SendGrid
  │   └─ Track opens/clicks → outreach_event
  │
  ├─ 5. STEP 4: SECOND MAIL (Day 12)
  │   ├─ Check: not responded
  │   ├─ Send mail_letter_2 (different angle/urgency)
  │   └─ Same Lob flow as Step 1
  │
  ├─ 6. STEP 5: SECOND SMS (Day 16)
  │   ├─ Same flow as Step 2 with sms_followup_2
  │   └─ Check not responded + not opted out
  │
  ├─ 7. STEP 6: PHONE CALL (Day 21, if surplus > $10K)
  │   ├─ Create FOUNDER ACTION notification
  │   │   ├─ Include: claimant name, phone, surplus amount, case summary
  │   │   ├─ Include: call script
  │   │   └─ Include: outcome logging instructions
  │   ├─ Founder makes call → logs result
  │   └─ If no answer → schedule retry in 3 days
  │
  ├─ 8. STEP 7: FINAL MAIL (Day 30)
  │   ├─ Check: not responded
  │   ├─ Send mail_final (urgency/last notice framing)
  │   └─ Same Lob flow
  │
  └─ 9. SEQUENCE COMPLETE (Day 35)
      ├─ If no response after all touches:
      │   └─ Update opportunity status → 'unresponsive'
      └─ Log completion in audit_log

INTERRUPT HANDLERS:
  ├─ If inbound response detected at any step:
  │   ├─ Pause remaining sequence
  │   ├─ Classify response (interested / declined / question / wrong person)
  │   ├─ Update opportunity status → 'responded'
  │   └─ If interested → status → 'interested', trigger intake flow
  │
  ├─ If opt-out received:
  │   ├─ Stop all outreach immediately
  │   ├─ Mark claimant.do_not_contact = true
  │   └─ Update opportunity status → 'do_not_contact'
  │
  └─ If mail returned (undeliverable):
      ├─ Try alternate address if available
      └─ If no alternate → adjust sequence (skip mail, rely on SMS/email/phone)
```

## Compliance Checks (Every Send)
- [ ] Opt-out not requested
- [ ] Within legal contact hours (SMS/phone)
- [ ] Required disclosures included
- [ ] Business info included
- [ ] Not a duplicate send (check outreach_events)
