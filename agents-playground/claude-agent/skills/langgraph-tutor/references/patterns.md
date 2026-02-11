# LangGraph Patterns Reference

Detailed implementation patterns for common LangGraph use cases.

## ReAct Agent Pattern

The most common pattern: Reasoning and Acting in a loop.

```python
from typing import Annotated, Literal
from typing_extensions import TypedDict
from langchain_anthropic import ChatAnthropic
from langchain_core.tools import tool
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition

# 1. Define State
class State(TypedDict):
    messages: Annotated[list, add_messages]

# 2. Create Tools
@tool
def search(query: str) -> str:
    """Search the web for information."""
    # Replace with actual search implementation
    return f"Search results for: {query}"

@tool
def calculator(expression: str) -> str:
    """Evaluate a math expression."""
    try:
        return str(eval(expression))
    except Exception as e:
        return f"Error: {e}"

tools = [search, calculator]

# 3. Create LLM with tools
llm = ChatAnthropic(model="claude-3-5-sonnet-20241022")
llm_with_tools = llm.bind_tools(tools)

# 4. Define Agent Node
def agent(state: State) -> dict:
    """The agent decides what to do next."""
    response = llm_with_tools.invoke(state["messages"])
    return {"messages": [response]}

# 5. Build Graph
graph = StateGraph(State)

# Add nodes
graph.add_node("agent", agent)
graph.add_node("tools", ToolNode(tools))

# Add edges
graph.add_edge(START, "agent")
graph.add_conditional_edges(
    "agent",
    tools_condition,  # Routes to "tools" if tool_calls exist, else END
)
graph.add_edge("tools", "agent")  # Loop back after tool execution

# 6. Compile
app = graph.compile()

# 7. Run
result = app.invoke({
    "messages": [("user", "What is 25 * 4 and search for Python tutorials")]
})
```

**Flow Diagram:**
```
         ┌──────────────────────┐
         │                      │
         ↓                      │
START → [agent] ──has_tools──→ [tools]
           │
           └──no_tools──→ END
```

## Chatbot with Memory

Persist conversations across sessions:

```python
from langgraph.checkpoint.memory import InMemorySaver

# ... (State and agent definition from above)

# Compile with checkpointer
memory = InMemorySaver()
app = graph.compile(checkpointer=memory)

# Use thread_id for conversation persistence
config = {"configurable": {"thread_id": "session-abc"}}

# First turn
result = app.invoke(
    {"messages": [("user", "My name is Alice")]},
    config
)

# Second turn - remembers the name
result = app.invoke(
    {"messages": [("user", "What's my name?")]},
    config
)
# Response will include "Alice"
```

## Branching Logic

Handle different paths based on content:

```python
def content_router(state: State) -> Literal["technical", "general", "escalate"]:
    """Route based on message content."""
    last_message = state["messages"][-1].content.lower()

    if "error" in last_message or "bug" in last_message:
        return "technical"
    elif "manager" in last_message or "complaint" in last_message:
        return "escalate"
    else:
        return "general"

def technical_support(state: State) -> dict:
    response = tech_llm.invoke(state["messages"])
    return {"messages": [response]}

def general_support(state: State) -> dict:
    response = general_llm.invoke(state["messages"])
    return {"messages": [response]}

def escalate_to_human(state: State) -> dict:
    return {"messages": [AIMessage("Connecting you to a human agent...")]}

# Build graph
graph = StateGraph(State)
graph.add_node("router_node", lambda s: s)  # Pass-through
graph.add_node("technical", technical_support)
graph.add_node("general", general_support)
graph.add_node("escalate", escalate_to_human)

graph.add_edge(START, "router_node")
graph.add_conditional_edges("router_node", content_router)
graph.add_edge("technical", END)
graph.add_edge("general", END)
graph.add_edge("escalate", END)
```

**Flow Diagram:**
```
                    ┌──→ [technical] ──→ END
                    │
START → [router] ──┼──→ [general] ───→ END
                    │
                    └──→ [escalate] ──→ END
```

## Subgraph Composition

Build complex systems from smaller graphs:

```python
# Define a reusable research subgraph
def create_research_graph():
    class ResearchState(TypedDict):
        query: str
        results: list[str]

    def search_node(state):
        results = search_tool.invoke(state["query"])
        return {"results": results}

    def summarize_node(state):
        summary = llm.invoke(f"Summarize: {state['results']}")
        return {"results": [summary.content]}

    graph = StateGraph(ResearchState)
    graph.add_node("search", search_node)
    graph.add_node("summarize", summarize_node)
    graph.add_edge(START, "search")
    graph.add_edge("search", "summarize")
    graph.add_edge("summarize", END)

    return graph.compile()

# Use in parent graph
research_subgraph = create_research_graph()

def research_wrapper(state: State) -> dict:
    """Wrap subgraph for parent graph."""
    result = research_subgraph.invoke({"query": state["query"]})
    return {"research_results": result["results"]}

parent_graph = StateGraph(ParentState)
parent_graph.add_node("research", research_wrapper)
# ... rest of parent graph
```

## Retry with Backoff

Handle transient failures:

```python
import time
from langgraph.types import Command

MAX_RETRIES = 3

class RetryState(TypedDict):
    messages: Annotated[list, add_messages]
    retry_count: int
    error: str | None

def api_call_node(state: RetryState) -> dict | Command:
    try:
        response = external_api.call(state["messages"])
        return {"messages": [response], "error": None, "retry_count": 0}
    except Exception as e:
        if state["retry_count"] < MAX_RETRIES:
            time.sleep(2 ** state["retry_count"])  # Exponential backoff
            return Command(
                goto="api_call",  # Retry same node
                update={"retry_count": state["retry_count"] + 1, "error": str(e)}
            )
        else:
            return {"error": f"Failed after {MAX_RETRIES} retries: {e}"}

def should_continue(state: RetryState) -> Literal["success", "failed"]:
    if state.get("error"):
        return "failed"
    return "success"
```
