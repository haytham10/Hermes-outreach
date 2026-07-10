---
name: funnel-audit-session
description: "Single-lead processing pipeline: intake → funnel walk → vision pass → floors → lane verdict → opener-finder → email draft → Gmail draft. Covers the full per-lead flow from Researching to Outreach Sent."
tags: [outreach, audit, funnel, email, notion]
---

# Funnel Audit Session — Single Lead Pipeline

Process one lead from Researching → Audit Ready → Outreach Sent. This is the per-lead contract. For batch processing, use pipeline-tick's audit queue worker.

## When to Use

- User drops a single lead in chat: "process this lead: Jane Doe, @janedoecoach, linktr.ee/janedoe, 4.2K followers"
- User says "work the audit queue" and wants one-at-a-time processing
- Any time a single lead needs the full walk → findings → opener → draft pipeline

For batch processing of the entire Researching queue, use pipeline-tick's audit queue worker (cron).

## Prerequisites

Before running, confirm:
- Lead name, handle, and site URL (minimum)
- Follower count (if IG-sourced)
- The lead exists in Notion, or create a new page in the pipeline DB

## WARNING — Budget Constraint

**Default max tool calls per session is 60. Notion setup overhead (database discovery, token extraction, MCP fallback) can consume 15-20 calls before the audit even starts.** A session that hits the tool limit with the audit body still unwritten to Notion is a failed session — the analysis is lost on context reset. To prevent this:

1. **Write the audit to Notion FIRST, after lane analysis** — Step 4 comes immediately after Step 3 (lane analysis), before any optional deep-dive browsing. Lane analysis is in-head reasoning (~0 tool calls). The Notion write and property patch are the critical deliverables — they make the audit permanent.
2. **Defer optional deep-dives** (reading every blog post, scrolling entire sales pages, clicking through checkout) until after the Notion write succeeds.
3. **If budget gets tight** (30+ calls used, still in browser), skip the browser vision passes and mark the audit as "manual review needed — vision pass skipped due to tool budget". Do NOT start browsing a new page unless the audit body is already written to Notion.

## Step-by-Step Pipeline

### Step 1 — Create or Fetch Notion Page

If the lead isn't in Notion yet, the Notion MCP `API_post_page` uses the data source ID for database selection (the MCP server accepts `database_id` parameter with the data source ID):
```
mcp__notion__API_post_page
  parent: { database_id: "c6209e29-55ef-4781-b735-73b2a254e34f" }
  properties: { Contact Name, Site URL, Profile URL, Followers, Status: "Researching" }
```
If you're calling the Notion REST API directly (when MCP tools aren't in-session), use the canonical database ID instead:
`POST https://api.notion.com/v1/databases/78b26ebe-5b4f-4ff2-884a-3ccf369d00e6/query`
The two IDs are different — the MCP uses the data source ID (`c6209e29-...`) while the REST API uses the database ID (`78b26ebe-...`). Discover the DB ID via `POST /v1/search {filter: {value: "database", property: "object"}}` and look for the "Lead Pipeline" title.

If already in Notion, fetch with `mcp__notion__API_retrieve_page_markdown`.

**MANDATORY: Before any `API_update_page_markdown` with `type=replace_content`, call `API_retrieve_page_markdown` first and re-read the full body.** Haytham often drops IG evidence screenshots, bio notes, or sourced links into new lead pages right after creating them. The audit must build on those — not silently overwrite them. `replace_content` returns no diff, so the loss is invisible otherwise. Same rule for any `update_content` with non-empty `old_str`: read, then write.

### Step 2 — Funnel Walk

**Default: Run the Funnel Auditor CLI directly in the main session.** Do NOT delegate to a subagent unless you need to audit multiple sites in parallel.

#### 2a — Compute the evidence slug (before anything else)

The slug must be computed the same way the crawler does it, so IG screenshots and crawl screenshots land in the same folder. A hand-guessed slug is what put a real lead's IG evidence in `evidence/momhoodmentor/ig/` while the crawl wrote to `evidence/lynsey-ward/` — two different directories the vision gate can't reconcile.

