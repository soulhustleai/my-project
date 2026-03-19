# Claimant Enrichment Flow

## Trigger
New opportunities with status = 'qualified' and score >= 20

## Flow

```
START (qualified opportunity)
  │
  ├─ 1. EXTRACT IDENTITY
  │   ├─ Get owner_name from opportunity
  │   ├─ Get property_address from opportunity
  │   ├─ Check if claimant already exists (by name + former address)
  │   └─ If exists → link opportunity to claimant, skip enrichment
  │
  ├─ 2. PRIMARY ENRICHMENT (People Data Labs API)
  │   ├─ Search by: name + address (former property address)
  │   ├─ If match found:
  │   │   ├─ Extract: current address, phone, email, DOB
  │   │   ├─ Calculate match confidence
  │   │   └─ Create claimant record (enrichment_source: 'pdl')
  │   └─ If no match → proceed to fallback
  │
  ├─ 3. FALLBACK ENRICHMENT (if primary fails)
  │   ├─ Option A: TruePeopleSearch (manual or scripted)
  │   ├─ Option B: Whitepages API
  │   ├─ Option C: BeenVerified
  │   └─ If all fail → create claimant with partial data, flag for manual
  │
  ├─ 4. ADDRESS VALIDATION
  │   ├─ Validate current address via Lob address verification
  │   ├─ NCOA check (has the person moved?)
  │   ├─ If address invalid → mark address_verified: false
  │   └─ If valid → mark address_verified: true
  │
  ├─ 5. CONTACT SCORING
  │   ├─ Has valid address? +30 points
  │   ├─ Has phone? +30 points
  │   ├─ Has email? +20 points
  │   ├─ Address verified? +10 points
  │   ├─ High name match confidence? +10 points
  │   ├─ Score → enrichment_confidence (0.0-1.0)
  │   └─ If confidence > 0.5 → opportunity status: 'contactable'
  │       If confidence <= 0.5 → flag for manual enrichment
  │
  └─ 6. LINK
      ├─ Link opportunity.claimant_id → claimant.id
      ├─ Update opportunity status
      └─ Log in audit_log
END
```

## Rate Limiting
- PDL: respect API rate limits (batch if possible)
- Max 100 enrichments per day at MVP (cost control)
- Process highest-scored opportunities first

## Outputs
- claimants table: new or updated claimant record
- opportunities table: claimant_id linked, status updated
- audit_log: enrichment events
