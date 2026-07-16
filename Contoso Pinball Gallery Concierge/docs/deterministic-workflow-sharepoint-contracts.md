# Deterministic Workflow SharePoint Contracts

This document maps each Contoso Pinball Gallery Concierge deterministic workflow to its SharePoint backing store. The goal is simple: if the agent promises a reference number, appointment, quote, hold, status, or valuation, the value comes from a list row, not from model text.

Target site:

```text
https://timwinfo2.sharepoint.com/sites/CERTSTAR.NET
```

## Backing Lists

| Workflow | SharePoint list | Stable key | Why it exists |
|----------|-----------------|------------|---------------|
| Inventory Lookup | `CPG Inventory Machines` | `SKU` | Reads price, condition, availability, location, and warranty fields. |
| Reserve / Hold a Machine | `CPG Inventory Holds` | `HoldReference` | Writes customer holds with expiry and status. |
| Inventory audit | `CPG Inventory Movements` | `MovementReference` | Records arrivals, sales, hold releases, and restoration milestones. |
| Book a Service Visit | `CPG Service Bookings` | `BookingReference` | Writes service commitments and approval status. |
| Request a Repair Quote | `CPG Repair Quotes` | `QuoteReference` | Writes pricing-band outputs and specialist review state. |
| Check Order or Service Status | `CPG Status Lookup` | `ReferenceNumber` | Reads `SVC-`, `QUO-`, `HLD-`, `TRD-`, and `ORD-` status rows. |
| Trade-In Valuation Start | `CPG Trade Ins` | `TradeInReference` | Writes trade-in starter requests and estimate bands. |
| Autonomous Repair Intake | `CPG Repair Intake` | `IntakeReference` | Stages list-item intake events for autonomous flow demos. |

## Flow Contracts

### Book a Service Visit

**Input fields:** `MachineTitle`, `Symptom`, `PreferredWindow`, `ContactEmail`

**Write target:** `CPG Service Bookings`

**Output fields:** `BookingReference`, `ConfirmedWindow`, `Status`

**Rule:** The flow creates or updates a row keyed by `BookingReference`. The agent repeats the reference and window exactly as returned.

### Request a Repair Quote

**Input fields:** `MachineTitle`, `Symptom`

**Write target:** `CPG Repair Quotes`

**Output fields:** `QuoteReference`, `Tier`, `PriceBand`, `Turnaround`, `Status`

**Rule:** The flow maps symptom to tier using the repair playbook and warranty policy. The agent must not invent a firm price.

### Check Order or Service Status

**Input fields:** `ReferenceNumber`

**Read target:** `CPG Status Lookup`

**Output fields:** `Found`, `ReferenceType`, `Status`, `LastUpdatedUtc`, `CustomerMessage`

**Rule:** If the reference is not found, return `Found = false`. Do not synthesize a status.

### Reserve / Hold a Machine

**Input fields:** `MachineTitle`, `ContactEmail`

**Read target:** `CPG Inventory Machines`

**Write target:** `CPG Inventory Holds`

**Output fields:** `Placed`, `HoldReference`, `ExpiresUtc`, `Availability`

**Rule:** Only place a hold when the machine row is `In stock`. On hold or sold machines route to waitlist wording.

### Trade-In Valuation Start

**Input fields:** `MachineTitle`, `Era`, `ConditionSelfGrade`, `ContactEmail`

**Write target:** `CPG Trade Ins`

**Output fields:** `TradeInReference`, `EstimateBand`, `Status`

**Rule:** The band is a starter estimate. A specialist confirms the final offer after review.

### Autonomous Repair Intake

**Input source:** SharePoint list item or document-library event

**Write/read target:** `CPG Repair Intake`

**Output fields:** `IntakeReference`, `ProcessingStatus`, `Priority`

**Rule:** This is the event-trigger demo lane. The list gives a lightweight trigger source when a document library trigger is too noisy for recording.

## Idempotency Rules

- Every flow has a stable business key ending in `Reference` except inventory lookup, which uses `SKU`.
- Deployment scripts upsert by the stable key.
- Power Automate flows should check for an existing row before creating a duplicate.
- Reference numbers should be generated once and then reused for status lookup.
- UTC timestamps are used for durable flow state.

## Recording Notes

- Use `CPG Service Bookings` for the repair-triage payoff.
- Use `CPG Repair Quotes` when demonstrating why pricing is deterministic.
- Use `CPG Status Lookup` for a clean follow-up turn.
- Use `CPG Trade Ins` as the revenue expansion path.
- Use `CPG Repair Intake` for the autonomous trigger segment.
