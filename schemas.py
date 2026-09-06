"""Pydantic schemas for Mixpanel Connector (C30. Email Marketing & Newsletter)."""
from __future__ import annotations
from typing import Any, Optional
from pydantic import BaseModel, Field

class ConnectParams(BaseModel):
    label: str = Field(default="", description="Friendly connection label, e.g. Acme Mixpanel.")
    api_key: str = Field(description="Marketing API Key or Bearer Token.")
    base_url: str = Field(default="", description="Optional custom base URL or instance domain.")

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
    id: str
    deleted: bool
    message: str

class ListSubscriberParams(BaseModel):
    connection_id: str = Field(default="", description="Connection identifier.")
    limit: int = Field(default=50, description="Max records to return (1-100).")
    cursor: str = Field(default="", description="Pagination cursor or page token.")

class GetSubscriberParams(BaseModel):
    connection_id: str = Field(default="", description="Connection identifier.")
    subscriber_id: str = Field(description="Unique identifier of the subscriber.")

class CreateSubscriberParams(BaseModel):
    connection_id: str = Field(default="", description="Connection identifier.")
    name: str = Field(description="Name or title of the record.")
    details: Optional[dict[str, Any]] = Field(default=None, description="Detailed attributes and payload.")

class UpdateSubscriberParams(BaseModel):
    connection_id: str = Field(default="", description="Connection identifier.")
    subscriber_id: str = Field(description="Unique identifier of the subscriber.")
    fields: dict[str, Any] = Field(description="Attributes to update.")

class DeleteSubscriberParams(BaseModel):
    connection_id: str = Field(default="", description="Connection identifier.")
    subscriber_id: str = Field(description="Unique identifier of the subscriber.")

class SubscriberRecord(BaseModel):
    id: str
    name: str
    status: str = "active"
    raw: dict[str, Any] = {}

class SubscriberList(BaseModel):
    items: list[SubscriberRecord]
    total: int
    next_cursor: Optional[str] = None

class ListCampaignParams(BaseModel):
    connection_id: str = Field(default="", description="Connection identifier.")
    limit: int = Field(default=50, description="Max records to return (1-100).")
    cursor: str = Field(default="", description="Pagination cursor or page token.")

class GetCampaignParams(BaseModel):
    connection_id: str = Field(default="", description="Connection identifier.")
    campaign_id: str = Field(description="Unique identifier of the campaign.")

class CreateCampaignParams(BaseModel):
    connection_id: str = Field(default="", description="Connection identifier.")
    name: str = Field(description="Name or title of the record.")
    details: Optional[dict[str, Any]] = Field(default=None, description="Detailed attributes and payload.")

class UpdateCampaignParams(BaseModel):
    connection_id: str = Field(default="", description="Connection identifier.")
    campaign_id: str = Field(description="Unique identifier of the campaign.")
    fields: dict[str, Any] = Field(description="Attributes to update.")

class DeleteCampaignParams(BaseModel):
    connection_id: str = Field(default="", description="Connection identifier.")
    campaign_id: str = Field(description="Unique identifier of the campaign.")

class CampaignRecord(BaseModel):
    id: str
    name: str
    status: str = "active"
    raw: dict[str, Any] = {}

class CampaignList(BaseModel):
    items: list[CampaignRecord]
    total: int
    next_cursor: Optional[str] = None

class ListListParams(BaseModel):
    connection_id: str = Field(default="", description="Connection identifier.")
    limit: int = Field(default=50, description="Max records to return (1-100).")
    cursor: str = Field(default="", description="Pagination cursor or page token.")

class GetListParams(BaseModel):
    connection_id: str = Field(default="", description="Connection identifier.")
    list_id: str = Field(description="Unique identifier of the list.")

class CreateListParams(BaseModel):
    connection_id: str = Field(default="", description="Connection identifier.")
    name: str = Field(description="Name or title of the record.")
    details: Optional[dict[str, Any]] = Field(default=None, description="Detailed attributes and payload.")

class UpdateListParams(BaseModel):
    connection_id: str = Field(default="", description="Connection identifier.")
    list_id: str = Field(description="Unique identifier of the list.")
    fields: dict[str, Any] = Field(description="Attributes to update.")

class DeleteListParams(BaseModel):
    connection_id: str = Field(default="", description="Connection identifier.")
    list_id: str = Field(description="Unique identifier of the list.")

class ListRecord(BaseModel):
    id: str
    name: str
    status: str = "active"
    raw: dict[str, Any] = {}

