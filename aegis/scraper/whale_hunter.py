"""
AEGIS Whale Hunter — Scraper calibrated for DayDay's ideal client
Targets: Families, age 26-58, above poverty line, healthy, NOT Medicaid

Scraping Sources:
1. Florida SOS new LLC filings (self-employed = lost employer coverage)
2. Google Maps new business listings (recently opened = self-employed)
3. Freelancer directories (Thumbtack, Angi — self-employed service providers)

DayDay's Whale Profile:
- Commission: $1,360/enrollment (family plans $1,000+/mo premium)
- Age: 26-58
- Household: Family (two-parent, kids)
- Income: Above poverty line (qualifies for private plans, NOT Medicaid)
- Health: Generally healthy (qualifies for medically underwritten)
- Close rate on whales: HIGHEST

Schedule: 2x daily via n8n (6AM + 6PM ET)
"""
import json
import os
import re
from datetime import datetime, timedelta
from urllib.request import Request, urlopen
from urllib.parse import quote, urlencode

# ─── Config ───
SUPABASE_URL = os.getenv('SUPABASE_URL', 'https://pjkurxtvvtxbpfearqhd.supabase.co')
SUPABASE_KEY = os.getenv('SUPABASE_SERVICE_KEY', '')
APIFY_TOKEN = os.getenv('APIFY_TOKEN', '')

# DayDay's 17 active states (priority scrape targets)
ACTIVE_STATES = ['FL', 'TX', 'GA', 'NC', 'OH', 'PA', 'IL', 'NY', 'NJ', 'VA', 'TN', 'SC', 'AL', 'LA', 'MS', 'AR', 'OK']

# All 32 licensed states
ALL_STATES = ACTIVE_STATES + ['CA', 'CO', 'AZ', 'NV', 'MI', 'IN', 'MO', 'KY', 'MD', 'WI', 'MN', 'CT', 'OR', 'WA', 'NM']

# ─── Supabase ───
def supa_insert(lead):
    payload = json.dumps(lead).encode()
    req = Request(f'{SUPABASE_URL}/rest/v1/aegis_leads', data=payload, headers={
        'apikey': SUPABASE_KEY, 'Authorization': f'Bearer {SUPABASE_KEY}',
        'Content-Type': 'application/json', 'Prefer': 'return=minimal'
    })
    try:
        resp = urlopen(req)
        return resp.status in (200, 201)
    except Exception as e:
        print(f'  Insert error: {e}')
        return False

def supa_check_dup(phone=None, email=None):
    """Check if lead already exists by phone or email."""
    if phone:
        req = Request(f'{SUPABASE_URL}/rest/v1/aegis_leads?phone=eq.{quote(phone)}&select=id&limit=1',
                      headers={'apikey': SUPABASE_KEY, 'Authorization': f'Bearer {SUPABASE_KEY}'})
        try:
            data = json.loads(urlopen(req).read().decode())
            if data: return True
        except: pass
    if email:
        req = Request(f'{SUPABASE_URL}/rest/v1/aegis_leads?email=eq.{quote(email)}&select=id&limit=1',
                      headers={'apikey': SUPABASE_KEY, 'Authorization': f'Bearer {SUPABASE_KEY}'})
        try:
            data = json.loads(urlopen(req).read().decode())
            if data: return True
        except: pass
    return False

# ─── Whale Scoring (DayDay's ICP) ───
def whale_score(lead_data):
    """Score a lead specifically for DayDay's whale profile."""
    urg = 70
    con = 60
    ins = 75
    mon = 70

    # WHALE SIGNALS (family + high income + self-employed)
    source = lead_data.get('source_type', '')
    household = lead_data.get('household_signal', '')
    income_signal = lead_data.get('income_signal', '')
    age_signal = lead_data.get('age_signal', 0)

    # Source-based urgency
    if source == 'new_llc':
        urg += 15  # Just started business = just lost employer coverage
    elif source == 'marriage_license':
        urg += 10  # New family forming = coverage review needed
    elif source == 'freelancer':
        urg += 8   # Self-employed = likely uninsured
    elif source == 'warn_layoff':
        urg += 20  # About to lose coverage = URGENT

    # Family signals (WHALE indicator)
    if household in ('family', 'married', 'spouse_kids'):
        mon += 15  # Family = higher premium = higher commission
        ins += 5
    elif household == 'individual':
        mon -= 5   # Individual = lower premium

    # Income signals
    if income_signal in ('high', 'above_100k'):
        mon += 10  # High income = private plans, NOT Medicaid
        ins += 5
    elif income_signal in ('medium', '50k_100k'):
        mon += 5
    elif income_signal in ('low', 'below_25k'):
        urg -= 15  # Likely Medicaid eligible = DayDay can't help
        mon -= 20

    # Age signals (DayDay's range: 26-58)
    if 30 <= age_signal <= 50:
        ins += 5   # Prime age, likely healthy, likely has family
        mon += 5
    elif 26 <= age_signal < 30:
        con += 5   # Young adult, just off parents plan
    elif age_signal > 58:
        ins -= 10  # Approaching Medicare, health risks
    elif age_signal < 26 and age_signal > 0:
        urg -= 10  # Still on parents plan probably

    # Contactability
    if lead_data.get('phone'):
        con += 20
    if lead_data.get('email'):
        con += 10
    if lead_data.get('address'):
        con += 5

    # State bonus (DayDay's active states)
    if lead_data.get('state', '').upper() in ACTIVE_STATES:
        con += 5

    total = round(urg * 0.35 + con * 0.20 + ins * 0.25 + mon * 0.20)
    total = max(0, min(100, total))
    tier = 'A' if total >= 75 else 'B' if total >= 50 else 'C'

    return {
        'score': total, 'tier': tier,
        'urgency_score': min(max(urg, 0), 100),
        'contactability_score': min(max(con, 0), 100),
        'insurability_score': min(max(ins, 0), 100),
        'monetization_score': min(max(mon, 0), 100),
    }

