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

Not on the sell page and not one of the four segments. These back the optional pro-code appendix on where Copilot Studio hands off heavier reasoning to Azure. Verify before delivery -- Foundry surfaces move fast.

- [Azure AI Foundry Agents](https://learn.microsoft.com/azure/ai-foundry/agents/)
- [`azure-ai-projects` (PyPI)](https://pypi.org/project/azure-ai-projects/)
- [Add a Foundry agent to Copilot Studio (preview)](https://learn.microsoft.com/microsoft-copilot-studio/add-agent-foundry-agent)
- [Model Context Protocol](https://modelcontextprotocol.io)

### Certifications

- [MS-4004: M365 Copilot Use Cases](https://learn.microsoft.com/en-us/training/courses/ms-4004)
- [Copilot & Agent Administration Fundamentals](https://learn.microsoft.com/en-us/credentials/certifications/copilot-and-agent-administration-fundamentals/)
- [AI-102: Azure AI Engineer Associate](https://learn.microsoft.com/en-us/credentials/certifications/azure-ai-engineer/)

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
