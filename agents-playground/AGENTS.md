# Repository Guidelines

## Project Structure & Module Organization

- `oreilly-agent-mvp/` is the primary Python project for the agent pipeline.
- `docs/` and `images/` hold course materials and supporting assets.
- `.github/` contains automation and repository settings.
- `oreilly-agent-mvp/` key paths:
  - `src/agent_mvp/` holds core code (pipeline, issue sources, watcher, utilities).
  - `incoming/`, `outgoing/`, `processed/` implement the file-based workflow.
  - `mock_issues/` provides sample issue JSON for local runs.
  - `scripts/` contains PowerShell helpers.
  - `tests/` contains pytest tests.

## Build, Test, and Development Commands

From `oreilly-agent-mvp/`:

- `.\scripts\setup.ps1` sets up the virtual environment and installs deps.
- `python -m agent_mvp.pipeline.run_once` runs the pipeline once.
- `.\scripts\run_once.ps1 [mock_issues\issue_002.json]` runs with a mock file.
- `.\scripts\run_watcher.ps1` watches `incoming/` for new issue files.
- `pytest` runs the test suite.
- `pytest --cov=agent_mvp` runs tests with coverage.

If installed in editable mode, you can also use `agent-mvp` and `agent-watcher`.

## Coding Style & Naming Conventions

- Python 3.11+, 4-space indentation, `snake_case` for modules/functions.
- `ruff` is the lint tool (line length 100, target `py311`, E/F/I/W rules).
- Test files follow `test_*.py` naming in `tests/`.

## Testing Guidelines

- Framework: `pytest` with optional coverage via `pytest-cov`.
- Prefer tests around file utilities, schema validation, and pipeline steps.
- Use `mock_issues/` fixtures; avoid network calls in tests.

## Commit & Pull Request Guidelines

- Commit messages are short and imperative (examples: "Add ...", "Refactor ...", "Update ...").
- Merge commits follow the default "Merge branch ..." format.
- PRs should describe behavior changes, link the issue, and include test results.
- If output changes, attach a sample `outgoing/` JSON or a CLI screenshot.

## Security & Configuration Tips

- Never commit secrets. Copy `.env.example` to `.env` and set one provider.
- MCP templates live in `.mcp.json` and `oreilly-agent-mvp/.vscode/mcp.json`.
