# Implementation Backlog

## Priority Levels
- **P0:** Must have before first outreach
- **P1:** Must have before first signed client
- **P2:** Must have before first claim filed
- **P3:** Nice to have in Month 1-2
- **P4:** Scale/improvement (Month 3+)

---

## Phase 1: Foundation (Week 1)

| ID | Title | Description | Why It Matters | Dependencies | Owner | Priority | Done Criteria |
|----|-------|-------------|---------------|-------------|-------|----------|--------------|
| BL-001 | Register LLC | Florida LLC for the surplus recovery business | Legal entity needed for contracts + bank account | None | FOUNDER | P0 | Sunbiz filing confirmed |
| BL-002 | Business bank account | Open account under LLC | Receive/disburse recovery funds | BL-001 | FOUNDER | P0 | Account open, routing # available |
| BL-003 | Business phone number | Dedicated phone (Twilio or Google Voice) | Outreach must come from business number | None | FOUNDER | P0 | Number active, can send/receive SMS |
| BL-004 | Business email + domain | Professional email (e.g., claims@[domain].com) | Credibility for outreach | None | FOUNDER | P0 | Email sending/receiving works |
| BL-005 | Supabase project setup | Create Supabase project, apply core schema | All data storage | None | SYSTEM | P0 | Tables created, API accessible |
| BL-006 | Core data model | Define and create all database tables | Foundation for all services | BL-005 | SYSTEM | P0 | Schema matches core-data-model.md |

## Phase 2: Lead Generation (Week 1-2)

| ID | Title | Description | Why It Matters | Dependencies | Owner | Priority | Done Criteria |
|----|-------|-------------|---------------|-------------|-------|----------|--------------|
| BL-010 | Validate FL county sources | Confirm exact URLs, formats, access methods for Broward, Palm Beach, Hillsborough | Can't scrape without source validation | None | SYSTEM | P0 | Source registry populated for 3 counties |
| BL-011 | Broward County scraper | Playwright script to download surplus list | First lead source | BL-010 | SYSTEM | P0 | Successfully downloads latest list |
| BL-012 | Palm Beach County scraper | Playwright script to download surplus list | Second lead source | BL-010 | SYSTEM | P0 | Successfully downloads latest list |
| BL-013 | Hillsborough County scraper | Playwright script to download surplus list | Third lead source | BL-010 | SYSTEM | P0 | Successfully downloads latest list |
| BL-014 | PDF parser (Broward) | pdfplumber script to extract structured data | Convert PDFs to usable records | BL-011 | SYSTEM | P0 | Parses 90%+ of records correctly |
| BL-015 | PDF parser (Palm Beach) | pdfplumber script | Same | BL-012 | SYSTEM | P0 | Same |
| BL-016 | PDF parser (Hillsborough) | pdfplumber script | Same | BL-013 | SYSTEM | P0 | Same |
| BL-017 | Normalization pipeline | Dedupe, validate, normalize parsed records | Clean data in opportunities table | BL-014,15,16 | SYSTEM | P0 | Deduped records in opportunities table |
| BL-018 | Opportunity scorer | Score leads by amount, recency, identifiability | Prioritize outreach | BL-017 | SYSTEM | P0 | All opportunities have scores |

## Phase 3: Enrichment & Outreach (Week 2)

| ID | Title | Description | Why It Matters | Dependencies | Owner | Priority | Done Criteria |
|----|-------|-------------|---------------|-------------|-------|----------|--------------|
| BL-020 | Skip trace integration | People Data Labs API or manual TruePeopleSearch | Find claimant contact info | BL-018 | SYSTEM | P0 | 50%+ hit rate on test batch |
| BL-021 | Lob integration | API for sending direct mail | Primary outreach channel | BL-004 | SYSTEM | P0 | Test letter sends successfully |
| BL-022 | Mail letter template | Professional letter template for Lob | Outreach content | None | SYSTEM | P0 | Template reviewed, merge fields work |
| BL-023 | Twilio SMS setup | SMS sending for follow-ups | Secondary outreach channel | BL-003 | SYSTEM | P0 | Test SMS sends successfully |
| BL-024 | SMS templates | Follow-up message templates | Outreach content | None | SYSTEM | P0 | Templates drafted, TCPA-compliant |
| BL-025 | Outreach sequencer | Logic to trigger mail→SMS→email→phone over 30 days | Automated multi-touch | BL-021,23 | SYSTEM | P1 | Sequence fires on schedule |
| BL-026 | Simple landing page | Website with business info, verification language | Trust-building for outreach | BL-004 | FOUNDER/SYSTEM | P1 | Page live, looks professional |

## Phase 4: Intake & Signing (Week 2-3)

