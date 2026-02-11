"""Run reporting utilities for pipeline output."""

from __future__ import annotations

from pathlib import Path
from typing import Optional

from ..models import PipelineResult


def format_run_report(
    result: PipelineResult,
    output_path: Optional[Path] = None,
    html_path: Optional[Path] = None,
) -> str:
    """Format a run report with status and token usage."""
    lines: list[str] = [
        "=" * 60,
        "PIPELINE RUN REPORT",
        "=" * 60,
        f"Run ID:  {result.run_id}",
        f"Issue:   {result.issue.issue_id}",
        f"Title:   {result.issue.title}",
        f"Verdict: {result.qa.verdict.value}",
        f"PM:      {len(result.pm.acceptance_criteria)} criteria, {len(result.pm.plan)} steps",
        f"Dev:     {len(result.dev.files)} files",
        f"QA:      {len(result.qa.findings)} findings",
    ]

    if output_path:
        lines.append(f"Output:  {output_path}")

    if html_path:
        lines.append(f"Report:  file://{html_path.resolve()}")

    if result.metadata and result.metadata.duration_seconds is not None:
        lines.append(f"Time:    {result.metadata.duration_seconds:.2f}s")

    lines.append("-" * 60)

    tokens = result.metadata.token_usage if result.metadata else None
    if not tokens:
        lines.append("Token usage: unavailable (provider did not return usage metadata)")
        lines.append("=" * 60)
        return "\n".join(lines)

    lines.append("Token usage:")
    for agent in tokens.agents:
        cost = agent.usage.estimated_cost_usd
        cost_str = f"${cost:.6f}" if cost is not None else "N/A"
        lines.append(
            f"  {agent.agent_name:>6}: {agent.usage.input_tokens:>6,} in + "
            f"{agent.usage.output_tokens:>6,} out = {agent.usage.total_tokens:>7,} total "
            f"({cost_str})"
        )

    total_cost = tokens.estimated_total_cost_usd
    total_cost_str = f"${total_cost:.6f}" if total_cost is not None else "N/A"
    lines.extend([
        "  " + "-" * 54,
        f"  TOTAL: {tokens.total_input_tokens:>6,} in + {tokens.total_output_tokens:>6,} out = "
        f"{tokens.total_tokens:>7,} total",
        f"  COST:  {total_cost_str}",
    ])

    metrics = tokens.efficiency_metrics or {}
    lines.extend([
        "  " + "-" * 54,
        f"  Avg tokens/agent: {metrics.get('average_tokens_per_agent', 0):,.0f}",
        f"  Max agent tokens: {metrics.get('max_agent_tokens', 0):,}",
        f"  Context usage:    {metrics.get('estimated_context_window_usage_percent', 0):.2f}%",
        f"  Input/Output:     {metrics.get('input_output_ratio', 0):.3f}",
    ])

    lines.append("=" * 60)
    return "\n".join(lines)
