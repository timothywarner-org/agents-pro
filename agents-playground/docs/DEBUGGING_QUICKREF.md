# 🐛 VSCode Debugging Quick Reference

> **Important:** Open `C:\github\agents2\` in VSCode (NOT the `oreilly-agent-mvp/` subfolder). All paths automatically resolve to the subfolder.

## Launch Configurations (Press F5)

| # | Config | Purpose | Key Breakpoint Locations |
|---|--------|---------|-------------------------|
| 1 | 🎯 **Interactive Menu** | Test user flows & menu navigation | `oreilly-agent-mvp/src/agent_mvp/cli/interactive_menu.py` |
| 2-7 | 🚀 **Run Once (001-006)** | Full pipeline with specific mock | `oreilly-agent-mvp/src/agent_mvp/pipeline/graph.py` nodes |
| 8 | 👁️ **Folder Watcher** | Event-driven file processing | `oreilly-agent-mvp/src/agent_mvp/watcher/process_file.py` |
| 9 | 🔧 **MCP Server** | MCP tools/resources testing | `oreilly-agent-mvp/src/agent_mvp/mcp_server/server.py` |
| 10-11 | 🧪 **Run Tests** | TDD & test debugging | Test files or implementation |
| 12 | 🔍 **Debug Current File** | Run whatever file is open | Your open file |
| 13 | 📊 **Pipeline Graph (Step Through)** | **START HERE** - Pauses immediately | Entry point, then step line-by-line |

### Mock Issues Available

| Issue | Description | GitHub Issue |
|-------|-------------|--------------|
| 001 | API Rate Limiting | timothywarner-org/agents2#101 |
| 002 | User Authentication | timothywarner-org/agents2#102 |
| 003 | Data Export | timothywarner-org/agents2#103 |
| 004 | Dashboard Performance | timothywarner-org/agents2#104 |
| 005 | Email Notifications | timothywarner-org/agents2#105 |
| 006 | Search Functionality | timothywarner-org/agents2#106 |

## Essential Breakpoints

### See Data Flow
```python
# oreilly-agent-mvp/src/agent_mvp/pipeline/graph.py

def pm_node(state):
    response = llm.invoke([...])
    token_usage = extract_token_usage(response, ...)  # ⬅️ BREAKPOINT 1
    pm_output = PMOutput(**pm_data)                   # ⬅️ BREAKPOINT 2
    return {**state, "pm_output": pm_output}

def finalize_node(state):
    pipeline_tokens = aggregate_pipeline_tokens(...)  # ⬅️ BREAKPOINT 3
    # Inspect: total_tokens, cost_breakdown
```

### See Token Costs
```python
# oreilly-agent-mvp/src/agent_mvp/util/token_tracking.py

def calculate_cost(input_tokens, output_tokens, model_name):
    pricing = PRICING[key]                            # ⬅️ BREAKPOINT 4
    input_cost = (input_tokens / 1_000_000) * pricing["input"]
    return round(input_cost + output_cost, 6)         # ⬅️ BREAKPOINT 5
```

## Keyboard Shortcuts

| Key | Action |
|-----|--------|
| **F5** | Start debugging / Continue to next breakpoint |
| **F9** | Toggle breakpoint on current line |
| **F10** | Step Over (execute current line, don't enter functions) |
| **F11** | Step Into (enter function call) |
| **Shift+F11** | Step Out (exit current function) |
| **Shift+F5** | Stop debugging |
| **Ctrl+Shift+Y** | Open Debug Console |
| **Ctrl+Shift+D** | Open Debug sidebar |

## Debug Console Commands

While stopped at breakpoint, type in Debug Console (`Ctrl+Shift+Y`):

```python
# Inspect variables
state["pm_output"]
state.get("token_usages", [])
dir(token_usage)

# Calculate on-the-fly
len(state.get("token_usages", []))
sum(t["usage"]["total_tokens"] for t in state.get("token_usages", []))

# Pretty print
import json
print(json.dumps(state["pm_output"], indent=2))

