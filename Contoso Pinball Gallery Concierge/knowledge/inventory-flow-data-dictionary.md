# Contoso Pinball Gallery -- Inventory Flow Data Dictionary

This document describes the SharePoint lists used by the **Inventory Lookup** and **Reserve / Hold a Machine** deterministic flows. The values are fictional and exist only for course demos.

## CPG Inventory Machines

The primary list for current and recently sold showroom machines.

| Field | Type | Purpose |
|-------|------|---------|
| Title | Text | Display title of the machine, for example `Medieval Madness`. |
| SKU | Text | Stable idempotency key. Power Automate and deployment scripts upsert by this value. |
| Manufacturer | Text | Machine maker such as Stern Pinball, Williams, or Bally. |
| ModelYear | Number | Release year of the machine. |
| Era | Text | Retrieval-friendly era label such as DMD golden era or LCD modern. |
| ConditionGrade | Choice | Museum, Excellent, Very Good, Good, or Project. |
| PriceUsd | Currency | Current listed price in USD. |
| Availability | Choice | In stock, On hold, Sold - waitlist open, or On order. |
| Location | Text | Internal showroom or operations location. |
| SerialNumber | Text | Fictional training serial number. |
| WarrantyDays | Number | Warranty duration offered by Contoso. Project machines can be zero. |
| HoldExpiresUtc | DateTime | Expiration time for active holds. Blank when not on hold. |
| Featured | Yes/No | Whether the machine belongs in flagship showroom responses. |
| Tags | Text | Search hints for Copilot Studio and maker debugging. |
| Notes | Multiple lines | Sales guidance grounded in the inventory record. |
| ServiceStatus | Text | Current shop-readiness state. |
| SourceDocument | Text | Matching Markdown document uploaded to the knowledge library. |

## CPG Inventory Holds

Tracks hold requests created by deterministic flows.

| Field | Type | Purpose |
|-------|------|---------|
| Title | Text | Hold reference such as `HLD-20260715-RUSH`. |
| HoldReference | Text | Stable idempotency key for deployment and flow writes. |
| SKU | Text | Machine SKU being held. |
| MachineTitle | Text | Human-readable machine title. |
| ContactName | Text | Customer name for the hold. |
| ContactEmail | Text | Customer email for follow-up. |
| Status | Choice | Pending deposit, Active, Released, Expired, or Converted. |
| ExpiresUtc | DateTime | Hold expiry timestamp. |
| Notes | Multiple lines | Audit notes for training demos. |

## CPG Inventory Movements

Lightweight audit trail for inventory changes.

| Field | Type | Purpose |
|-------|------|---------|
| Title | Text | Movement reference such as `MOV-20260715-0003`. |
| MovementReference | Text | Stable idempotency key. |
| SKU | Text | Machine SKU affected. |
| MachineTitle | Text | Human-readable machine title. |
| MovementType | Choice | New arrival, Hold placed, Hold released, Sold, Restoration complete, Price update. |
| MovementUtc | DateTime | When the movement happened. |
| QuantityDelta | Number | Inventory quantity effect, where sale is `-1` and arrival is `1`. |
| Notes | Multiple lines | Audit details. |

## Flow Contract

The **Inventory Lookup** flow should accept either `MachineTitle` or `SKU`.

Recommended outputs:

| Output | Type | Rule |
|--------|------|------|
| Found | Boolean | `true` when one matching machine row is found. |
| Title | Text | Echo from SharePoint, not from user input. |
| SKU | Text | Echo from SharePoint. |
| Manufacturer | Text | Echo from SharePoint. |
| ModelYear | Number | Echo from SharePoint. |
| ConditionGrade | Text | Echo from SharePoint. |
| PriceUsd | Number | Echo from SharePoint. |
| Availability | Text | Echo from SharePoint. |
| HoldExpiresUtc | DateTime | Present only when the row is on hold. |
| RecommendedReply | Text | Deterministic sentence assembled from the fields above. |

The flow should never invent price or availability. If no row is found, return `Found = false` and let the Concierge offer to take a note of interest.
