# Contoso Pinball Gallery Concierge -- Agent Intelligence Manifest

This folder stages the working intelligence pack for the **Contoso Pinball Gallery Concierge** agent.

Target SharePoint site:

```text
https://timwinfo2.sharepoint.com/sites/CERTSTAR.NET
```

Target folder:

```text
Pinball Concierge Agent Intelligence
```

## Contents

| Folder | Purpose |
|--------|---------|
| `knowledge` | Grounding documents for Copilot Studio knowledge sources. |
| `topics` | Copilot Studio `.mcs.yml` topic stubs for Inventory Lookup and Repair Triage. |
| `flows` | Deterministic flow specifications for actions that must read/write data. |
| `triggers` | Trigger phrases and routing guidance. |
| `evals` | Test utterances and expected behavior for validation. |
| `data` | Seed data for SharePoint-backed inventory, holds, and movement lists. |
| `docs` | Course notes, source grounding, and this manifest. |
| `icons` | Agent avatar and channel icon assets. |
| `scripts` | Idempotent Graph/PnP deployment scripts. |

## Source of Truth Rules

- **SharePoint lists** are the transactional source for flow-backed operations such as inventory lookup and holds.
- **Markdown knowledge files** are the grounding source for generative answers.
- **Topic `.mcs.yml` files** are code-first teaching artifacts, not a full deployable agent shell.
- **Scripts** are idempotent and should be rerun after local asset changes.

## Flow Binding Targets

| Flow | SharePoint list | Key |
|------|-----------------|-----|
| Inventory Lookup | `CPG Inventory Machines` | `SKU` |
| Reserve / Hold a Machine | `CPG Inventory Holds` | `HoldReference` |
| Inventory audit trail | `CPG Inventory Movements` | `MovementReference` |
| Book a Service Visit | `CPG Service Bookings` | `BookingReference` |
| Request a Repair Quote | `CPG Repair Quotes` | `QuoteReference` |
| Check Order or Service Status | `CPG Status Lookup` | `ReferenceNumber` |
| Trade-In Valuation Start | `CPG Trade Ins` | `TradeInReference` |
| Autonomous Repair Intake | `CPG Repair Intake` | `IntakeReference` |

See `docs/deterministic-workflow-sharepoint-contracts.md` for the full list schema, input/output contracts, and idempotency rules.
