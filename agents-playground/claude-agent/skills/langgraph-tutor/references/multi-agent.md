# Multi-Agent Patterns in LangGraph

Patterns for coordinating multiple specialized agents.

## Supervisor Pattern

A central coordinator routes work to specialist agents:

```python
from typing import Annotated, Literal
from typing_extensions import TypedDict
from langchain_anthropic import ChatAnthropic
from langgraph.graph import StateGraph, MessagesState, START, END
from langgraph.types import Command

llm = ChatAnthropic(model="claude-3-5-sonnet-20241022")

# Supervisor decides which agent to call
def supervisor(state: MessagesState) -> Command[Literal["researcher", "writer", "reviewer", END]]:
    """Route to the appropriate specialist."""

    system_prompt = """You are a supervisor coordinating a team:
    - researcher: Gathers information and data
    - writer: Creates content and documentation
    - reviewer: Reviews and improves content

    Based on the conversation, decide who should act next.
    If the task is complete, respond with "__end__".
    """

    response = llm.with_structured_output({
        "type": "object",
        "properties": {"next": {"enum": ["researcher", "writer", "reviewer", "__end__"]}},
        "required": ["next"]
    }).invoke([
        {"role": "system", "content": system_prompt},
        *state["messages"]
    ])

    goto = response["next"]
    if goto == "__end__":
        return Command(goto=END)
    return Command(goto=goto)

# Specialist agents
def researcher(state: MessagesState) -> Command[Literal["supervisor"]]:
    """Research agent gathers information."""
    response = llm.invoke([
        {"role": "system", "content": "You are a research specialist. Find relevant information."},
        *state["messages"]
    ])
    return Command(
        goto="supervisor",
        update={"messages": [response]}
    )

def writer(state: MessagesState) -> Command[Literal["supervisor"]]:
    """Writer agent creates content."""
    response = llm.invoke([
        {"role": "system", "content": "You are a content writer. Create clear, engaging content."},
        *state["messages"]
    ])
    return Command(
        goto="supervisor",
        update={"messages": [response]}
    )

def reviewer(state: MessagesState) -> Command[Literal["supervisor"]]:
    """Reviewer agent improves content."""
    response = llm.invoke([
        {"role": "system", "content": "You are an editor. Review and suggest improvements."},
        *state["messages"]
    ])
    return Command(
        goto="supervisor",
        update={"messages": [response]}
    )

# Build the graph
builder = StateGraph(MessagesState)
builder.add_node("supervisor", supervisor)
builder.add_node("researcher", researcher)
builder.add_node("writer", writer)
builder.add_node("reviewer", reviewer)

builder.add_edge(START, "supervisor")

graph = builder.compile()
```

**Flow Diagram:**
```
                    ┌──→ [researcher] ──┐
                    │                   │
START → [supervisor]┼──→ [writer] ──────┼──→ [supervisor] ──→ END
                    │                   │
                    └──→ [reviewer] ────┘
```

## Network Pattern (Peer-to-Peer)

Agents communicate directly without a central supervisor:

```python
def agent_researcher(state: MessagesState) -> Command[Literal["agent_writer", "agent_analyst", END]]:
    """Researcher can hand off to writer or analyst."""
    response = llm.invoke([
        {"role": "system", "content": "You research topics. Hand off to writer for content or analyst for data."},
        *state["messages"]
    ])

    # Decide next agent based on content
    next_agent = determine_handoff(response.content)

    return Command(
        goto=next_agent,
        update={"messages": [response]}
    )

def agent_writer(state: MessagesState) -> Command[Literal["agent_researcher", "agent_analyst", END]]:
    """Writer can request more research or analysis."""
    response = llm.invoke([
        {"role": "system", "content": "You write content. Request research or analysis if needed."},
        *state["messages"]
    ])

    next_agent = determine_handoff(response.content)

    return Command(
        goto=next_agent,
        update={"messages": [response]}
    )

def agent_analyst(state: MessagesState) -> Command[Literal["agent_researcher", "agent_writer", END]]:
    """Analyst provides data insights."""
    response = llm.invoke([
        {"role": "system", "content": "You analyze data. Share insights with researcher or writer."},
        *state["messages"]
    ])

    next_agent = determine_handoff(response.content)

    return Command(
        goto=next_agent,
        update={"messages": [response]}
    )

# Build network graph
builder = StateGraph(MessagesState)
builder.add_node("agent_researcher", agent_researcher)
builder.add_node("agent_writer", agent_writer)
builder.add_node("agent_analyst", agent_analyst)

builder.add_edge(START, "agent_researcher")

network = builder.compile()
```

**Flow Diagram:**
```
       ┌─────────────────────────────┐
       │                             │
       ↓                             │
[researcher] ←──────→ [writer] ←─────┘
       ↑                   ↑
       │                   │
       └────→ [analyst] ←──┘
```

## Hierarchical Pattern

Nested teams with sub-supervisors:

```python
# Create specialized team graphs
def create_research_team():
    """Team for research tasks."""
    builder = StateGraph(MessagesState)
    builder.add_node("lead", research_lead)
    builder.add_node("web_searcher", web_search_agent)
    builder.add_node("doc_reader", document_agent)
    # ... edges
    return builder.compile()

def create_writing_team():
    """Team for content creation."""
    builder = StateGraph(MessagesState)
    builder.add_node("lead", writing_lead)
    builder.add_node("copywriter", copywriting_agent)
    builder.add_node("editor", editing_agent)
    # ... edges
    return builder.compile()

# Top-level supervisor
research_team = create_research_team()
writing_team = create_writing_team()

def top_supervisor(state: MessagesState) -> Command[Literal["research_team", "writing_team", END]]:
    """Route to appropriate team."""
    decision = llm.invoke("Which team should handle this?")
    return Command(goto=decision)

def research_team_node(state: MessagesState) -> dict:
    """Execute research team subgraph."""
    result = research_team.invoke(state)
    return {"messages": result["messages"]}

def writing_team_node(state: MessagesState) -> dict:
    """Execute writing team subgraph."""
    result = writing_team.invoke(state)
    return {"messages": result["messages"]}

# Build hierarchical graph
main_graph = StateGraph(MessagesState)
main_graph.add_node("supervisor", top_supervisor)
main_graph.add_node("research_team", research_team_node)
main_graph.add_node("writing_team", writing_team_node)

main_graph.add_edge(START, "supervisor")
main_graph.add_edge("research_team", "supervisor")
main_graph.add_edge("writing_team", "supervisor")
```

## Shared State Between Agents

When agents need access to common data:

```python
class SharedState(TypedDict):
    messages: Annotated[list, add_messages]
    # Shared knowledge base
    facts: Annotated[list[str], operator.add]
    # Shared task list
    tasks: list[dict]
    # Current focus
    current_task: str | None

def agent_with_shared_state(state: SharedState) -> dict:
    """Agent can read and contribute to shared state."""
    # Read shared facts
    context = "\n".join(state["facts"])

    response = llm.invoke([
        {"role": "system", "content": f"Known facts:\n{context}"},
        *state["messages"]
    ])

    # Extract new facts from response
    new_facts = extract_facts(response.content)

    return {
        "messages": [response],
        "facts": new_facts  # Accumulates due to operator.add
    }
```

## Best Practices

1. **Keep agents focused** - Each agent should have one clear responsibility
2. **Limit handoff depth** - Prevent infinite loops with max iterations
3. **Use structured outputs** - For reliable routing decisions
4. **Log agent transitions** - For debugging complex flows
5. **Test individual agents** - Before combining into systems
