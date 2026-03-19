# Audit Log Schema

## Purpose

Immutable record of every significant action in the system. Required for compliance, debugging, and operational transparency.

---

## What Gets Logged

| Entity | Events Logged |
|--------|--------------|
| opportunities | created, status_change, score_updated, claimant_linked, disqualified |
| claimants | created, updated, enriched, do_not_contact_set |
| outreach_events | created (every send and receive) |
| cases | created, status_change, doc_uploaded, claim_filed, approved, disbursed, closed |
| documents | created, status_change |
| notifications | created, read, actioned |
| county_sources | check_started, check_succeeded, check_failed |

---

## Log Entry Structure

```sql
-- Already defined in core-data-model.md
-- Key fields:
--   entity_type: which table
--   entity_id: which record
--   action: what happened
--   old_value: previous state (JSONB)
--   new_value: new state (JSONB)
--   actor: who/what did it
--   created_at: when
```

## Actor Types

| Actor | Description |
|-------|-------------|
| system:source-monitor | Source monitoring service |
| system:record-ingestion | Record ingestion service |
| system:normalization | Normalization pipeline |
| system:opportunity-engine | Scoring engine |
| system:claimant-enrichment | Skip trace service |
| system:outreach-engine | Outreach sending service |
| system:document-engine | Document generation |
| system:submission-engine | Claim filing service |
| system:case-tracker | Status tracking service |
| system:notifications | Notification service |
| founder | Edwin (manual actions) |
| claimant | Claimant (form submissions, responses) |
| webhook:jotform | Jotform webhook |
| webhook:twilio | Twilio inbound webhook |
| webhook:lob | Lob delivery webhook |

---

## Retention Policy

- Keep all audit logs for minimum 7 years (legal/compliance)
- No deletion of audit log entries (append-only)
- Archive to cold storage after 2 years if needed for cost

---

## Querying Patterns

```sql
-- Full history of a case
SELECT * FROM audit_log
WHERE entity_type = 'cases' AND entity_id = '[case_id]'
ORDER BY created_at;

-- All status changes today
SELECT * FROM audit_log
WHERE action = 'status_change' AND created_at >= CURRENT_DATE
ORDER BY created_at;

-- All founder actions
SELECT * FROM audit_log
WHERE actor = 'founder'
ORDER BY created_at DESC;

-- Source monitoring failures
SELECT * FROM audit_log
WHERE entity_type = 'county_sources' AND action = 'check_failed'
AND created_at >= now() - interval '7 days';
```
