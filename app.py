"""Extension declaration, capabilities, health check for Mixpanel Connector."""
from __future__ import annotations
import json
from imperal_sdk import ChatExtension, Extension

ext = Extension(
    "mixpanel-connector",
    version="0.1.0",
    display_name="Mixpanel",
    icon="icon.svg",
    capabilities=["mixpanel:manage"],
    description="Official Imperal connector for Mixpanel (C30. Email Marketing & Newsletter). Manage operations securely."
)

chat = ChatExtension(ext)

@ext.health_check
async def health_check(ctx) -> dict:
    raw = await ctx.secrets.get("mixpanel_connections")
    try:
        count = len(json.loads(raw)) if raw else 0
    except Exception:
        count = 0
    return {
        "healthy": True,
        "detail": f"{count} Mixpanel connection(s) configured." if count else "Not connected yet."
    }
