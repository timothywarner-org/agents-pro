# Pipeline Orchestration Approaches

This folder contains multiple implementations of the same PM → Dev → QA pipeline, demonstrating different orchestration strategies. Use this as a teaching reference for understanding when to use each approach.

## Quick Comparison

| File/Folder | Orchestration | Agent Abstraction | Status |
|-------------|---------------|-------------------|--------|
| `graph.py` | LangGraph | Raw LLM calls | ✅ Primary |
| `crew.py` | CrewAI (single Crew) | CrewAI Agents | 📚 Demo only |
| `crew_variant/` | LangGraph + CrewAI | CrewAI Agents | ✅ Alternative |

---

## Approach 1: Pure LangGraph (`graph.py`)

**The primary implementation.** Each agent is a LangGraph node that makes direct LLM calls.

```
load_issue → pm_node → dev_node → qa_node → finalize → END
                ↓          ↓          ↓
            llm.invoke  llm.invoke  llm.invoke
```

### How It Works

```python
def pm_node(state: PipelineState) -> PipelineState:
    llm = config.get_llm()
    response = llm.invoke([
        {"role": "system", "content": PM_SYSTEM_PROMPT},
        {"role": "user", "content": format_pm_prompt(issue)},
    ])
    return {**state, "pm_output": parse_response(response)}
```

### Pros
- **Full control**: You see exactly what goes to the LLM
- **Debuggable**: Single execution model, predictable flow
- **Lightweight**: No framework overhead
- **Flexible**: Easy to add conditional logic, retries, custom parsing

### Cons
- **More boilerplate**: You write system prompts manually
- **No agent "personality"**: Just prompts, no role/goal/backstory abstraction

### When to Use
- Production pipelines where you need predictability
- When you want fine-grained control over prompts
- Teaching LLM fundamentals without framework magic

---

## Approach 2: Pure CrewAI (`crew.py`)

**Demo/reference only.** Shows how CrewAI would handle the full pipeline internally.

```
issue → Crew.kickoff() → result
           ↓
    [PM Agent] → [Dev Agent] → [QA Agent]
         (CrewAI handles orchestration internally)
```

### How It Works

```python
crew = Crew(
    agents=[pm_agent, dev_agent, qa_agent],
    tasks=[pm_task, dev_task, qa_task],
    process=Process.sequential,
)
result = crew.kickoff()  # One call, CrewAI does the rest
```

### Pros
- **Minimal code**: CrewAI handles task chaining via `context`
- **Agent abstraction**: Role, goal, backstory shape behavior
- **Built-in features**: Retries, caching, delegation (if enabled)

### Cons
- **Black box**: Hard to see what's happening between agents
- **Less control**: CrewAI decides execution details
- **Harder debugging**: Two log systems, opaque state
- **Dynamic tasks are awkward**: Tasks defined upfront, not based on runtime output

### When to Use
- Rapid prototyping
- When agent collaboration/delegation is needed
- When you trust CrewAI's defaults

### Why It's Not Our Primary Approach

The comment in `crew.py` explains:

> "For dynamic task creation based on previous outputs, you'd use callbacks or the hierarchical process. For MVP simplicity, we'll use the LangGraph pipeline instead."

---

## Approach 3: LangGraph + CrewAI Hybrid (`crew_variant/`)

**Best of both worlds.** CrewAI's agent abstractions with LangGraph's explicit control.

```
load_issue → pm_crew → dev_crew → qa_crew → finalize → END
                ↓          ↓          ↓
            Crew #1    Crew #2    Crew #3
           (1 agent)  (1 agent)  (1 agent)
```

### How It Works

Each LangGraph node runs a "mini-Crew" with one agent and one task:

```python
def pm_crew_node(state):
    pm_agent = PMAgent.create(llm)  # Has role, goal, backstory
    pm_task = create_pm_task(issue, pm_agent)

    crew = Crew(
        agents=[pm_agent],
        tasks=[pm_task],
        process=Process.sequential,
    )
    result = crew.kickoff()  # One kickoff per node

    return {**state, "pm_output": parse_result(result)}
```

### Pros
- **Agent abstractions**: Role/goal/backstory without losing control
- **Explicit state**: LangGraph manages what flows between agents
- **Per-node visibility**: See each agent's input/output clearly
- **Flexible flow**: Add conditionals, loops, parallel branches easily

### Cons
- **More overhead**: 3 Crew instances vs 1
- **Two frameworks**: Must understand both LangGraph and CrewAI
- **Verbose**: More setup code than pure CrewAI

### When to Use
- When you want CrewAI's agent modeling but LangGraph's control
- Complex pipelines with conditional branching
- When debugging agent-by-agent is important

---

## Parallel Execution Patterns

For parent → parallel children → join flows, **use pure LangGraph**.

### Why Not CrewAI for Parallelism?

| Concern | LangGraph | CrewAI |
|---------|-----------|--------|
| State sync | Single dict, atomic | Must merge Crew outputs manually |
| Error handling | Per-branch control | Crew fails as unit |
| Debugging | One execution model | Two frameworks |
| Fan-out | Native `Send()` | Manual thread coordination |
| Partial failure | Handle gracefully | Opaque |

### LangGraph Parallel Pattern

```python
from langgraph.graph import Send

def parent_node(state):
    """Fan out to parallel children."""
    return [
        Send("analyzer", {**state, "task": "analyze"}),
        Send("implementer", {**state, "task": "implement"}),
        Send("tester", {**state, "task": "test"}),
    ]

def join_node(state):
    """Receives merged results from all children."""
    # State automatically contains all child outputs
    return {"combined": merge(state)}

# Graph edges
builder.add_edge("analyzer", "join")
builder.add_edge("implementer", "join")
builder.add_edge("tester", "join")
```

### CrewAI Parallel (Less Recommended)

```python
# CrewAI's Process.parallel runs tasks in one Crew
crew = Crew(
    agents=[agent_a, agent_b, agent_c],
    tasks=[task_a, task_b, task_c],
    process=Process.parallel,  # All run at once
)
# Problems:
# - Shared context between all agents
# - One combined output, not per-agent
# - If one fails, all fail
# - No structured fan-in
```

---

## File Structure

```
pipeline/
├── README.md              # This file
├── __init__.py
├── graph.py               # Approach 1: Pure LangGraph (PRIMARY)
├── crew.py                # Approach 2: Pure CrewAI (DEMO)
├── prompts.py             # System prompts for graph.py
└── crew_variant/          # Approach 3: LangGraph + CrewAI
    ├── __init__.py
    ├── agents.py          # CrewAI Agent definitions
    ├── tasks.py           # Task factory functions
    ├── graph.py           # LangGraph with CrewAI nodes
    └── runner.py          # CLI runner
```

---

## Decision Guide

```
Need full control over prompts?
  → Use graph.py (pure LangGraph)

Want agent role/goal/backstory abstraction?
  → Use crew_variant/ (hybrid)

Rapid prototype with minimal code?
  → Use crew.py pattern (pure CrewAI)

Need parallel execution with structured fan-in?
  → Use pure LangGraph with Send()

Agents need to delegate to each other dynamically?
  → Consider pure CrewAI with hierarchical process
```

---

## Running the Pipelines

### Pure LangGraph (Primary)
```bash
python -m agent_mvp.cli run path/to/issue.json
```

### CrewAI Hybrid Variant
```bash
python -m agent_mvp.pipeline.crew_variant.runner path/to/issue.json
```

---

## Further Reading

- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [CrewAI Documentation](https://docs.crewai.com/)
- [LangGraph vs CrewAI comparison](https://blog.langchain.dev/langgraph-multi-agent-workflows/)
