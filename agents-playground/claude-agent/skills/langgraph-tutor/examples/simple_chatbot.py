#!/usr/bin/env python3
"""
Simple LangGraph Chatbot Example

A minimal chatbot demonstrating StateGraph fundamentals.
Run: python simple_chatbot.py
"""

from typing import Annotated
from typing_extensions import TypedDict

from langchain_anthropic import ChatAnthropic
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import InMemorySaver


# 1. Define the state schema
class State(TypedDict):
    """State that flows through the graph.

    messages: Conversation history (accumulates via add_messages reducer)
    """
    messages: Annotated[list, add_messages]


# 2. Create the LLM
llm = ChatAnthropic(model="claude-3-5-sonnet-20241022")


# 3. Define the chatbot node
def chatbot(state: State) -> dict:
    """Process messages and generate a response.

    Args:
        state: Current graph state with message history

    Returns:
        Dict with new message to add to state
    """
    response = llm.invoke(state["messages"])
    return {"messages": [response]}


# 4. Build the graph
def create_chatbot():
    """Create and compile the chatbot graph."""
    graph = StateGraph(State)

    # Add the chatbot node
    graph.add_node("chatbot", chatbot)

    # Connect: START -> chatbot -> END
    graph.add_edge(START, "chatbot")
    graph.add_edge("chatbot", END)

    # Compile with memory for conversation persistence
    memory = InMemorySaver()
    return graph.compile(checkpointer=memory)


# 5. Run the chatbot
def main():
    """Interactive chatbot loop."""
    app = create_chatbot()
    config = {"configurable": {"thread_id": "demo-session"}}

    print("=" * 50)
    print("Simple LangGraph Chatbot")
    print("Type 'quit' to exit")
    print("=" * 50)

    while True:
        user_input = input("\nYou: ").strip()
        if user_input.lower() in ["quit", "exit", "q"]:
            print("Goodbye!")
            break

        if not user_input:
            continue

        # Invoke the graph
        result = app.invoke(
            {"messages": [("user", user_input)]},
            config
        )

        # Print the response
        response = result["messages"][-1]
        print(f"\nAssistant: {response.content}")


if __name__ == "__main__":
    main()
