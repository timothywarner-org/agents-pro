# CLAUDE.md

This file provides guidance for Claude Code when working in this repository.

## Build & Run Commands

```bash
# Setup (Windows PowerShell)
.\scripts\setup.ps1              # Creates venv, installs dependencies

# Run pipeline once
.\scripts\run_once.ps1           # Uses mock issue
.\scripts\run_once.ps1 mock_issues/issue_002.json  # Specific file

# Run folder watcher (auto-processes incoming/)
.\scripts\run_watcher.ps1

# Tests
pytest                           # Run all tests
pytest --cov=agent_mvp          # With coverage
pytest tests/test_schema.py -v  # Single test file

# Linting
ruff check src/ tests/          # Check for issues
ruff format src/ tests/         # Format code
```

## Architecture

This is an AI agents demo teaching orchestration patterns using LangGraph and CrewAI.

### Pipeline Flow

```
Issue JSON → [load_issue] → [pm] → [dev] → [qa] → [finalize] → Result JSON
```

The pipeline is defined in `src/agent_mvp/pipeline/graph.py` using LangGraph's `StateGraph`. Each node represents an agent stage:

- **load_issue**: Validates the input Issue JSON
- **pm**: PM agent analyzes issue, creates acceptance criteria and plan
- **dev**: Dev agent implements the plan with code drafts
- **qa**: QA agent reviews implementation, gives pass/fail/needs-human verdict
- **finalize**: Assembles PipelineResult JSON

### Key Files

| Path | Purpose |
|------|---------|
| `src/agent_mvp/pipeline/graph.py` | LangGraph state machine with 5 nodes |
| `src/agent_mvp/pipeline/crew.py` | CrewAI agent/task definitions |
| `src/agent_mvp/pipeline/prompts.py` | System prompts for each agent |
| `src/agent_mvp/models.py` | Pydantic models: Issue, PMOutput, DevOutput, QAOutput, PipelineResult |
| `src/agent_mvp/config.py` | Config loading, LLM provider factory |
| `src/agent_mvp/watcher/folder_watcher.py` | Polls incoming/ for new issues |

### Data Contracts

All data flows through Pydantic models in `models.py`:

- **Issue**: Input from mock files or MCP
- **PMOutput**: summary, acceptance_criteria, plan, assumptions
- **DevOutput**: files (path, content, language), notes
- **QAOutput**: verdict (pass/fail/needs-human), findings, suggested_changes
- **PipelineResult**: Combines all outputs with metadata

### LLM Providers

Configured via `LLM_PROVIDER` env var. The `Config.get_llm()` method returns a LangChain-compatible chat model:

- `anthropic`: Uses `langchain-anthropic` (default)
- `openai`: Uses `langchain-openai`
- `azure`: Uses `AzureChatOpenAI`

### Folder Watcher Pattern

The watcher polls `incoming/` for JSON files:
1. New file detected → validates against Issue schema
2. Runs pipeline graph
3. Writes result to `outgoing/{issue_id}_{timestamp}.json`
4. Moves input to `processed/`

## Code Style

- Python 3.11+
- Ruff for linting/formatting (line-length 100)
- Pydantic v2 for all data models
- Type hints throughout
- Docstrings on public functions

## Testing

Tests are in `tests/` directory. Key patterns:
- `test_schema.py`: Issue validation tests
- `test_fs_moves.py`: File system utility tests

Mock issues in `mock_issues/` are used for testing without API calls.
