# CROWNED JOB OPS
## The Autonomous W2-to-Throne Pipeline

> **Original pitch name:** SOVEREIGN JOB OPS
> **Renamed to:** CROWNED JOB OPS (per `CLAUDE.md` — "sovereign" has sovereign-citizen baggage, word swap required across all copy)
> **Codename:** CJO
> **Operator:** Edwin | **AI partner:** Claude (Opus 4.6 + Sonnet sub-agents)
> **Mode:** Weekend-sprint build. Monitor-and-collect operation.

---

## WHAT THIS IS

An autonomous job-ops machine built on top of the best ideas from `santifer/career-ops` (8.2K stars, A–F scoring, ATS PDFs, batch parallel Claude evaluation) and welded to Edwin's full stack: **Make.com + Notion + Claude API + Twilio + Gmail MCP + Google Calendar MCP + ElevenLabs + ConvertKit + Later.com**.

career-ops is a terminal power-tool for a developer with 8 hours a day.
**CJO is a living swarm that runs while Edwin is at his W2.**

Edwin approves. Edwin closes. That's it.

---

## WHY CROWNED JOB OPS IS 100× BETTER THAN career-ops

| | `career-ops` | **CROWNED JOB OPS** |
|---|---|---|
| **Trigger** | Manual (`career-ops add <url>`) | Autonomous (6 AM daily Make.com scan) |
| **Intelligence** | Job description only | Job + company health + hiring manager + comp data + interview questions + referral paths |
| **Scoring** | 10 dimensions, static | 14 dimensions, Edwin-weighted, self-learning from outcomes |
| **Agent count** | 1 evaluator | 6-agent swarm (Fit, Health, Comp, Manager, Interview, Referral) + Synthesis |
| **Output** | PDF + markdown file | Full dossier: resume + cover letter + cold email + LinkedIn DM + intel brief + interview angle |
| **Alerting** | None | SMS via Twilio within 5 min of high-score match |
| **Status tracking** | Manual | Gmail MCP auto-detects recruiter replies, updates Notion, SMS Edwin |
| **Interview prep** | None | Calendar-triggered STAR + talk track + objection bank |
| **Warm outreach** | None | Auto-drafts LinkedIn engagement + referral DMs before cold apply |
| **Opsec** | None | Stealth mode — current-employer network monitoring |
| **Learning loop** | None | Rejection autopsy agent updates scoring weights from outcomes |
| **Compensation floor** | None | Dynamic — W2 + SH.AI MRR + GMC + prop trading, recalculated weekly |
| **Persona engine** | One resume | 3 personas (Operator / Fractional Exec / Trilingual Tech Lead) auto-selected |
| **Dual-pipeline** | Jobs only | Jobs **AND** contract gigs routed to SoulHustleAI as client leads |
| **Human hours/week** | 10–20 (manual feeding) | **~2 (review + approve)** |

---

## FILE INDEX

```
career-ops/
├── README.md                        # You are here
├── BLUEPRINT.md                     # The master architecture — 7 phases + sub-agent swarm
├── SCORING-RUBRIC.md                # 14-dimension Edwin-weighted rubric
├── NOTION-SCHEMA.md                 # Notion databases (jobs, companies, contacts, interviews, outcomes)
├── MAKE-SCENARIOS.md                # Make.com scenario specs (HUNT/SCORE/BUILD/TRACK/PREP + 5 support scenarios)
├── BUILD-PLAN.md                    # Weekend-by-weekend execution plan (30 days → 95% autonomy)
└── prompts/                         # Production Claude API prompts
    ├── scoring.md                   # 14-dim fit scoring (Sonnet 4.6)
    ├── build-package.md             # Resume + cover letter + cold email + DM (Sonnet 4.6)
    ├── interview-prep.md            # STAR + talk track + objection bank (Opus 4.6)
    ├── hiring-manager-profile.md    # LinkedIn scrape → profile dossier (Sonnet 4.6)
    └── rejection-autopsy.md         # Post-mortem + scoring-weight updates (Opus 4.6)
```

---

## THE 7 PHASES AT A GLANCE

```
  PHASE 0  │  PHASE 1  │  PHASE 2  │  PHASE 3  │  PHASE 4  │  PHASE 5  │  PHASE 6
  ────────────────────────────────────────────────────────────────────────────────
   FOUNDATION │  HUNT   │  SCORE   │  BUILD   │  WARM    │  TRACK   │  LEARN
  ────────────────────────────────────────────────────────────────────────────────
   Personas   │  6AM    │  6-agent │  Dossier │  Warm    │  Gmail   │  Autopsy
   Rubric     │  scan   │  swarm   │  + SMS   │  before  │  + Cal   │  +
   Floor      │  Dedupe │  Synth   │  Twilio  │  cold    │  MCP     │  Weekly
              │         │          │          │          │          │  review
```

See `BLUEPRINT.md` for full detail on every phase.

---

## THE GOLDEN RULE

> **Every job must be warmed before it's applied to.**

No cold applies. Before CJO submits anything, the system:
1. Drops a valuable LinkedIn comment on the hiring manager's last post
2. Schedules a thought-leadership post aligned with the role (Later.com)
3. Graph-searches for a 2nd-degree connection inside the company
4. Drafts an intro DM to that connection

**Cold applies are dead. Warm-before-cold is the Crowned way.**

---

## STATUS

- [ ] Phase 0 — Foundation (personas, rubric, Notion DBs)
- [ ] Phase 1 — HUNT (Make.com daily scan)
- [ ] Phase 2 — SCORE (6-agent Claude swarm)
- [ ] Phase 3 — BUILD (auto-dossier + SMS)
- [ ] Phase 4 — WARM (LinkedIn engagement + referral paths)
- [ ] Phase 5 — TRACK (Gmail + Calendar MCP)
- [ ] Phase 6 — LEARN (rejection autopsy + weekly review)

See `BUILD-PLAN.md` for the full 4-weekend sprint.
