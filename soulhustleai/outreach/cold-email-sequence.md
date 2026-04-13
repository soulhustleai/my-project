# Cold Email Sequence — SoulHustleAI
## "The Audit Offer" — 5 emails over 12 days

> **Purpose:** Take a cold B2B lead (service business $100K–$2M) from zero awareness to "book the audit call."
> **Goal metric:** 8-12% reply rate, 3-5% book rate.
> **Send from:** edwin@soulhustleai.com (never "info@" or "team@")
> **Tracking:** Resend + PostHog
> **Trigger:** lead.status = 'enriched' AND lead.brand = 'soulhustleai' AND lead.email IS NOT NULL

---

## Email 1 — Day 0 — "One-line observation"

**Subject:** {{business_name}} — quick thing I noticed

```
{{first_name}},

I was poking around {{business_name}} this morning (a buddy of mine
runs {{related_business_eli_or_similar}} and he mentioned you).

Three things stood out:

1. You're missing about {{missed_call_estimate}}/mo in calls
   (I pulled it from your Google Maps + BrightLocal data)
2. Your Yelp response time is {{yelp_response_time}}
3. You have zero automated follow-up on quotes

The first one alone is costing you ~${{leak_dollar_amount}}/year.

I build AI systems that plug all three in under 45 days.
Would a 15-min teardown of your setup be useful?

— Edwin
Founder, SoulHustleAI
P.S. You can also just call Zero (our AI CEO) at (929) 236-1567.
     He'll audit you live over the phone in 4 minutes.
```

---

## Email 2 — Day 3 — "The Eli case study"

**Subject:** Re: {{business_name}} — how Eli did it

```
{{first_name}},

Quick follow-up on my last note.

One of our clients — Eli, runs a junk removal + moving company in South FL —
was in almost the exact spot {{business_name}} is in now:

  - Missing 30%+ of after-hours calls
  - No quote follow-up
  - Review count stuck at 42 for 2 years

We built him a 7-automation system in 3 weeks. In the first 60 days:

  ✦ Missed call rate dropped to 4%
  ✦ Quote close rate jumped from 28% → 46%
  ✦ Added 23 reviews (now at 65)
  ✦ Monthly revenue attributed to automations: $11,400

The build was $2,500. Retainer is $1,497/mo.
Paid for itself in 6 weeks.

Want me to run the same audit on {{business_name}}?
It's free — I just need 15 minutes on the phone.

https://cal.com/soulhustleai/strategy

— Edwin
```

---

## Email 3 — Day 6 — "The free ROI calculator"

**Subject:** I built you a revenue leak calculator

```
{{first_name}},

No pitch in this one — just something useful.

Built a 2-minute ROI calculator that shows you exactly where your
service business is bleeding money:

  → https://soulhustleai.com/roi-calculator.html

You just plug in 4 numbers (calls/week, missed %, avg job, close rate)
and it spits out the leak. No email capture. No BS.

If the number scares you, my calendar's here:
https://cal.com/soulhustleai/strategy

If it doesn't, delete this and keep hustling.

— Edwin
```

---

## Email 4 — Day 9 — "The hard ask"

**Subject:** Am I reading this wrong?

```
{{first_name}},

I've sent you three emails. Either:

  (a) I'm barking up the wrong tree and {{business_name}} is already dialed in
  (b) You're swamped — totally fair
  (c) You're curious but haven't hit reply

If it's (a), tell me "we're good" and I'll stop.

If it's (b), just reply "later" and I'll ping you in 60 days.

If it's (c), call Zero at (929) 236-1567. He's an AI — takes 4 minutes.
No sales rep, no BS. If it's not a fit, he hangs up. If it is, he books you.

— Edwin
```

---

## Email 5 — Day 12 — "The door closes"

**Subject:** Closing your file today

```
{{first_name}},

Last email from me. Not playing pushy sales guy — I'm literally
closing your file in our CRM tonight so my system stops pinging you.

If you ever want that audit, the offer stands forever:

  → Call Zero: (929) 236-1567
  → Book me: https://cal.com/soulhustleai/strategy
  → Reply to this thread with "LET'S GO"

Best of luck out there. Keep building.

— Edwin
Founder, SoulHustleAI

---

P.S. If you're not the right person but know someone who'd want this,
forward this email. If they sign, I'll Venmo you $250 as a thank-you.
```

---

## Implementation Notes

### Sending tool
- **Primary:** Resend + custom n8n workflow (status: built)
- **Fallback:** Manual send via Gmail for warm leads

### Personalization variables (must be filled per lead)
- `{{first_name}}`
- `{{business_name}}`
- `{{missed_call_estimate}}` (calculated from enrichment)
- `{{yelp_response_time}}` (pulled from yelp_fusion source)
- `{{leak_dollar_amount}}` (calculated — ~30% × avg_revenue × 0.05)
- `{{related_business_eli_or_similar}}` (if applicable — else delete)

### Anti-spam best practices
- No unsubscribe link (b2b outbound, opt-out via reply)
- DKIM + SPF + DMARC on soulhustleai.com
- Max 50 sends/day to stay warm
- Random 30-90s delay between sends
- Never send Sunday or before 8am / after 7pm local

### Tracking
- Each email writes event to `email_sends` table
- Replies pipe back via IMAP → n8n → CRM update
- Open/click via Resend webhook → PostHog
