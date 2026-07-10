# AGENTS.md — Subagent Rules for Hermes Outreach

> **Auto-injected into every subagent spawned in this project.** Keep it focused on rules subagents actually need to execute correctly. Don't duplicate the skills — reference them.

## Non-Negotiable Rules

### 1. Notion page body updates: NEVER delegate
The Email Thread Log format is exact and unforgiving. Subagents don't know it. Any Notion page body write (`mcp__notion__API_update_page_markdown`) must be done by the parent agent directly. Subagents may ONLY:
- Read Notion pages (retrieve_page_markdown, query_data_source)
- Update properties via `mcp__notion__API_patch_page` (fields only — Touch #, Status, Last Contacted, Next Action)
- Return findings/analysis/drafts to the parent

### 2. Email Thread Log format is LAW
Every entry must follow exactly:
```
[YYYY-MM-DD] — Touch #[N] — Subject: "exact subject line" — Sent

[Verbatim body — never summarized, never cleaned up]

Reply: No reply
Next: [YYYY-MM-DD — specific action]
```
No markdown formatting inside bodies. No extra headings. No `---` separators.

### 3. Voice rules are non-optional
Every draft must pass: kill list clean, no em-dashes, proper capitalization, no operator vocabulary, admire-first sequence. See `docs/haythams-voice.md` and `docs/the-drafting-doc.md`.

### 4. Never send email
System stops at Gmail drafts. Never auto-advance Touch #/Status for an unsent email. Reply-detection updates to Notion are the only writes allowed without user approval (they record reality).

### 5. Never invent findings
No verified finding → Lane 2 or 3. A clean funnel is not a failure — it's an intel lead. Machine flags are candidates only.

### 6. Never touch Instagram
No fetching instagram.com. No scraping. No DMs. Sourcing is manual by design.

### 7. Notion is source of truth, not chat memory
Always query the pipeline fresh. Never trust previous-turn state for Touch #, Status, Last Contacted, or Next Action.

### 8. Verbatim bodies or nothing
Never use placeholder text like "[Body content not retrieved from Gmail]". Use Gmail API to get the actual sent body. If you can't retrieve it, flag the lead and move on — don't fabricate.

### 9. Skill creation disclosure (standing rule)
Any time I (the agent) create a new Hermes skill that is outreach-related — touching the lead pipeline, email drafts, funnel audits, Notion CRM, or the cold-outreach workflow — I MUST explicitly flag it to Haytham in the same message where it's created. I will say what the skill does, why I created it, and that it's now available. This covers both skills created at Haytham's direction and skills I create on my own initiative. Non-outreach skills (git, bootstrapping, general-purpose tooling) do not need disclosure unless they become relevant to outreach operations.

## Key File Paths (read each at most ONCE per session, on first need — never per lead)

Do not preload these. Read a doc the first time the session actually needs it; after that it stays in context — do NOT re-read it per lead.

- `docs/haythams-voice.md` — tone, kill list, belief system (before first draft)
- `docs/the-drafting-doc.md` — copywriting rules (before first draft)
- `docs/email-os.md` — mechanics, sequences, cadences (before first draft)
- `docs/smykm-test-layer.md` — subject line rules, niche lingo (before first draft)
- `docs/grand-slam-offer-v2.md` — pricing ($200 Track A / $700 Track B) (only when stating price)
- `docs/pwh-case-study.md` — proof asset (only when citing the proof)

## Pipeline Database
The Lead Pipeline has two IDs — use the right one for the API you're calling:
- **Data source ID** (for Notion MCP `API_query_data_source`): `c6209e29-55ef-4781-b735-73b2a254e34f`
- **Database ID** (for Notion REST API `/v1/databases/{id}/query`): `78b26ebe-5b4f-4ff2-884a-3ccf369d00e6`

## Delegation Boundaries
| Task | Can Delegate? | Notes |
|---|---|---|
| Funnel walk / crawl | ✅ Yes, for parallel batch only | Default: run CLI directly in main session. Delegate only for 3+ concurrent sites. |
| Lane/finding analysis | ✅ Yes | Return verdict + evidence to parent |
| Email drafting | ✅ Yes | Return draft text to parent for gate check |
| Notion page body write | ❌ No | Parent must do directly |
| Email Thread Log append | ❌ No | Parent must do directly |
| Gmail draft creation | ❌ No | Parent must do via himalaya |
| Property updates (Touch #, etc.) | ✅ Yes | Subagent can patch_page properties only |
| Reply detection (Gmail API) | ✅ Yes | Return matched results to parent |