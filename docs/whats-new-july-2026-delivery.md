# What's New This Delivery - Copilot Studio Cheat Sheet

_Instructor podium reference for **How to Create AI Agents Like a Pro**. Keep this open while teaching._

**Last refreshed:** 2026-07-14, grounded against <https://learn.microsoft.com/microsoft-copilot-studio/whats-new> and <https://learn.microsoft.com/microsoft-copilot-studio/authoring-select-agent-model>

This page captures only what **changed** since the materials were last written. Every claim is verified against Microsoft Learn. The golden rule on stage: **if you cannot cite it, do not say it.**

---

## The "say this, not that" table

These are the corrections most likely to bite you mid-segment. Read the right column out loud before each delivery.

| # | If you were about to say... | Say this instead | Why |
|---|------------------------------|------------------|-----|
| 1 | "GPT-5 is in preview" | "**GPT-5 Chat and GPT-5.5 Chat are GA**; GPT-5 *Reasoning*, *Auto*, and GPT-5.5 *Reasoning* are preview/experimental" | GPT-5 Chat went GA Nov 24 2025. GPT-5.5 Chat is now also GA. The reasoning/auto variants are not. **Never say bare "GPT-5"** on stage. |
| 2 | "Use Claude Sonnet 4.5 for orchestration" | "**Claude Sonnet 4.5 is retired** -- use **Claude Sonnet 4.6** (GA) or the newer **Claude Sonnet 5** (GA, early access environment, new-experience agents only)" | Sonnet 4.5 was the June recommendation; it has since retired from Copilot Studio's model list. |
| 3 | "Connected agents are how you add subagents" | "**Add other agents** is the taxonomy: child, connected, A2A, Foundry, Fabric, M365 SDK" | The concept broadened. The old `authoring-connected-agents` page is now `authoring-add-other-agents`. |
| 4 | "MCP uses stdio or SSE" | "Copilot Studio takes **Streamable HTTP only**; SSE was retired after Aug 2025" | Teaching SSE is teaching a dead transport. |
| 5 | "Wire up MCP with a custom connector" | "Use the **MCP onboarding wizard** (Tools > Add a tool > Model Context Protocol)" | Custom connector still works but is the fallback, not the headline path. |
| 6 | "Multi-turn evaluation is still preview" | "**Multi-turn evaluation is GA**, alongside single-response evaluations" | The June doc flagged this "GA projected June 2026" -- confirmed GA per the July `whats-new` page. |
| 7 | "You author agents in the web portal" | "Or in **VS Code with the GA extension**: clone, edit YAML, Git/PR, deploy" | MS docs name **Claude Code** and GitHub Copilot as authoring agents. Strong hook for this audience. |
| 8 | "Copilot Studio has one authoring experience" | "There's now a **classic** experience (what this course teaches) and a **new agent experience** (production-ready preview, natural-language-first, with Microsoft IQ, skills, and memory)" | New in June 2026. Worth a one-line mention and pointer, not a curriculum rewrite -- see "New agent experience" section below. |

---

## Model lineup (the part that changed most)

| Model | Status | Category | Teaching note |
|-------|--------|----------|---------------|
| **GPT-4.1** | GA (Default) | General | The fallback default, not the recommendation |
| **GPT-5 Chat** | **GA** (Nov 24 2025, ex-GCC) | General | The GA GPT-5 you can say out loud |
| **GPT-5 Reasoning / Auto** | Preview | Deep / Auto | Do not call these "GPT-5" without the qualifier |
| **GPT-5.5 Chat** | **GA** (cross-geo) | General | Newer than GPT-5 Chat; GA as of July 2026 |
| **GPT-5.5 Reasoning** | Experimental (early access) | Deep | Not for production |
| **Claude Sonnet 4.5** | **Retired** | General | Was GA/recommended in June; retired since. Do not teach as current. |
| **Claude Sonnet 4.6** | **GA** (cross-geo) | General | Current recommended general-purpose Claude option |
| **Claude Sonnet 5** | **GA** (early access environment, new-experience agents only) | General | Newest Claude option; not available in classic-experience agents |
| **Claude Opus 4.6** | **GA** (cross-geo) | Deep | GA reasoning-class option |
| **Claude Opus 4.7** | **GA** (cross-geo) | Deep | Was Experimental in June; now GA |
| **Grok 4.1 Fast (Non-Reasoning)** | Experimental (early access) | General | New since June. Microsoft's own safety evaluation flags this model as less aligned -- mention only, do not demo |
| **Mistral Medium 3.5** | Experimental (cross-geo) | General | New since June |

**Gotchas to mention:** Anthropic (Claude), xAI (Grok), and Mistral models are external, not Azure-hosted, so a **tenant admin must approve** them first. Some models are cross-geo and may process data outside your region. Model selection lives on the agent's **Overview** tab and requires **generative orchestration**. The June doc's orchestration recommendation ("use Claude Sonnet 4.5") is stale -- re-verify the current MS-recommended orchestrator against the live docs page before stating one on stage, since this list is now shifting release-to-release.

