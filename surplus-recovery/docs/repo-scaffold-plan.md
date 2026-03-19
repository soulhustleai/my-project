# Repo Scaffold Plan

## Recommended Structure

```
surplus-recovery/
├── README.md                          # Mission, architecture, status, next steps
├── .env.example                       # Required environment variables
│
├── docs/                              # Strategy, research, and specs
│   ├── executive-summary.md
│   ├── research-game-plan.md
│   ├── market-hypotheses.md
│   ├── research-findings.md
│   ├── state-county-ranking.md
│   ├── business-model-recommendation.md
│   ├── tool-stack-evaluation.md
│   ├── system-architecture.md
│   ├── mvp-build-plan.md
│   ├── first-deal-playbook.md
│   ├── founder-action-protocol.md
│   ├── human-task-map.md
│   ├── sop-teaching-system.md
│   ├── kpi-dashboard-spec.md
│   ├── autonomy-roadmap.md
│   └── repo-scaffold-plan.md
│
├── ops/                               # Operational management
│   ├── implementation-backlog.md
│   ├── risk-register.md
│   ├── launch-checklist.md
│   └── weekly-ops-rhythm.md
│
├── schemas/                           # Data model definitions
│   ├── core-data-model.md             # All Supabase tables
│   ├── county-source-registry.md      # Source config schema
│   ├── lead-lifecycle.md              # State machine definition
│   ├── claimant-schema.md             # Claimant entity definition
│   ├── opportunity-scoring-model.md   # Scoring algorithm
│   ├── outreach-event-schema.md       # Outreach tracking
│   └── audit-log-schema.md            # Audit trail
│
├── workflows/                         # Process flow definitions
│   ├── lead-ingestion-flow.md
│   ├── claimant-enrichment-flow.md
│   ├── outreach-flow.md
│   ├── intake-signature-flow.md
│   ├── claim-prep-flow.md
│   ├── submission-flow.md
│   ├── founder-escalation-flow.md
│   └── state-transition-map.md
│
├── services/                          # Service implementations
│   ├── source-monitor/                # County source scraping
│   │   ├── README.md
│   │   ├── monitor.py
│   │   └── sources/                   # Per-county source configs
│   │       ├── broward_fl.py
│   │       ├── palm_beach_fl.py
│   │       └── hillsborough_fl.py
│   ├── record-ingestion/              # PDF/HTML parsing
│   │   ├── README.md
│   │   ├── ingest.py
│   │   └── parsers/
│   │       ├── pdf_parser.py
│   │       └── html_parser.py
│   ├── normalization/                 # Data cleaning and dedup
│   │   ├── README.md
│   │   └── normalize.py
│   ├── opportunity-engine/            # Lead scoring
│   │   ├── README.md
│   │   └── score.py
│   ├── claimant-enrichment/           # Skip tracing
│   │   ├── README.md
│   │   └── enrich.py
│   ├── outreach-engine/               # Mail, SMS, email sending
│   │   ├── README.md
│   │   ├── outreach.py
│   │   ├── lob_client.py
│   │   ├── twilio_client.py
│   │   └── email_client.py
│   ├── document-engine/               # Claim packet generation
│   │   ├── README.md
│   │   └── generate.py
│   ├── submission-engine/             # Claim filing
│   │   ├── README.md
│   │   └── submit.py
│   ├── case-tracker/                  # Status monitoring
│   │   ├── README.md
│   │   └── track.py
│   └── notifications/                 # Alerts and escalations
│       ├── README.md
│       └── notify.py
│
├── packages/                          # Shared code
│   ├── shared-types/                  # TypeScript/Python type definitions
│   │   └── types.py
│   ├── config/                        # Environment and app config
│   │   └── config.py
│   ├── prompts/                       # LLM prompt templates
│   │   ├── parse_surplus_pdf.txt
│   │   └── classify_response.txt
│   └── utils/                         # Common utilities
│       ├── supabase_client.py
│       └── logger.py
│
├── templates/                         # Document and message templates
│   ├── outreach/
│   │   ├── mail_letter_1.md
│   │   ├── mail_letter_2.md
│   │   ├── sms_followup_1.txt
│   │   ├── sms_followup_2.txt
│   │   └── email_followup_1.md
│   ├── documents/
│   │   ├── contingency_agreement.md
│   │   ├── claim_cover_letter.md
│   │   ├── affidavit_template.md
│   │   └── w9_instructions.md
│   └── founder-actions/
│       ├── fa_claim_review.md
│       ├── fa_phone_call.md
│       └── fa_portal_submission.md
│
├── scripts/                           # Utility and setup scripts
│   ├── setup_supabase.sql             # Database schema creation
│   ├── seed_sources.py                # Populate county source registry
│   └── run_pipeline.py                # Manual full pipeline trigger
│
├── apps/                              # Frontend applications
│   ├── dashboard/                     # Pipeline dashboard (Next.js)
│   └── admin/                         # Admin panel (future)
│
└── tests/                             # Test files
    ├── test_parser.py
    ├── test_scorer.py
    └── test_enrichment.py
```

