-- Surplus Funds Recovery — Supabase Schema Setup
-- Run this in Supabase SQL Editor to create all tables

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ============================================
-- 1. county_sources
-- ============================================
CREATE TABLE IF NOT EXISTS county_sources (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  county TEXT NOT NULL,
  state TEXT NOT NULL,
  source_type TEXT NOT NULL CHECK (source_type IN ('foreclosure_surplus', 'tax_deed_overage', 'other')),
  source_url TEXT NOT NULL,
  data_format TEXT NOT NULL CHECK (data_format IN ('pdf', 'html_table', 'csv', 'portal_search')),
  parser_id TEXT NOT NULL,
  check_frequency_hours INT DEFAULT 24,
  last_checked_at TIMESTAMPTZ,
  last_success_at TIMESTAMPTZ,
  consecutive_failures INT DEFAULT 0,
  is_active BOOLEAN DEFAULT true,
  scraper_config JSONB DEFAULT '{}',
  parser_config JSONB DEFAULT '{}',
  notes TEXT,
  created_at TIMESTAMPTZ DEFAULT now(),
  updated_at TIMESTAMPTZ DEFAULT now()
);

-- ============================================
-- 2. raw_downloads
-- ============================================
CREATE TABLE IF NOT EXISTS raw_downloads (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  source_id UUID REFERENCES county_sources(id) ON DELETE CASCADE,
  file_path TEXT,
  file_hash TEXT,
  file_size_bytes INT,
  download_status TEXT DEFAULT 'pending' CHECK (download_status IN ('pending', 'success', 'failed', 'processed')),
  error_message TEXT,
  downloaded_at TIMESTAMPTZ DEFAULT now(),
  processed_at TIMESTAMPTZ
);

CREATE INDEX IF NOT EXISTS idx_raw_downloads_source ON raw_downloads(source_id);
CREATE INDEX IF NOT EXISTS idx_raw_downloads_status ON raw_downloads(download_status);

