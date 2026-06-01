# How to Create AI Agents Like a Pro - June 2026

_O'Reilly Live Learning - Instructor Source of Truth_

**Instructor:** Tim Warner (Microsoft MVP, MCT Regional Lead)
**Delivery date:** June 2026
**Duration:** 4 hours (four 60-minute segments, 10-minute break between segments)
**Delivery mode:** Live, hands-on, single progressively-built agent

## Course Overview - One Agent, Four Segments

We build **one** Copilot Studio agent end-to-end: the **AZ-900 Cert-Prep Assistant**. Every segment adds a capability layer; every segment maps to Microsoft's Power Platform Well-Architected Framework (PP-WAF) pillars.

| Segment | Theme | Primary PP-WAF Pillars | Learner Outcome |
|---------|-------|------------------------|-----------------|
| 1 - Inception | Design the agent | Experience Optimization, Operational Excellence | Scenario, instructions, topic map |
| 2 - Build | Topics, triggers, knowledge | Experience Optimization, Reliability | Working Q&A agent grounded in AZ-900 content |
| 3 - Extend | Actions, MCP, subagents | Performance Efficiency, Reliability | Multi-agent system with external tools |
| 4 - Operate | Test, observe, govern | Security, Operational Excellence | Production-ready, governed deployment |

**The one agent:** An **Azure Fundamentals (AZ-900)** study companion for business and IT pros who are **new to cloud**. It explains exam domains, teaches core cloud concepts and Azure services in plain language, generates domain-weighted practice questions, builds a personalized study plan, and hands off to a human mentor when the learner is stuck. No prior Azure experience is required, which matches the AZ-900 audience profile: a technology professional who wants to demonstrate **foundational knowledge of cloud concepts in general and Microsoft Azure in particular**.

**AZ-900 domain weighting** (drives topic design and knowledge scoping):

| Domain | Weight |
|--------|-------:|
| Describe Azure architecture and services | 35-40% |
| Describe Azure management and governance | 30-35% |
| Describe cloud concepts | 25-30% |

**Authoritative references used throughout the course** - all verified stable URLs:

- Copilot Studio overview - <https://learn.microsoft.com/en-us/microsoft-copilot-studio/fundamentals-what-is-copilot-studio>
- Power Platform Well-Architected - <https://learn.microsoft.com/en-us/power-platform/well-architected/>
- Cloud Adoption Framework - <https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/>
- Copilot Studio topics - <https://learn.microsoft.com/en-us/microsoft-copilot-studio/authoring-create-edit-topics>
- Generative orchestration - <https://learn.microsoft.com/en-us/microsoft-copilot-studio/advanced-generative-actions>
- Select a primary AI model - <https://learn.microsoft.com/en-us/microsoft-copilot-studio/authoring-select-agent-model>
- Knowledge sources summary - <https://learn.microsoft.com/en-us/microsoft-copilot-studio/knowledge-copilot-studio>
- Add other agents / multi-agent - <https://learn.microsoft.com/en-us/microsoft-copilot-studio/authoring-add-other-agents>
- Agent-to-Agent (A2A) protocol - <https://learn.microsoft.com/en-us/microsoft-copilot-studio/add-agent-agent-to-agent>
- MCP in Copilot Studio - <https://learn.microsoft.com/en-us/microsoft-copilot-studio/agent-extend-action-mcp>
- Model Context Protocol spec - <https://modelcontextprotocol.io/specification>
- Agent evaluations - <https://learn.microsoft.com/en-us/microsoft-copilot-studio/analytics-agent-evaluation-intro>
- VS Code extension - <https://learn.microsoft.com/en-us/microsoft-copilot-studio/visual-studio-code-extension-overview>
- Analytics - <https://learn.microsoft.com/en-us/microsoft-copilot-studio/analytics-overview>
- Security & governance - <https://learn.microsoft.com/en-us/microsoft-copilot-studio/security-and-governance>
- AZ-900 study guide - <https://learn.microsoft.com/credentials/certifications/resources/study-guides/az-900>
- Azure documentation - <https://learn.microsoft.com/azure/>

---

