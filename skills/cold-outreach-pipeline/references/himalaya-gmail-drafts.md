# Himalaya Gmail Drafts

## Confirmed: `template save` creates drafts

Himalaya has a `template save` subcommand that saves a message template to a specified folder. Combined with Gmail's `[Gmail]/Drafts` folder via the folder alias, this creates Gmail drafts that appear in the user's Drafts folder for manual review and send.

```bash
himalaya template save --folder Drafts
```

Piped input works:

```bash
cat << 'EOF' | himalaya template save --folder Drafts
From: sender@example.com
To: recipient@example.com
Subject: Test Draft

This is the body of the draft.
EOF
```

## Gmail Folder Aliases

Gmail uses non-standard IMAP folder names. Himalaya needs explicit mapping in `~/.config/himalaya/config.toml`:

```toml
[accounts.default]
# ... other config ...

folder.aliases.inbox = "INBOX"
folder.aliases.sent = "[Gmail]/Sent Mail"
folder.aliases.drafts = "[Gmail]/Drafts"
folder.aliases.trash = "[Gmail]/Trash"
```

**Note**: The alias syntax changed in Himalaya v1.2.0. Use `folder.aliases.drafts` (plural, dotted key under `[accounts.NAME]`). The old `[accounts.NAME.folder.alias]` sub-section syntax (singular `alias`) is silently ignored in v1.2.0+.

## Verification

```bash
# Check if folders are accessible
himalaya folder list

# Verify drafts are saving correctly by checking after save
himalaya envelope list --folder Drafts --page-size 5
```

## Template Format (MML)

Himalaya templates use MML format (see `references/message-composition.md` in the Himalaya skill). Minimum required headers:

- `From:` — sender
- `To:` — recipient(s), comma-separated
- `Subject:` — subject line

Body follows after a blank line. Plain text only for cold outreach (per Email OS rules: no HTML, no images).
