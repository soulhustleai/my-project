# SMS Scripts — SoulHustleAI Outreach
## Zero's Voice — Short, Direct, Unmistakable

> **Rule #1:** Every SMS ends with a call-to-action that's either a phone number, a link, or a reply keyword. Never a dead end.
> **Rule #2:** Max 160 chars per message. If it needs to be longer, send 2 messages 4 seconds apart.
> **Rule #3:** Never send before 9am or after 8pm local time.
> **Trigger:** lead.temperature IN ('warm','hot') AND lead.phone IS NOT NULL

---

## 1. COLD OPENER (after enrichment, never-contacted)

```
Hey {{first_name}}, Edwin from SoulHustleAI. Eli @ Abundantly
Blessed said you'd be the guy I should hit up about AI
automation. Got 2 min for a quick roast of your setup?
```

**Follow-up (if no reply in 24hr):**
```
No worries if not. Here's Zero our AI CEO — call him direct,
he'll audit you in 4 min, no sales rep: (929) 236-1567
```

---

## 2. WARM OPENER (replied to cold email, haven't booked yet)

```
{{first_name}} — saw you opened my email but no book yet.
Easier way: text "AUDIT" to (929) 236-1567 and Zero
runs the whole intake over SMS. Free. Takes 3 min.
```

---

## 3. MISSED CALL AUTORESPONDER (for Zero inbound)

```
Hey! This is Zero from SoulHustleAI — sorry I missed you.
Text me your biz name + biggest leak and I'll audit you
in 2 min. Or book Edwin direct: cal.com/soulhustleai/strategy
```

---

## 4. QUOTE FOLLOW-UP (24hr after proposal sent)

```
{{first_name}} — Edwin. Did the proposal land? Happy to hop
on a 10-min call to walk through it. Or if it's a no,
just reply "not now" and I'll get out of your hair.
```

**Follow-up (+48hr):**
```
One more thing {{first_name}}: the 10% build discount
expires tonight at midnight. If you want it locked in,
reply "LOCK IT" and I'll send the invoice.
```

---

## 5. DEAD LEAD RESURRECTION (90+ days no contact)

```
Yo {{first_name}}, Edwin from SoulHustleAI. Been 90 days
since we talked. Two things changed that might move
the needle: [1] new Empire tier includes dispatch,
[2] we just onboarded your competitor. Call me?
```

---

## 6. REFERRAL ASK (after 5-star review or happy touchpoint)

```
{{first_name}} — appreciate that 5-star 🙏. Quick ask:
know one other owner drowning in missed calls?
I'll Venmo you $250 if they sign. No weirdness —
just forward them: soulhustleai.com/apply
```

---

## 7. CLIENT ESCALATION (something broken, proactive)

```
{{first_name}} — Edwin. Heads up: n8n flagged an issue
on your {{workflow_name}} at {{time}}. Already fixing it.
Expected back online in {{eta}}. I'll text when it's live.
```

**Follow-up (when resolved):**
```
Back online. Root cause was {{cause}}. Adding a
watchdog so this can't happen again. My apologies.
```

---

## 8. UPSELL TO EMPIRE (from System tier, after 60+ days)

```
{{first_name}} — 60 days in, you're crushing it.
The System recovered ${{revenue}} so far.
Empire tier would unlock the dispatch + review
engine we've been talking about. Call me 10 min?
```

---

## Implementation

- **Twilio number:** +1 (844) 643-9825 (10DLC pending — use Resend email fallback)
- **Sending:** n8n HTTP node → Twilio API → Supabase sms_log write
- **Compliance:** All messages must have ability to reply STOP/OPT-OUT
- **Log every send** to `sms_log` with lead_id, template_used, body, direction, status
