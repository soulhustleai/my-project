# System Architecture

## Overview

A modular pipeline that flows: **Sources → Ingestion → Normalization → Scoring → Enrichment → Outreach → Intake → Claim Prep → Submission → Tracking → Payout**.

Each stage is a discrete service that reads from and writes to a shared Supabase (Postgres) database. Services communicate through database state changes and optional event triggers.

---

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                        COUNTY SOURCES                          │
│  (Clerk websites, court portals, treasurer sites, PDF lists)   │
└────────────────────────────┬────────────────────────────────────┘
                             │
                    ┌────────▼────────┐
                    │  Source Monitor  │  Cron: checks sources for new data
                    │  (Playwright)   │  Writes: raw_downloads table
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │ Record Ingestion│  Parses PDFs/HTML → structured records
                    │ (pdfplumber +   │  Writes: raw_records table
                    │  Claude API)    │
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │  Normalization  │  Dedupes, validates, normalizes
                    │                 │  Writes: opportunities table
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │ Opportunity     │  Scores by amount, recency, claimant
                    │ Engine          │  identifiability, county ease
                    │                 │  Updates: opportunities.score
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │ Claimant        │  Skip trace, phone/email/address
                    │ Enrichment      │  Writes: claimants table
                    │ (PDL/manual)    │  Links: opportunity → claimant
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │ Outreach Engine │  Mail (Lob), SMS (Twilio),
                    │                 │  Email, Phone queue
                    │                 │  Writes: outreach_events table
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │ Intake/Signing  │  Forms (Jotform), E-sign
                    │                 │  Writes: cases table (status → signed)
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │ Document Engine │  Generate claim packets
                    │ (templates)     │  Writes: documents table
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │ Submission      │  File claims (mail/portal/in-person)
                    │ Engine          │  Updates: cases.status → filed
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │ Case Tracker    │  Monitor claim status
                    │                 │  Updates: cases.status
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │ Notifications   │  Alerts, escalations, founder actions
                    │                 │  Writes: notifications table
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │   Dashboard     │  Pipeline view, KPIs, case management
                    │  (Next.js)      │  Reads: all tables
                    └─────────────────┘
```

---

## Data Flow

### Primary Data Tables (Supabase/Postgres)

```
county_sources        → Source registry (URLs, schedules, parsers)
raw_downloads         → Downloaded files/pages from sources
raw_records           → Parsed but unnormalized records
opportunities         → Normalized, scored surplus opportunities
claimants             → Enriched claimant contact data
outreach_events       → All outreach attempts and responses
cases                 → Signed clients with case lifecycle
documents             → Generated documents and claim packets
submissions           → Filed claims and tracking info
notifications         → System alerts and founder escalations
audit_log             → All state changes for compliance
```

### Event Flow

```
1. source_check_completed    → triggers record ingestion
2. records_ingested          → triggers normalization
3. opportunities_scored      → triggers claimant enrichment
4. claimant_enriched         → triggers outreach queuing
5. outreach_response         → triggers follow-up or intake
6. agreement_signed          → triggers document generation
7. documents_ready           → triggers submission (or founder escalation)
8. claim_filed               → triggers case tracking
9. claim_status_changed      → triggers notification
10. funds_disbursed          → triggers payout processing
```

Events are implemented as database triggers + cron-based polling (MVP) or BullMQ jobs (scale).

---

## State Transitions

### Opportunity Lifecycle

```
NEW → QUALIFIED → ENRICHING → CONTACTABLE → OUTREACH_ACTIVE →
  → RESPONDED → INTERESTED → INTAKE_PENDING → SIGNED →
  → CLAIM_PREP → FILED → TRACKING → APPROVED → DISBURSED → PAID

  (at any stage) → DISQUALIFIED / UNRESPONSIVE / DECLINED / DENIED
```

### Case Lifecycle (post-signing)

```
SIGNED → DOCS_COLLECTING → DOCS_COMPLETE → CLAIM_PREP →
  → REVIEW_PENDING → FILED → ACKNOWLEDGED → UNDER_REVIEW →
  → APPROVED → DISBURSEMENT_PENDING → DISBURSED →
  → FEE_COLLECTED → CLOSED

  (at any stage) → DENIED → APPEAL / CLOSED
  (at any stage) → STALLED → ESCALATED
