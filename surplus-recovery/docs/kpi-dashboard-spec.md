# KPI Dashboard Spec

## Purpose

Define every metric the dashboard must display. Organized by type: leading indicators (predict future), lagging indicators (measure past), and operational health.

---

## Dashboard Layout

```
┌─────────────────────────────────────────────────────────────┐
│  HEADER: Revenue MTD | Pipeline Value | Active Cases | Alerts│
├──────────────────────────┬──────────────────────────────────┤
│  FUNNEL METRICS          │  REVENUE METRICS                 │
│  (leads → signed)        │  (filed → paid)                  │
├──────────────────────────┼──────────────────────────────────┤
│  SOURCE HEALTH           │  OUTREACH PERFORMANCE            │
│  (per-county status)     │  (channel conversion)            │
├──────────────────────────┴──────────────────────────────────┤
│  CASE TABLE: All active cases with status, amounts, actions │
├─────────────────────────────────────────────────────────────┤
│  FOUNDER ACTION QUEUE: Items needing attention              │
└─────────────────────────────────────────────────────────────┘
```

---

## Leading Indicators (Predict Future Revenue)

| Metric | Definition | Target | Frequency |
|--------|-----------|--------|-----------|
| New leads/week | Raw surplus records ingested | 50+ | Weekly |
| Qualified leads/week | Leads passing score threshold | 25+ | Weekly |
| Enriched leads/week | Leads with valid contact info | 15+ | Weekly |
| Outreach sent/week | Mail + SMS + email touches | 50+ | Weekly |
| Response rate | Responses / outreach sent | >5% | Rolling 30-day |
| Interested rate | Interested / responded | >30% | Rolling 30-day |
| Pipeline value | Sum of surplus × fee % for all active leads | $50K+ | Real-time |
| Weighted pipeline | Pipeline value × stage probability | Track trend | Real-time |

---

## Lagging Indicators (Measure Results)

| Metric | Definition | Target | Frequency |
|--------|-----------|--------|-----------|
| Agreements signed/month | New signed clients | 2-4 | Monthly |
| Claims filed/month | Claims submitted to counties | 2-4 | Monthly |
| Recoveries/month | Successful disbursements received | 1-2 | Monthly |
| Revenue/month | Fees earned from recoveries | $5,000+ | Monthly |
| Avg revenue per case | Total revenue / total recoveries | $3,000+ | Rolling |
| Avg days to payout | Filing date → disbursement date | <120 days | Rolling |
| End-to-end conversion | Signed / raw leads | >1% | Rolling 90-day |
| Revenue per lead | Revenue / raw leads processed | >$20 | Rolling 90-day |

---

## Operational KPIs

| Metric | Definition | Healthy Range | Alert Threshold |
|--------|-----------|--------------|----------------|
| Source uptime | % of source checks that succeed | >95% | <90% |
| Parse success rate | % of records successfully parsed | >90% | <80% |
| Enrichment hit rate | % of leads with contact found | >50% | <30% |
| Mail delivery rate | % of mail delivered (Lob) | >95% | <90% |
| SMS delivery rate | % of SMS delivered (Twilio) | >95% | <90% |
| System error rate | Errors / total operations | <2% | >5% |
| Avg processing time | Source check → outreach ready | <24 hrs | >48 hrs |

---

## Source KPIs (Per County)

| Metric | Definition |
|--------|-----------|
| Last check timestamp | When was this source last successfully checked? |
| Records found (last check) | How many new records in the latest pull? |
| Records found (30-day) | Total new records in last 30 days |
| Avg surplus amount | Average surplus for this county's records |
| Parse success rate | % of records that parsed cleanly |
| Source status | Active / Error / Down / Stale |

---

## Funnel KPIs

| Stage | Count | Conversion to Next | Avg Time in Stage |
|-------|-------|-------------------|-------------------|
| Raw Leads | Total | → Qualified % | Hours |
| Qualified | Total | → Enriched % | Hours |
| Enriched | Total | → Contacted % | Hours |
| Contacted | Total | → Responded % | Days |
| Responded | Total | → Interested % | Days |
| Interested | Total | → Signed % | Days |
| Signed | Total | → Filed % | Days |
| Filed | Total | → Approved % | Weeks |
| Approved | Total | → Paid % | Weeks |

---

## Conversion KPIs

| Metric | Formula | Target |
|--------|---------|--------|
| Qualification rate | Qualified / Raw | >40% |
| Enrichment rate | Contactable / Qualified | >50% |
| Contact rate | Reached / Contacted | >15% |
| Interest rate | Interested / Reached | >30% |
| Close rate | Signed / Interested | >40% |
| Filing rate | Filed / Signed | >90% |
| Approval rate | Approved / Filed | >75% |
| Collection rate | Paid / Approved | >95% |

---

## Payout KPIs

| Metric | Definition |
|--------|-----------|
| Pending payouts | Count + total value of approved-but-not-yet-disbursed cases |
| Avg payout cycle | Days from filing → disbursement |
| Payout by county | Breakdown of disbursement timing per county |
| Fee collected MTD | Total fees collected this month |
| Client payouts MTD | Total paid to clients this month |
| Outstanding receivables | Approved cases awaiting disbursement (value) |

---

## Failure-Mode KPIs

| Metric | Definition | Action When Triggered |
|--------|-----------|---------------------|
| Source failures (consecutive) | 3+ failures on same source | Alert founder, check county site |
| Parse failure spike | >20% parse failures in a batch | Alert, review PDF format change |
| Enrichment failure spike | >70% enrichment failures | Check API key/credits, try backup |
| Outreach bounce rate | >10% mail/SMS bounce | Review address quality, NCOA check |
| Claim denial rate | >25% of filed claims denied | Review filing quality, county requirements |
| Stalled cases | Cases with no status change in 90+ days | Alert founder, call county |
| Zero leads (7 days) | No new leads ingested for a week | Source may be down, check immediately |

---

## Dashboard Implementation Notes

### MVP Dashboard (Week 1)
- Supabase table views with basic filters
- Manual SQL queries for KPIs
- Simple counts visible in Supabase dashboard

### V2 Dashboard (Month 2)
- Next.js app on Vercel
- Read from Supabase via API
- Real-time funnel visualization
- Case management table with inline actions
- Founder action queue

### V3 Dashboard (Month 4+)
- Charts and trend lines
- Automated alerts via SMS/email
- Revenue forecasting
- County comparison views

---

## Dependency Map

```
docs/kpi-dashboard-spec.md
  ↓ feeds
apps/dashboard/                (UI implementation)
schemas/core-data-model.md     (tables must support these queries)
services/notifications/        (alert triggers from KPIs)
```
