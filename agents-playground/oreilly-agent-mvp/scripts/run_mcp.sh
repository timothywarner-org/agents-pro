#!/usr/bin/env bash
# Run the MCP server for O'Reilly Agent MVP

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

cd "$PROJECT_ROOT"

# Activate virtual environment if it exists
if [ -d ".venv" ]; then
    source .venv/Scripts/activate 2>/dev/null || source .venv/bin/activate
fi

echo "Starting O'Reilly Agent MVP MCP Server..."
echo "Project root: $PROJECT_ROOT"
echo ""
echo "The server will listen on stdio for MCP client connections."
echo "Press Ctrl+C to stop."
echo ""

python -m agent_mvp.mcp_server