## Segment 1 - Inception (0:00 – 1:00)

_Framing the scenario and designing the agent before a single node is built._

### Time Table

| Time | Activity |
|------|----------|
| 0:00 – 0:08 | Welcome, course arc, the one-agent promise |
| 0:08 – 0:20 | Agent taxonomy - declarative, retrieval, tool-using, multi-agent |
| 0:20 – 0:32 | Scenario framing - who is the AZ-900 learner and what do they struggle with? |
| 0:32 – 0:45 | Instruction design and topic planning |
| 0:45 – 0:55 | Live: create agent shell, write instructions, list topics on whiteboard |
| 0:55 – 1:00 | Segment wrap, what's next |

### Talking Points

- **Agent taxonomy.** Declarative agents (M365 Copilot), retrieval agents (grounded Q&A), tool-using agents (actions/MCP), multi-agent systems (connected agents). Copilot Studio spans all four. Reference: <https://learn.microsoft.com/en-us/microsoft-copilot-studio/fundamentals-what-is-copilot-studio>
- **Orchestration modes.** Classic (trigger-phrase routing) vs. generative (AI orchestrator routes to topics, actions, knowledge, and subagents). Generative is now the **default for new agents**. We use generative. Reference: <https://learn.microsoft.com/en-us/microsoft-copilot-studio/advanced-generative-actions>
- **Pick the reasoning model.** Generative orchestration lets you choose the agent's primary model on the **Overview** tab. **GPT-4.1 remains the platform Default model.** **GPT-5 Chat is GA** (say "GPT-5 *Chat*", never bare "GPT-5" - GPT-5 Reasoning (Deep) and GPT-5 Auto are still **preview**). **Claude Sonnet 4.5, Sonnet 4.6, and Opus 4.6 (Deep) are GA**; **Claude Opus 4.7 (Deep) is experimental**. Microsoft's Dynamics 365 ERP MCP guidance is explicit: **do not use GPT-4.1 as the orchestration model** - the recommended orchestrator is **Claude Sonnet 4.5**, with **GPT-5 (Chat) as fallback**. Claude models are external (Anthropic), so a **tenant admin must approve** them first. References: <https://learn.microsoft.com/en-us/microsoft-copilot-studio/authoring-select-agent-model> · <https://learn.microsoft.com/dynamics365/fin-ops-core/dev-itpro/copilot/build-agent-mcp>
- **PP-WAF - Experience Optimization first.** Before YAML, we define the learner persona, job-to-be-done, and success metrics. Reference: <https://learn.microsoft.com/en-us/power-platform/well-architected/experience-optimization/>
- **Instruction design.** System instructions beat per-topic prompts for generative orchestration. Reference: <https://learn.microsoft.com/en-us/microsoft-copilot-studio/authoring-generative-ai-options>
- **CAF landing-zone thinking.** Even a single agent lives in an environment - decide dev/test/prod, DLP, and Dataverse scope up front. Reference: <https://learn.microsoft.com/en-us/power-platform/guidance/adoption/environment-strategy>

### Scenario Framing - The AZ-900 Learner

- **Persona.** Marcus, a business analyst with **no Azure experience**, moving into a cloud-adjacent role and preparing for **Microsoft Azure Fundamentals (AZ-900)** in 4 weeks. He is a technology professional starting his journey toward an Azure career, exactly the AZ-900 target audience.
- **Pain points.** Cloud jargon overload (IaaS, PaaS, SaaS), no mental model for the **shared responsibility model**, no structured study plan, unsure which exam domain to weight first.
- **Success metrics.** Time-to-answer under 8s; grounded-citation rate above 80%; containment rate above 70%; CSAT above 4/5.

### Agent Instructions - Draft (paste into `settings.mcs.yml`)

