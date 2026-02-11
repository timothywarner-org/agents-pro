"""
MCP Server for O'Reilly Agent MVP.

Exposes tools, resources, and prompts for the agent pipeline via Model Context Protocol.
Uses stdio transport for local integration with Claude Desktop and other MCP clients.
"""

import json
from pathlib import Path
from typing import Any

from mcp.server.fastmcp import Context, FastMCP
from mcp.server.session import ServerSession

from ..config import Config
from ..integrations.github_issue_fetcher import fetch_github_issue
from ..issue_sources import FileIssueSource
from ..logging_setup import setup_logging
from ..models import Issue
from ..pipeline.run_once import run_pipeline, save_result
from ..util.reporting import format_run_report

# Initialize FastMCP server
mcp = FastMCP(
    name="oreilly-agent-mvp",
    instructions=(
        "This server provides tools for running the O'Reilly Agent MVP pipeline. "
        "It can fetch issues from GitHub, process mock issues, or run the pipeline directly. "
        "The pipeline uses PM → Dev → QA agents to triage issues and draft implementation plans."
    ),
)

PROJECT_ROOT = Path(__file__).resolve().parents[3]


# ============================================================================
# TOOLS - Actions that can be called by LLM
# ============================================================================


@mcp.tool()
async def fetch_github_issue(
    issue_number: int,
    owner: str = "timothywarner-org",
    repo: str = "agents2",
    save_to_incoming: bool = True,
    ctx: Context[ServerSession, None] = None,
) -> dict[str, Any]:
    """
    Fetch an issue from GitHub and optionally save to incoming directory.

    Args:
        issue_number: GitHub issue number to fetch
        owner: Repository owner (default: timothywarner-org)
        repo: Repository name (default: agents2)
        save_to_incoming: If True, saves JSON to incoming/ directory
        ctx: MCP context for logging

    Returns:
        Dict containing issue data in standardized format
    """
    if ctx:
        await ctx.info(f"Fetching issue #{issue_number} from {owner}/{repo}")

    try:
        issue_data = fetch_github_issue(owner=owner, repo=repo, issue_number=issue_number)

        if save_to_incoming:
            incoming_dir = PROJECT_ROOT / "incoming"
            incoming_dir.mkdir(exist_ok=True)
            issue_file = incoming_dir / f"github_issue_{issue_number}.json"

            with open(issue_file, "w", encoding="utf-8") as f:
                json.dump(issue_data, f, indent=2)

            if ctx:
                await ctx.info(f"Saved issue to {issue_file}")

            return {
                "status": "success",
                "issue": issue_data,
                "saved_to": str(issue_file),
            }

        return {"status": "success", "issue": issue_data}

    except Exception as e:
        if ctx:
            await ctx.error(f"Failed to fetch issue: {e}")
        return {"status": "error", "error": str(e)}


@mcp.tool()
async def list_mock_issues(ctx: Context[ServerSession, None] = None) -> dict[str, Any]:
    """
    List available mock issue files.

    Returns:
        Dict containing list of mock issue filenames and their titles
    """
    if ctx:
        await ctx.debug("Listing mock issues")

    mock_dir = PROJECT_ROOT / "mock_issues"

    if not mock_dir.exists():
        return {"status": "error", "error": "mock_issues/ directory not found"}

    mock_files = sorted(mock_dir.glob("issue_*.json"))

    issues = []
    for file in mock_files:
        try:
            with open(file, "r", encoding="utf-8") as f:
                data = json.load(f)
                issues.append(
                    {
                        "filename": file.name,
                        "title": data.get("title", "Untitled"),
                        "priority": data.get("priority", "unknown"),
                        "path": str(file),
                    }
                )
        except Exception as e:
            if ctx:
                await ctx.warning(f"Could not read {file.name}: {e}")

    return {"status": "success", "mock_issues": issues, "count": len(issues)}


