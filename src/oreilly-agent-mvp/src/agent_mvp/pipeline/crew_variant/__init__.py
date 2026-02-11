"""
CrewAI-based pipeline variant.

This module demonstrates using CrewAI agents within LangGraph nodes.
Each node uses a CrewAI Agent to execute a single Task, giving you
the best of both worlds:
- CrewAI's agent abstractions (role, goal, backstory)
- LangGraph's explicit state management and control flow

Compare with ../graph.py which uses raw LLM calls instead of CrewAI.
"""

from .graph import create_crew_pipeline_graph, CrewPipelineState
from .agents import PMAgent, DevAgent, QAAgent

__all__ = [
    "create_crew_pipeline_graph",
    "CrewPipelineState",
    "PMAgent",
    "DevAgent",
    "QAAgent",
]
