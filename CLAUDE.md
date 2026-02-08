# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Purpose

O'Reilly Live Learning course repository for "How to Create AI Agents Like a Pro" -- a 4-hour instructor-led course that surveys the full AI agent landscape, from no-code to low-code to code-first. The repo is the instructor's source of truth and learner reference material.

**Important context:** The O'Reilly registration page (`docs/research/oreilly-reg-page-copy.md`) promises a Copilot Studio-only course. The actual delivery has been expanded to cover the broader agent ecosystem. When in doubt, the course structure below is authoritative; the reg page copy is legacy.

## Course Structure (4 Hours)

| Hour | Theme | Key Platforms & Tools |
|------|-------|-----------------------|
| 1 | What "Agent" Means | M365 Copilot agents (custom GPTs), declarative agents, agent landscape taxonomy |
| 2 | Low-Code Agents | Copilot Studio, Antigrav, Claude Code / GitHub Copilot agents |
| 3 | Code-First Agents | Azure AI Foundry agents, Python, LangGraph, FastMCP |
| 4 | TBD | Best practices, MCP deep dive, future trends (finalize before delivery) |

### Hour 1 -- Agent Landscape & M365 Copilot

Demystify the word "agent." Show where M365 Copilot agents (custom GPTs, declarative agents) fit vs. autonomous agents, chatbots, and RPA. Hands-on: learners interact with a pre-built M365 Copilot agent.

### Hour 2 -- Low-Code Agents

Build agents without writing traditional code. Copilot Studio (topics, triggers, knowledge, generative answers), Antigrav for rapid prototyping, and Claude Code / GitHub Copilot as developer-facing agents. Demo each platform; learners build in Copilot Studio.

### Hour 3 -- Code-First Agents

Write agent logic in Python. Cover Azure AI Foundry agent creation, LangGraph for multi-step orchestration, and FastMCP for exposing tools via Model Context Protocol. Learners follow along with a Python example.

### Hour 4 -- TBD

Placeholder. Candidate topics: cross-cutting best practices (testing, observability, security), MCP deep dive, future trends in agentic AI. Finalize based on learner profile and current momentum.

## Architecture

### Content Organization

```
agents-pro/
├── docs/                           # Course plans, research, reference material
│   ├── course-plan.md              # Instructor segment breakdown (update for new structure)
│   └── research/                   # Registration page copy, competitive research
├── copilot-studio-agents/          # Hour 2 -- Copilot Studio content (existing)
│   ├── _labs/                      # Hands-on lab guides
│   ├── _topics/                    # Topic blueprint conventions
│   ├── _automations/               # Power Automate flow templates
│   ├── customer-service-assistant/ # Beginner agent build
│   ├── employee-onboarding-agent/  # Intermediate agent build
│   └── document-processor-agent/   # Advanced agent build
└── .github/
    ├── agents/                     # GitHub Copilot agent definitions
    ├── prompts/                    # Copilot prompt templates
    └── instructions/               # Copilot coding instructions
```

**Planned new directories** (create as content is developed):
- `hour-1-agent-landscape/` -- M365 Copilot agent demos, declarative agent examples, taxonomy diagrams
- `hour-2-low-code/` -- Copilot Studio (migrated from `copilot-studio-agents/`), Antigrav, Claude Code agent configs
- `hour-3-code-first/` -- Python examples, LangGraph graphs, FastMCP server, Azure AI Foundry agent setup
- `hour-4-tbd/` -- Best practices checklists, MCP reference, or future trends content

### Copilot Studio Agent Scaffold (Hour 2)

Every Copilot Studio agent folder follows:
- `topics/` -- Conversation paths with trigger phrases and dialog logic (YAML blueprints)
- `actions/` -- Power Automate flows, connectors, tool integrations
- `knowledge/` -- Data sources, generative answers config, SharePoint/OneDrive references

Topic folders use `T##_` prefix for sequencing. Each contains:
- `README.md` -- Overview and learning objectives
- `topic.build.md` -- Step-by-step Copilot Studio build instructions
- `topic.blueprint.yaml` -- Truth table for triggers, variables, branching
- `assets/` -- Sample payloads, test transcripts, adaptive card templates

## Authoring Conventions

### Document Structure

Long-form guides follow: Overview > Scenario > Success Metrics > Phased Build Instructions > Testing/Publishing > Sample Transcript/Log

### Naming Standards

- Topic folders: `T##_TopicName` (e.g., `T01_ReturnsAndRefunds`)
- Topic variables: prefix with `t_` (e.g., `t_orderId`)
- Sample payloads: `snake_case` keys
- Filenames: lowercase with hyphens
- Python files: snake_case per PEP 8

### Style

- Headings: Title Case, em dash pattern for subtitles
- Lists: compact with `-`
- URLs: inside angle brackets `<...>`
- ASCII default; preserve existing em dashes
- Mermaid diagrams: reuse existing color palette and grouped subgraph styles

## Platform-Specific Notes

### Copilot Studio

- **Topic names**: Avoid periods (`.`) -- breaks solution exports
- **Event triggers**: Require generative orchestration enabled; affect billing
- **Analytics**: Test-panel interactions don't appear in Analytics
- **DLP**: Most restrictive policy wins when multiple apply

### Azure AI Foundry (Hour 3)

- Agents are created via the Azure AI Projects SDK (`azure-ai-projects`)
- Requires an Azure AI Hub + Project resource
- Connection strings stored in environment variables, never committed

### LangGraph (Hour 3)

- State machines for multi-step agent orchestration
- Graphs defined as Python code with nodes and edges
- Use `langgraph` package; avoid mixing with raw LangChain agent executors

### FastMCP (Hour 3)

- Python framework for Model Context Protocol servers
- Exposes tools, resources, and prompts to LLM clients
- Use `fastmcp` package; servers run via `mcp run` or `mcp dev`

## GitHub Copilot Configurations

- `.github/agents/copilot-studio-expert.agent.md` -- Expert on Copilot Studio, Power Platform, Power Automate, and CAF WAF
- `.github/prompts/copilot-studio-architect.prompt.md` -- Design and review prompt for agent blueprints
- `.github/instructions/power-platform-connector-dev.instructions.md` -- Power Platform Custom Connectors JSON Schema development

## No Build System (Yet)

The Copilot Studio content is documentation and YAML blueprints only. As code-first content (Hour 3) is added, expect Python projects with `pyproject.toml` or `requirements.txt`. Quality for documentation content comes from cross-checking against course proposal, marketing materials, and Microsoft documentation.

## Key External References

- [Copilot Studio Documentation](https://learn.microsoft.com/en-us/microsoft-copilot-studio/)
- [Power Platform Well-Architected](https://learn.microsoft.com/power-platform/well-architected/)
- [Azure AI Foundry](https://learn.microsoft.com/en-us/azure/ai-foundry/)
- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [Model Context Protocol](https://modelcontextprotocol.io)
- [FastMCP](https://github.com/jlowin/fastmcp)
- [M365 Copilot Extensibility](https://learn.microsoft.com/en-us/microsoft-365-copilot/extensibility/)
- [Declarative Agents](https://learn.microsoft.com/en-us/microsoft-365-copilot/extensibility/overview-declarative-agent)