@mcp.tool()
async def load_mock_issue(filename: str, ctx: Context[ServerSession, None] = None) -> dict[str, Any]:
    """
    Load a specific mock issue by filename.

    Args:
        filename: Name of the mock issue file (e.g., 'issue_001.json')
        ctx: MCP context for logging

    Returns:
        Dict containing the loaded issue data
    """
    if ctx:
        await ctx.info(f"Loading mock issue: {filename}")

    mock_dir = PROJECT_ROOT / "mock_issues"
    mock_file = mock_dir / filename

    if not mock_file.exists():
        if ctx:
            await ctx.error(f"Mock issue not found: {filename}")
        return {"status": "error", "error": f"File not found: {filename}"}

    try:
        with open(mock_file, "r", encoding="utf-8") as f:
            issue_data = json.load(f)

        return {"status": "success", "issue": issue_data, "path": str(mock_file)}

    except Exception as e:
        if ctx:
            await ctx.error(f"Failed to load mock issue: {e}")
        return {"status": "error", "error": str(e)}


@mcp.tool()
async def run_agent_pipeline(
    issue_data: dict[str, Any], ctx: Context[ServerSession, None] = None
) -> dict[str, Any]:
    """
    Run the full PM → Dev → QA agent pipeline on an issue.

    Args:
        issue_data: Issue data in standardized format (title, description, priority, etc.)
        ctx: MCP context for progress reporting

    Returns:
        Dict containing pipeline results (PM analysis, Dev plan, QA verdict)
    """
    if ctx:
        await ctx.info("Starting agent pipeline")
        await ctx.report_progress(0.0, 1.0, "Initializing...")

    try:
        # Parse issue from dict
        issue = Issue(**issue_data)

        # Load config
        config = Config.from_env(PROJECT_ROOT)
        setup_logging(level=config.log_level)

        if ctx:
            await ctx.report_progress(0.2, 1.0, "Running PM agent...")

        # Run pipeline
        result = run_pipeline(issue, config)

        if ctx:
            await ctx.report_progress(0.6, 1.0, "Running Dev agent...")
            await ctx.report_progress(0.8, 1.0, "Running QA agent...")

        # Save result (JSON + HTML)
        output_dir = config.outgoing_dir
        output_dir.mkdir(parents=True, exist_ok=True)
        json_path, html_path = save_result(result, output_dir)

        if ctx:
            await ctx.report_progress(1.0, 1.0, "Pipeline complete")
            await ctx.info(f"Results saved to {json_path}")
            await ctx.info(f"HTML report: file://{html_path.resolve()}")

        return {
            "status": "success",
            "run_id": result.run_id,
            "pm_output": result.pm.model_dump(),
            "dev_output": result.dev.model_dump(),
            "qa_output": result.qa.model_dump(),
            "output_file": str(json_path),
            "html_report": str(html_path),
            "html_report_url": f"file://{html_path.resolve()}",
            "token_usage": result.metadata.token_usage.model_dump()
            if result.metadata and result.metadata.token_usage
            else None,
            "report": format_run_report(result, json_path, html_path),
        }

    except Exception as e:
        if ctx:
            await ctx.error(f"Pipeline failed: {e}")
        return {"status": "error", "error": str(e)}


