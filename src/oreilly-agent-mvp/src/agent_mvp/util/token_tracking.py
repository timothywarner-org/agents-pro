"""
Token tracking utilities for teaching cost-aware AI agent development.

Provides helpers to extract token usage from LLM responses and calculate costs.
"""

from __future__ import annotations

from typing import Any, Optional

from ..models import TokenUsage, PipelineTokens, AgentTokens


# Pricing per 1M tokens (as of January 2025)
# Source: Provider pricing pages
# NOTE: More specific models must come BEFORE generic ones for lookup matching
PRICING = {
    # DeepSeek (OpenAI-compatible API)
    "deepseek-chat": {"input": 0.14, "output": 0.28},
    "deepseek-coder": {"input": 0.14, "output": 0.28},
    "deepseek-reasoner": {"input": 0.55, "output": 2.19},

    # Anthropic Claude
    "claude-3-5-sonnet-20241022": {"input": 3.00, "output": 15.00},
    "claude-3-5-sonnet-20240620": {"input": 3.00, "output": 15.00},
    "claude-3-opus-20240229": {"input": 15.00, "output": 75.00},
    "claude-3-sonnet-20240229": {"input": 3.00, "output": 15.00},
    "claude-3-haiku-20240307": {"input": 0.25, "output": 1.25},

    # OpenAI GPT-4o (must come before GPT-4)
    "gpt-4o-mini": {"input": 0.15, "output": 0.60},
    "gpt-4o": {"input": 2.50, "output": 10.00},

    # OpenAI GPT-4
    "gpt-4-turbo": {"input": 10.00, "output": 30.00},
    "gpt-4-turbo-preview": {"input": 10.00, "output": 30.00},
    "gpt-4-32k": {"input": 60.00, "output": 120.00},
    "gpt-4": {"input": 30.00, "output": 60.00},

    # OpenAI GPT-3.5
    "gpt-3.5-turbo-16k": {"input": 3.00, "output": 4.00},
    "gpt-3.5-turbo": {"input": 0.50, "output": 1.50},
}


def extract_token_usage(
    response: Any,
    model_name: str,
) -> Optional[TokenUsage]:
    """Extract token usage from an LLM response.

    Supports LangChain response objects with usage_metadata.

    Args:
        response: LLM response object (LangChain format).
        model_name: Model identifier for cost calculation.

    Returns:
        TokenUsage object with stats and cost estimate, or None if unavailable.
    """
    # Try to get usage_metadata (LangChain standard)
    usage = getattr(response, "usage_metadata", None)
    if not usage:
        # Try response_metadata (some providers)
        response_meta = getattr(response, "response_metadata", {})
        usage = response_meta.get("usage") or response_meta.get("token_usage")

    if not usage:
        return None

    # Extract token counts (handle different formats)
    input_tokens = (
        usage.get("input_tokens") or
        usage.get("prompt_tokens") or
        getattr(usage, "input_tokens", 0)
    )
    output_tokens = (
        usage.get("output_tokens") or
        usage.get("completion_tokens") or
        getattr(usage, "output_tokens", 0)
    )
    total_tokens = (
        usage.get("total_tokens") or
        getattr(usage, "total_tokens", input_tokens + output_tokens)
    )

    # Calculate cost
    cost = calculate_cost(input_tokens, output_tokens, model_name)

    return TokenUsage(
        input_tokens=input_tokens,
        output_tokens=output_tokens,
        total_tokens=total_tokens,
        model_name=model_name,
        estimated_cost_usd=cost,
    )


def calculate_cost(
    input_tokens: int,
    output_tokens: int,
    model_name: str,
) -> float:
    """Calculate estimated cost in USD based on token usage.

    Args:
        input_tokens: Number of input/prompt tokens.
        output_tokens: Number of output/completion tokens.
        model_name: Model identifier.

    Returns:
        Estimated cost in USD.
    """
    # Find pricing (handle model variants)
    pricing = None
    for key in PRICING:
        if key in model_name.lower():
            pricing = PRICING[key]
            break

    if not pricing:
        # Default to mid-range pricing if unknown
        pricing = {"input": 3.00, "output": 15.00}

    # Calculate (pricing is per 1M tokens)
    input_cost = (input_tokens / 1_000_000) * pricing["input"]
    output_cost = (output_tokens / 1_000_000) * pricing["output"]

    return round(input_cost + output_cost, 6)


