"""Pydantic schemas for Mixpanel Connector."""
from __future__ import annotations
from typing import Any, Optional, List, Dict
from pydantic import BaseModel, Field

class NoParams(BaseModel):
    """Empty parameters model."""
    pass

class ConnectParams(BaseModel):
    label: str = Field(default="", description="Friendly connection label, e.g. Primary Mixpanel.")
    api_key: str = Field(description="API Key / Project Token")
    base_url: str = Field(default="https://mixpanel.com/api/2.0", description="Mixpanel API base URL.")

class ConnectionIdParams(BaseModel):
    connection_id: str = Field(default="", description="Connection identifier (empty uses active connection).")

class ConnectionRecord(BaseModel):
    id: str
    label: str
    masked_key: str
    base_url: str
    is_active: bool

class ConnectionList(BaseModel):
    connections: list[ConnectionRecord]
    total: int

class DeleteResult(BaseModel):
    success: bool
    message: str

class EventRecord(BaseModel):
    id: str
    name: Optional[str] = None
    status: Optional[str] = None
    created_at: Optional[str] = None
    raw: Dict[str, Any] = Field(default_factory=dict)

class EventList(BaseModel):
    events: list[EventRecord]
    total: int

class ListEventParams(BaseModel):
    connection_id: str = Field(default="", description="Optional connection ID.")
    limit: int = Field(default=20, ge=1, le=100, description="Max records to return.")

class GetEventParams(BaseModel):
    connection_id: str = Field(default="", description="Optional connection ID.")
    event_id: str = Field(description="Mixpanel Event ID.")

class AuditHealthReport(BaseModel):
    healthy: bool
    total_events: int
    details: Dict[str, Any] = Field(default_factory=dict)
    summary: str
