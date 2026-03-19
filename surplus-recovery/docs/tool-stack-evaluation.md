# Tool Stack Evaluation

## Evaluation Criteria

| Factor | Weight | Definition |
|--------|--------|------------|
| Speed to deploy (MVP) | 25% | How fast can we ship with this? |
| Cost at MVP scale | 20% | Monthly cost at 200-500 leads/month |
| Reliability | 15% | Uptime, consistency, error handling |
| Maintenance burden | 15% | Ongoing effort to keep running |
| Scale ceiling | 10% | Can it handle 10x growth? |
| Integration ease | 10% | API quality, webhook support |
| Community/support | 5% | Docs, forums, responsiveness |

---

## Category 1: Scraping & Browser Automation

### Purpose: Extract surplus lists from county websites (PDF, HTML, portals)

| Tool | MVP Score | Scale Score | Cost (MVP) | Pros | Cons |
|------|-----------|-------------|-----------|------|------|
| **Playwright** | 5 | 5 | Free (self-hosted) | Full control, headless, handles JS-heavy sites, Python + TS support | Requires dev time, self-managed |
| **Apify** | 4 | 4 | $49/mo (starter) | Pre-built actors, proxy management, scheduling, anti-bot handling | Vendor lock-in, cost at scale |
| **Bright Data** | 3 | 5 | $500+/mo | Best proxy infra, SERP API, unblocking | Overkill for MVP, expensive |
| **Firecrawl** | 3 | 3 | $19/mo | Good for web-to-markdown, LLM-friendly | Not built for portal scraping |
| **Browser Use** | 3 | 3 | Free (self-hosted) | AI-driven browser control | Early stage, less reliable for production |
| **Selenium** | 2 | 3 | Free | Legacy, wide support | Slow, heavy, outdated vs Playwright |

**MVP Winner: Playwright (self-hosted Python scripts)**
- Free, full control, handles PDF downloads + HTML parsing + portal navigation
- County-specific scripts are unavoidable anyway — Playwright handles all of it
- Add Apify only if anti-bot becomes a real problem

**Scale Winner: Playwright + Apify (for proxy/anti-bot) or Bright Data**

---

## Category 2: PDF Parsing

### Purpose: Extract structured data from county surplus list PDFs

| Tool | MVP Score | Scale Score | Cost | Pros | Cons |
|------|-----------|-------------|------|------|------|
| **pdfplumber (Python)** | 5 | 4 | Free | Excellent table extraction, lightweight | Python only |
| **Tabula** | 4 | 3 | Free | Good table extraction | Less flexible than pdfplumber |
| **Claude API (vision)** | 4 | 4 | ~$0.01-0.05/page | Handles messy/scanned PDFs, flexible | Cost per page, latency |
| **AWS Textract** | 3 | 5 | $0.015/page | Production-grade OCR | AWS dependency, setup overhead |
| **Adobe PDF Extract** | 3 | 4 | $0.05/page | Good extraction | Expensive, complex API |

**MVP Winner: pdfplumber + Claude API (fallback for messy PDFs)**
- pdfplumber handles well-structured PDFs (most county lists)
- Claude vision handles scanned/messy PDFs that pdfplumber can't parse
- Total cost < $5/month at MVP volume

**Scale Winner: pdfplumber + AWS Textract (for OCR)**

---

## Category 3: Orchestration & Workflow

### Purpose: Coordinate pipeline steps (scrape → parse → enrich → outreach → track)

| Tool | MVP Score | Scale Score | Cost | Pros | Cons |
|------|-----------|-------------|------|------|------|
| **n8n (self-hosted)** | 4 | 4 | Free (self-hosted) | Visual workflows, good integrations, unlimited runs | Self-host maintenance, some limits |
| **Custom code (TS/Python)** | 5 | 5 | Free | Full control, testable, versionable | More dev time upfront |
| **Make.com** | 3 | 3 | $9-16/mo | Edwin already knows it, visual | Operation limits, fragile for complex flows |
| **Zapier** | 2 | 2 | $20+/mo | Easy | Expensive at scale, limited |
| **Temporal** | 2 | 5 | Free (self-hosted) | Best-in-class workflow engine | Overkill for MVP, complex setup |

