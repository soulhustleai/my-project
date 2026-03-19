# First Deal Playbook

## Objective

Sign the first claimant and file the first claim within 45 days of launch. This playbook is the daily operating system until that happens.

---

## First Target Markets

| Priority | County | State | Type | Why |
|----------|--------|-------|------|-----|
| 1 | Broward | FL | Tax deed surplus + foreclosure | High volume, good amounts, accessible data |
| 2 | Palm Beach | FL | Tax deed surplus + foreclosure | High avg amounts, adjacent to Broward |
| 3 | Hillsborough | FL | Tax deed surplus + foreclosure | Less competition than South FL |

---

## First Target Sources

### Broward County, FL
- **Clerk of Courts:** https://www.browardclerk.org
- **Surplus list location:** Court registry surplus funds page
- **Format:** PDF list of cases with surplus
- **Update frequency:** After foreclosure sales (monthly+)

### Palm Beach County, FL
- **Clerk & Comptroller:** https://www.mypalmbeachclerk.com
- **Surplus list location:** Surplus funds / registry of court page
- **Format:** PDF or searchable database
- **Update frequency:** Periodic

### Hillsborough County, FL
- **Clerk of Courts:** https://www.hillsclerk.com
- **Surplus list location:** Surplus funds page
- **Format:** PDF
- **Update frequency:** After sales

**VALIDATION TASK:** Confirm exact URLs, formats, and access methods for each source before first scrape.

---

## Daily Lead Generation Loop

### Automated (after Week 2)
```
6:00 AM  — Source monitor checks all 3 county sources
6:30 AM  — New lists downloaded, parsed, normalized
7:00 AM  — New opportunities scored and queued for enrichment
8:00 AM  — Enrichment runs on top-scored leads
9:00 AM  — Outreach generated for contactable leads
10:00 AM — Mail batch sent via Lob
```

### Manual (Week 1-2, while building automation)
```
Morning: Check each county clerk website for new surplus lists
Download any new lists
Manually enter top 10 leads into Supabase
Manually skip trace top leads (TruePeopleSearch)
Queue outreach for contactable leads
```

---

## Qualification Rubric

Score each lead 1-5 on each factor. Minimum total score of 12 to pursue.

| Factor | 1 (Poor) | 3 (Average) | 5 (Excellent) | Weight |
|--------|----------|-------------|----------------|--------|
| Surplus Amount | <$1,000 | $3,000-$10,000 | >$15,000 | 3x |
| Claimant Identifiable | Name unclear/entity | Partial name | Full name + address | 2x |
| Contactable | No info found | Address only | Phone + email + address | 2x |
| Recency | >2 years ago | 6-24 months | <6 months | 1x |
| Filing Simplicity | Attorney required | Standard process | Simple admin claim | 1x |

**Minimum score to pursue: 12/25**
**Priority leads: 18+/25**

---

## Claimant Discovery Workflow

```
1. Get owner/defendant name from surplus record
2. Cross-reference with property records (county property appraiser)
3. Search TruePeopleSearch for current contact info
4. If not found → People Data Labs API lookup
5. If still not found → BeenVerified or manual search
6. If found → verify address is current (USPS NCOA check via Lob)
7. Score contactability confidence (high/medium/low)
8. Route: high → immediate outreach; medium → outreach with caution; low → skip or manual
```

---

## Outreach Plan

### Channel Sequence (7-touch, 30 days)

| Day | Channel | Action |
|-----|---------|--------|
| 1 | **Direct Mail** | Personalized letter via Lob |
| 5 | **SMS** | Follow-up text referencing the letter |
| 8 | **Email** | If email available, send follow-up |
| 12 | **Direct Mail #2** | Second letter (different angle) |
| 16 | **SMS #2** | "Just checking if you received our letter" |
| 21 | **Phone Call** | For leads >$10K surplus (founder or VA) |
| 30 | **Final Mail** | "Last notice" urgency letter |

### Why Mail First
- Highest trust signal for "you have unclaimed money" messaging
- Not immediately dismissed as spam like email/SMS
- Physical presence (sits on counter, gets discussed with family)
- Required for some compliance standards

---

## Trust-Building Messaging

### Core Message Framework
1. **Specific:** Reference their actual property address, county, and approximate amount
2. **Verifiable:** Tell them how to verify independently with the county
3. **Risk-free:** Emphasize no upfront cost
4. **Professional:** Business letterhead, real address, real phone number
5. **Simple:** Explain in 3 sentences what happened and what you do

### Key Trust Phrases
- "The [County] Clerk of Courts is currently holding surplus funds from the sale of your former property at [address]."
- "You can verify this directly with the clerk's office at [phone number]."
- "Our service is free unless we successfully recover your funds."
- "We handle all the paperwork — you just need to sign and provide identification."

---

## Outreach Templates

### Direct Mail — Letter 1

