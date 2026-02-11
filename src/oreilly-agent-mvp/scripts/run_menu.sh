#!/bin/bash
# Start the interactive menu for the O'Reilly Agent MVP

set -e

# Activate virtual environment
source .venv/Scripts/activate

echo "Starting O'Reilly Agent MVP Interactive Menu..."
echo ""

# Run the menu
python -m agent_mvp.cli.interactive_menu
