# Grants & Benefits Automation System

**Autonomous benefits discovery, eligibility screening, and application engine.**

Built for Typically Not Lifestyle LLC / Edwin — to automatically find and apply for every grant, benefit, housing program, tax credit, and free resource available.

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    GRANTS-BENEFITS ENGINE                     │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐   │
│  │  Benefits     │  │  Grants      │  │  Housing         │   │
│  │  Screener     │  │  Scanner     │  │  Finder          │   │
│  │              │  │              │  │                  │   │
│  │ • SNAP       │  │ • grants.gov │  │ • HUD Section 8  │   │
│  │ • Medicaid   │  │ • SBA/SBIR   │  │ • USDA Rural     │   │
│  │ • LIHEAP     │  │ • State      │  │ • FHA Loans      │   │
│  │ • Lifeline   │  │ • Minority   │  │ • Down Payment   │   │
│  │ • ACP        │  │ • CDFI       │  │ • First-Time     │   │
│  │ • EITC       │  │ • MBDA       │  │ • Habitat        │   │
│  │ • WIC        │  │ • Foundation │  │ • Tax Credits    │   │
│  └──────┬───────┘  └──────┬───────┘  └────────┬─────────┘   │
│         │                 │                    │              │
│         └────────┬────────┴────────────────────┘              │
│                  ▼                                            │
│  ┌──────────────────────────────────────────────────────┐    │
│  │              Eligibility Engine                        │    │
│  │  • Profile matching against program requirements      │    │
│  │  • Income/household/location/business eligibility     │    │
│  │  • Priority scoring (amount × likelihood × effort)    │    │
│  └──────────────────────┬───────────────────────────────┘    │
│                         ▼                                     │
│  ┌──────────────────────────────────────────────────────┐    │
│  │              Application Engine                       │    │
│  │  • Auto-fill applications with profile data           │    │
│  │  • Document checklist generation                      │    │
│  │  • Submission tracking & follow-up                    │    │
│  │  • Deadline monitoring                                │    │
│  └──────────────────────┬───────────────────────────────┘    │
│                         ▼                                     │
│  ┌──────────────────────────────────────────────────────┐    │
│  │              Notification Engine                      │    │
│  │  • New opportunity alerts                             │    │
│  │  • Deadline reminders                                 │    │
│  │  • Status updates                                     │    │
│  │  • Weekly digest reports                              │    │
│  └──────────────────────────────────────────────────────┘    │
│                                                               │
├─────────────────────────────────────────────────────────────┤
│  Storage: Supabase │ Automation: Make.com │ AI: Claude API   │
└─────────────────────────────────────────────────────────────┘
```

## Services

| Service | Purpose | Status |
|---------|---------|--------|
| `benefits_screener` | Screen 50+ federal/state benefit programs | Active |
| `grants_scanner` | Search grants.gov, SBA, state, foundation grants | Active |
| `housing_finder` | Find housing assistance, down payment, Section 8 | Active |
| `eligibility_engine` | Match profile against all program requirements | Active |
| `application_engine` | Auto-fill, track, and submit applications | Active |
| `notification_engine` | Alerts, reminders, weekly digests | Active |

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Set up environment
cp .env.example .env
# Fill in your details in .env

# Run the full scan
python -m scripts.run_full_scan

# Run specific service
python -m services.grants_scanner.scanner
python -m services.benefits_screener.screener
python -m services.housing_finder.finder
```
