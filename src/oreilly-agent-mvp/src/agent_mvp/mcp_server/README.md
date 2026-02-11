# MCP Server for O'Reilly Agent MVP

This directory contains the Model Context Protocol (MCP) server implementation for the O'Reilly Agent MVP. The server exposes the agent pipeline as MCP tools, resources, and prompts that can be used by Claude Desktop, VS Code Copilot, and other MCP-compatible clients.

## Overview

The MCP server provides a standardized interface for:
- **Tools**: Actions that LLMs can call (fetch issues, run pipeline, etc.)
- **Resources**: Data that LLMs can read (config, schemas, architecture docs)
- **Prompts**: Reusable templates for common workflows

## Architecture

```
┌─────────────────────────────────────────────┐
│   MCP Client (Claude Desktop, VS Code)      │
└────────────────┬────────────────────────────┘
                 │ stdio transport
                 │
┌────────────────▼────────────────────────────┐
│   FastMCP Server (agent_mvp.mcp_server)     │
│                                              │
│   ┌──────────┐  ┌───────────┐  ┌─────────┐ │
│   │  Tools   │  │ Resources │  │ Prompts │ │
│   └────┬─────┘  └─────┬─────┘  └────┬────┘ │
│        │              │              │      │
└────────┼──────────────┼──────────────┼──────┘
         │              │              │
         ▼              ▼              ▼
┌────────────────────────────────────────────┐
│   Agent MVP Core (pipeline, integrations)  │
│   PM → Dev → QA agents (LangGraph/CrewAI)  │
└────────────────────────────────────────────┘
```

## Tools

### `fetch_github_issue`
Fetch an issue from GitHub and optionally save to `incoming/`.

**Parameters:**
- `issue_number` (int): GitHub issue number
- `owner` (str): Repository owner (default: timothywarner-org)
- `repo` (str): Repository name (default: agents2)
- `save_to_incoming` (bool): Save JSON to incoming/ directory

**Returns:**
```json
{
  "status": "success",
  "issue": {...},
  "saved_to": "incoming/github_issue_123.json"
}
```

### `list_mock_issues`
List available mock issue files in `mock_issues/`.

**Returns:**
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

### `load_mock_issue`
Load a specific mock issue by filename.

**Parameters:**
- `filename` (str): Name of the mock issue file (e.g., "issue_001.json")

**Returns:**
```json
{
  "status": "success",
  "issue": {...},
  "path": "/path/to/mock_issues/issue_001.json"
}
```

### `run_agent_pipeline`
Run the full PM → Dev → QA agent pipeline on an issue.

**Parameters:**
- `issue_data` (dict): Issue data in standardized format

**Returns:**
```json
{
  "status": "success",
  "run_id": "20250110_143022",
   "pm": {...},
   "dev": {...},
   "qa": {...},
   "output_file": "outgoing/result_20250110_143022.json",
   "token_usage": {...},
   "report": "..."
}
```

### `process_issue_file`
Process an issue from a JSON file through the pipeline.

**Parameters:**
- `file_path` (str): Path to JSON file containing issue data

**Returns:**
```json
{
  "status": "success",
  "run_id": "20250110_143022",
   "verdict": "pass",
   "output_file": "outgoing/result_20250110_143022.json",
   "token_usage": {...},
   "report": "..."
}
```

## Resources

### `config://settings`
Current application configuration (LLM provider, model, directories).

**URI:** `config://settings`

**Returns:** JSON with config settings

### `issues://mock/{filename}`
Content of a specific mock issue file.

**URI Template:** `issues://mock/{filename}`

**Example:** `issues://mock/issue_001.json`

### `pipeline://schema`
Pydantic schemas for pipeline input/output.

**URI:** `pipeline://schema`

**Returns:** JSON with Issue, PMOutput, DevOutput, QAOutput schemas

### `pipeline://architecture`
Architecture documentation for the agent pipeline.

**URI:** `pipeline://architecture`

**Returns:** Markdown documentation

## Prompts

### `analyze_github_issue`
Generate a prompt for analyzing a GitHub issue.

**Parameters:**
- `issue_url` (str): URL of the GitHub issue
- `focus` (str): Analysis focus (general, security, performance, architecture)

### `review_implementation_plan`
Generate a prompt for reviewing an implementation plan.

