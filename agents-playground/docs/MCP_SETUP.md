# MCP Server Setup Guide

## Prerequisites

1. **Python 3.11+** with pip
2. **Virtual environment** active (`.venv`)
3. **LLM Provider credentials** in `.env` file

## Installation Steps

### 1. Install MCP Python SDK

```bash
cd oreilly-agent-mvp
source .venv/Scripts/activate  # Git Bash
# OR
.\.venv\Scripts\Activate.ps1   # PowerShell

pip install mcp>=1.0.0
```

### 2. Reinstall Package (Pick Up New CLI Command)

```bash
pip install -e .
```

### 3. Verify Installation

```bash
# Check that agent-mcp command is available
agent-mcp --help

# Or run directly
python -m agent_mvp.mcp_server --help
```

### 4. Test the Server

**Option A: Run validation test**

```bash
python tests/test_mcp_server.py
```

**Option B: Use MCP Inspector (Recommended)**

The MCP Inspector provides a web UI for testing tools, resources, and prompts interactively:

```bash
# Requires Node.js installed
./scripts/run_mcp_inspector.sh  # Git Bash / Linux / macOS
# OR
.\scripts\run_mcp_inspector.ps1  # PowerShell
```

This will:
1. Start the MCP server
2. Launch MCP Inspector in your browser
3. Provide an interactive UI to test all tools, resources, and prompts
4. Show request/response details for debugging

Expected output:
```
╔==========================================================╗
║          MCP SERVER VALIDATION TEST                      ║
╚==========================================================╝

============================================================
SERVER METADATA TEST
============================================================
Server Name: oreilly-agent-mvp
Instructions: This server provides tools for running...
✅ Metadata configured

============================================================
TOOLS TEST
============================================================
✓ fetch_github_issue
  Fetch an issue from GitHub and optionally save to incoming directory.
✓ list_mock_issues
  List available mock issue files.
✓ load_mock_issue
  Load a specific mock issue by filename.
✓ run_agent_pipeline
  Run the full PM → Dev → QA agent pipeline on an issue.
✓ process_issue_file
  Process an issue from a JSON file through the pipeline.

Total: 5 tools registered
✅ All tools present

============================================================
RESOURCES TEST
============================================================
✓ config://settings
  Expose current application configuration.
✓ issues://mock/{filename}
  Get content of a specific mock issue file.
✓ pipeline://schema
  Get the data schema for pipeline input/output.
✓ pipeline://architecture
  Get architecture documentation for the agent pipeline.

Total: 4 resources registered
✅ All resources present

============================================================
PROMPTS TEST
============================================================
✓ analyze_github_issue
  Generate a prompt for analyzing a GitHub issue.
✓ review_implementation_plan
  Generate a prompt for reviewing an implementation plan.
✓ generate_test_issue
  Generate a prompt for creating a test issue.

Total: 3 prompts registered
✅ All prompts present

============================================================
SUMMARY
============================================================
✅ PASS - Server Metadata
✅ PASS - Tools
✅ PASS - Resources
✅ PASS - Prompts

🎉 All tests passed! MCP server is ready to use.
```

## Integration with Claude Desktop

### Step 1: Locate Claude Config

**macOS:**
```bash
~/Library/Application Support/Claude/claude_desktop_config.json
```

**Windows:**
```cmd
%APPDATA%\Claude\claude_desktop_config.json
```

### Step 2: Add Server Configuration

Open the config file and add (or merge with existing):

```json
{
  "mcpServers": {
    "oreilly-agent-mvp": {
      "command": "python",
      "args": ["-m", "agent_mvp.mcp_server"],
      "cwd": "c:/github/agents2/oreilly-agent-mvp",
      "env": {
        "PYTHONPATH": "c:/github/agents2/oreilly-agent-mvp/src"
      }
    }
  }
}
```

**Important:** Update the `cwd` path to match your actual project location!

### Step 3: Restart Claude Desktop

Close Claude completely and reopen.

### Step 4: Verify Connection

Look for the 🔌 (plug) icon in Claude's interface. If present, the server is connected.

Test with:
```
List available mock issues
```

