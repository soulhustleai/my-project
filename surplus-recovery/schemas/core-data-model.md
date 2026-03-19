# Core Data Model

## Overview

All tables live in Supabase (Postgres). This schema is implemented via `scripts/setup_supabase.sql`.

---

## Tables

### 1. county_sources

Registry of all monitored data sources.

```sql
CREATE TABLE county_sources (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  county TEXT NOT NULL,
  state TEXT NOT NULL,
  source_type TEXT NOT NULL,           -- 'foreclosure_surplus' | 'tax_deed_overage'
  source_url TEXT NOT NULL,
  data_format TEXT NOT NULL,           -- 'pdf' | 'html' | 'csv' | 'portal'
  parser_id TEXT NOT NULL,             -- maps to parser module
  check_frequency_hours INT DEFAULT 24,
  last_checked_at TIMESTAMPTZ,
  last_success_at TIMESTAMPTZ,
  consecutive_failures INT DEFAULT 0,
  is_active BOOLEAN DEFAULT true,
  notes TEXT,
  created_at TIMESTAMPTZ DEFAULT now(),
  updated_at TIMESTAMPTZ DEFAULT now()
);
```

### 2. raw_downloads

Files/pages downloaded from sources.

```sql
CREATE TABLE raw_downloads (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  source_id UUID REFERENCES county_sources(id),
  file_path TEXT,                       -- local or storage path
  file_hash TEXT,                       -- SHA256 for dedup
  file_size_bytes INT,
  download_status TEXT DEFAULT 'pending', -- 'pending' | 'success' | 'failed' | 'processed'
  error_message TEXT,
  downloaded_at TIMESTAMPTZ DEFAULT now(),
  processed_at TIMESTAMPTZ
);
```

### 3. raw_records

Parsed but unnormalized records from downloads.

```sql
CREATE TABLE raw_records (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  download_id UUID REFERENCES raw_downloads(id),
  source_id UUID REFERENCES county_sources(id),
  raw_data JSONB NOT NULL,             -- all parsed fields as-is
  case_number TEXT,
  property_address TEXT,
  owner_name TEXT,
  surplus_amount DECIMAL(12,2),
  sale_date DATE,
  sale_type TEXT,                       -- 'foreclosure' | 'tax_deed' | 'other'
  parse_status TEXT DEFAULT 'parsed',  -- 'parsed' | 'failed' | 'needs_review'
  parse_confidence DECIMAL(3,2),       -- 0.00-1.00
  created_at TIMESTAMPTZ DEFAULT now()
);
```

### 4. opportunities

Normalized, deduplicated, scored surplus opportunities.

```sql
CREATE TABLE opportunities (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  raw_record_id UUID REFERENCES raw_records(id),
  source_id UUID REFERENCES county_sources(id),
  county TEXT NOT NULL,
  state TEXT NOT NULL,
  case_number TEXT NOT NULL,
  property_address TEXT,
  owner_name TEXT,
  surplus_amount DECIMAL(12,2) NOT NULL,
  sale_date DATE,
  sale_type TEXT NOT NULL,
  score DECIMAL(5,2),                  -- composite score 0-100
  status TEXT DEFAULT 'new',           -- see lead-lifecycle.md
  claimant_id UUID REFERENCES claimants(id),
  disqualification_reason TEXT,
  created_at TIMESTAMPTZ DEFAULT now(),
  updated_at TIMESTAMPTZ DEFAULT now(),
  UNIQUE(county, state, case_number)
);

CREATE INDEX idx_opportunities_status ON opportunities(status);
CREATE INDEX idx_opportunities_score ON opportunities(score DESC);
CREATE INDEX idx_opportunities_county ON opportunities(county, state);
```

### 5. claimants

Enriched claimant contact records.

```sql
CREATE TABLE claimants (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  full_name TEXT NOT NULL,
  first_name TEXT,
  last_name TEXT,
  current_address_line1 TEXT,
  current_address_line2 TEXT,
  current_city TEXT,
  current_state TEXT,
  current_zip TEXT,
  phone_primary TEXT,
  phone_secondary TEXT,
  email TEXT,
  date_of_birth DATE,
  enrichment_source TEXT,              -- 'pdl' | 'truepeoplesearch' | 'manual'
  enrichment_confidence DECIMAL(3,2),  -- 0.00-1.00
  address_verified BOOLEAN DEFAULT false,
  phone_verified BOOLEAN DEFAULT false,
  do_not_contact BOOLEAN DEFAULT false,
  notes TEXT,
  created_at TIMESTAMPTZ DEFAULT now(),
  updated_at TIMESTAMPTZ DEFAULT now()
);
```

### 6. outreach_events

Every outreach attempt and response.

