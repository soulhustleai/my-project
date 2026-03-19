# Claimant Schema

## Purpose

Define the claimant entity — the person who is owed surplus funds.

---

## Fields

```python
class Claimant:
    # Identity
    id: str                        # UUID
    full_name: str                 # As found in records
    first_name: str                # Parsed
    last_name: str                 # Parsed
    middle_name: str | None        # If available
    suffix: str | None             # Jr, Sr, III, etc.
    date_of_birth: date | None     # From enrichment
    ssn_last4: str | None          # Only if provided by claimant during intake

    # Current Contact Info (from enrichment)
    current_address_line1: str | None
    current_address_line2: str | None
    current_city: str | None
    current_state: str | None
    current_zip: str | None
    phone_primary: str | None
    phone_secondary: str | None
    email: str | None

    # Former Address (from surplus record)
    former_address: str | None     # Property address from surplus record

    # Enrichment Metadata
    enrichment_source: str | None      # 'pdl' | 'truepeoplesearch' | 'beenverified' | 'manual'
    enrichment_confidence: float | None # 0.0 - 1.0
    address_verified: bool             # NCOA / Lob verification
    phone_verified: bool               # Phone validation check
    email_verified: bool               # Email validation check
    match_score: float | None          # How confident are we this is the right person?

    # Contact Preferences
    do_not_contact: bool               # Opted out of all contact
    preferred_channel: str | None      # 'phone' | 'email' | 'mail' | 'sms'
    best_time_to_call: str | None      # 'morning' | 'afternoon' | 'evening'
    language: str                       # Default: 'en'

    # Relationship to Property
    relationship: str | None           # 'owner' | 'heir' | 'spouse' | 'entity_member' | 'unknown'

    # Timestamps
    created_at: datetime
    updated_at: datetime
    enriched_at: datetime | None
    last_contacted_at: datetime | None
```

---

## Enrichment Pipeline

```
1. Owner name from surplus record
   ↓
2. Property address cross-reference (county property appraiser)
   ↓
3. People Data Labs API lookup (name + former address → current info)
   ↓
4. Address validation (Lob NCOA check)
   ↓
5. Phone validation (if phone found)
   ↓
6. Confidence scoring:
   - High (>0.8): Name + address + age/DOB match
   - Medium (0.5-0.8): Name + partial address match
   - Low (<0.5): Name only, common name, no address match
   ↓
7. If low confidence → flag for manual review
```

---

## Deduplication Rules

A claimant may appear in multiple surplus records (e.g., multiple properties foreclosed). Dedup by:

1. Exact name + exact former address → same claimant
2. Exact name + same county + similar address → likely same, flag for review
3. Different name + same property → possible entity/heir, create separate claimant

---

## Privacy Notes

- PII encrypted at rest (Supabase handles this)
- PII never logged in plain text to audit_log (use entity_id references only)
- SSN last 4 only collected during intake, never during enrichment
- Claimant can request data deletion (right to be forgotten — comply if requested)
- Minimize data collection to what's needed for the claim
