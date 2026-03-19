# SOP Teaching System

## Purpose

Teach the founder (and future team members) how the surplus funds recovery business works, in plain operator language. No jargon unless defined. No assumptions about prior knowledge.

---

## Chapter 1: How This Business Works

### The Simple Version

1. When a house gets sold at a foreclosure auction or tax sale, sometimes the sale price is more than what was owed
2. That extra money — the "surplus" — gets held by the county
3. The county doesn't actively try to find the person who's owed the money
4. We find those people, tell them their money exists, and handle the paperwork to get it back
5. We earn a percentage of whatever we recover — typically 25-35%

### The Money Flow

```
Property sold at auction → Sale price exceeds debt
  → County holds the excess ("surplus funds")
    → We find the surplus on public lists
      → We identify the rightful owner
        → We contact them and explain
          → They sign an agreement
            → We file a claim with the county
              → County approves and sends the money
                → We take our fee and send the rest to the client
```

### Real Example

- **Property:** 123 Oak Street, Fort Lauderdale, FL
- **Sold at:** Mortgage foreclosure auction
- **Sale price:** $285,000
- **Amount owed (mortgage + costs):** $210,000
- **Surplus:** $75,000
- **Held by:** Broward County Clerk of Courts
- **Former owner:** John Smith (claimant)
- **Our fee (30%):** $22,500
- **Client receives:** $52,500
- **Client's effort:** Sign some papers, provide ID

---

## Chapter 2: How Cases Move Through the System

### The Pipeline

Every lead goes through these stages:

```
RAW LEAD → QUALIFIED → ENRICHED → CONTACTED → RESPONDED →
INTERESTED → SIGNED → DOCS COLLECTED → CLAIM FILED →
UNDER REVIEW → APPROVED → MONEY RECEIVED → CLOSED
```

### What Happens at Each Stage

| Stage | What Happens | Who Does It | How Long |
|-------|-------------|-------------|----------|
| Raw Lead | Surplus record found on county list | System (auto) | Minutes |
| Qualified | Checked: amount > $1K, claimant identifiable | System (auto) | Minutes |
| Enriched | Found claimant's phone/email/address | System (auto) | Hours |
| Contacted | Mail/SMS/email sent | System (auto) | Same day |
| Responded | Claimant replied or called back | System detects | 1-3 weeks |
| Interested | Claimant wants to proceed | Founder confirms | 1 day |
| Signed | Agreement signed, intake form completed | Client + system | 1-3 days |
| Docs Collected | ID, notarized affidavit, all forms in | Client + founder | 1-7 days |
| Claim Filed | Packet submitted to county | System + founder review | 1-2 days |
| Under Review | County processing the claim | Waiting | 30-120 days |
| Approved | County approved the claim | County | — |
| Money Received | Check arrives or wire sent | Founder | 1-2 weeks |
| Closed | Fee collected, client paid, case done | Founder | 1 day |

---

## Chapter 3: Differences by Market/Process Type

### Foreclosure Surplus vs Tax Sale Overages

| | Foreclosure Surplus | Tax Sale Overages |
|--|-------------------|-------------------|
| **What caused it** | Mortgage foreclosure auction | Tax delinquency auction |
| **Who holds the money** | Circuit court clerk | County treasurer or tax collector |
| **Typical amount** | $5,000 - $100,000+ | $500 - $20,000 |
| **Who gets paid** | Former homeowner (usually) | Former property owner |
| **Competing claims** | Junior lienholders may have priority | Less common |
| **Filing method** | Court motion or clerk claim | Administrative claim (usually simpler) |
| **Attorney needed?** | Sometimes (court motions) | Rarely |
| **How long to get paid** | 60-180 days | 30-90 days |

### Florida-Specific Notes

- **Foreclosure surplus:** Florida Statute §45.032-45.033. Funds held by clerk of circuit court. Former owner has superior right unless junior liens exist.
- **Tax deed surplus:** Florida Statute §197.582. After tax deed sale, excess over taxes+costs goes to former owner. Claim filed with clerk.
- **No fee cap:** Florida does not cap recovery agent fees (unlike Texas at 10%).
- **Judicial foreclosure state:** All foreclosures go through court, meaning better records.

### County Differences

