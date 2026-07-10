---
name: cold-outreach-pipeline
description: "Manage a cold email outreach pipeline end-to-end: Notion CRM, funnel auditing, email drafting via Himalaya, follow-up sequencing, and scheduled workers. Built for parenting/faith-based coach outreach but the architecture is portable."
version: 2.0.0
author: user
metadata:
  hermes:
    tags: [outreach, cold-email, notion, himalaya, pipeline, crm, sales]
    related_skills: [notion, himalaya, google-workspace, pipeline-tick, haytham-email-draft]
---

# Cold Outreach Pipeline

End-to-end pipeline management for cold email outreach. Notion is the single source of truth for CRM, audit history, email threads, and scheduling. Emails are drafted via Himalaya and sent manually by the user — no automated sending.

## Tech Stack

- **CRM/state**: Notion (Lead Pipeline database, page bodies for audit logs and email threads)
- **Email drafts**: Himalaya CLI → `template save --folder Drafts`
- **Funnel crawling**: browser tools (browser_navigate, browser_snapshot, browser_console) or Funnel Auditor repo (`~/projects/Funnel-Auditor`)
- **Orchestration**: Hermes Agent (skills + cron jobs for scheduled workers)

## Skills Map (which skill owns what)

| Task | Skill | When |
|---|---|---|
| Daily ops: replies, follow-ups, send queue, hygiene | **pipeline-tick** | Every morning (cron or manual) |
| Email drafting (all types) | **haytham-email-draft** | Whenever a draft is needed |
| Single-lead audit: walk → findings → opener → draft | **funnel-audit-session** | Per-lead processing |
| Batch audit: process all Researching leads | **pipeline-tick** (or funnel-audit-session loop) | After sourcing sessions |

## Notion Workspace — Reliable Docs

These are the only current framework docs. **Never fetch them from Notion** — the canonical copies are cached locally (see below); the Notion IDs are kept only for provenance. Skip everything else — the workspace has stale docs.

| Doc | Notion ID | Purpose | Status |
|---|---|---|---|
| The Bible | `383382c8-4585-81ce-9f60-ecf42658b0ae` | Methodology, funnel walk, rules, lanes, artifact engine | **Load — some sections stale** |
| Email OS | `387382c8-4585-81ba-91e1-e4bde838a339` | Cold email mechanics, finding, writing, follow-ups, tracking | **Load** |
| SMYKM Test Layer | `389382c8-4585-8174-a5b4-d2b0194dcfc1` | Subject line rules, 48h bump, human-first research | **Load** |
| The Drafting Doc | `389382c8-4585-811d-8782-fa23ffd2e5ee` | Harry Dry copywriting: concrete, falsifiable, bespoke | **Load** |
| Haytham's Voice | `389382c8-4585-8130-85ec-ef54bb73813a` | Tone, belief system, kill list | **Load** |
| Grand Slam Offer v2 | `391382c8-4585-817a-8307-c9e91dbf01b8` | Current offer: two tracks, risk reversal, bonus stack | **Load** |
| PWH Case Study | `35a382c8-4585-8142-8e72-f12124daa0fc` | Proof asset: $8,123 launch, 4x 5-star reviews | **Load** |

**Cached locally at `~/projects/hermes-outreach/docs/`** — skills reference these instead of fetching from Notion every time. The 7 local markdown files are the canonical working copies.

**Skip these — outdated:** Prompt Starter, Launch Support Framework, The Offer (old, superseded by Grand Slam Offer v2), Sourced Leads, all old offer-related docs.

### Lead Pipeline Database

Database ID: `78b26ebe-5b4f-4ff2-884a-3ccf369d00e6`
Data source ID: `c6209e29-55ef-4781-b735-73b2a254e34f`

