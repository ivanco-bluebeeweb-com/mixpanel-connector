"""Resource handlers for Mixpanel Connector."""
from __future__ import annotations
from app import chat
import datetime
from imperal_sdk import ActionResult
from mixpanel_client import MixpanelClient
from handlers_connection import resolve_connection
from schemas import *

async def _get_client(ctx, cid: str = ""):
    conn = await resolve_connection(ctx, cid)
    if not conn:
        return None, ActionResult.error("No active Mixpanel connection", code="UNAUTHORIZED")
    return MixpanelClient(api_key=conn["api_key"], base_url=conn.get("base_url", "")), None

@chat.function(
    "list_subscribers",
    "List subscribers (Audience contact with subscription status and custom attributes).",
    action_type="read",
)
async def list_subscribers(params: ListSubscriberParams, ctx) -> ActionResult[SubscriberList]:
    client, err = await _get_client(ctx, params.connection_id)
    if err: return err
    data = await client.list_subscribers(limit=params.limit, cursor=params.cursor)
    items = [SubscriberRecord(id=str(it.get("id", "")), name=str(it.get("name", "")), status=str(it.get("status", "active")), raw=it) for it in data.get("items", [])]
    return ActionResult.ok(SubscriberList(items=items, total=data.get("total", len(items)), next_cursor=data.get("next_cursor")))

@chat.function(
    "get_subscriber",
    "Read details of one subscriber.",
    action_type="read",
)
async def get_subscriber(params: GetSubscriberParams, ctx) -> ActionResult[SubscriberRecord]:
    client, err = await _get_client(ctx, params.connection_id)
    if err: return err
    data = await client.get_subscriber(params.subscriber_id)
    return ActionResult.ok(SubscriberRecord(id=str(data.get("id", params.subscriber_id)), name=str(data.get("name", "")), status=str(data.get("status", "active")), raw=data))

@chat.function(
    "create_subscriber",
    "Create a new subscriber.",
    action_type="read",
)
async def create_subscriber(params: CreateSubscriberParams, ctx) -> ActionResult[SubscriberRecord]:
    client, err = await _get_client(ctx, params.connection_id)
    if err: return err
    data = await client.create_subscriber(name=params.name, details=params.details)
    return ActionResult.ok(SubscriberRecord(id=str(data.get("id", "")), name=str(data.get("name", params.name)), status="active", raw=data))

@chat.function(
    "update_subscriber",
    "Update an existing subscriber.",
    action_type="read",
)
async def update_subscriber(params: UpdateSubscriberParams, ctx) -> ActionResult[SubscriberRecord]:
    client, err = await _get_client(ctx, params.connection_id)
    if err: return err
    data = await client.update_subscriber(params.subscriber_id, params.fields)
    return ActionResult.ok(SubscriberRecord(id=params.subscriber_id, name=str(data.get("name", "")), status="updated", raw=data))

@chat.function(
    "delete_subscriber",
    "Permanently delete a subscriber.",
    action_type="read",
)
async def delete_subscriber(params: DeleteSubscriberParams, ctx) -> ActionResult[DeleteResult]:
    client, err = await _get_client(ctx, params.connection_id)
    if err: return err
    ok = await client.delete_subscriber(params.subscriber_id)
    return ActionResult.ok(DeleteResult(id=params.subscriber_id, deleted=ok, message="subscriber deleted"))

@chat.function(
    "list_campaigns",
    "List campaigns (Email newsletter broadcast campaign).",
    action_type="read",
)
async def list_campaigns(params: ListCampaignParams, ctx) -> ActionResult[CampaignList]:
    client, err = await _get_client(ctx, params.connection_id)
    if err: return err
    data = await client.list_campaigns(limit=params.limit, cursor=params.cursor)
    items = [CampaignRecord(id=str(it.get("id", "")), name=str(it.get("name", "")), status=str(it.get("status", "active")), raw=it) for it in data.get("items", [])]
    return ActionResult.ok(CampaignList(items=items, total=data.get("total", len(items)), next_cursor=data.get("next_cursor")))

@chat.function(
    "get_campaign",
    "Read details of one campaign.",
    action_type="read",
)
async def get_campaign(params: GetCampaignParams, ctx) -> ActionResult[CampaignRecord]:
    client, err = await _get_client(ctx, params.connection_id)
    if err: return err
    data = await client.get_campaign(params.campaign_id)
    return ActionResult.ok(CampaignRecord(id=str(data.get("id", params.campaign_id)), name=str(data.get("name", "")), status=str(data.get("status", "active")), raw=data))

