#!/usr/bin/env python3
"""
LangGraph Multi-Agent Example (Supervisor Pattern)

Demonstrates coordinating multiple specialized agents with a supervisor.
Run: python multi_agent.py
"""

from typing import Annotated, Literal
from typing_extensions import TypedDict

from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage, AIMessage
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.types import Command
from langgraph.checkpoint.memory import InMemorySaver


# 1. Define state
class State(TypedDict):
    """Multi-agent state with shared message history."""
    messages: Annotated[list, add_messages]
    next_agent: str | None


# 2. Create LLMs for each agent
llm = ChatAnthropic(model="claude-3-5-sonnet-20241022")


# 3. Define the Supervisor
def supervisor(state: State) -> Command[Literal["researcher", "writer", "critic", "__end__"]]:
    """Supervisor routes tasks to specialist agents.

    Decides which agent should handle the next step based on conversation context.
    """
    system_prompt = """You are a supervisor coordinating a team of specialists:

    - researcher: Finds information, gathers data, answers factual questions
    - writer: Creates content, drafts text, formats documents
    - critic: Reviews work, provides feedback, suggests improvements

    Based on the conversation, decide who should act next.
    If the task is complete and the user is satisfied, respond with "__end__".

    Respond with ONLY the agent name or "__end__"."""

    response = llm.invoke([
        {"role": "system", "content": system_prompt},
        *state["messages"],
        {"role": "user", "content": "Who should handle this next? Reply with just the agent name or __end__"}
    ])

    next_agent = response.content.strip().lower()

    # Validate response
    valid_agents = ["researcher", "writer", "critic", "__end__"]
    if next_agent not in valid_agents:
        next_agent = "researcher"  # Default fallback

    if next_agent == "__end__":
        return Command(goto=END)

    return Command(goto=next_agent)


# 4. Define Specialist Agents
def researcher(state: State) -> Command[Literal["supervisor"]]:
    """Research agent gathers information."""
    response = llm.invoke([
        {"role": "system", "content": """You are a research specialist.
        Your job is to find information, gather data, and answer factual questions.
        Be thorough but concise. Cite sources when possible."""},
        *state["messages"]
    ])

    return Command(
        goto="supervisor",
        update={"messages": [AIMessage(content=f"[Researcher]: {response.content}")]}
    )


def writer(state: State) -> Command[Literal["supervisor"]]:
    """Writer agent creates content."""
    response = llm.invoke([
        {"role": "system", "content": """You are a content writer.
        Your job is to create clear, engaging content based on requirements.
        Focus on structure, clarity, and readability."""},
        *state["messages"]
    ])

    return Command(
        goto="supervisor",
        update={"messages": [AIMessage(content=f"[Writer]: {response.content}")]}
    )


def critic(state: State) -> Command[Literal["supervisor"]]:
    """Critic agent reviews and improves."""
    response = llm.invoke([
        {"role": "system", "content": """You are a constructive critic.
        Your job is to review work, identify areas for improvement,
        and provide actionable feedback. Be helpful, not harsh."""},
        *state["messages"]
    ])

    return Command(
        goto="supervisor",
        update={"messages": [AIMessage(content=f"[Critic]: {response.content}")]}
    )


# 5. Build the graph
def create_multi_agent():
    """Create the multi-agent graph with supervisor."""
    graph = StateGraph(State)

    # Add all nodes
    graph.add_node("supervisor", supervisor)
    graph.add_node("researcher", researcher)
    graph.add_node("writer", writer)
    graph.add_node("critic", critic)

    # Start with supervisor
    graph.add_edge(START, "supervisor")

    # Compile with memory
    memory = InMemorySaver()
    return graph.compile(checkpointer=memory)


# 6. Run the multi-agent system
def main():
    """Interactive multi-agent loop."""
    app = create_multi_agent()
    config = {"configurable": {"thread_id": "multi-agent-session"}}

    print("=" * 60)
    print("LangGraph Multi-Agent System (Supervisor Pattern)")
    print("Agents: Supervisor, Researcher, Writer, Critic")
    print("Type 'quit' to exit")
    print("=" * 60)

    while True:
        user_input = input("\nYou: ").strip()
        if user_input.lower() in ["quit", "exit", "q"]:
            print("Goodbye!")
            break

        if not user_input:
            continue

        print("\n[Processing with multi-agent team...]")

        # Invoke the graph
        result = app.invoke(
            {"messages": [HumanMessage(content=user_input)]},
            config
        )

        # Print all agent responses
        print("\n" + "-" * 40)
        for msg in result["messages"]:
            if isinstance(msg, AIMessage):
                print(f"\n{msg.content}")
        print("-" * 40)


if __name__ == "__main__":
    main()
