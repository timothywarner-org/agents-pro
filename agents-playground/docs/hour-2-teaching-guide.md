# Hour 2 Teaching Guide: Run, Test, and Debug

**Goal:** Students run the full agent pipeline, understand how to test it, and master VSCode debugging.

**Time:** 60 minutes

---

## Opening (3 minutes)

**What We're Doing This Hour:**

1. Run the complete PM → Dev → QA pipeline
2. Understand the data flow through the system
3. Write and run tests
4. Master VSCode debugging with breakpoints
5. Inspect state and token usage in real-time

**Key Message:** "You can't fix what you can't see. Debugging agents requires understanding the state at every step."

---

## Run the Pipeline (15 minutes)

### Setup Verification (5 minutes)

**Everyone check their environment:**

```bash
cd agents2/oreilly-agent-mvp

# Check Python
python --version  # Should be 3.11+

# Check virtual environment
ls .venv  # Should exist

# Activate venv
source .venv/Scripts/activate  # Git Bash
# OR
.\.venv\Scripts\Activate.ps1   # PowerShell

# Check dependencies
pip list | grep langchain
```

**Verify API key:**

```bash
cat .env | grep -E "ANTHROPIC|OPENAI"
# Should show your key (no spaces, no quotes)
```

### First Pipeline Run (10 minutes)

**Launch the interactive menu:**

```bash
agent-menu
```

**Walk through the menu options:**

```
╔═══════════════════════════════════════╗
║     O'Reilly Agent MVP                ║
╠═══════════════════════════════════════╣
║  1. Request an issue from GitHub      ║
║  2. Load a mock issue                 ║
║  3. Watch incoming/ folder            ║
║  4. View recent results               ║
║  5. Exit                              ║
╚═══════════════════════════════════════╝
```

**Demo with mock issue:**

1. Select option `2` (Load a mock issue)
2. Choose `issue_001.json` (API Rate Limiting)
3. Confirm `y` to process

**While it runs, narrate:**

- "PM Agent is analyzing the issue..."
- "Dev Agent is writing code based on PM's plan..."
- "QA Agent is reviewing the implementation..."
- "Each agent adds to the pipeline state"

**Show the output:**

```bash
# List results
ls outgoing/

# View the latest result
cat outgoing/result_*.json | jq .

# Key sections to point out:
cat outgoing/result_*.json | jq .pm.summary
cat outgoing/result_*.json | jq .dev.files
cat outgoing/result_*.json | jq .qa.verdict
```

### Understanding the Mock Issues

**Available mock issues (use for testing):**

| Issue | Description | Complexity |
| --- | --- | --- |
| 001 | API Rate Limiting | Medium |
| 002 | User Authentication | High |
| 003 | Data Export | Low |
| 004 | Dashboard Performance | High |
| 005 | Email Notifications | Medium |
| 006 | Search Functionality | Medium |

**Say:** "Each mock issue tests different agent behaviors. Use them to verify changes."

---

## Understanding the Architecture (10 minutes)

### Pipeline State Flow

**Draw on whiteboard:**

```
┌──────────────┐
│ PipelineState│
├──────────────┤
│ run_id       │
│ issue        │ ← load_issue fills this
│ pm_output    │ ← pm_node fills this
│ dev_output   │ ← dev_node fills this
│ qa_output    │ ← qa_node fills this
│ token_usages │ ← each node appends
│ result       │ ← finalize_node fills this
└──────────────┘
```

**Key insight:** "State is a bucket that passes from node to node. Each agent reads what it needs and adds its output."

### The Graph Definition

**Show the code:**

```python
# src/agent_mvp/pipeline/graph.py (lines 312-330)
def create_pipeline_graph() -> StateGraph:
    builder = StateGraph(PipelineState)

    # Add nodes
    builder.add_node("load_issue", load_issue_node)
    builder.add_node("pm", pm_node)
    builder.add_node("dev", dev_node)
    builder.add_node("qa", qa_node)
    builder.add_node("finalize", finalize_node)

    # Define edges (linear flow)
    builder.set_entry_point("load_issue")
    builder.add_edge("load_issue", "pm")
    builder.add_edge("pm", "dev")
    builder.add_edge("dev", "qa")
    builder.add_edge("qa", "finalize")
    builder.add_edge("finalize", END)

    return builder.compile()
```

