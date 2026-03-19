# Autonomy Roadmap

## Purpose

Map the path from current state (mostly manual) to maximum realistic automation. Three stages: 50%, 75%, 90%.

---

## Stage 1: 50% Automation (Month 1-2)

### What's Automated
- Source monitoring and list downloading
- PDF parsing and record creation
- Lead scoring
- Basic skip tracing (API-based enrichment)
- Mail outreach generation and sending (Lob)
- SMS follow-up sequences (Twilio)
- Email follow-up sequences
- Intake form collection (Jotform)
- Audit logging

### What Remains Manual
- Enrichment for hard-to-find claimants
- All phone calls
- Complex response handling
- Walk-through intake (phone)
- Notarization coordination
- Claim packet review
- All claim submissions
- All case status tracking
- All payout processing
- County source URL maintenance

### Founder Time: ~8-10 hrs/week

### Blockers to Clear for Next Stage
- Build claim packet template library for 3 FL counties
- Integrate Lob for print-and-mail claim submissions
- Build dashboard for pipeline visibility
- Establish response classification system

---

## Stage 2: 75% Automation (Month 3-5)

### What's Added
- Automated claim packet generation from templates
- Automated claim submission via mail (Lob print + mail)
- Automated response classification (AI-powered)
- Automated inbound routing (interested → intake, declined → close)
- Dashboard with real-time pipeline view
- Automated follow-up scheduling
- Automated weekly pipeline report (emailed)
- County portal monitoring (where available)
- Multi-provider enrichment (fallback chain)
- Automated NCOA address validation

### What Remains Manual
- High-value phone calls (leads >$10K)
- Complex case handling (multiple claimants, probate)
- County portal submissions (where mail doesn't work)
- Notarization coordination
- Claim denial response / appeals
- Payout check deposit and disbursement
- Attorney coordination
- Source URL fixes when county sites change
- New county onboarding

### Founder Time: ~4-6 hrs/week

### Blockers to Clear for Next Stage
- Train VA on phone follow-ups
- Build AI response classifier with sufficient accuracy (>85%)
- Establish attorney network for complex cases
- Build county portal automation for top counties (if feasible)
- Remote online notarization integration

---

## Stage 3: 90% Automation (Month 6-12)

### What's Added
- VA handles phone follow-ups (script + training)
- AI-assisted response drafting (founder approves, not writes)
- Automated RON (remote online notarization) coordination
- Automated county portal submission (where technically possible)
- Automated case status polling (for counties with online portals)
- Automated payout calculation and client payment initiation
- Self-healing source monitors (detect + adapt to site changes)
- Auto-scaling outreach based on pipeline targets
- Predictive lead scoring (trained on real conversion data)
- Multi-state operation with state-specific workflow routing

### What Remains Manual (Likely Permanent)
- Identity verification calls (trust-building for large amounts)
- Physical check deposits
- Attorney consultations for complex/contested claims
- In-person county filings (rare but some require it)
- Business entity maintenance (LLC renewal, etc.)
- Strategy decisions (which counties to add, pricing changes)
- Edge cases the system can't classify
- Tax reporting and bookkeeping

### Founder Time: ~2-3 hrs/week

### Blockers to Clear
- Sufficient historical data to train predictive scoring
- VA hired and trained
- Attorney network established
- RON integration operational
- County portal automation feasible for target counties
- Self-healing scrapers (detect layout changes, auto-adjust)

---

## What Will Likely NEVER Be Fully Automated

| Task | Why |
|------|-----|
| High-trust phone conversations | Claimants need human connection for large sums |
| Physical check deposit/disbursement | Banking requires identity verification |
| In-person county filings | Some counties require physical presence |
| Attorney-required filings | Legal representation can't be automated away |
| Notarization (until RON is universal) | Legal identity verification requirement |
| Business entity maintenance | Government filings require human |
| Complex legal judgments | Lien priority, probate, contested claims |
| Tax reporting | Requires accountant/bookkeeper review |

---

## Automation Investment vs Return

| Investment | Cost | Time Savings | ROI |
|-----------|------|-------------|-----|
| Source monitoring automation | 2 days dev | 2 hrs/week saved | High — immediate |
| Outreach automation (Lob + Twilio) | 2 days dev | 3 hrs/week saved | High — immediate |
| Enrichment API integration | 1 day dev | 2 hrs/week saved | High — immediate |
| Claim packet template library | 3 days dev | 1 hr/case saved | High — per-case |
| Dashboard | 5 days dev | 1 hr/week saved | Medium — visibility value |
| AI response classification | 2 days dev | 1 hr/week saved | Medium — at volume |
| County portal automation | 5+ days/county | 30 min/submission | Low — high fragility |
| Self-healing scrapers | 10+ days dev | 1 hr/month saved | Low — until scale |

### Priority: Automate high-ROI items first. Leave low-ROI/high-fragility items for later.

---

## Dependency Map

```
docs/autonomy-roadmap.md
  ↓ feeds
ops/implementation-backlog.md   (prioritized tasks by automation stage)
docs/human-task-map.md          (task classification feeds this roadmap)
ops/launch-checklist.md         (what to ship for each stage)
```
