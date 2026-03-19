# Lead Ingestion Flow

## Trigger
Cron job (every 24 hours per source, configurable)

## Flow

```
START
  │
  ├─ For each active county_source:
  │   │
  │   ├─ 1. CHECK SOURCE
  │   │   ├─ Navigate to source_url (Playwright)
  │   │   ├─ Check for new content (compare hash with last download)
  │   │   ├─ If no new content → skip, update last_checked_at
  │   │   └─ If new content → proceed
  │   │
  │   ├─ 2. DOWNLOAD
  │   │   ├─ Download file (PDF/HTML/CSV)
  │   │   ├─ Save to storage, compute file_hash
  │   │   ├─ Create raw_downloads entry (status: success)
  │   │   ├─ On failure → retry 3x with backoff
  │   │   └─ After 3 failures → log error, increment consecutive_failures, alert
  │   │
  │   ├─ 3. PARSE
  │   │   ├─ Route to correct parser (parser_id from source config)
  │   │   ├─ Extract records: case_number, property_address, owner_name, surplus_amount, sale_date
  │   │   ├─ For each record → create raw_records entry
  │   │   ├─ If parse fails for a record → mark parse_status: 'needs_review'
  │   │   └─ If entire file fails → try Claude API vision as fallback
  │   │
  │   ├─ 4. NORMALIZE
  │   │   ├─ Deduplicate: check case_number + county doesn't already exist in opportunities
  │   │   ├─ Validate: surplus_amount > 0, case_number present
  │   │   ├─ Normalize: clean names, standardize addresses, parse amounts
  │   │   ├─ Create opportunities entry (status: 'new')
  │   │   └─ Log in audit_log
  │   │
  │   └─ 5. SCORE
  │       ├─ Apply scoring model (see opportunity-scoring-model.md)
  │       ├─ Update opportunities.score
  │       ├─ If score >= 20 → status: 'qualified'
  │       └─ If score < 20 → status: 'disqualified'
  │
  └─ Update source.last_checked_at, last_success_at, reset consecutive_failures
END
```

## Error Handling

| Error | Action |
|-------|--------|
| Source URL unreachable | Retry 3x, then alert |
| Download fails | Retry 3x, then skip |
| PDF corrupt/unreadable | Try Claude API, then flag for manual |
| Parse extracts 0 records | Alert — possible format change |
| Duplicate case_number | Skip (already in opportunities) |

## Outputs
- raw_downloads table: new download entry
- raw_records table: parsed records
- opportunities table: normalized, scored leads
- audit_log: all events logged
