# Simple Debugging Guide - O'Reilly Agent MVP

**No Function Keys? No Problem!** Use Command Palette (`Ctrl+Shift+P`) for everything.

> **Important:** Open `C:\github\agents2\` in VSCode (NOT the `oreilly-agent-mvp/` subfolder). All paths automatically resolve to the subfolder.

---

## 🚀 Quick Start (3 Steps)

### Step 1: Open Debug Panel
- **Keyboard:** `Ctrl+Shift+D`
- **Command Palette:** `Ctrl+Shift+P` → type `Debug: Focus on Debug View`
- **Mouse:** Click bug icon in left sidebar

### Step 2: Choose What to Debug
Click dropdown at top of Debug panel, select:
- **"📊 Pipeline Graph (Step Through)"** ← START HERE (pauses immediately)
- **"🚀 Run Once (Mock Issue 001-006)"** ← Run full pipeline with different mock issues
- **"🎯 Interactive Menu"** ← Test menu system

### Step 3: Start Debugging
- **Keyboard:** `F5`
- **Command Palette:** `Ctrl+Shift+P` → type `Debug: Start Debugging`
- **Mouse:** Click green play button in Debug panel

**That's it!** When it pauses, press F10 (or use Command Palette) to step through line-by-line.

---

## 🎮 Debug Controls (All Commands)

### Start & Stop

| Action | Function Key | Command Palette | Mouse |
|--------|--------------|-----------------|-------|
| **Start/Continue** | `F5` | `Debug: Continue` | Green play ▶️ |
| **Stop** | `Shift+F5` | `Debug: Stop` | Red square ⏹️ |
| **Restart** | `Ctrl+Shift+F5` | `Debug: Restart` | Green circle ⟳ |

### Stepping Through Code

| Action | Function Key | Command Palette | What It Does |
|--------|--------------|-----------------|--------------|
| **Step Over** | `F10` | `Debug: Step Over` | Execute current line, stay in this file |
| **Step Into** | `F11` | `Debug: Step Into` | Enter the function being called |
| **Step Out** | `Shift+F11` | `Debug: Step Out` | Finish current function, go back |

**Most Common:** Use **Step Over** (F10) to go line-by-line without diving into every function.

### Breakpoints

| Action | Function Key | Command Palette | Mouse |
|--------|--------------|-----------------|-------|
| **Toggle Breakpoint** | `F9` | `Debug: Toggle Breakpoint` | Click in gutter (left of line numbers) |
| **Remove All** | - | `Debug: Remove All Breakpoints` | - |
| **Disable All** | - | `Debug: Disable All Breakpoints` | - |

---

## 🎯 Recommended Debugging Flows

### Flow 1: "I want to understand how it works"

1. **Open file:** `oreilly-agent-mvp/src/agent_mvp/pipeline/graph.py`
2. **Set breakpoint:** Click gutter next to line 100 (in `pm_node`)
3. **Start:** Command Palette → `Debug: Start Debugging` → Select **"🚀 Run Once (Mock Issue 001)"**
4. **When it stops:**
   - Look at **Variables** pane (left) - see what's in `state`
   - Press F10 (or Command Palette → `Debug: Step Over`) to go line-by-line
   - Watch how `state` changes

### Flow 2: "I want to see token costs build up"

**Set 4 breakpoints in `oreilly-agent-mvp/src/agent_mvp/pipeline/graph.py`:**
- Line ~120: After PM calls LLM
- Line ~190: After Dev calls LLM
- Line ~260: After QA calls LLM
- Line ~320: In finalize (aggregation)

**Run:** Command Palette → `Debug: Start Debugging` → **"🚀 Run Once (Mock Issue 001)"**

**At each stop:** Look at Variables pane → expand `token_usage` → see input/output tokens and cost

**Press F5** (or Command Palette → `Debug: Continue`) to jump to next breakpoint

### Flow 3: "I want to step through everything slowly"

1. **Start:** Command Palette → `Debug: Start Debugging` → **"📊 Pipeline Graph (Step Through)"**
2. **It pauses immediately** at the first line
3. **Open Variables pane** (left sidebar under Debug)
4. **Press F10 repeatedly** (or use Command Palette → `Debug: Step Over`)
5. **Watch `state` variable grow:**
   - First: `issue` appears
   - Then: `pm_output` appears
   - Then: `dev_output` appears
   - Then: `qa_output` appears
   - Finally: `result` appears
   - Inspect `result["pm"]`, `result["dev"]`, and `result["qa"]` to see final outputs and verdict (`pass`, `fail`, or `needs-human`)

---

## 📍 Where to Set Breakpoints

### See Agent Execution
```
oreilly-agent-mvp/src/agent_mvp/pipeline/graph.py