-- ============================================
-- 3. raw_records
-- ============================================
CREATE TABLE IF NOT EXISTS raw_records (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  download_id UUID REFERENCES raw_downloads(id) ON DELETE CASCADE,
  source_id UUID REFERENCES county_sources(id),
  raw_data JSONB NOT NULL,
  case_number TEXT,
  property_address TEXT,
  owner_name TEXT,
  surplus_amount DECIMAL(12,2),
  sale_date DATE,
  sale_type TEXT,
  parse_status TEXT DEFAULT 'parsed' CHECK (parse_status IN ('parsed', 'failed', 'needs_review')),
  parse_confidence DECIMAL(3,2),
  created_at TIMESTAMPTZ DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_raw_records_download ON raw_records(download_id);
CREATE INDEX IF NOT EXISTS idx_raw_records_case ON raw_records(case_number);

-- ============================================
-- 4. claimants
-- ============================================
CREATE TABLE IF NOT EXISTS claimants (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  full_name TEXT NOT NULL,
  first_name TEXT,
  last_name TEXT,
  middle_name TEXT,
  suffix TEXT,
  current_address_line1 TEXT,
  current_address_line2 TEXT,
  current_city TEXT,
  current_state TEXT,
  current_zip TEXT,
  phone_primary TEXT,
  phone_secondary TEXT,
  email TEXT,
  date_of_birth DATE,
  former_address TEXT,
  enrichment_source TEXT,
  enrichment_confidence DECIMAL(3,2),
  address_verified BOOLEAN DEFAULT false,
  phone_verified BOOLEAN DEFAULT false,
  email_verified BOOLEAN DEFAULT false,
  do_not_contact BOOLEAN DEFAULT false,
  preferred_channel TEXT,
  relationship TEXT,
  notes TEXT,
  created_at TIMESTAMPTZ DEFAULT now(),
  updated_at TIMESTAMPTZ DEFAULT now(),
  enriched_at TIMESTAMPTZ,
  last_contacted_at TIMESTAMPTZ
);

CREATE INDEX IF NOT EXISTS idx_claimants_name ON claimants(full_name);
CREATE INDEX IF NOT EXISTS idx_claimants_dnc ON claimants(do_not_contact) WHERE do_not_contact = true;

-- ============================================
-- 5. opportunities
-- ============================================
CREATE TABLE IF NOT EXISTS opportunities (
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
  sale_type TEXT NOT NULL DEFAULT 'foreclosure',
  score DECIMAL(5,2),
  status TEXT DEFAULT 'new',
  claimant_id UUID REFERENCES claimants(id),
  disqualification_reason TEXT,
  created_at TIMESTAMPTZ DEFAULT now(),
  updated_at TIMESTAMPTZ DEFAULT now(),
  UNIQUE(county, state, case_number)
);

CREATE INDEX IF NOT EXISTS idx_opportunities_status ON opportunities(status);
CREATE INDEX IF NOT EXISTS idx_opportunities_score ON opportunities(score DESC);
CREATE INDEX IF NOT EXISTS idx_opportunities_county ON opportunities(county, state);

-- ============================================
-- 6. outreach_events
-- ============================================
CREATE TABLE IF NOT EXISTS outreach_events (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  opportunity_id UUID REFERENCES opportunities(id),
  claimant_id UUID REFERENCES claimants(id),
  channel TEXT NOT NULL CHECK (channel IN ('mail', 'sms', 'email', 'phone')),
  direction TEXT NOT NULL CHECK (direction IN ('outbound', 'inbound')),
  event_type TEXT NOT NULL,
  template_id TEXT,
  content_preview TEXT,
  external_id TEXT,
  metadata JSONB DEFAULT '{}',
  sequence_step INT,
  created_at TIMESTAMPTZ DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_outreach_opportunity ON outreach_events(opportunity_id);
CREATE INDEX IF NOT EXISTS idx_outreach_channel ON outreach_events(channel);
CREATE INDEX IF NOT EXISTS idx_outreach_created ON outreach_events(created_at);

-- ============================================
-- 7. cases
-- ============================================
CREATE TABLE IF NOT EXISTS cases (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  opportunity_id UUID REFERENCES opportunities(id),
  claimant_id UUID REFERENCES claimants(id),
  county TEXT NOT NULL,
  state TEXT NOT NULL,
  case_number TEXT NOT NULL,
  property_address TEXT,
  surplus_amount DECIMAL(12,2),
  fee_percentage DECIMAL(4,2) DEFAULT 30.00,
  fee_amount DECIMAL(12,2),
  status TEXT DEFAULT 'signed',
  agreement_signed_at TIMESTAMPTZ,
  agreement_url TEXT,
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

CREATE INDEX IF NOT EXISTS idx_cases_status ON cases(status);

-- ============================================
-- 8. documents
-- ============================================
CREATE TABLE IF NOT EXISTS documents (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  case_id UUID REFERENCES cases(id) ON DELETE CASCADE,
  doc_type TEXT NOT NULL,
  file_path TEXT,
  file_name TEXT,
  status TEXT DEFAULT 'pending' CHECK (status IN ('pending', 'collected', 'generated', 'signed', 'notarized')),
  uploaded_by TEXT,
  created_at TIMESTAMPTZ DEFAULT now(),
  updated_at TIMESTAMPTZ DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_documents_case ON documents(case_id);

-- ============================================
-- 9. notifications
-- ============================================
CREATE TABLE IF NOT EXISTS notifications (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  type TEXT NOT NULL CHECK (type IN ('founder_action', 'alert', 'info', 'error')),
  priority TEXT NOT NULL CHECK (priority IN ('p1_urgent', 'p2_action', 'p3_review', 'p4_info')),
  title TEXT NOT NULL,
  body TEXT NOT NULL,
  related_entity_type TEXT,
  related_entity_id UUID,
  is_read BOOLEAN DEFAULT false,
  is_actioned BOOLEAN DEFAULT false,
  sent_via TEXT[] DEFAULT '{}',
  created_at TIMESTAMPTZ DEFAULT now(),
  actioned_at TIMESTAMPTZ
);

CREATE INDEX IF NOT EXISTS idx_notifications_unread ON notifications(is_read) WHERE is_read = false;
CREATE INDEX IF NOT EXISTS idx_notifications_priority ON notifications(priority);

-- ============================================
-- 10. audit_log
-- ============================================
CREATE TABLE IF NOT EXISTS audit_log (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  entity_type TEXT NOT NULL,
  entity_id UUID NOT NULL,
  action TEXT NOT NULL,
  old_value JSONB,
  new_value JSONB,
  actor TEXT NOT NULL DEFAULT 'system',
  created_at TIMESTAMPTZ DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_audit_entity ON audit_log(entity_type, entity_id);
CREATE INDEX IF NOT EXISTS idx_audit_created ON audit_log(created_at);

-- ============================================
-- Updated_at triggers
-- ============================================
CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = now();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER tr_county_sources_updated
  BEFORE UPDATE ON county_sources
  FOR EACH ROW EXECUTE FUNCTION update_updated_at();

CREATE TRIGGER tr_opportunities_updated
  BEFORE UPDATE ON opportunities
  FOR EACH ROW EXECUTE FUNCTION update_updated_at();

CREATE TRIGGER tr_claimants_updated
  BEFORE UPDATE ON claimants
  FOR EACH ROW EXECUTE FUNCTION update_updated_at();

CREATE TRIGGER tr_cases_updated
  BEFORE UPDATE ON cases
  FOR EACH ROW EXECUTE FUNCTION update_updated_at();

CREATE TRIGGER tr_documents_updated
  BEFORE UPDATE ON documents
  FOR EACH ROW EXECUTE FUNCTION update_updated_at();
