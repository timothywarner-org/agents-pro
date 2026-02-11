# MCP Server Quick Reference

## Installation

```bash
pip install mcp>=1.0.0
pip install -e .
```

## Quick Launch (PowerShell 7) ⚡

**Main menu (all options):**
```powershell
.\launch.ps1
```

**Direct launchers:**
```powershell
.\mcp.ps1        # MCP server
.\inspector.ps1  # MCP Inspector (web UI)
```

## Start Server

```bash
agent-mcp                          # CLI command
python -m agent_mvp.mcp_server     # Direct Python
./scripts/run_mcp.sh               # Bash script
.\scripts\run_mcp.ps1              # PowerShell script
```

## Test Server

```bash
# Option 1: Validation test
python tests/test_mcp_server.py

# Option 2: MCP Inspector (web UI - requires Node.js)
./scripts/run_mcp_inspector.sh     # Bash
.\scripts\run_mcp_inspector.ps1    # PowerShell
```

## Available Tools (5)

| Tool | Description | Example Usage |
|------|-------------|---------------|
| `fetch_github_issue` | Fetch issue from GitHub | "Fetch issue #42" |
| `list_mock_issues` | List test issues | "What mock issues exist?" |
| `load_mock_issue` | Load specific mock issue | "Load issue_001.json" |
| `run_agent_pipeline` | Run PM→Dev→QA pipeline | "Run pipeline on this issue" |
| `process_issue_file` | Process JSON file | "Process incoming/issue.json" |

## Available Resources (4)

| Resource URI | Description |
|--------------|-------------|
| `config://settings` | App configuration |
| `issues://mock/{filename}` | Mock issue content |
| `pipeline://schema` | Pydantic schemas |
| `pipeline://architecture` | Pipeline docs |

## Available Prompts (3)

| Prompt | Parameters | Usage |
|--------|------------|-------|
| `analyze_github_issue` | `issue_url`, `focus` | Structured issue analysis |
| `review_implementation_plan` | `issue_title`, `implementation_plan`, `criteria` | QA review with standards |
| `generate_test_issue` | `issue_type`, `complexity`, `domain` | Create test data |

## Claude Desktop Setup

1. **Edit config** (macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`)
2. **Add server:**
   ```json
   {
     "mcpServers": {
       "oreilly-agent-mvp": {
         "command": "python",
         "args": ["-m", "agent_mvp.mcp_server"],
         "cwd": "YOUR_PROJECT_PATH",
         "env": {
           "PYTHONPATH": "YOUR_PROJECT_PATH/src"
         }
       }
     }
   }
   ```
3. **Restart Claude**
4. **Look for 🔌 icon**

## VS Code Setup

1. **Config already in** `.vscode/mcp.json`
2. **Reload window:** Ctrl+Shift+P → "Developer: Reload Window"
3. **Test in Copilot:** "@workspace List mock issues"

## Common Commands (In Claude/Copilot)

```
List available mock issues
Fetch issue #123 from timothywarner-org/agents2
Run the agent pipeline on this issue
Load issue_001.json and process it
Show me the pipeline architecture
What's in the config?
Analyze https://github.com/org/repo/issues/5 with security focus
Review this implementation plan with strict criteria
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `ModuleNotFoundError: No module named 'mcp'` | `pip install mcp>=1.0.0` |
| `agent-mcp: command not found` | `pip install -e .` |
| No 🔌 in Claude | Check config path, restart Claude |
| VS Code doesn't see tools | Reload window, check Output panel |
| Tools fail with auth errors | Check `.env` has LLM credentials |

## File Locations

```
oreilly-agent-mvp/
├── src/agent_mvp/mcp_server/
│   ├── server.py              # Main server implementation
│   └── README.md              # Full documentation
├── .mcp/
│   └── claude_desktop_config.json  # Claude config template
├── .vscode/
│   └── mcp.json               # VS Code config (ready to use)
├── scripts/
│   ├── run_mcp.sh             # Bash launcher
│   ├── run_mcp.ps1            # PowerShell launcher
│   ├── run_mcp_inspector.sh   # Inspector launcher (Bash)
│   └── run_mcp_inspector.ps1  # Inspector launcher (PowerShell)
├── tests/
│   └── test_mcp_server.py     # Validation test
├── MCP_SETUP.md               # Step-by-step setup guide
├── MCP_INSPECTOR_GUIDE.md     # Inspector usage guide
├── MCP_IMPLEMENTATION_SUMMARY.md  # Implementation details
└── MCP_QUICK_REF.md           # This file
```

## Documentation

- **Setup Guide:** `MCP_SETUP.md`
- **Full API Docs:** `src/agent_mvp/mcp_server/README.md`
- **Inspector Guide:** `MCP_INSPECTOR_GUIDE.md`
- **Implementation Summary:** `MCP_IMPLEMENTATION_SUMMARY.md`
- **Main README:** `README.md` (MCP section)

## Support

- **GitHub Issues:** [agents2/issues](https://github.com/timothywarner-org/agents2/issues)
- **Email:** tim@techtrainertim.com
- **Website:** [TechTrainerTim.com](https://TechTrainerTim.com)

---

**Quick Start:**
1. `./scripts/run_mcp_inspector.sh`  (opens browser)
3. Test all tools interactively!
4. Configure Claude Desktop (see `MCP_SETUP.md`)e)
4. Test: "List available mock issues"

**Version:** 0.1.0 | **Date:** January 2026
