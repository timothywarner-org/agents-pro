# Microsoft Copilot Studio Training Resources

Curated Microsoft Learn assets to accelerate building low-code agents that complement the O'Reilly course.

## Core Learning Paths

- [Microsoft Copilot Studio training catalog](https://learn.microsoft.com/training/browse/?terms=copilot%20studio&products=ms-copilot) - Full listing of guided modules and learning paths focused on Copilot Studio fundamentals and advanced capabilities.
- [Build an agent with generative AI from the ground up](https://learn.microsoft.com/microsoft-copilot-studio/fundamentals-get-started) - Step-by-step walkthrough for creating low-code agents using natural language and Copilot assistance.
- [Use generative AI to build agents fast](https://learn.microsoft.com/microsoft-copilot-studio/nlu-gpt-overview) - Best practices for leveraging generative authoring and generative answers inside Copilot Studio.

## Hands-on Workshops & Videos

- [Mastering Copilot Studio (video series)](https://learn.microsoft.com/shows/mastering-copilot-studio) - Microsoft-hosted show covering agent customization, integrations, and deployment scenarios.
- [Agent in a Day events](https://aka.ms/nextAgIAD) - Free instructor-led workshops teaching end-to-end agent design, topic authoring, and automation with low-code patterns.

## Best Practice Guidance

- [Plan a conversational AI project](https://learn.microsoft.com/microsoft-copilot-studio/guidance/project-best-practices) - Project planning checklist for aligning stakeholders, success metrics, and deployment environments.
- [Topics best practices](https://learn.microsoft.com/microsoft-copilot-studio/guidance/topics-overview) - Guidance on structuring conversational topics, trigger phrases, and system topic usage.
- [Measure and improve agent engagement](https://learn.microsoft.com/microsoft-copilot-studio/guidance/measuring-engagement) - Analytics strategies for tracking resolution rates, satisfaction, and continuous improvements.

## Choosing a Model

- [Select an agent model](https://learn.microsoft.com/microsoft-copilot-studio/authoring-select-agent-model) - Region availability table for the generative AI models you can pick as the agent orchestration model. As of July 2026, **GPT-5 Chat** (rolled out Nov 24, 2025) and **GPT-5.5 Chat** are generally available, as are **Claude Sonnet 4.6**, **Claude Opus 4.6 (Deep)**, and **Claude Opus 4.7 (Deep)**. **Claude Sonnet 5** is GA but only in new-experience agents, not the classic authoring surface this course teaches. **GPT-5 Reasoning (Deep)**, **GPT-5 Auto**, and **GPT-5.5 Reasoning** remain **Preview** or **Experimental**. **Claude Sonnet 4.5 has retired** - do not teach it as current.
- [Select an external response model](https://learn.microsoft.com/microsoft-copilot-studio/authoring-select-external-response-model) - Companion reference for choosing the model used for external responses.

> **Orchestration model note:** Per the Dynamics 365 finance and operations [Build an agent with MCP](https://learn.microsoft.com/dynamics365/fin-ops-core/dev-itpro/copilot/build-agent-mcp) guidance, do **not** use **GPT-4.1** as the orchestration model for Copilot Studio agents, even though it remains the platform **Default**. That page's named recommendation (**Claude Sonnet 4.5**) is stale as of July 2026 - the model retired. Copilot Studio's lineup turns over every 4-6 weeks, so **re-verify the current recommended orchestrator** against the model-selection page before each delivery rather than quoting any cached recommendation. **GPT-5 Chat** remains a safe GA fallback.

## Extending Low-Code Agents

- [Use agent flows with your agent](https://learn.microsoft.com/microsoft-copilot-studio/advanced-flow) - How to add Power Automate flows and low-code automation steps to Copilot Studio agents.
- [Use connectors](https://learn.microsoft.com/microsoft-copilot-studio/advanced-connectors) - Catalog of supported connectors and guidance on securing integrations.
- [Add tools to custom agents](https://learn.microsoft.com/microsoft-copilot-studio/advanced-plugin-actions) - Instructions for incorporating external tools and extending agent capabilities.
- [Extend an agent with a REST API tool](https://learn.microsoft.com/microsoft-copilot-studio/agent-extend-action-rest-api) - **Preview** guidance for adding tools from a REST API. Requires an **OpenAPI v2** spec (v3 specs are auto-downgraded to v2).

## Model Context Protocol (MCP)

- [Add an existing MCP server to an agent](https://learn.microsoft.com/microsoft-copilot-studio/mcp-add-existing-server-to-agent) - Walkthrough for the **MCP onboarding wizard** (Tools > Add a tool > New tool > Model Context Protocol) with None, API key, and OAuth 2.0 auth options.
- [Extend an agent with MCP actions](https://learn.microsoft.com/microsoft-copilot-studio/agent-extend-action-mcp) - Reference for MCP tool actions. MCP supports only the **Streamable HTTP** transport; **SSE transport is deprecated** and is no longer supported for MCP after August 2025.

## Multi-Agent Orchestration

- [Add other agents](https://learn.microsoft.com/microsoft-copilot-studio/authoring-add-other-agents) - Overview of multi-agent patterns. **Child agents, connected (in-environment) agents, and agent-to-agent (A2A) connections are generally available** (A2A reached GA in April 2026).
- [Add an agent-to-agent (A2A) connection](https://learn.microsoft.com/microsoft-copilot-studio/add-agent-agent-to-agent) - Connect an external agent over the A2A protocol.
- [Add a Microsoft Foundry agent](https://learn.microsoft.com/microsoft-copilot-studio/add-agent-foundry-agent) - **Preview** external connection to a Microsoft Foundry agent.
- [Add a Fabric data agent](https://learn.microsoft.com/microsoft-copilot-studio/add-agent-fabric-data-agent) - **Preview** external connection to a Fabric data agent.
- [Add an agent built with the Microsoft 365 Agents SDK](https://learn.microsoft.com/microsoft-copilot-studio/add-agent-microsoft-365-agents-sdk-agent) - **Preview** external connection to an Agents SDK agent.

## Testing & Tooling

- [Visual Studio Code extension overview](https://learn.microsoft.com/microsoft-copilot-studio/visual-studio-code-extension-overview) - The **Microsoft Copilot Studio extension for Visual Studio Code is generally available** as of January 2026. Author agents and edit YAML from VS Code.
- Agent evaluations: **agent evaluations reached general availability in March 2026** using customizable test sets, and **multi-turn conversation tests reached GA** as well (introduced March 2026 as Preview; GA confirmed as of July 2026). Up to 20 test cases per conversational test set, with conversation-level and turn-level assertions.

## Adoption & Scenarios

- [Copilot Studio Adoption hub](https://aka.ms/adoptcopilotstudio) - Templates, communication packs, and governance resources for rolling out Copilot Studio across an organization.
- [Copilot Studio scenarios library](https://adoption.microsoft.com/ai-agents/copilot-studio/#scenarios) - Downloadable playbooks illustrating common low-code agent scenarios for departments like HR, support, and operations.

## What's New

- [Copilot Studio What's new](https://learn.microsoft.com/microsoft-copilot-studio/whats-new) - Running log of feature releases. Check here for the latest model availability and feature changes.
