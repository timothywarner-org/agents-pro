# Token Tracking & Cost Awareness

## Overview

This pipeline includes comprehensive **token tracking** to teach responsible AI agent development. Every LLM call is monitored for token usage and estimated cost.

## Why Track Tokens?

**Teaching Objectives:**
1. **Cost Awareness** - Students see the real cost of each agent interaction
2. **Context Management** - Understand how much of the context window is being used
3. **Efficiency** - Learn to optimize prompts for token conservation
4. **Production Readiness** - Build habits for monitoring in real systems

## What's Tracked

### Per-Agent Metrics
For each agent (PM, Dev, QA):
- **Input tokens** - Tokens in the prompt/system message
- **Output tokens** - Tokens in the LLM response
- **Total tokens** - Sum of input + output
- **Model name** - LLM used (e.g., `claude-3-5-sonnet-20241022`)
- **Estimated cost** - USD cost based on published pricing

### Pipeline-Wide Metrics
- **Total tokens across all agents**
- **Total estimated cost**
- **Cost breakdown per agent**
- **Efficiency metrics:**
  - Average tokens per agent
  - Max tokens used by any agent
  - Context window utilization %
  - Input/output ratio (prompt efficiency)

## Output Format

### Console Summary
After each pipeline run, you'll see:

```
============================================================
📊 TOKEN USAGE SUMMARY
============================================================
    PM:   1,234 in +  2,456 out =   3,690 total ($0.009270)
   Dev:   2,345 in +  4,567 out =   6,912 total ($0.017355)
    QA:   1,890 in +  1,234 out =   3,124 total ($0.007935)
------------------------------------------------------------
TOTAL:   5,469 in +  8,257 out =  13,726 total
COST:    $0.034560
============================================================
Avg tokens/agent: 4,575
Max agent tokens: 6,912
Context usage:    3.46%
Input/Output:     0.662
============================================================
```

### JSON Output (in `outgoing/`)
Each result file includes a `metadata.token_usage` section:

```json
{
  "run_id": "abc-123",
  "timestamp_utc": "2026-01-10T12:34:56Z",
  "issue": { ... },
  "pm": { ... },
  "dev": { ... },
  "qa": { ... },
  "metadata": {
    "run_id": "abc-123",
    "timestamp_utc": "2026-01-10T12:34:56Z",
    "duration_seconds": 45.23,
    "token_usage": {
      "agents": [
        {
          "agent_name": "PM",
          "usage": {
            "input_tokens": 1234,
            "output_tokens": 2456,
            "total_tokens": 3690,
            "model_name": "claude-3-5-sonnet-20241022",
            "estimated_cost_usd": 0.009270
          }
        },
        {
          "agent_name": "Dev",
          "usage": {
            "input_tokens": 2345,
            "output_tokens": 4567,
            "total_tokens": 6912,
            "model_name": "claude-3-5-sonnet-20241022",
            "estimated_cost_usd": 0.017355
          }
        },
        {
          "agent_name": "QA",
          "usage": {
            "input_tokens": 1890,
            "output_tokens": 1234,
            "total_tokens": 3124,
            "model_name": "claude-3-5-sonnet-20241022",
            "estimated_cost_usd": 0.007935
          }
        }
      ],
      "total_input_tokens": 5469,
      "total_output_tokens": 8257,
      "total_tokens": 13726,
      "estimated_total_cost_usd": 0.034560,
      "cost_breakdown": {
        "PM": 0.009270,
        "Dev": 0.017355,
        "QA": 0.007935
      },
      "efficiency_metrics": {
        "average_tokens_per_agent": 4575.33,
        "max_agent_tokens": 6912,
        "estimated_context_window_usage_percent": 3.46,
        "input_output_ratio": 0.662,
        "total_agents": 3,
        "cost_per_agent_avg": 0.011520
      }
    }
  }
}
```

## Pricing

Pricing is based on published rates (as of January 2025) for common models:

### Anthropic Claude
| Model | Input (per 1M tokens) | Output (per 1M tokens) |
|-------|----------------------|------------------------|
| Claude 3.5 Sonnet | $3.00 | $15.00 |
| Claude 3 Opus | $15.00 | $75.00 |
| Claude 3 Haiku | $0.25 | $1.25 |

### OpenAI GPT
| Model | Input (per 1M tokens) | Output (per 1M tokens) |
|-------|----------------------|------------------------|
| GPT-4o | $2.50 | $10.00 |
| GPT-4o Mini | $0.15 | $0.60 |
| GPT-4 Turbo | $10.00 | $30.00 |
| GPT-3.5 Turbo | $0.50 | $1.50 |

