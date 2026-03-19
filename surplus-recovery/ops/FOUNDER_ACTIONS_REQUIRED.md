# Founder Actions Required

These are the ONLY things you (Edwin) need to do manually.
Everything else is automated.

---

## PRIORITY 1 — Do These TODAY (15 min total)

### 1. Create Supabase Tables (5 min)
The database tables aren't created yet. The SQL is ready.

**Steps:**
1. Open `surplus-recovery/scripts/setup_tables_browser.html` in your browser
2. Enter your Supabase service key
3. Click "CREATE ALL TABLES" — it copies the SQL and opens the SQL Editor
4. Paste (Ctrl+V) in the SQL Editor → Click "Run"
5. Come back and click "CHECK TABLE STATUS" to verify

**After this:** Run `python scripts/load_leads_to_supabase.py` to load 248 real leads.

### 2. Set Up Lob Billing Address (3 min)
Your Lob API key works but needs a billing address to send real mail.

**Steps:**
1. Log into https://dashboard.lob.com
2. Go to Settings → Billing
3. Add your business address for Typically Not Lifestyle LLC
4. Done — the outreach engine will handle the rest

### 3. Add Twilio Credentials to .env (2 min)
You have Twilio from SoulHustleAI. Just paste the creds.

**Edit `surplus-recovery/.env` and fill in:**
```
TWILIO_ACCOUNT_SID=your_sid_here
TWILIO_AUTH_TOKEN=your_token_here
TWILIO_PHONE_NUMBER=+1XXXXXXXXXX
```

### 4. Add Anthropic API Key to .env (1 min)
You use Claude already. Just paste the key.

**Edit `surplus-recovery/.env` and fill in:**
```
ANTHROPIC_API_KEY=sk-ant-...
```

---

## PRIORITY 2 — Do This Week

### 5. Set Up Business Email on soulhustleai.com (10 min)
Needed for: People Data Labs signup, outreach credibility, CAN-SPAM compliance.

**Options:**
- Google Workspace ($6/mo) — best for automation
- Zoho Mail (free tier) — good enough to start
- Your domain registrar may offer email forwarding

**Create:** `hello@soulhustleai.com` or `claims@soulhustleai.com`

### 6. Sign Up for People Data Labs (5 min)
Once you have a work email, sign up at https://www.peopledatalabs.com/
Free tier gives 100 enrichments/month — enough to start.

**After signup:** Add `PDL_API_KEY=your_key` to `.env`

---

## PRIORITY 3 — Before First Outreach

### 7. Get Contingency Agreement Reviewed ($200-500)
Template is at `surplus-recovery/templates/documents/contingency_agreement.md`
Have a FL attorney review before sending to any claimants.

### 8. Set Up Notary Access
Surplus claims require notarized documents. Options:
- Notarize.com ($25/session, remote)
- Local UPS Store / bank

---

## What's Already Done (You Don't Need to Touch)
- ✅ 248 leads scraped from Brevard & Sumter counties ($2.84M surplus)
- ✅ 33 leads have names + addresses ready for outreach
- ✅ Supabase project connected (just needs tables created)
- ✅ Lob API key configured (just needs billing address)
- ✅ Full pipeline code: scraping → parsing → scoring → enrichment → outreach
- ✅ Letter templates, SMS templates, email templates
- ✅ Scoring algorithm (0-100 scale)
- ✅ 7-touch outreach sequence configured
