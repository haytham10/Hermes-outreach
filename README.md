# Outreach Operations — Hermes Foundation

Your cold email outreach system running on Hermes Agent.

## Directory Structure

```
~/projects/hermes-outreach/
├── AGENTS.md                       # Subagent rules (auto-injected — keeps quality consistent)
├── docs/                           # Cached framework docs (canonical, no Notion fetch needed)
│   ├── the-bible.md                # Methodology playbook
│   ├── email-os.md                 # Cold email mechanics
│   ├── smykm-test-layer.md         # Subject line + research rules
│   ├── the-drafting-doc.md         # Copywriting rules (Harry Dry)
│   ├── haythams-voice.md           # Tone / belief system (FULL version — synced with skill)
│   ├── grand-slam-offer-v2.md      # Two-track pricing ($200 / $700)
│   └── pwh-case-study.md           # Proof asset (Dr. Hanaa)
│
├── cached-evidences/               # Crawler output (per lead)
├── scripts/                        # Helper scripts

~/projects/Funnel-Auditor/          # Crawler repo
├── main.py                         # CLI: walk / crawl
├── audit/                          # Crawler + checks
├── config.py                       # Funnel keywords, noise domains
├── .claude/skills/                 # Original Claude skills (reference only)
└── CLAUDE.md                       # System overview
```

## Tools

| Tool | Status | Usage |
|---|---|---|
| **Notion MCP** | ✅ Live | CRM + lead management |
| **Himalaya CLI** | ✅ Live | Gmail drafts (`template save --folder Drafts`) |
| **Funnel Auditor** | ✅ Installed | `python main.py walk <url>` |
| **Playwright** | ✅ Installed | Chromium browser for crawling |
| **Gmail API** | ✅ Live | Reply detection + verbatim body retrieval |

## Skills (all created ✅)

| Skill | Purpose | Delegation-safe? |
|---|---|---|
| **pipeline-tick** | Daily ops: reply detection, due follow-ups, send queue, hygiene, manual sync | Partial — body writes are parent-only |
| **haytham-email-draft** | Voice + silent gate loop + all email types + Gmail drafts | Partial — draft text can be delegated, final gate + himalaya is parent-only |
| **funnel-audit-session** | Single-lead: intake → walk → findings → opener → draft | Partial — crawling/analysis OK, Notion writes + Gmail drafts are parent-only |
| **cold-outreach-pipeline** | Architecture overview + session start workflow | N/A — reference skill |

## Cron Jobs

| Job | Schedule | Purpose |
|---|---|---|
| **Daily Pipeline Tick** | Every morning | Reply detection, due follow-ups, send queue, hygiene flags |
| **Audit Queue Worker** | TBD | Process Researching leads through funnel-audit-session |

## Delegation Rules (see AGENTS.md for full table)

Core principle: subagents can research, crawl, analyze, and draft text — but the parent always does the final gate check, Notion page body writes, Email Thread Log appends, and Gmail draft creation.

✅ **Can delegate**: funnel walking, lane/finding analysis, email drafting (return text), property-only Notion updates, Gmail reply detection
❌ **Never delegate**: Notion page body writes, Email Thread Log appends, Gmail draft creation, final voice gate checks

## Local Docs Cache

All 7 framework docs at `~/projects/hermes-outreach/docs/` are the canonical working copies. Skills reference these instead of fetching from Notion. The `haythams-voice.md` is the full authoritative version (includes kill list, operator vocabulary ban, quote rule, polish rule, two tests); the email skill's `references/voice-rules.md` is just a pointer to it, not a second copy.

Loading policy: each doc is read at most once per session, on first need — the four core drafting docs before the first draft, the-bible before the first funnel walk, offer/case-study only when a draft states price or cites the proof. Sessions that never draft load nothing.

## Efficiency configuration (do not undo casually)

Set in Hermes `config.yaml` (AppData/Local/hermes) on 2026-07-10:
- `mcp_servers.notion.tools.include` whitelists the 8 Notion endpoints the pipeline uses (the full server ships 24; the other 16 cost ~50KB of schema on every request). If a Notion call is missing, extend the list.
- `platform_toolsets.cli` / `.cron` trim built-in tools (no cronjob/code_execution/image_gen/tts tool schemas). Re-enable via `hermes tools`.
- `skills.disabled` hides ~66 bundled skills irrelevant to outreach from the per-request skills index. Re-enable via `hermes skills`.
- `model.max_tokens: 8192` caps output (unset = 65,536 reserved per request, which 402s at low OpenRouter balances).
- `tool_loop_guardrails.hard_stop_enabled: true` stops repeated identical tool failures from burning full-context retries.

## Quick Start

1. **Morning check**: Run pipeline-tick (manual or via cron) — "pipeline tick"
2. **Process a lead**: "process this lead: [name], [handle], [url], [followers]" → funnel-audit-session
3. **Batch audit**: "batch audit" → pipeline-tick audit queue mode
4. **Draft an email**: haytham-email-draft handles it automatically when you ask for a draft
5. **Catch-up after sending**: "sync sent emails" → pipeline-tick manual sync mode

> **Claude Code users**: If using Claude Code with this repo, it needs Bash+Read permissions to access `$HERMES_CONFIG/.env` and list/find skills under `$HERMES_CONFIG/skills/`. Those permissions live in `.claude/settings.local.json` (gitignored — template the file on clone).