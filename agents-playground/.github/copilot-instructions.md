# Copilot Instructions for agents2 (O'Reilly AI Agents MVP)

## Project Overview
- **Purpose:** Demonstrates production-ready AI agent patterns for issue triage and implementation draft pipelines, using LangGraph (stateful orchestration) and CrewAI (multi-agent collaboration: PM, Dev, QA).
- **Structure:**
  - `oreilly-agent-mvp/` is the main Python package.
    - `src/agent_mvp/` contains all core logic, organized by function:
      - `pipeline/` — pipeline orchestration (LangGraph, CrewAI agents)
      - `watcher/` — folder watcher for event-driven execution
      - `issue_sources/`, `util/` — supporting modules
    - `incoming/`, `outgoing/`, `processed/` — folders for file-based workflow triggers and outputs

## Key Workflows
- **Run the pipeline once:**
  - `python -m agent_mvp.pipeline.run_once` or use the script: `agent-mvp`
- **Run the folder watcher (event-driven):**
  - `python -m agent_mvp.watcher.folder_watcher` or use the script: `agent-watcher`
- **Environment:**
  - Copy `.env.example` to `.env` and set LLM provider credentials (Anthropic, OpenAI, or Azure)
- **Dependencies:**
  - Managed via `pyproject.toml` (see `[project.dependencies]`)

## Patterns & Conventions
- **Agents:** Defined in `pipeline/` (PM, Dev, QA) and orchestrated via LangGraph
- **Event-driven:** New files in `incoming/` trigger processing; results go to `outgoing/` and `processed/`
- **No business logic in `__init__.py`** — only imports and metadata
- **Scripts registered in `pyproject.toml`** for CLI use
- **Secrets:** Never commit `.env` or secrets; use environment variables

## Integration Points
- **LLM Providers:** Anthropic, OpenAI, Azure (configurable via `.env`)
- **MCP/GitHub:** Optional integration via `.mcp.json` for advanced workflows

## Examples
- To process a new issue file: place it in `incoming/` and run the watcher or pipeline script
- To add a new agent: extend `pipeline/` and update orchestration logic

## References
- See `pyproject.toml` for dependencies, scripts, and build config
- See `.env.example` for environment setup
- See `src/agent_mvp/` for all core logic

---
_Keep instructions concise and up-to-date. Update this file if workflows or architecture change._