# Check types
type(pm_output)
isinstance(pm_output, PMOutput)
```

## Watch Expressions

Add these in Debug sidebar → Watch section:

```python
state.keys()                                         # See what's in state
state.get("token_usages", [])                        # Token list
len(state.get("token_usages", []))                   # Agent count
sum(t["usage"]["total_tokens"] for t in state.get("token_usages", []))  # Total tokens
```

## Conditional Breakpoints

Right-click breakpoint → **Edit Breakpoint** → **Expression**

```python
token_usage.total_tokens > 5000          # Stop only if tokens high
state.get("error") is not None           # Stop only on errors
agent_name == "Dev"                      # Stop only for Dev agent
```

## Investigation Flows

### 🎯 Flow 1: First-Time Understanding
1. Run: **📊 Pipeline Graph (Step Through)**
2. Press **F10** repeatedly to go line-by-line
3. Watch `state` variable grow in Variables pane
4. See: issue → pm_output → dev_output → qa_output → result

### 🎯 Flow 2: Token Cost Analysis
1. Run: **🚀 Run Once (Mock Issue 001)**
2. Set breakpoints after each `llm.invoke()` call
3. Inspect `token_usage` at each stop
4. Compare costs: PM vs Dev vs QA
5. Check final `pipeline_tokens` for totals

### 🎯 Flow 3: Testing Changes
1. Modify code (e.g., prompt in `prompts.py`)
2. Run: **🚀 Run Once (Mock Issue 001)**
3. Set breakpoint in modified function
4. Inspect variables to verify changes
5. Check `outgoing/` for result

### 🎯 Flow 4: Menu Navigation
1. Run: **🎯 Interactive Menu**
2. Set breakpoints in menu handlers
3. Choose menu option
4. Step through handler execution
5. Verify expected behavior

## Common Patterns

### Pattern 1: Trace State Through Pipeline
```python
# Set breakpoints at end of each node:
pm_node:       return {**state, "pm_output": ...}     # Line ~150
dev_node:      return {**state, "dev_output": ...}    # Line ~210
qa_node:       return {**state, "qa_output": ...}     # Line ~280
finalize_node: return {**state, "result": ...}        # Line ~340

# At each stop, inspect state keys:
Debug Console: state.keys()
# See progression: issue → pm_output → dev_output → qa_output → result
# Final result keys: result["pm"], result["dev"], result["qa"]
```

### Pattern 2: Token Accumulation
```python
# Watch token_usages grow:
After PM:  state["token_usages"] = [PM_tokens]
After Dev: state["token_usages"] = [PM_tokens, Dev_tokens]
After QA:  state["token_usages"] = [PM_tokens, Dev_tokens, QA_tokens]
In finalize: pipeline_tokens = aggregate(all_tokens)
```

### Pattern 3: Cost Calculation
```python
# Step through pricing lookup:
calculate_cost() → PRICING dict lookup → cost math → return

# Verify at each step:
1. Model name matches PRICING key?
2. Input/output prices correct?
3. Division by 1M correct?
4. Final cost matches expectation?
```

## Pro Tips

1. **Start with "Pipeline Graph (Step Through)"** - Best for first-time learning
2. **Use Variables pane** - Easier than Debug Console for exploration
3. **Add Watch expressions** - Track key metrics automatically
4. **Conditional breakpoints for efficiency** - Don't stop on every iteration
5. **Logpoints for non-intrusive logging** - Log without stopping
6. **Debug Console for quick checks** - Test expressions on-the-fly
7. **Call Stack shows the path** - Understand how you got here

## Troubleshooting

**Breakpoint not hit?**
- Check `justMyCode: false` in launch.json ✅
- Ensure file is actually executed
- Try `stopOnEntry: true` to start from beginning

**Variables not showing?**
- Wait for breakpoint to trigger
- Check Variables pane is expanded
- Try Debug Console: `dir(variable_name)`

**Can't step into function?**
- Use **F11** (Step Into), not **F10** (Step Over)
- Check if function is in external library

**Debug Console shows error?**
- Check variable name spelling
- Ensure execution is paused at breakpoint
- Try simpler expression first

**Unicode/encoding errors on Windows?**
- Launch.json includes `PYTHONIOENCODING: utf-8` (already set)
- If you still see encoding errors, ensure you're using the provided launch configs
- Rich console box characters may cause issues outside the integrated terminal

**"Module not found" errors?**
- Make sure you opened `agents2/` (NOT `oreilly-agent-mvp/`) in VSCode
- The PYTHONPATH is set automatically by launch configurations

## Quick Start

**Never debugged before? Start here:**

1. Open `C:\github\agents2\` in VSCode (NOT the subfolder!)
2. Press **F5**
3. Select **"📊 Pipeline Graph (Step Through)"**
4. When it pauses, open Variables pane (left sidebar)
5. Press **F10** repeatedly
6. Watch variables change!
7. Press **F5** to finish

**That's it!** 🎉

---

**Full Guide:** [DEBUGGING.md](DEBUGGING.md)
