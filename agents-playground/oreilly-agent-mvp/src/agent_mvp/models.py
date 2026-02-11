"""
Pydantic models for issue input and pipeline output.

These models define the contracts between components:
- Issue: Input from GitHub or mock files
- PMOutput, DevOutput, QAOutput: Agent outputs
- PipelineResult: Final output written to outgoing/
"""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Literal, Optional, Any
from uuid import uuid4

from pydantic import BaseModel, Field


# =============================================================================
# Token Tracking Models
# =============================================================================


class TokenUsage(BaseModel):
    """Token usage statistics for an LLM call.

    Used to track token consumption and costs for teaching responsible AI usage.
    """
    input_tokens: int = Field(
        description="Number of tokens in the prompt (input)",
        ge=0,
    )
    output_tokens: int = Field(
        description="Number of tokens in the response (output)",
        ge=0,
    )
    total_tokens: int = Field(
        description="Total tokens used (input + output)",
        ge=0,
    )
    model_name: str = Field(
        description="LLM model used (e.g., 'claude-3-5-sonnet-20241022')",
    )
    estimated_cost_usd: Optional[float] = Field(
        default=None,
        description="Estimated cost in USD based on published pricing",
    )


class AgentTokens(BaseModel):
    """Token usage for a specific agent in the pipeline."""
    agent_name: str = Field(
        description="Name of the agent (PM, Dev, QA)",
    )
    usage: TokenUsage = Field(
        description="Token usage statistics for this agent",
    )


class PipelineTokens(BaseModel):
    """Complete token usage for a pipeline run.

    Tracks individual agent usage and provides totals for cost awareness.
    """
    agents: list[AgentTokens] = Field(
        description="Token usage per agent",
        default_factory=list,
    )
    total_input_tokens: int = Field(
        default=0,
        description="Total input tokens across all agents",
    )
    total_output_tokens: int = Field(
        default=0,
        description="Total output tokens across all agents",
    )
    total_tokens: int = Field(
        default=0,
        description="Total tokens used in entire pipeline",
    )
    estimated_total_cost_usd: Optional[float] = Field(
        default=None,
        description="Estimated total cost in USD",
    )
    cost_breakdown: dict[str, float] = Field(
        default_factory=dict,
        description="Cost per agent for detailed analysis",
    )
    efficiency_metrics: dict[str, Any] = Field(
        default_factory=dict,
        description="Additional metrics (tokens/agent, context %, etc.)",
    )


# =============================================================================
# Input Models
# =============================================================================


class IssueSource(str, Enum):
    """Where the issue came from."""
    MOCK = "mock"
    GITHUB_MCP = "github-mcp"
    MANUAL = "manual"


class Issue(BaseModel):
    """A GitHub issue to be processed by the pipeline.

    This is the input contract for the pipeline.
    Issues can come from GitHub MCP, mock files, or manual entry.
    """
    issue_id: str = Field(
        description="Unique identifier in format 'owner/repo#123'",
        examples=["microsoft/vscode#12345"],
    )
    repo: str = Field(
        description="Repository in 'owner/repo' format",
        examples=["microsoft/vscode"],
    )
    issue_number: int = Field(
        description="Issue number within the repository",
        ge=1,
    )
    title: str = Field(
        description="Issue title",
        min_length=1,
    )
    body: str = Field(
        description="Issue body/description (may be empty)",
        default="",
    )
    labels: list[str] = Field(
        description="Labels attached to the issue",
        default_factory=list,
    )
    url: str = Field(
        description="URL to the issue on GitHub",
        examples=["https://github.com/microsoft/vscode/issues/12345"],
    )
    source: IssueSource = Field(
        description="Where this issue came from",
        default=IssueSource.MANUAL,
    )


# =============================================================================
# Agent Output Models
# =============================================================================


class PMOutput(BaseModel):
    """Output from the PM (Product Manager) agent.

    The PM analyzes the issue and produces:
    - A summary of what needs to be done
    - Clear acceptance criteria
    - An implementation plan
    - Any assumptions made
    """
    summary: str = Field(
        description="Brief summary of the issue and what needs to be done",
    )
    acceptance_criteria: list[str] = Field(
        description="List of acceptance criteria for the implementation",
        default_factory=list,
    )
    plan: list[str] = Field(
        description="Ordered list of implementation steps",
        default_factory=list,
    )
    assumptions: list[str] = Field(
        description="Assumptions made during analysis",
        default_factory=list,
    )


