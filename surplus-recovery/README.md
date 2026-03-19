# Surplus Funds Recovery Agency

Automated surplus funds recovery operation. Finds unclaimed excess proceeds from foreclosure and tax sales, locates rightful claimants, handles outreach and paperwork, and earns a contingency fee on successful recovery.

## Architecture

```
County Sources → Source Monitor → Record Ingestion → Normalization → Scoring
    → Claimant Enrichment → Outreach → Intake/Signing → Claim Prep → Filing → Tracking → Payout
```

All data flows through **Supabase (Postgres)**. Services are Python scripts triggered by cron or manual execution.

## Quick Start

```bash
# 1. Copy env file and fill in values
cp .env.example .env

# 2. Set up Supabase — run scripts/setup_supabase.sql in Supabase SQL Editor

# 3. Install Python dependencies
pip install -r requirements.txt

# 4. Seed initial county sources
python scripts/seed_sources.py

# 5. Run the full pipeline
python scripts/run_pipeline.py
```

## Module Map

| Module | Purpose | Status |
|--------|---------|--------|
| services/source-monitor | Scrape county surplus lists | Scaffolded (needs source validation) |
| services/record-ingestion | Parse PDFs/HTML → structured records | Scaffolded |
| services/normalization | Dedupe and normalize records | Scaffolded |
| services/opportunity-engine | Score leads by value and actionability | Scaffolded |
| services/claimant-enrichment | Skip trace for contact info | Scaffolded |
| services/outreach-engine | Multi-channel outreach (mail, SMS, email) | Scaffolded |
| services/document-engine | Generate claim packets | Planned |
| services/submission-engine | File claims with counties | Planned |
| services/case-tracker | Monitor claim status | Planned |
| services/notifications | Founder alerts and escalations | Planned |
| apps/dashboard | Pipeline visibility UI | Planned |

## Launch Markets

**Primary:** Florida (Broward, Palm Beach, Hillsborough counties)
**Secondary:** Ohio (Cuyahoga, Franklin), Arizona (Maricopa)

## Tech Stack

- **Language:** Python (services), TypeScript (dashboard)
- **Database:** Supabase (Postgres)
- **Scraping:** Playwright
- **PDF Parsing:** pdfplumber + Claude API
- **Mail:** Lob API
- **SMS:** Twilio
- **Enrichment:** People Data Labs
- **Hosting:** Railway (services), Vercel (dashboard)
- **Monitoring:** Sentry

## Documentation

All strategy, research, and operational docs are in `docs/` and `ops/`. Start with:
- [Executive Summary](docs/executive-summary.md)
- [MVP Build Plan](docs/mvp-build-plan.md)
- [First Deal Playbook](docs/first-deal-playbook.md)
- [System Architecture](docs/system-architecture.md)

## Next Steps

1. Register LLC (founder action)
2. Validate county source URLs for 3 FL counties
3. Build and test first scraper (Broward County)
4. Run first batch of leads through pipeline
5. Send first outreach wave
