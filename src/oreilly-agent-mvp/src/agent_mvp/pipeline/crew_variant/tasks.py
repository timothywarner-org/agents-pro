"""
CrewAI task definitions for the pipeline.

Tasks define what each agent should do. Unlike the full Crew approach
where tasks are chained via `context`, here each task is standalone
and executed individually within a LangGraph node.
"""

from __future__ import annotations

from crewai import Agent, Task

from ...models import Issue, PMOutput, DevOutput


def create_pm_task(issue: Issue, agent: Agent) -> Task:
    """Create the PM analysis task.

    Args:
        issue: The GitHub issue to analyze.
        agent: The PM agent to assign.

    Returns:
        Task configured for PM analysis.
    """
    return Task(
        description=f"""Analyze this GitHub issue and create an implementation plan.

Issue: {issue.title}
Repository: {issue.repo}
Labels: {', '.join(issue.labels) if issue.labels else 'None'}

Description:
{issue.body or '(No description provided)'}

Your output MUST be a valid JSON object with these exact fields:
- "summary": Brief 1-2 sentence summary of what needs to be built
- "acceptance_criteria": Array of 3-5 specific, testable criteria
- "plan": Array of 3-7 ordered implementation steps
- "assumptions": Array of any assumptions you made

Output ONLY the JSON object, no markdown or explanation.""",
        expected_output="JSON object with summary, acceptance_criteria, plan, and assumptions",
        agent=agent,
    )


def create_dev_task(issue: Issue, pm_output: PMOutput, agent: Agent) -> Task:
    """Create the Dev implementation task.

    Args:
        issue: The original GitHub issue.
        pm_output: The PM's analysis and plan.
        agent: The Dev agent to assign.

    Returns:
        Task configured for implementation.
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

Your output MUST be a valid JSON object with these exact fields:
- "files": Array of objects, each with "path", "content", and "language"
- "notes": Array of implementation notes or decisions made

Output ONLY the JSON object, no markdown or explanation.""",
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
        issue: The original GitHub issue.
        pm_output: The PM's analysis and acceptance criteria.
        dev_output: The Dev's implementation.
        agent: The QA agent to assign.

    Returns:
        Task configured for QA review.
    """
    criteria = "\n".join(f"- {c}" for c in pm_output.acceptance_criteria)
    files_summary = "\n".join(
        f"- {f.path} ({f.language}, {len(f.content)} chars)"
        for f in dev_output.files
    )

    return Task(
        description=f"""Review this implementation against the requirements.

Issue: {issue.title}
Summary: {pm_output.summary}

Acceptance Criteria to verify:
{criteria}

Files Implemented:
{files_summary}

Developer Notes:
{chr(10).join('- ' + n for n in dev_output.notes) if dev_output.notes else 'None'}

Review each acceptance criterion and verify the implementation meets it.

Your output MUST be a valid JSON object with these exact fields:
- "verdict": One of "pass", "fail", or "needs-human"
- "findings": Array of issues or observations found
- "suggested_changes": Array of improvement suggestions

Output ONLY the JSON object, no markdown or explanation.""",
        expected_output="JSON object with verdict, findings, and suggested_changes",
        agent=agent,
    )
