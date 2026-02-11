"""
Runner for the CrewAI-based pipeline variant.

Usage:
    python -m agent_mvp.pipeline.crew_variant.runner path/to/issue.json

This demonstrates running the same pipeline flow using CrewAI agents
instead of raw LLM calls.
"""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path
from uuid import uuid4

from .graph import create_crew_pipeline_graph, CrewPipelineState


def run_crew_pipeline(issue_path: str) -> dict:
    """Run the CrewAI-based pipeline on an issue file.

    Args:
        issue_path: Path to JSON file containing issue data.

    Returns:
        Pipeline result dict.
    """
    # Load issue
    issue_file = Path(issue_path)
    if not issue_file.exists():
        raise FileNotFoundError(f"Issue file not found: {issue_path}")

    with open(issue_file) as f:
        issue_data = json.load(f)

    # Initialize state
    initial_state: CrewPipelineState = {
        "run_id": str(uuid4()),
        "start_time": time.time(),
        "source_file": str(issue_file),
        "issue": issue_data,
    }

    # Create and run pipeline
    print("\n" + "=" * 60)
    print("CrewAI Pipeline Variant")
    print("=" * 60)
    print(f"Issue: {issue_data.get('title', 'Unknown')}")
    print(f"Run ID: {initial_state['run_id']}")
    print("=" * 60 + "\n")

    graph = create_crew_pipeline_graph()
    final_state = graph.invoke(initial_state)

    # Output result
    if final_state.get("error"):
        print(f"\n❌ Pipeline failed: {final_state['error']}")
    else:
        print("\n✅ Pipeline completed successfully")
        if final_state.get("qa_output"):
            verdict = final_state["qa_output"].get("verdict", "unknown")
            print(f"   QA Verdict: {verdict}")

    return final_state.get("result", {})


def main():
    """CLI entry point."""
    if len(sys.argv) < 2:
        print("Usage: python -m agent_mvp.pipeline.crew_variant.runner <issue.json>")
        sys.exit(1)

    result = run_crew_pipeline(sys.argv[1])

    # Pretty print result
    print("\n" + "=" * 60)
    print("Pipeline Result")
    print("=" * 60)
    print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":
    main()
