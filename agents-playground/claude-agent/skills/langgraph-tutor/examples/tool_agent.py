#!/usr/bin/env python3
"""
LangGraph Agent with Tools Example

Demonstrates the ReAct pattern: Reasoning and Acting with tools.
Run: python tool_agent.py
"""

from typing import Annotated
from typing_extensions import TypedDict

from langchain_anthropic import ChatAnthropic
from langchain_core.tools import tool
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.memory import InMemorySaver


# 1. Define state
class State(TypedDict):
    """Agent state with message history."""
    messages: Annotated[list, add_messages]


# 2. Define tools
@tool
def calculator(expression: str) -> str:
    """Evaluate a mathematical expression.

    Args:
        expression: A valid Python math expression (e.g., "2 + 2", "10 * 5")

    Returns:
        The result of the calculation
    """
    try:
        # Safety: only allow basic math operations
        allowed_chars = set("0123456789+-*/(). ")
        if not all(c in allowed_chars for c in expression):
            return "Error: Only basic math operations allowed"
        result = eval(expression)
        return f"{expression} = {result}"
    except Exception as e:
        return f"Error evaluating '{expression}': {e}"


@tool
def get_weather(city: str) -> str:
    """Get the current weather for a city.

    Args:
        city: Name of the city

    Returns:
        Weather information for the city
    """
    # Mock implementation - replace with real API
    weather_data = {
        "new york": "72°F, Partly Cloudy",
        "london": "58°F, Rainy",
        "tokyo": "68°F, Clear",
        "paris": "64°F, Overcast",
    }
    city_lower = city.lower()
    if city_lower in weather_data:
        return f"Weather in {city}: {weather_data[city_lower]}"
    return f"Weather data not available for {city}"


@tool
def search(query: str) -> str:
    """Search for information on a topic.

    Args:
        query: The search query

    Returns:
        Search results summary
    """
    # Mock implementation - replace with real search API
    return f"Search results for '{query}': This is a mock search result. In production, this would return real search data."


# 3. Create LLM with tools
tools = [calculator, get_weather, search]
llm = ChatAnthropic(model="claude-3-5-sonnet-20241022")
llm_with_tools = llm.bind_tools(tools)


# 4. Define agent node
def agent(state: State) -> dict:
    """The agent decides what to do next.

    If tools are needed, it generates tool calls.
    Otherwise, it responds directly.
    """
    response = llm_with_tools.invoke(state["messages"])
    return {"messages": [response]}


# 5. Build the graph
def create_agent():
    """Create the tool-using agent graph."""
    graph = StateGraph(State)

    # Add nodes
    graph.add_node("agent", agent)
    graph.add_node("tools", ToolNode(tools))

    # Add edges
    graph.add_edge(START, "agent")

    # Conditional edge: route to tools if tool calls exist, else END
    graph.add_conditional_edges(
        "agent",
        tools_condition,
        # Default mapping: "tools" -> tools node, "__end__" -> END
    )

    # After tools execute, go back to agent
    graph.add_edge("tools", "agent")

    # Compile with memory
    memory = InMemorySaver()
    return graph.compile(checkpointer=memory)


# 6. Run the agent
def main():
    """Interactive agent loop."""
    app = create_agent()
    config = {"configurable": {"thread_id": "tool-agent-session"}}

    print("=" * 50)
    print("LangGraph Agent with Tools")
    print("Available tools: calculator, get_weather, search")
    print("Type 'quit' to exit")
    print("=" * 50)

    while True:
        user_input = input("\nYou: ").strip()
        if user_input.lower() in ["quit", "exit", "q"]:
            print("Goodbye!")
            break

        if not user_input:
            continue

        # Invoke the agent
        result = app.invoke(
            {"messages": [("user", user_input)]},
            config
        )

        # Print the final response
        response = result["messages"][-1]
        print(f"\nAssistant: {response.content}")


if __name__ == "__main__":
    main()
