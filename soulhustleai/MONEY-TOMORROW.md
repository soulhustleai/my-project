# 💰 MONEY TOMORROW
## SoulHustleAI — 24-hour Revenue Execution Playbook

> **Mission:** First paid deal inside 24 hours of launch. Minimum $2,500 build fee collected.
> **Target deals:** Mike (AC contractor) + 3 hot leads from the NYC pipeline.
> **Budget:** $0 ad spend. Pure outreach + existing pipe.

---

## 6AM — MORNING WAR ROOM (20 min)

Open Command Center: `soulhustleai/dashboard/command-center.html`

- [ ] Pull coffee. Dial in focus mode.
- [ ] Verify enrichment ran overnight (queue → completed)
- [ ] Identify **3 hot leads** with:
  - score ≥ 85
  - email discovered (thanks HUNTER)
  - phone valid (thanks numverify)
  - NOT "Pupkin Insurance" or "Z & R Associates" (phones are bad)
- [ ] Copy names + contact info to a scratch pad

Expected hot leads to target:
```
1. Brooklyn Dental Professionals — dental, score 99
2. Harris Plumbing & Heating — plumbing, score 99
3. Concerned Dental Care of the Bronx — dental, score 99
```

Plus existing warm lead: **Mike (AC contractor)** — referred by Eli.

---

## 7AM — MIKE CLOSE ATTEMPT (30 min)

Mike is referred by Eli. Highest conversion probability. Go first.

- [ ] Review `soulhustleai/pitches/mike-ac-contractor.md`
- [ ] Send the pitch via email + text the Loom link
- [ ] Immediately follow up with SMS: "Mike — Edwin. Dropped you a proposal. 72hr discount ends Tuesday. Call me 5 min? (929) 236-1567"
- [ ] Set Cal.com hold for 11am and 3pm

**Expected:** Mike replies within 2 hours. Either books or counter-offers.

**If Mike closes:** $2,025 (50% of $4,500 build) invoiced immediately via Square. DONE. Today is a win.

---

## 8AM — COLD OUTREACH BLAST (60 min)

Fire the cold email sequence at all 10 hot-score enriched leads.

```bash
# Via n8n workflow 03
curl -X POST "$N8N_URL/webhook/shai-cold-blast" \
  -H 'Content-Type: application/json' \
  -d '{"sequence":"cold_email","batch":"morning_blast_2026_04_14","limit":10}'
```

Or manually from `soulhustleai/outreach/cold-email-sequence.md` → Email 1.

- [ ] Blast 10 cold emails (Email 1 only — the hook)
- [ ] Blast 10 cold SMS (SMS 1 — the opener)
- [ ] Wait 90 minutes for replies

**Expected:** 1-2 replies. One of them books.

---

## 9AM — ZERO CALL CAMPAIGN (60 min)

For the top 5 hot leads that haven't replied yet, fire outbound Zero calls:

```bash
# Fire Zero outbound via VAPI
for lead in lead1 lead2 lead3 lead4 lead5; do
  curl -X POST "https://api.vapi.ai/call" \
    -H "Authorization: Bearer $VAPI_API_KEY" \
    -H "Content-Type: application/json" \
    -d "{\"assistantId\":\"$VAPI_ZERO_AGENT_ID\",\"customer\":{\"number\":\"$lead_phone\"}}"
done
```

**Expected:** 3/5 pick up. 1/3 agrees to book. 1 new booked call.

---

## 11AM — FIRST STRATEGY CALL (30-60 min)

If Mike or another hot lead booked → take the call.

**Pre-call checklist:**
- [ ] Review their industry + the BOSSMoves framework
- [ ] Have `pitches/proposal-template.md` open in a tab
- [ ] Have Cal.com / Square / Stripe payment links ready
- [ ] Have the Eli case study ready to reference

**On the call — the 4-step close:**
1. **Mirror their pain** (2 min) — "So you're missing X, not closing Y, losing Z..."
2. **Show the ROI math** (3 min) — "At $X recovery, you pay this off in <30 days"
3. **Offer the tier** (2 min) — "I'm recommending The Empire at $3,497/mo + $4,500 build"
4. **Close** (3 min) — "If we lock this in today I'll knock 10% off the build. Square link right now?"

Collect payment LIVE on the call. Do not let them "think about it."

---

## 12PM — LUNCH + SECOND WAVE (30 min)

- [ ] Email 2 (Eli case study) to all 10 cold leads from morning blast
- [ ] SMS 2 to anyone who opened but didn't reply
- [ ] Re-queue any leads still in `pending_enrichment` from this morning
- [ ] Post 1 TikTok about "The morning I closed my first $4,500 deal in 2 hours" (if you close!)

---

## 2PM — INBOUND PIPELINE REVIEW (30 min)

- [ ] Check Command Center for any new inbound leads (from website, SMS, Zero calls)
- [ ] Respond to every inbound within 15 min
- [ ] Book any warm responders into Cal.com for same-day slots

---

## 3PM — SECOND STRATEGY CALL SLOT

If you have a booking here → take the call. Same 4-step close.

---

## 5PM — DAY RECAP + PIPELINE UPDATE (20 min)

- [ ] Update `soulhustleai/CLIENTS.md` with any new prospects
- [ ] Update Supabase with call outcomes:
  ```sql
  UPDATE leads SET status = 'strategy_call', last_contacted_at = NOW()
  WHERE id IN ('...','...');
  ```
- [ ] Log revenue in `financial_transactions` if any came in
- [ ] Post in ceo_action_log: "Day 1 of launch — X touches, Y responses, Z closed"

---

## REVENUE TARGETS (conservative)

| Scenario | Revenue | Probability |
|----------|---------|-------------|
| Mike closes on proposal | **$2,025** (50% build) | 40% |
| 1 cold lead books + closes | **$2,025** | 25% |
| Zero qualifies 1 → Edwin closes | **$1,250** (System tier) | 30% |
| No close, but 3 booked for this week | **$0 today** | 50% |

**Expected value day 1:** ~$1,800
**Expected cumulative day 7:** ~$9,000

---

## FALLBACK: NO CLOSE BY 6PM

If nothing converts:
1. Don't panic.
2. Pipeline is still alive.
3. Focus on booking — a booked call is 50% closed.
4. Run Email 3 (ROI calculator) blast to all remaining
5. Run SMS 3 (dead lead resurrection) to cold ones
6. Sleep. Execute Day 2 plan tomorrow.

---

## STOP-LOSS RULES

**Don't:**
- Discount past 10% off build (floor is sacred)
- Agree to "I'll pay later" (NO deal starts without payment)
- Chase past 3 touches in 24 hours (let the sequence breathe)
- Skip the Cal.com booking step ("I'll call you tomorrow" = lost)

**Do:**
- Collect payment ON the call, not after
- Text the recap + Loom walkthrough immediately after every call
- Log every interaction in Supabase
- Celebrate the first $2,000 — you earned it

---

**The machine is built. Fire it.**

— 2026-04-14 execution day
