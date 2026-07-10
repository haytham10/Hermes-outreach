"""Audit all leads in Audit Ready or Outreach Sent for stale Gmail drafts."""
import json, os, re, requests as r

CONFIG_PATH = os.path.join(
    os.environ.get("LOCALAPPDATA", os.path.expanduser("~/.hermes")),
    "hermes", "config.yaml",
)
DB_ID = "78b26ebe-5b4f-4ff2-884a-3ccf369d00e6"

with open(CONFIG_PATH) as f:
    c = f.read()
token = re.search(r"NOTION_TOKEN:\s*(\S+)", c).group(1)
h = {"Authorization": f"Bearer {token}", "Content-Type": "application/json", "Notion-Version": "2022-06-28"}

# Query for Audit Ready + Outreach Sent
resp = r.post(f"https://api.notion.com/v1/databases/{DB_ID}/query", headers=h, json={
    "filter": {
        "or": [
            {"property": "Status", "select": {"equals": "Audit Ready"}},
            {"property": "Status", "select": {"equals": "Outreach Sent"}},
        ]
    },
    "sorts": [{"property": "Last Update", "direction": "descending"}]
})
data = resp.json()
results = data.get("results", [])
print(f"Total leads in Audit Ready or Outreach Sent: {len(results)}\n")

for r2 in results:
    p = r2["id"]
    props = r2["properties"]
    name = "".join(t.get("text",{}).get("content","") for t in props.get("Contact Name",{}).get("title",[]))
    status = (props.get("Status",{}).get("select") or {}).get("name","")
    email = props.get("Email",{}).get("email") or ""
    touch = props.get("Touch #",{}).get("number") or "—"
    print(f"  {name:<30} | Status: {status:<15} | Touch #{touch} | Email: {email}")
    if email:
        print(f"  {'':>30} | Page ID: {p}")