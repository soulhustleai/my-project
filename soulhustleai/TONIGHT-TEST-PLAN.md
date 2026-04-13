# 🔥 TONIGHT — LIVE TEST PLAN
## SoulHustleAI End-to-End Verification

> **Goal:** By midnight tonight, every critical system is green and you've seen it working with your own eyes.
> **Duration:** ~90 minutes
> **You'll need:** laptop + phone + Supabase service key + Twilio + VAPI + Resend creds

---

## PHASE 0 — Setup (10 min)

- [ ] Pull latest on branch: `git pull origin claude/finish-soulhustle-ai-X6e5Q`
- [ ] `cd soulhustleai/scripts && cp .env.example .env`
- [ ] Fill in all real values in `.env` (never commit this file)
- [ ] Run: `chmod +x smoke_test.sh`

---

## PHASE 1 — Infrastructure Smoke Test (5 min)

```bash
cd soulhustleai/scripts
./smoke_test.sh
```

**Expected result:** ALL GREEN except Stripe (optional).
If any row is RED, fix before proceeding.

Likely failures + fixes:
- **Supabase ping fails** → check SUPABASE_URL and SUPABASE_SERVICE_KEY in `.env`
- **Twilio fails** → check SID/Auth token, verify account balance
- **VAPI fails** → check agent ID exists in VAPI dashboard
- **Resend fails** → check API key + verified domain

---

## PHASE 2 — Command Center Verification (10 min)

Open `soulhustleai/dashboard/command-center.html` in your browser.

- [ ] Paste Supabase service key when prompted (stored locally only)
- [ ] Verify **Leads in Pipeline** shows 20+ leads
- [ ] Verify **Enrichment Queue** shows 20 pending jobs (these are the ones we just queued)
- [ ] Verify **Active Clients** shows Eli (+ Andrade if exists)
- [ ] Click **Refresh** — no errors in browser console (F12)

If leads don't show:
```sql
-- Run in Supabase SQL editor to verify
SELECT id, name, status, score FROM leads WHERE brand = 'soulhustleai' ORDER BY score DESC;
```

---

## PHASE 3 — Fire The Enrichment Engine (20 min)

Option A — Via script (recommended for tonight):
```bash
cd soulhustleai/scripts
source .env
python3 fire_enrichment.py
```

Option B — Via n8n:
- Import `soulhustleai/automations/n8n/02_hunter_enrichment.json` into n8n
- Activate workflow
- Wait 30 min (runs on cron)

**Watch the Command Center:**
- Enrichment Queue status should flip from `pending` → `running` → `completed`
- Leads that had NULL emails should start showing email addresses
- Should see confidence_score > 0 on enriched_contacts

**Check a specific lead in SQL:**
```sql
SELECT name, email, phone, status FROM leads
WHERE source = 'scrape_nyc_2026-04-03'
ORDER BY score DESC;
```

Target: at least 5-10 of the 20 should have an email discovered after the run.

---

## PHASE 4 — The Gate Webhook Test (10 min)

Open `soulhustleai/website/apply.html` in browser (or deploy to Vercel if you want).

- [ ] Fill out the form with test data: name="Test Edwin", business="Test Corp"
- [ ] Submit

Verify in Supabase:
```sql
SELECT id, name, score, temperature, notes FROM leads
WHERE source = 'website_apply' ORDER BY created_at DESC LIMIT 1;
```

Expected: a new row with score 40-100 and temperature = cold/warm/hot.

You should also receive an SMS alert at your phone within 10 seconds.

---

## PHASE 5 — Call Zero (5 min)

**Dial (929) 236-1567 from your cell.**

- [ ] Zero picks up within 2 rings
- [ ] Introduces himself as "Zero from SoulHustleAI"
- [ ] Asks a qualifying question
- [ ] You give him a fake business (say "TestCorp, plumbing, $500K/yr, missing calls")
- [ ] He offers to text you the Cal.com link
- [ ] You receive the SMS within 15 seconds

If Zero fails:
- Check VAPI dashboard → is the agent ACTIVE?
- Check VAPI phone number mapping
- Check Twilio routing

---

## PHASE 6 — Eli Client Portal (5 min)

Open `soulhustleai/clients/eli/dashboard.html` in browser.

- [ ] Paste Supabase key
- [ ] Verify all 7 workflows show status (LIVE / 10DLC / BUILDING)
- [ ] Verify client row pulls Eli's data
- [ ] No console errors

---

## PHASE 7 — End-to-End Revenue Flow (15 min)

The full loop: **website → apply → score → email → book → close → pay**

1. On `apply.html`: submit as a hot lead (revenue 2M+, timeline "this week")
2. Verify n8n triggered Resend email to your address
3. Verify Cal.com link in the email works (book a slot)
4. Verify webhook from Cal.com creates a `proposal_sent` event on the lead

If ANY step breaks, note it in `soulhustleai/KNOWN-ISSUES.md` and route around it manually.

---

## PHASE 8 — Final Green Check (5 min)

- [ ] Command Center: all panels load, no red errors
- [ ] Enrichment queue: at least 50% completed
- [ ] Lead pipeline: at least 5 leads have emails after enrichment run
- [ ] Twilio: test SMS sent and received
- [ ] VAPI Zero: call picked up and responded
- [ ] n8n: Gate webhook responded within 3 seconds
- [ ] Supabase: writing successfully (new test lead visible)

---

## ✓ IF ALL GREEN
Tomorrow morning → execute `MONEY-TOMORROW.md`.

## ✗ IF RED
Document the blocker in `KNOWN-ISSUES.md`, work around it for tomorrow's launch,
loop back to fix at first break.

**Escalation path:** you → Claude → fix.
Don't try to fix broken infrastructure at 2am on launch night.
Route around, launch, fix in daylight.

---

**Last updated:** 2026-04-13
**Branch:** claude/finish-soulhustle-ai-X6e5Q
