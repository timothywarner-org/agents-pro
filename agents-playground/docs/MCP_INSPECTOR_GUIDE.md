# MCP Inspector Guide

## What is MCP Inspector?

MCP Inspector is an interactive web UI for testing and debugging MCP servers. Think of it as Postman for MCP - it lets you:

- 📋 Browse available tools, resources, and prompts
- 🔧 Call tools with custom arguments
- 📊 View request/response details
- 🐛 Debug server behavior in real-time
- 📝 Test prompts and resource URIs

## Prerequisites

- **Node.js** installed (for `npx`)
- **MCP server** working (test with `python tests/test_mcp_server.py`)
- **Internet connection** (downloads inspector on first run)

## Starting MCP Inspector

### Windows (PowerShell)
```powershell
cd oreilly-agent-mvp
.\.venv\Scripts\Activate.ps1
.\scripts\run_mcp_inspector.ps1
```

### Git Bash / Linux / macOS
```bash
cd oreilly-agent-mvp
source .venv/Scripts/activate  # or source .venv/bin/activate
./scripts/run_mcp_inspector.sh
```

**What happens:**
1. Script checks for Node.js
2. Runs `npx @modelcontextprotocol/inspector python -m agent_mvp.mcp_server`
3. Downloads inspector (first run only, ~5-10 seconds)
4. Starts MCP server
5. Opens browser at `http://localhost:5173`

## Using the Inspector

### Main Interface

When the inspector opens, you'll see:

```
┌─────────────────────────────────────────────────────────┐
│  MCP Inspector                                          │
├─────────────────────────────────────────────────────────┤
│  Tabs: [Tools] [Resources] [Prompts] [Logs]            │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  Content area (varies by tab)                           │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### Tools Tab

**What you see:**
- List of all 5 tools
- Each tool shows:
  - Name
  - Description
  - Parameters (with types)
  - "Execute" button

**Example: Testing `list_mock_issues`**

1. Click **Tools** tab
2. Find **list_mock_issues** in the list
3. Click **Execute** (no parameters needed)
4. View JSON response:
   ```json
   {
      "status": "success",
      "mock_issues": [
         {
            "filename": "issue_001.json",
            "title": "CLI: add 'validate-issue' command for issue JSON files",
            "priority": "unknown",
            "path": "/path/to/issue_001.json"
         },
         {
            "filename": "issue_002.json",
            "title": "MCP: list_mock_issues should derive priority from labels (schema-safe)",
            "priority": "unknown",
            "path": "/path/to/issue_002.json"
         },
         {
            "filename": "issue_003.json",
            "title": "Watcher: avoid processing partially-written incoming JSON files (Windows-safe)",
            "priority": "unknown",
            "path": "/path/to/issue_003.json"
         },
         {
            "filename": "issue_004.json",
            "title": "Token tracking: handle missing usage data and keep totals consistent",
            "priority": "unknown",
            "path": "/path/to/issue_004.json"
         },
         {
            "filename": "issue_005.json",
            "title": "Schema: allow optional issue metadata while keeping strict validation",
            "priority": "unknown",
            "path": "/path/to/issue_005.json"
         },
         {
            "filename": "issue_006.json",
            "title": "Pipeline UX: add --dry-run and clarify output directory behavior",
            "priority": "unknown",
            "path": "/path/to/issue_006.json"
         }
      ],
      "count": 6
   }
   ```

**Example: Testing `fetch_github_issue`**

1. Click **Tools** tab
2. Find **fetch_github_issue**
3. Fill in parameters:
   - `issue_number`: 42
   - `owner`: timothywarner-org
   - `repo`: agents2
   - `save_to_incoming`: true
4. Click **Execute**
5. View response with fetched issue data

### Resources Tab

**What you see:**
- List of resource URIs
- Template URIs with parameter placeholders
- "Fetch" button for each resource

**Example: Reading `config://settings`**

1. Click **Resources** tab
2. Find **config://settings**
3. Click **Fetch**
4. View JSON config:
   ```json
   {
     "llm_provider": "anthropic",
     "llm_model": "claude-sonnet-4-20250514",
     "project_root": "/path/to/project",
     ...
   }
   ```