class DevFile(BaseModel):
    """A file proposed by the Dev agent."""
    path: str = Field(
        description="Relative file path (e.g., 'src/utils/helper.py')",
    )
    content: str = Field(
        description="Proposed file content",
    )
    language: str = Field(
        description="Programming language (e.g., 'python', 'typescript')",
        default="python",
    )


class DevOutput(BaseModel):
    """Output from the Dev (Developer) agent.

    The Dev implements the PM's plan by:
    - Drafting code files
    - Writing tests
    - Adding implementation notes
    """
    files: list[DevFile] = Field(
        description="Proposed code and test files",
        default_factory=list,
    )
    notes: list[str] = Field(
        description="Implementation notes and considerations",
        default_factory=list,
    )


class QAVerdict(str, Enum):
    """QA review verdict."""
    PASS = "pass"
    FAIL = "fail"
    NEEDS_HUMAN = "needs-human"


class QAOutput(BaseModel):
    """Output from the QA (Quality Assurance) agent.

    The QA reviews the Dev's work and provides:
    - An overall verdict
    - Specific findings and issues
    - Suggested changes
    """
    verdict: QAVerdict = Field(
        description="Overall assessment: pass, fail, or needs-human",
    )
    findings: list[str] = Field(
        description="Specific issues or observations found during review",
        default_factory=list,
    )
    suggested_changes: list[str] = Field(
        description="Suggested improvements or fixes",
        default_factory=list,
    )


# =============================================================================
# Pipeline Result Model
# =============================================================================


class RunMetadata(BaseModel):
    """Metadata about a pipeline run."""
    run_id: str = Field(
        default_factory=lambda: str(uuid4()),
        description="Unique run identifier",
    )
    timestamp_utc: str = Field(
        default_factory=lambda: datetime.utcnow().isoformat() + "Z",
        description="Run timestamp in ISO8601 format",
    )
    source_file: Optional[str] = Field(
        default=None,
        description="Source file path if loaded from file",
    )
    duration_seconds: Optional[float] = Field(
        default=None,
        description="Total pipeline duration in seconds",
    )
    token_usage: Optional[PipelineTokens] = Field(
        default=None,
        description="Token usage statistics for the entire pipeline run",
    )


class PipelineResult(BaseModel):
    """Complete pipeline output written to outgoing/.

    This is the final output contract combining all agent outputs.
    """
    run_id: str = Field(
        description="Unique identifier for this run",
    )
    timestamp_utc: str = Field(
        description="When the pipeline completed (ISO8601)",
    )
    issue: Issue = Field(
        description="The original issue that was processed",
    )
    pm: PMOutput = Field(
        description="PM agent analysis and planning output",
    )
    dev: DevOutput = Field(
        description="Dev agent implementation output",
    )
    qa: QAOutput = Field(
        description="QA agent review output",
    )
    next_steps: list[str] = Field(
        description="Recommended next steps for the human reviewer",
        default_factory=list,
    )
    metadata: Optional[RunMetadata] = Field(
        default=None,
        description="Run metadata including duration and token usage",
    )

    @classmethod
    def create(
        cls,
        issue: Issue,
        pm: PMOutput,
        dev: DevOutput,
        qa: QAOutput,
        metadata: Optional[RunMetadata] = None,
    ) -> PipelineResult:
        """Create a PipelineResult with proper metadata.

        Args:
            issue: The original issue.
            pm: PM agent output.
            dev: Dev agent output.
            qa: QA agent output.
            metadata: Optional run metadata.

        Returns:
            Complete PipelineResult ready for serialization.
        """
        meta = metadata or RunMetadata()

        # Generate next steps based on QA verdict
        next_steps = []
        if qa.verdict == QAVerdict.PASS:
            next_steps = [
                "Review the proposed implementation",
                "Create a feature branch",
                "Apply the generated code",
                "Run full test suite",
                "Submit PR for review",
            ]
        elif qa.verdict == QAVerdict.FAIL:
            next_steps = [
                "Review QA findings",
                "Address suggested changes",
                "Re-run pipeline or manually fix issues",
            ]
        else:  # NEEDS_HUMAN
            next_steps = [
                "Human review required before proceeding",
                "Clarify requirements if needed",
                "Consider breaking into smaller tasks",
            ]

        return cls(
            run_id=meta.run_id,
            timestamp_utc=meta.timestamp_utc,
            issue=issue,
            pm=pm,
            dev=dev,
            qa=qa,
            next_steps=next_steps,
            metadata=meta,
        )