@mcp.tool()
async def process_issue_file(
    file_path: str, ctx: Context[ServerSession, None] = None
) -> dict[str, Any]:
    """
    Process an issue from a JSON file through the pipeline.

    Args:
        file_path: Path to JSON file containing issue data
        ctx: MCP context for logging

    Returns:
        Dict containing pipeline results
    """
    if ctx:
        await ctx.info(f"Processing issue file: {file_path}")

    try:
        issue_file = Path(file_path)
        if not issue_file.exists():
            return {"status": "error", "error": f"File not found: {file_path}"}

        # Load issue
        issue = FileIssueSource.from_path(issue_file)

        # Run pipeline
        config = Config.from_env(PROJECT_ROOT)
        setup_logging(level=config.log_level)

        result = run_pipeline(issue, config, source_file=str(issue_file))

        # Save result (JSON + HTML)
        output_dir = config.outgoing_dir
        output_dir.mkdir(parents=True, exist_ok=True)
        json_path, html_path = save_result(result, output_dir)

        if ctx:
            await ctx.info(f"Pipeline complete. Output: {json_path}")
            await ctx.info(f"HTML report: file://{html_path.resolve()}")

        return {
            "status": "success",
            "run_id": result.run_id,
            "verdict": result.qa.verdict.value,
            "output_file": str(json_path),
            "html_report": str(html_path),
            "html_report_url": f"file://{html_path.resolve()}",
            "token_usage": result.metadata.token_usage.model_dump()
            if result.metadata and result.metadata.token_usage
            else None,
            "report": format_run_report(result, json_path, html_path),
        }

    except Exception as e:
        if ctx:
            await ctx.error(f"Failed to process file: {e}")
        return {"status": "error", "error": str(e)}


# ============================================================================
# RESOURCES - Data exposed to LLM
# ============================================================================


@mcp.resource("config://settings")
def get_config() -> str:
    """
    Expose current application configuration.

    Returns:
        JSON string containing config settings
    """
    config = Config.from_env(PROJECT_ROOT)

    config_data = {
        "llm_provider": config.llm_provider.value,
        "llm_model": config.llm_model,
        "llm_temperature": config.llm_temperature,
        "project_root": str(config.project_root),
        "incoming_dir": str(config.incoming_dir),
        "outgoing_dir": str(config.outgoing_dir),
        "processed_dir": str(config.processed_dir),
        "log_level": config.log_level,
    }

    return json.dumps(config_data, indent=2)


@mcp.resource("issues://mock/{filename}")
def get_mock_issue(filename: str) -> str:
    """
    Get content of a specific mock issue file.

    Args:
        filename: Name of the mock issue file

    Returns:
        JSON string containing issue data
    """
    mock_file = PROJECT_ROOT / "mock_issues" / filename

    if not mock_file.exists():
        return json.dumps({"error": f"Mock issue not found: {filename}"})

    with open(mock_file, "r", encoding="utf-8") as f:
        return f.read()


@mcp.resource("pipeline://schema")
def get_pipeline_schema() -> str:
    """
    Get the data schema for pipeline input/output.

    Returns:
        JSON string containing Pydantic schemas
    """
    from ..models import DevOutput, Issue, PMOutput, PipelineResult, QAOutput

    schemas = {
        "Issue": Issue.model_json_schema(),
        "PMOutput": PMOutput.model_json_schema(),
        "DevOutput": DevOutput.model_json_schema(),
        "QAOutput": QAOutput.model_json_schema(),
        "PipelineResult": PipelineResult.model_json_schema(),
    }

    return json.dumps(schemas, indent=2)


@mcp.resource("pipeline://architecture")
def get_pipeline_architecture() -> str:
    """
    Get architecture documentation for the agent pipeline.

    Returns:
        Markdown string describing pipeline architecture
    """
    return """# O'Reilly Agent MVP Pipeline Architecture

## Overview
The pipeline orchestrates three specialized agents:
1. **PM Agent** - Analyzes issues and assigns priority/difficulty
2. **Dev Agent** - Creates implementation plan with file changes
3. **QA Agent** - Reviews plan and renders verdict (APPROVE/REVISE/REJECT)

## Orchestration
- **LangGraph**: StateGraph with sequential nodes (pm → dev → qa)
- **CrewAI**: Alternative implementation with Agent/Task/Crew pattern

## Data Flow
```
Issue → PM Analysis → Dev Plan → QA Review → PipelineResult
```

## State Management
Each agent receives full state, updates specific fields, returns new state.
State is a TypedDict with: issue, pm_output, dev_output, qa_output.

## LLM Integration
Supports Anthropic Claude, OpenAI GPT-4o, and Azure OpenAI.
Configurable via .env file (LLM_PROVIDER, LLM_MODEL).

## File Structure
- `pipeline/graph.py` - LangGraph orchestration
- `pipeline/crew.py` - CrewAI agents
- `pipeline/prompts.py` - System prompts for each agent
- `models.py` - Pydantic schemas
"""


