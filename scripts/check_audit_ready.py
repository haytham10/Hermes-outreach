"""Check only Audit Ready leads with drafts."""
import json, os, re, requests as r

CONFIG_PATH = os.path.join(os.environ.get("LOCALAPPDATA", os.path.expanduser("~/.hermes")), "hermes", "config.yaml")
DB_ID = "78b26ebe-5b4f-4ff2-884a-3ccf369d00e6"

with open(CONFIG_PATH) as f:
    c = f.read()
token = re.search(r"NOTION_TOKEN:\s*(\S+)", c).group(1)
h = {"Authorization": f"Bearer {token}", "Content-Type": "application/json", "Notion-Version": "2022-06-28"}

resp = r.post(f"https://api.notion.com/v1/databases/{DB_ID}/query", headers=h, json={
    "filter": {"property": "Status", "select": {"equals": "Audit Ready"}},
})
results = resp.json().get("results", [])
for r2 in results:
    props = r2["properties"]
    name = "".join(t.get("text",{}).get("content","") for t in props.get("Contact Name",{}).get("title",[]))
    email = props.get("Email",{}).get("email") or "no email"
    site = props.get("Site URL",{}).get("url") or ""
    touch = props.get("Touch #",{}).get("number") or "—"
    print(f"{name:<30} | {email:<35} | Touch #{touch:<3} | {site}")