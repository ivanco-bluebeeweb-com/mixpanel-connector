"""Connection management for Mixpanel Connector."""
from __future__ import annotations
import uuid
from typing import Any
from imperal_sdk import ActionResult
from app import chat
from schemas import NoParams, ConnectParams, ConnectionIdParams, ConnectionRecord, ConnectionList, DeleteResult
from mixpanel_connector_client import MixpanelClient

def _mask(v: str) -> str:
    if not v:
        return ""
    if len(v) <= 8:
        return "*" * len(v)
    return v[:4] + "*" * (len(v) - 8) + v[-4:]

async def get_connections_list(ctx) -> list[dict]:
    page = await ctx.store.query("connections")
    docs = page.data if hasattr(page, "data") else []
    conns = []
    for d in docs:
        data = d.data if hasattr(d, "data") else d
        doc_id = d.id if hasattr(d, "id") else data.get("id")
        data["_store_id"] = doc_id
        conns.append(data)
    return conns

async def resolve_client(ctx, connection_id: str = "") -> MixpanelClient:
    conns = await get_connections_list(ctx)
    if not conns:
        raise ValueError("No Mixpanel connections configured. Use connect_mixpanel_connector first.")
    conn = None
    if connection_id:
        for c in conns:
            if c.get("id") == connection_id:
                conn = c
                break
        if not conn:
            raise ValueError(f"Connection {connection_id} not found.")
    else:
        conn = conns[0]
    return MixpanelClient(
        project_token=conn.get("project_token", ""),
        api_secret=conn.get("api_secret", ""),
        project_id=conn.get("project_id", ""),
        base_url=conn.get("base_url", "")
    )

@chat.function("connect_mixpanel_connector", "Connect Mixpanel account via credentials.", action_type="write", chain_callable=True, event="mixpanel-connector.connect_mixpanel_connector", effects=["create:connection"], data_model=ConnectionRecord)
async def connect_mixpanel_connector(params: ConnectParams, ctx) -> ActionResult:
    client = MixpanelClient(
        project_token=params.project_token,
        api_secret=params.api_secret or "",
        project_id=params.project_id or "",
        base_url=params.base_url
    )
    res = await client.verify_auth()
    if res.get("status") == "error":
        return ActionResult.error(f"Failed to connect to Mixpanel: {res.get('error')}")

    cid = f"conn_{uuid.uuid4().hex[:8]}"
    rec = {
        "id": cid,
        "label": params.label or "Primary Mixpanel",
        "project_token": params.project_token,
        "api_secret": params.api_secret or "",
        "project_id": params.project_id or "",
        "masked_token": _mask(params.project_token),
        "base_url": params.base_url,
        "is_active": True
    }

    conns = await get_connections_list(ctx)
    for c in conns:
        if c.get("is_active"):
            c["is_active"] = False
            sid = c.get("_store_id")
            if sid:
                c_clean = {k: v for k, v in c.items() if not k.startswith("_")}
                await ctx.store.create("connections", c_clean, id=sid)

    await ctx.store.create("connections", rec, id=cid)
    out = {
        "id": rec["id"],
        "label": rec["label"],
        "masked_token": rec["masked_token"],
        "project_id": rec["project_id"],
        "base_url": rec["base_url"],
        "is_active": rec["is_active"]
    }
    return ActionResult.success(out, summary=f"Connected Mixpanel ({rec['label']}).")

@chat.function("list_connections", "List configured Mixpanel connections.", action_type="read", chain_callable=True, event="mixpanel-connector.list_connections", effects=["read:connections"], data_model=ConnectionList)
async def list_connections(params: NoParams, ctx) -> ActionResult:
    conns = await get_connections_list(ctx)
    items = [{
        "id": c.get("id"),
        "label": c.get("label", "Primary Mixpanel"),
        "masked_token": c.get("masked_token") or _mask(c.get("project_token", "")),
        "project_id": c.get("project_id"),
        "base_url": c.get("base_url", "https://api.mixpanel.com"),
        "is_active": c.get("is_active", False)
    } for c in conns]
    return ActionResult.success({"connections": items, "total": len(items)}, summary=f"Found {len(items)} connection(s).")

@chat.function("disconnect_mixpanel_connector", "Disconnect Mixpanel account and delete stored credentials.", action_type="destructive", chain_callable=True, event="mixpanel-connector.disconnect_mixpanel_connector", effects=["delete:connection"], data_model=DeleteResult)
async def disconnect_mixpanel_connector(params: ConnectionIdParams, ctx) -> ActionResult:
    conns = await get_connections_list(ctx)
    if not conns:
        return ActionResult.error("No connections to disconnect.")
    if params.connection_id:
        target = next((c for c in conns if c.get("id") == params.connection_id), None)
        if not target:
            return ActionResult.error(f"Connection {params.connection_id} not found.")
        sid = target.get("_store_id") or target.get("id")
        await ctx.store.delete("connections", sid)
    else:
        for c in conns:
            sid = c.get("_store_id") or c.get("id")
            await ctx.store.delete("connections", sid)
    return ActionResult.success({"success": True, "message": "Disconnected successfully."}, summary="Disconnected Mixpanel connection.")
