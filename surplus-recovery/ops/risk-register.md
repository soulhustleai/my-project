# Risk Register

## Risk Scoring

- **Likelihood:** 1 (Rare) → 5 (Almost Certain)
- **Impact:** 1 (Negligible) → 5 (Critical)
- **Risk Score:** Likelihood × Impact (max 25)

---

## Legal Risks

| ID | Risk | Likelihood | Impact | Score | Mitigation |
|----|------|-----------|--------|-------|------------|
| L-01 | State introduces fee cap in FL | 2 | 5 | 10 | Monitor legislation; diversify to multiple states. If passed, adjust fee structure or exit state. |
| L-02 | Unauthorized practice of law claim | 2 | 4 | 8 | Never provide legal advice. Use "recovery agent" framing. Partner with attorney for court motions. Clearly disclaim legal advice in all agreements. |
| L-03 | TCPA violation (SMS/phone) | 3 | 4 | 12 | Strict opt-in/opt-out. Honor STOP requests immediately. Don't use auto-dialers for cold calls. Keep records of all outreach. |
| L-04 | State solicitation regulation violation | 2 | 3 | 6 | Research each state's specific rules before entering. Some states require specific disclosures in recovery agent agreements. |
| L-05 | Agreement enforceability challenged | 2 | 3 | 6 | Have attorney review agreement template. Include clear fee terms, cancellation clause, and dispute resolution. |
| L-06 | Data privacy violation (PII handling) | 2 | 4 | 8 | Encrypt PII at rest and in transit. Minimize PII retention. Use Supabase RLS. Don't expose PII in logs. |

---

## Data Quality Risks

| ID | Risk | Likelihood | Impact | Score | Mitigation |
|----|------|-----------|--------|-------|------------|
| D-01 | County changes surplus list format | 4 | 3 | 12 | Source-specific parsers. Health monitoring alerts on parse failures. Fallback to Claude API for unexpected formats. |
| D-02 | Surplus amounts on list are inaccurate | 3 | 3 | 9 | Cross-reference with court records when possible. Disclose "estimated" amounts in outreach. |
| D-03 | Wrong person identified as claimant | 3 | 4 | 12 | Verify with property records. Require ID during intake. Use multiple data points for matching. Always verify before filing. |
| D-04 | Duplicate outreach to same person | 3 | 3 | 9 | Deduplication by name + address + case number. Check before every outreach send. |
| D-05 | Stale contact info (moved, changed number) | 4 | 2 | 8 | NCOA validation on addresses. Multi-channel outreach. Address validation via Lob. |

---

## Website / Anti-Bot Risks

| ID | Risk | Likelihood | Impact | Score | Mitigation |
|----|------|-----------|--------|-------|------------|
| W-01 | County site blocks scraper (CAPTCHA, IP ban) | 3 | 3 | 9 | Residential proxies (Apify/Bright Data). Respect rate limits. Rotate user agents. Manual fallback. |
| W-02 | County site redesigns / URL changes | 4 | 3 | 12 | Source health monitoring. Alert on failures. Modular scrapers that are quick to update. |
| W-03 | County adds terms of service prohibiting scraping | 2 | 3 | 6 | Surplus lists are public records. Use open records requests as fallback. Prefer downloading public documents over scraping portal data. |
| W-04 | Source goes offline temporarily | 3 | 2 | 6 | Retry logic with backoff. Alert after 3 consecutive failures. Process backlog when source returns. |

---

## Contact Data Risks

| ID | Risk | Likelihood | Impact | Score | Mitigation |
|----|------|-----------|--------|-------|------------|
| C-01 | Low enrichment hit rate (<30%) | 3 | 4 | 12 | Multi-provider enrichment chain (PDL → Whitepages → manual). Budget for lower hit rates. |
| C-02 | Enrichment provider raises prices or shuts down | 2 | 3 | 6 | Use abstraction layer. Multiple providers integrated. Can switch without code rewrite. |
| C-03 | Skip tracing returns wrong person (common name) | 3 | 3 | 9 | Verify match with property address, age, and other identifiers. Flag low-confidence matches for manual review. |

