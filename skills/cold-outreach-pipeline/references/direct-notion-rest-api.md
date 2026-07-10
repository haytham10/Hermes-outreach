# Direct Notion REST API Usage

When Notion MCP tools aren't available in-session (e.g. MCP tool naming mismatch in config, session not reloaded after config change, or MCP server failed to start), you can call the Notion API directly using `requests` or `curl`.

## Setup

```python
import json, re, requests

# Read token from Hermes config
CONFIG_PATH = r"C:\Users\cnara\AppData\Local\hermes\config.yaml"
with open(CONFIG_PATH, "r") as f:
    content = f.read()
m = re.search(r"NOTION_TOKEN:\s*(\S+)", content)
token = m.group(1)

headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28",
}
```

## Common Operations

### 1. Find the real database ID
The data source ID (e.g. `c6209e29-...`) is NOT the database ID. Search to discover the real one:
```python
resp = requests.post("https://api.notion.com/v1/search", headers=headers, json={
    "filter": {"value": "database", "property": "object"},
    "sort": {"direction": "descending", "timestamp": "last_edited_time"},
})
db_id = None
for r in resp.json().get("results", []):
    title = "".join(p.get("text", {}).get("content","") for p in r.get("title",[]))
    if title == "Lead Pipeline":
        db_id = r["id"]
        break
```

### 2. Query the database
```python
resp = requests.post(f"https://api.notion.com/v1/databases/{DB_ID}/query",
    headers=headers, json={
        "filter": {"property": "Status", "select": {"equals": "Researching"}},
        "sorts": [{"property": "Created time", "direction": "descending"}],
    })
```

**PITFALL — filter type must match the property's schema type.** The `Status` property in the Lead Pipeline is a `select` type, not a Notion `status` type. Using `"status": {...}` instead of `"select": {...}` returns `400: database property select does not match filter status`. Always check the database schema to know whether a property is `select`, `status`, `rich_text`, `multi_select`, etc. To inspect:
```python
resp = requests.get(f"https://api.notion.com/v1/databases/{DB_ID}", headers=headers)
props = resp.json().get("properties", {})
for name, schema in props.items():
    print(f"{name}: {schema['type']}")
```

### 3. Retrieve page body (markdown)
```python
resp = requests.get(f"https://api.notion.com/v1/pages/{PAGE_ID}/markdown",
    headers=headers)
markdown = resp.json().get("markdown", "")
```

### 4. Update page body (blocks) — fallback when MCP is unavailable

The `/v1/pages/{id}/markdown` endpoint is provided by the `@notionhq/notion-mcp-server` MCP server — it is NOT a native Notion REST API endpoint. Calling it directly returns `400: body.type should be defined`. When MCP tools aren't in-session, you must use the block-level API instead.

Read existing body blocks (images + text):
```python
# Get the page's block children
resp = requests.get(f"https://api.notion.com/v1/blocks/{PAGE_ID}/children",
    headers=headers, params={"page_size": 50})
blocks = resp.json().get("results", [])
```

Append text blocks (one block per markdown section):
```python
from datetime import datetime

def notion_rich_text(text):
    """Wrap plain text into a Notion rich_text array."""
    return [{"type": "text", "text": {"content": text}}]

def notion_heading_block(heading_text, level=2):
    """Create a heading block."""
    htype = f"heading_{level}"
    return {
        "object": "block",
        "type": htype,
        htype: {"rich_text": notion_rich_text(heading_text)}
    }

def notion_paragraph_block(text):
    """Create a paragraph block."""
    return {
        "object": "block",
        "type": "paragraph",
        "paragraph": {"rich_text": notion_rich_text(text)}
    }

# Append multiple blocks at once
new_blocks = {
    "children": [
        notion_heading_block("Overview"),
        notion_paragraph_block("One paragraph about the lead."),
        notion_heading_block("Funnel Walk"),
        notion_paragraph_block("Stop 1 — ..."),
    ]
}
resp = requests.patch(
    f"https://api.notion.com/v1/blocks/{PAGE_ID}/children",
    headers=headers, json=new_blocks
)
```

**PITFALL:** The block-level API can only APPEND — you cannot atomically replace all body content like you can with the MCP markdown endpoint. Existing blocks (including Haytham's IG screenshots) remain. To fully replace content, you'd need to DELETE existing blocks first (not recommended — IG screenshots are sourced evidence). Always append your audit text below the existing image blocks.

### 5. Update page properties (patch_page)
```python
resp = requests.patch(f"https://api.notion.com/v1/pages/{PAGE_ID}",
    headers=headers, json={
        "properties": {
            "Status": {"select": {"name": "Audit Ready"}},
            "Lane": {"select": {"name": "Lane 2: Warm-Up"}},
        }
    })
```

## Pitfalls
- **Property types in the Lead Pipeline DB: `Status` is `select`, not `status`.** This has caused `400: database property select does not match filter status` errors in past sessions. When filtering or patching Status, always use `{"select": {"equals": "..."}}` or `{"select": {"name": "..."}}`, never `status`. The database schema categorizes Status as a `select` field (custom options), not a Notion-native `status` field (built-in workflow states).
- The markdown endpoint (`/v1/pages/{id}/markdown`) preserves image blocks but replaces ALL text content. Read the body first, then write the full audit body.
- `replace_content` returns 200 even if the write partially fails — always verify by reading back.
- Property values use Notion's API types: `select`, `rich_text`, `multi_select`, `title`, `url`, `email`, `number`, `date`, `phone_number` (note: `status` type is only used for Notion-native status properties, which this DB doesn't use).
- For `rich_text` and `multi_select` through the MCP, pass arrays as JSON-encoded strings (see `notion-patch-page-shapes.md`). Through the direct REST API, pass native arrays.
