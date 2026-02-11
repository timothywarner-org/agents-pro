"""
LangGraph pipeline for issue triage and implementation.

Defines the state machine that orchestrates PM -> Dev -> QA flow.
Each node represents a stage in the pipeline.
"""

from __future__ import annotations

import json
import time
from dataclasses import dataclass, field
from typing import Any, Optional, TypedDict
from uuid import uuid4

from langgraph.graph import StateGraph, END

from ..config import get_config
from ..models import (
    Issue,
    PMOutput,
    DevOutput,
    QAOutput,
    PipelineResult,
    RunMetadata,
    AgentTokens,
)
from ..logging_setup import get_pipeline_logger
from ..util.token_tracking import extract_token_usage, format_token_summary
from .prompts import (
    PM_SYSTEM_PROMPT,
    DEV_SYSTEM_PROMPT,
    QA_SYSTEM_PROMPT,
    format_pm_prompt,
    format_dev_prompt,
    format_qa_prompt,
)


# =============================================================================
# Pipeline State
# =============================================================================


class PipelineState(TypedDict, total=False):
    """State passed through the LangGraph pipeline.

    All fields are optional to allow incremental building.
    """
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

    # Token tracking
    token_usages: list[dict]  # List of serialized AgentTokens

    # Final result
    result: Optional[dict]  # Serialized PipelineResult

    # Error tracking
    error: Optional[str]


# =============================================================================
# Node Functions
# =============================================================================


def load_issue_node(state: PipelineState) -> PipelineState:
    """Load and validate the issue.

    This node expects the issue to already be in state (loaded before graph execution).
    It just validates and logs.
    """
    logger = get_pipeline_logger()
    logger.node_enter("load_issue")

    issue_data = state.get("issue")
    if not issue_data:
        logger.error("No issue data in state")
        return {**state, "error": "No issue data provided"}

    # Validate we can parse it
    try:
        issue = Issue(**issue_data)
        logger.agent_message("system", f"Loaded issue: {issue.issue_id}")
        logger.node_exit("load_issue", f"Issue #{issue.issue_number}")
    except Exception as e:
        logger.error(f"Failed to parse issue: {e}")
        return {**state, "error": str(e)}

    return state


