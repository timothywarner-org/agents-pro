# Document Processor Agent — Event Trigger: SharePoint File Created → Classify + Route

## Goal
When a document lands in a SharePoint library, the agent classifies it (invoice/contract/resume) and routes it to the right workflow.

## Event trigger choice (native Copilot Studio)
Use a **Copilot Studio event trigger** based on a SharePoint connector event (File created), which generates a trigger payload through a connector and invokes the agent autonomously.

## Trigger payload fields (recommended)
- `siteUrl`
- `libraryName`
- `fileName`
- `fileUrl`
- `createdBy`
- `createdUtc`

## Suggested agent behavior
1. Classify document type + confidence.
2. If confidence >= 0.85, auto-route using routing-rules.csv.
3. If 0.6–0.85, route to manual review queue.
4. If < 0.6, ask for human triage (Teams message to reviewers).

## Optional Power Automate companion flow
If you prefer deterministic routing, create a flow:
- Trigger: SharePoint — *When a file is created (properties only)*
- Action: *Get file content*
- Action: AI Builder (or model) extract fields (Invoice/Contract)
- Action: Dataverse create record + Approvals create approval
- Action: Teams post proactive message via agent

## Notes
The event trigger and payload pattern is described in Microsoft Learn under "Event triggers overview" and "Add an event trigger".
