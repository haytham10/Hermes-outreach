# Manual Sync — Gmail Sent → Notion Pipeline

Use this when Haytham says he sent emails but didn't update the pipeline. This is the manual catch-up mode of pipeline-tick.

## Approach

1. **Fetch today's sent emails** from Gmail via Gmail API (preferred — returns full verbatim bodies):
   ```bash
   GAPI="python ${HERMES_HOME:-$HOME/.hermes}/skills/productivity/google-workspace/scripts/google_api.py"
   $GAPI gmail search "from:haytham@auto-mate.one newer_than:1d" --max 50
   ```
   Fallback: `himalaya envelope list --folder Sent --page 1 --page-size 50 --output json`

2. **Get full verbatim body for each sent message** — ALWAYS do this. Any message, get the body:
   ```bash
   $GAPI gmail get MESSAGE_ID
   ```
   The JSON response has a `body` field with the complete message text including thread history.

3. **Match each sent email to a Notion lead individually.** Do NOT rely on bulk queries — the Notion MCP returns double-wrapped JSON that is error-prone to parse. Instead, query each email address individually:
   ```
   mcp__notion__API_query_data_source with:
     data_source_id = "c6209e29-55ef-4781-b735-73b2a254e34f"
     # ^ MCP data_source_id — for REST API use database ID 78b26ebe-5b4f-4ff2-884a-3ccf369d00e6
     filter = {"property": "Email", "email": {"equals": "lead@example.com"}}
   ```
   This reliably returns the page_id even when bulk parsing fails.

4. **For each matched lead, update BOTH:**
   - **Page body** — append to Email Thread Log section using `mcp__notion__API_update_page_markdown` with `type="update_content"`
   - **Properties** — Touch # (+1), Last Contacted = today, Next Action = today + cadence using `mcp__notion__API_patch_page`

5. **Report unmatched sends.** List emails sent to addresses not found in the pipeline.

## Thread log entry format

Each entry uses the full verbatim body from the Gmail API:

```
[YYYY-MM-DD] — Touch #[N] — Subject: "exact subject line" — Sent

[VERBATIM BODY FROM GMAIL API - INCLUDES FULL THREAD HISTORY]

Reply: No reply yet
Next: YYYY-MM-DD
```

## Critical rules (earned from real errors)

- **BOTH page body AND properties must be updated.** Properties alone (Touch #, Last Contacted, Next Action) is incomplete. The Email Thread Log is where the actual email record lives. This is the #1 mistake.
- **Query each email individually.** Bulk pipeline queries fail to match reliably because the Notion MCP double-wraps its JSON. Individual queries by email always find the page if it exists.
- **Use Gmail API for verbatim bodies, not himalaya.** Himalaya's IMAP access to Gmail's Sent folder returns empty bodies for sent messages. The Gmail API returns full bodies including thread history. I found this out the hard way — don't repeat it.
- **"Body content not retrieved from Gmail" is never acceptable.** If a lead got an email, the verbatim text is in the Gmail API. Get it.
- **Email typo guard:** Check for slight mismatches (e.g. `brightbegginings` vs `brightbeginnings`). Query the Notion DB if nothing matches.