def aggregate_pipeline_tokens(
    agent_usages: list[AgentTokens],
) -> PipelineTokens:
    """Aggregate token usage from all agents with efficiency metrics.

    Args:
        agent_usages: List of per-agent token usage.

    Returns:
        PipelineTokens with totals, costs, and teaching metrics.
    """
    total_input = sum(a.usage.input_tokens for a in agent_usages)
    total_output = sum(a.usage.output_tokens for a in agent_usages)
    total = sum(a.usage.total_tokens for a in agent_usages)
    total_cost = sum(a.usage.estimated_cost_usd or 0 for a in agent_usages)

    # Cost breakdown per agent
    cost_breakdown = {
        a.agent_name: a.usage.estimated_cost_usd or 0
        for a in agent_usages
    }

    # Calculate teaching metrics
    avg_tokens_per_agent = total / len(agent_usages) if agent_usages else 0

    # Context window estimation (assuming ~200k token models like Claude Sonnet)
    typical_context_window = 200_000
    max_tokens_used = max(
        (a.usage.total_tokens for a in agent_usages),
        default=0,
    )
    context_percentage = (max_tokens_used / typical_context_window) * 100

    # Input/output ratio (shows prompt efficiency)
    io_ratio = total_input / total_output if total_output > 0 else 0

    efficiency_metrics = {
        "average_tokens_per_agent": round(avg_tokens_per_agent, 2),
        "max_agent_tokens": max_tokens_used,
        "estimated_context_window_usage_percent": round(context_percentage, 2),
        "input_output_ratio": round(io_ratio, 3),
        "total_agents": len(agent_usages),
        "cost_per_agent_avg": round(total_cost / len(agent_usages), 6) if agent_usages else 0,
    }

    return PipelineTokens(
        agents=agent_usages,
        total_input_tokens=total_input,
        total_output_tokens=total_output,
        total_tokens=total,
        estimated_total_cost_usd=round(total_cost, 6) if total_cost else None,
        cost_breakdown=cost_breakdown,
        efficiency_metrics=efficiency_metrics,
    )


def format_token_summary(tokens: PipelineTokens) -> str:
    """Format token usage as a human-readable summary for logging.

    Args:
        tokens: Pipeline token statistics.

    Returns:
        Formatted string for console output.
    """
    lines = [
        "=" * 60,
        "📊 TOKEN USAGE SUMMARY",
        "=" * 60,
    ]

    # Per-agent breakdown
    for agent in tokens.agents:
        cost_str = f"${agent.usage.estimated_cost_usd:.6f}" if agent.usage.estimated_cost_usd else "N/A"
        lines.append(
            f"{agent.agent_name:>6}: {agent.usage.input_tokens:>6,} in + "
            f"{agent.usage.output_tokens:>6,} out = {agent.usage.total_tokens:>7,} total "
            f"({cost_str})"
        )

    lines.append("-" * 60)

    # Totals
    cost_str = f"${tokens.estimated_total_cost_usd:.6f}" if tokens.estimated_total_cost_usd else "N/A"
    lines.extend([
        f"TOTAL:  {tokens.total_input_tokens:>6,} in + "
        f"{tokens.total_output_tokens:>6,} out = {tokens.total_tokens:>7,} total",
        f"COST:   {cost_str}",
    ])

    lines.append("=" * 60)

    # Efficiency metrics
    metrics = tokens.efficiency_metrics
    lines.extend([
        f"Avg tokens/agent: {metrics.get('average_tokens_per_agent', 0):,.0f}",
        f"Max agent tokens: {metrics.get('max_agent_tokens', 0):,}",
        f"Context usage:    {metrics.get('estimated_context_window_usage_percent', 0):.2f}%",
        f"Input/Output:     {metrics.get('input_output_ratio', 0):.3f}",
        "=" * 60,
    ])

    return "\n".join(lines)