**MVP Winner: Custom Python/TS scripts + cron jobs**
- Simple, debuggable, versionable
- Each pipeline stage is a script triggered by cron or queue
- No vendor dependency, no operation limits
- n8n for visual monitoring/triggers if desired

**Scale Winner: Custom code + n8n (for visual management) or Temporal**

---

## Category 4: LLMs / AI

### Purpose: Parse messy data, generate outreach, classify records, extract entities

| Tool | MVP Score | Scale Score | Cost | Pros | Cons |
|------|-----------|-------------|------|------|------|
| **Claude API (Sonnet)** | 5 | 5 | ~$3/1M input tokens | Best reasoning, great at extraction, Edwin already uses | Cost at high volume |
| **Claude API (Haiku)** | 5 | 5 | ~$0.25/1M input tokens | Fast, cheap, good for classification | Less capable for complex reasoning |
| **OpenAI GPT-4o-mini** | 4 | 4 | ~$0.15/1M tokens | Cheap, fast | Slightly less capable than Claude for extraction |
| **Gemini** | 3 | 4 | Free tier available | Good PDF handling | API less mature, rate limits |
| **Local LLMs** | 2 | 3 | Free (compute cost) | No API cost | Quality gap, infra needed |

**MVP Winner: Claude Haiku (bulk classification/extraction) + Claude Sonnet (complex parsing)**
- Edwin already has Anthropic API access
- Haiku for high-volume, low-complexity tasks (entity extraction, classification)
- Sonnet for complex parsing (messy PDFs, ambiguous records)
- Total cost: <$20/month at MVP scale

**Scale Winner: Same stack, add caching and batching**

---

## Category 5: CRM / Data Model / Pipeline

### Purpose: Store leads, track cases, manage pipeline stages

| Tool | MVP Score | Scale Score | Cost | Pros | Cons |
|------|-----------|-------------|------|------|------|
| **Supabase** | 5 | 5 | Free tier → $25/mo | Postgres, auth, real-time, API auto-generated, dashboard | Requires schema design |
| **Airtable** | 4 | 3 | Free tier → $20/seat | Quick setup, visual, automations | Scale limits, cost per seat |
| **Notion** | 3 | 2 | Free-$8/mo | Edwin already uses it | Not a real database, slow API, no relational queries |
| **HubSpot** | 3 | 4 | Free CRM → $45/mo | Full CRM features | Overkill, complex, cost |
| **Close** | 3 | 4 | $49/mo | Built for sales, calling built in | Cost, sales-focused not case-focused |
| **GoHighLevel** | 3 | 4 | $97/mo | All-in-one | Expensive, complex, agency-focused |

**MVP Winner: Supabase**
- Free tier handles MVP easily
- Real Postgres database — proper relational data model
- Auto-generated REST API for all tables
- Built-in auth, real-time subscriptions
- Dashboard/admin UI can be built on top
- Edwin's existing Notion for project management, Supabase for operational data

**Scale Winner: Supabase (grows with the business)**

---

## Category 6: Enrichment / Skip Tracing

### Purpose: Find current contact info (phone, email, address) for claimants

| Tool | MVP Score | Scale Score | Cost | Pros | Cons |
|------|-----------|-------------|------|------|------|
| **TruePeopleSearch** | 4 | 2 | Free | Free, decent data | Manual, no API, may block |
| **People Data Labs** | 4 | 5 | $0.02-0.10/record | API-first, good coverage, bulk | Cost adds up |
| **BeenVerified** | 3 | 3 | $27/mo | Consumer-friendly | No real API, manual |
| **Whitepages Pro** | 3 | 4 | Per-lookup pricing | Established, reliable | Expensive per lookup |
| **Skip tracing vendors (IDI, TLO)** | 3 | 5 | Varies | Best data for this use case | Requires credentialed access |
| **Spokeo** | 3 | 2 | $20/mo | Consumer-friendly | Manual, limited API |
| **Pipl (now Pipl.ai)** | 3 | 4 | Enterprise pricing | Very good matching | Expensive |

