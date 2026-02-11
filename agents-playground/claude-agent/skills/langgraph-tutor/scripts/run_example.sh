#!/bin/bash
# Run LangGraph examples with proper environment setup

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
EXAMPLES_DIR="$SCRIPT_DIR/../examples"

echo "======================================"
echo "LangGraph Example Runner"
echo "======================================"

# Check for virtual environment
if [ -z "$VIRTUAL_ENV" ]; then
    echo "Warning: No virtual environment detected"
    echo "Consider activating a venv with LangGraph installed"
    echo ""
fi

# Check for ANTHROPIC_API_KEY
if [ -z "$ANTHROPIC_API_KEY" ]; then
    echo "Error: ANTHROPIC_API_KEY environment variable not set"
    echo ""
    echo "Set it with:"
    echo "  export ANTHROPIC_API_KEY=your-key-here"
    exit 1
fi

# List available examples
echo ""
echo "Available examples:"
echo "  1. simple_chatbot.py  - Basic chatbot with memory"
echo "  2. tool_agent.py      - Agent with calculator, weather, search"
echo "  3. multi_agent.py     - Supervisor pattern multi-agent"
echo ""

# Get user choice
read -p "Enter example number (1-3): " choice

case $choice in
    1)
        python "$EXAMPLES_DIR/simple_chatbot.py"
        ;;
    2)
        python "$EXAMPLES_DIR/tool_agent.py"
        ;;
    3)
        python "$EXAMPLES_DIR/multi_agent.py"
        ;;
    *)
        echo "Invalid choice. Please enter 1, 2, or 3."
        exit 1
        ;;
esac
