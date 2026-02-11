# Tool Integration in LangGraph

How to add and manage tools in LangGraph agents.

## Basic Tool Definition

Create tools using the `@tool` decorator:

```python
from langchain_core.tools import tool

@tool
def search(query: str) -> str:
    """Search the web for information.

    Args:
        query: The search query to execute

    Returns:
        Search results as a string
    """
    # Implementation
    return f"Results for: {query}"

@tool
def calculator(expression: str) -> str:
    """Evaluate a mathematical expression.

    Args:
        expression: A valid Python math expression

    Returns:
        The result of the calculation
    """
    try:
        result = eval(expression)
        return str(result)
    except Exception as e:
        return f"Error: {e}"
```

**Key points:**
- Docstring becomes the tool description (used by LLM)
- Type hints define the input schema
- Return type should be string for LLM consumption

## Binding Tools to LLM

```python
from langchain_anthropic import ChatAnthropic

llm = ChatAnthropic(model="claude-3-5-sonnet-20241022")
tools = [search, calculator]

# Bind tools to the model
llm_with_tools = llm.bind_tools(tools)
```

## Using ToolNode

The prebuilt `ToolNode` executes tool calls:

```python
from langgraph.prebuilt import ToolNode, tools_condition

# Create tool execution node
tool_node = ToolNode(tools)

# Build graph
graph = StateGraph(State)
graph.add_node("agent", agent_node)
graph.add_node("tools", tool_node)

# Route: if tool calls exist, go to tools; else END
graph.add_conditional_edges("agent", tools_condition)
graph.add_edge("tools", "agent")  # Loop back
```

## Custom Tool Execution

For more control over tool execution:

```python
from langchain_core.messages import ToolMessage

def custom_tool_node(state: State) -> dict:
    """Custom tool execution with error handling."""
    messages = state["messages"]
    last_message = messages[-1]

    tool_results = []
    for tool_call in last_message.tool_calls:
        try:
            # Find and execute the tool
            tool_fn = tool_map[tool_call["name"]]
            result = tool_fn.invoke(tool_call["args"])

            tool_results.append(ToolMessage(
                content=result,
                tool_call_id=tool_call["id"]
            ))
        except Exception as e:
            tool_results.append(ToolMessage(
                content=f"Error: {e}",
                tool_call_id=tool_call["id"]
            ))

    return {"messages": tool_results}
```

## Tools with Side Effects

Tools that modify external state:

```python
@tool
def save_to_database(data: dict) -> str:
    """Save data to the database.

    Args:
        data: Dictionary of data to save

    Returns:
        Confirmation message with record ID
    """
    record_id = db.insert(data)
    return f"Saved with ID: {record_id}"

@tool
def send_email(to: str, subject: str, body: str) -> str:
    """Send an email.

    Args:
        to: Recipient email address
        subject: Email subject line
        body: Email body content

    Returns:
        Confirmation of email sent
    """
    email_service.send(to=to, subject=subject, body=body)
    return f"Email sent to {to}"
```

## Structured Output Tools

Return complex data from tools:

```python
from pydantic import BaseModel
import json

class SearchResult(BaseModel):
    title: str
    url: str
    snippet: str

@tool
def structured_search(query: str) -> str:
    """Search and return structured results.

    Args:
        query: Search query

    Returns:
        JSON array of search results
    """
    results = [
        SearchResult(
            title="Result 1",
            url="https://example.com/1",
            snippet="First result snippet"
        ),
        SearchResult(
            title="Result 2",
            url="https://example.com/2",
            snippet="Second result snippet"
        )
    ]
    return json.dumps([r.model_dump() for r in results])
```

## Tools with Confirmation (Human-in-the-Loop)

Require approval before executing:

```python
from langgraph.types import interrupt

@tool
def delete_record(record_id: str) -> str:
    """Delete a record from the database (requires approval).

    Args:
        record_id: ID of record to delete

    Returns:
        Confirmation of deletion
    """
    # Pause for human approval
    response = interrupt({
        "action": "delete_record",
        "record_id": record_id,
        "message": f"Approve deletion of record {record_id}?"
    })

    if response.get("approved"):
        db.delete(record_id)
        return f"Record {record_id} deleted"
    else:
        return f"Deletion of {record_id} was rejected"
```

## Tool Routing Pattern

Different tools for different scenarios:

```python
from typing import Literal

def tool_router(state: State) -> Literal["search_tools", "code_tools", "data_tools"]:
    """Route to appropriate tool set."""
    last_message = state["messages"][-1]

    if last_message.tool_calls:
        tool_name = last_message.tool_calls[0]["name"]

        if tool_name in ["search", "browse"]:
            return "search_tools"
        elif tool_name in ["run_code", "debug"]:
            return "code_tools"
        elif tool_name in ["query_db", "save_data"]:
            return "data_tools"

    return "search_tools"  # Default

# Specialized tool nodes
search_node = ToolNode([search, browse])
code_node = ToolNode([run_code, debug])
data_node = ToolNode([query_db, save_data])

graph.add_node("search_tools", search_node)
graph.add_node("code_tools", code_node)
graph.add_node("data_tools", data_node)

graph.add_conditional_edges("agent", tool_router)
```

## Error Handling

Graceful tool failure handling:

```python
def safe_tool_node(state: State) -> dict:
    """Execute tools with comprehensive error handling."""
    messages = state["messages"]
    last_message = messages[-1]

    results = []
    for tool_call in last_message.tool_calls:
        try:
            tool = tool_map.get(tool_call["name"])
            if not tool:
                raise ValueError(f"Unknown tool: {tool_call['name']}")

            result = tool.invoke(tool_call["args"])
            results.append(ToolMessage(
                content=result,
                tool_call_id=tool_call["id"]
            ))

        except TimeoutError:
            results.append(ToolMessage(
                content="Tool execution timed out. Try a simpler query.",
                tool_call_id=tool_call["id"]
            ))

        except PermissionError:
            results.append(ToolMessage(
                content="Permission denied. This action requires elevated access.",
                tool_call_id=tool_call["id"]
            ))

        except Exception as e:
            results.append(ToolMessage(
                content=f"Tool error: {type(e).__name__}: {e}",
                tool_call_id=tool_call["id"]
            ))

    return {"messages": results}
```

## Best Practices

1. **Clear docstrings** - The LLM uses these to decide when to call tools
2. **Validate inputs** - Check arguments before processing
3. **Return strings** - LLMs work best with string outputs
4. **Handle errors gracefully** - Return error messages, don't crash
5. **Limit side effects** - Use confirmation for destructive actions
6. **Log tool calls** - For debugging and auditing