**MVP Winner: TruePeopleSearch (free manual) → People Data Labs (API at scale)**
- Start with free manual lookups to validate conversion
- Move to People Data Labs API when doing 50+ lookups/week
- Add skip tracing vendor (IDI/TLO) for hard-to-find claimants

**Scale Winner: People Data Labs + IDI/TLO**

---

## Category 7: Outreach

### Purpose: Contact claimants via mail, email, SMS, phone

| Channel / Tool | MVP Score | Scale Score | Cost | Pros | Cons |
|---------------|-----------|-------------|------|------|------|
| **Lob (direct mail API)** | 5 | 5 | $0.75-1.50/letter | API-driven mail, address verification, tracking | Cost per piece |
| **Handwritten mail (Handwrytten)** | 3 | 3 | $3-5/letter | Higher open rate | Expensive per piece |
| **Smartlead** | 4 | 4 | $39/mo | Email warmup, multi-inbox, sequences | Email may not be primary channel |
| **Instantly** | 4 | 4 | $30/mo | Similar to Smartlead | Same |
| **Twilio (SMS)** | 4 | 5 | $0.0079/SMS | Reliable, API-driven, Edwin already has | 10DLC registration required |
| **Twilio (Voice)** | 3 | 4 | $0.014/min | Programmable calls | Need human for trust-building |
| **Retell AI (voice)** | 2 | 3 | $0.10-0.20/min | AI voice agent | Low trust for this use case |
| **Bland AI** | 2 | 3 | Similar | AI calling | Same trust issue |
| **Manual phone calls** | 5 | 2 | Free (time) | Highest trust | Doesn't scale |

**MVP Winner: Lob (direct mail) + Twilio (SMS follow-up) + manual phone (high-value)**
- Direct mail is the primary channel — it builds trust
- SMS for follow-up after mail is received
- Manual phone calls for high-value leads (>$10K surplus)
- Email as supplementary channel

**Scale Winner: Lob + Twilio + Smartlead + VA phone team**

---

## Category 8: Forms / E-Sign / Document Generation

### Purpose: Collect intake info, get signatures, generate claim packets

| Tool | MVP Score | Scale Score | Cost | Pros | Cons |
|------|-----------|-------------|------|------|------|
| **Jotform** | 5 | 4 | Free tier → $34/mo | Forms + e-sign built in, HIPAA option | E-sign limits on free tier |
| **Tally** | 4 | 3 | Free → $29/mo | Clean, simple, good free tier | No built-in e-sign |
| **Typeform** | 3 | 3 | $25/mo | Beautiful forms | No e-sign, expensive |
| **PandaDoc** | 4 | 5 | $19/mo | Full doc gen + e-sign + templates | More complex setup |
| **DocuSign** | 3 | 5 | $10-25/mo | Industry standard e-sign | Expensive for volume, complex API |
| **Google Docs + PDF gen** | 4 | 3 | Free | Templates → PDF, simple | Manual, no e-sign |

**MVP Winner: Jotform (intake + e-sign) + Google Docs templates (claim packets)**
- Jotform handles intake forms AND electronic signatures in one tool
- Google Docs templates with mail merge for claim packet generation
- Total cost: Free at MVP scale

**Scale Winner: PandaDoc (full document workflow) or custom doc generation**

---

## Category 9: Backend / Database / Deployment

### Purpose: Store data, run services, deploy and monitor

