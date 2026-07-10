"""Query the Notion Lead Pipeline database for leads in Researching status."""
import json
import re
import requests

import os

CONFIG_PATH = os.path.join(
    os.environ.get("LOCALAPPDATA", os.path.expanduser("~/.hermes")),
    "hermes",
    "config.yaml",
)
DATABASE_ID = "78b26ebe-5b4f-4ff2-884a-3ccf369d00e6"

def get_token():
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        content = f.read()
    m = re.search(r"NOTION_TOKEN:\s*(\S+)", content)
    if m:
        return m.group(1)
    raise ValueError("NOTION_TOKEN not found in config")

token = get_token()

headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28",
}

# Query the database for Researching status
payload = {
    "filter": {
        "property": "Status",
        "select": {"equals": "Researching"}
    }
}

resp = requests.post(
    f"https://api.notion.com/v1/databases/{DATABASE_ID}/query",
    headers=headers,
    json=payload,
)

print(f"Status: {resp.status_code}")
data = resp.json()

if resp.status_code != 200:
    print(f"Error: {json.dumps(data, indent=2)}")
else:
    results = data.get("results", [])
    print(f"Found {len(results)} leads in Researching status")
    for r in results:
        props = r.get("properties", {})
        name = ""
        if "Contact Name" in props:
            name_obj = props["Contact Name"]
            if name_obj.get("type") == "title":
                name = name_obj.get("title", [{}])[0].get("text", {}).get("content", "")
        site_url = ""
        if "Site URL" in props:
            site_url = props["Site URL"].get("url") or ""
        profile_url = ""
        if "Profile URL" in props:
            profile_url = props["Profile URL"].get("url") or ""
        
        print(f"\n  Name: {name}")
        print(f"  Page ID: {r['id']}")
        print(f"  Site URL: {site_url}")
        print(f"  Profile URL: {profile_url}")
        # Print all properties
        for prop_name, prop_data in props.items():
            ptype = prop_data.get("type", "")
            value = "?"
            if ptype == "title":
                titles = prop_data.get("title", [])
                value = titles[0].get("text", {}).get("content", "") if titles else ""
            elif ptype == "rich_text":
                texts = prop_data.get("rich_text", [])
                value = texts[0].get("text", {}).get("content", "") if texts else ""
            elif ptype == "select":
                sel = prop_data.get("select")
                value = sel.get("name", "") if sel else ""
            elif ptype == "multi_select":
                value = ", ".join(item.get("name", "") for item in prop_data.get("multi_select", []))
            elif ptype == "url":
                value = prop_data.get("url") or ""
            elif ptype == "number":
                value = prop_data.get("number") or ""
            elif ptype == "date":
                d = prop_data.get("date")
                value = d.get("start", "") if d else ""
            elif ptype == "email":
                value = prop_data.get("email") or ""
            elif ptype == "status":
                st = prop_data.get("status")
                value = st.get("name", "") if st else ""
            elif ptype == "phone_number":
                value = prop_data.get("phone_number") or ""
            else:
                value = f"<{ptype}>"
            print(f"    {prop_name}: {value}")
        print()