**Parameters:**
- `issue_title` (str): Title of the issue
- `implementation_plan` (str): The dev team's plan
- `criteria` (str): Review criteria (standard, strict, lenient)

### `generate_test_issue`
Generate a prompt for creating a test issue.

**Parameters:**
- `issue_type` (str): Type of issue (bug, feature, enhancement, refactor)
- `complexity` (str): Complexity level (simple, medium, complex)
- `domain` (str): Technical domain (web, api, database, infrastructure)

## Setup

### Installation

1. **Install the MCP Python SDK:**
   ```bash
   pip install mcp>=1.0.0
   ```

2. **Install agent-mvp in editable mode:**
   ```bash
   cd oreilly-agent-mvp
   pip install -e .
   ```

3. **Configure environment:**
   ```bash
   cp .env.example .env
   # Edit .env and add your LLM provider credentials
   ```

### Running Standalone

Run the MCP server directly:

```bash
# Using the CLI command
agent-mcp

# Or using Python module
python -m agent_mvp.mcp_server

# Or using the shell script
./scripts/run_mcp.sh  # Git Bash/Linux/Mac
.\scripts\run_mcp.ps1  # PowerShell
```

The server will listen on stdio for MCP client connections.

### Testing with MCP Inspector

MCP Inspector provides a web UI for testing tools, resources, and prompts interactively.

**Prerequisites:**
- Node.js installed (for `npx`)

**Run the inspector:**

```bash
./scripts/run_mcp_inspector.sh  # Git Bash/Linux/Mac
# OR
.\scripts\run_mcp_inspector.ps1  # PowerShell
```

