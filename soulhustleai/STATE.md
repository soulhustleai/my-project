# SoulHustleAI — Live State (Synced from Supabase)

> **Last synced:** 2026-04-13 from Supabase project `pjkurxtvvtxbpfearqhd`
> **Source of truth:** production database. This file beats CLIENTS.md, README.md, and CONTEXT.md when they disagree.

---

## Current Revenue
- **MRR: $400** (Eli / Abundantly Blessed Solutions — Foundation tier)
- **Target: $5,000 MRR** (Phase 1 — Cash Flow Foundation)
- **Gap: $4,600 MRR** (~3 Empire deals or 7 System deals or 15 Catalyst deals)
- **Infrastructure burn: ~$101/mo** (Supabase Pro $25, Railway $5, ElevenLabs $22, domains $24, OpenRouter $20, Supabase compute $5)
- **Net: ~$299/mo** — infrastructure is paid. Every new deal is ~100% margin until scale.

## Live Clients (clients table)

### 1. Adam Andrade — Andrade Health Services  `first client`
- **id:** `01b17786-a57f-4034-a150-19231c617b51`
- **industry:** Health Insurance
- **package:** AEGIS Partner
- **monthly_rate:** $0 (partner/revenue share, not retainer)
- **status:** active
- **phone:** (407) 561-2878
- **email:** Deandradehealthadvisor@gmail.com
- **go_live:** 2026-04-04
- **live systems:**
  - aegis.soulhustleai.com/aegis — dashboard
  - health.soulhustleai.com — intake form
  - 10 n8n workflows (5 active on Railway)
  - 197 leads in AEGIS pipeline
- **stripe_customer_id:** NULL (not billed)

### 2. Eli — Abundantly Blessed Solutions  `first paying client`
- **id:** `0554fcd6-9f7e-42d1-8a59-8eefe65b5abc`
- **industry:** Junk Removal / Moving
- **location:** South Florida
- **package:** Foundation — $400/mo
- **status:** active
- **phone:** +1 954-218-9947
- **email:** NULL (needs capture)
- **go_live_at:** NULL (deploy pending — 7-day onboarding stalled at day 0)
- **stripe_customer_id:** NULL (paid offline — webhook not wired)
- **blockers:**
  - Twilio 10DLC carrier approval → switched to Resend email workaround
  - client_onboarding stalled at day 0 (Edwin must trigger manually)

## Pipeline (leads table)

### Hot Scraped Leads — score 99, `status=enriched|contacted`  `NYC 2026-04-03`
All 11 missing email. Most have phone. None have `cal_booked`.

| Name | Phone | Status |
|---|---|---|
| Pupkin Insurance | (866) 273-6369 | enriched |
| Concerned Dental Care of the Bronx | (718) 652-7370 | contacted |
| Harris Plumbing & Heating | (718) 495-3400 | contacted |
| Brooklyn Cleaning Services | (929) 656-6456 | contacted |
| BarberSpa BK | (929) 479-3900 | contacted |
| Sammy Brokerage Inc | (718) 204-1555 | enriched |
| Regency Agency Inc | (718) 377-0566 | enriched |
| Z & R Associates | (316) 943-2683 | enriched |
| Brooklyn Dental Professionals | (718) 486-7600 | enriched |
| Neuhaus Realty | (718) 979-3400 | enriched |
| Cleaning Brooklyn | (929) 656-6456 | enriched |

### Warm Leads — score 88
Brooklyn Law Group, Crown Heights Plumbing, Innovative Health Dental, Fresh Start Cleaning NYC, Queens Tax Services

### Named Prospect: Mike — RTS Appliance  `from ceo_tasks`
- **Target deal:** $797/mo  (maps to System tier +$100 or discounted Empire)
- **Industry:** Appliance repair (NOT "AC contractor" — CLIENTS.md was wrong)
- **Status:** pending close, original due 2026-03-28

## Live Infrastructure (tech_stack, website_canonical, etc.)

