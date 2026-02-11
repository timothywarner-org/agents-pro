#!/bin/bash
# Setup script for the O'Reilly Agent MVP project

set -e

echo "Setting up O'Reilly Agent MVP..."

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python -m venv .venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source .venv/Scripts/activate

# Upgrade pip
echo "Upgrading pip..."
python -m pip install --upgrade pip

# Install the package in editable mode with dependencies
echo "Installing agent_mvp package and dependencies..."
pip install -e .

# Create necessary directories
echo "Creating workflow directories..."
mkdir -p incoming outgoing processed

echo ""
echo "Setup complete! ✓"
echo ""
echo "Next steps:"
echo "1. Ensure your .env file has API credentials configured"
echo "2. Run './scripts/run_once.sh' to test the pipeline"
echo "3. Run './scripts/run_watcher.sh' to start the folder watcher"
