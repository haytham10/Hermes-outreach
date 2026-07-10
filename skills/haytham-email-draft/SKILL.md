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

### Motivation must feel real

The voice doc models: "I couldn't just sit around and watch your work go underappreciated." Say WHY you're writing. But keep it brief. "I couldn't just watch it." is enough when context supplies "it" (11,500 people disappearing).

### The close is an open door, not a bow

No "let me know." No "looking forward." No "if you're open to it." A conditional offer with a concrete picture ends the email:

Good: "If you want, I can show you what I'd put between the feed and a list."
Bad: "Let me know if you'd like to chat about this."
Bad: "If you're open to it, I'd love to show you some ideas."

The concrete picture ("between the feed and a list") does the work. The question mark does not need to carry the weight alone.

## Logging (only after user says "log this")

Append to lead's Notion page body under Email Thread Log:

```
[Date] — Touch #N — Subject: "exact subject line" — Sent

[Verbatim email body]

Reply: No reply
Next: [specific next action + specific date]
```

Update ALL properties in one call: Touch # (+1), Sequence (Cold→Warm on first reply), Status (Outreach Sent / Reply Received / Loom Sent / Call Booked / Won / Lost / Dormant), Last Contacted (today), Next Action (depends on touch type).

## Creating Gmail drafts

After user approves, create the draft:

```bash
cat << 'EOF' | himalaya template save --folder Drafts
From: haytham@auto-mate.one
To: recipient@example.com
Subject: Subject line

Body text here.
EOF
```

## What this skill does NOT do

- It does not log to Notion before user approval. Draft is not send.
- It does not invent findings. No verified finding → ask.
- It does not advance Status/Touch #/Last Contacted for a draft. Only after user confirms a send.