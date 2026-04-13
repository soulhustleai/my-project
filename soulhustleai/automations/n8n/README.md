# n8n Workflow Blueprints — SoulHustleAI
## Importable JSON workflows for Railway n8n instance

> **n8n instance:** https://n8n-production-524ef.up.railway.app
> **How to import:** n8n UI → Workflows → Import from File → select .json → save → activate
> **Environment variables required:** see `.env.required.md`

---

## The 5 Core Workflows

| # | File | Purpose | Trigger |
|---|------|---------|---------|
| 01 | `01_the_gate_intake.json` | The Gate application intake | POST /webhook/shai-gate-intake |
| 02 | `02_hunter_enrichment.json` | Fire enrichment engine (15 sources) on pending leads | Cron: every 30 min |
| 03 | `03_outreach_cold_email.json` | Send cold email sequence to enriched leads | Cron: every 2 hours (business hours) |
| 04 | `04_zero_missed_call.json` | Missed call autotext + CRM update | Twilio webhook |
| 05 | `05_dead_lead_resurrection.json` | 3-touch revival for 90+ day dead leads | Cron: daily 10am ET |

---

## Required environment variables (set in n8n credentials)

```
SUPABASE_URL=https://pjkurxtvvtxbpfearqhd.supabase.co
SUPABASE_SERVICE_KEY=<service role key>
TWILIO_ACCOUNT_SID=<sid>
TWILIO_AUTH_TOKEN=<token>
TWILIO_FROM_NUMBER=+18446439825
VAPI_API_KEY=<key>
VAPI_ZERO_AGENT_ID=<agent id>
RESEND_API_KEY=<key>
RESEND_FROM=edwin@soulhustleai.com
CAL_COM_API_KEY=<key>
CAL_COM_EVENT_ID=<strategy-call>
POSTHOG_API_KEY=<key>
APOLLO_API_KEY=<key>
HUNTER_IO_API_KEY=<key>
```

---

## Activation checklist

- [ ] Import all 5 workflows from JSON files
- [ ] Attach credentials (Supabase, Twilio, Resend, VAPI)
- [ ] Activate workflow 01 → test with curl POST to webhook
- [ ] Activate workflow 02 → verify enrichment_jobs start processing
- [ ] Activate workflow 03 → verify cold email template renders correctly
- [ ] Activate workflow 04 → test with Twilio test call
- [ ] Activate workflow 05 → dry-run with 1 dead lead manually
