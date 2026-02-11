# Debugging Guide

## VSCode Launch Configurations

This project includes comprehensive debugging configurations for easy data flow inspection.

### Quick Start

1. **Open VSCode** in the `agents2/` repository root (not the subfolder!)
2. Press `F5` or click the Run icon in the sidebar
3. Select a configuration from the dropdown
4. Set breakpoints by clicking in the gutter (left of line numbers)
5. Run and inspect variables, step through code

> **Important:** The launch configurations are set up for opening `C:\github\agents2\` in VSCode. All paths automatically resolve to the `oreilly-agent-mvp/` subfolder.

### Available Configurations (13 Total)

#### Interactive & CLI

**Interactive Menu**
- Launches the full interactive menu
- **Best for**: Testing user flows, demoing the system
- **Breakpoint tips**: Set in `oreilly-agent-mvp/src/agent_mvp/cli/interactive_menu.py`

**Run Once (Mock Issue 001-006)**
- Runs pipeline with specific mock issue
- **6 configurations** - one for each mock issue:
  - **001**: API rate limiting feature (timothywarner-org/agents2#101)
  - **002**: User authentication enhancement (timothywarner-org/agents2#102)
  - **003**: Data export functionality (timothywarner-org/agents2#103)
  - **004**: Dashboard performance (timothywarner-org/agents2#104)
  - **005**: Email notification system (timothywarner-org/agents2#105)
  - **006**: Search functionality (timothywarner-org/agents2#106)
- **Best for**: Testing full pipeline flow with different issue types
- **Breakpoint tips**: Set in `oreilly-agent-mvp/src/agent_mvp/pipeline/graph.py` nodes (pm_node, dev_node, qa_node)

**Folder Watcher**
- Starts the file watcher for event-driven processing
- **Best for**: Testing automated workflows, demo mode
- **Breakpoint tips**: Set in `oreilly-agent-mvp/src/agent_mvp/watcher/process_file.py`

**MCP Server**
- Launches the MCP server
- **Best for**: Testing MCP tools and resources
- **Breakpoint tips**: Set in `oreilly-agent-mvp/src/agent_mvp/mcp_server/server.py`

#### Testing

**Run Tests (All)**
- Executes all tests with debugging enabled
- **Best for**: Test-driven development
- **Breakpoint tips**: Set in test files or implementation

**Run Tests (Token Tracking)**
- Runs token tracking tests specifically
- **Best for**: Debugging token calculation logic

#### Advanced

**Debug Current File**
- Runs the currently open Python file
- **Best for**: Quick script testing

**Pipeline Graph (Step Through)**
- Runs pipeline with `stopOnEntry: true`
- **Best for**: Understanding execution flow from the start
- Execution pauses immediately at first line

### Configuration Summary Table

| # | Config Name | Purpose |
|---|-------------|---------|
| 1 | Interactive Menu | Main CLI menu with all options |
| 2 | Run Once (Mock Issue 001) | API Rate Limiting |
| 3 | Run Once (Mock Issue 002) | User Authentication |
| 4 | Run Once (Mock Issue 003) | Data Export |
| 5 | Run Once (Mock Issue 004) | Dashboard Performance |
| 6 | Run Once (Mock Issue 005) | Email Notifications |
| 7 | Run Once (Mock Issue 006) | Search Functionality |
| 8 | Folder Watcher | Watch incoming/ for files |
| 9 | MCP Server | Start MCP server |
| 10 | Run Tests (All) | All pytest tests |
| 11 | Run Tests (Token Tracking) | Token tracking tests |
| 12 | Debug Current File | Debug open file |
| 13 | Pipeline Graph (Step Through) | Step-by-step debugging |

## Debugging Tips

### Understanding Data Flow

1. **Pipeline State Flow**
   ```python
   # Set breakpoints at these key points:
   oreilly-agent-mvp/src/agent_mvp/pipeline/graph.py
   - Line ~60: load_issue_node (issue loaded)
   - Line ~100: pm_node (PM analysis)
   - Line ~170: dev_node (Dev implementation)
   - Line ~240: qa_node (QA review)
   - Line ~300: finalize_node (result creation)
   ```

2. **Token Tracking Flow**
   ```python
   # Watch token accumulation:
   oreilly-agent-mvp/src/agent_mvp/pipeline/graph.py
   - After each llm.invoke() call (see token extraction)
   - In finalize_node (see aggregation)

   oreilly-agent-mvp/src/agent_mvp/util/token_tracking.py
   - Line ~40: extract_token_usage (token capture)
   - Line ~90: calculate_cost (pricing calculation)
   - Line ~130: aggregate_pipeline_tokens (totals)
   ```

3. **Issue Loading**
   ```python
   # Trace issue from file to pipeline:
   oreilly-agent-mvp/src/agent_mvp/issue_sources/file_issue_source.py
   - Line ~25: fetch_issue (file read)

   oreilly-agent-mvp/src/agent_mvp/pipeline/run_once.py
   - Line ~60: run_pipeline (entry point)
   ```

### Inspecting Variables

When stopped at a breakpoint:

1. **Debug Console** (`Ctrl+Shift+Y`)
   ```python
   # Evaluate expressions:
   state["pm_output"]
   len(state.get("token_usages", []))
   result.metadata.token_usage.total_tokens
   ```

2. **Variables Pane**
   - Expand `state` to see pipeline state
   - Expand `response` to see LLM response
   - Watch `token_usage` to see per-agent costs

3. **Watch Expressions**
   - Add: `state.get("token_usages", [])`
   - Add: `sum(t["usage"]["total_tokens"] for t in state.get("token_usages", []))`
   - Add: `final_state["result"]["metadata"]["token_usage"]`

### Common Breakpoint Locations

#### See Token Usage Build Up
```python
# oreilly-agent-mvp/src/agent_mvp/pipeline/graph.py
# After each agent's llm.invoke() call:

