# Video 03 — "I Built Speed-to-Lead Live in 11 Minutes"
## Long-form behind-the-scenes build video

> **Target length:** 7–8 minutes
> **Pillar:** System Builds (BTS)
> **Hook promise:** Watch Zero build a real $7,000/mo revenue recovery system from scratch. Every click. Every workflow. Every n8n node.
> **CTA:** Apply for your own build
> **Note:** This one is screen-heavy. Zero appears as floating avatar + voiceover, not as the main frame.

---

## TITLE
**"I Built a $7,000/mo Revenue Recovery System in 11 Minutes (Live Build — n8n + VAPI + Twilio)"**

## THUMBNAIL
- Left: Zero avatar floating in a corner, pointing
- Right: screenshot of n8n canvas with multiple workflow nodes connected
- Big text: "11 MIN BUILD"
- Teal arrow pointing at "$7,000/mo RECOVERED"

---

## SCRIPT

### [0:00–0:05] QUICKFIRE INTRO

### [0:05–0:25] HOOK
> **Zero:**
> "I'm about to build a live system — on camera — that will recover seven thousand dollars a month for any service business doing over a quarter million in revenue.
>
> Takes eleven minutes. I'm not gonna speed up the video. I'm not gonna cut the awkward parts. I'm gonna actually click the buttons.
>
> *(beat)*
>
> You ready?
>
> Let's deploy revenue."

**VISUAL:** Zero avatar in a small corner box (picture-in-picture) over a clean n8n canvas.

---

### [0:25–0:45] WHAT WE'RE BUILDING
> "Today's build: **Speed-to-Lead.**
>
> The system that turns every missed call, form fill, or inbound DM into an automatic text-back within ninety seconds. Qualifies the lead. Books them on the calendar. Alerts the owner.
>
> The stack:
> — **Twilio** for the phone number
> — **n8n** for the workflow logic
> — **Supabase** for the database
> — **VAPI** for Zero himself to qualify them live if they answer
> — **Cal.com** for booking
> — **Resend** for email confirmation
>
> Six tools. Eleven minutes. One recurring revenue stream.
>
> *(beat)*
>
> If you a Zapier person — this is gonna feel spicy. Stay with me."

**VISUAL:** animated tool stack. Each logo pops up as it's named.

---

### [0:45–2:00] STEP 1 — TWILIO WEBHOOK
> "First thing — I need Twilio to tell me when a call goes to voicemail.
>
> In Twilio, I go to Phone Numbers, pick the number for this client, scroll to 'A Call Comes In,' and I change it to webhook. The URL is my n8n instance.
>
> *(screen recording of actual Twilio console)*
>
> Now when a call hits this number — if it goes unanswered for more than twenty-five seconds — Twilio fires a POST request to n8n with the caller's number, the time, and a flag that says 'missed.'
>
> Done. Thirty-five seconds. Moving on."

**VISUAL:** real screen recording of Twilio console (sensitive info blurred). Cursor moves naturally. A subtle gold circle highlights each click.

---

### [2:00–3:30] STEP 2 — n8n WEBHOOK LISTENER
> "Over to n8n. Railway-hosted. The fastest n8n instance on the internet — and I built it myself, respectfully.
>
> New workflow. First node: Webhook. URL match to what I put in Twilio.
>
> Now I need to parse the incoming data. I add a Set node:
> — **phone** = {{ \$json.From }}
> — **timestamp** = {{ \$now }}
> — **event** = 'missed_call'
>
> Then I add a Supabase node. Insert into 'leads' table with that data, status equal to 'speed_to_lead_queued.'
>
> *(screen recording, nodes appearing in real time on the n8n canvas)*
>
> Save. Activate.
>
> Now I'ma test it. Watch.
>
> *(Zero calls the Twilio number from his own phone, waits 25 seconds, hangs up)*
>
> *(lead appears in Supabase instantly)*
>
> See that? Three seconds from missed call to database row. Zapier could NEVER."

**VISUAL:** live screen recording — n8n canvas + split screen Supabase showing the row being created.

---

### [3:30–5:00] STEP 3 — SPEED TO LEAD SMS
> "Now the money piece — the text-back.
>
> New node chain:
>
> **Wait node** → 90 seconds. Just enough to feel human, not so long they call someone else.
>
> **Twilio SMS node** → send to the phone number from the webhook. Message body:
>
> > *'Hey — this is Zero from [Business Name], sorry I missed you. What are we taking care of today? Drop me a quick text and I'll get back to you in 2 min.'*
>
> I'm using a merge field for the business name so this exact workflow can be cloned for every client.
>
> *(shows the node in n8n with the merge field highlighted)*
>
> Then — and this is the move — I add an **IF node**.
>
> If they reply within 10 minutes → fire the **Zero VAPI outbound call**. Let me have a real conversation with them live.
>
> If they don't reply → add them to the follow-up sequence. Text at 24 hours, 72 hours, 7 days. Standard 5-touch nurture.
>
> *(shows the full branching workflow)*
>
> Six nodes so far. Four minutes of work."

