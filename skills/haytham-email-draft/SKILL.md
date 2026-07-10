---
name: haytham-email-draft
description: "Draft cold outreach emails, follow-ups, warm replies, money emails, and past-client reactivation in Haytham's voice for parenting/faith-based coach leads. Full silent gate loop, logging rules, Gmail draft via himalaya. Never sends — drafts only."
tags: [email, outreach, cold-email, copywriting, voice]
---

# Haytham Email Draft

Draft outreach that reads like a real person who walked their funnel, admired the work, noticed a gap almost against his will, and cares enough to mention it. Not a freelancer running a play.

## Local docs (load each at most ONCE per session, on first need — never per lead)

Do not preload anything at session start. Before the FIRST draft of the session, read the four core docs. After that they are in your active context: refer to context rather than re-reading the files. Only re-read if you have explicit reason to believe a file changed on disk. If unsure, say so and ask — don't silently re-read everything.

Core (read before the first draft):
- `~/projects/hermes-outreach/docs/haythams-voice.md` -- the belief system + full kill list (canonical; `references/voice-rules.md` is only a pointer to it — never load both)
- `~/projects/hermes-outreach/docs/email-os.md` -- mechanics, follow-up sequences, tracking
- `~/projects/hermes-outreach/docs/smykm-test-layer.md` -- SMYKM subject line rules
- `~/projects/hermes-outreach/docs/the-drafting-doc.md` -- copywriting rules

On demand only (skip unless the draft actually needs them):
- `~/projects/hermes-outreach/docs/grand-slam-offer-v2.md` -- only when the email states price/terms
- `~/projects/hermes-outreach/docs/pwh-case-study.md` -- only when the email cites the proof asset

## Reference files

- `references/known-docs.md` — which Notion docs are current vs outdated (fetch these, skip those)
- `references/cold-touch-1-pattern.md` — proven cold opener structure (concrete example + all anti-patterns)

Gate checks are plain text reasoning — never execute_code, never a script.

## The non-negotiable order of operations

1. **Identify the email type first.** Cold Touch 1 opener, cold follow-up (Touch 2-4), warm bump, turn-two reply (offering the Loom), money email (priced close), objection reply, or past-client reactivation.

2. **Confirm you have the input.** Lead name, niche, verified finding, enough of the funnel walk. If the finding is vague, ask for the specific thing on the specific page.

3. **Check whether the docs are already in context.** If you drafted in this session already, the core docs are in your active context — use what you have. Do NOT call read_file again on the same file within the same session. If context has been trimmed mid-session, say so explicitly and ask -- do not silently re-read everything.

4. **See in the right order.** Admire first. Find the gap reluctantly. Help before sell.

5. **Draft it.** One finding, one cost, one question or one offer. Plain text. No Loom or Calendly link in email 1. Proper capitalization. No sign-off (Gmail auto-signature handles it). Every sentence is one idea, then stop. No compound sentences that pack three claims into one line (that is a three-beat in camouflage).

6. **Run the burrito test.** Pull each sentence out. Does the email still stand without it? If yes, cut it.

7. **Run the gate as plain text reasoning.** Check manually against: kill list, em-dash rule, three drafting rules (visualize, falsify, bespoke), mechanics (subject, one CTA, niche lingo), the three-beat ban (X, Y, and Z -- any variant in any sentence), and the subject-body continuity rule (first sentence must echo the SMYKM hook). No draft shown until it clears every check. Do NOT use execute_code for gate checks -- these are plain text scans: word count, kill list lookup, em-dash search. If you can do it by eye in 30 seconds, do it by eye.

8. **Run the register test.** Read the draft aloud. Does it sound like Haytham talking to someone who already trusts him? Or does it sound written, polished, consultant-y? If it sounds written, rewrite from scratch. This test overrides all others.

9. **Check for rough edges.** Good copy is never perfect. Is there a fragment, a line that just stops, a word dropped on purpose? If every sentence is a full grammatical clause with perfect comma placement, the draft is too polished. Sanding is the tell of someone trying — and trying is the opposite of the register.

10. **Deliver via message-composer.** Subject in subject field, body in body. Single variant unless the user asks for options.