class ListList(BaseModel):
    items: list[ListRecord]
    total: int
    next_cursor: Optional[str] = None

class ListSegmentParams(BaseModel):
    connection_id: str = Field(default="", description="Connection identifier.")
    limit: int = Field(default=50, description="Max records to return (1-100).")
    cursor: str = Field(default="", description="Pagination cursor or page token.")

class GetSegmentParams(BaseModel):
    connection_id: str = Field(default="", description="Connection identifier.")
    segment_id: str = Field(description="Unique identifier of the segment.")

class CreateSegmentParams(BaseModel):
    connection_id: str = Field(default="", description="Connection identifier.")
    name: str = Field(description="Name or title of the record.")
    details: Optional[dict[str, Any]] = Field(default=None, description="Detailed attributes and payload.")

class UpdateSegmentParams(BaseModel):
    connection_id: str = Field(default="", description="Connection identifier.")
    segment_id: str = Field(description="Unique identifier of the segment.")
    fields: dict[str, Any] = Field(description="Attributes to update.")

class DeleteSegmentParams(BaseModel):
    connection_id: str = Field(default="", description="Connection identifier.")
    segment_id: str = Field(description="Unique identifier of the segment.")

class SegmentRecord(BaseModel):
    id: str
    name: str
    status: str = "active"
    raw: dict[str, Any] = {}

class SegmentList(BaseModel):
    items: list[SegmentRecord]
    total: int
    next_cursor: Optional[str] = None

class ListTemplateParams(BaseModel):
    connection_id: str = Field(default="", description="Connection identifier.")
    limit: int = Field(default=50, description="Max records to return (1-100).")
    cursor: str = Field(default="", description="Pagination cursor or page token.")

class GetTemplateParams(BaseModel):
    connection_id: str = Field(default="", description="Connection identifier.")
    template_id: str = Field(description="Unique identifier of the template.")

class CreateTemplateParams(BaseModel):
    connection_id: str = Field(default="", description="Connection identifier.")
    name: str = Field(description="Name or title of the record.")
    details: Optional[dict[str, Any]] = Field(default=None, description="Detailed attributes and payload.")

class UpdateTemplateParams(BaseModel):
    connection_id: str = Field(default="", description="Connection identifier.")
    template_id: str = Field(description="Unique identifier of the template.")
    fields: dict[str, Any] = Field(description="Attributes to update.")

class DeleteTemplateParams(BaseModel):
    connection_id: str = Field(default="", description="Connection identifier.")
    template_id: str = Field(description="Unique identifier of the template.")

class TemplateRecord(BaseModel):
    id: str
    name: str
    status: str = "active"
    raw: dict[str, Any] = {}

class TemplateList(BaseModel):
    items: list[TemplateRecord]
    total: int
    next_cursor: Optional[str] = None

class ListAutomationParams(BaseModel):
    connection_id: str = Field(default="", description="Connection identifier.")
    limit: int = Field(default=50, description="Max records to return (1-100).")
    cursor: str = Field(default="", description="Pagination cursor or page token.")

class GetAutomationParams(BaseModel):
    connection_id: str = Field(default="", description="Connection identifier.")
    automation_id: str = Field(description="Unique identifier of the automation.")

class CreateAutomationParams(BaseModel):
    connection_id: str = Field(default="", description="Connection identifier.")
    name: str = Field(description="Name or title of the record.")
    details: Optional[dict[str, Any]] = Field(default=None, description="Detailed attributes and payload.")

class UpdateAutomationParams(BaseModel):
    connection_id: str = Field(default="", description="Connection identifier.")
    automation_id: str = Field(description="Unique identifier of the automation.")
    fields: dict[str, Any] = Field(description="Attributes to update.")

class DeleteAutomationParams(BaseModel):
    connection_id: str = Field(default="", description="Connection identifier.")
    automation_id: str = Field(description="Unique identifier of the automation.")

class AutomationRecord(BaseModel):
    id: str
    name: str
    status: str = "active"
    raw: dict[str, Any] = {}

class AutomationList(BaseModel):
    items: list[AutomationRecord]
    total: int
    next_cursor: Optional[str] = None

class AuditAudienceHealthResult(BaseModel):
    summary: str
    metrics: dict[str, Any]
    timestamp: str

class GetCampaignAnalyticsResult(BaseModel):
    summary: str
    metrics: dict[str, Any]
    timestamp: str


class NoParams(BaseModel):
    """Empty parameter model."""
    pass
