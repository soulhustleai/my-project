# Human Task Map

## Purpose

Classify every business step by automation level. This prevents over-automating what needs humans and under-automating what doesn't.

---

## Classification Key

| Level | Code | Definition |
|-------|------|-----------|
| Fully Automatable | **AUTO** | System handles end-to-end, no human touch |
| Automatable with Review | **AUTO-R** | System does the work, human confirms/approves |
| Founder-Only | **FOUNDER** | Requires Edwin's direct involvement |
| Attorney/Specialist | **LEGAL** | Requires attorney, notary, or specialist |

---

## Pipeline Stage Map

### Stage 1: Lead Generation

| Task | Level | Notes |
|------|-------|-------|
| Monitor county sources for new lists | **AUTO** | Cron + Playwright |
| Download surplus list files | **AUTO** | Automated download |
| Parse PDFs/HTML into structured data | **AUTO** | pdfplumber + Claude |
| Normalize and deduplicate records | **AUTO** | Rules-based |
| Score opportunities | **AUTO** | Scoring algorithm |
| Filter minimum threshold | **AUTO** | Amount > $1,000 |

### Stage 2: Claimant Discovery

| Task | Level | Notes |
|------|-------|-------|
| Extract owner/defendant name | **AUTO** | From surplus record |
| Cross-reference property records | **AUTO** | Property appraiser lookup |
| Skip trace for contact info | **AUTO** | PDL API |
| Validate address (NCOA check) | **AUTO** | Lob address verification |
| Manual enrichment for hard-to-find | **FOUNDER** | TruePeopleSearch manual lookup |
| Verify identity match (is this the right person?) | **AUTO-R** | System matches, founder spot-checks |

### Stage 3: Outreach

| Task | Level | Notes |
|------|-------|-------|
| Generate personalized mail letters | **AUTO** | Templates + merge fields |
| Send direct mail | **AUTO** | Lob API |
| Send SMS follow-ups | **AUTO** | Twilio |
| Send email follow-ups | **AUTO** | Smartlead/SendGrid |
| Schedule and manage drip sequence | **AUTO** | Automated sequences |
| Handle inbound responses (initial) | **AUTO-R** | System categorizes, founder reviews |
| Make phone calls (high-value leads) | **FOUNDER** | Trust-building requires human voice |
| Handle objections on phone | **FOUNDER** | Human judgment needed |

### Stage 4: Intake & Signing

| Task | Level | Notes |
|------|-------|-------|
| Send intake form link | **AUTO** | Triggered by "interested" status |
| Collect intake information | **AUTO** | Jotform |
| Collect e-signature on agreement | **AUTO** | Jotform e-sign or PandaDoc |
| Follow up on incomplete forms | **AUTO** | Automated reminders |
| Walk claimant through form (phone) | **FOUNDER** | For non-tech-savvy claimants |
| Collect notarized documents | **FOUNDER** | Coordinate RON or in-person notary |
| Verify document completeness | **AUTO-R** | System checks, founder confirms |

### Stage 5: Claim Preparation

| Task | Level | Notes |
|------|-------|-------|
| Generate claim packet from template | **AUTO** | County-specific templates |
| Populate claim forms with case data | **AUTO** | Data merge |
| Assemble supporting documents | **AUTO** | System organizes uploads |
| Review claim packet accuracy | **AUTO-R** | System generates, founder reviews |
| Identify missing or incorrect items | **AUTO** | Checklist validation |

### Stage 6: Claim Submission

| Task | Level | Notes |
|------|-------|-------|
| Submit via mail (print + send) | **AUTO** | Lob API for print + mail |
| Submit via county portal | **FOUNDER** | Most portals can't be automated |
| Submit in person | **FOUNDER** | When required by county |
| Notarize documents | **LEGAL** | Notary public (RON or in-person) |
| Attorney filing (if required) | **LEGAL** | Complex cases or county requires it |

### Stage 7: Case Tracking

| Task | Level | Notes |
|------|-------|-------|
| Monitor claim status online | **AUTO** | Portal check where available |
| Call clerk for status update | **FOUNDER** | Many counties have no online tracking |
| Respond to county requests for info | **AUTO-R** | System drafts response, founder sends |
| Handle claim denial/appeal | **LEGAL** | Attorney involvement recommended |
| Track payout disbursement | **FOUNDER** | Check receipt, bank coordination |

### Stage 8: Payout & Fee Collection

| Task | Level | Notes |
|------|-------|-------|
| Receive disbursement check | **FOUNDER** | Physical mail |
| Deposit check | **FOUNDER** | Bank deposit |
| Calculate fee and client portion | **AUTO** | Based on agreement terms |
| Send client their portion | **FOUNDER** | Wire/check/Zelle |
| Generate receipt/invoice | **AUTO** | Template-based |
| Update case status to closed | **AUTO** | Triggered by payout confirmation |

### Stage 9: Business Operations

| Task | Level | Notes |
|------|-------|-------|
| Pipeline reporting | **AUTO** | Dashboard |
| KPI calculation | **AUTO** | Automated queries |
| Revenue reporting | **AUTO** | From case data |
| Tax reporting / bookkeeping | **FOUNDER** | Or hire bookkeeper |
| Business entity maintenance | **FOUNDER** | Annual filings, renewals |
| Marketing / brand building | **FOUNDER** | Website, social, content |

---

## Summary Statistics

| Level | Count | % of Total |
|-------|-------|-----------|
| **AUTO** (Fully Automatable) | 22 | 50% |
| **AUTO-R** (Auto with Review) | 7 | 16% |
| **FOUNDER** (Founder-Only) | 12 | 27% |
| **LEGAL** (Attorney/Specialist) | 3 | 7% |

**73% of all tasks are fully or mostly automatable.**

---

## Founder Time Estimate (Steady State)

| Activity | Frequency | Time/Instance | Weekly Total |
|----------|-----------|--------------|-------------|
| Review inbound responses | Daily | 10 min | 70 min |
| Phone calls (high-value) | 2-3/week | 15 min | 45 min |
| Review claim packets | 1-2/week | 10 min | 20 min |
| Deposit/disburse checks | 1-2/month | 15 min | 8 min |
| Pipeline review | Weekly | 15 min | 15 min |
| Handle escalations | As needed | 10 min | 20 min |
| **Total** | | | **~3 hrs/week** |

After automation is stable, founder should spend 3-5 hours/week max.

---

## Dependency Map

```
docs/human-task-map.md
  ↓ feeds
docs/founder-action-protocol.md    (format for FOUNDER tasks)
docs/autonomy-roadmap.md           (path to reduce FOUNDER tasks)
workflows/founder-escalation-flow.md
```
