# Mixpanel Connector — Executed Validation Evidence

**Target:** Mixpanel Ingestion API & Query API (`https://api.mixpanel.com`, `https://mixpanel.com/api/2.0`)  
**Date:** 2026-09-07  
**Credentials:** Mixpanel Project Token (`f0a2...`) and API Secret (`d6fa...`) obtained via real Google Chrome registration and onboarding for organisation `Bluebeeweb` (Project ID `4061542`).

## Part A — Authentication and Connection Lifecycle

| Scenario | Result | Evidence |
|---|---|---|
| A1: Ingestion API Token Validation | Passed | Live `POST https://api.mixpanel.com/track` with project token returned HTTP 200 (`status: 1, error: null`). |
| A2: Connect Lifecycle | Passed | `connect_mixpanel_connector` validated ingestion, persisted connection to Document store (`ctx.store`), and returned masked token with asterisks (`f0a2************************aff8`). |
| A3: List Connections | Passed | `list_connections` retrieved 1 configured connection with accurate metadata and masked token. |
| A4: Disconnect Lifecycle | Passed | `disconnect_mixpanel_connector` deleted the connection from Document store; subsequent listing returned 0 connections. |

## Part B — Live Event Tracking & Ingestion (CRUD Write)

| Scenario | Result | Evidence |
|---|---|---|
| B1: Track Event (`/track`) | Passed | Ingested live event `imperal_connector_live_test` with distinct ID `vlad@bluebeeweb.com` and custom properties. Received HTTP 200 `{"status": 1, "error": null}`. |
| B2: Health Audit (`audit_event_health`) | Passed | Verified live ingestion status (`operational`) and honest reporting of Query API availability (`plan_upgrade_required`). Returned `healthy: True`. |

## Part C — Vendor Limitation & Honest Reporting

| Scenario | Result | Evidence |
|---|---|---|
| C1: Query API Plan Restriction | Blocked by Vendor Tier | `GET /api/2.0/events/names` and `GET /api/2.0/annotations` with Basic Auth returned HTTP 402 `{"error": "Your plan does not allow API calls. Upgrade at mixpanel.com/pricing"}`. |
| C2: Service Accounts Availability | Blocked by Vendor Tier | On Mixpanel Free tier, Service Account creation is unavailable. |
| C3: Non-Fabrication Adherence | Passed | Connector handlers return honest `PermissionError` explaining plan restriction rather than fabricating mock event lists. |
