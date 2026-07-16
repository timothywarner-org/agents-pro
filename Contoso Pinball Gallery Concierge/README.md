# Contoso Pinball Gallery Concierge

A demo **Microsoft Copilot Studio** agent for a fictional company, **Contoso Pinball Gallery** -- a boutique showroom that sells, restores, and services classic and modern pinball machines. The Concierge is the always-on expert on inventory, repairs, and pinball history, ready to publish to **Microsoft 365 Copilot**, **SharePoint**, and **Microsoft Teams**.

Everything here is teaching material for the O'Reilly course *How to Create AI Agents Like a Pro*. The company, catalog, prices, and service records are invented. Facts about Copilot Studio itself are grounded in Microsoft Learn (see `docs/ms-learn-sources.md`).

## What this agent does

| Capability | How it is built | Orchestration style |
|-----------|------------------|---------------------|
| Answer inventory questions ("Do you have Medieval Madness? What's the price?") | Generative answers grounded in the inventory catalog | Generative |
| Triage a repair ("My flipper is weak") and offer a service booking | Topic + grounded repair playbook + handoff to a flow | Mixed |
| Research and history ("Who made Attack from Mars? What era is it?") | Generative answers grounded in the history/research doc | Generative |
| Book a service visit, request a quote, check order status | **Deterministic** Power Automate flows | Deterministic |

The design follows the Microsoft guidance that Copilot Studio agents should combine **a few curated topics** with **generative answers grounded in trusted sources**, not hundreds of rigid topics. Deterministic flows are reserved for the exact-steps work (bookings, quotes, status) where an auditable path matters.

## Folder layout

```
Contoso Pinball Gallery Concierge/
  README.md                      <- you are here
  instructions.md                <- the agent's system prompt / instructions block
  topics/                        <- Topic .mcs.yml stubs for the VS Code extension
    T01_InventoryLookup.mcs.yml
    T02_RepairTriage.mcs.yml
  knowledge/                     <- fake demo docs + upload metadata (grounding)
    inventory-catalog.md
    repair-playbook.md
    pinball-history-research.md
    warranty-and-services.md
    KNOWLEDGE-UPLOAD-METADATA.md <- the description fields you paste on upload
  flows/
    deterministic-flow-ideas.md  <- Power Automate flow specs (easy wins)
  triggers/
    quick-win-triggers.md        <- trigger phrases + generative descriptions
  evals/
    eval-set.md                  <- test utterances + expected behavior
  icons/
    agent-avatar.svg             <- agent avatar
    store-icon.svg               <- Teams / M365 store color icon
    icon-outline.svg             <- monochrome outline variant
  docs/
    ms-learn-sources.md          <- grounding citations for the Copilot Studio facts
```

## How to load it into Copilot Studio

There are two supported paths, matching how the course teaches it.

**Path A -- portal-first (fastest for a live demo).**
1. Create a blank agent in Copilot Studio named **Contoso Pinball Gallery Concierge**.
2. Paste `instructions.md` into the agent's **Instructions**.
3. Add the four `knowledge/` docs as knowledge sources. Paste each file's **description** from `KNOWLEDGE-UPLOAD-METADATA.md` -- metadata drives retrieval quality, so this step is not optional.
4. Recreate the two topics from `topics/` (or import via the VS Code extension, Path B).
5. Build the deterministic flows from `flows/deterministic-flow-ideas.md`.
6. Publish, then add the **Microsoft 365 Copilot and Teams** channel and the **SharePoint** channel.

**Path B -- code-first (VS Code extension).**
1. Install the **Microsoft Copilot Studio** VS Code extension (GA).
2. Clone your Contoso agent locally, drop these `.mcs.yml` topic files into the cloned `topics/` folder, edit, and **Apply changes** back to your environment.
3. The `.mcs.yml` shape here matches the agent-definition language the extension reads.

> **Note on the topic stubs.** `topics/T01_InventoryLookup.mcs.yml` and `T02_RepairTriage.mcs.yml` are deliberately **topic stubs**, not a complete deployable agent. There is no `agent.mcs.yml` / `settings.mcs.yml` shell in this folder yet, so the topics have no parent to import into on their own. To make them deploy, first scaffold the agent shell (with generative orchestration on, to match the `modelDescription`-driven routing the stubs assume), then bind the two knowledge sources so each `SearchAndSummarizeContent` node resolves, and finally replace the `MAKER TODO` handoff in T02 with the real **Book a Service** action. Do the shell and any `.mcs.yml` edits through the `@copilot-studio:*` sub-agents.

## Publishing to the three targets

You publish once, then connect channels. Publishing updates every connected channel at the same time, so re-publish after any edit.

| Target | Channel to add | Notes grounded in MS Learn |
|--------|----------------|----------------------------|
| Microsoft 365 Copilot | **Teams and Microsoft 365 Copilot** channel; keep **Make agent available in Microsoft 365 Copilot** selected | Submits the agent as a **request** in the Microsoft 365 admin center; an admin approves it before org users see it |
| Microsoft Teams | Same **Teams and Microsoft 365 Copilot** channel (one channel serves both) | Sideload for yourself, share an install link, or **Show to the organization** |
| SharePoint | **SharePoint** channel | Embed on a SharePoint site for contextual help |

**Authentication:** leave **Authenticate with Microsoft** on (the default) so the agent works in Teams, M365 Copilot, and SharePoint with Entra ID and no manual setup. Only switch to **No authentication** for an anonymous web demo, and know that it disables tools that need user credentials.

## Next Best Steps

1. Load `instructions.md` + the four knowledge docs into a blank agent and publish to the Teams and M365 Copilot channel for a live smoke test.
2. Wire the two deterministic flows (Book a Service, Request a Quote) so the agent can act, not just answer.
3. Run the `evals/eval-set.md` utterances in the test panel and tune trigger phrases and knowledge descriptions from the misses.
