# Market Hypotheses

## Purpose

State our best guesses before validation. Every hypothesis here will be confirmed, adjusted, or killed through research. This prevents confirmation bias and keeps us honest.

---

## H1: Best States for Launch

### Hypothesis
Florida, Texas, and Georgia are the best launch states due to high foreclosure volume, accessible public records, and operator-friendly filing processes.

### Reasoning
- Florida: High foreclosure volume, clerk-of-court publishes surplus lists, no state income tax (more equity in properties)
- Texas: Tax sale overages are common, county trustees hold funds, high property values in metro areas
- Georgia: Foreclosure surplus held by courts, moderate competition, growing market

### Validation Needed
- Confirm surplus list accessibility for top counties in each state
- Confirm filing requirements (attorney needed? notarization? forms available?)
- Estimate average surplus amounts from actual lists
- Assess competition density

### Alternatives to Test
- Ohio: High foreclosure volume, potentially lower competition
- Arizona: Maricopa County alone may have significant volume
- North Carolina: Growing awareness but potentially less competition
- California: Very high surplus amounts but complex filing and heavy competition

---

## H2: Best County Clusters

### Hypothesis
The best strategy is to cluster 3-5 counties in a single state to:
- Leverage shared filing processes
- Reuse templates and workflows
- Build local expertise
- Reduce legal complexity

### Specific Cluster Hypotheses

**Florida Cluster (Primary):**
- Miami-Dade County
- Broward County
- Palm Beach County
- Hillsborough County (Tampa)
- Orange County (Orlando)

**Texas Cluster (Secondary):**
- Harris County (Houston)
- Dallas County
- Tarrant County (Fort Worth)
- Bexar County (San Antonio)
- Travis County (Austin)

**Georgia Cluster (Tertiary):**
- Fulton County (Atlanta)
- DeKalb County
- Gwinnett County
- Cobb County

### Validation Needed
- Actual surplus list URLs for each county
- Format of published data (PDF vs HTML vs CSV vs portal search)
- Publication frequency (daily, weekly, monthly, after each sale)
- Historical volume (cases per year with surplus > $1,000)

---

## H3: Best Process Types

### Hypothesis
Foreclosure surplus (mortgage foreclosure excess proceeds) is the best starting point, followed by tax sale overages.

### Reasoning
- Foreclosure surplus tends to be higher dollar amounts ($5K-$100K+)
- Tax sale overages are more numerous but often smaller ($500-$10K)
- Foreclosure surplus claimants are often the former homeowner (easier to identify)
- Tax sale overage claimants may include lienholders, complicating priority

### Alternative Hypothesis
Tax sale overages may be better for MVP because:
- Lists are more frequently published
- Filing may be simpler in some states
- Higher volume = more at-bats for learning the process

### Validation Needed
- Compare average amounts: foreclosure surplus vs tax overages by county
- Compare filing complexity
- Compare claimant identification difficulty
- Compare time to payout

---

## H4: Best Claimant Segment

### Hypothesis
Former homeowners who lost property to foreclosure 6-24 months ago are the best initial target because:
- They are the most likely rightful claimant
- They are identifiable from the foreclosure record
- The surplus is recent enough that contact info may still be valid
- They are far enough out from the foreclosure to be receptive (not in crisis mode)

### Alternative Segments
- **Heirs of deceased owners** — Higher surplus amounts but harder to identify and longer process
- **Tax sale property owners** — Often still at the same address (didn't necessarily lose their home)
- **Lienholders** — May have valid claims but adds legal complexity

### Validation Needed
- Conversion rate by claimant segment (if data available from operator reports)
- Average surplus by segment
- Contact discovery difficulty by segment
- Filing complexity by segment

---

## H5: Launch Assumptions

### Assumption: Conversion Funnel
| Stage | Rate | Basis |
|-------|------|-------|
| Raw leads (from surplus list) | 100% | Starting population |
| Qualified (surplus > $1,000, claimant identifiable) | 40-60% | Many entries are small or unidentifiable |
| Contactable (valid phone/email/address found) | 50-70% of qualified | Skip tracing hit rate |
| Reached (actually responded to outreach) | 10-20% of contactable | Multi-channel outreach |
| Interested (willing to learn more) | 30-50% of reached | Once they hear "free money" |
| Signed (executed agreement) | 40-60% of interested | Trust barrier is real |
| Successful recovery | 70-85% of signed | Some claims get denied or delayed |

### Implied Math
- 100 raw leads → 50 qualified → 30 contactable → 5 reached → 2 interested → 1 signed → 0.8 recovered
- ~1% end-to-end conversion from raw lead to revenue
- Need ~200 raw leads/month for 2 recoveries/month

### Assumption: Timeline
- Week 1-2: Setup, first list pull, first enrichment
- Week 3-4: First outreach wave
- Week 5-8: First signed agreements
- Week 9-16: First claims filed
- Week 13-24: First payouts received

### Assumption: Unit Economics
- Cost per lead (enrichment): $0.50-$2.00
- Cost per outreach attempt: $1-5 (mail is ~$1-2, skip trace + multi-channel adds up)
- Cost per signed client: $50-200 (at ~1% conversion)
- Revenue per successful recovery: $3,000-$10,000+
- Gross margin per case: 85-95% (after enrichment, mail, filing costs)

---

## H6: Assumptions Requiring Urgent Validation

| # | Assumption | Risk If Wrong | Validation Method |
|---|-----------|---------------|-------------------|
| 1 | Florida counties publish surplus lists online | Can't start without leads | Check clerk websites directly |
| 2 | Surplus amounts are large enough to justify work | Bad unit economics | Pull actual lists, calculate averages |
| 3 | Skip tracing can find 50%+ of claimants | Not enough contactable leads | Test enrichment on sample batch |
| 4 | No attorney required in Florida for surplus claims | Would add cost and complexity | Review Florida statute §45.033 |
| 5 | 30% contingency fee is legal and market-standard | Fee structure at risk | Review state regulations and competitor terms |
| 6 | Outreach won't trigger legal issues (TCPA, state laws) | Compliance risk | Review outreach compliance requirements |
| 7 | County filing can be done by mail/online | In-person would slow everything | Check filing procedures per county |
| 8 | Payouts happen within 90-180 days | Cash flow problem if longer | Research actual payout timelines |

---

## Hypothesis Tracking

Each hypothesis will be updated with:
- **Status:** Unvalidated / Partially Validated / Validated / Killed
- **Evidence:** What we found
- **Impact:** How this changes the plan
- **Date validated:** When we confirmed/killed it

Current status: ALL UNVALIDATED — research phase beginning.
