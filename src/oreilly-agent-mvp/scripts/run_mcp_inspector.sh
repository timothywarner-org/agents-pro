#!/usr/bin/env bash
# Run the MCP server with MCP Inspector for debugging and testing

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

cd "$PROJECT_ROOT"

# Activate virtual environment if it exists
if [ -d ".venv" ]; then
    source .venv/Scripts/activate 2>/dev/null || source .venv/bin/activate
fi

echo "============================================================"
echo "  MCP Inspector - O'Reilly Agent MVP Server"
echo "============================================================"
echo ""
echo "Starting MCP Inspector..."
echo "This opens a web UI for testing MCP tools, resources, and prompts."
echo ""
echo "Prerequisites:"
echo "  - Node.js installed (for npx)"
echo "  - Internet connection (downloads inspector on first run)"
echo ""
echo "The inspector will:"
echo "  1. Launch the MCP server (agent-mvp)"
echo "  2. Open a browser with interactive testing UI"
echo "  3. Let you call tools, browse resources, and test prompts"
echo ""
echo "Press Ctrl+C to stop both server and inspector."
echo ""
echo "============================================================"
echo ""

# Check if Node.js is available
if ! command -v node &> /dev/null; then
    echo "ERROR: Node.js not found!"
    echo ""
    echo "MCP Inspector requires Node.js."
    echo "Install from: https://nodejs.org/"
    echo ""
    exit 1
fi

# Run MCP Inspector
# It will automatically download and run the inspector
npx @modelcontextprotocol/inspector python -m agent_mvp.mcp_server