**What it does:**
1. Launches the MCP server
2. Opens MCP Inspector in your browser (usually http://localhost:5173)
3. Provides interactive UI to:
   - Browse available tools, resources, and prompts
   - Call tools with custom arguments
   - View request/response details
   - Test error handling
   - Debug server behavior

**Example workflow:**
1. Start inspector → Browser opens with UI
2. Select "Tools" tab → See all 5 tools listed
3. Click "fetch_github_issue" → Fill in parameters
4. Click "Execute" → See JSON response
5. Check "Logs" tab → View server-side logging

**Tip:** Leave the inspector running while developing new tools. It auto-refreshes when you restart the server.

## Integration

### Claude Desktop

1. **Locate Claude Desktop config:**
   - **macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`
   - **Windows:** `%APPDATA%\Claude\claude_desktop_config.json`

2. **Add server configuration:**
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

3. **Restart Claude Desktop**

4. **Verify connection:**
   - Look for 🔌 icon in Claude chat
   - Ask: "List available MCP tools"

### VS Code Copilot

The server is already configured in `.vscode/mcp.json`.

1. **Ensure virtual environment is active:**
   ```bash
   source .venv/Scripts/activate  # Git Bash
   .\.venv\Scripts\Activate.ps1   # PowerShell
   ```

2. **Reload VS Code window:**
   - Press `Ctrl+Shift+P`
   - Run "Developer: Reload Window"

3. **Use in Copilot Chat:**
   - Ask: "Fetch issue #123 from GitHub"
   - Ask: "List available mock issues"
   - Ask: "Run the agent pipeline on issue_001.json"

## Usage Examples

### Example 1: Fetch and Process GitHub Issue

```
You: Fetch issue #42 from timothywarner-org/agents2

Claude: I'll fetch that issue for you.
[Uses fetch_github_issue tool]

You: Now run the agent pipeline on it

Claude: Running the PM → Dev → QA pipeline...
[Uses run_agent_pipeline tool]
```

### Example 2: List and Process Mock Issue

```
You: What mock issues are available?

Claude: [Uses list_mock_issues tool]
Here are the available mock issues:
1. issue_001.json - #101 CLI: validate issue JSON files
2. issue_002.json - #102 MCP: mock issue listing priority from labels
3. issue_003.json - #103 Watcher: avoid partially-written files
4. issue_004.json - #104 Token tracking: handle missing usage
5. issue_005.json - #105 Schema: allow optional issue metadata
6. issue_006.json - #106 Pipeline: dry-run + output-dir consistency

You: Process issue_001.json

Claude: [Uses process_issue_file tool]
Processing complete! Results saved to outgoing/result_20250110_143022.json
```

### Example 3: Use Prompt Templates

```
You: Analyze https://github.com/timothywarner-org/agents2/issues/42
     with a security focus

Claude: [Uses analyze_github_issue prompt]
[Provides detailed security analysis]

You: Review this implementation plan with strict criteria:
     [paste plan]

Claude: [Uses review_implementation_plan prompt]
[Provides thorough QA review]
```

## Development

### Testing Tools

Test individual tools using the Python client:

```python
import asyncio
from mcp.client.session import ClientSession
from mcp.client.stdio import StdioServerParameters, stdio_client

async def test_tools():
    async with stdio_client(
        StdioServerParameters(
            command="python",
            args=["-m", "agent_mvp.mcp_server"]
        )
    ) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            # List available tools
            tools = await session.list_tools()
            print(f"Available tools: {[t.name for t in tools.tools]}")

            # Call a tool
            result = await session.call_tool(
                "list_mock_issues",
                arguments={}
            )
            print(f"Result: {result}")

asyncio.run(test_tools())
```

### Adding New Tools

1. **Define the tool function:**
   ```python
   @mcp.tool()
   async def my_new_tool(
       param: str,
       ctx: Context[ServerSession, None] = None
   ) -> dict[str, Any]:
       """Tool description."""
       if ctx:
           await ctx.info("Doing something...")

       # Implementation
       return {"status": "success", "result": "..."}
   ```

2. **Reinstall package:**
   ```bash
   pip install -e .
   ```

3. **Restart MCP server**

### Adding New Resources

```python
@mcp.resource("namespace://path/{param}")
def get_resource(param: str) -> str:
    """Resource description."""
    return json.dumps({"data": "..."})
```

### Adding New Prompts

```python
@mcp.prompt()
def my_prompt(param: str, option: str = "default") -> str:
    """Prompt description."""
    return f"Please do something with {param} using {option} approach."
```

## Troubleshooting

### Server Won't Start

**Error:** `ModuleNotFoundError: No module named 'mcp'`

**Solution:**
```bash
pip install mcp>=1.0.0
```

**Error:** `ModuleNotFoundError: No module named 'agent_mvp'`

**Solution:**
```bash
pip install -e .
```

### Tools Not Appearing in Claude

1. Check Claude Desktop config file path
2. Verify JSON syntax (no trailing commas)
3. Ensure `cwd` path is correct
4. Restart Claude Desktop completely
5. Check Claude's developer console for errors

### Connection Issues in VS Code

1. Verify virtual environment is active
2. Check `.vscode/mcp.json` syntax
3. Reload VS Code window
4. Check VS Code Output panel → "Language Model" for errors

### Environment Variables Not Loading

**Issue:** LLM calls failing with authentication errors

**Solution:**
- Ensure `.env` file exists in project root
- Check env vars in MCP config: add to `env` section
- For Claude Desktop, use absolute paths in config

### Performance Issues

**Issue:** Tools are slow to respond

**Possible causes:**
- LLM provider API latency
- Large issues taking time to process
- Network issues fetching from GitHub

**Solutions:**
- Use mock issues for testing
- Check LLM provider status
- Consider caching for frequently accessed data

## Best Practices

### Security

- **Never commit credentials** - use environment variables
- **Use separate API keys** for development and production
- **Review prompts** before exposing to users
- **Validate inputs** in all tool functions

### Performance

- **Use progress reporting** for long-running tools
- **Cache resources** when appropriate
- **Batch operations** where possible
- **Set timeouts** for external API calls

### Reliability

- **Handle errors gracefully** - return status objects
- **Log important events** using context methods
- **Validate schemas** for all inputs/outputs
- **Test tools independently** before integration

## Related Documentation

- [MCP Specification](https://spec.modelcontextprotocol.io/)
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- [Claude Desktop Configuration](https://modelcontextprotocol.io/docs/clients/claude-desktop)
- [VS Code MCP Integration](https://code.visualstudio.com/docs/copilot/chat/mcp-servers)
- [Agent MVP Pipeline Documentation](../README.md)

## Support

For issues or questions:
- **GitHub Issues:** [agents2/issues](https://github.com/timothywarner-org/agents2/issues)
- **Email:** tim@techtrainertim.com
- **Website:** [TechTrainerTim.com](https://TechTrainerTim.com)

---

**Last updated:** January 2026
**Version:** 0.1.0