### Websites (website_canonical)
| Property | URL |
|---|---|
| main | https://soulhustleai.com |
| gate (application) | https://soulhustleai-gate.vercel.app |
| Zero CRM | https://zero.soulhustleai.com |
| AEGIS dashboard | https://aegis.soulhustleai.com |
| DayDay intake | https://health.soulhustleai.com |
| Boardroom | https://godfident-boardroom.vercel.app |
| Repo | https://github.com/soulhustleai |
| Contact | soulhustleai@gmail.com |

### Zero (VAPI + ElevenLabs) — `assistant_id 2fdd8b29-0e1b-4c01-94ae-e5190f350558`
| Property | Value |
|---|---|
| phone | **+1 929-236-1567** |
| voice | Orlando (ElevenLabs `4t8HWMowRF0NaJl0r9MS`) |
| voice settings | stability 0.42, similarity 0.9, style 0.52 |
| cal.com | cal.com/soulhustleai/strategy (event `4946321`) |
| email inbox | gf-zero@agentmail.to |
| email webhook | https://n8n-production-524ef.up.railway.app/webhook/zero-email-inbound |
| title | "C.E.O. of Soul Hustle A.I. — Godfident Collective" |

### 5 CEO Phones (vapi_ceo_phones)
| CEO | Phone | VAPI assistant_id |
|---|---|---|
| Zero (SHAI) | +1 929-236-1567 | 2fdd8b29-0e1b-4c01-94ae-e5190f350558 |
| AEGIS (DayDay/health) | +1 929-236-1564 | db00cd0f-688c-4425-b766-720e6820526f |
| MIDAS (surplus recovery) | +1 929-202-9427 | 8dc784e9-b9e8-4fca-8a9e-48b330e33669 |
| APEX (GOD MODE Credit) | +1 929-236-1353 | 00341d48-d079-4b0b-82fe-89f6febe1702 |
| SOVEREIGN (oversight) | +1 929-499-9842 | de9f8e6c-ce71-4006-a508-58e98bdffd37 |

### n8n on Railway — **40 active workflows**
- **URL:** https://n8n-production-524ef.up.railway.app
- **Division I — Intelligence & Lead Acquisition:** L1 discovery, L2 capture, L3 scoring, L4 speed-to-lead, L5 nurture, L6 email, L7 call, L8 reporting, L9 CERBERUS security
- **Key workflows:**
  - Zero Speed-to-Lead call: `q4XBdQaUhUqOVLeV`
  - Pre-call briefing: `XJQVZEIGEAbM6JZ1`
  - Dead lead resurrection: `vy2mRMVy0IPSwzZL`
  - Zero email system: `0fmhEnPDxFkGjZlP`

### Supabase
- **project:** pjkurxtvvtxbpfearqhd
- **URL:** https://pjkurxtvvtxbpfearqhd.supabase.co
- **Key tables:** leads, clients, client_onboarding, client_metrics, client_health, follow_up_sequences, sms_log, email_queue, webhook_events, financial_transactions, ceo_tasks, system_config, ceo_action_log

### Twilio
- **account_sid:** (stored in `system_config.twilio_credentials` — redacted from repo)
- **numbers:** +1 844-643-9825 (toll-free, 10DLC pending), +1 347-404-5448
- **status:** Auth token needs configuring in n8n HTTP Basic Auth credential. 10DLC for Eli's SMS still pending carrier approval.

## Service Packages (shai_service_packages)  `LIVE`

### Catalyst — $297 deposit + $297/mo  `entry tier`
- **Target:** Solo to small team, under $300K revenue
- **Build time:** 48 hours
- **Automations:** 1 (Speed to Lead)
- **ROI:** 6-12x
- **Value delivered:** $2,000-$4,000/mo recovered revenue
- **Tagline:** "First one in wins. Always."
- **Stripe link:** https://buy.stripe.com/14A9AT3eV8TAait2kn73G00
- **product_id:** prod_UHtzReiOmAcovb