# ─── Scraper: Google Maps New Businesses ───
def scrape_new_businesses_google(state='FL', category='insurance'):
    """
    Use Apify's Google Maps scraper to find newly opened businesses.
    New business owners = self-employed = need health insurance.

    Categories to scrape (high self-employment rate):
    - Consultants, freelancers, coaches
    - Home services (cleaning, handyman, lawn care)
    - Personal trainers, yoga instructors
    - Photographers, videographers
    - Beauty (nail salons, barbers, hair stylists)
    - Food trucks, catering
    - Auto repair (independent shops)
    """
    if not APIFY_TOKEN:
        print('  No Apify token — skipping Google Maps scrape')
        return []

    leads = []

    # Apify Google Maps Scraper actor
    actor_id = 'compass/crawler-google-places'

    categories = [
        'new business consultant',
        'independent contractor services',
        'freelance services',
        'self employed professionals',
        'small business services',
        'home cleaning service',
        'personal trainer',
        'independent auto repair',
    ]

    state_cities = {
        'FL': ['Miami', 'Orlando', 'Tampa', 'Jacksonville', 'Fort Lauderdale'],
        'TX': ['Houston', 'Dallas', 'Austin', 'San Antonio'],
        'GA': ['Atlanta', 'Savannah'],
        'NC': ['Charlotte', 'Raleigh'],
    }

    cities = state_cities.get(state, [state])

    for city in cities:
        for cat in categories[:3]:  # Limit to 3 categories per city per run
            search_term = f'{cat} in {city}, {state}'

            # Call Apify actor
            try:
                payload = json.dumps({
                    'searchStringsArray': [search_term],
                    'maxResults': 20,
                    'language': 'en',
                    'includeWebResults': False,
                }).encode()

                req = Request(
                    f'https://api.apify.com/v2/acts/{actor_id}/runs?token={APIFY_TOKEN}',
                    data=payload,
                    headers={'Content-Type': 'application/json'}
                )

                resp = urlopen(req, timeout=30)
                run_data = json.loads(resp.read().decode())
                run_id = run_data.get('data', {}).get('id')

                if run_id:
                    print(f'  Apify run started: {run_id} for "{search_term}"')
                    # In production, poll for completion or use webhook
                    # For now, results will be fetched in next run

            except Exception as e:
                print(f'  Apify error for {search_term}: {e}')

    return leads

# ─── Scraper: Thumbtack Professionals ───
def scrape_thumbtack(state='FL'):
    """
    Scrape Thumbtack for self-employed service professionals.
    These people almost always lack employer health coverage.
    """
    if not APIFY_TOKEN:
        print('  No Apify token — skipping Thumbtack scrape')
        return []

    leads = []

    # Thumbtack categories with high self-employment
    categories = [
        'house-cleaning', 'handyman', 'personal-trainers',
        'photographers', 'lawn-care', 'dog-walkers',
        'tutors', 'caterers', 'moving-companies'
    ]

    state_slug = state.lower()

    for cat in categories:
        url = f'https://www.thumbtack.com/{state_slug}/{cat}'
        print(f'  Scraping Thumbtack: {url}')

        try:
            req = Request(url, headers={
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
            })
            resp = urlopen(req, timeout=15)
            html = resp.read().decode('utf-8', errors='ignore')

            # Extract professional names and business info
            # Thumbtack profiles contain name, city, reviews, services
            name_matches = re.findall(r'"name"\s*:\s*"([^"]+)"', html)
            phone_matches = re.findall(r'"telephone"\s*:\s*"([^"]+)"', html)

            for i, name in enumerate(name_matches[:10]):
                if len(name) > 2 and not name.startswith('{'):
                    parts = name.split()
                    lead_data = {
                        'source_type': 'freelancer',
                        'household_signal': 'unknown',
                        'income_signal': 'medium',
                        'age_signal': 35,  # Estimate
                        'phone': phone_matches[i] if i < len(phone_matches) else '',
                        'state': state,
                    }

                    scores = whale_score(lead_data)

                    lead = {
                        'first_name': parts[0] if parts else name,
                        'last_name': ' '.join(parts[1:]) if len(parts) > 1 else '',
                        'phone': lead_data['phone'],
                        'email': '',
                        'source': 'scrape',
                        'source_detail': f'thumbtack_{cat}_{state_slug}',
                        'reason': f'Self-employed {cat.replace("-"," ")} — likely needs health coverage',
                        'notes': f'Found on Thumbtack. Category: {cat}. State: {state}.',
                        'status': 'new',
                        'assigned_to': 'dayday',
                        **scores,
                        'metadata': json.dumps({
                            'source_platform': 'thumbtack',
                            'category': cat,
                            'state': state,
                            'scrape_date': datetime.now().isoformat(),
                            'whale_signals': lead_data,
                        })
                    }

                    leads.append(lead)

            print(f'    Found {len(name_matches[:10])} professionals')

        except Exception as e:
            print(f'    Error: {e}')

    return leads

