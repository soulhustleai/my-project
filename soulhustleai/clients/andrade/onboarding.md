# Adam Andrade — Andrade Health Services (AEGIS)
## Onboarding & Operating Runbook

> **Status:** ACTIVE — 1st SoulHustleAI client (partner/rev-share, not retainer)
> **Package:** AEGIS Partner — $0/mo, revenue share model
> **Business:** Health Insurance advisory
> **Go-live:** 2026-04-04
> **Supabase client id:** `01b17786-a57f-4034-a150-19231c617b51`
> **Owner at SHAI:** Edwin (direct)

---

## Quick Facts

| Field | Value |
|-------|-------|
| Name | Adam Andrade |
| Phone | (407) 561-2878 |
| Email | Deandradehealthadvisor@gmail.com |
| Business | Health Insurance advisor |
| Location | Florida |
| Package | AEGIS Partner (rev-share) |
| Monthly retainer | $0 |
| Stripe customer | NULL (not billed — partner model) |

---

## The AEGIS System (what's live)

Adam runs on our **AEGIS** subsystem — a dedicated health insurance lead gen + follow-up brand.
He's not on the standard SoulHustleAI Catalyst/System/Empire tiers because his compensation
comes from commissions, not retainer. We take a rev-share cut of the commissions.

### Live infrastructure
- **Dashboard:** https://aegis.soulhustleai.com/aegis
- **Intake form:** https://health.soulhustleai.com
- **n8n workflows active:** 5 of 10 built
- **Leads in pipeline:** 197 (live pull)
- **CEO phone for AEGIS:** +1 (929) 236-1564 (separate from Zero)
- **VAPI agent id:** db00cd0f-688c-4425-b766-720e6820526f
- **Voice:** DayDay — the AEGIS front-desk agent (separate from Zero)

---

## The 10 AEGIS Workflows

| # | Workflow | Status |
|---|----------|--------|
| 01 | Intake form → lead capture | ✅ LIVE |
| 02 | Lead scoring + routing | ✅ LIVE |
| 03 | DayDay outbound qualifying call | ✅ LIVE |
| 04 | Text follow-up sequence | ✅ LIVE |
| 05 | Cal.com booking → Adam's calendar | ✅ LIVE |
| 06 | Post-call SMS recap | 🔧 BUILDING |
| 07 | Policy application handoff | 🔧 BUILDING |
| 08 | Commission tracking (Adam → SHAI rev share) | 🔧 BUILDING |
| 09 | Reactivation for expired leads (90-day) | 🔧 BUILDING |
| 10 | Renewal reminder / client retention | 🔧 BUILDING |

---

## Rev-Share Model

- Adam pays $0/mo retainer
- SoulHustleAI takes **25% of commissions** earned on leads generated through the AEGIS pipeline
- Tracked in `client_metrics` table (commission_earned column)
- Paid out monthly via Stripe Connect (wiring pending)

---

## Weekly Health Check (Mondays 10am ET)

```
1. Open clients/andrade/dashboard.html
2. Check:
   - New leads this week (target +40)
   - DayDay call completion rate (target >60%)
   - Bookings created (target +8/wk)
   - Commissions tracked in Supabase
3. SMS Adam: "Week recap: X leads, Y calls, Z booked. Anything to flag?"
4. Log touch in ceo_action_log with business='AEGIS'
```

---

## Known Issues / Next Steps

- [ ] Build workflows 06-10 (pending Edwin review of priority)
- [ ] Wire Stripe Connect for commission payouts
- [ ] Build clients/andrade/dashboard.html (next up)
- [ ] First rev-share settlement calculation due end of month
- [ ] Validate 197 lead count — pull fresh from `aegis_leads` table

---

## Escalation Path

Adam is a friend / founding partner. Never auto-escalate.
- Anything urgent → Edwin calls Adam directly
- System outage → Edwin + hot-fix, DayDay voicemail fallback
- Commission dispute → Edwin resolves personally, in favor of Adam, same-day

---

**Next review:** weekly Monday. Mark in ceo_tasks.
