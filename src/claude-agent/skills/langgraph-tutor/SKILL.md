---
name: langgraph-tutor
description: >
  Expert skill for teaching LangGraph - the orchestration framework for stateful
  AI agents. Covers StateGraph, nodes, edges, conditional routing, checkpointing,
  human-in-the-loop, and multi-agent patterns. Invoke when users ask about
  LangGraph, building agent graphs, state machines for LLMs, or workflow
  orchestration. Keywords: langgraph, state graph, agent workflow, orchestration,
  multi-agent, checkpointing, human-in-the-loop.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash(python:*), Bash(pip:*)
---

# LangGraph Tutor Skill

Expert guidance for building production AI agents with LangGraph.

## Quick Start

```python
from langgraph.graph import StateGraph, START, END
from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph.message import add_messages

class State(TypedDict):
    messages: Annotated[list, add_messages]

def chatbot(state: State):
    return {"messages": [llm.invoke(state["messages"])]}

graph = StateGraph(State)
graph.add_node("chatbot", chatbot)
graph.add_edge(START, "chatbot")
graph.add_edge("chatbot", END)
app = graph.compile()
```

## Core Concepts

### 1. State Definition

State flows through the graph. Use TypedDict with optional reducers:

```python
class State(TypedDict):
    messages: Annotated[list, add_messages]  # Accumulates
    context: str                              # Overwrites
    count: Annotated[int, operator.add]       # Sums
```

### 2. Nodes

Functions that receive state and return updates:

```python
def my_node(state: State) -> dict:
    # Read from state
    messages = state["messages"]
    # Return updates (don't mutate!)
    return {"context": "new value"}
```

### 3. Edges

Connect nodes in the graph:

```python
graph.add_edge(START, "node_a")      # Entry point
graph.add_edge("node_a", "node_b")   # Linear flow
graph.add_edge("node_b", END)        # Exit point
```

### 4. Conditional Routing

Route based on state:

```python
def router(state: State) -> Literal["path_a", "path_b"]:
    if condition:
        return "path_a"
    return "path_b"

graph.add_conditional_edges("source", router)
```

### 5. Memory/Checkpointing

Persist state across invocations:

```python
from langgraph.checkpoint.memory import InMemorySaver

memory = InMemorySaver()
app = graph.compile(checkpointer=memory)

config = {"configurable": {"thread_id": "user-123"}}
result = app.invoke({"messages": [msg]}, config)
```

### 6. Human-in-the-Loop

Pause for human input:

```python
from langgraph.types import interrupt

def approval_node(state):
    response = interrupt({"question": "Approve?"})
    return {"approved": response["answer"]}
```

## Common Patterns

### ReAct Agent (Reasoning + Acting)

See [references/patterns.md](references/patterns.md) for full implementation.

### Supervisor Multi-Agent

See [references/multi-agent.md](references/multi-agent.md) for patterns.

### Tool Calling

See [references/tools.md](references/tools.md) for integration.

## Validation

Run the validation script to check your graph:

```bash
python scripts/validate_graph.py your_graph.py
```

## Examples

Working examples in [examples/](examples/):

- `simple_chatbot.py` - Minimal chatbot
- `tool_agent.py` - Agent with tools
- `multi_agent.py` - Supervisor pattern

## Common Errors

| Error | Cause | Fix |
| --- | --- | --- |
| "Node has no outgoing edge" | Missing edge | Add edge to END or next node |
| "State key not found" | Accessing undefined key | Check State TypedDict |
| "Cannot serialize" | Complex objects in state | Use JSON-serializable types |

## Resources

- [LangGraph Docs](https://langchain-ai.github.io/langgraph/)
- [Tutorials](https://langchain-ai.github.io/langgraph/tutorials/)
- [API Reference](https://langchain-ai.github.io/langgraph/reference/)
