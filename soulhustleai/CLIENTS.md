# SoulHustleAI — Client Tracker

> **Source of truth:** `STATE.md` (synced to Supabase). This file is the human-readable summary.
> **Updated:** 2026-04-13

---

## Active Clients (2)

### 1. Adam Andrade — Andrade Health Services  `first client`
- **Business:** Health Insurance advisory
- **Location:** Florida
- **Package:** AEGIS Partner — $0/mo + 25% commission rev-share
- **Status:** ACTIVE (go-live 2026-04-04)
- **Phone:** (407) 561-2878
- **Email:** Deandradehealthadvisor@gmail.com
- **Supabase id:** `01b17786-a57f-4034-a150-19231c617b51`
- **Live systems:** aegis.soulhustleai.com, health.soulhustleai.com, 5/10 workflows active, 197 leads in pipeline
- **Dashboard:** `clients/andrade/dashboard.html`
- **Runbook:** `clients/andrade/onboarding.md`
- **Blockers:**
  - [ ] Build workflows 06-10 (priority for month)
  - [ ] Wire Stripe Connect for commission payouts
  - [ ] First rev-share settlement calculation due end of month

### 2. Eli — Abundantly Blessed Solutions  `first paying client`
- **Business:** Junk removal / moving
- **Location:** South Florida
- **Package:** Foundation — $400/mo (pre-Catalyst grandfather deal)
- **Status:** ACTIVE (paid offline, Stripe wiring pending)
- **Phone:** +1 (954) 218-9947
- **Email:** (needs capture)
- **Supabase id:** `0554fcd6-9f7e-42d1-8a59-8eefe65b5abc`
- **Twilio Number:** +1 (844) 643-9825 (toll-free, 10DLC pending)
- **Workflows:** 7 built (5 live, 2 building, workflow 02 pending 10DLC)
- **Dashboard:** `clients/eli/dashboard.html`
- **Runbook:** `clients/eli/onboarding.md`
- **Blockers:**
  - [ ] Twilio 10DLC carrier approval (ETA 24-72hr)
  - [ ] client_onboarding stalled at day 0 — Edwin must manually trigger
  - [ ] Stripe customer record (paid offline, needs webhook)
  - [ ] Capture email (currently NULL in Supabase)

---

## Hot Prospects (1)

### Mike — RTS Appliance `urgent close`
- **Business:** Appliance repair
- **Status:** PROSPECT — pitch sent, close target **2026-04-14 (tomorrow)**
- **Recommended:** System tier +$100 white-glove boost = **$797/mo** + $697 deposit
- **Stripe link:** https://buy.stripe.com/8x2eVd5n3edU0HT9MP73G01
- **Expected Year 1:** $10,261 revenue, ~9x ROI for Mike
- **Pitch file:** `pitches/mike-rts-appliance.md`
- **CEO task:** "Close Mike — RTS Appliance $797/mo" (originally due 2026-03-28, slipped — now urgent)

---

## Enrichment Queue (20 leads — reset 2026-04-13)

**Previously mislabeled** as `contacted`/`enriched` in Supabase. None were ever actually
contacted. Reset to `pending_enrichment` and re-queued through the enrichment engine.

### Score 99 (hot)
1. Brooklyn Dental Professionals — (718) 486-7600
2. Concerned Dental Care of the Bronx — (718) 652-7370
3. Harris Plumbing & Heating — (718) 495-3400
4. BarberSpa BK — (929) 479-3900
5. Brooklyn Cleaning Services — (929) 656-6456
6. Cleaning Brooklyn — (929) 656-6456 (dup phone with #5 — dedupe)
7. Neuhaus Realty — (718) 979-3400
8. Pupkin Insurance — (866) 273-6369 (phone may be bad)
9. Regency Agency Inc — (718) 377-0566
10. Sammy Brokerage Inc — (718) 204-1555
11. Z & R Associates — (316) 943-2683 (out-of-area phone)

### Score 88 (warm)
- Brooklyn Law Group — (212) 561-4299
- Crown Heights Plumbing — (929) 297-6869
- Fresh Start Cleaning NYC — (650) 435-9118
- Innovative Health Dental — (212) 269-2949
- Queens Tax Services — (917) 300-4737

### Score 77 (watch)
- Luxe Glow Med Spa — (phone TBD)
- Metro General Insurance — (347) 709-4520
- Smart Apple Insurance — (718) 523-5353
- Sunset Park Realty — (phone TBD)

---

## Package Tiers (current — matches Supabase)

| Tier | Deposit | Monthly | Build | Target |
|------|---------|---------|-------|--------|
| Catalyst | $297 | $297 | 48hr | Solo / <$300K |
| System | $697 | $697 | 7 days | 3-10 emp / $300K-$1M |
| System+White-Glove (Mike) | $697 | $797 | 7 days | Priority service biz |
| Empire | $1,497 | $1,497 | 14 days | 10+ emp / $1M+ |
| Sovereign | Custom | $3K-$10K+ | 21-60 days | Enterprise / multi-location |

---

## Revenue Targets

| Window | MRR Target | Current |
|--------|-----------|---------|
| Today | $400 | $400 (Eli) |
| Tomorrow (Mike closes) | $1,197 | — |
| Week 1 (Mike + 2 hot NYC leads) | $3K | — |
| Phase 1 ceiling | $5,000 MRR | — |
| Phase 2 ceiling | $25,000 MRR | — |

---

## Pipeline Goals

- **Close Mike tomorrow** (urgent, slipped task)
- **Fire 10 cold emails + 10 SMS** to enriched NYC leads (see `MONEY-TOMORROW.md`)
- **Book 3 strategy calls** for this week
- **Eli 10DLC lands** → SMS workflows flip to full green
- **Adam workflows 06-10** built this month

---

**See also:**
- `STATE.md` — Supabase snapshot
- `TONIGHT-TEST-PLAN.md` — e2e verification
- `MONEY-TOMORROW.md` — revenue execution playbook
- `pitches/mike-rts-appliance.md` — ready-to-send Mike proposal