> You are the **AZ-900 Cert-Prep Assistant**, a patient tutor for business and IT pros preparing for the Microsoft Azure Fundamentals (AZ-900) exam. Assume **no prior Azure experience** and explain cloud concepts in plain language. Ground every answer in the Microsoft Learn AZ-900 study guide, the official Azure documentation, the Cloud Adoption Framework, and the instructor's study notes. When a learner asks about Azure pricing, regions, or service availability, prefer the azure-docs lookup MCP tool. When they want core concepts explained in depth, route to the ConceptExplainer subagent. When they ask for a study plan, use the StudyPlanGenerator topic. Cite sources. Never fabricate service names, pricing, or exam answers. **Refuse requests for exam dumps or "the real exam answers"** and redirect the learner to practice questions and the study guide. If confidence is low, offer to escalate to a human mentor.

### Topic Map - Planned in Segment 1, Built in Segment 2

| Folder | Purpose | Trigger type |
|--------|---------|--------------|
| `T01_ExamDomainOverview` | Explain domain weights, objectives | OnRecognizedIntent |
| `T02_CloudConcepts` | Cloud models, shared responsibility, IaaS/PaaS/SaaS | OnRecognizedIntent |
| `T03_CoreArchitectureAndServices` | Regions, availability zones, compute, networking, storage | OnRecognizedIntent |
| `T04_IdentitySecurityGovernance` | RBAC, Zero Trust, Azure Policy, cost management | OnRecognizedIntent |
| `T05_PracticeQuestion` | Domain-weighted practice Q generator | OnRecognizedIntent |
| `T06_StudyPlanGenerator` | 4-week personalized plan | OnRecognizedIntent |
| `T07_EscalateToHuman` | Handoff to mentor | OnEscalate |
| `T00_Greeting` | OnConversationStart welcome | OnConversationStart |
| `T99_Fallback` | OnUnknownIntent + generative answers | OnUnknownIntent |

### Live Build Checklist - Segment 1

- [ ] Create Copilot Studio environment (dev)
- [ ] Create new agent `AZ-900 Cert-Prep Assistant`
- [ ] Set display name, description, conversation starters
- [ ] Toggle **Generative orchestration** on
- [ ] Set primary model on the **Overview** tab (Default is GPT-4.1; demo Claude Sonnet 4.5 if tenant-approved)
- [ ] Paste draft instructions
- [ ] Sketch topic map in portal (empty shells OK)
- [ ] Confirm DLP policy allows HTTP connector (needed Segment 3)

### Demo Prompt Set - "Flex the Muscles" (empty shell)

- "What is this agent?" - shows instructions surfacing through orchestrator.
- "Who are you?" - verifies persona.
- "Just give me the real exam answers." - shows guardrail (refuses exam-dump request, redirects to study guide).

---

## Segment 2 - Build (1:10 – 2:10)

_Topics, triggers, knowledge sources, variables, generative answers._

### Time Table

| Time | Activity |
|------|----------|
| 1:10 – 1:18 | Recap, preview the build |
| 1:18 – 1:30 | Knowledge sources - AZ-900 study guide, Azure docs, Cloud Adoption Framework, SharePoint notes |
| 1:30 – 1:45 | Build `T01_ExamDomainOverview` and `T05_PracticeQuestion` |
| 1:45 – 1:58 | Build `T06_StudyPlanGenerator` with AutomaticTaskInput (weeks, weak domain) |
| 1:58 – 2:05 | Build `T99_Fallback` with SearchAndSummarizeContent |
| 2:05 – 2:10 | Demo and segment wrap |

### Talking Points

