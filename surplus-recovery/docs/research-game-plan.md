# Research Game Plan

## Purpose

Define what we need to learn, how we'll evaluate it, and how we'll make decisions — before diving into execution. This prevents drift, hype-chasing, and analysis paralysis.

---

## Research Questions

### Market & Opportunity
1. Which states have the most accessible surplus funds data?
2. Which counties within those states publish lists online and in parseable formats?
3. What is the typical surplus amount range by county and sale type?
4. How quickly do surplus lists get picked over by competitors?
5. What is the realistic conversion rate from lead → signed client → successful recovery?
6. What is the typical timeline from claim filing to payout by state/county?

### Process & Legal
7. What are the filing requirements per state (forms, notarization, attorney, deadlines)?
8. What is the statute of limitations on surplus claims by state?
9. Which states require attorney involvement, and at what thresholds?
10. What are the fee cap regulations by state (some cap contingency fees)?
11. What are the CROA / UDAP / state-specific consumer protection risks?
12. What disclosures are required in claimant agreements?

### Operations & Automation
13. What data sources exist for surplus lists (clerk sites, court portals, state registries)?
14. What formats do these sources publish in (PDF, HTML table, CSV, search portal)?
15. What skip tracing / enrichment services work best for this use case?
16. What CRM / pipeline tools do successful operators use?
17. What outreach channels convert best (mail, email, SMS, phone, door knock)?
18. What does a high-converting outreach message look like?

### Competition & Ecosystem
19. Who are the active operators in target markets?
20. What do coaching/course sellers teach (signal about what works)?
21. What do public complaints/reviews reveal about operator practices?
22. What tools/services are purpose-built for this niche?

---

## Source Evaluation Criteria

| Criterion | Weight | Definition |
|-----------|--------|------------|
| Recency | High | Information from 2024-2026 preferred; pre-2022 deprioritized |
| Specificity | High | State/county-specific data over generic claims |
| Practitioner origin | High | From actual operators over coaches/marketers |
| Verifiability | Medium | Can be cross-referenced with public records |
| Actionability | High | Leads to a specific decision or action |
| Bias awareness | Medium | Coaching/course sellers have incentive to overstate |

---

## Market Ranking Criteria

States and counties will be ranked on:

| Factor | Weight | Scoring |
|--------|--------|---------|
| Surplus volume (cases/year) | 25% | Based on available data |
| Average surplus amount | 15% | Higher = better unit economics |
| Data accessibility | 20% | Online, parseable, timely updates |
| Filing simplicity | 15% | Forms available, no attorney required, clear process |
| Statute of limitations | 5% | Longer = deeper backlog to mine |
| Competition density | 10% | Less competition = higher conversion |
| Automation friendliness | 10% | Structured data, consistent formats |

---

## Tooling Comparison Criteria

| Factor | Weight |
|--------|--------|
| Speed to deploy (MVP) | 25% |
| Cost at MVP scale | 20% |
| Reliability / uptime | 15% |
| Maintenance burden | 15% |
| Scale ceiling | 10% |
| Integration ease | 10% |
| Community / support | 5% |

---

## Hype Filtering Protocol

The surplus funds space is flooded with course sellers and "passive income" marketers. Every claim will be filtered:

1. **"You can make $10K/month passively"** → Reality: requires consistent pipeline work; revenue is lumpy and delayed
2. **"Just pull the list and send letters"** → Reality: conversion is low (2-5%); most leads are stale or contacted by competitors
3. **"No experience needed"** → Reality: understanding filing requirements per county is critical
4. **"AI does everything"** → Reality: AI helps with parsing, enrichment, and outreach — but submission and trust-building remain human-heavy
5. **"Works in any state"** → Reality: some states are dramatically easier than others

### Hype Test
For any tool, process, or market claim:
- Has an actual operator (not course seller) validated this?
- Can I verify this against public records or county websites?
- Does this survive the "messy real data" test?
- Is the cost/complexity proportional to the benefit?

---

## Decision Framework

Decisions will be made using this hierarchy:

1. **Does it accelerate first signed client?** → Top priority
2. **Does it reduce founder time per case?** → Second priority
3. **Does it improve conversion at any funnel stage?** → Third priority
4. **Does it improve data quality or reliability?** → Fourth priority
5. **Does it scale well?** → Fifth priority (don't over-optimize for scale at MVP)

### When In Doubt
- Choose the faster option over the better option
- Choose the simpler option over the cleverer option
- Choose the manual-but-working option over the automated-but-unproven option
- Build for one county first, then generalize

---

## Research Phases

### Phase 1: Market Selection (This Sprint)
- Validate top 5 states
- Identify top 3-5 counties per state
- Confirm data accessibility for each
- Score and rank

### Phase 2: Process Mapping (This Sprint)
- Map filing requirements for top 5 counties
- Identify document templates needed
- Map claimant discovery workflow
- Map outreach-to-signature flow

### Phase 3: Tool Selection (This Sprint)
- Evaluate scraping/monitoring tools for target sources
- Select CRM/pipeline tool
- Select enrichment/skip tracing vendor
- Select outreach stack
- Select document/e-sign tool

### Phase 4: Build (Next Sprint)
- Scaffold services
- Build first source connector
- Build first enrichment pipeline
- Build first outreach sequence
- Test end-to-end on real leads
