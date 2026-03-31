"""
AEGIS Lead Scraper — Florida New LLC Filings
Scrapes Florida Division of Corporations (sunbiz.org) for new business filings.
People who just filed an LLC likely lost employer coverage and need health insurance.

Schedule: Runs 2x daily via n8n (6AM ET + 6PM ET)
Output: Inserts scored leads into aegis_leads table in Supabase
"""
import json
import re
import os
from datetime import datetime, timedelta
from urllib.request import Request, urlopen
from urllib.parse import urlencode, quote

# ─── Config ───
SUPABASE_URL = os.getenv('SUPABASE_URL', 'https://pjkurxtvvtxbpfearqhd.supabase.co')
SUPABASE_KEY = os.getenv('SUPABASE_SERVICE_KEY', '')
APIFY_TOKEN = os.getenv('APIFY_TOKEN', '')

# ─── Supabase helpers ───
def supabase_insert(table, data):
    """Insert a row into Supabase."""
    payload = json.dumps(data).encode()
    req = Request(
        f'{SUPABASE_URL}/rest/v1/{table}',
        data=payload,
        headers={
            'apikey': SUPABASE_KEY,
            'Authorization': f'Bearer {SUPABASE_KEY}',
            'Content-Type': 'application/json',
            'Prefer': 'return=minimal'
        }
    )
    try:
        resp = urlopen(req)
        return resp.status in (200, 201)
    except Exception as e:
        print(f'Insert error: {e}')
        return False

def supabase_check_exists(phone):
    """Check if a lead with this phone already exists."""
    req = Request(
        f'{SUPABASE_URL}/rest/v1/aegis_leads?phone=eq.{quote(phone)}&select=id&limit=1',
        headers={
            'apikey': SUPABASE_KEY,
            'Authorization': f'Bearer {SUPABASE_KEY}',
        }
    )
    try:
        resp = urlopen(req)
        data = json.loads(resp.read().decode())
        return len(data) > 0
    except:
        return False

# ─── Scoring ───
def score_llc_lead(filing_data):
    """Score a new LLC filing as a health insurance lead."""
    # New LLC owners are HIGH intent — they just left employer coverage
    urgency = 85  # High base — just started business
    contactability = 60  # We have name + address from filing, may need enrichment for phone/email
    insurability = 80  # Likely healthy (starting a business requires energy/health)
    monetization = 75  # Self-employed, likely above poverty line

    # Boost for sole member LLCs (individual, not corporate entity)
    if filing_data.get('entity_type', '').lower() in ('llc', 'sole proprietorship', 'single member llc'):
        urgency += 5
        monetization += 5

    # Boost for Florida (DayDay's primary state, knows the market)
    if filing_data.get('state', '').upper() == 'FL':
        contactability += 5

    # Calculate total
    total = round(urgency * 0.35 + contactability * 0.20 + insurability * 0.25 + monetization * 0.20)
    tier = 'A' if total >= 75 else 'B' if total >= 50 else 'C'

    return {
        'score': min(total, 100),
        'tier': tier,
        'urgency_score': min(urgency, 100),
        'contactability_score': min(contactability, 100),
        'insurability_score': min(insurability, 100),
        'monetization_score': min(monetization, 100),
    }

# ─── Florida SOS Scraper ───
def scrape_florida_new_filings(days_back=1):
    """
    Scrape new LLC filings from Florida Division of Corporations.

    Florida sunbiz.org has a search API that returns recent filings.
    We search for entities filed in the last N days.
    """
    leads = []

    # sunbiz.org search endpoint
    # We use the document number search with date filter
    target_date = (datetime.now() - timedelta(days=days_back)).strftime('%m/%d/%Y')
    today = datetime.now().strftime('%m/%d/%Y')

    print(f'Scraping Florida SOS filings from {target_date} to {today}...')

    # Method 1: Use the sunbiz API endpoint for recent filings
    # The detail search allows filtering by filing date
    search_url = f'https://search.sunbiz.org/Inquiry/CorporationSearch/SearchByName'

    # Alternative: Use the Apify actor for sunbiz if available
    if APIFY_TOKEN:
        leads = scrape_via_apify('florida', target_date, today)
    else:
        # Direct scraping approach
        leads = scrape_sunbiz_direct(target_date, today)

    return leads