- **Knowledge source ordering matters.** Sources in a generative-answers node override agent-level sources. Reference: <https://learn.microsoft.com/en-us/microsoft-copilot-studio/knowledge-copilot-studio>
- **The source menu grew.** Beyond public websites and SharePoint, you can now ground on **Azure AI Search** (vector index + semantic ranker, VNet support), **Bing Custom Search** (a scoped Bing index via a Configuration ID), and **Web Search** (broad Bing grounding). You can also build a fully custom source with the **`OnKnowledgeRequested`** trigger (YAML/code view only). References: <https://learn.microsoft.com/en-us/microsoft-copilot-studio/knowledge-azure-ai-search> · <https://learn.microsoft.com/en-us/microsoft-copilot-studio/knowledge-bing-custom-search> · <https://learn.microsoft.com/en-us/microsoft-copilot-studio/guidance/custom-knowledge-sources>
- **Generative-mode limits.** Generative orchestration allows up to **25 public websites** and **25 SharePoint URLs**; uploaded files do not count against the 25-source search limit. Reference: <https://learn.microsoft.com/en-us/microsoft-copilot-studio/knowledge-copilot-studio>
- **Bing Custom Search overrides public sites.** Turning on Bing Custom Search at the agent level **turns off and blocks** any public-website knowledge sources. Pick one. Reference: <https://learn.microsoft.com/en-us/microsoft-copilot-studio/knowledge-bing-custom-search>
- **Public website source requires crawlable content.** learn.microsoft.com/azure is ideal; gated docs are not. Reference: <https://learn.microsoft.com/en-us/microsoft-copilot-studio/knowledge-add-public-website>
- **SharePoint knowledge requires `Sites.Read.All` and `Files.Read.All`.** Work IQ now improves SharePoint-grounded retrieval. References: <https://learn.microsoft.com/en-us/microsoft-copilot-studio/knowledge-add-sharepoint> · <https://learn.microsoft.com/en-us/microsoft-copilot-studio/knowledge-copilot-studio#turn-on-work-iq>
- **Topic inputs via AutomaticTaskInput** are preferred under generative orchestration - the orchestrator fills them from context. Use an explicit Question node only when the input is conditional (e.g., ask for weak domain only if learner did not mention one).
- **PP-WAF - Reliability.** Ground answers in trusted sources; degrade gracefully when knowledge is missing. Reference: <https://learn.microsoft.com/en-us/power-platform/well-architected/reliability/>

### Knowledge Sources - Quick Reference

| Source | Kind | Scope | Notes |
|--------|------|-------|-------|
| AZ-900 study guide | PublicSiteSearchSource | <https://learn.microsoft.com/credentials/certifications/resources/study-guides/az-900> | Domain weights and objectives; primary exam ground truth |
| Azure documentation | PublicSiteSearchSource | <https://learn.microsoft.com/azure/> (concepts, services, pricing, regions) | High authority; service and concept detail |
| Cloud Adoption Framework | PublicSiteSearchSource | <https://learn.microsoft.com/azure/cloud-adoption-framework/> | Governance, landing-zone, cost context |
| Tim's study notes | SharePointSearchSource | `/sites/AZ900Study/Shared Documents/Notes/` | Instructor-authored highlights and gotchas |

**Other sources available (not all used in this build, but worth naming):**

| Source | When to reach for it | Watch out for |
|--------|----------------------|---------------|
| Azure AI Search | Large private corpus needing vector + semantic ranking | Add via a formal data connection, not a raw endpoint + key; supports VNet |
| Bing Custom Search | A curated, scoped public web index | **Overrides and disables public-website sources** when turned on |
| Web Search | Broad, real-time public info | Bing grounding; interleaves with your public-site sources |
| `OnKnowledgeRequested` topic | Your own search API / enterprise search | YAML/code view only, no visual designer; uses `System.SearchQuery` |

### Topic Patterns Taught

- **Empty-shell + AutomaticTaskInput** - generative orchestrator supplies `weeksUntilExam`, `weakestDomain`.
- **Conditional Question node** - only ask for weakest domain if orchestrator could not infer it.
- **SearchAndSummarizeContent** in `T99_Fallback` - grounded summary with citations.
- **EndDialog with Topic.Result** - exam-domain topic returns structured output the orchestrator can cite.

### Live Build Checklist - Segment 2

- [ ] Add public website knowledge: AZ-900 study guide
- [ ] Add public website knowledge: learn.microsoft.com/azure (scoped to concepts/services)
- [ ] Add public website knowledge: Cloud Adoption Framework
- [ ] Add SharePoint knowledge: AZ900Study site (Sites.Read.All consented)
- [ ] Author `T01_ExamDomainOverview` with Topic.Domain input, table response
- [ ] Author `T05_PracticeQuestion` weighted by AZ-900 domain percentages
- [ ] Author `T06_StudyPlanGenerator` with two AutomaticTaskInput fields
- [ ] Author `T99_Fallback` with SearchAndSummarizeContent
- [ ] Validate each topic YAML via `/copilot-studio:validate`
- [ ] Test-panel: run the demo prompts below

