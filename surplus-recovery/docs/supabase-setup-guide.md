# Supabase Setup Guide — Step by Step

## What Is Supabase

Supabase is a hosted Postgres database with a built-in API. It's where all your leads, cases, and pipeline data will live. Free tier is more than enough for MVP.

---

## Step 1: Create Account (2 min)

1. Go to **https://supabase.com**
2. Click **Start your project** (or Sign Up)
3. Sign up with GitHub or email
4. Free plan is fine — don't enter payment info

---

## Step 2: Create Project (2 min)

1. Click **New Project**
2. Enter:
   - **Name:** `surplus-recovery` (or whatever you want)
   - **Database Password:** Choose a strong password — **SAVE THIS, you'll need it**
   - **Region:** East US (closest to Florida)
3. Click **Create new project**
4. Wait ~2 minutes for it to provision

---

## Step 3: Get Your Keys (1 min)

1. In your project dashboard, click **Settings** (gear icon) in the left sidebar
2. Click **API** under Configuration
3. You need TWO things:
   - **Project URL** — looks like `https://abcdefg.supabase.co`
   - **Service Role Key** (under "service_role" — the secret one, NOT the anon key)
4. Copy both and put them in your `.env` file:
   ```
   SUPABASE_URL=https://your-project-id.supabase.co
   SUPABASE_SERVICE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
   ```

**IMPORTANT:** The service role key bypasses all security. Never commit it to git or share it publicly.

---

## Step 4: Create Tables (3 min)

1. In the left sidebar, click **SQL Editor**
2. Click **New query**
3. Open the file `surplus-recovery/scripts/setup_supabase.sql` from this repo
4. Copy ALL the SQL content and paste it into the SQL editor
5. Click **Run** (or Ctrl+Enter)
6. You should see "Success. No rows returned" for each statement
7. If any errors appear, they'll tell you exactly which line — usually a typo

---

## Step 5: Verify Tables (1 min)

1. Click **Table Editor** in the left sidebar
2. You should see all 10 tables:
   - `county_sources`
   - `raw_downloads`
   - `raw_records`
   - `opportunities`
   - `claimants`
   - `outreach_events`
   - `cases`
   - `documents`
   - `notifications`
   - `audit_log`
3. Click any table to see its columns — should match the schema

---

## Step 6: Seed County Sources (1 min)

After your `.env` file has the Supabase URL and key:

```bash
cd surplus-recovery
pip install supabase python-dotenv
python scripts/seed_sources.py
```

This adds the initial Florida county source configs to the `county_sources` table.

---

## That's It

Total time: ~10 minutes. Your database is ready.

The pipeline scripts will now be able to read/write to Supabase using the API keys in your `.env` file.

---

## If Something Goes Wrong

- **"relation already exists"** — Tables were already created. Safe to ignore.
- **"permission denied"** — Make sure you're using the service_role key, not the anon key.
- **Can't connect from Python** — Check that SUPABASE_URL doesn't have a trailing slash.
- **Tables look empty** — That's normal! Data comes from running the pipeline.
