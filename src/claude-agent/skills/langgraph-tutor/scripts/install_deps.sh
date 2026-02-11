#!/bin/bash
# Install LangGraph dependencies

set -e

echo "======================================"
echo "Installing LangGraph Dependencies"
echo "======================================"

# Check Python version
python_version=$(python --version 2>&1 | cut -d' ' -f2 | cut -d'.' -f1,2)
echo "Python version: $python_version"

if [[ $(echo "$python_version < 3.9" | bc -l) -eq 1 ]]; then
    echo "Error: Python 3.9+ required"
    exit 1
fi

# Install dependencies
echo ""
echo "Installing packages..."

pip install --upgrade pip

# Core LangGraph
pip install langgraph>=0.2.0

# LangChain core
pip install langchain-core>=0.3.0

# Anthropic (for Claude)
pip install langchain-anthropic>=0.2.0

# OpenAI (optional, for GPT models)
pip install langchain-openai>=0.2.0

echo ""
echo "======================================"
echo "Installation complete!"
echo ""
echo "Installed packages:"
pip show langgraph | grep -E "^(Name|Version):"
pip show langchain-core | grep -E "^(Name|Version):"
pip show langchain-anthropic | grep -E "^(Name|Version):"
echo ""
echo "Don't forget to set your API key:"
echo "  export ANTHROPIC_API_KEY=your-key-here"
echo "======================================"