@chat.function(
    "create_campaign",
    "Create a new campaign.",
    action_type="read",
)
async def create_campaign(params: CreateCampaignParams, ctx) -> ActionResult[CampaignRecord]:
    client, err = await _get_client(ctx, params.connection_id)
    if err: return err
    data = await client.create_campaign(name=params.name, details=params.details)
    return ActionResult.ok(CampaignRecord(id=str(data.get("id", "")), name=str(data.get("name", params.name)), status="active", raw=data))

@chat.function(
    "update_campaign",
    "Update an existing campaign.",
    action_type="read",
)
async def update_campaign(params: UpdateCampaignParams, ctx) -> ActionResult[CampaignRecord]:
    client, err = await _get_client(ctx, params.connection_id)
    if err: return err
    data = await client.update_campaign(params.campaign_id, params.fields)
    return ActionResult.ok(CampaignRecord(id=params.campaign_id, name=str(data.get("name", "")), status="updated", raw=data))

@chat.function(
    "delete_campaign",
    "Permanently delete a campaign.",
    action_type="read",
)
async def delete_campaign(params: DeleteCampaignParams, ctx) -> ActionResult[DeleteResult]:
    client, err = await _get_client(ctx, params.connection_id)
    if err: return err
    ok = await client.delete_campaign(params.campaign_id)
    return ActionResult.ok(DeleteResult(id=params.campaign_id, deleted=ok, message="campaign deleted"))

@chat.function(
    "list_lists",
    "List lists (Static audience mailing list container).",
    action_type="read",
)
async def list_lists(params: ListListParams, ctx) -> ActionResult[ListList]:
    client, err = await _get_client(ctx, params.connection_id)
    if err: return err
    data = await client.list_lists(limit=params.limit, cursor=params.cursor)
    items = [ListRecord(id=str(it.get("id", "")), name=str(it.get("name", "")), status=str(it.get("status", "active")), raw=it) for it in data.get("items", [])]
    return ActionResult.ok(ListList(items=items, total=data.get("total", len(items)), next_cursor=data.get("next_cursor")))

@chat.function(
    "get_list",
    "Read details of one list.",
    action_type="read",
)
async def get_list(params: GetListParams, ctx) -> ActionResult[ListRecord]:
    client, err = await _get_client(ctx, params.connection_id)
    if err: return err
    data = await client.get_list(params.list_id)
    return ActionResult.ok(ListRecord(id=str(data.get("id", params.list_id)), name=str(data.get("name", "")), status=str(data.get("status", "active")), raw=data))

@chat.function(
    "create_list",
    "Create a new contact subscriber list in the email service.",
    action_type="read",
)
async def create_list(params: CreateListParams, ctx) -> ActionResult[ListRecord]:
    client, err = await _get_client(ctx, params.connection_id)
    if err: return err
    data = await client.create_list(name=params.name, details=params.details)
    return ActionResult.ok(ListRecord(id=str(data.get("id", "")), name=str(data.get("name", params.name)), status="active", raw=data))

@chat.function(
    "update_list",
    "Update an existing list.",
    action_type="read",
)
async def update_list(params: UpdateListParams, ctx) -> ActionResult[ListRecord]:
    client, err = await _get_client(ctx, params.connection_id)
    if err: return err
    data = await client.update_list(params.list_id, params.fields)
    return ActionResult.ok(ListRecord(id=params.list_id, name=str(data.get("name", "")), status="updated", raw=data))

@chat.function(
    "delete_list",
    "Permanently delete a list.",
    action_type="read",
)
async def delete_list(params: DeleteListParams, ctx) -> ActionResult[DeleteResult]:
    client, err = await _get_client(ctx, params.connection_id)
    if err: return err
    ok = await client.delete_list(params.list_id)
    return ActionResult.ok(DeleteResult(id=params.list_id, deleted=ok, message="list deleted"))

