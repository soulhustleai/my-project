# Opportunity Scoring Model

## Purpose

Score every opportunity on a 0-100 scale to prioritize outreach. Higher score = more likely to be worth pursuing.

---

## Scoring Factors

| Factor | Weight | Range | Description |
|--------|--------|-------|-------------|
| Surplus Amount | 40% | 0-40 pts | Higher surplus = higher score |
| Recency | 20% | 0-20 pts | More recent = higher score |
| Claimant Identifiability | 20% | 0-20 pts | Clearer name/identity = higher score |
| County Filing Ease | 10% | 0-10 pts | Simpler filing = higher score |
| Competition Estimate | 10% | 0-10 pts | Less competition = higher score |

---

## Scoring Rules

### Surplus Amount (0-40 points)

```python
def score_amount(surplus_amount: float) -> float:
    if surplus_amount >= 50000: return 40
    if surplus_amount >= 25000: return 35
    if surplus_amount >= 15000: return 30
    if surplus_amount >= 10000: return 25
    if surplus_amount >= 5000:  return 20
    if surplus_amount >= 3000:  return 12
    if surplus_amount >= 1000:  return 5
    return 0  # Below threshold — disqualify
```

### Recency (0-20 points)

```python
def score_recency(sale_date: date, today: date) -> float:
    days_ago = (today - sale_date).days
    if days_ago <= 30:   return 20
    if days_ago <= 90:   return 18
    if days_ago <= 180:  return 15
    if days_ago <= 365:  return 10
    if days_ago <= 730:  return 5
    return 2  # Very old but may still be claimable
```

### Claimant Identifiability (0-20 points)

```python
def score_identifiability(owner_name: str) -> float:
    if not owner_name:
        return 0
    # Full name (first + last)
    if ' ' in owner_name.strip() and not is_entity(owner_name):
        if len(owner_name.split()) >= 2:
            return 20
    # Entity name (LLC, Corp, Trust, etc.)
    if is_entity(owner_name):
        return 5
    # Single name or unclear
    return 8

def is_entity(name: str) -> bool:
    entities = ['llc', 'inc', 'corp', 'trust', 'estate', 'bank', 'association']
    return any(e in name.lower() for e in entities)
```

### County Filing Ease (0-10 points)

```python
# Pre-configured per county in county_sources
COUNTY_FILING_EASE = {
    'Broward_FL': 7,
    'Palm Beach_FL': 7,
    'Hillsborough_FL': 8,
    'Cuyahoga_OH': 9,
    'Franklin_OH': 9,
    'Maricopa_AZ': 8,
}
```

### Competition Estimate (0-10 points)

```python
# Pre-configured per county — based on how quickly leads get picked up
COUNTY_COMPETITION = {
    'Broward_FL': 4,       # High competition
    'Palm Beach_FL': 5,    # Medium-high
    'Hillsborough_FL': 7,  # Medium
    'Cuyahoga_OH': 8,      # Low-medium
    'Franklin_OH': 9,      # Low
    'Maricopa_AZ': 6,      # Medium
}
```

---

## Composite Score

```python
def score_opportunity(opportunity) -> float:
    return (
        score_amount(opportunity.surplus_amount) +
        score_recency(opportunity.sale_date, date.today()) +
        score_identifiability(opportunity.owner_name) +
        COUNTY_FILING_EASE.get(f"{opportunity.county}_{opportunity.state}", 5) +
        COUNTY_COMPETITION.get(f"{opportunity.county}_{opportunity.state}", 5)
    )
```

---

## Thresholds

| Score Range | Action |
|-------------|--------|
| 0-19 | DISQUALIFY — don't pursue |
| 20-39 | LOW — enrich only if capacity allows |
| 40-59 | MEDIUM — enrich and outreach |
| 60-79 | HIGH — priority outreach |
| 80-100 | PREMIUM — immediate outreach + phone call |

---

## Calibration

This model will be recalibrated after 50+ leads go through the full funnel. Actual conversion data will inform weight adjustments.

Track: score at enrichment vs. conversion outcome. If high-scored leads don't convert and low-scored ones do, adjust.