---

## Module Responsibilities

| Module | Responsibility | Language | Key Dependencies |
|--------|---------------|----------|-----------------|
| source-monitor | Check county sites, download new files | Python | Playwright, Supabase |
| record-ingestion | Parse PDFs/HTML into structured records | Python | pdfplumber, Anthropic SDK |
| normalization | Clean, dedupe, validate records | Python | Supabase |
| opportunity-engine | Score leads by value and actionability | Python | Supabase |
| claimant-enrichment | Find contact info for claimants | Python | PDL API, Supabase |
| outreach-engine | Send mail, SMS, email outreach | Python | Lob, Twilio, Supabase |
| document-engine | Generate claim packets from templates | Python | Jinja2/Google Docs API |
| submission-engine | File claims with counties | Python | Lob (mail), Supabase |
| case-tracker | Monitor claim status | Python | Supabase |
| notifications | Send alerts to founder | Python | Twilio, SendGrid, Supabase |
| dashboard | Visual pipeline management | TypeScript (Next.js) | Supabase, Vercel |
| shared-types | Shared data types and enums | Python | None |
| config | Environment and app configuration | Python | python-dotenv |
| utils | Supabase client, logger, common helpers | Python | supabase-py, Sentry |

---

## Package Boundaries

- **Services** are standalone scripts that can run independently via cron or manual trigger
- **Packages** are imported by services (never run standalone)
- **Templates** are data files consumed by document-engine and outreach-engine
- **Schemas** are documentation — they define the Supabase schema, implemented via scripts/setup_supabase.sql
- **Apps** are separately deployed (Vercel)

---

## MVP Services (Build First)

1. source-monitor (3 county scrapers)
2. record-ingestion (PDF parser)
3. normalization
4. opportunity-engine
5. claimant-enrichment
6. outreach-engine (Lob + Twilio)

## Later Services

7. document-engine (Month 2)
8. submission-engine (Month 2)
9. case-tracker (Month 2)
10. notifications (Month 2)
11. dashboard (Month 2-3)

---

## Scaffold Order

```
1. packages/config/          → env vars, Supabase connection
2. packages/utils/           → Supabase client, logger
3. packages/shared-types/    → Enums, type definitions
4. scripts/setup_supabase.sql → Create all tables
5. services/source-monitor/  → First scraper (Broward)
6. services/record-ingestion/ → PDF parser
7. services/normalization/   → Dedup + validate
8. services/opportunity-engine/ → Scorer
9. services/claimant-enrichment/ → Skip trace
10. services/outreach-engine/  → Lob + Twilio
11. templates/outreach/        → Letter + SMS templates
12. templates/documents/       → Agreement template
```

---

## Dependency Map

```
docs/repo-scaffold-plan.md
  ↓ feeds
All /services, /packages, /schemas, /scripts, /templates creation
ops/implementation-backlog.md (build tasks map to this scaffold)
```