# ============================================================================
# PROMPTS - Reusable prompt templates
# ============================================================================


@mcp.prompt()
def analyze_github_issue(issue_url: str, focus: str = "general") -> str:
    """
    Generate a prompt for analyzing a GitHub issue.

    Args:
        issue_url: URL of the GitHub issue
        focus: Analysis focus (general, security, performance, architecture)

    Returns:
        Formatted prompt for the LLM
    """
    focus_instructions = {
        "general": "Provide a comprehensive analysis of the issue.",
        "security": "Focus on security implications and potential vulnerabilities.",
        "performance": "Analyze performance impact and optimization opportunities.",
        "architecture": "Evaluate architectural design decisions and patterns.",
    }

    instruction = focus_instructions.get(focus, focus_instructions["general"])

    return f"""Please analyze this GitHub issue: {issue_url}

{instruction}

Consider:
- Technical complexity and implementation difficulty
- Impact on existing codebase
- Required skills and estimated effort
- Potential risks and blockers

Provide your analysis in a structured format."""


@mcp.prompt()
def review_implementation_plan(
    issue_title: str, implementation_plan: str, criteria: str = "standard"
) -> str:
    """
    Generate a prompt for reviewing an implementation plan.

    Args:
        issue_title: Title of the issue being implemented
        implementation_plan: The dev team's implementation plan
        criteria: Review criteria (standard, strict, lenient)

    Returns:
        Formatted prompt for QA review
    """
    criteria_instructions = {
        "standard": "Apply normal QA standards for approval.",
        "strict": "Apply rigorous QA standards - only approve if plan is exceptionally thorough.",
        "lenient": "Apply flexible QA standards - approve if plan is reasonable.",
    }

    criteria_text = criteria_instructions.get(criteria, criteria_instructions["standard"])

    return f"""Issue: {issue_title}

Implementation Plan:
{implementation_plan}

Review Instructions:
{criteria_text}

Evaluate:
1. Completeness - Does the plan address all requirements?
2. Clarity - Is the plan clear and actionable?
3. Feasibility - Is the plan realistic and achievable?
4. Quality - Does the plan follow best practices?

Provide your verdict: APPROVE, REVISE, or REJECT with detailed reasoning."""


@mcp.prompt()
def generate_test_issue(
    issue_type: str = "bug", complexity: str = "medium", domain: str = "web"
) -> str:
    """
    Generate a prompt for creating a test issue.

    Args:
        issue_type: Type of issue (bug, feature, enhancement, refactor)
        complexity: Complexity level (simple, medium, complex)
        domain: Technical domain (web, api, database, infrastructure)

    Returns:
        Prompt for generating a test issue
    """
    return f"""Please create a realistic GitHub issue for testing purposes.

Requirements:
- Type: {issue_type}
- Complexity: {complexity}
- Domain: {domain}

The issue should include:
- Clear, descriptive title
- Detailed description of the problem or feature
- Steps to reproduce (for bugs) or acceptance criteria (for features)
- Technical context and constraints
- Expected outcome

Format the output as JSON matching this schema:
{{
  "title": "Issue title",
  "description": "Detailed description",
  "priority": "low|medium|high|critical",
  "labels": ["label1", "label2"]
}}"""


# ============================================================================
# SERVER ENTRY POINT
# ============================================================================


def main() -> None:
    """Run the MCP server with stdio transport."""
    # Run server with default stdio transport for local integration
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
