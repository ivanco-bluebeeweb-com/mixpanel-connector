"""HTTP client for Mixpanel API."""
from __future__ import annotations
import httpx
import time
from typing import Any, Optional

DEFAULT_INGEST_BASE = "https://api.mixpanel.com"
DEFAULT_QUERY_BASE = "https://mixpanel.com/api/2.0"

class MixpanelClient:
    def __init__(
        self,
        project_token: str,
        api_secret: str = "",
        project_id: str = "",
        base_url: str = ""
    ):
        self.project_token = project_token.strip()
        self.api_secret = api_secret.strip()
        self.project_id = project_id.strip()
        self.base_url = (base_url.strip() if base_url else DEFAULT_INGEST_BASE).rstrip("/")
        self.query_base = DEFAULT_QUERY_BASE
        self.timeout = httpx.Timeout(30.0, connect=10.0)

    async def verify_auth(self) -> dict[str, Any]:
        """Verify token and credentials against Mixpanel APIs."""
        if not self.project_token:
            return {"status": "error", "error": "Mixpanel project_token is required."}

        # 1. Ingestion test ping
        ingestion_ok = False
        ingestion_details = {}
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                resp = await client.post(
                    f"{self.base_url}/track",
                    params={"verbose": "1"},
                    json=[{
                        "event": "$ping",
                        "properties": {
                            "token": self.project_token,
                            "distinct_id": "imperal_verification",
                            "time": int(time.time()),
                            "mp_lib": "imperal_connector"
                        }
                    }]
                )
                if resp.status_code == 200:
                    data = resp.json() if resp.content else {}
                    ingestion_ok = data.get("status") == 1
                    ingestion_details = data
                else:
                    ingestion_details = {"error": f"HTTP {resp.status_code}: {resp.text}"}
            except Exception as e:
                ingestion_details = {"error": str(e)}

        # 2. Query API access check (if secret is provided)
        query_status = "unconfigured"
        if self.api_secret:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                try:
                    params: dict[str, Any] = {"type": "general"}
                    if self.project_id:
                        params["project_id"] = self.project_id
                    q_resp = await client.get(
                        f"{self.query_base}/events/names",
                        auth=(self.api_secret, ""),
                        params=params
                    )
                    if q_resp.status_code == 200:
                        query_status = "ok"
                    elif q_resp.status_code == 402:
                        query_status = "plan_upgrade_required"
                    else:
                        query_status = f"HTTP_{q_resp.status_code}"
                except Exception as e:
                    query_status = f"error: {e}"

        if ingestion_ok:
            return {
                "status": "ok",
                "ingestion": "operational",
                "query_api": query_status,
                "project_id": self.project_id or None
            }
        return {
            "status": "error",
            "error": "Failed to verify event ingestion against Mixpanel.",
            "details": ingestion_details
        }

    async def list_events(self, limit: int = 20) -> list[dict[str, Any]]:
        """List event names through Mixpanel Query API when entitlement is available."""
        if not self.api_secret:
            raise PermissionError("Mixpanel API Secret is required to read events. Event ingestion is operational with Project Token.")

        async with httpx.AsyncClient(timeout=self.timeout) as client:
            params: dict[str, Any] = {"type": "general"}
            if self.project_id:
                params["project_id"] = self.project_id
            resp = await client.get(
                f"{self.query_base}/events/names",
                auth=(self.api_secret, ""),
                params=params
            )
            if resp.status_code == 200:
                data = resp.json()
                if isinstance(data, list):
                    return [{"id": name, "name": name, "status": "active"} for name in data[:limit]]
                return []
            if resp.status_code == 402:
                raise PermissionError("Mixpanel Query API returned HTTP 402 (Plan does not allow API calls). Upgrade Mixpanel plan to enable event reads; Project Token ingestion remains operational.")
            raise ValueError(f"Mixpanel event query failed: HTTP {resp.status_code}: {resp.text}")

    async def get_event(self, event_id: str) -> dict[str, Any]:
        """Retrieve one event from the accessible Mixpanel event catalogue."""
        events = await self.list_events(limit=100)
        event = next((item for item in events if item["name"] == event_id or item["id"] == event_id), None)
        if not event:
            raise ValueError(f"Event '{event_id}' was not found in the Mixpanel event catalogue.")
        return event
