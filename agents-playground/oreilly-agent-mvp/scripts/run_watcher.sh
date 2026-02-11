#!/bin/bash
# Start the folder watcher for event-driven processing

set -e

# Activate virtual environment
source .venv/Scripts/activate

echo "Starting folder watcher..."
echo "Drop issue JSON files into incoming/ to trigger processing"
echo "Press Ctrl+C to stop"
echo ""

# Run the watcher
python -m agent_mvp.watcher.folder_watcher