Line ~100  - pm_node starts
Line ~120  - PM got LLM response (see tokens here)
Line ~150  - PM finished (see plan & criteria)

Line ~170  - dev_node starts
Line ~190  - Dev got LLM response (see tokens here)
Line ~210  - Dev finished (see files created)

Line ~240  - qa_node starts
Line ~260  - QA got LLM response (see tokens here)
Line ~280  - QA finished (see verdict)

Line ~300  - finalize_node starts
Line ~320  - Tokens aggregated (see total cost)
```

### See Token Calculation
```
oreilly-agent-mvp/src/agent_mvp/util/token_tracking.py

Line ~40   - Token extraction from LLM response
Line ~90   - Cost calculation (see pricing lookup)
Line ~130  - Total aggregation across all agents
```

---

## 🔍 Inspecting Variables

When stopped at a breakpoint, you have 3 ways to see data:

### 1. Variables Pane (Easiest)
- **Location:** Left sidebar under Debug
- **Show:** Automatically shows all variables in scope
- **Tip:** Click ▶️ arrows to expand nested objects

**Example:** Expand `state` → see `issue`, `pm_output`, `token_usages`

### 2. Debug Console (Most Powerful)
- **Show:** Command Palette → `View: Debug Console` (or `Ctrl+Shift+Y`)
- **Type Python:** Enter any Python expression

**Try these:**
```python
state.keys()                           # What's in state?
state["pm_output"]                     # See PM output
len(state.get("token_usages", []))     # How many agents done?
token_usage.total_tokens               # Total tokens for this agent
result["qa"]["verdict"]                # Final pass/fail/needs-human verdict
```

### 3. Watch Expressions (Auto-Update)
- **Location:** Debug sidebar → Watch section
- **Add:** Click + button
- **Enter:** `state.get("token_usages", [])`

**Useful watches:**
```python
state.keys()
len(state.get("token_usages", []))
sum(t["usage"]["total_tokens"] for t in state.get("token_usages", []))
```

---

## 🎨 Available Configurations (13 Total)

Press `Ctrl+Shift+D` → dropdown at top → choose:

| # | Config | When to Use |
|---|--------|-------------|
| 1 | 🎯 **Interactive Menu** | Test the CLI menu system |
| 2 | 🚀 **Run Once (Mock Issue 001)** | API Rate Limiting feature (timothywarner-org/agents2#101) |
| 3 | 🚀 **Run Once (Mock Issue 002)** | User Authentication enhancement (timothywarner-org/agents2#102) |
| 4 | 🚀 **Run Once (Mock Issue 003)** | Data Export functionality (timothywarner-org/agents2#103) |
| 5 | 🚀 **Run Once (Mock Issue 004)** | Dashboard Performance (timothywarner-org/agents2#104) |
| 6 | 🚀 **Run Once (Mock Issue 005)** | Email Notification system (timothywarner-org/agents2#105) |
| 7 | 🚀 **Run Once (Mock Issue 006)** | Search Functionality (timothywarner-org/agents2#106) |
| 8 | 👁️ **Folder Watcher** | Test auto-processing of dropped files |
| 9 | 🔧 **MCP Server** | Debug MCP tools/resources |
| 10 | 🧪 **Run Tests (All)** | Debug all tests |
| 11 | 🧪 **Run Tests (Token Tracking)** | Debug token tracking tests |
| 12 | 🔍 **Debug Current File** | Run whatever file is open |
| 13 | 📊 **Pipeline Graph (Step Through)** | ⭐ START HERE - Pauses at beginning |

---

## 💡 Common Scenarios

### "My breakpoint isn't being hit"

**Solution:**
1. Make sure you started debugging (green play button or F5)
2. Check the file is actually executed (try earlier breakpoint)
3. Try Command Palette → `Debug: Restart`

### "I see too many variables"

**Solution:**
- Collapse sections you don't need in Variables pane
- Use Watch expressions for specific values
- Use Debug Console to check just what you need

### "I stepped into a function I don't care about"

**Solution:**
- Command Palette → `Debug: Step Out` (or `Shift+F11`)
- Gets you back to your code

### "I want to run to a specific line"

**Solution:**
1. Right-click the line → **"Run to Cursor"**
2. Or set a breakpoint there and press F5 (Continue)

### "How do I see what just changed?"

**Solution:**
- Use **Step Over** (F10) one line at a time
- After each step, check Variables pane
- See what changed highlighted in yellow

---

## 🎓 Learning Path

**Day 1: Just Watch**
1. Start with **"📊 Pipeline Graph (Step Through)"**
2. Press F10 (Step Over) repeatedly
3. Just watch Variables pane
4. Goal: See the flow

**Day 2: Set Breakpoints**
1. Open `oreilly-agent-mvp/src/agent_mvp/pipeline/graph.py`
2. Set breakpoint at line 120 (after PM LLM call)
3. Run **"🚀 Run Once (Mock Issue 001)"**
4. When it stops, look at `token_usage`
5. Goal: See what data looks like

**Day 3: Inspect Data**
1. Same as Day 2, but now...
2. Open Debug Console (`Ctrl+Shift+Y`)
3. Type: `token_usage.input_tokens`
4. Try: `state["pm_output"]["plan"]`
5. Goal: Query data yourself

**Day 4: Track Changes**
1. Watch token costs accumulate
2. Set breakpoints after each agent (PM, Dev, QA)
3. Use Watch expression: `len(state.get("token_usages", []))`
4. See it grow: 0 → 1 → 2 → 3
5. Goal: Understand data flow

---

## 🆘 Quick Help

**Open Command Palette:** `Ctrl+Shift+P` (works everywhere)

**Essential Commands:**
- Type `debug start` → Start debugging
- Type `debug stop` → Stop debugging
- Type `debug step` → See step options
- Type `debug toggle` → Toggle breakpoint
- Type `debug console` → Open debug console
- Type `debug restart` → Restart debugging

**Remember:** Command Palette autocompletes! Just type a few letters.

---

## ✅ Checklist for First Debug Session

- [ ] Open `C:\github\agents2\` folder in VSCode (NOT the subfolder!)
- [ ] Press `Ctrl+Shift+D` (or click bug icon)
- [ ] Select **"📊 Pipeline Graph (Step Through)"** from dropdown
- [ ] Press `F5` (or Command Palette → `Debug: Start Debugging`)
- [ ] When it pauses, look at left sidebar (Variables section)
- [ ] Press `F10` a few times (or Command Palette → `Debug: Step Over`)
- [ ] Watch variables change
- [ ] Press `F5` to finish (or Command Palette → `Debug: Continue`)

**You did it!** 🎉

---

## 🔧 Troubleshooting

**"Module not found" errors?**
- Make sure you opened `agents2/` (NOT `oreilly-agent-mvp/`) in VSCode
- The PYTHONPATH is set automatically by launch configurations

**Unicode/encoding errors on Windows?**
- The launch.json includes `PYTHONIOENCODING: utf-8` (already configured)
- If you still see encoding errors, ensure you're using the provided launch configs
- Rich console box characters may cause issues outside the integrated terminal

**Breakpoint not being hit?**
- Ensure debugging is actually started (green play button or F5)
- Try setting breakpoint earlier in the file
- Use Command Palette → `Debug: Restart`

---

## 📚 More Resources

- **Full Guide:** [DEBUGGING.md](DEBUGGING.md) - Comprehensive debugging documentation
- **Quick Reference:** [DEBUGGING_QUICKREF.md](DEBUGGING_QUICKREF.md) - One-page cheat sheet
- **VSCode Docs:** [Python Debugging Guide](https://code.visualstudio.com/docs/python/debugging)

---

**Tip:** Bookmark this page and keep it open while debugging! 📌