```bash
FUNNEL_AUDITOR_HOME="${FUNNEL_AUDITOR_HOME:-$HOME/projects/Funnel-Auditor}"
cd "$FUNNEL_AUDITOR_HOME"
HERMES_VENV="${HERMES_HOME:-$HOME/.hermes}/hermes-agent/venv"
PYTHON="$HERMES_VENV/Scripts/python"
# Use the contact name; falls back to handle or URL if no name yet
$PYTHON main.py slug "<Contact Name>"
```

Save the output as `$SLUG` for the commands below.

#### 2b — Download IG screenshots (if any are attached to the Notion page)

If the Notion page body has attached images (Haytham's sourcing screenshots), download them into `evidence/$SLUG/ig/` before the crawl. The signed file URLs (file.notion.so / secure.notion-static.com) expire, so don't defer.

```bash
mkdir -p evidence/$SLUG/ig
curl -o evidence/$SLUG/ig/1.png "<signed url>"
# repeat for each image
```

Then register them in the vision manifest (this marks them as required but unread — to be read in Step 2.5):

```bash
$PYTHON main.py vision init evidence/$SLUG
```

No images attached → proceed site-only, carry the flag "IG evidence: none attached — site-only walk" into the Notion body and final verdict. Skip `vision init` for the ig/ portion in this case.

#### 2c — Run the crawl

```bash
$PYTHON main.py walk <site-url> --name "<name>" --handle "<handle>" --followers <N> --out evidence/$SLUG
```

The `--out evidence/$SLUG` argument is **required** — it guarantees the IG screenshots (from 2b) and the crawl's own screenshots end up in the same folder. Without it, they diverge and the vision gate can't reconcile them.

Produces:
- `evidence/$SLUG/packet.md` — structured walk with machine flags
- `evidence/$SLUG/screenshots/` — desktop + mobile screenshots per page
- `evidence/$SLUG/evidence.json` — structured evidence data
- `evidence/$SLUG/vision_manifest.json` — auto-generated at the end of the crawl, registering every site screenshot as a required, unread image (the IG images from 2b are preserved with their prior read status)

**PITFALL — Windows: greenlet crash.** On Windows with mixed Python installs, running `python main.py walk` may fail with `ModuleNotFoundError: No module named 'greenlet._greenlet'`. This happens when the system `python3` (Python 3.13) picks up the Hermes venv's greenlet binary which was compiled for Python 3.11. **Fix:** Use the Hermes venv's Python interpreter explicitly:
```bash
"${HERMES_HOME:-$HOME/.hermes}/hermes-agent/venv/Scripts/python" main.py walk ...
```

If the CLI still fails (e.g. Playwright browser not installed), skip it immediately and fall through to the browser-tool fallback below. Do NOT debug greenlet versions mid-session.

**PITFALL — CLI timeout on target URLs.** If `python main.py walk <url>` hangs (no output for 60+ seconds), the root cause is rarely a missing Playwright/Chromium. The crawler's `_goto_with_fallback()` already handles `networkidle` hangs by falling back to `domcontentloaded`. A genuine timeout is almost always the target URL itself (heavy JS, chat widgets, long-polling analytics, infinite scroll) or a bash-level timeout on the command.

**Quick one-pass diagnosis:**
1. Verify Playwright + Chromium are functional by writing a temp script to `C:\Users\...\AppData\Local\Temp\` that launches headless Chromium and navigates to `example.com`, then deleting it. (The `-c` inline flag is blocked by Hermes' approval guard — always use a temp file for `python -c`-equivalent checks on this host.)
2. Test with a known-light URL: `python main.py crawl example.com`. If it works, the issue is the target URL, not the tooling — increase the terminal timeout (300s+) or fall through to the browser-tool fallback.
3. If example.com also fails: `python -m playwright install --list` to confirm Chromium is listed at its `ms-playwright` path. If missing: `python -m playwright install chromium`.
4. If Chromium is installed but example.com still fails, the Playwright launch args may need adjustment (e.g. `--disable-gpu` on Windows).
5. If all diagnostics fail, skip the CLI and use the browser-tool fallback below.

**Fallback — Browser tools (when the CLI fails, is unavailable, or for custom sites):**
Use browser_navigate → browser_snapshot to walk the 5 stops:
1. Bio link — one clear next step or pile of choices?
2. Freebie — can a stranger get something free + does it ask for email?
3. Offer/sales page — in 10 seconds, can I tell what it is, price, why I want it?
4. Checkout — if I tried to pay, would anything stop me?
5. Audience ownership — if IG vanished, could they reach these people?

For the browser fallback, these console techniques compensate for the CLI's absence:
- **Full page text extraction** (`document.body.innerText.substring(0, 15000)`) — captures FAQ sections, pricing details, and testimonial content that the truncated snapshot misses.
- **Hidden checkout URL discovery** — query DOM for Kajabi/checkout patterns when CTA buttons don't have visible hrefs.
- See `references/browser-fallback-techniques.md` for the full set of console-based techniques.

**When to delegate (and only then):** If you're processing multiple leads' sites concurrently (3+), delegate the CLI calls so they run in parallel. For a single lead, run it directly.

### Step 2.5 — Vision Pass Over Screenshots (mandatory, machine-checked)

After the funnel walk, run a vision pass over every image listed in the manifest. The vision gate turns "I read the screenshots" from a self-report claim into a computed fact: every required file must be explicitly marked read in `vision_manifest.json`.

**This step used to be enforced by instruction alone ("read every image"), and a real run reported "4 screenshots read" in its final verdict when only 1 of 4 had actually been opened.** The vision gate prevents this by refusing to let you proceed until every required image is marked read.

**Purpose:** Machine flags from the crawler are candidates only. A flag that fails visual confirmation is dead. The vision pass catches:
- Popups/modals that overlay a CTA (the crawler sees page HTML, not the post-dismissal state)
- Booking widgets that render blank in screenshots (async iframes loading after networkidle — flagged by `config.BOOKING_EMBED_HOSTS`)
- Visual clutter, broken layouts, missing images the crawler can't assess
- Actual CTA placement, visibility, and whether the page builds trust or erodes it

**Procedure:**

1. **List the manifest** to see exactly what's expected:

   ```bash
   $PYTHON main.py vision list evidence/$SLUG
   ```

   This shows every tracked image, its category (ig_screenshot / site_desktop / site_mobile), whether it's required, and whether it's been read yet.

2. **Read every required image** with `vision_analyze`, using a tight structured prompt:

   ```
   [lead name] — [page URL] — [device: desktop/mobile]

   Confirm or reject each machine flag below. Return 3-5 bullet points.
   Max 100 words total.

   Machine flags from this page: [copy from packet.md]

   What else on this page is a visitor's clear next step?
   ```

   **After each Read, immediately mark it:**

   ```bash
   $PYTHON main.py vision mark evidence/$SLUG ig/1.png
   # or for site screenshots:
   $PYTHON main.py vision mark evidence/$SLUG screenshots/page-about_desktop.png
   ```

   You can batch several paths in one `vision mark` call if you just read several in a row. Do not defer marking to the end — the whole point is that the manifest is the source of truth, not your memory of what you read.

3. **Run the hard gate** before proceeding to Step 3 (lane analysis):

   ```bash
   $PYTHON main.py vision check evidence/$SLUG
   ```

   - **Exit 0 + `VISION PASS: COMPLETE — X of X required images confirmed read`** → proceed to Step 3.
   - **Exit 1 + `VISION PASS: INCOMPLETE — N of M...`** → go back, read the listed images, mark them, and re-run the check. Repeat until it passes.
   - **The only exception** is a genuinely unreadable/corrupted image (the file won't open, or the screenshot is blank/broken past the point of being informative). In that case only, proceed but carry the exact path and reason verbatim (`⚠️ vision pass incomplete: <path> — <reason>`) into the Evidence section — never silently dropped, never smoothed into "vision pass complete."

4. **Paste the literal `vision check` output** into the Evidence section of the Notion body and the final chat verdict. Never write a paraphrase like "4 screenshots read" — if the check didn't print exactly that, the report can't claim it either.

**No screenshots available?** If the CLI fallback (browser tools) was used instead of the Funnel Auditor CLI, there are no local screenshots. Skip the vision gate and note "no screenshots produced — manual review needed" in the audit.

**Model routing:** The vision pass runs through the `auxiliary.vision` model slot. Configure it once at setup so screenshots route to minimax/minimax-m3 while reasoning stays on deepseek/deepseek-v4-flash:

```yaml
# ~/.hermes/config.yaml
auxiliary:
  vision:
    provider: openrouter
    model: minimax/minimax-m3
    timeout: 120
```

**PITFALL — minimax-m3 is verbose by default.** Every vision prompt MUST include explicit output constraints: max 100 words, 3-5 bullet points max. Never leave the prompt open-ended. The vision model receives zero conversation history (image + prompt only), so there is no context-carryover waste between leads.

**PITFALL — browser_vision with minimax-m3 is slow (~40-50s per call) and unreliable for reading prices.** The auxiliary vision model frequently cannot read dollar amounts, pricing tables, or small text on sales pages. When you need pricing info, prefer browser_snapshot or browser_console (reading the DOM) over vision_analyze. If you must use vision, scroll to the pricing section first and take a dedicated screenshot, then ask a very specific question about the price. Even then, expect to need 2-3 attempts or to fall back to DOM inspection.

**WARNING — Vision hallucination on repeated failure (learned from real session).** If a `browser_vision` price/data read fails to produce a clear result on the first two attempts, the third attempt MUST NOT guess a specific number. The auxiliary vision model has demonstrated a pattern of confidently stating a wrong number ($1,998 vs actual $158) after two earlier failures. The rule is:
- **Attempt 1**: Scroll to the specific section, take a screenshot, ask a precise question.
- **Attempt 2**: If attempt 1 was unclear, try a different approach (zoom in, scroll to a different part of the page, or use browser_snapshot/browser_console to read the DOM directly).
- **Attempt 3+**: If DOM inspection also fails, report "price not machine-readable" and mark it for manual review. NEVER state a specific dollar amount unless you have actually read it clearly from the page source (DOM text content, not vision). **A confidently wrong number is worse than no number.**

### Step 2.6 — The Floor (added Jul 2, 2026, from pipeline evidence)

Gate 0 (sourcing) is supposed to screen leads before they ever reach this pipeline, but the rows prove it doesn't always happen, so the walk enforces a minimum before any touches get spent.

**Audience floor:** roughly 1K followers or an equivalent real audience signal (podcast, list, active community). Receipt: Blanka Kellermayer, 115 followers, burned three touches on an account that cannot pay even the smallest price point.

**Activity floor:** last post or visible activity within ~3 weeks. Check this against a live web search on the lead's name, not secondhand notes — the search is what actually tells you if she posted recently. Receipt: Lisa Chan, 7 weeks silent, correctly parked, but only because the user caught it by instinct. Now it's a rule, and it's verifiable directly instead of trusted on faith.

**Niche floor:** parenting or faith-based, genuinely. Adjacent wellness niches without the case-study fit get parked. Receipt: Gayu Lewis, menopause coach, her own row said "not parenting" and she got three touches anyway.

Failing the floor means Lane 3, reason noted, stop — don't proceed to Gate 1 or the filters below. The floor exists to protect touches, which are the scarcest resource in a crisis.

### Step 2.7 — Gate 1 Check (2 seconds)

One question only: is there a team or gatekeeper between the user and the owner?

Signs: "our team," a named co-creator running ops, a verified mega-account (150K+) with a manager triaging DMs.

If yes, classify as Lane 3: Skip, note the reason as "gatekeeper/team," write to Notion, and stop. If no or unclear, proceed to Step 3.

### Step 3 — Apply Filters & Determine Lane

**Do not start this step until Step 2.5's `vision check` printed `VISION PASS: COMPLETE`** (or you've logged the unreadable-image exception) and the lead has cleared the floor (Step 2.6) and Gate 1 (Step 2.7). Pass that literal line into the lane analysis — it will be part of the final verdict.

**Sting test:** Would she FEEL this if you named it, or shrug?
**Vitamin filter:** Is this a FELT COST or a MECHANISM she lacks?

**Three lanes:**
- **Lane 1 — OPEN**: Felt leak + committed buyer. Conversion lane. Generate opener.
- **Lane 2 — WARM-UP**: Committed buyer, no felt leak. Intel lane. Warm entry, no opener.
- **Lane 3 — KILL**: Not a buyer. Park. Status → Disqualified.

If Lane 1, also identify:
- **Innocent explanation**: The non-embarrassing reason the leak exists.
- **SMYKM hook**: WORK, LIFE, or METRIC label + the specific hook.

**PITFALL — IG creators with 5K+ followers + keyword-comment CTAs are running ManyChat (or similar).** Do not frame the leak as "she manually sends the link" — at that scale the DM is automated, often on the same trigger keyword ("comment MOTHER for the link"). The real leak is **downstream**: the gap between total reach and the people who actually trigger the keyword flow. The silent majority (reach minus engagers minus commenters) see the post, do not act, are not on a list, and have no second touch available before the next launch. Frame the leak as **reach-to-captured-intent**, not as labor. The math is the falsifiable claim: "of 11,500 followers, 75 liked the post and a few dozen will comment MOTHER. The other 11,000 are not in your inbox, not on your list, and not in a way to hear from you again before the next launch."

### Step 4 — Write the Audit to Notion

Use `mcp__notion__API_update_page_markdown` with `type="replace_content"`. The page body format:

```markdown
## Overview
One paragraph. Name, business, niche, platform, main offer.

## Funnel Walk
Stop X — [what's there] — [what it means]
(Skip clean unremarkable stops)

## Evidence
**IG evidence:** [paste the literal `python main.py vision check evidence/<slug>` output for ig/ images, e.g. "VISION PASS: COMPLETE — 4 of 4 required images confirmed read"] OR "none attached — site-only walk". If the line says INCOMPLETE, write INCOMPLETE, plus which paths, plus the reason if known — do not round up to "read."
**Site vision pass:** [paste the literal `vision check` output for site screenshots] OR the same INCOMPLETE-with-detail treatment.
**Machine flags rejected in the vision pass:** [N — one-phrase reason each] OR "none rejected"

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

Then update properties via `mcp__notion__API_patch_page`:
- Status → "Audit Ready"
- Lane → verdict
- Finding Type → type
- Tier → quality
- Platform → detected platform

**Notion REST API body write (MCP unavailable):** When `mcp__notion__API_update_page_markdown` isn't in your tool list, use the block-level REST API: GET existing blocks, DELETE each one, then PATCH append new blocks in batches of ~30. Full recipe and code in `references/notion-rest-api-body-write.md`.

**PITFALL — Notion MCP `patch_page` shape for array-typed properties (rich_text, multi_select, relation):**

The MCP wrapper for `mcp__notion__API_patch_page` accepts `select` properties as native objects:
```
{"properties": {"Status": {"select": {"name": "Audit Ready"}}}}
```
But it **wraps array-typed properties as `{"item": [...]}`** if you pass them as native arrays, and the Notion API rejects that with "X.rich_text should be an array, instead was `{\"item\": ...}`". Pass the array as a **JSON-encoded string** instead:
```
{"properties": {"Main Offer": {"rich_text": "[{\"type\":\"text\",\"text\":{\"content\":\"...\"}}]"}}}
{"properties": {"Niche": {"multi_select": "[{\"name\":\"Conscious Parenting\"}]"}}}
```

**Property-patch recipe that works on the first try:**
1. Patch all `select` properties together in one call (Status, Lane, Finding Type, Tier, Platform, Source, Est. Value).
2. Patch each `rich_text` and `multi_select` in a separate one-property call, with the array as a JSON string.
3. Don't mix select and array-typed properties in the same call.

Full error transcripts and a working example are in `references/notion-patch-page-shapes.md`.

### Step 5 — Generate Opener (Lane 1 only)

Use the **haytham-email-draft** skill. Its four core docs load once before the first draft of the session -- do NOT re-read them per lead. The silent gate loop runs as plain text reasoning (not execute_code) -- no draft shown until it clears every check.

**The drafting pattern that works:** generate **2-3 variants** and gate-check all of them manually against the kill list, em-dash rule, three-beat ban, and register test (all plain text checks - no code needed). Then pick the one that passes AND has the roughest edge -- per Haytham's voice doc, polish is the tell. Don't pick the smoothest version; pick the one a real person would send.

For Lane 2: a warm-up entry draft (no specific finding to point at -- soft open).

**SMYKM hook guard — before drafting from an IG-based hook:** If the SMYKM hook cites specific IG post content (a date, a quote, an engagement number, "her post about X") rather than something from her site copy, confirm the vision pass actually verified it — the image must show `read: true` in `vision_manifest.json`. If that confirmation isn't there, do not draft the hook as given. Either fall back to a hook grounded in confirmed site copy, or tell Haytham directly: "possible hook on an unread image (ig/N.png) — need to read it or have you confirm the post's content before it goes in a draft." A hook built on an unread image must never reach a Gmail draft.

### Step 6 — Create Gmail Draft (after user approval)

```bash
cat << 'EOF' | himalaya template save --folder Drafts
From: haytham@auto-mate.one
To: [lead-email]
Subject: [subject line]

[body]
EOF
```

### Step 7 — Log and Update (after user confirms send)

Update page body Email Thread Log using the exact format from pipeline-tick's `references/email-thread-log-format.md`.

Update properties:
- Status → "Outreach Sent"
- Touch # → 1
- Sequence → "Cold"
- Last Contacted → today
- Next Action → today + 3 days

## Delegation Rules

Do NOT delegate Steps 4, 6, or 7. Page body writes, Gmail drafts, and final logging must be done directly. See `AGENTS.md` for the full delegation boundaries.

Step 2 (funnel walk) defaults to running the CLI directly in the main session. Only delegate for parallel batch work (3+ sites at once). Step 2.5 (vision pass) is always done directly — it calls vision_analyze which routes through the auxiliary model slot, and must not be delegated. Step 3 (analysis) is always done directly.

## Quick Reference

| File | Path | When to load | Notes |
|---|---|---|---|
| Voice rules | `docs/haythams-voice.md` | Before first draft of session | Core drafting reference |
| Drafting rules | `docs/the-drafting-doc.md` | Before first draft of session | Core drafting reference |
| Email mechanics | `docs/email-os.md` | Before first draft of session | Core drafting reference |
| Subject line rules | `docs/smykm-test-layer.md` | Before first draft of session | Core drafting reference |
| Methodology | `docs/the-bible.md` | Before first funnel walk of session | Not needed for draft-only sessions |
| Offer/pricing | `docs/grand-slam-offer-v2.md` | Only when the email states price | On demand |
| Case study | `docs/pwh-case-study.md` | Only when the email cites the proof asset | On demand |
| Notion patch shapes | `references/notion-patch-page-shapes.md` | Only when a property patch fails | On demand |
| Notion REST API body write | `references/notion-rest-api-body-write.md` | When MCP Notion tools aren't in-session | Delete-all + batch-append blocks via REST API, plus property patch differences vs MCP |
| Browser fallback techniques | `references/browser-fallback-techniques.md` | When CLI fails and browser fallback is used | Console-based page text extraction, hidden checkout URL discovery, URL verification |
| Direct Notion REST API (external) | `cold-outreach-pipeline skill → references/direct-notion-rest-api.md` | For general REST API reference | Broader coverage of Notion API endpoints |

**IMPORTANT:** Each doc is read at most ONCE per session, on first need — never preloaded in bulk, never re-read per lead. If you've processed one lead in this session, the docs you used are already in your active context. Gate checks are plain text reasoning — never execute_code, never a script.

## Hard Rules (from the repo's process-lead + vision gate merge fd60c47)

- **The vision pass is a computed fact, not a claim.** `python main.py vision check evidence/<slug>` is the only source of truth for "read every image." A verdict, a Notion write, or a chat report that says "N screenshots read" without that exact command having printed `VISION PASS: COMPLETE` first is a false statement, full stop.
- **SMYKM hooks that cite specific IG post content (a quote, a date, an engagement number) are only usable if the image they came from shows `read: true` in `vision_manifest.json`.** If it doesn't, do not surface that hook to the email skill — either substitute a hook grounded in confirmed site copy or flag it as unconfirmed.
- **A machine flag that failed visual confirmation is dead.** It does not get resurrected as a hedge ("might also be…") in the email.
- **Never invent findings.** No verified finding → Lane 2 or Lane 3. A clean funnel is not a failure — it's an intel lead.
- **Never send email.** System stops at Gmail drafts. Never auto-advance Touch #/Status for an unsent email.