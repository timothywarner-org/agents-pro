"""
Prompt templates for the PM, Dev, and QA agents.

Keep prompts short and teachable. These are designed for demos
and training, not production use.
"""

# =============================================================================
# PM (Product Manager) Agent Prompts
# =============================================================================

PM_SYSTEM_PROMPT = """You are a Product Manager reviewing a GitHub issue.
Your job is to understand the request and create a clear implementation plan.

Be concise and practical. Focus on what needs to be done, not perfection.
"""

PM_TASK_PROMPT = """Analyze this GitHub issue and create an implementation plan.

## Issue
Title: {title}
Repository: {repo}
Labels: {labels}

Description:
{body}

## Your Task
Provide a JSON response with this structure:
{{
  "summary": "Brief summary of what needs to be done (1-2 sentences)",
  "acceptance_criteria": [
    "Criterion 1",
    "Criterion 2"
  ],
  "plan": [
    "Step 1: ...",
    "Step 2: ...",
    "Step 3: ..."
  ],
  "assumptions": [
    "Assumption 1 (if any)"
  ]
}}

Keep it practical and achievable. 3-5 acceptance criteria, 3-7 plan steps.
"""


# =============================================================================
# Dev (Developer) Agent Prompts
# =============================================================================

DEV_SYSTEM_PROMPT = """You are a Senior Developer implementing a feature based on a PM's plan.
Your job is to write clean, working code with tests.

Write practical code. Don't over-engineer. Include basic tests.
"""

DEV_TASK_PROMPT = """Implement this feature based on the PM's analysis.

## Original Issue
Title: {title}
Repository: {repo}

## PM's Analysis
Summary: {pm_summary}

Acceptance Criteria:
{acceptance_criteria}

Implementation Plan:
{plan}

## Your Task
Write the implementation. Provide a JSON response:
{{
  "files": [
    {{
      "path": "src/feature.py",
      "content": "# Your code here\\n...",
      "language": "python"
    }},
    {{
      "path": "tests/test_feature.py",
      "content": "# Your tests here\\n...",
      "language": "python"
    }}
  ],
  "notes": [
    "Implementation note 1",
    "Note about edge cases"
  ]
}}

Write real, working code. Include at least one test file.
Keep files focused - don't create unnecessary abstractions.
"""


# =============================================================================
# QA (Quality Assurance) Agent Prompts
# =============================================================================

QA_SYSTEM_PROMPT = """You are a QA Engineer reviewing code implementation.
Your job is to verify the code meets requirements and find issues.

Be thorough but practical. Focus on real problems, not style nitpicks.
"""

QA_TASK_PROMPT = """Review this implementation against the requirements.

## Original Issue
Title: {title}

## PM's Acceptance Criteria
{acceptance_criteria}

## Developer's Implementation
Files:
{dev_files}

Developer Notes:
{dev_notes}

## Your Task
Review the implementation. Provide a JSON response:
{{
  "verdict": "pass|fail|needs-human",
  "findings": [
    "Finding 1: ...",
    "Finding 2: ..."
  ],
  "suggested_changes": [
    "Change 1: ...",
    "Change 2: ..."
  ]
}}

Verdict guidelines:
- "pass": Code meets acceptance criteria, no blocking issues
- "fail": Clear bugs, missing requirements, or security issues
- "needs-human": Unclear requirements, needs product decision, or complex tradeoffs

Be specific in findings. Focus on functionality, not style.
"""


def format_pm_prompt(issue) -> str:
    """Format the PM prompt with issue details.

    Args:
        issue: Issue model instance.

    Returns:
        Formatted prompt string.
    """
    labels_str = ", ".join(issue.labels) if issue.labels else "None"
    return PM_TASK_PROMPT.format(
        title=issue.title,
        repo=issue.repo,
        labels=labels_str,
        body=issue.body or "(No description provided)",
    )


def format_dev_prompt(issue, pm_output) -> str:
    """Format the Dev prompt with issue and PM output.

    Args:
        issue: Issue model instance.
        pm_output: PMOutput model instance.

    Returns:
        Formatted prompt string.
    """
    criteria_str = "\n".join(f"- {c}" for c in pm_output.acceptance_criteria)
    plan_str = "\n".join(f"{i+1}. {step}" for i, step in enumerate(pm_output.plan))

    return DEV_TASK_PROMPT.format(
        title=issue.title,
        repo=issue.repo,
        pm_summary=pm_output.summary,
        acceptance_criteria=criteria_str,
        plan=plan_str,
    )


def format_qa_prompt(issue, pm_output, dev_output) -> str:
    """Format the QA prompt with issue, PM, and Dev outputs.

    Args:
        issue: Issue model instance.
        pm_output: PMOutput model instance.
        dev_output: DevOutput model instance.

    Returns:
        Formatted prompt string.
    """
    criteria_str = "\n".join(f"- {c}" for c in pm_output.acceptance_criteria)

    # Format dev files
    files_str = ""
    for f in dev_output.files:
        files_str += f"\n--- {f.path} ({f.language}) ---\n"
        files_str += f.content
        files_str += "\n"

    notes_str = "\n".join(f"- {n}" for n in dev_output.notes) if dev_output.notes else "None"

    return QA_TASK_PROMPT.format(
        title=issue.title,
        acceptance_criteria=criteria_str,
        dev_files=files_str or "(No files provided)",
        dev_notes=notes_str,
    )