def pm_node(state: PipelineState) -> PipelineState:
    """PM agent analyzes the issue and creates a plan."""
    logger = get_pipeline_logger()
    logger.node_enter("pm")

    if state.get("error"):
        return state

    try:
        config = get_config()
        llm = config.get_llm()

        # Parse issue
        issue = Issue(**state["issue"])

        # Create prompt
        prompt = format_pm_prompt(issue)

        # Call LLM
        logger.agent_message("pm", "Analyzing issue and creating plan...")
        response = llm.invoke([
            {"role": "system", "content": PM_SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ])

        # Extract token usage
        token_usage = extract_token_usage(response, config.llm_model)
        if token_usage:
            logger.agent_message(
                "pm",
                f"Tokens: {token_usage.input_tokens} in + {token_usage.output_tokens} out = "
                f"{token_usage.total_tokens} total (${token_usage.estimated_cost_usd:.6f})"
            )
            agent_tokens = AgentTokens(agent_name="PM", usage=token_usage)
            token_usages = state.get("token_usages", [])
            token_usages.append(agent_tokens.model_dump())
        else:
            token_usages = state.get("token_usages", [])

        # Parse response as JSON
        content = response.content
        # Try to extract JSON from response
        pm_data = _extract_json(content)

        if pm_data is None:
            logger.warning("PM response was not valid JSON, using fallback")
            pm_data = {
                "summary": content[:500],
                "acceptance_criteria": ["Review PM response manually"],
                "plan": ["Parse PM output and refine"],
                "assumptions": ["LLM response format issue"],
            }

        pm_output = PMOutput(**pm_data)
        logger.agent_message("pm", f"Created {len(pm_output.plan)} plan steps")
        logger.node_exit("pm", f"{len(pm_output.acceptance_criteria)} criteria")

        return {**state, "pm_output": pm_output.model_dump(), "token_usages": token_usages}

    except Exception as e:
        logger.error(f"PM agent failed: {e}", e)
        return {**state, "error": f"PM agent failed: {e}"}


def dev_node(state: PipelineState) -> PipelineState:
    """Dev agent implements the PM's plan."""
    logger = get_pipeline_logger()
    logger.node_enter("dev")

    if state.get("error"):
        return state

    try:
        config = get_config()
        llm = config.get_llm()

        # Parse inputs
        issue = Issue(**state["issue"])
        pm_output = PMOutput(**state["pm_output"])

        # Create prompt
        prompt = format_dev_prompt(issue, pm_output)

        # Call LLM
        logger.agent_message("dev", "Implementing feature...")
        response = llm.invoke([
            {"role": "system", "content": DEV_SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ])

        # Extract token usage
        token_usage = extract_token_usage(response, config.llm_model)
        if token_usage:
            logger.agent_message(
                "dev",
                f"Tokens: {token_usage.input_tokens} in + {token_usage.output_tokens} out = "
                f"{token_usage.total_tokens} total (${token_usage.estimated_cost_usd:.6f})"
            )
            agent_tokens = AgentTokens(agent_name="Dev", usage=token_usage)
            token_usages = state.get("token_usages", [])
            token_usages.append(agent_tokens.model_dump())
        else:
            token_usages = state.get("token_usages", [])

        # Parse response
        content = response.content
        dev_data = _extract_json(content)

        if dev_data is None:
            logger.warning("Dev response was not valid JSON, using fallback")
            dev_data = {
                "files": [{
                    "path": "implementation.txt",
                    "content": content,
                    "language": "text",
                }],
                "notes": ["Response was not structured JSON"],
            }

        dev_output = DevOutput(**dev_data)
        logger.agent_message("dev", f"Created {len(dev_output.files)} file(s)")
        logger.node_exit("dev", f"{len(dev_output.files)} files")

        return {**state, "dev_output": dev_output.model_dump(), "token_usages": token_usages}

    except Exception as e:
        logger.error(f"Dev agent failed: {e}", e)
        return {**state, "error": f"Dev agent failed: {e}"}


def qa_node(state: PipelineState) -> PipelineState:
    """QA agent reviews the implementation."""
    logger = get_pipeline_logger()
    logger.node_enter("qa")

    if state.get("error"):
        return state

    try:
        config = get_config()
        llm = config.get_llm()

        # Parse inputs
        issue = Issue(**state["issue"])
        pm_output = PMOutput(**state["pm_output"])
        dev_output = DevOutput(**state["dev_output"])

        # Create prompt
        prompt = format_qa_prompt(issue, pm_output, dev_output)

        # Call LLM
        logger.agent_message("qa", "Reviewing implementation...")
        response = llm.invoke([
            {"role": "system", "content": QA_SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ])

        # Extract token usage
        token_usage = extract_token_usage(response, config.llm_model)
        if token_usage:
            logger.agent_message(
                "qa",
                f"Tokens: {token_usage.input_tokens} in + {token_usage.output_tokens} out = "
                f"{token_usage.total_tokens} total (${token_usage.estimated_cost_usd:.6f})"
            )
            agent_tokens = AgentTokens(agent_name="QA", usage=token_usage)
            token_usages = state.get("token_usages", [])
            token_usages.append(agent_tokens.model_dump())
        else:
            token_usages = state.get("token_usages", [])

        # Parse response
        content = response.content
        qa_data = _extract_json(content)

        if qa_data is None:
            logger.warning("QA response was not valid JSON, using fallback")
            qa_data = {
                "verdict": "needs-human",
                "findings": ["Response was not structured JSON", content[:200]],
                "suggested_changes": ["Review QA output manually"],
            }

        qa_output = QAOutput(**qa_data)
        logger.agent_message("qa", f"Verdict: {qa_output.verdict.value}")
        logger.node_exit("qa", qa_output.verdict.value)

        return {**state, "qa_output": qa_output.model_dump(), "token_usages": token_usages}

    except Exception as e:
        logger.error(f"QA agent failed: {e}", e)
        return {**state, "error": f"QA agent failed: {e}"}


def finalize_node(state: PipelineState) -> PipelineState:
    """Finalize the pipeline run and create the result."""
    logger = get_pipeline_logger()
    logger.node_enter("finalize")

    if state.get("error"):
        # Create error result
        error_result = {
            "run_id": state.get("run_id", str(uuid4())),
            "timestamp_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "error": state["error"],
            "issue": state.get("issue"),
        }
        logger.node_exit("finalize", "Error result created")
        return {**state, "result": error_result}

    try:
        # Import here to avoid circular import
        from ..util.token_tracking import aggregate_pipeline_tokens, format_token_summary

        # Build the final result
        issue = Issue(**state["issue"])
        pm_output = PMOutput(**state["pm_output"])
        dev_output = DevOutput(**state["dev_output"])
        qa_output = QAOutput(**state["qa_output"])

        # Calculate duration
        duration = None
        if "start_time" in state:
            duration = time.time() - state["start_time"]

        # Aggregate token usage
        pipeline_tokens = None
        if state.get("token_usages"):
            agent_tokens_list = [AgentTokens(**t) for t in state["token_usages"]]
            pipeline_tokens = aggregate_pipeline_tokens(agent_tokens_list)

            # Log token summary to console
            print("\n" + format_token_summary(pipeline_tokens))

        metadata = RunMetadata(
            run_id=state.get("run_id", str(uuid4())),
            source_file=state.get("source_file"),
            duration_seconds=duration,
            token_usage=pipeline_tokens,
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


def create_pipeline_graph() -> StateGraph:
    """Create the LangGraph pipeline.

    Returns:
        Compiled StateGraph ready for execution.
    """
    # Create the graph
    builder = StateGraph(PipelineState)

    # Add nodes
    builder.add_node("load_issue", load_issue_node)
    builder.add_node("pm", pm_node)
    builder.add_node("dev", dev_node)
    builder.add_node("qa", qa_node)
    builder.add_node("finalize", finalize_node)

    # Define edges (linear flow)
    builder.set_entry_point("load_issue")
    builder.add_edge("load_issue", "pm")
    builder.add_edge("pm", "dev")
    builder.add_edge("dev", "qa")
    builder.add_edge("qa", "finalize")
    builder.add_edge("finalize", END)

    # Compile
    return builder.compile()


# =============================================================================
# Helpers
# =============================================================================


def _extract_json(text: str) -> Optional[dict]:
    """Extract JSON from LLM response text.

    Handles common patterns:
    - Pure JSON
    - JSON in markdown code blocks
    - JSON with surrounding text

    Args:
        text: LLM response text.

    Returns:
        Parsed dict or None if extraction fails.
    """
    import re

    # Try direct parse first
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    # Try to find JSON in code blocks
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
