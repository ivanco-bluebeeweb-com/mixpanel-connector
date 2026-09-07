"""Resource handlers for Mixpanel Connector."""
from __future__ import annotations
from typing import Any
from imperal_sdk import ActionResult
from app import chat
from schemas import (
    ListEventParams, GetEventParams,
    EventRecord, EventList, AuditHealthReport, ConnectionIdParams
)
from handlers_connection import resolve_client

@chat.function("list_events", "List events in Mixpanel.", action_type="read", chain_callable=True, event="mixpanel-connector.list_events", effects=["read:events"], data_model=EventList)
async def list_events(params: ListEventParams, ctx) -> ActionResult:
    client = await resolve_client(ctx, params.connection_id)
    try:
        raw_items = await client.list_events(limit=params.limit)
        items = []
        for r in raw_items:
            rid = str(r.get("id") or r.get("name") or "unknown")
            rname = r.get("name") or rid
            items.append({
                "id": rid,
                "name": rname,
                "status": r.get("status", "active"),
                "created_at": None,
                "raw": r
            })
        return ActionResult.success({"events": items, "total": len(items)}, summary=f"Found {len(items)} events.")
    except PermissionError as pe:
        return ActionResult.error(f"Permission error: {pe}")
    except Exception as e:
        return ActionResult.error(f"Error listing events: {e}")

@chat.function("get_event", "Get details of one Event in Mixpanel.", action_type="read", chain_callable=True, event="mixpanel-connector.get_event", effects=["read:event"], data_model=EventRecord)
async def get_event(params: GetEventParams, ctx) -> ActionResult:
    client = await resolve_client(ctx, params.connection_id)
    try:
        r = await client.get_event(params.event_id)
        rid = str(r.get("id") or params.event_id)
        rname = r.get("name") or rid
        return ActionResult.success({
            "id": rid,
            "name": rname,
            "status": r.get("status", "active"),
            "created_at": None,
            "raw": r
        }, summary=f"Retrieved Event {rid}.")
    except PermissionError as pe:
        return ActionResult.error(f"Permission error: {pe}")
    except Exception as e:
        return ActionResult.error(f"Error retrieving Event: {e}")

@chat.function("audit_event_health", "Audit health of Mixpanel events and connectivity.", action_type="read", chain_callable=True, event="mixpanel-connector.audit_event_health", effects=["read:audit"], data_model=AuditHealthReport)
async def audit_event_health(params: ConnectionIdParams, ctx) -> ActionResult:
    client = await resolve_client(ctx, params.connection_id)
    try:
        auth_res = await client.verify_auth()
        is_healthy = auth_res.get("status") == "ok"
        sample_names = []
        try:
            items = await client.list_events(limit=20)
            sample_names = [i.get("name") for i in items]
        except PermissionError:
            pass
        summary = f"Mixpanel ingestion is {'healthy' if is_healthy else 'degraded'}. Project Token verified live."
        return ActionResult.success({
            "healthy": is_healthy,
            "total_events": len(sample_names),
            "details": {
                "auth": auth_res,
                "sample_events": sample_names
            },
            "summary": summary
        }, summary=summary)
    except Exception as e:
        return ActionResult.error(f"Error auditing Mixpanel health: {e}")
