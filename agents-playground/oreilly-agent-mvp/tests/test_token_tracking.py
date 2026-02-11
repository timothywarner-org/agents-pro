"""
Test token tracking functionality.

Validates that token usage is captured, aggregated, and reported correctly.
"""

import pytest
from agent_mvp.models import TokenUsage, AgentTokens, PipelineTokens
from agent_mvp.util.token_tracking import (
    calculate_cost,
    aggregate_pipeline_tokens,
    format_token_summary,
)


def test_calculate_cost_claude_sonnet():
    """Test cost calculation for Claude 3.5 Sonnet."""
    cost = calculate_cost(
        input_tokens=10_000,
        output_tokens=5_000,
        model_name="claude-3-5-sonnet-20241022",
    )

    # 10k * $3/1M = $0.03, 5k * $15/1M = $0.075, total = $0.105
    assert cost == pytest.approx(0.105, abs=0.001)


def test_calculate_cost_gpt4o():
    """Test cost calculation for GPT-4o."""
    cost = calculate_cost(
        input_tokens=10_000,
        output_tokens=5_000,
        model_name="gpt-4o",
    )

    # 10k * $2.50/1M = $0.025, 5k * $10/1M = $0.05, total = $0.075
    assert cost == pytest.approx(0.075, abs=0.001)


def test_calculate_cost_unknown_model():
    """Test cost calculation for unknown model uses default pricing."""
    cost = calculate_cost(
        input_tokens=10_000,
        output_tokens=5_000,
        model_name="unknown-model-xyz",
    )

    # Should use default mid-range pricing ($3/1M in, $15/1M out)
    assert cost == pytest.approx(0.105, abs=0.001)


def test_aggregate_pipeline_tokens():
    """Test aggregation of token usage across agents."""
    pm_usage = TokenUsage(
        input_tokens=1000,
        output_tokens=2000,
        total_tokens=3000,
        model_name="claude-3-5-sonnet-20241022",
        estimated_cost_usd=0.0375,
    )

    dev_usage = TokenUsage(
        input_tokens=1500,
        output_tokens=3000,
        total_tokens=4500,
        model_name="claude-3-5-sonnet-20241022",
        estimated_cost_usd=0.0495,
    )

    qa_usage = TokenUsage(
        input_tokens=800,
        output_tokens=1200,
        total_tokens=2000,
        model_name="claude-3-5-sonnet-20241022",
        estimated_cost_usd=0.0204,
    )

    agent_tokens = [
        AgentTokens(agent_name="PM", usage=pm_usage),
        AgentTokens(agent_name="Dev", usage=dev_usage),
        AgentTokens(agent_name="QA", usage=qa_usage),
    ]

    pipeline = aggregate_pipeline_tokens(agent_tokens)

    assert pipeline.total_input_tokens == 3300
    assert pipeline.total_output_tokens == 6200
    assert pipeline.total_tokens == 9500
    assert pipeline.estimated_total_cost_usd == pytest.approx(0.1074, abs=0.001)

    assert pipeline.cost_breakdown["PM"] == pytest.approx(0.0375, abs=0.001)
    assert pipeline.cost_breakdown["Dev"] == pytest.approx(0.0495, abs=0.001)
    assert pipeline.cost_breakdown["QA"] == pytest.approx(0.0204, abs=0.001)

    assert pipeline.efficiency_metrics["total_agents"] == 3
    assert pipeline.efficiency_metrics["average_tokens_per_agent"] == pytest.approx(3166.67, abs=1)
    assert pipeline.efficiency_metrics["max_agent_tokens"] == 4500
    assert pipeline.efficiency_metrics["cost_per_agent_avg"] == pytest.approx(0.0358, abs=0.001)

    assert pipeline.efficiency_metrics["input_output_ratio"] == pytest.approx(0.532, abs=0.01)


def test_format_token_summary():
    """Test that token summary formats without errors."""
    pm_usage = TokenUsage(
        input_tokens=1000,
        output_tokens=2000,
        total_tokens=3000,
        model_name="claude-3-5-sonnet-20241022",
        estimated_cost_usd=0.0375,
    )

    agent_tokens = [AgentTokens(agent_name="PM", usage=pm_usage)]
    pipeline = aggregate_pipeline_tokens(agent_tokens)

    summary = format_token_summary(pipeline)

    assert "TOKEN USAGE SUMMARY" in summary
    assert "PM:" in summary
    assert "1,000" in summary
    assert "2,000" in summary
    assert "3,000" in summary
    assert "$0.037500" in summary
    assert "TOTAL:" in summary
    assert "Avg tokens/agent" in summary


def test_token_usage_model():
    """Test TokenUsage model validation."""
    usage = TokenUsage(
        input_tokens=1234,
        output_tokens=5678,
        total_tokens=6912,
        model_name="test-model",
        estimated_cost_usd=0.042,
    )

    assert usage.input_tokens == 1234
    assert usage.output_tokens == 5678
    assert usage.total_tokens == 6912
    assert usage.model_name == "test-model"
    assert usage.estimated_cost_usd == 0.042


def test_agent_tokens_model():
    """Test AgentTokens model."""
    usage = TokenUsage(
        input_tokens=1000,
        output_tokens=2000,
        total_tokens=3000,
        model_name="test-model",
    )

    agent = AgentTokens(agent_name="TestAgent", usage=usage)

    assert agent.agent_name == "TestAgent"
    assert agent.usage.input_tokens == 1000


def test_pipeline_tokens_serialization():
    """Test that PipelineTokens can be serialized to JSON."""
    usage = TokenUsage(
        input_tokens=1000,
        output_tokens=2000,
        total_tokens=3000,
        model_name="test-model",
        estimated_cost_usd=0.05,
    )

    agent_tokens = [AgentTokens(agent_name="Test", usage=usage)]
    pipeline = aggregate_pipeline_tokens(agent_tokens)

    data = pipeline.model_dump()

    assert data["total_input_tokens"] == 1000
    assert data["total_output_tokens"] == 2000
    assert data["total_tokens"] == 3000
    assert "efficiency_metrics" in data
    assert "cost_breakdown" in data


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
