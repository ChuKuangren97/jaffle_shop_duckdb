import os
import asyncio
import requests
from fastmcp import Client

GITHUB_TOKEN = os.environ["GITHUB_TOKEN"]
REPO = os.environ["REPO"]
PR_NUMBER = os.environ["PR_NUMBER"]
GMS_URL = os.environ["DATAHUB_GMS_URL"]

HEADERS = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Accept": "application/vnd.github+json",
}

def get_changed_files():
    url = f"https://api.github.com/repos/{REPO}/pulls/{PR_NUMBER}/files"
    resp = requests.get(url, headers=HEADERS)
    resp.raise_for_status()
    return [f["filename"] for f in resp.json()]

def extract_table_names(files):
    tables = []
    for f in files:
        if f.startswith("models/") and f.endswith(".sql"):
            tables.append(f.split("/")[-1].replace(".sql", ""))
    return tables

def build_urn(table_name):
    return f"urn:li:dataset:(urn:li:dataPlatform:dbt,jaffle_shop.main.{table_name},PROD)"

async def get_downstream(table_name):
    config = {
        "mcpServers": {
            "datahub": {
                "command": "mcp-server-datahub",
                "env": {"DATAHUB_GMS_URL": GMS_URL}
            }
        }
    }
    async with Client(config) as client:
        result = await client.call_tool("get_lineage", {
            "urn": build_urn(table_name),
            "upstream": False,
            "max_hops": 2
        })
        return result.data

async def tag_reviewed(urn):
    config = {
        "mcpServers": {
            "datahub": {
                "command": "mcp-server-datahub",
                "env": {
                    "DATAHUB_GMS_URL": GMS_URL,
                    "TOOLS_IS_MUTATION_ENABLED": "true"
                }
            }
        }
    }
    async with Client(config) as client:
        await client.call_tool("add_tags", {
            "tag_urns": ["urn:li:tag:break-predictor-reviewed"],
            "entity_urns": [urn]
        })

def format_comment(table_name, lineage_data):
    downstreams = lineage_data.get("downstreams", {}).get("searchResults", [])

    real_downstreams = [
        d for d in downstreams
        if table_name.lower() not in d["entity"].get("name", "").lower()
    ]

    if not real_downstreams:
        return f"✅ **Cross-Domain Break Predictor**: No downstream dependents found for `{table_name}`. This change looks low-risk."

    lines = [f"⚠️ **Cross-Domain Break Predictor**: `{table_name}` has {len(real_downstreams)} downstream dependent(s):\n"]
    for d in real_downstreams:
        entity = d["entity"]
        name = entity.get("name", "unknown")
        owners = entity.get("ownership", {}).get("owners", [])
        owner_names = [
            o["owner"]["properties"]["displayName"]
            for o in owners
            if "properties" in o.get("owner", {})
        ]
        owner_str = ", ".join(owner_names) if owner_names else "no listed owner"
        lines.append(f"- **{name}** (owner: {owner_str})")
