"""
CrewAI agent definitions for PM, Dev, and QA roles.

This module provides an alternative orchestration approach using CrewAI's
agent collaboration patterns. The LangGraph pipeline (graph.py) is the
primary orchestration, but this demonstrates CrewAI concepts.

Note: For the MVP, we keep prompts short and avoid tool-calling to
focus on teachability.
"""

from __future__ import annotations

import os
from typing import Optional

from crewai import Agent, Crew, Process, Task
from crewai import LLM

from ..config import get_config, LLMProvider
from ..models import Issue, PMOutput, DevOutput, QAOutput


# =============================================================================
# Agent Definitions
# =============================================================================


class PMAgent:
    """Product Manager agent that analyzes issues and creates plans.

    Responsibilities:
    - Understand the issue requirements
    - Define clear acceptance criteria
    - Create an implementation plan
    - Document assumptions
    """

    ROLE = "Product Manager"
    GOAL = "Analyze GitHub issues and create clear, actionable implementation plans"
    BACKSTORY = """You are a seasoned Product Manager with experience in software development.
You excel at breaking down feature requests into clear requirements and actionable plans.
You focus on user value and practical implementation paths."""

    @classmethod
    def create(cls, llm: Optional[LLM] = None) -> Agent:
        """Create the PM agent instance.

        Args:
            llm: Optional LLM instance. Uses config default if not provided.

        Returns:
            Configured Agent instance.
        """
        return Agent(
            role=cls.ROLE,
            goal=cls.GOAL,
            backstory=cls.BACKSTORY,
            llm=llm or _get_crew_llm(),
            verbose=True,
            allow_delegation=False,
        )


class DevAgent:
    """Developer agent that implements features.

    Responsibilities:
    - Write clean, working code
    - Create tests for the implementation
    - Document implementation decisions
    """

    ROLE = "Senior Developer"
    GOAL = "Implement features with clean, tested code"
    BACKSTORY = """You are a Senior Developer with strong coding skills.
You write practical, maintainable code and always include tests.
You focus on getting things done right the first time."""

    @classmethod
    def create(cls, llm: Optional[LLM] = None) -> Agent:
        """Create the Dev agent instance.

        Args:
            llm: Optional LLM instance.

        Returns:
            Configured Agent instance.
        """
        return Agent(
            role=cls.ROLE,
            goal=cls.GOAL,
            backstory=cls.BACKSTORY,
            llm=llm or _get_crew_llm(),
            verbose=True,
            allow_delegation=False,
        )


class QAAgent:
    """QA Engineer agent that reviews implementations.

    Responsibilities:
    - Verify code meets requirements
    - Identify bugs and issues
    - Suggest improvements
    - Provide clear verdict
    """

    ROLE = "QA Engineer"
    GOAL = "Ensure implementations meet requirements and identify issues"
    BACKSTORY = """You are a thorough QA Engineer who catches bugs others miss.
You verify implementations against acceptance criteria.
You provide clear, actionable feedback."""

    @classmethod
    def create(cls, llm: Optional[LLM] = None) -> Agent:
        """Create the QA agent instance.

        Args:
            llm: Optional LLM instance.

        Returns:
            Configured Agent instance.
        """
        return Agent(
            role=cls.ROLE,
            goal=cls.GOAL,
            backstory=cls.BACKSTORY,
            llm=llm or _get_crew_llm(),
            verbose=True,
            allow_delegation=False,
        )


# =============================================================================
# Task Definitions
# =============================================================================


def create_pm_task(issue: Issue, agent: Agent) -> Task:
    """Create the PM analysis task.

    Args:
        issue: The issue to analyze.
        agent: The PM agent.

    Returns:
        Configured Task.
    """
    return Task(
        description=f"""Analyze this GitHub issue and create an implementation plan.

Issue: {issue.title}
Repository: {issue.repo}
Labels: {', '.join(issue.labels) if issue.labels else 'None'}

Description:
{issue.body or '(No description)'}

Your output should be a JSON object with:
- summary: Brief summary (1-2 sentences)
- acceptance_criteria: List of 3-5 criteria
- plan: List of 3-7 implementation steps
- assumptions: List of any assumptions made
""",
        expected_output="JSON object with summary, acceptance_criteria, plan, and assumptions",
        agent=agent,
    )


