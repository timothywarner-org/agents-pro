# How to Create AI Agents Like a Pro

![How to Create AI Agents Like a Pro cover](images/cover.png)

[![Website TechTrainerTim.com](https://img.shields.io/badge/Website-TechTrainerTim.com-0a66c2)](https://techtrainertim.com) [![GitHub Copilot Memory Store](https://img.shields.io/badge/GitHub-copilot--memory--store-181717?logo=github)](https://github.com/timothywarner-org/copilot-memory-store) [![GitHub Prompt Pro](https://img.shields.io/badge/GitHub-prompt--pro-181717?logo=github)](https://github.com/timothywarner-org/prompt-pro)

**O'Reilly Live Learning Course** | 4 Hours | Copilot Studio -- One Agent, Four Segments

Build one **Microsoft Copilot Studio** agent end to end. We start from a natural-language description, add knowledge sources, wire topics and Power Automate flows, turn on autonomous event triggers, then publish and measure ROI. One low-context-switch scenario -- the **Contoso Pinball Gallery Concierge** -- carries all four segments.

## Course Overview -- One Agent, Four Segments

This is a **Copilot Studio** course. The four segment titles below are the ones on the O'Reilly sell page, kept verbatim. We satisfy every one of them by building **one** agent progressively: the **Contoso Pinball Gallery Concierge**, the always-on virtual host for a fictional boutique that sells, restores, and services classic and modern pinball machines. Every segment adds a capability layer.

| Segment | Sell-page Title                                          | Contoso Pinball Demo (the running scenario)                                                                         |
| ------- | ------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------ |
| 1       | Copilot Studio Fundamentals & Creating Your First Agent | Describe the Concierge in natural language, add three knowledge sources, test in the simulator                      |
| 2       | Topics, Actions, and Power Automate Integration         | Build the Repair Triage topic and the **Book a Service** Power Automate flow with an approval step                  |
| 3       | Autonomous Agents & Event Triggers                      | A repair-intake or trade-in form lands in SharePoint, an event trigger fires, the agent processes it autonomously   |
| 4       | Deployment, Analytics, and ROI                          | Publish to Teams / SharePoint / M365 Copilot; walk Analytics, the Savings-calculator ROI tile, and governance      |

**The one agent:** The **Contoso Pinball Gallery Concierge** answers **inventory** questions (stock, condition, price, availability), **triages repairs** (a reported symptom, safe first-line guidance, a booking offer), explains **history and research**, and hands off to **deterministic Power Automate flows** for anything transactional (bookings, quotes, status, holds, trade-ins). The company, catalog, prices, and service records are invented. The Copilot Studio facts are grounded in Microsoft Learn.

> **Off-contract bonus:** Azure AI Foundry appears only as a clearly-labeled appendix in the instructor plan (`docs/course-plan-july-2026.md`), a 5-minute aside on where the no-code ceiling is. It is **not** one of the four contracted segments.

## Prerequisites

- Microsoft 365 account (Business or Enterprise) -- [start free trial](https://www.microsoft.com/en-us/microsoft-365/try)
- Copilot Studio access -- [start free trial](https://copilotstudio.microsoft.com)
- Power Automate Premium -- [start 90-day trial](https://www.microsoft.com/en-us/power-platform/try-free)
- Microsoft Teams desktop app
- Basic familiarity with Microsoft 365 apps

**Optional trials for extended scenarios:**

| Resource                  | URL                                                                 | Duration              |
| ------------------------- | ------------------------------------------------------------------- | --------------------- |
| Power Apps Developer Plan | <https://www.microsoft.com/power-platform/products/power-apps/free> | No limit              |
| Power Platform Trials Hub | <https://www.microsoft.com/en-us/power-platform/try-free>           | Various               |

> **Off-contract bonus prerequisites (Azure AI Foundry appendix only):** Python 3.11+ (<https://www.python.org/downloads/>) and an Azure subscription (<https://azure.microsoft.com/en-us/free>). Not needed for any of the four core segments.

## Repository Structure

```text
agents-pro/
├── README.md                           # This file
├── CLAUDE.md                           # Claude Code instructions
├── CODE_OF_CONDUCT.md                  # Community guidelines
├── contributing.md                     # Contribution guide
├── security.md                         # Security policy
├── LICENSE                             # MIT License
├── .markdownlint.json                  # Markdown linting config
│
├── .github/                            # GitHub Copilot configurations
│   ├── agents/                         # Copilot agent definitions
│   ├── prompts/                        # Copilot prompt templates
│   └── instructions/                   # Copilot coding instructions
│
├── Contoso Pinball Gallery Concierge/  # PRIMARY course agent -- the one we build across all four segments
├── CKA Exam Prep Assistant/            # Deployable Copilot Studio agent (.mcs.yml), reference sibling
├── RAI Advisor/                        # Deployable Responsible AI agent (.mcs.yml + workflow + icons)
│
├── agents-playground/                  # Archived predecessor course ("Build Production-Ready AI Agents")
├── docs/                               # Course plan, WAF notes, reference library, research
├── images/                             # Course images and assets
├── scripts/                            # Repo-level utility scripts
└── src/                                # Reference and predecessor agent implementations
    ├── claude-agent/                   # Claude Code agent materials
    ├── copilot-studio/                 # Copilot Studio topic assets and tutorials
    ├── copilot-studio-agent/           # Blueprint originals of the three sold patterns (now consolidated in the Concierge)
    ├── foundry-agent/                  # Azure AI Foundry code-first agent (off-contract bonus material)
    └── oreilly-agent-mvp/              # LangGraph + CrewAI Python pipeline (reference)
```

## Quick Start

1. **Clone the repository**

   ```bash
   git clone https://github.com/timothywarner-org/agents-pro.git
   ```

2. **Read the instructor plan:** `docs/course-plan-july-2026.md` is the source of truth -- four segments, time tables, talking points, demo prompt sets, and the PP-WAF pillar mapping.

3. **Open the primary build target:** `Contoso Pinball Gallery Concierge/`. Its `README.md` covers both load paths (portal-first and the VS Code extension), and `instructions.md` holds the vetted agent system prompt.

4. **Segment 1 -- Fundamentals:** Create the Concierge by natural-language description, paste `instructions.md`, and add the three knowledge docs from `Contoso Pinball Gallery Concierge/knowledge/` (inventory, history/research, warranty). Test in the simulator.

5. **Segment 2 -- Topics, Actions, Flows:** Build the `T02_RepairTriage` topic from `topics/`, then the **Book a Service** Power Automate flow with an approval step from `flows/deterministic-flow-ideas.md`.

6. **Segment 3 -- Autonomous & Event Triggers:** Add the "When an item is created in SharePoint" trigger so a repair-intake row is processed with no user in the chat.

7. **Segment 4 -- Deploy, Analytics, ROI:** Publish to Teams / SharePoint / M365 Copilot, then walk Analytics, the Savings-calculator ROI tile, custom metrics, and governance.

## How to Set Up the Demo

Two ways in. **Path A** is what you want for a live session; **Path B** is the code-first story that lands with a developer audience.

### Path A -- portal-first (fastest, no local tooling)

1. Create a **blank agent** in Copilot Studio named **Contoso Pinball Gallery Concierge**.
2. Paste `Contoso Pinball Gallery Concierge/instructions.md` into the agent's **Instructions**.
3. Add the `knowledge/` docs as knowledge sources. **Paste each file's description from `KNOWLEDGE-UPLOAD-METADATA.md`** -- those descriptions drive retrieval quality, so skipping them is the single fastest way to make the demo look broken.
4. Turn on **generative orchestration** (Overview tab). The topic stubs assume `modelDescription`-driven routing, and event triggers and MCP both require it.
5. Recreate the two topics from `topics/`, or import them via Path B.
6. Build the deterministic flows from `flows/deterministic-flow-ideas.md`.
7. **Publish once**, then add the **Teams and Microsoft 365 Copilot** channel and the **SharePoint** channel. Re-publish after every edit; publishing updates all connected channels together.

### Path B -- code-first (VS Code extension, GA)

1. Install the **Microsoft Copilot Studio** extension for VS Code.
2. Clone your Contoso agent locally, drop the `.mcs.yml` topic files into the cloned `topics/` folder, edit, then **Apply changes** back to the environment.
3. Git and PR the agent definition like any other source. Microsoft's docs name **Claude Code** and GitHub Copilot as supported authoring agents, which is a strong hook for a developer room.

> **Known gap, call it out rather than get surprised:** `topics/` currently holds **topic stubs**, not a complete deployable agent. There is no `agent.mcs.yml` / `settings.mcs.yml` shell yet, so the topics have no parent to import into on their own. Scaffold the shell first (generative orchestration on), bind the knowledge sources so each `SearchAndSummarizeContent` node resolves, then replace the `MAKER TODO` handoff in T02 with the real **Book a Service** action. Route all `.mcs.yml` work through the `@copilot-studio:*` sub-agents.

### Optional -- provision the SharePoint backing data

Only needed if you are demoing the **deterministic flows** (inventory lookup, bookings, quotes, status) against real lists rather than hand-waving them. The scripts are idempotent, so re-runs are safe.

Validate before touching the tenant:

```powershell
pwsh ".\Contoso Pinball Gallery Concierge\scripts\deploy-contoso-inventory-assets.ps1" -TenantName <yourtenant> -DryRun
```

Then deploy with a tenant or SharePoint admin account:

```powershell
pwsh ".\Contoso Pinball Gallery Concierge\scripts\deploy-contoso-inventory-assets.ps1" -TenantName <yourtenant> -OwnerEmail admin@<yourtenant>.com -DeviceLogin
```

This creates the site, the `Concierge Knowledge` library, and the `CPG Inventory *` lists seeded from `data/*.seed.json`. A second script (`deploy-contoso-deterministic-workflow-assets.graph.ps1`) adds the Service Bookings, Repair Quotes, Status Lookup, Trade Ins, and Repair Intake lists. Full schema and flow contract: `Contoso Pinball Gallery Concierge/docs/deterministic-workflow-sharepoint-contracts.md`.

> The committed script defaults point at Tim's tenants (`techtrainertim`, `timwinfo2`). **Substitute your own** tenant and site path before running.

### Pre-flight checklist

- [ ] Copilot Studio environment with **generative orchestration** enabled
- [ ] Maker can **publish** (M365 Copilot license, or Copilot Studio user license plus credits -- trial licenses build and test but **cannot publish**)
- [ ] **Model picked and verified today.** The lineup turns over every 4-6 weeks. Never say bare "GPT-5" (the Reasoning/Auto variants are preview), and **Claude Sonnet 4.5 has retired**. See `docs/whats-new-july-2026-delivery.md`.
- [ ] Knowledge descriptions pasted from `KNOWLEDGE-UPLOAD-METADATA.md`, not left blank
- [ ] Event-trigger demo: budget for **Copilot Credits**; the trigger's SharePoint connector must survive your DLP policy (most restrictive policy wins)
- [ ] Smoke-test with `evals/eval-set.md` in the test panel. Test-panel traffic does **not** appear in Analytics, so generate real channel traffic before demoing the Segment 4 dashboards.

## Slide Deck

The instructor deck (`docs/warner-agents-pro-july-2026.pptx`) is gitignored -- PowerPoint files are large and change often between deliveries. A flattened PDF render (`docs/warner-agents-pro-july-2026.pdf`) is committed for quick reference, **but it may lag the current .pptx** because there is no PDF renderer wired into this repo yet. Re-render the PDF from the latest .pptx before you rely on it for anything but a rough preview.

## Segment Summaries

### Segment 1: Copilot Studio Fundamentals & Creating Your First Agent

**Theme:** Describe an agent in natural language, ground it, test it

- What "agent" means in Copilot Studio -- a few curated topics plus generative answers grounded in trusted sources
- Generative vs classic orchestration; pick the reasoning model on the Overview tab
- Write the agent instructions, then create the Concierge by natural-language description
- Add three knowledge sources (inventory catalog, history/research, warranty and services) with retrieval-driving descriptions
- Hands-on: test in the simulator against inventory, research, and warranty questions

**Skills:** Agent scaffolding, generative orchestration, knowledge grounding, instruction design

---

### Segment 2: Topics, Actions, and Power Automate Integration

**Theme:** Conversation logic in topics, transactions in flows

- When to make something deterministic -- a booking, quote, or status check returns a **real** reference number, not a guessed one
- Build the `T02_RepairTriage` topic: question, grounded playbook search, booking offer, condition branch
- Model descriptions are the routing contract under generative orchestration
- Build the **Book a Service** Power Automate flow (`MachineTitle`, `Symptom`, `PreferredWindow`, `ContactEmail`) with an approval step
- Hands-on: test the end-to-end triage-to-booking path

**Skills:** Topic authoring, Power Automate flows, approval steps, human-in-the-loop patterns

---

### Segment 3: Autonomous Agents & Event Triggers

**Theme:** The agent acts on an event, with no user in the chat

- Conversational vs autonomous; what an event trigger is; the Copilot Credits billing impact
- Add the "When an item is created in SharePoint" trigger and define the payload
- Write the autonomous plan: read the intake row, triage against the playbook, create a booking or trade-in record
- Debug with the activity map; keep consecutive action/topic calls under 15
- Optional pro-code extension: connect an MCP tool (FastMCP over Streamable HTTP)

**Skills:** Event triggers, autonomous plans, activity-map debugging, DLP-aware trigger connectors

---

### Segment 4: Deployment, Analytics, and ROI

**Theme:** Publish, measure, and defend the business value

- Publish once, connect channels -- **Teams and Microsoft 365 Copilot** channel plus the **SharePoint** channel
- Built-in analytics: Total Sessions, Engagement, Resolution, Escalation, Abandon, CSAT
- The Savings-calculator ROI tile and up to three natural-language custom metrics
- Native agent evaluations (GA), themes-to-eval-sets, and Application Insights KQL
- Security and governance: Entra ID SSO, DLP, content moderation, solution-aware ALM, CoE Starter Kit

**Skills:** Channel publishing, Copilot Studio Analytics, ROI storytelling, agent evaluations, governance

## Learning Resources

### Copilot Studio (all four segments)

- [Copilot Studio Documentation](https://learn.microsoft.com/en-us/microsoft-copilot-studio/)
- [What is Copilot Studio](https://learn.microsoft.com/microsoft-copilot-studio/fundamentals-what-is-copilot-studio)
- [Create and edit topics](https://learn.microsoft.com/microsoft-copilot-studio/authoring-create-edit-topics)
- [Generative orchestration (generative actions)](https://learn.microsoft.com/microsoft-copilot-studio/advanced-generative-actions)
- [Select a primary AI model](https://learn.microsoft.com/microsoft-copilot-studio/authoring-select-agent-model)
- [Knowledge sources summary](https://learn.microsoft.com/microsoft-copilot-studio/knowledge-copilot-studio)
- [Power Automate flow actions](https://learn.microsoft.com/microsoft-copilot-studio/advanced-flow)
- [Event trigger overview](https://learn.microsoft.com/microsoft-copilot-studio/authoring-triggers-about)
- [Design autonomous agent capabilities](https://learn.microsoft.com/microsoft-copilot-studio/guidance/autonomous-agents)
- [Analytics overview](https://learn.microsoft.com/microsoft-copilot-studio/analytics-overview)
- [Savings calculator (cost savings)](https://learn.microsoft.com/microsoft-copilot-studio/analytics-cost-savings)
- [Agent evaluations](https://learn.microsoft.com/microsoft-copilot-studio/analytics-agent-evaluation-intro)
- [Security & governance](https://learn.microsoft.com/microsoft-copilot-studio/security-and-governance)
- [Copilot Studio VS Code extension (GA)](https://learn.microsoft.com/microsoft-copilot-studio/visual-studio-code-extension-overview)
- [Power Platform Well-Architected](https://learn.microsoft.com/power-platform/well-architected/)

### Bonus (off-contract): Azure AI Foundry

Not on the sell page and not one of the four segments. These back the optional pro-code appendix on where Copilot Studio hands off heavier reasoning to Azure. Verify before delivery -- Foundry surfaces move fast, and the product is now branded **Microsoft Foundry**.

- [Foundry Agent Service overview](https://learn.microsoft.com/en-us/azure/foundry/agents/overview)
- [Microsoft Foundry documentation (hub)](https://learn.microsoft.com/en-us/azure/foundry/)
- [`azure-ai-projects` (PyPI)](https://pypi.org/project/azure-ai-projects/)
- [Add a Foundry agent to Copilot Studio (preview)](https://learn.microsoft.com/microsoft-copilot-studio/add-agent-foundry-agent)
- [Model Context Protocol](https://modelcontextprotocol.io)

## Where to Go Next -- Certifications and Self-Paced Training

Everything below was verified against the Microsoft Learn catalog API on **July 16, 2026**. Credentials churn fast, so re-check before you recommend any of them from the podium.

### Credentials that actually match what we build

| Credential | Type | Why it fits this course |
| ---------- | ---- | ----------------------- |
| [**Applied Skills: Build an agent in Microsoft Copilot Studio**](https://learn.microsoft.com/en-us/credentials/applied-skills/build-an-agent-in-microsoft-copilot-studio/) (APL-6006) | Free hands-on lab, no proctor | **The closest match to Segments 1, 2, and 4.** Assesses exactly what we do live: create and configure an agent, configure generative AI and knowledge, create topics, configure tools, share and publish. Start here. |
| [**Applied Skills: Enhance agents with autonomous capabilities**](https://learn.microsoft.com/en-us/credentials/applied-skills/enhance-agents-with-autonomous-capabilities/) (APL-6000) | Free hands-on lab, no proctor | **Segment 3 in credential form.** Assesses agent flows as tools, **event triggers for autonomous behavior**, and error handling plus human interaction. |
| [**Microsoft Certified: AI Agent Builder Associate**](https://learn.microsoft.com/en-us/credentials/certifications/ai-agent-builder-associate/) (exam AB-620) | Proctored, 120 min | The developer-track certification built on Copilot Studio: multi-agent, MCP, A2A, connectors, computer use, ALM. The natural next step after this course. |
| [**Microsoft 365 Certified: Copilot and Agent Administration Fundamentals**](https://learn.microsoft.com/en-us/credentials/certifications/copilot-and-agent-administration-fundamentals/) (exam AB-900) | Proctored, fundamentals | The **administration** angle on Segment 4: approval processes, monitoring, admin centers. Complements the maker track rather than duplicating it. |
| [**Microsoft Certified: Agentic AI Business Solutions Architect**](https://learn.microsoft.com/en-us/credentials/certifications/agentic-ai-business-solutions-architect/) | Proctored, advanced | The architect track, for anyone whose day job is deciding *where* agents belong in a solution. |

> **Retired, do not chase:** **APL-7008 "Create agents in Microsoft Copilot Studio"** retired **July 8, 2026**. If you find it in an older reading list (including this repo's `docs/copilot-studio-certs.md`), the live replacement is **APL-6006 "Build an agent in Microsoft Copilot Studio"** in the table above.

### Self-paced learning paths (all free on Microsoft Learn)

Ordered to mirror the four segments. Times are Microsoft's own estimates.

| Segment | Learning path | Time |
| ------- | ------------- | ---- |
| Start here | [Create agents with Microsoft Copilot Studio - Online Workshop](https://learn.microsoft.com/en-us/training/paths/power-virtual-agents-workshop/) (beginner, 5 modules) | ~171 min |
| 1 | [Create agents in Microsoft Copilot Studio](https://learn.microsoft.com/en-us/training/paths/create-extend-custom-copilots-microsoft-copilot-studio/) (4 modules) | ~222 min |
| 2 | [Design agent conversations and responses using topics](https://learn.microsoft.com/en-us/training/paths/design-agent-conversations-responses-topics-copilot-studio/) (3 modules) | ~137 min |
| 2 | [Automate tasks and workflows in Microsoft Copilot Studio](https://learn.microsoft.com/en-us/training/paths/automate-tasks-workflows-copilot-studio/) (3 modules) | ~160 min |
| 3 | [Enhance agents with autonomous capabilities](https://learn.microsoft.com/en-us/training/paths/enhance-autonomous-agents/) (3 modules) -- preps APL-6000 | ~120 min |
| 3 | [Integrate agents with enterprise systems](https://learn.microsoft.com/en-us/training/paths/integrate-agents-enterprise-systems-copilot-studio/) (4 modules) | ~198 min |
| 4 | [Explore Microsoft 365 Copilot and agent administration](https://learn.microsoft.com/en-us/training/paths/explore-microsoft-365-copilot-agent-administration/) (3 modules) | ~199 min |
| Beyond | [Design and build multi-agent solutions in Copilot Studio](https://learn.microsoft.com/en-us/training/paths/design-build-multi-agent-solutions-copilot-studio/) (4 modules) | ~174 min |
| Beyond | [Architect AI solutions for business productivity](https://learn.microsoft.com/en-us/training/paths/architect-agentic-ai-business-solutions/) (advanced, 11 modules) | ~684 min |

### Instructor-led course

- [MS-4004: Empower your workforce with Microsoft 365 Copilot Use Cases](https://learn.microsoft.com/en-us/training/courses/ms-4004)

## Course Schedule

| Time        | Activity                                                                                                     |
| ----------- | ------------------------------------------------------------------------------------------------------------ |
| 0:00 - 0:50 | Segment 1: Copilot Studio Fundamentals & Creating Your First Agent -- describe, ground, test the Concierge   |
| 0:50 - 1:00 | Q&A + Break                                                                                                  |
| 1:00 - 1:50 | Segment 2: Topics, Actions, and Power Automate Integration -- Repair Triage topic + Book a Service flow      |
| 1:50 - 2:00 | Q&A + Break                                                                                                  |
| 2:00 - 2:50 | Segment 3: Autonomous Agents & Event Triggers -- SharePoint intake, event trigger, autonomous plan           |
| 2:50 - 3:00 | Q&A + Break                                                                                                  |
| 3:00 - 3:50 | Segment 4: Deployment, Analytics, and ROI -- publish to three channels, Analytics, Savings tile, governance  |
| 3:50 - 4:00 | Wrap-up, resources, next steps                                                                               |

## Instructor

**Tim Warner** -- Microsoft MVP (Azure AI and Cloud/Datacenter Management), Microsoft Certified Trainer

- [LinkedIn](https://www.linkedin.com/in/timothywarner/)
- [Website](https://techtrainertim.com/)
- [O'Reilly Author Page](https://learning.oreilly.com/search/?query=Tim%20Warner)

## License

MIT License - See [LICENSE](./LICENSE) for details.

---

**Questions?** Open an issue or reach out via the course chat during live sessions.
