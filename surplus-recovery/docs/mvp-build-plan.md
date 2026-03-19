# MVP Build Plan

## Guiding Principle

The smallest system capable of generating a signed client from a real surplus lead. Everything else waits.

---

## What "MVP" Means Here

Not a demo. Not a prototype. A working pipeline that:
1. Finds real surplus leads from real county sources
2. Identifies the claimant
3. Finds their contact info
4. Sends professional outreach
5. Collects a signed agreement
6. Prepares a claim packet
7. Files the claim (with founder assist where needed)

---

## MVP Scope

### MUST BUILD NOW (Week 1-2)

| # | Component | What It Does | Build Effort | Tool |
|---|-----------|-------------|-------------|------|
| 1 | Source connectors (3 counties) | Download surplus lists from Broward, Palm Beach, Hillsborough FL | 1-2 days | Playwright + Python |
| 2 | PDF parser | Extract structured data from surplus list PDFs | 1-2 days | pdfplumber + Claude Haiku |
| 3 | Supabase schema | Core tables: opportunities, claimants, outreach_events, cases | 1 day | Supabase SQL |
| 4 | Opportunity scorer | Score leads by amount, recency, identifiability | 0.5 day | Python script |
| 5 | Enrichment pipeline | Look up claimant contact info | 1 day | Python + PDL API / manual |
| 6 | Outreach generator | Generate personalized mail letters | 0.5 day | Python + templates |
| 7 | Mail sender | Send physical letters via API | 0.5 day | Lob API |
| 8 | SMS follow-up | Send follow-up SMS after mail | 0.5 day | Twilio |
| 9 | Intake form | Collect claimant info + e-sign agreement | 1 day | Jotform |
| 10 | Claim packet template | County-specific filing templates (FL) | 1 day | Google Docs |

**Total build time: ~8-10 days of focused work**

### CAN BE SEMI-MANUAL INITIALLY (Month 1-2)

| Component | Manual Approach | Automate When |
|-----------|----------------|--------------|
| Source monitoring | Manual check 2x/week | After first 10 leads processed |
| Enrichment | TruePeopleSearch manual lookups | After first 5 enrichments |
| Phone follow-up | Edwin calls high-value leads | After first signed client |
| Document generation | Fill templates manually | After 3rd claim packet |
| Claim submission | Mail via USPS or county portal | Keep manual until patterns clear |
| Case tracking | Spreadsheet or Supabase manual updates | After 5 filed claims |
| Dashboard | Supabase table view | After pipeline is flowing |

### SHOULD WAIT (Month 3+)

| Component | Why It Waits |
|-----------|-------------|
| Full dashboard UI | Pipeline needs to be flowing first |
| Multi-state expansion | Validate FL first |
| AI voice follow-up | Manual calls convert better initially |
| Automated case tracking | Need to understand county response patterns first |
| Advanced scoring model | Need real conversion data to calibrate |
| Contractor/VA onboarding | Need SOPs from doing it yourself first |

### MUST BE STABLE FROM DAY ONE

| Component | Why |
|-----------|-----|
| Data model | Changing schema later is painful; get it right |
| Outreach compliance | TCPA/state law violations are expensive |
| Agreement template | Legal document — must be correct |
| Audit logging | Track every action for compliance |
| Lead deduplication | Contacting same person twice looks unprofessional |

---

## Build Order

```
Week 1:
  Day 1-2: Supabase schema + county source configs
  Day 3-4: Source connectors (Playwright scripts for 3 FL counties)
  Day 5:   PDF parser + normalization pipeline

Week 2:
  Day 1:   Opportunity scoring + enrichment pipeline
  Day 2:   Outreach templates + Lob integration
  Day 3:   Twilio SMS follow-up sequence
  Day 4:   Jotform intake form + agreement template
  Day 5:   Claim packet templates (FL-specific)

Week 3:
  First batch of real leads through the pipeline
  Manual enrichment + first outreach wave
  Monitor responses, iterate messaging

Week 4:
  Follow-up sequences active
  First intake conversations
  Target: first signed agreement
```

---

## MVP Architecture (Simplified)

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│ Python        │     │  Supabase    │     │  External    │
│ Scripts       │────▶│  (Postgres)  │◀────│  Services    │
│ (cron/manual) │     │              │     │              │
└──────────────┘     └──────────────┘     └──────────────┘
                            │
  Scripts:                  │              Services:
  - scrape_sources.py       │              - Lob (mail)
  - parse_pdfs.py           │              - Twilio (SMS)
  - normalize.py            │              - PDL (enrichment)
  - score.py                │              - Claude API (parsing)
  - enrich.py               │              - Jotform (intake)
  - generate_outreach.py    │
  - send_mail.py            │
  - send_sms.py             │
  - generate_claim.py       │
```

No microservices. No event bus. No complex orchestration. Just Python scripts that read/write to Supabase, triggered by cron or manually.

---

## Cost Budget (Month 1)

| Item | Cost |
|------|------|
| Supabase | $0 (free tier) |
| Railway (cron hosting) | $5 |
| Claude API | $10-20 |
| People Data Labs | $0-50 |
| Lob (50-100 letters) | $75-150 |
| Twilio (SMS) | $5-10 |
| Jotform | $0 (free tier) |
| Domain + business email | $10-15 |
| **Total** | **$105-250** |

---

## Success Criteria

| Metric | Target | Timeframe |
|--------|--------|-----------|
| Leads ingested | 100+ | Week 2 |
| Leads enriched | 50+ | Week 3 |
| Outreach sent | 50+ | Week 3 |
| Responses received | 5+ | Week 4-5 |
| Agreements signed | 1+ | Week 5-6 |
| Claims filed | 1+ | Week 7-8 |

---

## Dependency Map

```
docs/mvp-build-plan.md
  ↓ feeds
schemas/core-data-model.md     (what to build in Supabase)
services/source-monitor/       (scrape_sources.py)
services/record-ingestion/     (parse_pdfs.py)
services/normalization/        (normalize.py)
services/opportunity-engine/   (score.py)
services/claimant-enrichment/  (enrich.py)
services/outreach-engine/      (generate_outreach.py, send_mail.py, send_sms.py)
services/document-engine/      (generate_claim.py)
templates/outreach/            (letter templates)
templates/documents/           (claim packet templates)
ops/implementation-backlog.md  (task list derived from this plan)
```