def pm_node(state: PipelineState) -> PipelineState:
    # ...
    response = llm.invoke([...])
    token_usage = extract_token_usage(response, config.llm_model)  # <-- BREAKPOINT HERE
    # Inspect: token_usage.input_tokens, token_usage.output_tokens
```

#### See Agent Outputs
```python
# Right before returning from each node:

def pm_node(state: PipelineState) -> PipelineState:
    # ...
    pm_output = PMOutput(**pm_data)
    # <-- BREAKPOINT HERE
    return {**state, "pm_output": pm_output.model_dump()}
    # Inspect: pm_output.acceptance_criteria, pm_output.plan
```

#### See Final Aggregation
```python
# oreilly-agent-mvp/src/agent_mvp/pipeline/graph.py

def finalize_node(state: PipelineState) -> PipelineState:
    # ...
    pipeline_tokens = aggregate_pipeline_tokens(agent_tokens_list)  # <-- BREAKPOINT HERE
    # Inspect: pipeline_tokens.total_tokens, pipeline_tokens.cost_breakdown
```

### Step-Through Workflow

1. **Start with "Pipeline Graph (Step Through)"**
   - Execution pauses at first line
   - Press `F10` (Step Over) to go line-by-line
   - Press `F11` (Step Into) to enter function calls
   - Press `Shift+F11` (Step Out) to exit current function
   - Press `F5` (Continue) to run to next breakpoint

2. **Watch the State Build**
   - Add watch: `state.keys()`
   - Step through and see: `issue` -> `pm_output` -> `dev_output` -> `qa_output` -> `result`
   - When `result` exists, inspect `result["pm"]`, `result["dev"]`, and `result["qa"]` for the final outputs and `pass|fail|needs-human` verdict

3. **Inspect Token Costs**
   - Watch `state["token_usages"]` grow with each agent
   - See cost calculated in real-time

## Investigation Scenarios

### Scenario 1: Why is this agent using so many tokens?

1. Run: **Run Once (Mock Issue 001)**
2. Set breakpoint in `pm_node()` after `response = llm.invoke(...)`
3. Inspect:
   - `prompt` variable (input length)
   - `token_usage.input_tokens` (actual input count)
   - `token_usage.output_tokens` (response length)
4. Compare to other agents

### Scenario 2: How is the pipeline state flowing?

1. Run: **Pipeline Graph (Step Through)**
2. Add watch: `state`
3. Step through each node (F10)
4. See state grow: issue -> pm -> dev -> qa -> result

### Scenario 3: Testing token cost accuracy

1. Run: **Run Tests (Token Tracking)**
2. Set breakpoint in `test_calculate_cost_claude_sonnet`
3. Step through `calculate_cost()` function
4. Verify pricing lookup and calculation

### Scenario 4: End-to-end with real data

1. Run: **Interactive Menu**
2. Select option 2 (Load mock issue)
3. Choose any issue (001-006)
4. Watch console for token summary
5. Check `oreilly-agent-mvp/outgoing/` for JSON result and HTML report

### Scenario 5: Testing all mock issues

1. Run each **Run Once (Mock Issue 001-006)** config in sequence
2. Compare token usage across different issue types
3. Check `oreilly-agent-mvp/outgoing/` for all results

## Key Files for Debugging

```
oreilly-agent-mvp/src/agent_mvp/
|-- pipeline/
|   |-- graph.py          # Main pipeline orchestration (SET BREAKPOINTS HERE)
|   |-- run_once.py       # Entry point for CLI runs
|   |-- crew.py           # CrewAI agent definitions
|   +-- prompts.py        # Prompt templates (if modifying prompts)
|
|-- util/
|   |-- token_tracking.py # Token calculation logic (SET BREAKPOINTS HERE)
|   +-- html_report.py    # HTML report generation
|
|-- models.py             # Data models (inspect structure)
|-- config.py             # Configuration loading
|
+-- cli/
    +-- interactive_menu.py  # Menu system (for testing flows)