def scrape_sunbiz_direct(from_date, to_date):
    """Direct scrape of sunbiz.org for new filings."""
    leads = []

    # sunbiz has a filing search that can be queried
    # We'll use the detail search endpoint
    # Note: This is a simplified version — production would use Playwright for JS-rendered pages

    try:
        # Search for recent LLC filings
        # sunbiz provides an XML/JSON endpoint for bulk filings
        url = 'https://search.sunbiz.org/Inquiry/CorporationSearch/GetSearchResults'

        # We search for common LLC naming patterns filed recently
        # In production, use Playwright to handle the JS-heavy interface
        print('  Note: sunbiz requires browser automation for full scraping.')
        print('  Using Apify or Playwright recommended for production.')
        print('  For now, generating sample data structure...')

    except Exception as e:
        print(f'  Scrape error: {e}')

    return leads

def scrape_via_apify(state, from_date, to_date):
    """Use Apify actor to scrape state SOS filings."""
    # Apify has pre-built actors for business registry scraping
    # Actor: apify/web-scraper or custom actor for sunbiz

    print(f'  Using Apify to scrape {state} SOS filings...')

    # In production, this calls the Apify API to run an actor
    # For now, return empty — will be filled when Apify token is provided
    return []

# ─── WARN Act Scraper ───
def scrape_warn_notices(state='FL'):
    """Scrape WARN Act layoff notices from Florida DOL."""
    leads = []

    # Florida WARN notices URL
    warn_url = 'https://floridajobs.org/office-directory/division-of-workforce-services/workforce-programs/reemployment-and-emergency-assistance-coordination-team-react/warn-notices'

    print(f'Scraping WARN Act notices for {state}...')

    try:
        req = Request(warn_url, headers={'User-Agent': 'Mozilla/5.0'})
        resp = urlopen(req, timeout=30)
        html = resp.read().decode('utf-8', errors='ignore')

        # Parse WARN notices — these are typically in HTML tables or PDFs
        # Extract: company name, location, number affected, layoff date
        # Each notice represents potentially hundreds of people losing coverage

        # Look for table rows with company data
        # In production, use BeautifulSoup for robust parsing
        company_matches = re.findall(r'<td[^>]*>([^<]+)</td>', html)

        print(f'  Found {len(company_matches)} data cells in WARN page')

        # WARN notices don't give individual names — they give:
        # Company, location, employee count, layoff date
        # Strategy: Use this for geographic targeting
        # "500 people in Orlando just lost coverage" → target that ZIP with ads/outreach

    except Exception as e:
        print(f'  WARN scrape error: {e}')

    return leads

# ─── Lead Processing ───
def process_filing_to_lead(filing):
    """Convert a business filing into an AEGIS lead."""
    # Extract registrant info
    name = filing.get('registrant_name', filing.get('name', ''))
    if not name:
        return None

    # Split name
    parts = name.strip().split()
    first_name = parts[0] if parts else ''
    last_name = ' '.join(parts[1:]) if len(parts) > 1 else ''

    # Get address
    address = filing.get('address', '')
    state = filing.get('state', 'FL')

    # Score the lead
    scores = score_llc_lead(filing)

    lead = {
        'first_name': first_name,
        'last_name': last_name,
        'phone': filing.get('phone', ''),
        'email': filing.get('email', ''),
        'source': 'scrape',
        'source_detail': f'sos_llc_filing_{state.lower()}',
        'reason': f'New {filing.get("entity_type", "LLC")} filing — likely lost employer coverage',
        'notes': f'Business: {filing.get("business_name", "?")}. Filed: {filing.get("filing_date", "?")}. Address: {address}',
        'status': 'new',
        'assigned_to': 'dayday',
        'score': scores['score'],
        'tier': scores['tier'],
        'urgency_score': scores['urgency_score'],
        'contactability_score': scores['contactability_score'],
        'insurability_score': scores['insurability_score'],
        'monetization_score': scores['monetization_score'],
        'metadata': json.dumps({
            'business_name': filing.get('business_name', ''),
            'entity_type': filing.get('entity_type', ''),
            'filing_date': filing.get('filing_date', ''),
            'filing_number': filing.get('filing_number', ''),
            'state': state,
            'address': address,
            'scrape_source': 'state_sos',
            'scrape_date': datetime.now().isoformat(),
        })
    }

    return lead

