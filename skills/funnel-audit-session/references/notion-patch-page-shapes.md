# Notion MCP `patch_page` — Array Property Shapes

## The rule (one line)

**Select properties** pass as native objects. **Array-typed properties** (rich_text, multi_select, relation) pass as **JSON-encoded strings**, not native arrays.

## Why

The Notion MCP wrapper at `mcp__notion__API_patch_page` (as of 2026-07-09) accepts select objects directly but wraps native arrays as `{"item": [...]}` before sending to the Notion API. The Notion API then rejects with a "should be an array, instead was `{\"item\": ...}`" error.

## Working shapes

### Select (native object) — works directly

```json
{
  "page_id": "...",
  "properties": {
    "Status": {"select": {"name": "Audit Ready"}},
    "Lane": {"select": {"name": "Lane 1: Felt leak"}},
    "Finding Type": {"select": {"name": "No opt-in capture"}},
    "Tier": {"select": {"name": "Tier 1: Start here"}},
    "Platform": {"select": {"name": "GHL"}}
  }
}
```

### rich_text (JSON string) — required

```json
{
  "page_id": "...",
  "properties": {
    "Main Offer": {
      "rich_text": "[{\"type\":\"text\",\"text\":{\"content\":\"1:1 Coaching $147, mini-courses $11-$333\"}}]"
    }
  }
}
```

### multi_select (JSON string) — required

```json
{
  "page_id": "...",
  "properties": {
    "Niche": {
      "multi_select": "[{\"name\":\"Conscious Parenting\"},{\"name\":\"Mom Mental Health\"}]"
    }
  }
}
```

## Broken shapes (will fail validation)

### Native array (wrapped by MCP as {"item":[...]}):

```json
{
  "Main Offer": {"rich_text": [{"type":"text","text":{"content":"..."}}]}
}
```
Error: `body.properties.Main Offer.rich_text should be an array, instead was {"item":[{"text":{...}}]}`

### Mixed select + array in same call:

Sometimes works, sometimes doesn't. Don't risk it. Split into two calls.

## Recipe for an audit-update burst

1. **Call 1** — all select properties at once.
2. **Call 2** — `Main Offer` (rich_text) as JSON string.
3. **Call 3** — `Niche` (multi_select) as JSON string.
4. **Verify** with `mcp__notion__API_query_data_source` filtered to the page.

Three calls, ~5 seconds, zero retries.

## When the error changes shape

If the wrapper is updated and these shapes stop working, the new error will mention the actual wrapping key. Look for it in the error message and adjust accordingly — the principle (array-typed properties need special encoding) is the durable lesson, not the specific wrapper behavior.