**Visual representation:**

```
load_issue → pm → dev → qa → finalize → END
```

**Ask:** "What would you change to make PM and QA run in parallel?"

---

## Running Tests (12 minutes)

### Test Suite Overview (3 minutes)

**Show the test structure:**

```bash
tree tests/
# tests/
# ├── test_schema.py        # Pydantic model validation
# ├── test_fs_moves.py      # File system utilities
# ├── test_mcp_server.py    # MCP server validation
# └── conftest.py           # Shared fixtures
```

**Say:** "Tests verify contracts. When you change code, tests catch regressions."

### Run All Tests (4 minutes)

**Basic test run:**

```bash
pytest
```

**With coverage:**

```bash
pytest --cov=agent_mvp
```

**Expected output:**

```
========================= test session starts =========================
collected 12 items

tests/test_schema.py ....                                        [ 33%]
tests/test_fs_moves.py ....                                      [ 66%]
tests/test_mcp_server.py ....                                    [100%]

========================= 12 passed in 2.34s ==========================
```

**Verbose mode (see each test):**

```bash
pytest -v
```

### Run Specific Tests (5 minutes)

**Single file:**

```bash
pytest tests/test_schema.py -v
```

**Single test function:**

```bash
pytest tests/test_schema.py::test_issue_validation -v
```

**Pattern matching:**

```bash
pytest -k "token" -v  # All tests with "token" in name
```

**Hands-on:** "Everyone run the schema tests and verify they pass."

---

## VSCode Debugging (20 minutes)

### Open VSCode Correctly (2 minutes)

**IMPORTANT:** Open the `agents2/` folder, NOT `oreilly-agent-mvp/`.

```bash
code c:/github/agents2
```

**Why?** The launch configurations set PYTHONPATH relative to this root.

### Available Debug Configurations (3 minutes)

**Press F5 and see the dropdown:**

| Config | Purpose | Best For |
| --- | --- | --- |
| Interactive Menu | Full menu with all options | Testing user flows |
| Run Once (001-006) | Pipeline with specific mock | Testing full flow |
| Folder Watcher | Event-driven processing | Testing automation |
| MCP Server | MCP tools/resources | Testing MCP |
| Run Tests (All) | All pytest tests | TDD workflow |
| Pipeline Graph (Step Through) | Pauses immediately | Learning execution flow |

**Say:** "Start with 'Pipeline Graph (Step Through)' -- it pauses at the first line so you can step through everything."

### Essential Keyboard Shortcuts (2 minutes)

| Key | Action |
| --- | --- |
| **F5** | Start debugging / Continue |
| **F9** | Toggle breakpoint |
| **F10** | Step Over (next line) |
| **F11** | Step Into (enter function) |
| **Shift+F11** | Step Out (exit function) |
| **Ctrl+Shift+Y** | Open Debug Console |

### Demo: Step Through the Pipeline (8 minutes)

**Setup:**

1. Open VSCode in `agents2/`
2. Open `oreilly-agent-mvp/src/agent_mvp/pipeline/graph.py`
3. Set breakpoints at:
   - Line ~100: Inside `pm_node()` after `response = llm.invoke()`
   - Line ~170: Inside `dev_node()` after `response = llm.invoke()`
   - Line ~240: Inside `qa_node()` after `response = llm.invoke()`

**Run:**

1. Press F5
2. Select "Run Once (Mock Issue 001)"
3. When it pauses at pm_node:
   - **Variables pane:** Expand `state` to see `issue` data
   - **Debug Console:** Type `state["issue"]["title"]`
   - Press F5 to continue to next breakpoint

4. When it pauses at dev_node:
   - **Check:** `state["pm_output"]` now exists
   - **Debug Console:** `state["pm_output"]["plan"]`
   - Press F5

5. When it pauses at qa_node:
   - **Check:** Both `pm_output` and `dev_output` exist
   - **Debug Console:** `len(state["dev_output"]["files"])`

**Key insight:** "Watch state.keys() grow: issue → pm_output → dev_output → qa_output → result"

### Hands-On: Debug Token Tracking (5 minutes)

**Set breakpoint in token tracking:**

Open `oreilly-agent-mvp/src/agent_mvp/util/token_tracking.py`

Set breakpoint at line ~40 (inside `extract_token_usage`):