| Tool | MVP Score | Scale Score | Cost | Pros | Cons |
|------|-----------|-------------|------|------|------|
| **Supabase** | 5 | 5 | Free → $25/mo | Postgres + API + auth + storage | See CRM section |
| **Railway** | 5 | 4 | $5/mo + usage | Easy deployment, good DX, cron support | Cost at scale |
| **Render** | 4 | 4 | Free → $7/mo | Simple, cron jobs, good free tier | Limited resources on free |
| **Vercel** | 4 | 4 | Free → $20/mo | Great for Next.js frontend/dashboard | Backend limits |
| **Fly.io** | 4 | 5 | Free → usage | Good for persistent services | More complex setup |
| **AWS** | 2 | 5 | Varies | Everything | Overkill for MVP, complex |
| **Digital Ocean** | 3 | 4 | $5/mo | Droplets, simple | More manual ops |

**MVP Winner: Supabase (data) + Railway (services) + Vercel (dashboard)**
- Supabase: database, auth, API, storage
- Railway: Python/TS services, cron jobs, background workers
- Vercel: Next.js dashboard for pipeline visibility
- Total cost: <$10/month at MVP

**Scale Winner: Same stack scales well to $50K+ MRR**

---

## Category 10: Monitoring / Logging / Queuing

| Tool | MVP Score | Scale Score | Cost | Pros | Cons |
|------|-----------|-------------|------|------|------|
| **Supabase (Postgres as queue)** | 4 | 3 | Included | Simple, no new tool | Not a real queue |
| **BullMQ + Redis** | 3 | 5 | $0-10/mo | Real job queue, retries, scheduling | Setup complexity |
| **Sentry** | 4 | 5 | Free tier | Error tracking, alerts | Need to integrate |
| **Logflare / Axiom** | 4 | 4 | Free tier | Structured logging, dashboards | Another tool |
| **Console.log + Supabase audit table** | 5 | 2 | Free | Dead simple | Won't scale |

**MVP Winner: Console.log + Supabase audit table + Sentry (free tier)**
- Log to console and write key events to a Supabase audit table
- Sentry for error alerting
- Add BullMQ when job processing needs real queuing

**Scale Winner: BullMQ + Sentry + Axiom**

---

## Recommended MVP Stack (Total)

| Layer | Tool | Cost/Month |
|-------|------|-----------|
| Scraping | Playwright (Python) | $0 |
| PDF Parsing | pdfplumber + Claude API | <$5 |
| Orchestration | Python scripts + cron | $0 |
| AI | Claude Haiku + Sonnet | <$20 |
| Database/API | Supabase | $0 (free tier) |
| Enrichment | TruePeopleSearch → People Data Labs | $0-50 |
| Direct Mail | Lob API | ~$1-2/letter |
| SMS | Twilio | <$10 |
| Email | Smartlead or Gmail + sequences | $0-39 |
| Forms/E-Sign | Jotform | $0 (free tier) |
| Doc Generation | Google Docs templates | $0 |
| Services | Railway | $5 |
| Dashboard | Vercel + Next.js | $0 |
| Monitoring | Sentry + Supabase audit log | $0 |

### Total MVP Monthly Cost: ~$30-130/month (excluding per-lead enrichment and mail costs)

### Variable Costs Per Lead
- Skip trace: $0-0.10/lead
- Direct mail: $1-2/lead
- SMS: $0.01-0.05/lead
- Total per lead: ~$1-3

### Cost Per Signed Client (at 1% conversion)
- 100 leads × $2/lead = $200 cost per signed client
- Revenue per client: $3,000-$10,000
- **ROI: 15-50x**

---

## Dependency Map

```
docs/tool-stack-evaluation.md
  ↓ feeds
schemas/core-data-model.md        (Supabase schema design)
services/source-monitor/           (Playwright scripts)
services/record-ingestion/         (pdfplumber + Claude)
services/claimant-enrichment/      (People Data Labs)
services/outreach-engine/          (Lob + Twilio + Smartlead)
services/document-engine/          (Jotform + Google Docs)
apps/dashboard/                    (Next.js + Vercel)
```
