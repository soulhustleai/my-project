"""
AEGIS ELITE SCRAPER — The Best Health Insurance Lead Scraper in the Industry

Multi-source, trigger-based lead generation targeting DayDay's whale profile:
- Families, age 26-58, above poverty line, healthy, NOT Medicaid
- Commission: $1,360/enrollment (whale) vs $816 (regular)

Sources (Priority Order):
1. Florida SOS — New LLC filings (self-employed = lost employer coverage)
2. Google Maps — New/small businesses in target cities
3. LinkedIn — Recently self-employed professionals (via Apify)
4. Indeed — "No benefits" job postings (people taking these jobs need insurance)
5. Reddit — Intent signals from insurance-related subreddits

Schedule: 2x daily (6AM + 6PM ET) via n8n on Railway
"""
import json
import os
import re
import time
from datetime import datetime, timedelta
from urllib.request import Request, urlopen
from urllib.parse import quote, urlencode

# ─── Config ───
SUPABASE_URL = os.getenv('SUPABASE_URL', 'https://pjkurxtvvtxbpfearqhd.supabase.co')
SUPABASE_KEY = os.getenv('SUPABASE_SERVICE_KEY', '')
APIFY_TOKEN = os.getenv('APIFY_TOKEN', '')

# DayDay's active states
ACTIVE_STATES = ['FL', 'TX', 'GA', 'NC', 'OH', 'PA', 'IL', 'NY', 'NJ', 'VA', 'TN', 'SC', 'AL', 'LA', 'MS', 'AR', 'OK']

# Target cities per state (top cities with highest self-employment)
TARGET_CITIES = {
    'FL': ['Miami', 'Orlando', 'Tampa', 'Jacksonville', 'Fort Lauderdale', 'West Palm Beach', 'St Petersburg'],
    'TX': ['Houston', 'Dallas', 'Austin', 'San Antonio', 'Fort Worth'],
    'GA': ['Atlanta', 'Marietta', 'Savannah'],
    'NC': ['Charlotte', 'Raleigh', 'Durham'],
}

# ─── Supabase Helpers ───
def supa_insert(lead):
    payload = json.dumps(lead).encode()
    req = Request(f'{SUPABASE_URL}/rest/v1/aegis_leads', data=payload, headers={
        'apikey': SUPABASE_KEY, 'Authorization': f'Bearer {SUPABASE_KEY}',
        'Content-Type': 'application/json', 'Prefer': 'return=minimal'
    })
    try:
        return urlopen(req).status in (200, 201)
    except Exception as e:
        if 'duplicate' not in str(e).lower() and '409' not in str(e):
            print(f'    Insert error: {str(e)[:100]}')
        return False

def supa_check_phone(phone):
    if not phone: return False
    req = Request(f'{SUPABASE_URL}/rest/v1/aegis_leads?phone=eq.{quote(phone)}&select=id&limit=1',
                  headers={'apikey': SUPABASE_KEY, 'Authorization': f'Bearer {SUPABASE_KEY}'})
    try:
        return len(json.loads(urlopen(req).read().decode())) > 0
    except: return False

# ─── Whale Scoring ───
def whale_score(source_type, signals={}):
    urg, con, ins, mon = 70, 60, 75, 70

    # Source-based urgency
    source_boosts = {
        'new_llc': 15, 'warn_layoff': 20, 'marriage': 10,
        'freelancer': 8, 'no_benefits_job': 12, 'self_employed': 10,
        'gig_worker': 8, 'turning_26': 15, 'reddit_intent': 5,
    }
    urg += source_boosts.get(source_type, 0)

    # Family signals
    if signals.get('household') in ('family', 'married', 'spouse_kids'):
        mon += 15; ins += 5
    # Income signals
    if signals.get('income') in ('high', 'above_100k'):
        mon += 10; ins += 5
    elif signals.get('income') in ('low', 'below_25k'):
        urg -= 15; mon -= 20
    # Age
    age = signals.get('age', 35)
    if 30 <= age <= 50: ins += 5; mon += 5
    # Contactability
    if signals.get('phone'): con += 20
    if signals.get('email'): con += 10
    if signals.get('state', '').upper() in ACTIVE_STATES: con += 5

    total = round(urg * 0.35 + con * 0.20 + ins * 0.25 + mon * 0.20)
    total = max(0, min(100, total))
    tier = 'A' if total >= 75 else 'B' if total >= 50 else 'C'
    return {'score': total, 'tier': tier,
            'urgency_score': min(max(urg,0),100), 'contactability_score': min(max(con,0),100),
            'insurability_score': min(max(ins,0),100), 'monetization_score': min(max(mon,0),100)}

# ─── Apify Runner ───
def run_apify_actor(actor_id, input_data, wait_secs=120):
    """Run an Apify actor and return results."""
    if not APIFY_TOKEN:
        return []

    try:
        payload = json.dumps(input_data).encode()
        req = Request(
            f'https://api.apify.com/v2/acts/{actor_id}/runs?token={APIFY_TOKEN}&waitForFinish={wait_secs}',
            data=payload, headers={'Content-Type': 'application/json'}
        )
        resp = urlopen(req, timeout=wait_secs + 30)
        run = json.loads(resp.read().decode())
        dataset_id = run.get('data', {}).get('defaultDatasetId')

        if not dataset_id:
            return []

        # Fetch results
        req2 = Request(f'https://api.apify.com/v2/datasets/{dataset_id}/items?token={APIFY_TOKEN}&limit=50')
        resp2 = urlopen(req2, timeout=30)
        return json.loads(resp2.read().decode())

    except Exception as e:
        print(f'    Apify error: {str(e)[:100]}')
        return []