Even within Florida, counties differ:
- Different clerk websites and data formats
- Different forms required
- Different processing times
- Different internal procedures
- Same underlying statutes, but different local practices

**Key lesson:** Build county-specific knowledge. Don't assume what works in Broward works identically in Hillsborough.

---

## Chapter 4: How the Automation Works

### What the System Does Automatically

```
Morning (6 AM):
  → Checks county websites for new surplus lists
  → Downloads new files
  → Parses data from PDFs/HTML
  → Creates new lead records in database
  → Scores each lead
  → Enriches top leads (finds contact info)
  → Generates outreach (letters, SMS, emails)
  → Queues mail for sending via Lob
  → Sends scheduled SMS follow-ups
  → Sends scheduled email follow-ups
  → Logs everything

When someone responds:
  → System detects response (inbound SMS, email, form submission)
  → Categorizes: interested / not interested / wrong number / etc.
  → If interested → sends intake form link automatically
  → Notifies founder of hot lead

When someone signs:
  → System creates case record
  → Generates claim packet from templates
  → Queues for founder review
  → Sends founder notification

After founder approves claim:
  → System mails claim packet
  → Sets follow-up reminders
  → Tracks status
```

### What the Founder Does

- Review hot leads and make phone calls (high-value)
- Review and approve claim packets before filing
- Handle claimant questions that need a human
- Deposit and distribute recovery checks
- Weekly: 15-minute pipeline review

### What the System Can't Do

- Build trust on a phone call (humans only)
- Sign notarized documents (notary required)
- Interact with some county portals (CAPTCHAs, manual login)
- Make legal judgment calls (attorney for complex cases)
- Deposit physical checks (founder must visit bank or use mobile deposit)

---

## Chapter 5: How to Troubleshoot

### Common Issues and Fixes

| Problem | Likely Cause | Fix |
|---------|-------------|-----|
| No new leads coming in | County source changed URL or format | Check source URL manually, update scraper config |
| PDF parsing errors | County changed their PDF layout | Review PDF, update parser template |
| Low enrichment hit rate | Names are too common or addresses are old | Try alternate enrichment providers, manual lookup |
| Low response rate | Messaging isn't landing, or letters not delivered | Review message templates, check Lob delivery reports |
| Claimant says "not me" | Wrong person identified (common name) | Verify with property records, apologize and remove |
| County rejects claim | Missing document or incorrect form | Review rejection reason, fix and refile |
| System not sending outreach | Cron job failed or API key expired | Check Railway logs, verify API keys |

### How to Check System Health

1. **Dashboard:** View pipeline counts — are leads flowing?
2. **Supabase:** Check raw_records table — new entries today?
3. **Railway logs:** Check for errors in cron jobs
4. **Lob dashboard:** Check mail delivery status
5. **Twilio dashboard:** Check SMS delivery status
6. **Sentry:** Check for any error alerts

---

## Chapter 6: How to Improve Over Time

### Metrics to Watch

| Metric | What It Tells You | Action If Bad |
|--------|-------------------|---------------|
| Leads/week | Is the pipeline fed? | Add counties, check sources |
| Enrichment hit rate | Can we find people? | Try new providers |
| Response rate | Is outreach working? | Change messaging, timing, channels |
| Sign rate (of interested) | Are we closing? | Improve phone script, trust elements |
| Recovery rate (of filed) | Are claims succeeding? | Review filing quality, county requirements |
| Avg days to payout | Cash flow health | Prioritize faster counties |
| Revenue per case | Unit economics | Focus on higher-value cases |

### Improvement Cycle

```
Every month:
1. Review all metrics
2. Identify weakest funnel stage
3. Make one change to improve it
4. Measure for 2-4 weeks
5. Keep or revert
6. Repeat
```

### Adding New Counties

When adding a new county:
1. Find the surplus list source URL
2. Determine data format (PDF/HTML/portal)
3. Write or adapt a parser
4. Create county-specific filing template
5. Test with 10 leads end-to-end
6. Add to regular monitoring schedule

### Adding New States

When adding a new state:
1. Research state statutes for surplus fund claims
2. Check for fee caps (dealbreaker if <20%)
3. Identify top 3 counties by volume
4. Validate data accessibility
5. Create state-specific agreement and filing templates
6. Consult attorney if state requirements are complex
7. Test with one county before expanding