def create_dev_task(issue: Issue, pm_output: PMOutput, agent: Agent) -> Task:
    """Create the Dev implementation task.

    Args:
        issue: The original issue.
        pm_output: PM's analysis.
        agent: The Dev agent.

    Returns:
        Configured Task.
    """
    criteria = "\n".join(f"- {c}" for c in pm_output.acceptance_criteria)
    plan = "\n".join(f"{i+1}. {s}" for i, s in enumerate(pm_output.plan))

    return Task(
        description=f"""Implement this feature based on the PM's plan.

Issue: {issue.title}
Summary: {pm_output.summary}

Acceptance Criteria:
{criteria}

Implementation Plan:
{plan}

Your output should be a JSON object with:
- files: Array of {{path, content, language}} objects
- notes: Array of implementation notes
""",
        expected_output="JSON object with files array and notes array",
        agent=agent,
    )


def create_qa_task(
    issue: Issue,
    pm_output: PMOutput,
    dev_output: DevOutput,
    agent: Agent,
) -> Task:
    """Create the QA review task.

    Args:
        issue: The original issue.
        pm_output: PM's analysis.
        dev_output: Dev's implementation.
        agent: The QA agent.

    Returns:
        Configured Task.
    """
    criteria = "\n".join(f"- {c}" for c in pm_output.acceptance_criteria)
    files = "\n".join(f"- {f.path}" for f in dev_output.files)

    return Task(
        description=f"""Review this implementation against requirements.

Issue: {issue.title}

Acceptance Criteria:
{criteria}

Files Implemented:
{files}

Developer Notes:
{chr(10).join('- ' + n for n in dev_output.notes) if dev_output.notes else 'None'}

Your output should be a JSON object with:
- verdict: "pass", "fail", or "needs-human"
- findings: Array of issues found
- suggested_changes: Array of improvement suggestions
""",
        expected_output="JSON object with verdict, findings, and suggested_changes",
        agent=agent,
    )


# =============================================================================
# Crew Builder
# =============================================================================


def create_crew(issue: Issue) -> Crew:
    """Create a CrewAI crew for processing an issue.

    This creates a sequential crew: PM -> Dev -> QA

    Note: For the MVP, we use Process.sequential for simplicity.
    In production, you might use hierarchical or custom processes.

    Args:
        issue: The issue to process.

    Returns:
        Configured Crew ready for kickoff.
    """
    llm = _get_crew_llm()

    # Create agents
    pm_agent = PMAgent.create(llm)
    dev_agent = DevAgent.create(llm)
    qa_agent = QAAgent.create(llm)

    # Create initial task (PM)
    pm_task = create_pm_task(issue, pm_agent)

    # Note: In CrewAI, tasks are typically defined upfront.
    # For dynamic task creation based on previous outputs,
    # you'd use callbacks or the hierarchical process.
    # For MVP simplicity, we'll use the LangGraph pipeline instead.

    return Crew(
        agents=[pm_agent, dev_agent, qa_agent],
        tasks=[pm_task],  # Simplified for MVP
        process=Process.sequential,
        verbose=True,
    )


# =============================================================================
# Helpers
# =============================================================================


def _get_crew_llm() -> LLM:
    """Get the LLM configured for CrewAI.

    CrewAI uses its own LLM wrapper, so we need to configure it
    based on our settings.

    Returns:
        Configured LLM for CrewAI.
    """
    config = get_config()

    if config.llm_provider == LLMProvider.ANTHROPIC:
        return LLM(
            model=f"anthropic/{config.llm_model}",
            temperature=config.llm_temperature,
            api_key=config.anthropic_api_key,
        )
    elif config.llm_provider == LLMProvider.OPENAI:
        kwargs = {
            "model": f"openai/{config.llm_model}",
            "temperature": config.llm_temperature,
            "api_key": config.openai_api_key,
        }
        # Add base_url for OpenAI-compatible APIs (DeepSeek, etc.)
        if config.openai_base_url:
            kwargs["base_url"] = config.openai_base_url
        return LLM(**kwargs)
    elif config.llm_provider == LLMProvider.AZURE:
        # Azure OpenAI through CrewAI
        return LLM(
            model=f"azure/{config.azure_openai_deployment}",
            temperature=config.llm_temperature,
            api_key=config.azure_openai_api_key,
            base_url=config.azure_openai_endpoint,
        )
    else:
        raise ValueError(f"Unsupported LLM provider: {config.llm_provider}")