### System — $697 deposit + $697/mo  `mid tier`
- **Target:** 3-10 employees, $300K-$1M revenue
- **Build time:** 7 days
- **Automations:** 3 (Speed to Lead + Follow-up Sequences + Database Reactivation)
- **ROI:** 7-20x
- **Value delivered:** $5,000-$15,000/mo
- **Tagline:** "Three automations working while you sleep."
- **Stripe link:** https://buy.stripe.com/8x2eVd5n3edU0HT9MP73G01
- **product_id:** prod_UHu0uGMoPtF53g

### Empire — $1497 deposit + $1497/mo  `high tier`
- **Target:** 10+ employees, $1M+ revenue, professional services
- **Build time:** 14 days
- **Automations:** ALL 5 (Speed to Lead + Doc Processing + Follow-up + DB Reactivation + Internal Reporting)
- **ROI:** 10-30x
- **Value delivered:** $15,000-$50,000/mo
- **Tagline:** "All 5 automations. KEEPER oversight. Monthly strategy call."
- **Stripe link:** https://buy.stripe.com/aFa8wP16N7Pw76h3or73G02
- **product_id:** prod_UHu0r9XLAepjK9

### Sovereign Build — custom $3K-$10K+/mo  `enterprise`
- **Target:** Multi-location, enterprise, law firms, insurance agencies, accounting firms, franchises
- **Build time:** 21-60 days
- **Automations:** unlimited + custom builds + multi-location + API integrations
- **ROI:** 15-50x
- **Tagline:** "Full empire. Custom integrations. SOVEREIGN oversight."
- **Edwin-direct consulting tier.** No Stripe link — custom quote.

### The Big Promise
> "We put $10,000+ back in your pocket in 30 days — or we keep building for free until we do. We have never had to honor that guarantee."

### Rockefeller Cross-Sell Logic
One qualified lead → up to 4 revenue streams:
- Has credit issues → **APEX** (GOD MODE Credit)
- Has unclaimed funds / real estate → **MIDAS** (surplus recovery)
- Needs health insurance → **AEGIS/DayDay**
- Has a service business → **SHAI** (this brand)

## 5 Core Automations

| # | Automation | Who | Math | Tagline |
|---|---|---|---|---|
| 1 | **Speed to Lead** | HVAC, junk, cleaning, plumbing, roofing, real estate, insurance | 78% of deals go to first responder. Service biz loses 8-12 after-hours leads/week. At $300/job = $2,400-$3,600/WEEK lost | "First one in wins. Always." |
| 2 | **Document Processing** | Accountants, law firms, insurance, healthcare, mortgage, property managers | 3 hrs/day @ $100/hr = $6K/mo. AI does it in 10 min. | "200 invoices in the inbox. Done in 10 minutes." |
| 3 | **Follow-up Sequences** | Anyone with multi-day sales cycle | 80% of sales happen after the 5th contact. Most businesses quit at 2. | "80% of sales happen after the 5th contact." |
| 4 | **Database Reactivation** | Anyone with 90-day-old contacts, seasonal, restaurants, real estate | 500 old contacts × 10% × 30% close × $300 = $4,500 from $0 | "Your dead list is not dead. It is untouched money." |
| 5 | **Internal Reporting** | Multi-employee, B2B, property mgmt, healthcare, logistics | Saves 1-2 hrs/day in status calls. Reduces complaints 60%. | "Nobody asks where the job is when the system already told them." |

## Division II Gaps — `P0 revenue blockers`

1. **11 score-99 leads unenriched** — no email captured. HUNTER enrichment workflow runs but Hunter.io doesn't find every biz. Fix: SerpAPI Google Maps fallback. See `scripts/enrich_hot_leads.sql`.
2. **5 enriched leads not being contacted** — Multi-Touch Outreach trigger broken. Fix: verify trigger fires on `status=enriched AND has_phone=true`.
3. **VAPI calls not logging to `call_logs`** — webhook payload mapping broken.
4. **No auto-proposal generator** — D2.3 Blueprint Email only fires post-payment. Need pre-close proposal on `status=qualified`.
5. **Stripe webhooks not wired to Supabase** — both clients have `stripe_customer_id=NULL`. Need webhook → n8n → upsert clients.
6. **Eli onboarding stalled at day 0** — all `client_onboarding` flags false despite `payment_received=true`. Manual trigger needed.