# ─── Enrichment ───
def enrich_lead(lead):
    """Enrich a lead with phone/email using Apollo or Hunter.io."""
    # In production, call Apollo.io or Hunter.io API
    # For now, return lead as-is

    name = f"{lead['first_name']} {lead['last_name']}"

    # Apollo.io enrichment (when API key is available)
    # endpoint: https://api.apollo.io/v1/people/match
    # payload: { "first_name": ..., "last_name": ..., "organization_name": ..., "domain": ... }
    # Returns: email, phone, LinkedIn, title, etc.

    return lead

# ─── Main Pipeline ───
def run_morning_scrape():
    """Morning scrape: SOS filings + WARN notices."""
    print(f'\n{"="*50}')
    print(f'AEGIS MORNING SCRAPE — {datetime.now().strftime("%Y-%m-%d %H:%M")}')
    print(f'{"="*50}\n')

    all_leads = []

    # 1. Florida SOS new LLC filings
    fl_filings = scrape_florida_new_filings(days_back=1)
    print(f'Florida SOS: {len(fl_filings)} raw filings')

    # 2. WARN Act notices
    warn_data = scrape_warn_notices('FL')
    print(f'Florida WARN: {len(warn_data)} notices')

    # 3. Process filings into leads
    for filing in fl_filings:
        lead = process_filing_to_lead(filing)
        if lead:
            # Check for duplicates
            if lead.get('phone') and supabase_check_exists(lead['phone']):
                continue

            # Enrich
            lead = enrich_lead(lead)

            # Insert to Supabase
            if supabase_insert('aegis_leads', lead):
                all_leads.append(lead)
                print(f'  + {lead["first_name"]} {lead["last_name"]} | Score: {lead["score"]} | {lead["tier"]}-tier')

    print(f'\nTotal leads inserted: {len(all_leads)}')
    return all_leads

def run_evening_scrape():
    """Evening scrape: Job boards + freelancer platforms."""
    print(f'\n{"="*50}')
    print(f'AEGIS EVENING SCRAPE — {datetime.now().strftime("%Y-%m-%d %H:%M")}')
    print(f'{"="*50}\n')

    # 1. Job boards with "no benefits" filter
    # 2. Freelancer platforms (new profiles)
    # 3. Google Trends spike detection

    print('Evening scrape: Job boards + freelancer platforms')
    print('  (Requires Apify token for production scraping)')

    return []

# ─── Entry Point ───
if __name__ == '__main__':
    import sys

    mode = sys.argv[1] if len(sys.argv) > 1 else 'morning'

    if mode == 'morning':
        run_morning_scrape()
    elif mode == 'evening':
        run_evening_scrape()
    elif mode == 'test':
        # Insert a test scraped lead to verify the pipeline
        test_lead = {
            'first_name': 'Maria',
            'last_name': 'Rodriguez',
            'phone': '(305) 555-0199',
            'email': '',
            'source': 'scrape',
            'source_detail': 'sos_llc_filing_fl',
            'reason': 'New LLC filing — likely lost employer coverage',
            'notes': 'Business: Rodriguez Consulting LLC. Filed: 2026-03-31. Address: 1234 Brickell Ave, Miami FL 33131',
            'status': 'new',
            'assigned_to': 'dayday',
            'score': 82,
            'tier': 'A',
            'urgency_score': 85,
            'contactability_score': 65,
            'insurability_score': 80,
            'monetization_score': 80,
            'metadata': json.dumps({
                'business_name': 'Rodriguez Consulting LLC',
                'entity_type': 'LLC',
                'filing_date': '2026-03-31',
                'filing_number': 'L26000123456',
                'state': 'FL',
                'address': '1234 Brickell Ave, Miami FL 33131',
                'scrape_source': 'state_sos',
                'scrape_date': datetime.now().isoformat(),
            })
        }

        if SUPABASE_KEY:
            success = supabase_insert('aegis_leads', test_lead)
            print(f'Test lead inserted: {success}')
        else:
            print('Set SUPABASE_SERVICE_KEY env var to test insertion')
            print(f'Lead data: {json.dumps(test_lead, indent=2)}')
    else:
        print(f'Usage: python scraper.py [morning|evening|test]')