## Critical failures (learned from repeated user corrections)

These are the most common mistakes. Each one has been corrected by the user — sometimes with frustration. Internalize them before every draft.

### Three-beat parallel structures (banned per voice.md)

The voice doc bans "not just X, but Y, and Z." The intent extends to ANY three-item parallel list in one sentence.

**Common violations:**
- "The cohort is well built, the voice is consistent, and the niche has weight." — three clauses in one sentence
- "11,500 people visit, leave, and never hear from you again." — three verbs in series
- "They are not in your inbox, not on your list, and not reachable." — three parallel negatives

**Fix:** Break into separate sentences. "The cohort is well built. The voice is consistent. The niche has weight." Each period is a pause for the reader. Multiple short sentences in a row is NOT a three-beat — beats require parallel clauses inside one sentence.

### Formulaic transitions (banned)

These become templates the user can spot instantly:
- "The thing that got me though" / "What I couldn't shake" / "The thing I noticed" — overused frames
- "Deliberate, or one of the things that has not been built yet?" — templated question that repeats across emails
- "I noticed..." — on the kill list
- "I wanted to reach out..." — on the kill list
- "Anyway, the reason I'm writing..." — the SMYKM transition line is an OPTION, not a formula. Don't default to it.

**Fix:** State the finding flatly. "Your site doesn't have an email signup." No discovery frame. No "I went through your site and found..." Just the fact.

### Math breakdowns read like audits

"Of the 11,500 followers who saw that post, 75 liked it and a few dozen will comment MOTHER. The other 11,000 are not in your inbox..." — this reads like a funnel report, not a human cold email.

**Fix:** The number is backdrop, not the argument. "11,500 followers and nowhere for them to leave an email. They leave. Next launch, clean slate." One number. One cost. Done.

### Subject-body disconnect

The SMYKM subject must be echoed in the first body sentence. If the subject is "the comment MOTHER button" and the first body sentence names the cohort, the subject feels disconnected.

**Fix:** The SMYKM rule says "elaborate on the SMYKM hook, then bridge to finding" (option A). First sentence = elaborates on the hook (mentions "comment MOTHER" or the specific CTA). Second sentence = bridges to the finding. This is also how "admire first" and "finding first" resolve — the hook elaboration IS the admiration.

### The email OS vs voice doc tension

The email doc says "Line 1: the finding, stated flatly. No warm-up." The voice doc says "admire first."

**Resolution for cold Touch 1:**
- The SMYKM subject IS the hook
- First body sentence: elaborate on the hook (this IS the admiration — her CTA works)
- Second sentence: bridge to the finding
- Example: "Your comment MOTHER posts work for the parents who act that morning. The rest of the 11,500 visit your site though. Nothing to sign up for."

### Small metric next to big one (banned)

When contrasting a big number she owns against a small one she owns, never name the small one alongside the big one — not in subject, not in body. Lead with the strength only (the big thing, the admired thing). Let the gap be felt without announcing both numbers side by side.

**Violation:** Subject = "the broken link on your linktree" (small thing), body opens with 37.8K followers and a $158 program (big things). The small thing deflates the big thing before the gap is even named.

**Fix:** Lead with the strength. Subject = the thing she's winning at. The gap is felt in the body, not announced stat-to-stat.

### Disguised kill-list patterns

The gate checks the *pattern*, not the literal kill-list string. A phrase that functions the same as a banned phrase is banned.

**"I went through your site today"** = the "I came across your profile" pattern with different words. Also "I checked out your site," "I looked at your [page]," "I was looking at your [page]." All banned. State the finding flatly — no discovery frame at all.

**"I could not just watch it"** / **"I could not just sit around"** = the "stuck with me" / "stayed with me" pattern — performing emotional investment instead of stating a fact. Cut it. State what happened, not how you felt watching it.

### Two findings stacked in Touch 1

One finding, one cost, one question — that is non-negotiable for every touch, and it is especially non-negotiable on Touch 1. Pick the single strongest finding and hold the rest for later touches or drop them entirely.