**Example: Reading dynamic resource `issues://mock/{filename}`**

1. Click **Resources** tab
2. Find **issues://mock/{filename}**
3. Replace `{filename}` with `issue_001.json`
4. URI becomes: `issues://mock/issue_001.json`
5. Click **Fetch**
6. View issue JSON content

### Prompts Tab

**What you see:**
- List of available prompts
- Parameters for each prompt
- "Generate" button

**Example: Using `analyze_github_issue` prompt**

1. Click **Prompts** tab
2. Find **analyze_github_issue**
3. Fill in parameters:
   - `issue_url`: https://github.com/timothywarner-org/agents2/issues/42
   - `focus`: security
4. Click **Generate**
5. View generated prompt text

**Example: Using `generate_test_issue` prompt**

1. Click **Prompts** tab
2. Find **generate_test_issue**
3. Fill in parameters:
   - `issue_type`: bug
   - `complexity`: medium
   - `domain`: web
4. Click **Generate**
5. Copy generated prompt
6. Use with LLM to create test data

### Logs Tab

**What you see:**
- Real-time server logs
- Requests and responses
- Error messages
- Progress updates

**Useful for:**
- Debugging tool failures
- Understanding request flow
- Monitoring progress updates
- Catching validation errors

## Common Workflows

### Workflow 1: Test All Tools

```
1. Start inspector
2. Go to Tools tab
3. Test each tool:
   - list_mock_issues ✓
   - load_mock_issue (use "issue_001.json") ✓
   - fetch_github_issue (pick an issue number) ✓
   - run_agent_pipeline (use issue from above) ✓
   - process_issue_file (use path from load_mock) ✓
4. Check Logs tab for any errors
```

### Workflow 2: Develop New Tool

```
1. Add tool function to server.py:
   @mcp.tool()
   def my_new_tool(param: str) -> dict:
       return {"status": "success", "data": param}

2. Save file
3. Restart inspector (Ctrl+C, then re-run script)
4. Tools tab auto-refreshes
5. Find "my_new_tool" in list
6. Test with different parameters
7. Check Logs for debugging
8. Iterate until working
```

### Workflow 3: Debug Failing Tool

```
1. Call tool through inspector
2. Tool fails with error
3. Check Logs tab for:
   - Python stack trace
   - Error message details
   - Request parameters sent
4. Fix code in server.py
5. Restart inspector
6. Re-test tool
7. Verify fix in Logs
```

### Workflow 4: Test Resource URIs

```
1. Go to Resources tab
2. Test static resources:
   - config://settings ✓
   - pipeline://schema ✓
   - pipeline://architecture ✓
3. Test dynamic resources:
   - issues://mock/issue_001.json ✓
   - issues://mock/issue_002.json ✓
   - issues://mock/issue_003.json ✓
4. Verify all URIs resolve correctly
```

### Workflow 5: Validate Prompts

```
1. Go to Prompts tab
2. Test each prompt with different parameters:

   analyze_github_issue:
   - focus=general ✓
   - focus=security ✓
   - focus=performance ✓

   review_implementation_plan:
   - criteria=standard ✓
   - criteria=strict ✓
   - criteria=lenient ✓

   generate_test_issue:
   - Try all combinations of type/complexity/domain ✓

3. Verify prompt quality and formatting
```

## Tips & Tricks

### Tip 1: Keep Inspector Running While Coding

Leave the inspector open in your browser while editing `server.py`. When you make changes:
1. Save the file
2. Stop server (Ctrl+C in terminal)
3. Restart: `./scripts/run_mcp_inspector.sh`
4. Browser auto-refreshes with new tools/resources

### Tip 2: Use Logs Tab for Debugging

The Logs tab is invaluable for:
- Seeing actual request payloads
- Understanding error messages
- Monitoring progress updates
- Debugging async operations

### Tip 3: Test Edge Cases

Use the inspector to test:
- Invalid parameters
- Missing required fields
- Empty strings
- Very large inputs
- Concurrent requests

### Tip 4: Compare with Claude Desktop

