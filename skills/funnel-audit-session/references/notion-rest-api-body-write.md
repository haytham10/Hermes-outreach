# Notion REST API — Page Body Write (MCP Unavailable)

When `mcp__notion__API_update_page_markdown` isn't in the tools list, use the Notion REST API block-level endpoints to replace a page's body content.

## Recipe: Replace All Page Body Content

### Step 1 — Get existing blocks

```
GET https://api.notion.com/v1/blocks/{page_id}/children?page_size=50
```

Returns the current blocks on the page (images, paragraphs, headings, etc.).

### Step 2 — Delete every existing block

Each block must be deleted individually:
```
DELETE https://api.notion.com/v1/blocks/{block_id}
```

Iterate through all results from Step 1 and DELETE each block ID.

Notion's API doesn't support batch delete — you must loop. For a page with 6 blocks (4 images + 2 paragraphs), this takes 6 DELETE calls.

### Step 3 — Build your blocks

Notion's API accepts blocks in this shape:

```python
def heading_2_block(content):
    return {
        "object": "block",
        "type": "heading_2",
        "heading_2": {
            "rich_text": [{"type": "text", "text": {"content": content}}]
        }
    }

def paragraph_block(content):
    return {
        "object": "block",
        "type": "paragraph",
        "paragraph": {
            "rich_text": [{"type": "text", "text": {"content": content}}]
        }
    }

def bullet_block(content):
    return {
        "object": "block",
        "type": "bulleted_list_item",
        "bulleted_list_item": {
            "rich_text": [{"type": "text", "text": {"content": content}}]
        }
    }
```

**PITFALL — empty paragraph blocks are stripped by Notion.** Do NOT insert `paragraph_block("")` between content lines to create visual spacing. Notion's block renderer eliminates paragraph blocks with empty rich_text. Adjacent paragraph blocks render with natural spacing automatically — consecutive content blocks are visually distinct without empty spacers. This applies most commonly to Email Thread Log entries: append header, body, Reply, and Next lines as consecutive paragraph blocks with no empty blocks between them.

Available block types: `heading_1`, `heading_2`, `heading_3`, `paragraph`, `bulleted_list_item`, `numbered_list_item`, `to_do`, `toggle`, `callout`, `quote`, `divider`, `image`, `video`, `file`, `code`, `table_of_contents`, `column_list`, `embed`, `bookmark`, `equation`.

For the audit body format (headings + paragraphs + bullets), `heading_2`, `heading_3`, `paragraph`, and `bulleted_list_item` cover all the required shapes.

### Step 4 — Append in batches (max ~30 per call)

Notion limits batch appends. Split into chunks of ~30 blocks:

```
PATCH https://api.notion.com/v1/blocks/{page_id}/children
{
    "children": [{block1}, {block2}, ...]
}
```

A typical audit body (Overview, Funnel Walk, Evidence, Gate 1, Lane + Opening Angle, Email Thread Log) is ~20-27 blocks — fits in 1 or 2 chunks.

### Full Recipe (Python)

```python
import requests

headers = {
    'Authorization': f'Bearer {token}',
    'Content-Type': 'application/json',
    'Notion-Version': '2022-06-28',
}

page_id = '...'

# 1. Get existing blocks
resp = requests.get(f'https://api.notion.com/v1/blocks/{page_id}/children?page_size=50', headers=headers)
existing = resp.json().get('results', [])
block_ids = [b['id'] for b in existing]

# 2. Delete them
for bid in block_ids:
    requests.delete(f'https://api.notion.com/v1/blocks/{bid}', headers=headers)

# 3. Build blocks list
blocks = [
    heading_2_block("Overview"),
    paragraph_block("..."),
    # ... all blocks
]

# 4. Append in batches of 30
for i in range(0, len(blocks), 30):
    chunk = blocks[i:i+30]
    requests.patch(
        f'https://api.notion.com/v1/blocks/{page_id}/children',
        headers=headers,
        json={"children": chunk}
    )
```

## Property Patches (REST API)

Property patches via the REST API (`PATCH /v1/pages/{id}`) do NOT have the MCP array-wrapping issue documented in `notion-patch-page-shapes.md`. With the REST API, you can pass `rich_text` as a native array and `select` as a native object in the same call — it works fine.

```python
# REST API — all property types work together:
payload = {
    "properties": {
        "Status": {"select": {"name": "Audit Ready"}},
        "Main Offer": {"rich_text": [{"type": "text", "text": {"content": "..."}}]},
    }
}
```

## Key Differences from MCP

| Aspect | MCP `patch_page` | REST API `PATCH /v1/pages/{id}` |
|---|---|---|
| Array props (rich_text, multi_select) | Must be JSON-encoded string | Native array works fine |
| Mixed select + array in same call | Breaks | Works fine |
| Page body write | `API_update_page_markdown` (one-call markdown) | Delete-all + batch-append blocks |
| Batch delete | N/A | Must loop per block (no batch) |