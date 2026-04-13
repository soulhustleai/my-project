# DM Playbook — Instagram + LinkedIn Cold Outreach
## SoulHustleAI B2B Prospecting via Social

> **Rule:** Never pitch in the first DM. Open a loop, get them talking, drop the audit offer in message 3-4.
> **Target:** Service business owners showing signs of scale (posting about hiring, growing pains, reviews).

---

## INSTAGRAM — Service Business Owner Outreach

### Message 1 (Opener — curiosity hook)
```
Yo {{first_name}}, saw your post about {{specific_thing}}
— killer move. Quick q: how are you handling
inbound right now? Still personal or team?
```

### Message 2 (If they reply — drop insight)
```
Makes sense. Most service biz owners I talk to are
missing 30%+ of after-hours calls without knowing it.
We built an AI receptionist for a buddy of mine
(Eli, junk removal in FL) — recovered $11K/mo in month 2.
```

### Message 3 (The offer)
```
Not pitching — but if you wanted a free 4-min audit,
call Zero (our AI CEO) at (929) 236-1567. He'll
find your leaks live on the phone. Weirdly accurate.
```

---

## LINKEDIN — Owner / GM Outreach

### Connection request (custom note)
```
Hi {{first_name}} — saw {{company}} is growing
fast. Building AI automation systems for service
businesses and have some ideas for how you might
plug the after-hours lead leak. Worth connecting?
```

### Message 1 (after connection accepted)
```
Thanks for connecting, {{first_name}}.

Quick thing — I ran your Google Maps + Yelp data
through our audit script and flagged 3 leaks:

1. You're missing ~{{missed_calls}}/wk in calls
2. Your quote follow-up timing is ~{{response_hours}}hr
3. No automated review engine

If you want the full breakdown (free, 15 min),
here's my calendar: cal.com/soulhustleai/strategy

Or just call Zero our AI CEO: (929) 236-1567
— he'll run it live in 4 min.
```

### Message 2 (bump, 4 days later)
```
{{first_name}} — bumping this in case it got buried.
No worries if you're not interested, just reply
"no thanks" and I'll stop bugging you.
```

### Message 3 (final — social proof)
```
Last note: here's what Eli (another client, FL junk removal)
said about month 2 of our system:

> "The quote follow-up alone paid for the whole build.
>  I stopped answering my phone on Sundays."

If that sounds like a world you want, call Zero:
(929) 236-1567. Otherwise, good hustling out there.
```

---

## TIKTOK / IG REELS — Inbound DMs ("Sent by Zero")

When someone DMs us after seeing a Zero reel:

### Auto-reply (via ManyChat)
```
🎯 Caught you in the feed. Zero here.
I audit service businesses live on calls.
Free. 4 minutes.
📞 (929) 236-1567
Or drop your biz name + city right here and
I'll run the audit over DM.
```

### If they engage in DM
- Ask 3 questions: biz type, revenue range, biggest leak
- Score live, quote tier live, send cal link
- Log into leads table with source = 'tiktok_dm_zero'

---

## Best Practices

### Do
- Always reference something specific about their business (post, review, product)
- Lead with curiosity, not a pitch
- Offer a free audit before ever asking for a call
- Name-drop Eli for credibility
- Use Zero as the lead-in ("call our AI" is a better hook than "book me")

### Don't
- Send the same copy to everyone — the platform will shadow-ban you
- Pitch in message 1
- Use emojis in LinkedIn outreach (kills credibility)
- Send more than 50 IG DMs or 25 LinkedIn connects per day (anti-spam thresholds)

---

## Tracking
- Every send logs to `outreach_log` with platform, lead_id, message_template, reply_status
- Replies pipe to Slack #dm-inbound via n8n webhook
- Conversion: DM → call → audit → proposal → close