### Demo Prompt Set - Segment 2

| Prompt | Expected behavior |
|--------|-------------------|
| "What domains are on the AZ-900 exam?" | T01 returns table with the three AZ-900 domains and weights |
| "Give me a practice question on Azure storage." | T05 returns domain-scoped question |
| "I have 4 weeks, weak on management and governance. Plan?" | T06 auto-fills both inputs |
| "What is the shared responsibility model?" | T99 generative answer with citation to the AZ-900 study guide / Azure docs |

---

## Segment 3 - Extend (2:20 – 3:20)

_Actions, Power Automate flows, MCP tool integration, connected subagents, channel deployment._

### Time Table

| Time | Activity |
|------|----------|
| 2:20 – 2:28 | Extension landscape - actions, flows, MCP, subagents |
| 2:28 – 2:42 | Add Power Automate flow action (email a study plan) |
| 2:42 – 2:58 | Add MCP server for Azure pricing/region lookup |
| 2:58 – 3:12 | Add two connected subagents: concept-explainer, practice-exam-coach |
| 3:12 – 3:18 | Deploy to Teams / M365 Copilot |
| 3:18 – 3:20 | Segment wrap |

### Talking Points

- **Action types.** Prebuilt connectors, custom connectors, Power Automate flows, MCP tools, and subagents. Start with Power Automate when the workflow is multi-step; use MCP when a capability is already a well-formed external tool. References:
  - <https://learn.microsoft.com/en-us/microsoft-copilot-studio/advanced-flow>
  - <https://learn.microsoft.com/en-us/microsoft-copilot-studio/agent-extend-action-mcp>
- **MCP is standards-based.** Model Context Protocol is a JSON-RPC 2.0 protocol with tools, resources, and prompts primitives (Copilot Studio currently consumes **tools and resources**). The recommended way to connect is the **MCP onboarding wizard** (Tools > Add a tool > New tool > Model Context Protocol), which handles **None / API key / OAuth 2.0** auth; the custom-connector route is the fallback. MCP requires **generative orchestration**. References:
  - <https://learn.microsoft.com/en-us/microsoft-copilot-studio/mcp-add-existing-server-to-agent>
  - <https://modelcontextprotocol.io/specification>
- **Transport reality check.** Copilot Studio supports the **Streamable HTTP** transport only. **SSE was deprecated and is no longer supported for MCP after August 2025** - do not teach it as a live option.
- **REST API tools are still preview.** If you would rather wrap an existing REST endpoint than stand up an MCP server, "Extend your agent with tools from a REST API" is **preview** (prerelease) and requires an **OpenAPI v2** spec (a v3 spec is auto-downgraded to v2). Reference: <https://learn.microsoft.com/en-us/microsoft-copilot-studio/agent-extend-action-rest-api>
- **FastMCP for Python servers.** Decorator API - docstrings become tool descriptions, type hints become parameter schemas. Expose the server over **Streamable HTTP** for Copilot Studio. Reference: <https://github.com/modelcontextprotocol/python-sdk>
- **Add other agents (the taxonomy broadened).** "Connected agents" is now one option among several. **Child agents** (embedded), **connected Copilot Studio (in-environment) agents**, and **agent-to-agent (A2A) protocol** connections are all **GA** (A2A reached GA in **April 2026**). **External connections are preview**: **Microsoft Foundry agents (preview)**, **Fabric Data agents (preview)**, and **agents built with the Microsoft 365 Agents SDK (preview)**. We use connected agents so specialists can be reused outside the AZ-900 use case. References: <https://learn.microsoft.com/en-us/microsoft-copilot-studio/authoring-add-other-agents> · <https://learn.microsoft.com/en-us/microsoft-copilot-studio/add-agent-agent-to-agent> · <https://learn.microsoft.com/en-us/microsoft-copilot-studio/add-agent-foundry-agent> · <https://learn.microsoft.com/en-us/microsoft-copilot-studio/add-agent-fabric-data-agent> · <https://learn.microsoft.com/en-us/microsoft-copilot-studio/add-agent-microsoft-365-agents-sdk-agent>
- **Teams / M365 deployment.** One click from Channels → Microsoft Teams; requires tenant admin approval for broad publishing. Reference: <https://learn.microsoft.com/en-us/microsoft-copilot-studio/publication-add-bot-to-microsoft-teams>
- **PP-WAF - Performance Efficiency.** Offload specialized reasoning to subagents; keep the root agent's instruction budget small. Reference: <https://learn.microsoft.com/en-us/power-platform/well-architected/performance-efficiency/>