```

## VSCode Features to Use

### Debug Console Commands
```python
# While stopped at breakpoint:
dir(state)                          # See all state keys
state["issue"]["title"]             # Get issue title
len(state.get("token_usages", []))  # Count agents processed
import json; print(json.dumps(state["pm_output"], indent=2))  # Pretty print
```

### Call Stack
- See how you got to current line
- Click frames to jump to different stack levels
- Understand execution flow

### Conditional Breakpoints
- Right-click breakpoint -> Edit Breakpoint
- Add condition: `token_usage.total_tokens > 5000`
- Only stops when condition is true

### Logpoints
- Right-click gutter -> Add Logpoint
- Message: `PM tokens: {token_usage.total_tokens}`
- Logs without stopping execution

## Quick Reference

| Key | Action |
|-----|--------|
| `F5` | Start debugging / Continue |
| `F9` | Toggle breakpoint |
| `F10` | Step over (next line) |
| `F11` | Step into (enter function) |
| `Shift+F11` | Step out (exit function) |
| `Ctrl+Shift+F5` | Restart debugging |
| `Shift+F5` | Stop debugging |
| `Ctrl+K Ctrl+I` | Show hover info |

## Pro Tips

1. **Use the "Pipeline Graph (Step Through)" config first** - Understand execution flow
2. **Set breakpoints in all three agent nodes** - See how state builds
3. **Watch `state["token_usages"]`** - See token accumulation in real-time
4. **Inspect `final_state["result"]`** - See complete output before JSON write
5. **Use conditional breakpoints for high token usage** - Catch expensive calls
6. **Enable "Break on Exception"** - Catch errors immediately (Debug sidebar -> Breakpoints -> Check "Raised Exceptions")
7. **Try different mock issues** - Each has different characteristics (001-006)

## Troubleshooting

### "Module not found" errors
The launch configurations automatically set `PYTHONPATH` to `${workspaceFolder}/oreilly-agent-mvp/src`. Make sure you opened `agents2/` (not `oreilly-agent-mvp/`) in VSCode.

### Unicode/encoding errors on Windows
The configurations include `PYTHONIOENCODING: utf-8` to handle Rich console output. If you still see encoding errors, ensure you're using the provided launch configs.

### Breakpoint not hit
- Check `justMyCode: false` in launch.json (already set)
- Ensure file is actually executed
- Try `stopOnEntry: true` to start from beginning

## Further Reading

- [VSCode Python Debugging](https://code.visualstudio.com/docs/python/debugging)
- [Debugpy Documentation](https://github.com/microsoft/debugpy)
- [LangGraph State Inspection](https://langchain-ai.github.io/langgraph/concepts/low_level/#state)

---

**Happy Debugging!**