```

---

## Service Specifications

### 1. Source Monitor
- **Trigger:** Cron (every 6-24 hours per source, configurable)
- **Input:** county_sources registry
- **Output:** raw_downloads table (files, HTML snapshots)
- **Failure mode:** Log error, retry next cycle, alert after 3 consecutive failures
- **Retry:** 3 attempts with exponential backoff per source
- **Dependencies:** Playwright, county_sources config

### 2. Record Ingestion
- **Trigger:** New raw_downloads entry
- **Input:** Downloaded PDF/HTML files
- **Output:** raw_records table (parsed fields)
- **Failure mode:** Flag unparseable records, queue for manual review
- **Tools:** pdfplumber (structured PDFs), Claude API (messy PDFs), BeautifulSoup (HTML)
- **Dependencies:** pdfplumber, anthropic SDK

### 3. Normalization
- **Trigger:** New raw_records entries
- **Input:** raw_records
- **Output:** opportunities table (deduplicated, validated)
- **Logic:** Deduplicate by case number + county, validate surplus amount > $0, normalize names/addresses
- **Failure mode:** Flag ambiguous records for review

### 4. Opportunity Engine
- **Trigger:** New opportunities entries
- **Input:** opportunities table
- **Output:** Updated score field on opportunities
- **Scoring factors:** Surplus amount (40%), recency (20%), claimant identifiability (20%), county filing ease (10%), competition estimate (10%)
- **Dependencies:** Scoring model config

### 5. Claimant Enrichment
- **Trigger:** Opportunities with score > threshold
- **Input:** Owner name, property address from opportunity
- **Output:** claimants table (phone, email, current address, confidence score)
- **Tools:** People Data Labs API, TruePeopleSearch (manual fallback)
- **Failure mode:** Mark as "enrichment_failed," retry once, then flag for manual
- **Rate limiting:** Respect API limits, batch requests

### 6. Outreach Engine
- **Trigger:** New contactable claimants
- **Input:** claimants + opportunities
- **Output:** outreach_events table
- **Channels:** Direct mail (Lob API) → SMS (Twilio, day 5) → Email (day 7) → Phone queue (day 10, high-value only)
- **Sequence:** 7-touch sequence over 30 days
- **Failure mode:** Log delivery failures, skip undeliverable addresses
- **Compliance:** TCPA for SMS/phone, CAN-SPAM for email, state-specific rules

### 7. Document Engine
- **Trigger:** Case status → SIGNED
- **Input:** Case data, claimant data, county filing templates
- **Output:** documents table (generated PDFs)
- **Templates:** Contingency agreement, affidavit, POA, cover letter, claim form
- **Tools:** Google Docs API or Puppeteer PDF generation
- **Dependencies:** County-specific template library

### 8. Submission Engine
- **Trigger:** Documents complete + founder review (if required)
- **Input:** Completed claim packet
- **Output:** submissions table (tracking number, filing date)
- **Methods:** Mail (Lob for print + mail), portal upload, in-person (founder escalation)
- **Failure mode:** Escalate to founder if submission method unclear

### 9. Case Tracker
- **Trigger:** Cron (weekly check on all filed cases)
- **Input:** Filed cases
- **Output:** Updated case status
- **Methods:** Portal check (if available), phone call to clerk (founder/VA), mail status inquiry
- **Failure mode:** Flag stalled cases after 90 days with no update

### 10. Notifications
- **Trigger:** Any significant state change
- **Input:** Event data
- **Output:** Notification to founder (SMS, email, dashboard)
- **Types:** New high-value lead, client signed, claim filed, status change, payout received, error alert
- **Priority levels:** INFO, ACTION_NEEDED, URGENT

---

## Human Checkpoints

These are the points where founder/human review is required or recommended:

| Checkpoint | When | Why | Automatable Later? |
|-----------|------|-----|-------------------|
| High-value outreach review | Before first contact on >$25K cases | Customize messaging | Partially |
| Agreement review | Before sending for signature | Legal accuracy | With templates |
| Claim packet review | Before filing | Ensure completeness | With checklist validation |
| Submission (some counties) | When portal/in-person required | Can't automate all methods | Partially (portal bots) |
| Status check calls | When no portal exists | Manual inquiry | No (human required) |
| Payout processing | When check received | Deposit and disburse | No (banking) |

---

## Retries & Fallbacks

| Service | Retry Strategy | Fallback |
|---------|---------------|----------|
| Source Monitor | 3x exponential backoff | Alert, skip this cycle |
| Record Ingestion | Re-parse with Claude API | Flag for manual parsing |
| Enrichment | Retry different provider | Mark as manual enrichment needed |
| Outreach (mail) | Lob handles delivery | Skip if undeliverable |
| Outreach (SMS) | 1 retry | Fall back to email only |
| Submission | Retry mail delivery | Escalate to founder |
| Case Tracking | Retry next cycle | Flag stalled case |

---

## Observability

- **Audit log:** Every state change on every record is logged with timestamp, actor, old/new state
- **Error tracking:** Sentry for all services
- **Pipeline metrics:** Records processed, success/failure rates, latency per stage
- **Business metrics:** Leads generated, conversion rates, revenue pipeline
- **Alerts:** Sentry + Twilio SMS for critical errors, daily digest email for pipeline summary

---

## Dependency Map

```
docs/system-architecture.md
  ↓ feeds
schemas/core-data-model.md          (table definitions)
schemas/lead-lifecycle.md           (state machine)
schemas/county-source-registry.md   (source configs)
workflows/*                         (all workflow specs)
services/*                          (all service implementations)
apps/dashboard/                     (UI reads from all tables)
```
