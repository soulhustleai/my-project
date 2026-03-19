# Executive Summary — Surplus Funds Recovery Agency

## What This Business Is

A surplus funds recovery operation that identifies unclaimed excess proceeds from foreclosure sales, tax sales, and other forced property sales — then locates the rightful claimant, secures authorization, prepares the claim, and collects a contingency fee upon successful recovery.

When a property is sold at a foreclosure or tax sale for more than the debt owed, the excess ("surplus" or "overage") is held by the county clerk, court, or treasury. Many rightful owners never learn this money exists. This business finds them, contacts them, earns their trust, and handles the paperwork for a percentage of recovered funds.

---

## How the Money Is Made

- **Fee model:** Contingency fee — typically 25-35% of recovered surplus funds
- **Average surplus amount:** $5,000-$50,000+ per case (varies wildly by county/state)
- **Revenue per case:** $1,250-$17,500+ at 25-35%
- **No upfront cost to claimant** — the fee is earned only on successful recovery
- **Payment timing:** After the county/court disburses funds (30-180 days typical, some longer)

### Revenue Math to $5K/Month

| Scenario | Avg Recovery | Fee % | Revenue/Case | Cases/Month |
|----------|-------------|-------|-------------|-------------|
| Conservative | $10,000 | 30% | $3,000 | 2 |
| Moderate | $20,000 | 30% | $6,000 | 1 |
| Aggressive | $40,000 | 25% | $10,000 | 1 |

**Reality:** At 1-2 successful recoveries per month at moderate case sizes, $5K/month is achievable. The bottleneck is pipeline build time — expect 60-120 days from first outreach to first payout.

---

## What Is Truly Automatable Now

| Step | Automation Level | Notes |
|------|-----------------|-------|
| Source monitoring (county surplus lists) | 80-90% | Most counties publish lists; formats vary |
| Data ingestion & normalization | 70-80% | Parseable with targeted scrapers per source |
| Opportunity identification & scoring | 85-90% | Rules + LLM-based extraction |
| Claimant discovery (name → person) | 70-80% | Skip tracing APIs + public records |
| Contact enrichment (phone, email, address) | 75-85% | Multiple enrichment vendors |
| Initial outreach (email, SMS, mail) | 80-90% | Templates + CRM automation |
| Follow-up sequences | 90%+ | Fully automatable drip campaigns |
| Intake form collection | 85-90% | E-forms with e-sign |
| Agreement/contract generation | 85-90% | Template-driven doc generation |
| Claim packet preparation | 60-70% | County-specific; requires templates per county |
| Claim submission | 20-40% | Many counties require physical mail or in-person |
| Case status tracking | 50-70% | Some counties have online portals; many don't |
| Payout collection | 10-20% | Checks mailed, wire setup varies |

---

## What Is NOT Fully Automatable

1. **Claim submission** — Many counties require notarized documents, physical mail, or in-person filing
2. **Attorney involvement** — Some states require attorney representation for claims above certain thresholds
3. **Notarization** — Required in most jurisdictions; remote online notarization (RON) helps but isn't universal
4. **Trust-building phone calls** — High-value claimants often need a human conversation before signing
5. **County portal interactions** — Some portals require manual login, CAPTCHA, or specific browser workflows
6. **Legal judgment calls** — Priority of claims, lien disputes, probate situations
7. **Payment receipt** — Physical checks, wire coordination

---

## Recommended Path to First Signed Client

### Week 1-2: Setup & First Leads
1. Register business entity (LLC)
2. Set up CRM (Airtable or Supabase)
3. Target 2-3 high-volume Florida counties (Miami-Dade, Broward, Palm Beach)
4. Manually pull surplus lists from county clerk websites
5. Build first batch of 20-50 qualified leads
6. Enrich with skip tracing (TruePeopleSearch free tier → paid vendor for scale)

### Week 3-4: First Outreach
7. Send first outreach batch (mail + email + SMS)
8. Follow up aggressively (5-7 touch sequence over 21 days)
9. Handle inbound responses
10. Close first signed agreement

### Target: First signed client within 30-45 days of launch

---

## Recommended Path to $5K/Month

1. **Month 1:** Manual pipeline — 3 counties, 100+ leads, first outreach wave
2. **Month 2:** First signed clients, claim prep begins, expand to 5-7 counties
3. **Month 3:** First claims submitted, pipeline flowing, automation replacing manual steps
4. **Month 4-5:** First payouts arrive, system stabilizing, 200-500 leads/month
5. **Month 6:** $5K/month achievable with consistent 1-2 recoveries/month

### Critical Success Factors
- **Volume:** More leads = more signed clients = more revenue. The funnel is wide at top, narrow at bottom
- **Speed:** Faster outreach after list publication = higher conversion (competition is real)
- **Trust:** Professional, compliant outreach that doesn't feel like a scam
- **County selection:** Focus on counties with accessible data, reasonable filing processes, and good surplus volumes
- **Follow-through:** Most operators fail at the paperwork stage. Completing claims correctly is the moat

---

## Strategic Position

This business complements Edwin's existing operations:
- **SoulHustleAI** — The automation infrastructure being built here can become a case study and future product offering
- **GOD MODE CREDIT** — The claimant audience overlaps with credit-rebuilding customers (people who lost homes to foreclosure)
- **Weekend operator model** — Once automated, this requires 5-10 hrs/week of founder time, fitting Edwin's W2 + side business model

---

## Key Risks

1. **Cash flow lag:** 60-180 days from signed client to payout
2. **Competition:** Growing niche with increasing operator count in popular counties
3. **Data quality:** County lists are messy, incomplete, and inconsistent
4. **Conversion:** Claimants are skeptical of "you have unclaimed money" outreach
5. **Legal variation:** Rules differ by state and county; some require attorney involvement
6. **Anti-bot:** County websites may block automated access

---

## Bottom Line

This is a real, proven business model with strong unit economics. The moat is operational: finding leads fast, contacting claimants professionally, and completing paperwork correctly. Automation dramatically reduces the labor per case, making it viable as a lean operation. The path to first revenue is clear — it requires execution, not innovation.