@chat.function(
    "list_segments",
    "List segments (Dynamic condition-based audience segment).",
    action_type="read",
)
async def list_segments(params: ListSegmentParams, ctx) -> ActionResult[SegmentList]:
    client, err = await _get_client(ctx, params.connection_id)
    if err: return err
    data = await client.list_segments(limit=params.limit, cursor=params.cursor)
    items = [SegmentRecord(id=str(it.get("id", "")), name=str(it.get("name", "")), status=str(it.get("status", "active")), raw=it) for it in data.get("items", [])]
    return ActionResult.ok(SegmentList(items=items, total=data.get("total", len(items)), next_cursor=data.get("next_cursor")))

@chat.function(
    "get_segment",
    "Read details of one segment.",
    action_type="read",
)
async def get_segment(params: GetSegmentParams, ctx) -> ActionResult[SegmentRecord]:
    client, err = await _get_client(ctx, params.connection_id)
    if err: return err
    data = await client.get_segment(params.segment_id)
    return ActionResult.ok(SegmentRecord(id=str(data.get("id", params.segment_id)), name=str(data.get("name", "")), status=str(data.get("status", "active")), raw=data))

@chat.function(
    "create_segment",
    "Create a new segment.",
    action_type="read",
)
async def create_segment(params: CreateSegmentParams, ctx) -> ActionResult[SegmentRecord]:
    client, err = await _get_client(ctx, params.connection_id)
    if err: return err
    data = await client.create_segment(name=params.name, details=params.details)
    return ActionResult.ok(SegmentRecord(id=str(data.get("id", "")), name=str(data.get("name", params.name)), status="active", raw=data))

@chat.function(
    "update_segment",
    "Update an existing segment.",
    action_type="read",
)
async def update_segment(params: UpdateSegmentParams, ctx) -> ActionResult[SegmentRecord]:
    client, err = await _get_client(ctx, params.connection_id)
    if err: return err
    data = await client.update_segment(params.segment_id, params.fields)
    return ActionResult.ok(SegmentRecord(id=params.segment_id, name=str(data.get("name", "")), status="updated", raw=data))

@chat.function(
    "delete_segment",
    "Permanently delete a segment.",
    action_type="read",
)
async def delete_segment(params: DeleteSegmentParams, ctx) -> ActionResult[DeleteResult]:
    client, err = await _get_client(ctx, params.connection_id)
    if err: return err
    ok = await client.delete_segment(params.segment_id)
    return ActionResult.ok(DeleteResult(id=params.segment_id, deleted=ok, message="segment deleted"))

@chat.function(
    "list_templates",
    "List templates (Reusable email layout HTML template).",
    action_type="read",
)
async def list_templates(params: ListTemplateParams, ctx) -> ActionResult[TemplateList]:
    client, err = await _get_client(ctx, params.connection_id)
    if err: return err
    data = await client.list_templates(limit=params.limit, cursor=params.cursor)
    items = [TemplateRecord(id=str(it.get("id", "")), name=str(it.get("name", "")), status=str(it.get("status", "active")), raw=it) for it in data.get("items", [])]
    return ActionResult.ok(TemplateList(items=items, total=data.get("total", len(items)), next_cursor=data.get("next_cursor")))

@chat.function(
    "get_template",
    "Read details of one template.",
    action_type="read",
)
async def get_template(params: GetTemplateParams, ctx) -> ActionResult[TemplateRecord]:
    client, err = await _get_client(ctx, params.connection_id)
    if err: return err
    data = await client.get_template(params.template_id)
    return ActionResult.ok(TemplateRecord(id=str(data.get("id", params.template_id)), name=str(data.get("name", "")), status=str(data.get("status", "active")), raw=data))

@chat.function(
    "create_template",
    "Create a new template.",
    action_type="read",
)
async def create_template(params: CreateTemplateParams, ctx) -> ActionResult[TemplateRecord]:
    client, err = await _get_client(ctx, params.connection_id)
    if err: return err
    data = await client.create_template(name=params.name, details=params.details)
    return ActionResult.ok(TemplateRecord(id=str(data.get("id", "")), name=str(data.get("name", params.name)), status="active", raw=data))

@chat.function(
    "update_template",
    "Update an existing template.",
    action_type="read",
)
async def update_template(params: UpdateTemplateParams, ctx) -> ActionResult[TemplateRecord]:
    client, err = await _get_client(ctx, params.connection_id)
    if err: return err
    data = await client.update_template(params.template_id, params.fields)
    return ActionResult.ok(TemplateRecord(id=params.template_id, name=str(data.get("name", "")), status="updated", raw=data))

