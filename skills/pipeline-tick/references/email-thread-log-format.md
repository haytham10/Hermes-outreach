# Email Thread Log — Exact Format

This is the ONLY format allowed for the `## Email Thread Log` section in a lead's Notion page body.

## New entry format (append after the last entry)

```
[YYYY-MM-DD] — Touch #[N] — Subject: "exact subject line" — Sent

[Verbatim email body — the exact text that was sent, including any quoted thread history]

Reply: No reply
Next: [YYYY-MM-DD — specific next action + date]
```

## Rules

1. **Date format**: `[2026-07-09]` — ISO date, brackets
2. **Touch #**: Increment by 1 from the lead's current Touch # property
3. **Subject**: Exact subject line in quotes
4. **Status**: `Sent` (after user confirms send), `Draft created` (before send)
5. **Body**: FULL verbatim text of the email that was sent. Include quoted thread history if it's a reply.
6. **Reply**: `No reply` if no response yet, or verbatim reply text if one exists
7. **Next**: Specific date + specific action. Never "follow up soon" — always a concrete date.

## Example

```
[2026-07-09] — Touch #3 — Subject: "Re: the sink that's already full" — Sent

Hey Dr. Gila

The contact form on your coaching page is still the only way to get in touch. A parent who's ready to book hits that instead of a calendar and has to wait for a reply.

Same offer's still open — $200, everything fixed and live within 48 hours, you check it works, then you pay. Worth doing this week?

On Mon, Jul 07, 2026 at 12:05 PM, Haytham Mokhtari <haytham@auto-mate.one> wrote:
> Hey Dr. Gila
> 
> No prices anywhere on the site, just a 7-field intake form. A parent who's ready to buy has no way to self-qualify before committing.
> 
> Still curious whether that pricing structure is intentional or just not set yet?

Reply: No reply
Next: 2026-07-12 — follow up if no reply
```

## What this format does NOT include

- No extra headings inside the entry
- No "---" separators between entries
- No markdown formatting inside the body (preserve plain text)
- No extra blank lines beyond the single blank line between body and Reply: