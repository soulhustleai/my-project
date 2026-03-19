# Launch Checklist

## Pre-Launch (Before First Outreach)

### Business Setup
- [ ] Register Florida LLC (FA-001)
- [ ] Open business bank account (FA-002)
- [ ] Get business phone number (Twilio or Google Voice)
- [ ] Set up business email (claims@[domain].com)
- [ ] Create simple landing page / website
- [ ] Draft contingency fee agreement (attorney review recommended)
- [ ] Set up Google Business Profile
- [ ] Get BBB listing (or at minimum, register)

### Tech Setup
- [ ] Create Supabase project
- [ ] Apply database schema (setup_supabase.sql)
- [ ] Set up Lob account + API key
- [ ] Verify Twilio number for SMS (10DLC if needed)
- [ ] Set up Sentry project for error monitoring
- [ ] Set up Railway account for service hosting
- [ ] Configure .env with all API keys

### Source Validation
- [ ] Validate Broward County surplus list source URL + format
- [ ] Validate Palm Beach County surplus list source URL + format
- [ ] Validate Hillsborough County surplus list source URL + format
- [ ] Document access methods in county-source-registry

### Pipeline Build
- [ ] Deploy source-monitor (3 county scrapers)
- [ ] Deploy record-ingestion (PDF parser)
- [ ] Deploy normalization pipeline
- [ ] Deploy opportunity scorer
- [ ] Test: first batch of 20+ leads ingested and scored
- [ ] Set up enrichment (PDL API key or manual process)
- [ ] Test: first 10 leads enriched with contact info
- [ ] Deploy outreach-engine (Lob mail + Twilio SMS)
- [ ] Test: send 1 test letter via Lob
- [ ] Test: send 1 test SMS via Twilio
- [ ] Create Jotform intake form with e-sign

### Templates Ready
- [ ] Mail letter template 1 (initial contact)
- [ ] Mail letter template 2 (follow-up)
- [ ] SMS follow-up template 1
- [ ] SMS follow-up template 2
- [ ] Email follow-up template
- [ ] Contingency agreement (for e-sign)

---

## Launch Day
- [ ] Run source monitor on all 3 counties
- [ ] Ingest and score first full batch
- [ ] Enrich top 25 leads
- [ ] Send first outreach wave (mail via Lob)
- [ ] Schedule SMS follow-ups for Day 5
- [ ] Log everything in Supabase

---

## Post-Launch (Week 1-2)
- [ ] Monitor Lob delivery status
- [ ] Check for inbound responses daily
- [ ] Send Day 5 SMS follow-ups
- [ ] Send Day 8 email follow-ups
- [ ] Send Day 12 second mail
- [ ] Pull next batch of surplus leads
- [ ] Repeat outreach cycle
- [ ] Make phone calls on leads >$10K (Day 16+)

---

## First Signed Client Milestone
- [ ] Intake form completed
- [ ] Agreement signed (e-sign)
- [ ] ID collected
- [ ] Notarization coordinated
- [ ] Case created in Supabase
- [ ] Claim packet generated
- [ ] Claim packet reviewed by founder
- [ ] Claim filed with county
- [ ] Status tracking initiated
