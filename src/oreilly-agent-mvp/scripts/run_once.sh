#!/bin/bash
# Run the agent pipeline once with an optional mock issue file

set -e

# Activate virtual environment
source .venv/Scripts/activate

# Use provided mock issue or default
MOCK_ISSUE=${1:-"mock_issues/issue_001.json"}

echo "Running agent pipeline with: $MOCK_ISSUE"
echo ""

# Run the pipeline
python -m agent_mvp.pipeline.run_once "$MOCK_ISSUE"

echo ""
echo "Pipeline complete! Check outgoing/ for results."