**Fix:** When you have multiple flags (broken CTA, 404 linktree link, non-delivering freebie), choose the one that is the most direct version of the Lane's felt leak. Drop the others.

### Admire must be genuine seeing, not stat recitation

Listing her follower count, credentials, and price is a stat sheet, not admiration. The gate wants you to actually see what she built and feel it before the leak shows up — not justify the pitch with numbers.

**Good:** "Your Real-Life Regulation Guide is exactly the kind of resource parents need. A free download they can actually use." — sees the resource, feels its value.

**Bad:** "You've got 37.8K followers, a therapist's training, and a $158 program shaped by 10 years of clinical work." — inventory, not admiration.

### Close is a real question, not a scheduling ask

"Do you have time over the next week or so?" is a generic scheduling ask the gate exists to kill. Close with a real one-line-answerable question tied to the specific finding.

**Good:** "Do you know the guide is not sending?" — answerable in a word or sentence, tied to the specific thing.

**Bad:** "Do you have time over the next week or so?" — generic, unanswerable except with a calendar.

**Bad:** "Deliberate, or one of the things that has not been built yet?" — formulaic, repeats across emails.

### No solution pitch before reply (help before sell)

On Touch 1, do not offer to build, fix, or implement anything. She has not replied yet. A solution pitch before reply is selling before helping. The close must be a question she can answer in a sentence — not an offer to deliver.

**Good:** "Do you know the guide is not sending?" — question.

**Bad:** "If you want, I can build the part that sends the guide." — solution pitch before she has engaged.

**Bad:** "If you want, I can show you what I'd put between the feed and a list." — offer before relationship.

### No name salutation in cold emails

Cold emails start with the first body sentence directly. No "Hi [Name]," no "Hey [Name]," no name greeting. The SMYKM subject is the hook; the first body sentence elaborates on it. A salutation before that creates dead weight.

## Logging (only after user says "log this")

Append to lead's Notion page body under Email Thread Log:

```
[Date] — Touch #N — Subject: "exact subject line" — Sent

[Verbatim email body]

Reply: No reply
Next: [specific next action + specific date]
```

**PITFALL — empty paragraph blocks are stripped by Notion.** When using the block-level REST API to append the thread log entry, do NOT insert empty paragraph blocks (`para("")`) between content lines for visual spacing. Notion eliminates paragraph blocks with empty rich_text. Adjacent content paragraphs render with natural spacing. Append the header, body, Reply, and Next lines as consecutive paragraph blocks with no empty spacers between them.

Update ALL properties in one call: Touch # (+1), Sequence (Cold→Warm on first reply), Status (Outreach Sent / Reply Received / Loom Sent / Call Booked / Won / Lost / Dormant), Last Contacted (today), Next Action (depends on touch type).

## Creating Gmail drafts — final write-back (MANDATORY)

After user approves a final gated draft, you MUST write it to Gmail AND verify it. "Showing the text" and "saving the draft" are two different actions — the workflow does both, in that order, every time.

### Step A — Check for an existing draft to the same address

Before saving, check whether a previous draft to this contact already exists:

```bash
himalaya envelope list --folder Drafts --page 1 --page-size 50 --output json
```

If a draft exists, note its ID. You will delete it after the new one is saved (or before, but deleting first leaves a window with zero drafts — safer to save new, then delete old).

### Step B — Save the new draft

```bash
cat << 'EOF' | himalaya template save --folder Drafts
From: haytham@auto-mate.one
To: recipient@example.com
Subject: Subject line

Body text here.
EOF
```

### Step C — Delete the old draft (if any)

```bash
himalaya message delete OLD_ID --folder Drafts
```

### Step D — Verify the live draft matches the approved text

Read the draft back from Gmail and confirm subject + body match the final gate-approved version:

```bash
himalaya message read NEW_ID --folder Drafts --output json
```

Compare the output to the final text. If they differ, delete and re-save.

**Do not tell the user the draft is ready until step D confirms a byte-exact match.**

## What this skill does NOT do

- It does not log to Notion before user approval. Draft is not send.
- It does not invent findings. No verified finding → ask.
- It does not advance Status/Touch #/Last Contacted for a draft. Only after user confirms a send.