---

## Claimant Conversion Risks

| ID | Risk | Likelihood | Impact | Score | Mitigation |
|----|------|-----------|--------|-------|------------|
| V-01 | Low response rate (<2%) | 3 | 4 | 12 | Multi-touch, multi-channel sequence. Test and iterate messaging. Speed-to-contact matters — send within days of list publication. |
| V-02 | High "this is a scam" perception | 4 | 3 | 12 | Professional presentation. County verification language. BBB listing. Website. No-upfront-cost emphasis. Specific case details prove legitimacy. |
| V-03 | Competitor contacts claimant first | 3 | 3 | 9 | Speed. Monitor sources daily or more. Send outreach within 48 hours of list publication. |
| V-04 | Claimant hires attorney instead | 2 | 3 | 6 | Emphasize simplicity of our service. Competitive fee. Some claimants will go to attorneys — accept this as funnel loss. |
| V-05 | Claimant files on their own | 2 | 2 | 4 | Happens, but rare. Most people want help with paperwork. Not preventable or worth worrying about. |

---

## Operational Fragility Risks

| ID | Risk | Likelihood | Impact | Score | Mitigation |
|----|------|-----------|--------|-------|------------|
| O-01 | Single point of failure (founder) | 4 | 4 | 16 | Automation reduces dependency. Document all processes. SOPs enable VA/contractor backup. |
| O-02 | Cash flow gap (long payout cycles) | 4 | 3 | 12 | Build pipeline volume to smooth revenue. Track expected payout timing. Edwin has W2 income as buffer. |
| O-03 | Claim denied for wrong filing | 2 | 3 | 6 | County-specific templates. Checklist validation before filing. Founder review of first 5 claims per county. |
| O-04 | System downtime / data loss | 2 | 5 | 10 | Supabase handles backups. Code in git. Railway auto-restarts. Sentry monitoring. |
| O-05 | Outreach marked as spam by mail carriers | 2 | 3 | 6 | Professional formatting. Real return address. Avoid spam trigger words. Lob handles deliverability. |

---

## Vendor / Tooling Risks

| ID | Risk | Likelihood | Impact | Score | Mitigation |
|----|------|-----------|--------|-------|------------|
| T-01 | Lob API downtime | 2 | 2 | 4 | Queue mail, retry. Manual USPS fallback for urgent items. |
| T-02 | Twilio deliverability issues | 2 | 2 | 4 | 10DLC registration (Edwin already familiar). Backup number. |
| T-03 | Supabase free tier limits reached | 3 | 2 | 6 | Upgrade to $25/mo plan. Clean up unused data. |
| T-04 | Claude API pricing increase | 2 | 2 | 4 | Haiku is already cheap. Can switch to OpenAI for classification tasks. |
| T-05 | People Data Labs API changes | 2 | 2 | 4 | Abstraction layer. Multiple enrichment providers. |

---

## Top 5 Risks by Score

| Rank | ID | Risk | Score | Priority Mitigation |
|------|-----|------|-------|-------------------|
| 1 | O-01 | Single point of failure (founder) | 16 | Automate aggressively, document everything |
| 2 | L-03 | TCPA violation | 12 | Strict compliance protocol |
| 3 | D-01 | County format changes | 12 | Source health monitoring, modular parsers |
| 4 | D-03 | Wrong person identified | 12 | Multi-point verification |
| 5 | V-01 | Low response rate | 12 | Multi-channel, speed, iterate messaging |
| 5 | V-02 | Scam perception | 12 | Professional presentation, verification |
| 5 | C-01 | Low enrichment hit rate | 12 | Multi-provider chain |
| 5 | O-02 | Cash flow gap | 12 | Pipeline volume, W2 buffer |