Ref: <https://learn.microsoft.com/microsoft-copilot-studio/authoring-select-agent-model> · <https://learn.microsoft.com/microsoft-copilot-studio/authoring-select-external-response-model>

---

## The nine deltas, one line each

1. **Models.** GPT-5 Chat + GPT-5.5 Chat GA; Claude Sonnet 4.6, Sonnet 5 (new-experience only), Opus 4.6, and **Opus 4.7 (newly GA)** all GA; **Claude Sonnet 4.5 retired**. Grok 4.1 Fast and Mistral Medium 3.5 are new Experimental external options. <https://learn.microsoft.com/microsoft-copilot-studio/authoring-select-agent-model>
2. **Multi-agent.** "Add other agents" taxonomy; **A2A protocol is GA** (no preview banner); Foundry, Fabric, M365 SDK connections are preview. <https://learn.microsoft.com/microsoft-copilot-studio/authoring-add-other-agents> · <https://learn.microsoft.com/microsoft-copilot-studio/add-agent-agent-to-agent>
3. **MCP transport.** Streamable HTTP only, SSE retired after Aug 2025; onboarding wizard is the recommended path; MCP needs generative orchestration. <https://learn.microsoft.com/microsoft-copilot-studio/mcp-add-existing-server-to-agent>
4. **Agent evaluations.** Single-response evaluations **GA** (test sets ≤100 cases, activity maps, version compare, REST API + connector automation, 89-day retention). **Multi-turn evaluation is now GA** (was Preview as of the June materials; the projected June 2026 GA landed). <https://learn.microsoft.com/microsoft-copilot-studio/analytics-agent-evaluation-intro> · <https://learn.microsoft.com/microsoft-copilot-studio/analytics-agent-evaluation-multi-turn>
5. **VS Code extension.** **GA**: clone agent, edit `.mcs.yml`, Git/PR, deploy; Claude Code and GitHub Copilot named as authoring agents. <https://learn.microsoft.com/microsoft-copilot-studio/visual-studio-code-extension-overview>
6. **REST API tools.** Still **Preview**, now a first-class Tools-page type (Prompt / Agent flow / Computer use / Custom connector / MCP / REST API); OpenAPI v2 (v3 auto-downgrades). <https://learn.microsoft.com/microsoft-copilot-studio/agent-extend-action-rest-api>
7. **Knowledge sources.** Added **Azure AI Search** (vector + semantic ranker, VNet), **Bing Custom Search** (agent-level, overrides public sites), **Web Search** (Bing grounding), and the **`OnKnowledgeRequested`** custom-knowledge trigger (YAML only). Generative mode: 25 websites / 25 SharePoint URLs. <https://learn.microsoft.com/microsoft-copilot-studio/knowledge-copilot-studio>
8. **New agent experience.** Production-ready preview (June 2026): natural-language-first authoring, Microsoft IQ (org data grounding -- email, calendar, files, Teams, people), reusable skills, persistent memory. Runs alongside the classic experience this course teaches; agents cannot convert between the two. Mention it exists, do not rebuild the course around it yet. <https://learn.microsoft.com/microsoft-copilot-studio/agents-experience/overview>
9. **Deck filename.** The current deck is `warner-agents-pro-july-2026.pptx`.

---

## Labels are precise on purpose

One vocabulary across all materials. **GA** means production-ready. **Preview** means early access, not for production. **Experimental** means do not bet a demo on it.

| GA (safe to teach as production) | Preview (frame as "early, may change") | Experimental (mention only) |
|----------------------------------|----------------------------------------|------------------------------|
| GPT-5 Chat, GPT-5.5 Chat | GPT-5 Reasoning / Auto | GPT-5.5 Reasoning |
| Claude Sonnet 4.6, Sonnet 5, Opus 4.6, Opus 4.7 | Multi-turn evaluation is GA now -- see #4 above | Grok 4.1 Fast (Non-Reasoning) |
| A2A protocol | REST API tools | Mistral Medium 3.5 |
| Child + connected CS agents | Foundry / Fabric / M365 SDK connections | |
| Single-response + multi-turn evaluations | Real-time voice agents | |
| VS Code extension | New agent experience (agents-experience/overview) | |

> **Workload note:** the WAF teaching doc uses a **different agent set** (Customer Service, Onboarding, Document Processor) than this course's single **AZ-900 Cert-Prep Assistant**. Do not blur them. They are separate teaching workloads that share the same WAF lens.
>
> **Retired model note:** **Claude Sonnet 4.5** was this doc's recommended orchestrator as of June 2026. It is now retired. Do not repeat the June recommendation on stage -- verify the current MS-recommended orchestration model against <https://learn.microsoft.com/microsoft-copilot-studio/authoring-select-agent-model> before each delivery, since Copilot Studio's model lineup is turning over roughly every 4-6 weeks.