**WARNING:** These are different IDs. The data source ID (`collection://c6209e29-...`) is used by the Notion MCP `API_query_data_source` tool. The database ID (`78b26ebe-...`) is what the Notion REST API v1 expects for `/v1/databases/{id}/query`. If the MCP tools aren't available in-session (e.g. MCP naming mismatch, session not reloaded after config change), use the database ID with the direct REST API. To discover the real DB ID, search Notion: `POST /v1/search {filter: {value: "database", property: "object"}}` — the `Lead Pipeline` title gives the canonical database ID.

Key fields: Status, Tier, Lane, Sequence, Touch #, Next Action, Last Contacted, Email, Finding Type, Niche, Platform, Est. Value, Lost Reason.

Full schema: see `pipeline-tick` skill → `references/pipeline-schema.md`.

## Session Start

Every new session where you're doing outreach work:

1. Query the Lead Pipeline for leads with Next Action ≤ today (WHERE Status != Won/Lost/Disqualified, sort by Next Action ascending)
2. Query for any leads still in Status = Researching (audit queue backlog)

Do NOT preload the cached docs. Each doc in `~/projects/hermes-outreach/docs/` is read at most once per session, at the moment it's first needed: the four core drafting docs before the first draft, the-bible before the first funnel walk, offer/case-study only if the email states price or cites the proof. A session that never drafts never loads them. Never re-read a doc already in context.

Never treat chat memory as pipeline state — always read Notion.

## The Three Workflows

### 1. Audit Workflow — Single Lead (manual trigger)

Use the **funnel-audit-session** skill. Quick reference:

1. Fetch the lead page from Notion
2. Crawl their website using browser tools or `python ~/projects/Funnel-Auditor/main.py walk <url>`
3. Run the 5-stop funnel walk (from The Bible): bio link → freebie → offer/sales page → checkout → audience ownership
4. Apply the two filters: sting test and vitamin filter
5. Determine Lane (1/2/3) and Finding Type
6. Write the full audit into the lead's Notion page body
7. Update lead properties: Status → Audit Ready, Lane → verdict, etc.
8. If Lane 1: generate a personalized opener email using **haytham-email-draft** skill
9. Create Gmail draft via Himalaya
10. Update properties after user confirms send

### 2. Audit Queue Worker (daily cron)

Set up as a cron job using the **pipeline-tick** skill. Scans for leads still in Researching and processes them — same as workflow 1 but unmanned.

### 3. Daily Pipeline Tick (cron or manual)

Use the **pipeline-tick** skill. The full morning loop:

1. Reply detection (Gmail API → Notion)
2. Due follow-ups with drafts
3. Today's send queue
4. Hygiene flags

## Gmail Drafts via Himalaya

Quick usage:

```bash
cat << 'EOF' | himalaya template save --folder Drafts
From: haytham@auto-mate.one
To: prospect@example.com
Subject: your [specific thing]

[Email body — plain text, sentence case, Haytham voice]
EOF
```

Requires `folder.aliases.drafts = "[Gmail]/Drafts"` in `~/.config/himalaya/config.toml`.

## Voice & Tone — Quick Reference

From Haytham's Voice (the full doc is at `docs/haythams-voice.md` -- read once before the first draft of a session, never re-read per lead):

- Write to a stranger like someone who already knows you're a good person
- Admire first, find the gap reluctantly, help before sell
- Peer, never above or below: "from one business owner to another"
- Lowercase by default, sentence case, "I" capitalized
- Short lines, one idea then stop
- No soft exits: kill "no pressure", "no worries if not", "just checking in"
- Kill list: "stuck with me", "love that energy", "I noticed...", "love what you're doing", "quick question"
- No em-dashes. Anywhere. Ever.
- No operator vocabulary: "funnel", "sequence", "opt-in", "conversion", "audit"

## Offer Reference

From Grand Slam Offer v2:

- **Track A — 48-Hour Rescue**: $200 flat, micro coaches. Fix + capture + bonus walkthrough. Pay-after option. Guarantee: if anything isn't working, keep the work free.
- **Track B — Launch-Ready in 5 Days**: $700, roster operators. Order bump guarantee pays for project within 30 days. Bonuses instead of discounts.
- Core rule: price never drops. Bonuses answer stalls. Terms restructure for term objections.