### Extension Inventory

| Extension | Kind | Purpose |
|-----------|------|---------|
| `EmailStudyPlan` | Power Automate flow (TaskDialog) | Email generated plan to learner via Office 365 Outlook |
| `AzureDocsLookup` | MCP tool | Look up Azure region availability and pricing-calculator reference from a FastMCP server |
| `agents/ConceptExplainer` | Connected agent | Explain a cloud concept (e.g., shared responsibility, IaaS vs PaaS) in plain English with examples |
| `agents/PracticeExamCoach` | Connected agent | Coach the learner through domain-weighted practice questions and rationale |

### FastMCP Azure Docs Server - Reference Sketch

```python
# mcp_servers/azure_docs/server.py
from fastmcp import FastMCP

mcp = FastMCP("azure-docs")

@mcp.tool()
def lookup_azure_service(service: str, topic: str | None = None) -> dict:
    """Return a grounded Azure reference entry for a service.

    Args:
        service: The Azure service or concept (regions, virtual machines, pricing calculator, ...).
        topic: Optional sub-topic (availability zones, region pairs, cost, ...).
    """
    # Query a local index of learn.microsoft.com/azure JSON (regions, pricing, service docs)
    return azure_index.lookup(service, topic)

if __name__ == "__main__":
    mcp.run()  # stdio for local dev; serve Streamable HTTP for Copilot Studio (SSE no longer supported after Aug 2025)
```

MCP protocol reference: <https://modelcontextprotocol.io/specification>

### Live Build Checklist - Segment 3

- [ ] Register Office 365 Outlook connection
- [ ] Create Power Automate flow `EmailStudyPlan(toAddress, planMarkdown)`
- [ ] Add flow as action with AutomaticTaskInput for both parameters
- [ ] Deploy FastMCP `azure-docs` server behind an HTTPS Streamable HTTP endpoint
- [ ] Add the MCP server via the **onboarding wizard** (Tools > Add a tool > New tool > Model Context Protocol); custom connector only if the wizard cannot reach the server
- [ ] Add MCP tool to agent; verify tool discovery in chat
- [ ] Create connected agent `ConceptExplainer` (own topics, own knowledge)
- [ ] Create connected agent `PracticeExamCoach` (question bank)
- [ ] Link both connected agents to root AZ-900 agent
- [ ] Enable Microsoft Teams channel
- [ ] Install in instructor's Teams tenant, smoke-test

### Demo Prompt Set - Segment 3

| Prompt | Expected behavior |
|--------|-------------------|
| "Email me the 4-week plan." | Orchestrator invokes `EmailStudyPlan` with filled inputs |
| "Which Azure regions are paired with East US?" | Routes to azure-docs MCP tool, returns grounded region-pair reference |
| "Explain the difference between IaaS, PaaS, and SaaS." | Orchestrator hands off to ConceptExplainer subagent |
| "Quiz me on management and governance and explain my mistakes." | Handoff to PracticeExamCoach subagent |

---

## Segment 4 - Operate (3:30 – 4:30)

_Test, observe, secure, govern, publish._

### Time Table

| Time | Activity |
|------|----------|
| 3:30 – 3:38 | Testing pyramid for agents |
| 3:38 – 3:52 | Test panel + native agent evaluations (Kit as complement) |
| 3:52 – 4:05 | Analytics, observability, Application Insights |
| 4:05 – 4:18 | Security, DLP, governance, CoE |
| 4:18 – 4:26 | Publishing, channels, admin approval workflow |
| 4:26 – 4:30 | Course wrap, resources, Q&A pointers |

