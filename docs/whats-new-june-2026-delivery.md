# What's New This Delivery - Copilot Studio Cheat Sheet

_Instructor podium reference for **How to Create AI Agents Like a Pro**. Keep this open while teaching._

**Last refreshed:** 2026-06-01, grounded against <https://learn.microsoft.com/microsoft-copilot-studio/whats-new>

This page captures only what **changed** since the materials were last written. Every claim is verified against Microsoft Learn. The golden rule on stage: **if you cannot cite it, do not say it.**

---

## The "say this, not that" table

These are the corrections most likely to bite you mid-segment. Read the right column out loud before each delivery.

| # | If you were about to say... | Say this instead | Why |
|---|------------------------------|------------------|-----|
| 1 | "GPT-5 is in preview" | "**GPT-5 Chat is GA**; GPT-5 *Reasoning* and *Auto* are preview" | GPT-5 Chat went GA Nov 24 2025, globally except GCC. The reasoning variants did not. **Never say bare "GPT-5"** on stage. |
| 2 | "Use GPT-4.1 for orchestration" | "**Claude Sonnet 4.5 is the recommended orchestrator**; GPT-4.1 is the default, not the best" | MS docs explicitly say do not use GPT-4.1 as the orchestration model; Claude Sonnet 4.5 has a better success rate. |
| 3 | "Connected agents are how you add subagents" | "**Add other agents** is the taxonomy: child, connected, A2A, Foundry, Fabric, M365 SDK" | The concept broadened. The old `authoring-connected-agents` page is now `authoring-add-other-agents`. |
| 4 | "MCP uses stdio or SSE" | "Copilot Studio takes **Streamable HTTP only**; SSE was retired after Aug 2025" | Teaching SSE is teaching a dead transport. |
| 5 | "Wire up MCP with a custom connector" | "Use the **MCP onboarding wizard** (Tools > Add a tool > Model Context Protocol)" | Custom connector still works but is the fallback, not the headline path. |
| 6 | "Batch testing means the Copilot Studio Kit" | "**Native agent evaluations are GA**; the Kit is now complementary" | Evaluations are built in: test sets, generate-from-knowledge, activity maps, version compare. |
| 7 | "You author agents in the web portal" | "Or in **VS Code with the GA extension**: clone, edit YAML, Git/PR, deploy" | MS docs name **Claude Code** and GitHub Copilot as authoring agents. Strong hook for this audience. |

---

## Model lineup (the part that changed most)

| Model | Status | Category | Teaching note |
|-------|--------|----------|---------------|
| **GPT-4.1** | GA (Default) | General | The fallback default, not the recommendation |
| **GPT-5 Chat** | **GA** (Nov 24 2025, ex-GCC) | General | The GA GPT-5 you can say out loud |
| **GPT-5 Reasoning / Auto** | Preview | Deep / Auto | Do not call these "GPT-5" without the qualifier |
| **GPT-5.5 Reasoning (Deep)** | Experimental | Deep | Early-access only, not for production |
| **Claude Sonnet 4.5** | **GA** (cross-geo) | General | **MS-recommended orchestration model** |
| **Claude Sonnet 4.6** | **GA** (cross-geo) | General | Newer general-purpose option |
| **Claude Opus 4.6** | **GA** (cross-geo) | Deep | GA reasoning-class option |
| **Claude Opus 4.7** | Experimental | Deep | Not GA |

**Gotchas to mention:** Anthropic (Claude) models are external, not Azure-hosted, so a **tenant admin must approve** them first. Some models are cross-geo and may process data outside your region. Model selection lives on the agent's **Overview** tab and requires **generative orchestration**.

Ref: <https://learn.microsoft.com/microsoft-copilot-studio/authoring-select-agent-model> · <https://learn.microsoft.com/microsoft-copilot-studio/authoring-select-external-response-model>

---

## The eight deltas, one line each

1. **Models.** GPT-5 Chat GA, Claude Sonnet 4.5/4.6 + Opus 4.6 GA, Claude is the recommended orchestrator. <https://learn.microsoft.com/microsoft-copilot-studio/authoring-select-agent-model>
2. **Multi-agent.** "Add other agents" taxonomy; **A2A protocol is GA** (no preview banner); Foundry, Fabric, M365 SDK connections are preview. <https://learn.microsoft.com/microsoft-copilot-studio/authoring-add-other-agents> · <https://learn.microsoft.com/microsoft-copilot-studio/add-agent-agent-to-agent>
3. **MCP transport.** Streamable HTTP only, SSE retired after Aug 2025; onboarding wizard is the recommended path; MCP needs generative orchestration. <https://learn.microsoft.com/microsoft-copilot-studio/mcp-add-existing-server-to-agent>
4. **Agent evaluations.** Single-response evaluations **GA** (test sets ≤100 cases, activity maps, version compare, REST API + connector automation, 89-day retention). **Multi-turn evaluation is Preview** (landed Mar 31 2026, GA projected Jun 2026). <https://learn.microsoft.com/microsoft-copilot-studio/analytics-agent-evaluation-intro>
5. **VS Code extension.** **GA**: clone agent, edit `.mcs.yml`, Git/PR, deploy; Claude Code and GitHub Copilot named as authoring agents. <https://learn.microsoft.com/microsoft-copilot-studio/visual-studio-code-extension-overview>
6. **REST API tools.** Still **Preview**, now a first-class Tools-page type (Prompt / Agent flow / Computer use / Custom connector / MCP / REST API); OpenAPI v2 (v3 auto-downgrades). <https://learn.microsoft.com/microsoft-copilot-studio/agent-extend-action-rest-api>
7. **Knowledge sources.** Added **Azure AI Search** (vector + semantic ranker, VNet), **Bing Custom Search** (agent-level, overrides public sites), **Web Search** (Bing grounding), and the **`OnKnowledgeRequested`** custom-knowledge trigger (YAML only). Generative mode: 25 websites / 25 SharePoint URLs. <https://learn.microsoft.com/microsoft-copilot-studio/knowledge-copilot-studio>
8. **Deck filename.** The current deck is `warner-agents-pro-april-2026.pptx` (not the old February name).

---

## Labels are precise on purpose

One vocabulary across all materials. **GA** means production-ready. **Preview** means early access, not for production. **Experimental** means do not bet a demo on it.

| GA (safe to teach as production) | Preview (frame as "early, may change") | Experimental (mention only) |
|----------------------------------|----------------------------------------|------------------------------|
| GPT-5 Chat | GPT-5 Reasoning / Auto | GPT-5.5 Reasoning |
| Claude Sonnet 4.5 / 4.6, Opus 4.6 | Multi-turn evaluation | Claude Opus 4.7 |
| A2A protocol | REST API tools | |
| Child + connected CS agents | Foundry / Fabric / M365 SDK connections | |
| Single-response evaluations | Real-time voice agents | |
| VS Code extension | | |

> **Workload note:** the WAF teaching doc uses a **different agent set** (Customer Service, Onboarding, Document Processor) than this course's single **CKA Study Assistant**. Do not blur them. They are separate teaching workloads that share the same WAF lens.