Expected: Claude will use the `list_mock_issues` tool and show results.

## Integration with VS Code Copilot

### Step 1: Verify Config

Config is already in `.vscode/mcp.json`. Check that paths are correct:

```json
{
  "servers": {
    "oreilly-agent-mvp": {
      "type": "stdio",
      "command": "python",
      "args": ["-m", "agent_mvp.mcp_server"],
      "env": {
        "PYTHONPATH": "${workspaceFolder}/src"
      },
      "description": "O'Reilly Agent MVP - PM/Dev/QA pipeline for issue triage"
    }
  }
}
```

### Step 2: Reload VS Code

Press `Ctrl+Shift+P` (or `Cmd+Shift+P` on Mac) and run:
```
Developer: Reload Window
```

### Step 3: Test in Copilot Chat

Open Copilot Chat and ask:
```
@workspace What MCP tools are available?
```

Or:
```
@workspace Fetch issue #1 from the repo
```

## Troubleshooting

### Issue: `ModuleNotFoundError: No module named 'mcp'`

**Solution:**
```bash
pip install mcp>=1.0.0
```

### Issue: `agent-mcp: command not found`

**Solution:**
```bash
pip install -e .  # Reinstall package to register CLI commands
```

### Issue: Claude Desktop doesn't show 🔌 icon

**Checklist:**
1. ✅ Claude Desktop fully restarted (quit from system tray)
2. ✅ Config file has valid JSON (no trailing commas)
3. ✅ `cwd` path exists and is correct
4. ✅ Python can be found in PATH
5. ✅ Virtual environment includes `mcp` package

**Debug:**
Check Claude's logs:
- **macOS:** `~/Library/Logs/Claude/mcp*.log`
- **Windows:** `%APPDATA%\Claude\logs\mcp*.log`

### Issue: VS Code Copilot doesn't recognize tools

**Solution:**
1. Ensure workspace is open (not just loose files)
2. Check VS Code Output panel → "Language Model"
3. Verify `.vscode/mcp.json` exists in workspace root
4. Reload window again

### Issue: Server starts but tools fail

**Possible causes:**
- `.env` file missing or incomplete
- LLM provider credentials invalid
- Project structure changed

**Solution:**
1. Check `.env` has required keys (ANTHROPIC_API_KEY or OPENAI_API_KEY)
2. Run `python tests/test_mcp_server.py` to validate structure
3. Check logs for specific error messages

## Usage Examples

### Example 1: Fetch and Analyze GitHub Issue

**In Claude Desktop:**
```
Fetch issue #42 from timothywarner-org/agents2
```

Claude will use `fetch_github_issue` tool.

Then:
```
Run the agent pipeline on this issue
```

Claude will use `run_agent_pipeline` tool.

### Example 2: Work with Mock Issues

**In Claude Desktop:**
```
Show me the available test issues
```

Claude uses `list_mock_issues`.

```
Load issue_001.json and run the pipeline
```

Claude uses `load_mock_issue` and `run_agent_pipeline`.

### Example 3: Use Prompt Templates

**In Claude Desktop:**
```
Use the analyze_github_issue prompt for https://github.com/example/repo/issues/5
with a security focus
```

Claude will generate the prompt and analyze the issue.

## Advanced: Custom Transport

The server uses stdio (standard input/output) by default for local integration. For remote servers, you can use SSE (Server-Sent Events):

```python
# In server.py, change:
mcp.run(transport="stdio")

# To:
mcp.run(transport="streamable-http", port=8000)
```

Then update client config to connect via HTTP instead of stdio.

## Next Steps

- ✅ Server is running
- ✅ Integrated with Claude or VS Code
- 📖 Read [Full MCP Documentation](src/agent_mvp/mcp_server/README.md)
- 🎓 Try the example workflows above
- 🚀 Build your own tools and prompts

## Support

**Issues?** Open a GitHub issue: [agents2/issues](https://github.com/timothywarner-org/agents2/issues)

**Questions?** Email: tim@techtrainertim.com

**Documentation:** [TechTrainerTim.com](https://TechTrainerTim.com)