**Note:** Costs are estimates. Actual pricing may vary by region and agreement. Always check provider documentation.

## Teaching Moments

### 1. Prompt Engineering Impact
Show students how prompt length affects cost:
- **Verbose prompts** → Higher input tokens → Higher cost
- **Concise prompts** → Lower input tokens → Lower cost
- **Example:** Reducing a 2000-token prompt to 1000 tokens saves ~$0.003 per call

### 2. Context Window Economics
Demonstrate the trade-off:
- **Large context** → More background info → Better responses → Higher cost
- **Small context** → Less background → May need clarification → Lower cost per call
- **Sweet spot:** Find the minimum context for acceptable results

### 3. Output Length Control
Show how output limits affect cost:
- Output tokens are typically **5x more expensive** than input (Claude Sonnet)
- Setting `max_tokens` can prevent runaway costs
- **Example:** Capping output at 2000 tokens vs 4000 saves ~$0.030 per call

### 4. Multi-Agent Economics
Analyze the cost structure:
- **Sequential agents:** Each adds to the total cost
- **Parallel agents:** Same context, multiple calls → context duplication
- **Optimization:** Can we merge agents or share context?

### 5. Production Cost Estimation
Calculate monthly costs:
- **Example:** 1000 issues/month × $0.035/issue = **$35/month**
- Scale factors: 10,000 issues/month = **$350/month**
- Budget planning: Set alerts, optimize high-cost agents

## Implementation Details

### Token Extraction
Uses LangChain's standard `usage_metadata` attribute:

```python
response = llm.invoke(messages)
usage = response.usage_metadata
# Returns: {'input_tokens': 1234, 'output_tokens': 2456, 'total_tokens': 3690}
```

### Cost Calculation
```python
# Per 1M tokens pricing
input_cost = (input_tokens / 1_000_000) * input_price_per_million
output_cost = (output_tokens / 1_000_000) * output_price_per_million
total_cost = input_cost + output_cost
```

### Aggregation
Tokens are tracked in the LangGraph state and aggregated in the `finalize_node`:

```python
# State flows through: PM → Dev → QA → Finalize
state["token_usages"] = [
    {"agent_name": "PM", "usage": {...}},
    {"agent_name": "Dev", "usage": {...}},
    {"agent_name": "QA", "usage": {...}},
]

# Finalize aggregates into PipelineTokens
pipeline_tokens = aggregate_pipeline_tokens(agent_tokens_list)
metadata.token_usage = pipeline_tokens
```

## Code Tour

### Models
- **`models.py`** - `TokenUsage`, `AgentTokens`, `PipelineTokens` classes
- **`models.py`** - `RunMetadata.token_usage` field
- **`models.py`** - `PipelineResult.metadata` includes token data

### Token Tracking
- **`util/token_tracking.py`** - Core tracking logic
  - `extract_token_usage()` - Get tokens from LLM response
  - `calculate_cost()` - USD cost from token counts
  - `aggregate_pipeline_tokens()` - Sum across agents
  - `format_token_summary()` - Console output
  - `PRICING` - Per-model pricing table

### Pipeline Integration
- **`pipeline/graph.py`** - Each node (PM, Dev, QA) tracks tokens
  - Calls `extract_token_usage()` after LLM invoke
  - Stores `AgentTokens` in state
  - Logs tokens per agent
- **`pipeline/graph.py`** - `finalize_node()` aggregates and displays summary

## Extending

### Add New Models
Update `PRICING` in `util/token_tracking.py`:

```python
PRICING = {
    "your-new-model": {"input": 2.50, "output": 10.00},
    # ... existing models
}
```

### Add Metrics
Extend `efficiency_metrics` in `aggregate_pipeline_tokens()`:

```python
efficiency_metrics = {
    # ... existing metrics
    "your_custom_metric": calculate_your_metric(),
}
```

### Custom Alerts
Add cost threshold alerts in `finalize_node()`:

```python
if pipeline_tokens.estimated_total_cost_usd > 0.10:
    logger.warning(f"High cost run: ${pipeline_tokens.estimated_total_cost_usd:.4f}")
```

## References

- [Anthropic Pricing](https://www.anthropic.com/pricing)
- [OpenAI Pricing](https://openai.com/pricing)
- [LangChain Usage Metadata](https://python.langchain.com/docs/concepts/chat_models#usage-metadata)
- [Azure OpenAI Pricing](https://azure.microsoft.com/en-us/pricing/details/cognitive-services/openai-service/)

---

**Teaching Tip:** After each pipeline run, ask students:
1. Which agent used the most tokens? Why?
2. How could we reduce the cost by 50%?
3. What's the input/output ratio telling us?
4. Is the context usage efficient?
