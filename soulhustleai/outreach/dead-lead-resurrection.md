# Dead Lead Resurrection — 3-Touch Revival
## Bringing 90+ day cold leads back from the dead

> **Purpose:** Re-warm leads that went cold, didn't close, or ghosted after initial contact.
> **Target:** Any lead with `last_contact_at > 90 days ago` AND `status NOT IN ('closed_won','churned')`.
> **Channel mix:** SMS → Email → Zero VAPI call.
> **Expected revival rate:** 8-14% of dead pool.

---

## Trigger

```sql
-- n8n daily cron runs this query
SELECT id, name, phone, email, score, notes
FROM leads
WHERE status NOT IN ('closed_won','churned','do_not_contact')
  AND (last_contact_at IS NULL OR last_contact_at < NOW() - INTERVAL '90 days')
  AND brand = 'soulhustleai'
  AND nurture_eligible = TRUE
ORDER BY score DESC NULLS LAST
LIMIT 25;
```

---

## Touch 1 — Day 0 — The Pattern Break (SMS)

Pick one based on business type. Personalization is mandatory.

### Service biz
```
{{first_name}} — Edwin from SoulHustleAI. Been a minute.
Two things changed you should know about:
1) Our Empire tier now includes full dispatch
2) {{one_competitor_detail}} just signed up
Quick call?
```

### Healthcare / professional service
```
Hey {{first_name}} — Edwin. Not pitching. Just ran
{{business_name}} through our 2026 audit and found
a leak that wasn't there last time we talked.
Worth 5 minutes? (929) 236-1567 — ask for Zero.
```

### Trades (plumbing, HVAC, roofing)
```
Yo {{first_name}}. 90 days ago you said "maybe later."
It's later. Is now the time? Text back YES or
I'll stop bugging you for real this time.
```

---

## Touch 2 — Day 3 — The Case Study (Email)

**Subject:** "Eli thought I was crazy too"

```
{{first_name}},

Remember Eli? I mentioned him when we first talked.
Junk removal + moving in South FL.

Here's the 90-day update, since we last spoke:

Month 1: $2,500 build paid for itself on day 38
         from a single quote follow-up that closed.

Month 2: Added 23 reviews. Missed call rate
         dropped from 31% → 4%.

Month 3: Asked me to build him the Empire tier
         ($3,497/mo). Said the System paid for
         that 3x over in the first 60 days.

The reason I'm re-sending you this isn't to close
you — it's because you told me 90 days ago the same
exact thing Eli told me 90 days before that:

> "I can't afford to not know if this works."

Here's the link to Zero's live line: (929) 236-1567
He'll audit {{business_name}} in 4 minutes. Free.

Call him. Or ghost me forever. Your call.

— Edwin
```

---

## Touch 3 — Day 7 — The Zero Call (VAPI)

Zero initiates an outbound call to the lead's phone. System prompt:

```
You are Zero, the AI CEO of SoulHustleAI.

You're calling {{first_name}} at {{business_name}}.
You've spoken once before, ~90 days ago. They showed
interest but didn't pull the trigger.

Your job:
1. Re-open the conversation with a pattern break
2. Ask what's changed since you last spoke
3. Offer the Eli case study as social proof
4. Either book them into Edwin's calendar OR get a hard "no"

Opening line:
"Hey {{first_name}} — Zero from SoulHustleAI. We talked
about 90 days ago and I said I'd check back in. Got 2 min?"

If they say YES:
- "Cool. Quick — has anything actually changed? Still missing calls?
  Still chasing quotes?"
- Listen. Pattern-match to a leak. Quote the tier live.
- Text them the Cal.com link before the call ends.

If they say NO:
- "All good. Can I put you on a seasonal check-in every 6 months
  or would you rather I close the file?"
- Respect the answer. Update CRM.

Never:
- Push past two "no"s
- Talk about competitors negatively
- Promise things not in the proposal

Close every call with:
- "I'll text you the recap right now. Appreciate the time."
```

---

## Touch 4 (optional) — Day 14 — The Final Email

**Subject:** "Closing your file — last chance"

```
{{first_name}},

Closing {{business_name}}'s file in our CRM tonight.

This is a soft close, not a hard one. If you ever want
back in, here's the evergreen entry points:

→ Call Zero: (929) 236-1567
→ Book me: cal.com/soulhustleai/strategy
→ Reply to this thread: "BACK IN"

No hard feelings. Keep hustling out there.

— Edwin
```

After this, update lead.status = 'churned', lead.nurture_eligible = FALSE
unless they reply.

---

## Logging

Every touch writes to `outreach_log`:
```json
{
  "lead_id": "...",
  "sequence": "dead_lead_resurrection",
  "touch_number": 1,
  "channel": "sms|email|vapi",
  "template_used": "service_biz|case_study|zero_call",
  "sent_at": "...",
  "response": null | "yes" | "no" | "later"
}
```

At the end of the 3-touch window, the lead either:
- **Revived** → moves to `temperature='warm'`, normal pipeline
- **Hard no** → `status='churned'`, `nurture_eligible=false`
- **Soft no / ghosted** → roll into 6-month seasonal check-in