| ID | Title | Description | Why It Matters | Dependencies | Owner | Priority | Done Criteria |
|----|-------|-------------|---------------|-------------|-------|----------|--------------|
| BL-030 | Contingency agreement | Legal agreement template | Required for every client | None | SYSTEM/LEGAL | P1 | Attorney-reviewed template ready |
| BL-031 | Intake form (Jotform) | Collect claimant info + ID upload + e-sign | Client onboarding | BL-030 | SYSTEM | P1 | Form live, submissions flow to Supabase |
| BL-032 | Jotform → Supabase webhook | Auto-create case from form submission | Eliminate manual data entry | BL-031,005 | SYSTEM | P1 | Submission creates case record |
| BL-033 | Notarization coordination SOP | Instructions for RON or in-person notary | Required for most claims | None | SYSTEM | P1 | SOP written, RON vendor identified |

## Phase 5: Claim Filing (Week 3-4)

| ID | Title | Description | Why It Matters | Dependencies | Owner | Priority | Done Criteria |
|----|-------|-------------|---------------|-------------|-------|----------|--------------|
| BL-040 | Broward claim template | County-specific filing forms + instructions | File claims correctly | BL-010 | SYSTEM | P2 | Template matches county requirements |
| BL-041 | Palm Beach claim template | Same | Same | BL-010 | SYSTEM | P2 | Same |
| BL-042 | Hillsborough claim template | Same | Same | BL-010 | SYSTEM | P2 | Same |
| BL-043 | Claim packet generator | Assemble all docs into filing-ready packet | Reduce prep time per claim | BL-040-42 | SYSTEM | P2 | Generates complete packet from case data |
| BL-044 | Claim submission via Lob | Print and mail claim packets via API | Automate physical submission | BL-043 | SYSTEM | P2 | Packet mails successfully |

## Phase 6: Tracking & Operations (Month 2)

| ID | Title | Description | Why It Matters | Dependencies | Owner | Priority | Done Criteria |
|----|-------|-------------|---------------|-------------|-------|----------|--------------|
| BL-050 | Case status tracking | Track filed claims through to payout | Know where each case stands | BL-044 | SYSTEM | P3 | Status field updated per case |
| BL-051 | Pipeline dashboard (v1) | Supabase views or simple Next.js page | Visibility into operations | BL-005 | SYSTEM | P3 | Founder can see full pipeline |
| BL-052 | Founder action queue | Dashboard section showing pending actions | Reduce missed actions | BL-051 | SYSTEM | P3 | Actions visible with priority |
| BL-053 | Automated weekly report | Email summary of pipeline KPIs | Keep founder informed | BL-050 | SYSTEM | P3 | Email sends weekly with key metrics |
| BL-054 | Response classification | AI-powered inbound response sorting | Reduce manual triage | BL-025 | SYSTEM | P3 | >85% classification accuracy |

## Phase 7: Scale (Month 3+)

| ID | Title | Description | Why It Matters | Dependencies | Owner | Priority | Done Criteria |
|----|-------|-------------|---------------|-------------|-------|----------|--------------|
| BL-060 | Ohio county scrapers | Add Cuyahoga, Franklin, Hamilton OH | Expand market | Phase 1-4 complete | SYSTEM | P4 | 3 OH counties live |
| BL-061 | Maricopa AZ scraper | Add Maricopa County AZ | Expand market | Phase 1-4 complete | SYSTEM | P4 | AZ county live |
| BL-062 | Predictive lead scoring | ML model trained on conversion data | Improve lead prioritization | 50+ closed cases | SYSTEM | P4 | Model outperforms rules-based |
| BL-063 | VA onboarding system | Training docs + scripts for VA phone team | Scale outreach capacity | SOPs complete | FOUNDER | P4 | VA makes first calls independently |
| BL-064 | Full dashboard (v2) | Charts, trends, multi-county views | Operational maturity | BL-051 | SYSTEM | P4 | Full KPI dashboard spec implemented |

---

## Dependency Graph (Simplified)

```
BL-001 (LLC) ──→ BL-002 (Bank) ──→ BL-044 (Submissions)
BL-003 (Phone) ──→ BL-023 (Twilio)
BL-004 (Email) ──→ BL-021 (Lob) ──→ BL-025 (Sequencer)
BL-005 (Supabase) ──→ BL-006 (Schema) ──→ everything downstream
BL-010 (Source validation) ──→ BL-011,12,13 (Scrapers) ──→ BL-014,15,16 (Parsers)
  ──→ BL-017 (Normalize) ──→ BL-018 (Score) ──→ BL-020 (Enrich) ──→ BL-025 (Outreach)
BL-030 (Agreement) ──→ BL-031 (Intake form) ──→ BL-032 (Webhook)
BL-040-42 (Templates) ──→ BL-043 (Generator) ──→ BL-044 (Submit)
```