# ═══════════════════════════════════════════
# SOURCE 1: Google Maps — Self-Employed Businesses
# ═══════════════════════════════════════════
def scrape_google_maps(state='FL', max_per_city=15):
    """Find self-employed business owners via Google Maps."""
    leads = []
    cities = TARGET_CITIES.get(state, [state])

    # Searches that find INDIVIDUALS who are self-employed (not chains/corporations)
    whale_queries = [
        'independent contractor',
        'freelance consultant',
        'sole proprietor',
        'self employed professional',
        'home based business',
        'personal trainer',
        'independent photographer',
        'mobile notary',
        'independent insurance',  # Other agents = referral partners
        'life coach',
        'independent real estate agent',
        'mobile mechanic',
    ]

    for city in cities[:3]:  # Limit cities per run
        for query in whale_queries[:4]:  # Limit queries per city
            search = f'{query} {city} {state}'
            print(f'  Google Maps: "{search}"')

            results = run_apify_actor('compass~crawler-google-places', {
                'searchStringsArray': [search],
                'maxCrawledPlacesPerSearch': max_per_city,
                'language': 'en',
                'maxImages': 0,
                'includeHistogram': False,
                'includeOpeningHours': False,
                'includePeopleAlsoSearch': False,
            }, wait_secs=90)

            for item in results:
                title = item.get('title', '')
                phone = item.get('phone', '')
                biz_city = item.get('city', city)

                if not phone or not title:
                    continue
                # Skip chains and large companies
                if any(x in title.lower() for x in ['walmart','target','cvs','walgreens','bank of','wells fargo','chase','starbucks','mcdonald']):
                    continue
                # Skip if already in database
                if supa_check_phone(phone):
                    continue

                # Parse owner name from business title
                # Many small businesses are named after the owner
                name_parts = title.replace('LLC', '').replace('Inc', '').replace('.', '').strip().split()
                first = name_parts[0] if name_parts else 'Business'
                last = name_parts[1] if len(name_parts) > 1 else 'Owner'

                scores = whale_score('self_employed', {
                    'phone': phone, 'state': state,
                    'income': 'medium', 'age': 38,
                })

                lead = {
                    'first_name': first, 'last_name': last, 'phone': phone,
                    'email': item.get('email', ''),
                    'source': 'scrape', 'source_detail': f'google_maps_{state.lower()}',
                    'reason': f'Self-employed in {biz_city} — {item.get("categoryName","business owner")}. Likely needs coverage.',
                    'notes': f'Business: {title}. Category: {item.get("categoryName","")}. Rating: {item.get("totalScore","")}. Reviews: {item.get("reviewsCount","")}. Website: {item.get("website","none")}',
                    'status': 'new', 'assigned_to': 'dayday',
                    **scores,
                    'metadata': json.dumps({
                        'business_name': title, 'city': biz_city, 'state': state,
                        'category': item.get('categoryName', ''),
                        'website': item.get('website', ''),
                        'rating': item.get('totalScore'),
                        'reviews': item.get('reviewsCount'),
                        'address': item.get('address', ''),
                        'scrape_source': 'google_maps', 'scrape_date': datetime.now().isoformat(),
                    })
                }

                if lead['tier'] != 'C':  # Only A and B tier
                    leads.append(lead)

            time.sleep(2)  # Rate limit between searches

    return leads

# ═══════════════════════════════════════════
# SOURCE 2: Indeed — "No Benefits" Job Postings
# ═══════════════════════════════════════════
def scrape_indeed_no_benefits(state='FL'):
    """Find people taking jobs without health benefits — they need individual coverage."""
    leads = []

    # Search Indeed for jobs explicitly stating no benefits
    queries = [
        f'1099 contractor {state}',
        f'no benefits part time {state}',
        f'independent contractor {state}',
    ]

    for query in queries:
        print(f'  Indeed: "{query}"')
        results = run_apify_actor('misceres~indeed-scraper', {
            'query': query,
            'location': state,
            'maxResults': 10,
        }, wait_secs=60)

        # Indeed results give us COMPANIES hiring without benefits
        # We can't target the job seekers directly, but we can target the AREA
        # This is more of a geographic intelligence source
        for item in results:
            company = item.get('company', '')
            location = item.get('location', '')
            print(f'    {company} in {location} (no-benefits posting)')

    return leads  # Indeed is more for intelligence than direct leads

# ═══════════════════════════════════════════
# MAIN PIPELINE
# ═══════════════════════════════════════════
def run_elite_scrape(mode='morning'):
    print(f'\n{"="*60}')
    print(f'AEGIS ELITE SCRAPER — {mode.upper()} RUN')
    print(f'{datetime.now().strftime("%Y-%m-%d %H:%M")}')
    print(f'Target: DayDay\'s whales — families, 26-58, self-employed')
    print(f'{"="*60}\n')

    total = 0
    states = ACTIVE_STATES[:3] if mode == 'morning' else ACTIVE_STATES[3:6]

    for state in states:
        print(f'\n=== {state} ===')

        # Google Maps — self-employed businesses
        gm_leads = scrape_google_maps(state, max_per_city=10)
        for lead in gm_leads:
            if supa_insert(lead):
                total += 1
                print(f'  + {lead["first_name"]} {lead["last_name"]} | {lead["phone"]} | {lead["tier"]}-tier')

        print(f'  Google Maps: {len(gm_leads)} leads')

    print(f'\n{"="*60}')
    print(f'TOTAL INSERTED: {total} leads')
    print(f'{"="*60}\n')
    return total


if __name__ == '__main__':
    import sys
    mode = sys.argv[1] if len(sys.argv) > 1 else 'morning'
    run_elite_scrape(mode)
