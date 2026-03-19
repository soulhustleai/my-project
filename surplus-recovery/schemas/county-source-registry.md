# County Source Registry

## Purpose

Define how each monitored county source is configured. Each source gets a config entry that tells the source-monitor how to fetch data, and the record-ingestion service how to parse it.

---

## Schema

```python
class CountySource:
    id: str                        # UUID
    county: str                    # "Broward"
    state: str                     # "FL"
    source_type: str               # "foreclosure_surplus" | "tax_deed_overage"
    source_url: str                # Full URL to surplus list page
    data_format: str               # "pdf" | "html_table" | "csv" | "portal_search"
    parser_id: str                 # "broward_fl_foreclosure_pdf"
    check_frequency_hours: int     # 24
    download_method: str           # "direct_link" | "navigate_and_download" | "search_portal"
    auth_required: bool            # False
    notes: str                     # Free text

    # Scraper config
    scraper_config: dict           # Source-specific config
    # Example:
    # {
    #   "navigate_steps": ["click #surplus-link", "select year=2026"],
    #   "download_selector": "a.pdf-download",
    #   "wait_for": "#results-table",
    #   "proxy_required": false
    # }

    # Parser config
    parser_config: dict            # Parser-specific config
    # Example:
    # {
    #   "table_area": [50, 50, 750, 550],  # PDF crop area
    #   "columns": ["case_number", "property_address", "owner_name", "surplus_amount", "sale_date"],
    #   "header_row": 0,
    #   "skip_rows": 1,
    #   "amount_column": "surplus_amount",
    #   "date_format": "%m/%d/%Y"
    # }
```

---

## Initial Registry (Florida MVP)

### Broward County — Foreclosure Surplus
```yaml
county: Broward
state: FL
source_type: foreclosure_surplus
source_url: "https://www.browardclerk.org/Web2/Default.aspx"  # NEEDS VALIDATION
data_format: pdf
parser_id: broward_fl_foreclosure_pdf
check_frequency_hours: 24
download_method: navigate_and_download
auth_required: false
scraper_config:
  navigation: "Navigate to surplus funds page, find latest PDF link"
  proxy_required: false
parser_config:
  expected_columns: [case_number, property_address, defendant_name, surplus_amount, sale_date]
  amount_format: "$X,XXX.XX"
  date_format: "%m/%d/%Y"
status: NEEDS_VALIDATION
```

### Palm Beach County — Foreclosure Surplus
```yaml
county: Palm Beach
state: FL
source_type: foreclosure_surplus
source_url: "https://www.mypalmbeachclerk.com"  # NEEDS VALIDATION
data_format: pdf
parser_id: palm_beach_fl_foreclosure_pdf
check_frequency_hours: 24
download_method: navigate_and_download
auth_required: false
scraper_config:
  navigation: "Navigate to surplus funds / registry of court page"
  proxy_required: false
parser_config:
  expected_columns: [case_number, property_address, defendant_name, surplus_amount]
  amount_format: "$X,XXX.XX"
status: NEEDS_VALIDATION
```

### Hillsborough County — Foreclosure Surplus
```yaml
county: Hillsborough
state: FL
source_type: foreclosure_surplus
source_url: "https://www.hillsclerk.com"  # NEEDS VALIDATION
data_format: pdf
parser_id: hillsborough_fl_foreclosure_pdf
check_frequency_hours: 24
download_method: navigate_and_download
auth_required: false
scraper_config:
  navigation: "Navigate to surplus funds page"
  proxy_required: false
parser_config:
  expected_columns: [case_number, defendant_name, surplus_amount, sale_date]
status: NEEDS_VALIDATION
```

---

## Adding a New Source

1. Research the county's surplus list publication method
2. Create a source entry with all fields
3. Write a source-specific scraper in `services/source-monitor/sources/`
4. Write or adapt a parser in `services/record-ingestion/parsers/`
5. Insert config into `county_sources` table
6. Test end-to-end: scrape → parse → normalize → score
7. Add to monitoring schedule

---

## Source Health Monitoring

Each source is monitored for:
- **Last successful check** — alert if >48 hours for daily sources
- **Consecutive failures** — alert after 3 consecutive failures
- **Parse success rate** — alert if <80% on a batch
- **Records found** — alert if 0 records found when >0 expected

Alerts route through notifications service to founder.
