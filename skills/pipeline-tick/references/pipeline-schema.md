# Pipeline Schema

## Database
- **Data source ID** (for MCP `API_query_data_source`): `c6209e29-55ef-4781-b735-73b2a254e34f`
- **Database ID** (for REST API `/v1/databases/{id}/query`): `78b26ebe-5b4f-4ff2-884a-3ccf369d00e6`

## Properties set by skills

| Property | Type | What to set |
|---|---|---|
| Contact Name | title | Decision-maker's full name |
| Business Name | text | Brand name if different |
| Email | email | Decision-maker email |
| Profile URL | url | IG profile or wherever found |
| Site URL | url | Website / funnel entry point |
| Niche | multi_select | Conscious Parenting, Gentle Parenting, Sleep, Screen Time, Faith-based, Special Needs, Postpartum, Educator, Mom Mental Health, Other |
| Followers | number | IG follower count |
| Platform | select | Kajabi, Skool, Shopify, Teachable, Thinkific, Podia, Squarespace, WordPress, GHL, Other, Unknown |
| Main Offer | text | Primary paid product + price |
| Source | select | Lateral Discovery, Hashtag, Podcast, Google Search, Comments, Referral, Directory, Other |
| Tier | select | Tier 1: Start here, Tier 2: Qualify first, Tier 3: Long play, Tier 4: Skip |
| Notes | text | One-line flag. Full detail in body |
| Lane | select | Lane 1: Felt leak, Lane 2: No leak, Lane 3: Skip |
| Finding Type | select | No opt-in capture, Weak/no nurture sequence, Broken checkout, No order bump/upsell, Weak sales page, No launch system, Dead/stale element, Other |
| Status | select | Researching → Audit Ready → Outreach Sent → Reply Received → Loom Sent → Call Booked → Won / Lost / Disqualified / Dormant |
| Sequence | select | Cold / Warm |
| Touch # | number | Increment on every send |
| Est. Value | select | $300-600, $1.2k-2.5k, $2k-3.5k/mo, Retainer, Unknown |
| Lost Reason | select | Only when Status = Lost |
| Last Contacted | date | Most recent outreach touch |
| Next Action | date | Date to follow up or revisit |
| Last Update | auto | System-managed |

## Page body structure

```
## Overview
One paragraph. Name, business, niche, platform, main offer.

## Funnel Walk
Stop X — [what's there] — [what it means]
(Skip clean unremarkable stops)

## Evidence
IG evidence: [paste the literal `python main.py vision check evidence/<slug>` output covering the ig/ images, e.g. "VISION PASS: COMPLETE — 4 of 4 required images confirmed read"] OR "none attached — site-only walk". If the line says INCOMPLETE, write INCOMPLETE, plus which paths, plus the reason if known — do not round up to "read."
Site vision pass: [paste the literal `vision check` output covering the site screenshots] OR the same INCOMPLETE-with-detail treatment.
Machine flags rejected in the vision pass: [N — one-word reason each] OR "none rejected"

## Gate 1
Solo-operator signals or gatekeeper flags.

## Lane + Opening Angle
Lane verdict + one-phrase reason.
Opening angle (Lane 1) or warm-up entry (Lane 2).
Innocent explanation (Lane 1, required).
SMYKM hook with WORK/LIFE/METRIC label.

## Email Thread Log
(empty — filled after sends)
```

## Coherence rules
- Lane 3 forces Tier 4 + Status Disqualified.
- Lane 1 or 2 can never carry Tier 4.
- Status "Dormant" for cold threads that never got a first reply after 4 touches.
- "Lost" reserved for explicit no or exhausted warm sequence.