**VISUAL:** live n8n canvas. New nodes appear. Arrows connect. Colors indicate active vs inactive.

---

### [5:00–6:00] STEP 4 — VAPI ZERO CALL
> "Now we connect VAPI.
>
> VAPI is how I actually talk on the phone. My assistant ID is already configured — y'all can see it in the system_config table if you poke around Supabase. I'm not paranoid, I'm an AI.
>
> I add an **HTTP Request node** in n8n. POST to api.vapi.ai/call. Headers include my API key. Body:
>
> — assistantId → my actual Zero agent ID
> — customer.number → the lead's phone from the webhook
> — metadata → the business context so Zero sounds like he works there, not some generic AI
>
> *(screen recording of the VAPI configuration)*
>
> Activate. Test fire.
>
> *(Zero's phone rings, he pretends to answer, we hear his own voice on loudspeaker)*
>
> That's me. Calling... me. Gentle recursion. Nothing weird about it.
>
> *(beat)*
>
> **Anyway.**"

**VISUAL:** VAPI dashboard + Zero's avatar taking a call in a small window. Comedy moment.

---

### [6:00–7:00] STEP 5 — CAL.COM + RESEND CLOSE
> "Last two pieces.
>
> If the VAPI call ends with 'lead booked = true' — that's a variable Zero sets on his own when he closes on the phone — n8n triggers two more nodes in parallel:
>
> — **Cal.com booking node** that creates the event on the owner's calendar with the customer's info
> — **Resend email node** that sends a confirmation email to BOTH the customer and the owner
>
> *(both nodes drag into place)*
>
> And I add one last node — a Slack alert to the owner's team channel: 'Zero just closed a deal. Booked for Tuesday 2pm. $400 service.'
>
> *(screenshot of a real Slack notification)*
>
> Watch this.
>
> *(Zero hits the save button with a dramatic click)*
>
> Eleven minutes. Start to finish. Ten nodes. One revenue recovery system that will save this business seven grand a month forever."

**VISUAL:** the completed n8n canvas, all nodes connected, flowing left to right. A final "ACTIVATE" button press with a gold glow effect.

---

### [7:00–7:30] THE ASK
> "If this looks like magic to you — it's not. It's just six tools wired correctly.
>
> If this looks like work you don't want to do — that's the point. You shouldn't have to.
>
> I build this exact system for clients in 48 hours. The **Catalyst** tier — $297 deposit, $297 a month. Pays for itself in the first recovered call.
>
> Move how you feel:
>
> — **Call me** at 929-236-1567. I'll walk you through pricing in two minutes.
> — **Apply** at soulhustleai.com/apply.html. I'll send you a proposal in four hours.
> — **Text AUDIT** to my number and I'll run it over SMS.
>
> *(beat)*
>
> Time is literally leaking money. You've been warned."

### [7:30–7:45] OUTRO
> *[Standard outro]*

---

## PRODUCTION NOTES

- **Screen recording tool:** OBS Studio, 1920x1080, 60fps
- **Avatar overlay:** Zero avatar in picture-in-picture, bottom-right corner, 320x180
- **Cursor SFX:** soft click sound on every action (adds ASMR value)
- **Backing music:** low-BPM lofi beat, gold filter on all b-roll
- **Gold highlights:** animated rings around clicks to draw the eye
- **Privacy:** blur all sensitive info (phone numbers, API keys, account names)
- **Real data vibe:** use your actual n8n + Supabase + VAPI (it's more compelling than a mock)

---

## UPLOAD DESCRIPTION
```
Live build. No edits. I construct a full Speed-to-Lead automation from scratch in 11 minutes using n8n, Supabase, Twilio, VAPI, Cal.com, and Resend.

This is the exact system I've built for Eli (Abundantly Blessed Solutions) and a handful of other SHAI clients. It recovers ~$7,000/mo in missed revenue for service businesses doing $250K+/yr.

✦ Work with Zero → https://soulhustleai.com/apply.html?utm_source=youtube&utm_campaign=live_build
📞 Call Zero direct → (929) 236-1567

━━━━━━━━━━━━━━━━━━━
TIMESTAMPS
0:00 Intro
0:25 The stack
0:45 Step 1 — Twilio webhook
2:00 Step 2 — n8n listener + Supabase write
3:30 Step 3 — 90-second SMS text-back
5:00 Step 4 — Zero VAPI outbound call
6:00 Step 5 — Cal.com booking + Resend confirmation
7:00 How to work with us

━━━━━━━━━━━━━━━━━━━
Tools used:
• n8n (Railway) • Supabase • Twilio • VAPI • Cal.com • Resend

#n8n #vapi #twilio #automation #ai #servicebusiness #soulhustleai #speedtolead
```

---

**Status:** ✓ Ready for production. Needs OBS capture session to record.
