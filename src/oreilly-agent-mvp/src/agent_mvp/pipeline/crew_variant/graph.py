"""
LangGraph pipeline using CrewAI agents.

This variant uses CrewAI's Agent abstraction within LangGraph nodes.
Each node runs a single-agent Crew with one Task, giving you:
- CrewAI's role/goal/backstory agent shaping
- LangGraph's explicit state management and flow control

Key difference from ../graph.py:
- There: Raw LLM calls with system prompts
- Here: CrewAI Agent.execute_task() with role-based prompting

Each node = 1 Agent + 1 Task = 1 Crew.kickoff()
"""

from __future__ import annotations

import json
import re
import time
from typing import Optional, TypedDict
from uuid import uuid4

from crewai import Crew, Process
from langgraph.graph import StateGraph, END

from ...config import get_config
from ...models import (
    Issue,
    PMOutput,
    DevOutput,
    QAOutput,
    PipelineResult,
    RunMetadata,
)
from ...logging_setup import get_pipeline_logger

from .agents import PMAgent, DevAgent, QAAgent, get_crew_llm
from .tasks import create_pm_task, create_dev_task, create_qa_task


# =============================================================================
# Pipeline State
# =============================================================================


class CrewPipelineState(TypedDict, total=False):
    """State passed through the CrewAI-based LangGraph pipeline."""

    # Run metadata
    run_id: str
    start_time: float
    source_file: Optional[str]

    # Input
    issue: Optional[dict]  # Serialized Issue

    # Agent outputs
    pm_output: Optional[dict]  # Serialized PMOutput
    dev_output: Optional[dict]  # Serialized DevOutput
    qa_output: Optional[dict]  # Serialized QAOutput

    # Final result
    result: Optional[dict]  # Serialized PipelineResult

    # Error tracking
    error: Optional[str]


# =============================================================================
# Node Functions
# =============================================================================


def load_issue_node(state: CrewPipelineState) -> CrewPipelineState:
    """Load and validate the issue."""
    logger = get_pipeline_logger()
    logger.node_enter("load_issue")

    issue_data = state.get("issue")
    if not issue_data:
        logger.error("No issue data in state")
        return {**state, "error": "No issue data provided"}

    try:
        issue = Issue(**issue_data)
        logger.agent_message("system", f"Loaded issue: {issue.issue_id}")
        logger.node_exit("load_issue", f"Issue #{issue.issue_number}")
    except Exception as e:
        logger.error(f"Failed to parse issue: {e}")
        return {**state, "error": str(e)}

    return state


def pm_crew_node(state: CrewPipelineState) -> CrewPipelineState:
    """PM agent analyzes the issue using CrewAI.

    Creates a single-agent Crew with one Task and kicks it off.
    This is one of 3 "mini-crews" in our pipeline.
    """
    logger = get_pipeline_logger()
    logger.node_enter("pm_crew")

    if state.get("error"):
        return state

    try:
        # Parse input
        issue = Issue(**state["issue"])

        # Create agent and task
        llm = get_crew_llm()
        pm_agent = PMAgent.create(llm)
        pm_task = create_pm_task(issue, pm_agent)

        # Create single-agent Crew and run
        # This is ONE Crew.kickoff() call for the PM node
        logger.agent_message("pm", "CrewAI agent analyzing issue...")
        crew = Crew(
            agents=[pm_agent],
            tasks=[pm_task],
            process=Process.sequential,
            verbose=True,
        )
        result = crew.kickoff()

        # Parse the output
        pm_data = _extract_json(result.raw)
        if pm_data is None:
            logger.warning("PM response was not valid JSON, using fallback")
            pm_data = {
                "summary": str(result.raw)[:500],
                "acceptance_criteria": ["Review PM response manually"],
                "plan": ["Parse PM output and refine"],
                "assumptions": ["LLM response format issue"],
            }

        pm_output = PMOutput(**pm_data)
        logger.agent_message("pm", f"Created {len(pm_output.plan)} plan steps")
        logger.node_exit("pm_crew", f"{len(pm_output.acceptance_criteria)} criteria")

        return {**state, "pm_output": pm_output.model_dump()}

    except Exception as e:
        logger.error(f"PM crew failed: {e}", e)
        return {**state, "error": f"PM crew failed: {e}"}


def dev_crew_node(state: CrewPipelineState) -> CrewPipelineState:
    """Dev agent implements the feature using CrewAI.

    Second mini-crew: receives PM output, produces implementation.
    """
    logger = get_pipeline_logger()
    logger.node_enter("dev_crew")

    if state.get("error"):
        return state

    try:
        # Parse inputs
        issue = Issue(**state["issue"])
        pm_output = PMOutput(**state["pm_output"])

        # Create agent and task
        llm = get_crew_llm()
        dev_agent = DevAgent.create(llm)
        dev_task = create_dev_task(issue, pm_output, dev_agent)

        # Create single-agent Crew and run
        # This is ONE Crew.kickoff() call for the Dev node
        logger.agent_message("dev", "CrewAI agent implementing feature...")
        crew = Crew(
            agents=[dev_agent],
            tasks=[dev_task],
            process=Process.sequential,
            verbose=True,
        )
        result = crew.kickoff()

        # Parse the output
        dev_data = _extract_json(result.raw)
        if dev_data is None:
            logger.warning("Dev response was not valid JSON, using fallback")
            dev_data = {
                "files": [{
                    "path": "implementation.txt",
                    "content": str(result.raw),
                    "language": "text",
                }],
                "notes": ["Response was not structured JSON"],
            }

        dev_output = DevOutput(**dev_data)
        logger.agent_message("dev", f"Created {len(dev_output.files)} file(s)")
        logger.node_exit("dev_crew", f"{len(dev_output.files)} files")

        return {**state, "dev_output": dev_output.model_dump()}

    except Exception as e:
        logger.error(f"Dev crew failed: {e}", e)
        return {**state, "error": f"Dev crew failed: {e}"}


