# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Purpose

O'Reilly Live Learning course repo for "How to Create AI Agents Like a Pro" -- a 4-hour instructor-led course surveying the full AI agent landscape (no-code, low-code, code-first). This is Tim Warner's instructor source of truth and learner reference material.

**Important context:** The O'Reilly registration page (`docs/research/oreilly-reg-page-copy.md`) promises a Copilot Studio-only course. The actual delivery covers the broader agent ecosystem. The course structure below is authoritative; the reg page copy is legacy.

## Course Structure (4 Hours)

| Hour | Theme | Platforms & Tools |
|------|-------|--------------------|
| 1 | What "Agent" Means | M365 Copilot agents, declarative agents, taxonomy |
| 2 | Low-Code Agents | Copilot Studio, Antigrav, Claude Code / GitHub Copilot |
| 3 | Code-First Agents | Azure AI Foundry, Python, LangGraph, FastMCP |
| 4 | TBD | Best practices, MCP deep dive, or future trends |

The detailed instructor plan is in `docs/course-plan-february-2026.md`. The slide deck is `docs/warner-agents-pro-february-2026.pptx`.

## Two Content Trees

This repo contains **two generations** of course material:

1. **`src/copilot-studio-agent/`** -- The current primary content for Hour 2. Three progressive Copilot Studio agents (customer-service-assistant, employee-onboarding-agent, document-processor-agent) with topics, actions, knowledge sources, and SharePoint-uploadable demo data.

2. **`agents2/`** -- Archived snapshot of the predecessor repo (`timothywarner-org/agents2`), cloned without git history. Contains a working Python agent pipeline (`agents2/oreilly-agent-mvp/`), Claude Code skill definitions, Copilot Studio adaptive cards, per-hour teaching guides, and research docs. Treat as a reference library, not active development.

### Deployable `.mcs.yml` agents (top-level folders)

Distinct from the blueprint tree above, two top-level folders hold **real, deployable Copilot Studio agents** in the current `.mcs.yml` format (the schema the Copilot Studio VS Code extension reads, and a real Dataverse export shape). These import and run, not just document:

| Agent folder | Focus | Custom topics |
|-------------|-------|--------------|
| `CKA Exam Prep Assistant/` | Kubernetes CKA exam prep | Practice questions, lab generator, troubleshooting, kubectl help, exam domains |
| `RAI Advisor/` | Microsoft Responsible AI principles and how to operationalize them | Principles explainer, Impact Assessment, Transparency Note, content moderation, harm evaluation |

`RAI Advisor/` is the schema sibling of the CKA agent (same `cr84c` publisher prefix). It ships an XML system prompt, two icons (agent avatar + Teams/M365 store icon), and a repeatable Impact Assessment workflow (`docs/` bootstrap prompt + click-by-click guide). The agent's grounding carries verified RAI facts -- notably the Responsible AI Standard v2 has **17 goals, not 14**, and the per-prompt content-moderation slider went GA February 11, 2026. When editing any `.mcs.yml` here, delegate to the `@copilot-studio:*` sub-agents (the SessionStart hook requires it).

## Content Architecture

### Copilot Studio Agents (src/copilot-studio-agent/)

Three agents at increasing complexity -- all blueprint/documentation, no executable code:

| Agent | Level | Key Concepts |
|-------|-------|-------------|
| `customer-service-assistant/` | Beginner | Knowledge sources, generative answers, escalation |
| `employee-onboarding-agent/` | Intermediate | Auth, Power Automate flows, approvals |
| `document-processor-agent/` | Advanced | Autonomous triggers, AI Builder, event-driven |

Each agent folder follows the same scaffold:
- `topics/T##_TopicName/` -- trigger phrases, variables, build steps, blueprint YAML, test transcripts
- `actions/` -- Power Automate flow definitions and connector specs
- `knowledge/` -- SharePoint-ready demo documents (docx, pdf, xlsx, json) and upload instructions

### agents2/oreilly-agent-mvp/ (Reference Python Project)

A working LangGraph + CrewAI pipeline that processes issue JSON through PM, Dev, and QA agent stages. Has its own CLAUDE.md with build/test commands. Key commands (run from `agents2/oreilly-agent-mvp/`):

```powershell
.\scripts\setup.ps1                              # Create venv, install deps
.\scripts\run_once.ps1 mock_issues\issue_002.json # Run pipeline on a mock issue
pytest                                            # Run tests
pytest --cov=agent_mvp                           # Tests with coverage
ruff check src/ tests/                           # Lint
```

### GitHub Copilot Configurations (.github/)

Three Copilot agent definitions for VS Code:
- `agents/copilot-studio-expert.agent.md` -- Copilot Studio, Power Platform, CAF WAF expertise
- `agents/Python-Foundry.agent.md` -- Microsoft Agent Framework (Python) code generation
- `agents/Azure Architect.agent.md` -- Azure Well-Architected Framework guidance

Also: `prompts/copilot-studio-architect.prompt.md` (blueprint design) and `instructions/power-platform-connector-dev.instructions.md` (Custom Connectors JSON Schema).

## No Build System for Primary Content

The `src/copilot-studio-agent/` content is documentation and YAML blueprints only -- no build, lint, or test pipeline. Quality comes from cross-checking against `docs/course-plan-february-2026.md`, the registration page, and Microsoft documentation.

Markdown linting config exists at `.markdownlint.json` (line length 120, 2-space indent for lists).

## Authoring Conventions

- **Document structure:** Overview > Scenario > Success Metrics > Phased Build > Testing/Publishing > Sample Transcript
- **Topic folders:** `T##_TopicName` (e.g., `T01_ReturnsAndRefunds`)
- **Topic variables:** prefix with `t_` (e.g., `t_orderId`) or `Topic.` scope (e.g., `Topic.OrderNumber`)
- **Filenames:** lowercase with hyphens; Python files use snake_case
- **Headings:** Title Case, em dash subtitles
- **Lists:** compact with `-`; URLs in angle brackets `<...>`
- **Mermaid diagrams:** reuse existing fill color palette (`#e1f5fe`, `#c8e6c9`, `#ffcdd2`, `#fff3e0`) and grouped subgraph styles

## Platform Gotchas

### Copilot Studio
- Topic names must **never contain periods** -- breaks solution exports
- Event triggers require generative orchestration enabled and affect billing
- Test-panel interactions do not appear in Analytics
- SharePoint knowledge requires `Sites.Read.All` and `Files.Read.All` scopes
- Sources in a generative answers node override agent-level sources
- Most restrictive DLP policy wins when multiple apply

### Azure AI Foundry (Hour 3)
- Uses `azure-ai-projects` SDK with Hub + Project model
- Auth via `DefaultAzureCredential` (`az login` required)
- Env vars: `PROJECT_ENDPOINT`, `MODEL_DEPLOYMENT_NAME`

### LangGraph (Hour 3)
- State machines with `StateGraph`, nodes, and conditional edges
- Use `langgraph` package; avoid mixing with raw LangChain agent executors

### FastMCP (Hour 3)
- Decorator-based Python API; docstrings become tool descriptions, type hints become parameter schemas
- Servers run via `mcp run` or `mcp dev`; stdio transport by default