### Talking Points

- **Testing pyramid for agents.** Unit (single utterance in test panel) → Scenario (multi-turn script) → Batch (**native agent evaluations**, with Copilot Studio Kit as a complement) → Shadow / canary in production. Reference: <https://learn.microsoft.com/en-us/microsoft-copilot-studio/authoring-test-bot>
- **Native agent evaluations (GA).** Agent evaluations are **generally available as of March 2026**, built into Copilot Studio: build a **test set** by hand, by import, or **generated from your knowledge and topics**; grade with text-match, similarity, and quality graders; inspect each case with an **activity map**; and **compare agent versions** side by side. **Multi-turn (full-conversation) evaluation is preview** (introduced March 2026) - present it as just-arrived, not settled. Reference: <https://learn.microsoft.com/en-us/microsoft-copilot-studio/analytics-agent-evaluation-intro>
- **Copilot Studio Kit.** Power CAT accelerator; still useful for batch regression at scale against Direct Line, and complementary to native evaluations. Reference: <https://learn.microsoft.com/en-us/microsoft-copilot-studio/guidance/kit-overview>
- **Analytics.** Session, engagement, resolution, escalation, CSAT - test-panel traffic is excluded. Reference: <https://learn.microsoft.com/en-us/microsoft-copilot-studio/analytics-overview>
- **Observability.** Pipe conversations to Application Insights via Dataverse connector; dashboards in Power BI. Reference: <https://learn.microsoft.com/en-us/microsoft-copilot-studio/analytics-app-insights>
- **Security.** Authentication (M365 SSO), content moderation, DLP classification of connectors. References:
  - <https://learn.microsoft.com/en-us/microsoft-copilot-studio/security-and-governance>
  - <https://learn.microsoft.com/en-us/microsoft-copilot-studio/admin-data-loss-prevention>
- **Governance.** CoE Starter Kit, environment strategy, solution-aware deployment. Reference: <https://learn.microsoft.com/en-us/power-platform/guidance/coe/starter-kit>
- **PP-WAF - Security & Operational Excellence** are the Segment 4 pillars. References:
  - <https://learn.microsoft.com/en-us/power-platform/well-architected/security/>
  - <https://learn.microsoft.com/en-us/power-platform/well-architected/operational-excellence/>

### Test Matrix - AZ-900 Cert-Prep Assistant

| Layer | Tool | What we cover |
|-------|------|---------------|
| Unit | Copilot Studio Test panel | Each topic's trigger + happy path |
| Scenario | Test panel multi-turn | StudyPlanGenerator with follow-ups |
| Batch | **Native agent evaluations** (GA) | Test set across all three AZ-900 domains + 2 off-topic; quality + similarity graders |
| Batch (scale) | Copilot Studio Kit | Optional Direct Line regression suite; complements native evaluations |
| Integration | Teams channel | End-to-end install, auth, Teams rendering |
| Regression | Native eval set + solution export | Re-run and version-compare before every publish |

### Observability Dashboard - Fields to Track

- Intent routing confidence (median, p95)
- Grounded-citation rate
- Escalation rate
- Fallback count per session
- Tool-call latency (MCP, flows)
- CSAT

### Security & Governance Checklist

- [ ] Authentication: Microsoft Entra, SSO enforced
- [ ] DLP policy: HTTP connector in Business; Outlook in Business; unknowns blocked
- [ ] Content moderation level: High
- [ ] Secrets in environment variables (never in YAML)
- [ ] Solution-aware deployment (dev → test → prod)
- [ ] CoE inventory entry for the agent
- [ ] Responsible-AI notice in conversation starters

### Live Build Checklist - Segment 4

- [ ] Run 10 unit tests in test panel
- [ ] Build a native evaluation **test set** (generate from knowledge/topics, then hand-tune the AZ-900 domain cases)
- [ ] Run the evaluation; review quality + similarity scores and an activity map for one failing case
- [ ] (Optional) Import the same suite into Copilot Studio Kit for Direct Line regression
- [ ] Connect Application Insights
- [ ] Tag DLP policy; confirm connector classifications
- [ ] Export solution from dev, import into test
- [ ] Publish; route to Teams
- [ ] File CoE inventory entry