## Pending CEO Tasks — `soulhustleai-related`

- **urgent** Close Mike — RTS Appliance $797/mo  (original due 2026-03-28, slipped)
- **urgent** Restart n8n after v2.15.1 upgrade (13 workflows activated via SQLite, webhooks need re-register)
- **high** Wire Resend in n8n (unblocks email workflows for Eli)
- **high** Activate lead gen — 20 new prospects this week
- **urgent** Fix CC revenue display bug (type=Revenue vs type=income)

---

## 2026-04-13 — Enrichment Reset + Repo Build Session

### Data corrections
- **20 NYC leads reset** from mislabeled `contacted`/`enriched` → `pending_enrichment`
  - All 20 had `last_contact_at=NULL`, `call_attempt_count=0`, `email_opened=false`, `cal_booked=false`
  - Confirmed: **never actually contacted**. Previous status was wrong.
  - Cleared all stale flags, set `nurture_eligible=true`, appended notes
- **20 enriched_contacts rows created** + 20 `enrichment_jobs` rows queued with status=`pending`
  - `triggered_by = 'edwin_reset_2026_04_13_soulhustleai_hot_leads'`
  - Each job carries `enrichment_data.source_lead_id` so the HUNTER workflow can write back to the leads table
  - 15 enrichment sources standing by (holehe, maigret, sherlock, phoneinfoga, theharvester, emailrep, hunter_io, apollo, gravatar, numverify, opencorporates, courtlistener, google_places, yelp_fusion, abstract_api)

### Files built tonight (`claude/finish-soulhustle-ai-X6e5Q`)

```
soulhustleai/
├── STATE.md                              (this file)
├── TONIGHT-TEST-PLAN.md                  e2e verification runbook
├── MONEY-TOMORROW.md                     24-hour revenue playbook
├── dashboard/
│   └── command-center.html               live Supabase-backed CC (v1)
├── website/
│   ├── index.html                        main marketing site
│   ├── apply.html                        The Gate intake
│   ├── roi-calculator.html               2-min leak calculator
│   └── zero-hq.html                      Zero AI CEO page
├── clients/
│   ├── eli/
│   │   ├── dashboard.html                Supabase-backed portal
│   │   └── onboarding.md                 runbook
│   └── andrade/                          (todo — Adam client)
├── pitches/
│   ├── mike-ac-contractor.md             ⚠ file misnamed — needs rewrite as RTS Appliance
│   └── proposal-template.md              reusable template
├── outreach/
│   ├── cold-email-sequence.md            5-email sequence
│   ├── sms-scripts.md                    8 SMS templates
│   ├── dm-playbook.md                    IG + LinkedIn
│   └── dead-lead-resurrection.md         90-day revival
├── automations/n8n/
│   ├── README.md
│   ├── 01_the_gate_intake.json
│   └── 02_hunter_enrichment.json
└── scripts/
    ├── smoke_test.sh                     e2e infra test
    ├── fire_enrichment.py                manual enrichment fire
    └── .env.example                      required env vars
```

### Corrections applied in same session
- ✅ `website/index.html` now uses real packages: Catalyst $297 / System $697 /
  Empire $1497 / Sovereign custom — with live Stripe links embedded
- ✅ `website/apply.html` package selector fixed to match real tiers
- ✅ `pitches/mike-rts-appliance.md` written (replaces wrong mike-ac-contractor.md)
  with appliance-repair content + $797/mo target + real Stripe link
- ✅ `clients/andrade/dashboard.html` + `onboarding.md` written for Adam
- ✅ `CLIENTS.md` rewritten with Adam + Eli + Mike reality