## Subagent Delegation Rules

See `AGENTS.md` at the project root for the full delegation boundaries table. Quick summary:

- ✅ **Can delegate**: funnel walking, lane/finding analysis, email drafting (return text to parent), property-only Notion updates, Gmail reply detection
- ❌ **Never delegate**: Notion page body writes, Email Thread Log appends, Gmail draft creation (himalaya), final gate checks on drafts

**Important change from v1:** Funnel walks now default to running the CLI directly in the main session (not delegated to a subagent). Only delegate for parallel batch work (3+ sites at once). See funnel-audit-session skill for details.

## Pitfalls

### From pipeline-tick (real errors — don't repeat)
- **Gmail body retrieval**: Himalaya's IMAP access to Gmail Sent folder returns empty bodies. Use Gmail API (`google-workspace` skill scripts) for verbatim sent message bodies.
- **Notion MCP double-wrapped JSON**: Bulk pipeline queries return double-wrapped JSON that's error-prone to parse. Query each email address individually instead.
- **Placeholder text is never acceptable**: "[Body content not retrieved from Gmail]" is banned. Get the verbatim body or flag the lead and move on.
- **Both body AND properties must be updated**: After a send, the Email Thread Log in the page body AND the property fields (Touch #, Last Contacted, Next Action) must be updated. Properties alone is the #1 mistake.
- **Never stack unsent drafts**: Check Gmail drafts before creating a new one. Two unsent drafts to the same address is noise.

### Funnel Auditor CLI
- **Windows: greenlet._greenlet ModuleNotFoundError**: The Funnel Auditor CLI (`python main.py walk ...`) imports playwright which depends on the `greenlet` C extension. On Windows with mixed Python installs (e.g. Python3.11 system-wide but Hermes venv Python3.13), the greenlet binary loads from the wrong venv and crashes. Default to browser-tool fallback immediately — do not debug greenlet versions mid-session.

### Notion
- **MCP tool naming mismatch**: The Notion MCP server exposes tools with hyphens (`API-query-data-source`), but the default config may have underscores (`API_query_data_source`). If a session loads and MCP tools don't appear as available, check `config.yaml` `mcp_servers.notion.tools.include` — tool names must use hyphens. Fix with `hermes mcp configure notion` (interactive) or edit the config. Requires `/reload-mcp` or a new session to take effect.
- **Database ID ≠ data source ID**: The data source ID (`c6209e29-...`) is a `collection://` identifier used by `API_query_data_source`. The actual database ID on the Notion REST API is `78b26ebe-...`. When working outside MCP (direct REST calls), always use the database ID. Discover via `POST /v1/search` filtered to databases.
- **Direct REST API reference**: See `references/direct-notion-rest-api.md` for complete recipes (query, read/append blocks, patch properties) when MCP tools are unavailable. **PITFALL:** `PATCH /v1/pages/{id}/markdown` is MCP-only — calling it against the native Notion REST API returns `400: body.type should be defined`. Use the block-level API for body writes when MCP is not in-session.

### General
- **Don't load outdated Notion docs**: Prompt Starter, Launch Support Framework, old "The Offer" page, Sourced Leads are stale.
- **Don't trust chat memory for pipeline state**: Always fetch from Notion.
- **Don't send without human review**: Drafts go to Gmail Drafts folder only.
- **Himalaya folder aliases**: Without correct `folder.aliases.drafts` mapping, `template save --folder Drafts` will fail silently.
- **July seasonality**: Parenting coach niche — kids home from school, inboxes ignored, launches postponed. Slow weeks are calendar-driven, not a verdict on copy or motion.
- **Email typo guard**: Check for slight mismatches (e.g. `brightbegginings` vs `brightbeginnings`) when matching sent emails to pipeline leads.