```python
def extract_token_usage(response, model_name: str) -> Optional[TokenUsage]:
    # BREAKPOINT HERE
    ...
```

**Run with Mock Issue 001:**

When it stops:
- Inspect `response` object
- Check `response.usage_metadata`
- See `input_tokens` and `output_tokens`

**Debug Console commands:**

```python
response.usage_metadata
response.content[:200]  # First 200 chars of response
```

---

## Common Debugging Scenarios (5 minutes)

### Scenario 1: "Why is QA failing?"

1. Run "Run Once (Mock Issue 001)"
2. Set breakpoint in `qa_node` before return
3. Inspect `qa_data["verdict"]` and `qa_data["findings"]`
4. Check if findings are reasonable or hallucinated

### Scenario 2: "Token costs seem high"

1. Add watch expression: `state.get("token_usages", [])`
2. Step through each agent
3. Compare input_tokens vs output_tokens
4. Identify which agent is expensive

### Scenario 3: "Pipeline hangs at dev_node"

1. Enable "Break on Exception" (Debug sidebar → Breakpoints)
2. Run pipeline
3. When it hangs, press pause button
4. Check Call Stack to see where it's stuck
5. Often: API timeout or rate limiting

### Scenario 4: "JSON parsing error"

1. Set breakpoint at `_extract_json()` function
2. Step through regex matching
3. Inspect `response.content` for malformed JSON
4. Check if LLM returned natural language instead

---

## Wrap-Up (5 minutes)

### What We Accomplished

- Ran the full PM → Dev → QA pipeline
- Understood state flow through the graph
- Ran tests with pytest
- Mastered VSCode debugging with breakpoints
- Inspected variables and token usage in real-time

### What's Next (Hour 3)

- Configure MCP server for external integration
- Add a new feature: RAG vector source
- Vibe coding with Claude Code
- Local, cheap vector database setup

### Quick Reference Card

**Run pipeline:**
```bash
agent-menu
```

**Run tests:**
```bash
pytest -v
pytest --cov=agent_mvp
```

**Debug in VSCode:**
1. F5 → Select config
2. F9 → Toggle breakpoint
3. F10 → Step over
4. Ctrl+Shift+Y → Debug console

**Inspect state:**
```python
state.keys()
state["pm_output"]["plan"]
state.get("token_usages", [])
```

---

## Teaching Tips

### If VSCode Debugging Doesn't Work

**Check:**
1. Opened `agents2/` not `oreilly-agent-mvp/`
2. Python extension installed
3. Correct Python interpreter selected (bottom status bar)
4. `.venv` activated

**Fix PYTHONPATH issues:**
```bash
# In terminal before launching VSCode
export PYTHONPATH=$PWD/oreilly-agent-mvp/src
code .
```

### If Tests Fail

**Common issues:**

1. Missing dependencies: `pip install -e .`
2. Missing `.env` file: Copy from `.env.example`
3. API key issues: Check for spaces/quotes

### If Pipeline Hangs

**Causes:**
- API rate limiting (wait 60 seconds)
- Network issues (check connectivity)
- Model overload (try different provider)

**Fix:** Add timeout to `llm.invoke()`:

```python
response = llm.invoke([...], timeout=60)
```

### Time Management

- If setup takes too long: Demo on your screen
- If students are ahead: Challenge them to add a 4th agent
- If debugging is confusing: Focus on just F5/F10/F9

---

## Advanced: Conditional Breakpoints

**Right-click breakpoint → Edit Breakpoint → Expression:**

```python
# Only stop if tokens are high
token_usage.total_tokens > 5000

# Only stop on errors
state.get("error") is not None

# Only stop for specific agent
agent_name == "QA"
```

---

## File Reference

| File | Purpose | Key Lines |
| --- | --- | --- |
| `pipeline/graph.py` | Graph definition and nodes | 44-70 (state), 100-150 (pm_node), 312-330 (graph) |
| `pipeline/prompts.py` | Agent prompts | 8-20 (PM), 78-90 (Dev), 138-150 (QA) |
| `util/token_tracking.py` | Token extraction and cost | 40 (extract), 90 (cost) |
| `models.py` | Pydantic data models | 15-45 (Issue), 40-60 (PMOutput) |
| `config.py` | Environment and LLM config | 15-30 (env vars), 50-70 (get_llm) |

---

**You got this! Debug like you mean it.**