```sql
CREATE TABLE outreach_events (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  opportunity_id UUID REFERENCES opportunities(id),
  claimant_id UUID REFERENCES claimants(id),
  channel TEXT NOT NULL,               -- 'mail' | 'sms' | 'email' | 'phone'
  direction TEXT NOT NULL,             -- 'outbound' | 'inbound'
  event_type TEXT NOT NULL,            -- 'sent' | 'delivered' | 'opened' | 'replied' | 'bounced' | 'failed' | 'opted_out'
  template_id TEXT,                    -- reference to template used
  content_preview TEXT,                -- first 200 chars
  external_id TEXT,                    -- Lob ID, Twilio SID, etc.
  metadata JSONB,                      -- channel-specific data
  sequence_step INT,                   -- which step in the outreach sequence
  created_at TIMESTAMPTZ DEFAULT now()
);

CREATE INDEX idx_outreach_opportunity ON outreach_events(opportunity_id);
CREATE INDEX idx_outreach_channel ON outreach_events(channel);
```

### 7. cases

Signed clients with full case lifecycle.

```sql
CREATE TABLE cases (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  opportunity_id UUID REFERENCES opportunities(id),
  claimant_id UUID REFERENCES claimants(id),
  county TEXT NOT NULL,
  state TEXT NOT NULL,
  case_number TEXT NOT NULL,
  property_address TEXT,
  surplus_amount DECIMAL(12,2),
  fee_percentage DECIMAL(4,2),         -- e.g., 30.00
  fee_amount DECIMAL(12,2),            -- calculated: surplus × fee%
  status TEXT DEFAULT 'signed',        -- see lead-lifecycle.md
  agreement_signed_at TIMESTAMPTZ,
  agreement_url TEXT,                  -- link to signed agreement
  docs_complete BOOLEAN DEFAULT false,
  claim_filed_at TIMESTAMPTZ,
  claim_tracking_number TEXT,
  claim_approved_at TIMESTAMPTZ,
  disbursement_amount DECIMAL(12,2),
  disbursement_received_at TIMESTAMPTZ,
  client_paid_at TIMESTAMPTZ,
  client_paid_amount DECIMAL(12,2),
  closed_at TIMESTAMPTZ,
  notes TEXT,
  created_at TIMESTAMPTZ DEFAULT now(),
  updated_at TIMESTAMPTZ DEFAULT now()
);

CREATE INDEX idx_cases_status ON cases(status);
```

### 8. documents

Generated and collected documents.

```sql
CREATE TABLE documents (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  case_id UUID REFERENCES cases(id),
  doc_type TEXT NOT NULL,              -- 'agreement' | 'affidavit' | 'id_copy' | 'claim_form' | 'cover_letter' | 'poa' | 'w9' | 'claim_packet'
  file_path TEXT,                      -- Supabase storage path
  file_name TEXT,
  status TEXT DEFAULT 'pending',       -- 'pending' | 'collected' | 'generated' | 'signed' | 'notarized'
  uploaded_by TEXT,                     -- 'claimant' | 'system' | 'founder'
  created_at TIMESTAMPTZ DEFAULT now(),
  updated_at TIMESTAMPTZ DEFAULT now()
);
```

### 9. notifications

System alerts and founder escalations.

```sql
CREATE TABLE notifications (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  type TEXT NOT NULL,                  -- 'founder_action' | 'alert' | 'info' | 'error'
  priority TEXT NOT NULL,              -- 'p1_urgent' | 'p2_action' | 'p3_review' | 'p4_info'
  title TEXT NOT NULL,
  body TEXT NOT NULL,
  related_entity_type TEXT,            -- 'opportunity' | 'case' | 'claimant'
  related_entity_id UUID,
  is_read BOOLEAN DEFAULT false,
  is_actioned BOOLEAN DEFAULT false,
  sent_via TEXT[],                     -- ['sms', 'email', 'dashboard']
  created_at TIMESTAMPTZ DEFAULT now(),
  actioned_at TIMESTAMPTZ
);

CREATE INDEX idx_notifications_unread ON notifications(is_read) WHERE is_read = false;
```

### 10. audit_log

Immutable log of all state changes.

```sql
CREATE TABLE audit_log (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  entity_type TEXT NOT NULL,           -- table name
  entity_id UUID NOT NULL,
  action TEXT NOT NULL,                -- 'create' | 'update' | 'delete' | 'status_change'
  old_value JSONB,
  new_value JSONB,
  actor TEXT NOT NULL,                 -- 'system' | 'founder' | 'claimant' | service name
  created_at TIMESTAMPTZ DEFAULT now()
);

CREATE INDEX idx_audit_entity ON audit_log(entity_type, entity_id);
CREATE INDEX idx_audit_created ON audit_log(created_at);
```

---

## Entity Relationships

```
county_sources  1──M  raw_downloads  1──M  raw_records
                                              │
                                              1
                                              │
                                              M
opportunities  M──1  claimants
     │
     1
     │
     M
outreach_events
     │
     1
     │
cases  1──M  documents
     │
notifications (linked via related_entity_id)
audit_log (linked via entity_type + entity_id)
```

---

## Row-Level Security (RLS)

For MVP, use Supabase service role key (server-side only). No public access.

When dashboard is built, add RLS policies:
- Dashboard reads: authenticated users only
- Writes: service role only
- No public access to any table

---

## Dependency Map

```
schemas/core-data-model.md
  ↓ feeds
scripts/setup_supabase.sql          (implementation)
packages/shared-types/types.py      (Python type definitions)
All services                        (read/write these tables)
apps/dashboard/                     (reads these tables)
```
