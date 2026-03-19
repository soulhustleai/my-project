# County Source Registry — VALIDATED

## Research Findings (March 2026)

**Key discovery:** Florida's big counties do NOT publish simple downloadable surplus funds lists like smaller counties (e.g., Sumter, Brevard) do. Instead, surplus funds data must be assembled from multiple sources.

---

## How Florida Surplus Fund Lead Generation Actually Works

### The Real Workflow (confirmed from operator research)

1. **Monitor foreclosure auction results** on `[county].realforeclose.com`
2. **Identify properties that sold above judgment amount** (overbid = surplus)
3. **Look up the case** on the clerk's online case search portal to find:
   - Final judgment amount
   - Sale price (from Certificate of Sale)
   - Certificate of Disbursement (shows surplus amount)
   - Defendant/owner name
   - Property address (from lis pendens or case filings)
4. **Cross-reference** with county property appraiser for owner details
5. **Skip trace** the former owner for current contact info

### This means our pipeline needs TWO data sources per county:
1. **Foreclosure auction results** (realforeclose.com) — to identify overbids
2. **Clerk case search portal** — to get surplus amounts, owner names, property details

### For Tax Deed Surplus (separate from foreclosure):
- Broward: `broward.deedauction.net/reports/total_sales` + `broward.org/RecordsTaxesTreasury/TaxesFees/Pages/Overbid.aspx`
- Tax deed overbids are tracked separately by the tax collector, not the clerk

---

## Validated Sources — Broward County, FL

### Foreclosure Surplus
| Field | Value |
|-------|-------|
| Auction platform | `https://broward.realforeclose.com` |
| Case search portal | `https://www.browardclerk.org` (online records search) |
| Data method | Monitor auction results → cross-reference case for surplus |
| Auction schedule | Monday-Friday, properties listed on auction calendar |
| Key page | Auction calendar shows upcoming and past sales |
| Login required? | Yes for bidding; browsing calendar/results may be public |
| Surplus list published? | **NO** — must be assembled from auction results + case lookups |

### Tax Deed Surplus
| Field | Value |
|-------|-------|
| Auction platform | `https://broward.deedauction.net` |
| Past results | `https://broward.deedauction.net/reports/total_sales` |
| Overbid file (historical) | `https://www.broward.org/RecordsTaxesTreasury/TaxesFees/Pages/Overbid.aspx` |
| Surplus affidavit form | `https://www.broward.org/RecordsTaxesTreasury/TaxesFees/Documents/Affidavit_TaxDeed_Surplus_Funds_Post.pdf` |
| Data method | Download overbid file, identify surplus amounts |
| Login required? | May need login for full auction list download |

### Property Appraiser
| Field | Value |
|-------|-------|
| URL | `https://web.bcpa.net/BcpaClient/` |
| Purpose | Look up property details, owner of record, address |

### Key Contacts
- Court Registry Clerk: (954) 831-5659
- Finance Division: APClerk@browardclerk.org
- Filing address: Broward County Records Division, Governmental Center, Room 114, Fort Lauderdale, FL 33301

---

## Validated Sources — Palm Beach County, FL

### Foreclosure Surplus
| Field | Value |
|-------|-------|
| Auction platform | `https://palmbeach.realforeclose.com` |
| Clerk foreclosure page | `https://www.mypalmbeachclerk.com/departments/courts/foreclosures` |
| General info | `https://www.mypalmbeachclerk.com/departments/courts/foreclosures/general-information` |
| Owner's Claim form | Available for download on the foreclosure page |
| Data method | Monitor auction results → case lookup for surplus |
| Surplus list published? | **NO** — "the excess funds list is not available to download or preview online" (confirmed) |
| Alternative | "Generate your own list by following auction reports and verifying funds with case research" |
| Clerk Cart (paid reports) | Can order foreclosure case reports via Clerk Cart system |

### Key Contacts
- Foreclosures department: (561) 355-6240
- Address: Main Courthouse, 205 N. Dixie Hwy., Room 3.2400, West Palm Beach, FL 33401
- Hours: Mon-Fri 8 AM - 4 PM

---

## Validated Sources — Hillsborough County, FL

### Foreclosure Surplus
| Field | Value |
|-------|-------|
| Auction platform | `https://hillsborough.realforeclose.com` |
| Clerk website | `https://www.hillsclerk.com` |
| Circuit Civil page | `https://www.hillsclerk.com/Court-Services/Circuit-Civil` |
| Unclaimed funds page | `https://www.hillsclerk.com/records-and-reports/unclaimed-funds` |
| Case search (HOVER) | Hillsborough Online Viewing of Electronic Records |
| Data method | Monitor auction results → case lookup for surplus via HOVER |
| Surplus list published? | **NO** — must request "Statement of Registry Funds" per case |
| Request method | e-Filing Portal, mail to PO Box 3360 Tampa FL 33601, or in-person |

### Tax Deed Surplus
| Field | Value |
|-------|-------|
| Tax Collector | `https://www.hillstaxfl.gov/taxes/tax-certificate/tax-deeds/` |

### Key Contacts
- Main office: 800 E. Twiggs Street, Room 101, Tampa, FL 33602
- Phone: 813-276-8100
- Accounting: CCCACCT@hillsclerk.com

---

## Revised Pipeline Strategy

Given that these counties don't publish simple surplus lists, our scraping approach changes:

### Phase 1: Monitor Auctions (Automated)
```
1. Scrape [county].realforeclose.com daily
2. Capture completed auction results:
   - Case number
   - Property address
   - Final bid amount
3. Store in raw_records
```

### Phase 2: Case Enrichment (Semi-Automated)
```
4. For each completed sale, look up the case on clerk portal:
   - Get final judgment amount
   - Calculate surplus: sale_price - judgment_amount - costs
   - Get defendant/owner name
5. Filter: surplus > $1,000
6. Store qualified opportunities
```

### Phase 3: Owner Enrichment (Automated)
```
7. Cross-reference owner name with property appraiser
8. Skip trace for current contact info
9. Standard outreach pipeline
```

### Why This Changes Things
- **It's slightly more work** than downloading a PDF list
- **But it also means less competition** — operators who rely on pre-made lists miss these counties
- **The data is fresher** — we get it from auction results in near-real-time
- **Smaller counties** (Sumter, Brevard, Polk, Lee, Pasco) DO publish downloadable surplus lists and can be added as easy wins

---

## Easy-Win Counties to Add (Published Surplus Lists)

These Florida counties publish downloadable surplus lists:

| County | URL | Format |
|--------|-----|--------|
| Sumter | `https://www.sumterclerk.com/surplus-funds-list` | PDF lists on page |
| Brevard | `https://www.brevardclerk.us/tax-deed-surplus` | Online list |
| Polk | `https://www.polkclerkfl.gov/280/Surplus-Funds-List` | Published list |
| Lee | `https://www.leeclerk.org/departments/courts/property-sales/tax-deed-sales/tax-deed-reports` | Reports page |
| Pasco | `https://www.pascoclerk.com/839/Tax-Deed-Surplus` | Published list |
| Columbia | `https://columbiaclerk.com/tax-deed-unclaimed-funds-list/` | Published list |
| Marion | `https://www.marioncountyclerk.org/.../unclaimed-funds/` | Published list |

**Recommendation:** Start with these easy-win counties for immediate leads while building the auction-monitoring pipeline for the big 3.