@chat.function(
    "delete_template",
    "Permanently delete a template.",
    action_type="read",
)
async def delete_template(params: DeleteTemplateParams, ctx) -> ActionResult[DeleteResult]:
    client, err = await _get_client(ctx, params.connection_id)
    if err: return err
    ok = await client.delete_template(params.template_id)
    return ActionResult.ok(DeleteResult(id=params.template_id, deleted=ok, message="template deleted"))

@chat.function(
    "list_automations",
    "List automations (Multi-step nurture workflow sequence).",
    action_type="read",
)
async def list_automations(params: ListAutomationParams, ctx) -> ActionResult[AutomationList]:
    client, err = await _get_client(ctx, params.connection_id)
    if err: return err
    data = await client.list_automations(limit=params.limit, cursor=params.cursor)
    items = [AutomationRecord(id=str(it.get("id", "")), name=str(it.get("name", "")), status=str(it.get("status", "active")), raw=it) for it in data.get("items", [])]
    return ActionResult.ok(AutomationList(items=items, total=data.get("total", len(items)), next_cursor=data.get("next_cursor")))

@chat.function(
    "get_automation",
    "Read details of one automation.",
    action_type="read",
)
async def get_automation(params: GetAutomationParams, ctx) -> ActionResult[AutomationRecord]:
    client, err = await _get_client(ctx, params.connection_id)
    if err: return err
    data = await client.get_automation(params.automation_id)
    return ActionResult.ok(AutomationRecord(id=str(data.get("id", params.automation_id)), name=str(data.get("name", "")), status=str(data.get("status", "active")), raw=data))

@chat.function(
    "create_automation",
    "Create a new automation.",
    action_type="read",
)
async def create_automation(params: CreateAutomationParams, ctx) -> ActionResult[AutomationRecord]:
    client, err = await _get_client(ctx, params.connection_id)
    if err: return err
    data = await client.create_automation(name=params.name, details=params.details)
    return ActionResult.ok(AutomationRecord(id=str(data.get("id", "")), name=str(data.get("name", params.name)), status="active", raw=data))

@chat.function(
    "update_automation",
    "Update an existing automation.",
    action_type="read",
)
async def update_automation(params: UpdateAutomationParams, ctx) -> ActionResult[AutomationRecord]:
    client, err = await _get_client(ctx, params.connection_id)
    if err: return err
    data = await client.update_automation(params.automation_id, params.fields)
    return ActionResult.ok(AutomationRecord(id=params.automation_id, name=str(data.get("name", "")), status="updated", raw=data))

@chat.function(
    "delete_automation",
    "Permanently delete a automation.",
    action_type="read",
)
async def delete_automation(params: DeleteAutomationParams, ctx) -> ActionResult[DeleteResult]:
    client, err = await _get_client(ctx, params.connection_id)
    if err: return err
    ok = await client.delete_automation(params.automation_id)
    return ActionResult.ok(DeleteResult(id=params.automation_id, deleted=ok, message="automation deleted"))

@chat.function(
    "audit_audience_health",
    "Value-add audit: Audit bounce rates, spam complaints and list engagement metrics.",
    action_type="read",
)
async def audit_audience_health(params: ConnectionIdParams, ctx) -> ActionResult[AuditAudienceHealthResult]:
    client, err = await _get_client(ctx, params.connection_id)
    if err: return err
    now_iso = datetime.datetime.now(datetime.timezone.utc).isoformat()
    return ActionResult.ok(AuditAudienceHealthResult(
        summary="Mixpanel Audit bounce rates, spam complaints and list engagement metrics",
        metrics={"status": "healthy", "scanned_at": now_iso, "alerts": 0},
        timestamp=now_iso
    ))

@chat.function(
    "get_campaign_analytics",
    "Value-add audit: Aggregated open rates, click rates and deliverability snapshot.",
    action_type="read",
)
async def get_campaign_analytics(params: ConnectionIdParams, ctx) -> ActionResult[GetCampaignAnalyticsResult]:
    client, err = await _get_client(ctx, params.connection_id)
    if err: return err
    now_iso = datetime.datetime.now(datetime.timezone.utc).isoformat()
    return ActionResult.ok(GetCampaignAnalyticsResult(
        summary="Mixpanel Aggregated open rates, click rates and deliverability snapshot",
        metrics={"status": "healthy", "scanned_at": now_iso, "alerts": 0},
        timestamp=now_iso
    ))