def qa_crew_node(state: CrewPipelineState) -> CrewPipelineState:
    """QA agent reviews the implementation using CrewAI.

    Third mini-crew: receives all prior outputs, produces verdict.
    """
    logger = get_pipeline_logger()
    logger.node_enter("qa_crew")

    if state.get("error"):
        return state

    try:
        # Parse inputs
        issue = Issue(**state["issue"])
        pm_output = PMOutput(**state["pm_output"])
        dev_output = DevOutput(**state["dev_output"])

        # Create agent and task
        llm = get_crew_llm()
        qa_agent = QAAgent.create(llm)
        qa_task = create_qa_task(issue, pm_output, dev_output, qa_agent)

        # Create single-agent Crew and run
        # This is ONE Crew.kickoff() call for the QA node
        logger.agent_message("qa", "CrewAI agent reviewing implementation...")
        crew = Crew(
            agents=[qa_agent],
            tasks=[qa_task],
            process=Process.sequential,
            verbose=True,
        )
        result = crew.kickoff()

        # Parse the output
        qa_data = _extract_json(result.raw)
        if qa_data is None:
            logger.warning("QA response was not valid JSON, using fallback")
            qa_data = {
                "verdict": "needs-human",
                "findings": ["Response was not structured JSON"],
                "suggested_changes": ["Review QA output manually"],
            }

        qa_output = QAOutput(**qa_data)
        logger.agent_message("qa", f"Verdict: {qa_output.verdict.value}")
        logger.node_exit("qa_crew", qa_output.verdict.value)

        return {**state, "qa_output": qa_output.model_dump()}

    except Exception as e:
        logger.error(f"QA crew failed: {e}", e)
        return {**state, "error": f"QA crew failed: {e}"}


def finalize_node(state: CrewPipelineState) -> CrewPipelineState:
    """Finalize the pipeline run and create the result."""
    logger = get_pipeline_logger()
    logger.node_enter("finalize")

    if state.get("error"):
        error_result = {
            "run_id": state.get("run_id", str(uuid4())),
            "timestamp_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "error": state["error"],
            "issue": state.get("issue"),
        }
        logger.node_exit("finalize", "Error result created")
        return {**state, "result": error_result}

    try:
        issue = Issue(**state["issue"])
        pm_output = PMOutput(**state["pm_output"])
        dev_output = DevOutput(**state["dev_output"])
        qa_output = QAOutput(**state["qa_output"])

        duration = None
        if "start_time" in state:
            duration = time.time() - state["start_time"]

        metadata = RunMetadata(
            run_id=state.get("run_id", str(uuid4())),
            source_file=state.get("source_file"),
            duration_seconds=duration,
        )

        result = PipelineResult.create(
            issue=issue,
            pm=pm_output,
            dev=dev_output,
            qa=qa_output,
            metadata=metadata,
        )

        logger.node_exit("finalize", "Result created")
        return {**state, "result": result.model_dump()}

    except Exception as e:
        logger.error(f"Finalization failed: {e}", e)
        return {**state, "error": f"Finalization failed: {e}"}


# =============================================================================
# Graph Builder
# =============================================================================


def create_crew_pipeline_graph() -> StateGraph:
    """Create the LangGraph pipeline using CrewAI agents.

    Graph structure:
        load_issue -> pm_crew -> dev_crew -> qa_crew -> finalize -> END

    Each *_crew node runs a single-agent CrewAI Crew.
    Total: 3 Crew.kickoff() calls per pipeline run.

    Returns:
        Compiled StateGraph ready for execution.
    """
    builder = StateGraph(CrewPipelineState)

    # Add nodes
    builder.add_node("load_issue", load_issue_node)
    builder.add_node("pm_crew", pm_crew_node)      # Crew #1
    builder.add_node("dev_crew", dev_crew_node)    # Crew #2
    builder.add_node("qa_crew", qa_crew_node)      # Crew #3
    builder.add_node("finalize", finalize_node)

    # Define edges (linear flow)
    builder.set_entry_point("load_issue")
    builder.add_edge("load_issue", "pm_crew")
    builder.add_edge("pm_crew", "dev_crew")
    builder.add_edge("dev_crew", "qa_crew")
    builder.add_edge("qa_crew", "finalize")
    builder.add_edge("finalize", END)

    return builder.compile()


# =============================================================================
# Helpers
# =============================================================================


def _extract_json(text: str) -> Optional[dict]:
    """Extract JSON from CrewAI output text."""
    # Try direct parse first
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    # Try to find JSON in code blocks or raw
    patterns = [
        r"```json\s*([\s\S]*?)\s*```",
        r"```\s*([\s\S]*?)\s*```",
        r"\{[\s\S]*\}",
    ]

    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            try:
                json_str = match.group(1) if match.lastindex else match.group(0)
                return json.loads(json_str)
            except json.JSONDecodeError:
                continue

    return None