Use inspector alongside Claude Desktop:
1. Test tool in inspector → Works correctly
2. Test same tool in Claude → Behaves differently
3. Compare request parameters in Logs tab
4. Debug the discrepancy

### Tip 5: Export Test Cases

When you find good test cases in the inspector:
1. Note the parameters that worked
2. Add to `tests/test_mcp_server.py`
3. Automate testing for regression prevention

## Troubleshooting

### Issue: Inspector won't start

**Error:** `node: command not found`

**Solution:**
```bash
# Install Node.js from https://nodejs.org/
# Then retry
```

### Issue: Port already in use

**Error:** `EADDRINUSE: address already in use :::5173`

**Solution:**
```bash
# Find and kill process using port 5173
# Windows:
netstat -ano | findstr :5173
taskkill /PID <PID> /F

# Mac/Linux:
lsof -i :5173
kill -9 <PID>
```

### Issue: Browser doesn't open automatically

**Solution:**
Manually open: `http://localhost:5173`

### Issue: Tools don't appear in inspector

**Possible causes:**
1. Server failed to start (check terminal for errors)
2. Python import errors (check `.env` file exists)
3. MCP SDK not installed (`pip install mcp>=1.0.0`)

**Solution:**
Check terminal output for error messages. Common fixes:
- Verify virtual environment is active
- Ensure `.env` file has LLM credentials
- Run `python tests/test_mcp_server.py` first

### Issue: Tool execution fails

**Symptoms:** Click Execute → Error in Logs tab

**Debug steps:**
1. Check Logs tab for Python traceback
2. Verify parameters are correct types
3. Check `.env` has required credentials
4. Test tool directly: `python tests/test_mcp_server.py`
5. Fix error in `server.py`
6. Restart inspector

## Keyboard Shortcuts

- **Ctrl+C** - Stop inspector and server
- **Ctrl+Shift+R** - Hard refresh browser (clear cache)
- **F12** - Open browser DevTools for advanced debugging

## Best Practices

### 1. Test Before Integrating

Always test tools in the inspector before trying them in Claude Desktop or VS Code. This isolates issues and speeds up debugging.

### 2. Use Inspector for Documentation

The inspector auto-generates documentation from your docstrings and type hints. Keep them up-to-date!

### 3. Test All Parameter Combinations

For tools with optional parameters, test all combinations:
- All parameters provided
- Only required parameters
- Default values
- Edge cases

### 4. Monitor Logs During Development

Keep the Logs tab open while developing. It shows:
- When tools are called
- What parameters were sent
- Response times
- Error details

### 5. Save Test Scenarios

When you find good test cases, document them in your README or add to automated tests.

## Advanced Usage

### Custom Port

If port 5173 conflicts, specify a custom port:

```bash
# Edit script to use custom port
npx @modelcontextprotocol/inspector --port 8080 python -m agent_mvp.mcp_server
```

### Remote Inspector

To access inspector from another machine:

```bash
npx @modelcontextprotocol/inspector --host 0.0.0.0 python -m agent_mvp.mcp_server
# Access from: http://<your-ip>:5173
```

### Debug Mode

For more verbose logging:

```bash
# Set debug environment variable
DEBUG=* npx @modelcontextprotocol/inspector python -m agent_mvp.mcp_server
```

## Summary

**MCP Inspector is essential for:**
- ✅ Testing tools interactively
- ✅ Debugging server issues
- ✅ Validating resources and prompts
- ✅ Developing new features
- ✅ Learning MCP protocol behavior

**Quick start:**
```bash
./scripts/run_mcp_inspector.sh
# Opens browser at http://localhost:5173
# Test all tools, resources, and prompts!
```

## Related Documentation

- **MCP Server README:** `src/agent_mvp/mcp_server/README.md`
- **Setup Guide:** `MCP_SETUP.md`
- **Quick Reference:** `MCP_QUICK_REF.md`
- **Official Docs:** https://modelcontextprotocol.io/docs/tools/inspector

## Support

**Issues?** Open a GitHub issue: [agents2/issues](https://github.com/timothywarner-org/agents2/issues)

**Questions?** Email: tim@techtrainertim.com

---

**Happy testing with MCP Inspector!** 🔍✨
