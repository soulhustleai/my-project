# Eli — Abundantly Blessed Solutions
## Onboarding & Operating Runbook

> **Status:** ACTIVE — 7 n8n workflows built, SMS blocked on Twilio 10DLC
> **Package:** The System — $1,497/mo + $2,500 build
> **Business:** Junk removal / moving (South Florida)
> **Twilio:** +1 (844) 643-9825 (toll-free, 10DLC pending)
> **Onboarded:** 2026-02
> **Owner at SHAI:** Edwin (direct)

---

## Quick Links
- **Client portal:** `clients/eli/dashboard.html`
- **Make.com / n8n scenarios:** logged in Notion → Eli CRM
- **Webhook URLs:** see Notion `Eli → Integrations`
- **Contact:** Eli via SMS — replies in 2-4hr business hours

---

## The 7 Automations We Built

| # | Name | Trigger | Status |
|---|------|---------|--------|
| 01 | Inbound Lead Capture | Website form → Cal.com | ✅ LIVE |
| 02 | Missed Call Auto-Text | Twilio webhook on voicemail | ⚠ 10DLC pending |
| 03 | Quote Follow-Up (24hr) | Quote sent but not signed | ✅ LIVE |
| 04 | Post-Job Review Request | Invoice paid | ✅ LIVE |
| 05 | Reactivation (90-day dormant) | No contact 90+ days | ✅ LIVE |
| 06 | Referral Ask (happy customer) | 5-star review received | 🔧 pending confirm |
| 07 | Ascension Offer (repeat customer) | 2+ jobs completed | 🔧 pending confirm |

### The 10DLC Blocker (Most Important)
- Twilio toll-free `+18446439825` needs 10DLC campaign approval
- **Action required from Edwin:** submit TCR registration for "Abundantly Blessed Solutions" brand
- Timeline: 24-72hr standard, up to 2 weeks worst case
- **Workaround until approved:** scenarios 02 + 03 use email fallback (Resend)

---

## Weekly Health Check (do every Monday 9am ET)

```
1. Open clients/eli/dashboard.html
2. Check:
   - Jobs booked this week ↑
   - Missed call rate (target <15%)
   - Review count (target +3/wk)
   - Revenue attributed to SHAI automations
3. Send Eli a 2-line SMS: "Last week: X jobs booked, Y reviews pulled. Issue to flag: Z."
4. Log touch in ceo_action_log
```

---

## When Something Breaks
- n8n failure → auto-posts to #eli-ops Slack channel
- Twilio outage → fallback to Resend email + Eli gets personal text from Edwin
- Payment dispute → immediately credit + escalate, don't argue
- **Escalation path:** Edwin (personal) → pause automation → fix → resume → apology SMS

---

## Upsell Path (when ready)
Once 10DLC lands and SMS is clean for 30 days, pitch Eli The Empire ($3,497/mo):
- Dedicated Zero sub-agent with Eli's voice cloned
- Dispatch engine (route jobs to crews)
- Square payment automation
- Custom client review farm
- Monthly strategy call with Edwin

**Upgrade trigger:** Eli clears $25K/mo attributed to SHAI automations → pitch Empire.

---

## Known Quirks
- Eli prefers SMS over email. Never call unless urgent.
- He moves fast — don't slow him down with long proposals.
- He referred Mike (next client). Treat the relationship like gold.
- Spanish-speaking customers = big part of his pipeline. Zero's voice supports both EN/ES — confirm ES side is toggled on when 10DLC lands.

---

**Next review:** weekly Monday. Mark in ceo_tasks.