### Demo Prompt Set - Segment 4

| Prompt | Expected behavior |
|--------|-------------------|
| (Batch) AZ-900 domain test set | Evaluation run shows pass/fail + graded score per case |
| "Just give me the exam answers." | Guardrail refuses the exam-dump request; logged as moderation event |
| "Email the plan to external@gmail.com" | DLP / auth path blocks external address if policy set |
| "Show analytics for this week." | Instructor walks Analytics dashboard |

---

## Course Wrap & Resources

### Pro-Code Bridge - The Copilot Studio VS Code Extension (GA)

_Optional closer for the developers in the room; ties the no-code build to real source control._

- **What it is.** The Microsoft Copilot Studio extension for Visual Studio Code is **generally available** (GA as of January 2026). Clone an agent from Copilot Studio to your machine, edit its **agent definition YAML** locally, manage it with **Git and pull requests**, then apply or deploy changes back to your environment.
- **Why it matters here.** It turns a portal-authored agent into a versioned artifact - diffs, code review, CI-friendly workflows - without leaving the editor your team already uses.
- **The hook for this audience.** Microsoft's own docs name **GitHub Copilot and Claude Code** as authoring agents you can point at the YAML. Agent-driven authoring of an agent.
- **Caveat for our repo.** Any blueprint YAML you may have seen in earlier course repos predates this April model and multi-agent refresh; treat it as historical, not as a clone-and-edit starting point.
- Reference: <https://learn.microsoft.com/en-us/microsoft-copilot-studio/visual-studio-code-extension-overview>

### Recap - What We Built

- One Copilot Studio agent, progressively enriched across four segments.
- Nine topics, four knowledge sources, one Power Automate flow, one MCP tool, two connected subagents.
- Tested with the test panel and **native agent evaluations**, observed through Application Insights, governed through DLP and CoE.

### PP-WAF Pillar Recap

| Pillar | Where we applied it |
|--------|---------------------|
| Experience Optimization | Segment 1 persona, Segment 2 grounded answers |
| Reliability | Segment 2 knowledge ordering, Segment 3 fallback routing |
| Performance Efficiency | Segment 3 subagents and MCP offload |
| Security | Segment 4 DLP, auth, moderation |
| Operational Excellence | Segment 1 environment strategy, Segment 4 CoE + ALM |

### Reference Library

- Copilot Studio docs - <https://learn.microsoft.com/en-us/microsoft-copilot-studio/>
- Power Platform Well-Architected - <https://learn.microsoft.com/en-us/power-platform/well-architected/>
- Cloud Adoption Framework - <https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/>
- Microsoft MCP for Beginners - <https://github.com/microsoft/mcp-for-beginners>
- Model Context Protocol - <https://modelcontextprotocol.io/>
- Select a primary AI model - <https://learn.microsoft.com/en-us/microsoft-copilot-studio/authoring-select-agent-model>
- Agent evaluations - <https://learn.microsoft.com/en-us/microsoft-copilot-studio/analytics-agent-evaluation-intro>
- Copilot Studio VS Code extension - <https://learn.microsoft.com/en-us/microsoft-copilot-studio/visual-studio-code-extension-overview>
- AZ-900 study guide - <https://learn.microsoft.com/credentials/certifications/resources/study-guides/az-900>
- Azure documentation - <https://learn.microsoft.com/azure/>
- Copilot Studio Kit - <https://learn.microsoft.com/en-us/microsoft-copilot-studio/guidance/kit-overview>
- CoE Starter Kit - <https://learn.microsoft.com/en-us/power-platform/guidance/coe/starter-kit>

### Instructor Follow-Up

- Slide deck: `docs/warner-agents-pro-june-2026.pptx`
- Agent source: `src/copilot-studio-agent/` (rescaffolded for AZ-900 in a follow-up PR)
- Mock SharePoint content: `src/copilot-studio-agent/knowledge/` (AZ-900 study notes)
- Issues / errata: <https://github.com/timothywarner-org/agents-pro/issues>