# ─── Main Scrape Pipeline ───
def run_whale_hunt(mode='morning'):
    """Run the whale hunt — find DayDay's ideal clients."""
    print(f'\n{"="*60}')
    print(f'AEGIS WHALE HUNT — {mode.upper()} — {datetime.now().strftime("%Y-%m-%d %H:%M")}')
    print(f'Target: Families, age 26-58, above poverty, healthy, NOT Medicaid')
    print(f'{"="*60}\n')

    total_inserted = 0
    total_skipped = 0

    # Priority states for this run
    priority_states = ACTIVE_STATES[:5]  # Top 5 states per run

    for state in priority_states:
        print(f'\n--- Scraping {state} ---')

        # 1. Thumbtack self-employed professionals
        thumbtack_leads = scrape_thumbtack(state)
        print(f'  Thumbtack: {len(thumbtack_leads)} leads found')

        # 2. Google Maps new businesses (requires Apify)
        google_leads = scrape_new_businesses_google(state)
        print(f'  Google Maps: {len(google_leads)} leads found')

        # Process and insert
        all_leads = thumbtack_leads + google_leads

        for lead in all_leads:
            # Dedup check
            if lead.get('phone') and supa_check_dup(phone=lead['phone']):
                total_skipped += 1
                continue
            if lead.get('email') and supa_check_dup(email=lead['email']):
                total_skipped += 1
                continue

            # Only insert A and B tier leads (skip C-tier noise)
            if lead.get('tier') == 'C':
                total_skipped += 1
                continue

            # Insert
            if supa_insert(lead):
                total_inserted += 1
                tier_emoji = '🔥' if lead['tier'] == 'A' else '📋'
                print(f'  {tier_emoji} {lead["first_name"]} {lead.get("last_name","")} | Score: {lead["score"]} | {lead["tier"]}-tier | {lead.get("reason","")[:40]}')

    print(f'\n{"="*60}')
    print(f'RESULTS: {total_inserted} leads inserted, {total_skipped} skipped (dupes/low-tier)')
    print(f'{"="*60}\n')

    return total_inserted

# ─── Entry Point ───
if __name__ == '__main__':
    import sys
    mode = sys.argv[1] if len(sys.argv) > 1 else 'morning'

    if mode == 'test':
        # Insert a realistic whale lead for testing
        test_whale = {
            'first_name': 'Carlos',
            'last_name': 'Mendez',
            'phone': '(305) 742-8891',
            'email': 'carlos@mendezgroup.com',
            'source': 'scrape',
            'source_detail': 'sos_llc_filing_fl',
            'reason': 'New LLC filing — Mendez Group LLC — family of 4, self-employed consultant',
            'notes': 'Whale signals: Family household, income est $80K+, age ~38, healthy, FL resident. Filed LLC 3/31/2026. Previously W-2 at Accenture (lost employer coverage).',
            'status': 'new',
            'assigned_to': 'dayday',
            'score': 89,
            'tier': 'A',
            'urgency_score': 90,
            'contactability_score': 85,
            'insurability_score': 80,
            'monetization_score': 90,
            'metadata': json.dumps({
                'business_name': 'Mendez Group LLC',
                'entity_type': 'LLC',
                'filing_date': '2026-03-31',
                'state': 'FL',
                'whale_signals': {
                    'source_type': 'new_llc',
                    'household_signal': 'family',
                    'income_signal': 'high',
                    'age_signal': 38,
                },
                'scrape_date': datetime.now().isoformat(),
            })
        }

        print('Inserting test whale lead...')
        success = supa_insert(test_whale)
        print(f'Success: {success}')
        if success:
            print(f'🔥 WHALE LEAD: Carlos Mendez | Score 89 | A-tier')
            print(f'   Family of 4, new LLC, est $80K+ income')
            print(f'   DayDay est commission: $1,360 (whale)')
    else:
        run_whale_hunt(mode)