```
[Business Letterhead]
[Date]

[Claimant Name]
[Claimant Address]

RE: Unclaimed Surplus Funds — [Property Address]
Case/Reference: [Case Number]
Estimated Amount: $[Amount]

Dear [First Name],

I'm writing because [County] County is currently holding surplus funds
from the sale of your former property at [Property Address]. Based on
public records, the estimated surplus is approximately $[Amount].

Many former property owners don't know these funds exist, and the county
won't seek you out. If unclaimed, these funds may eventually be
transferred to the state's unclaimed property division.

We specialize in recovering surplus funds on behalf of rightful
claimants. Our service costs you nothing upfront — we only earn a fee
if we successfully recover your money.

You can verify these funds exist by contacting the [County] Clerk of
Courts at [Phone Number] and referencing case [Case Number].

If you'd like to learn more or begin the recovery process, please:
- Call us at [Phone Number]
- Text "CLAIM" to [Phone Number]
- Visit [Website URL]

Sincerely,

[Business Name]
[Phone Number]
[Email]
[Website]
[Business Address]
```

### SMS — Follow-up (Day 5)

```
Hi [First Name], this is [Name] from [Business]. We sent you a letter
about surplus funds (~$[Amount]) from the sale of your property at
[Short Address]. You can verify with [County] Clerk at [Phone]. Would
you like to learn more? Reply YES or call us at [Phone]. Reply STOP
to opt out.
```

### Email — Follow-up (Day 8)

```
Subject: $[Amount] in surplus funds from [Property Address]

Hi [First Name],

I recently sent you a letter regarding surplus funds being held by
[County] County from the sale of your property at [Property Address].

The estimated amount is approximately $[Amount], and these funds
belong to you.

I wanted to follow up in case the letter didn't reach you. You can
verify these funds by contacting the [County] Clerk at [Phone].

Our recovery service is completely free unless we successfully recover
your money. We handle all the paperwork.

Would you like to learn more? Just reply to this email or call me at
[Phone].

Best,
[Name]
[Business Name]
```

---

## Objection Handling

| Objection | Response |
|-----------|----------|
| "This sounds like a scam" | "I completely understand the skepticism. You can verify these funds exist by calling the [County] Clerk at [phone number] and referencing case [number]. We're a registered business — here's our website and business registration. You pay nothing unless we recover your money." |
| "Why can't I do this myself?" | "You absolutely can. The process involves filing the right paperwork with the county, providing notarized documents, and following up. If you'd prefer to handle it yourself, I can point you to the clerk's office. Most people prefer to have someone handle the paperwork for them." |
| "What's your fee?" | "Our fee is [X]% of the recovered amount, and only if we successfully recover your funds. You pay nothing upfront and nothing if we're unsuccessful." |
| "How long does it take?" | "Typically 60-120 days from filing to receiving funds, depending on the county's processing time." |
| "How did you find me?" | "Surplus funds from property sales are public record. We review these records to identify people who may be owed money and help them recover it." |
| "I need to think about it" | "Of course. I'll follow up in a week. In the meantime, you can verify the funds exist by calling the clerk at [phone]. Here's my direct number if you have any questions." |

---

## Intake and Signature Flow

```
1. Claimant agrees to proceed (phone/text/email)
2. Send intake link (Jotform) via SMS + email
3. Form collects:
   - Full legal name
   - Date of birth
   - Current address
   - Phone + email
   - Government ID upload
   - Connection to property (were you the owner? heir?)
   - E-signature on contingency agreement
4. System receives submission → creates case in Supabase
5. If notarization needed → send RON link or mobile notary instructions
6. Follow up within 24 hrs if form incomplete
7. Once all docs received → status → DOCS_COMPLETE
```

---

## Claim Prep and Submission Flow

```
1. Case status: DOCS_COMPLETE
2. Generate claim packet from county-specific template:
   - Cover letter to clerk/court
   - Claim form (county-specific)
   - Copy of claimant ID
   - Notarized affidavit
   - Contingency agreement (if required by county)
   - Power of Attorney (if required)
   - W-9
   - Any county-specific supplemental forms
3. Founder reviews packet (5-10 min)
4. Submit via best available method:
   - Mail: Print and send (Lob or manual)
   - Portal: Upload if county allows
   - In-person: Only if required (founder escalation)
5. Log submission in Supabase with tracking number
6. Set follow-up reminder for 30 days
```

---

## Daily/Weekly Priorities Until First Signed Client

### Daily (30-60 min)
- [ ] Check for new surplus lists on 3 county sources
- [ ] Process any new leads (parse, score, enrich)
- [ ] Send outreach for new contactable leads
- [ ] Check for responses (calls, texts, emails)
- [ ] Follow up with any warm leads
- [ ] Log all activity in Supabase

### Weekly (2-3 hrs)
- [ ] Review full pipeline: leads → contacted → responded → interested
- [ ] Adjust outreach messaging based on response patterns
- [ ] Check for new surplus list publications
- [ ] Review automation — fix any broken scrapes or failed sends
- [ ] Update KPIs: leads generated, outreach sent, responses, pipeline value

### Weekly Targets

| Week | Leads Ingested | Outreach Sent | Responses | Goal |
|------|---------------|---------------|-----------|------|
| 1 | 25+ | 0 (building) | 0 | Setup complete |
| 2 | 50+ | 25+ | 0 | First outreach wave |
| 3 | 75+ | 50+ | 2-5 | First responses |
| 4 | 100+ | 75+ | 5-10 | First conversations |
| 5-6 | 100+ | 100+ | 10+ | **First signed client** |
