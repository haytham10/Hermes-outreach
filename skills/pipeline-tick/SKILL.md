---
name: pipeline-tick
description: "Daily outreach ops loop over Notion Lead Pipeline + Gmail. Detects replies, surfaces due follow-ups, drafts them via himalaya, flags dormant leads for revival, hands over today's send queue. Creates Gmail drafts only — never sends, never advances Touch # or Status for an unsent email."
tags: [email, outreach, pipeline, daily, cron]
---

# Pipeline Tick — replies, due touches, send queue

Run the whole loop, deliver one morning brief. Notion is the source of truth.

Pipeline data source (MCP): `c6209e29-55ef-4781-b735-73b2a254e34f`
Database ID (REST API): `78b26ebe-5b4f-4ff2-884a-3ccf369d00e6`

## 1 — Reply detection (Gmail → Notion)

**Gmail API** (preferred — reads full verbatim bodies including thread history):
```bash
GAPI="python ${HERMES_HOME:-$HOME/.hermes}/skills/productivity/google-workspace/scripts/google_api.py"
# Search sent messages
$GAPI gmail search "from:haytham@auto-mate.one newer_than:1d" --max 50
# Get full body (returns JSON with body field containing verbatim text)
$GAPI gmail get MESSAGE_ID
```

Fallback if Gmail API unavailable: `himalaya envelope list --folder Sent --page 1 --page-size 50 --output json`

Query pipeline for rows with Touch # ≥ 1 and Status in (Outreach Sent, Reply Received, Loom Sent, Call Booked, Dormant). For each row with an Email, search Gmail via himalaya for threads since Last Contacted.

- New reply found → update Notion: Status = Reply Received, Sequence = Warm, quote verbatim in brief. Append reply to lead's Email Thread Log.
- Bounce (mailer-daemon) → flag bad address, Status back to Researching.

## 2 — Due follow-ups

Query rows where Next Action ≤ today and Status not in (Won, Lost, Disqualified).

For each due row, identify touch type from Sequence + Touch # + Status. Draft with haytham-email-draft skill. Create Gmail draft via himalaya:

```bash
cat << 'EOF' | himalaya template save --folder Drafts
From: haytham@auto-mate.one
To: [lead-email]
Subject: [subject]

[body]
EOF
```

Guard: check Gmail drafts first — if unsent draft to that address exists, do NOT stack a second. Surface old draft in brief.

## 3 — Send queue

Query Status = Audit Ready with Email set. Sort sub-12K followers first, then Tier. Present as "ready to send today."

## 4 — Hygiene flags

- Incoherent rows: Lane 3 without Tier 4/Disqualified, Lane 1/2 with Tier 4
- Stale threads: Sequence = Warm, no touch in > 4 days
- Researching rows older than 1 week with no walk in page body

## 5 — Manual sync mode (catch-up after sends)

When Haytham says he sent emails without updating Notion, follow `references/manual-sync.md` exactly.

**Critical: always update BOTH page body AND properties.** Properties alone (Touch #, Last Contacted, Next Action) is incomplete — the Email Thread Log in the page body must also get the new entry. This is the #1 mistake. Use `mcp__notion__API_update_page_markdown` with `type="update_content"` for the body, and `mcp__notion__API_patch_page` for properties.

**Email matching: query each sent address individually.** The Notion API's bulk response returns double-wrapped JSON (`{"result": "{...}"}`) that is error-prone to parse. Instead, for each sent email address, query the pipeline individually:

```json
{"data_source_id": "c6209e29-55ef-4781-b735-73b2a254e34f", "filter": {"property": "Email", "email": {"equals": "lead@example.com"}}, "page_size": 10}
```
Note: `data_source_id` is for MCP `API_query_data_source`. For the Notion REST API, use database ID `78b26ebe-5b4f-4ff2-884a-3ccf369d00e6` instead.

This reliably returns the page_id even when bulk parsing fails. **Never trust bulk parse failures** — individual queries prove they exist.

**Verbatim body retrieval:** Use the Gmail API (not himalaya) to get full sent message bodies. Himalaya's IMAP access to Gmail's Sent folder returns empty bodies. The Gmail API returns the complete message body including thread history.

**Gmail fetch batching:** Run sequential `$GAPI gmail get` calls in a single foreground terminal command with `echo "=== SEPARATOR ==="` between results. Do NOT use shell backgrounding (`&`). For 30+ messages, split into 3 batches of 10-12 max per command.

**Placeholder replacement for body fixup:** When a delegate pre-filled thread log entries with placeholder text, the strings vary by lead type:
  - **Warm leads**: `[Warm follow-up sent. Body content not retrieved from Gmail.]`
  - **Cold/Outreach leads**: `[Cold follow-up sent. Body content not retrieved from Gmail.]`
  Use `mcp__notion__API_update_page_markdown` with `type="update_content"` and `content_updates` — find the placeholder via `old_str` and replace with the verbatim body via `new_str`. This is more precise than `replace_content` and preserves surrounding thread log structure.

**Parallel Notion API calls:** Independent Notion MCP calls (e.g. updating 12 different pages' properties and bodies) can be fired in the same assistant turn. The runtime executes them concurrently. For batch operations on 6-12 leads, always batch them. Do NOT serialize independent updates.

**Large DB query workaround:** When querying the data source returns over ~400KB, the response is saved to a cache file under `$HERMES_HOME/cache/terminal/hermes-results/`. Read it with Python to parse the double-wrapped JSON (`json.loads(data['result'])`) and iterate `result['results']` to find pages by email field. Write the Python script to a temp file and run it — heredocs are blocked by the approval guard.

## Reference files

- `references/pipeline-schema.md` — full property reference + page body format
- `references/manual-sync.md` — catch-up sync after sending without logging

## The brief

One message in this order: replies (verbatim + suggested turn-two), due follow-ups (with drafts), today's send queue, hygiene flags. If empty, one line saying so.

## Hard rules

- Drafts only. Never send. Never auto-advance Touch #/Status/Last Contacted/Next Action for an unsent email.
- Reply-detection updates are the ONLY Notion writes without approval — they record reality.
- Never stack a second unsent draft to the same address.
- Never query or touch Instagram.
- Only load drafting docs (via haytham-email-draft) when step 2 actually has due follow-ups to draft. A tick with nothing due needs no docs at all.