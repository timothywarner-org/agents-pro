"""
Contoso Electronics Support Agent -- Azure AI Foundry + Function Calling

This is a teaching scaffold for the O'Reilly "How to Create AI Agents Like a Pro"
course (Hour 3: Code-First Agents). It demonstrates:

  1. Creating an AIProjectClient and authenticating via DefaultAzureCredential
  2. Defining custom function tools the agent can call
  3. Creating an agent with instructions and tool definitions
  4. Running a conversation with manual polling and function dispatch
  5. Cleanup

Prerequisites:
  - pip install -r requirements.txt
  - az login
  - Copy .env.example to .env and fill in PROJECT_ENDPOINT + MODEL_DEPLOYMENT_NAME

Run:
  python agent.py
"""

import os
import time
import json

from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.agents.models import FunctionTool, ListSortOrder

from tools import ALL_TOOLS, lookup_order, check_return_eligibility, check_warranty

load_dotenv()

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
PROJECT_ENDPOINT = os.environ["PROJECT_ENDPOINT"]
MODEL_DEPLOYMENT_NAME = os.environ.get("MODEL_DEPLOYMENT_NAME", "gpt-4o-mini")

AGENT_NAME = "Contoso Support Agent"
AGENT_INSTRUCTIONS = """\
You are a helpful customer support agent for Contoso Electronics.

Your capabilities:
- Look up order status by order ID
- Check return/refund eligibility
- Check product warranty coverage

Guidelines:
- Be friendly and professional
- Always confirm the order ID or product name before looking it up
- If you cannot resolve the issue, suggest the customer contact support@contoso.com
- Keep responses concise
"""

# ---------------------------------------------------------------------------
# Function dispatch map -- maps function names to callables
# ---------------------------------------------------------------------------
FUNCTION_DISPATCH = {
    "lookup_order": lookup_order,
    "check_return_eligibility": check_return_eligibility,
    "check_warranty": check_warranty,
}


def handle_tool_calls(project_client, thread_id, run_id, tool_calls):
    """Execute requested function calls and submit outputs back to the agent."""
    tool_outputs = []
    for tool_call in tool_calls:
        func_name = tool_call.function.name
        func_args = json.loads(tool_call.function.arguments)
        print(f"  -> Tool call: {func_name}({func_args})")

        func = FUNCTION_DISPATCH.get(func_name)
        if func:
            output = func(**func_args)
        else:
            output = json.dumps({"error": f"Unknown function: {func_name}"})

        tool_outputs.append({"tool_call_id": tool_call.id, "output": output})

    project_client.agents.runs.submit_tool_outputs(
        thread_id=thread_id,
        run_id=run_id,
        tool_outputs=tool_outputs,
    )


def run_conversation(project_client, agent_id, user_message):
    """Send a message and run the agent with function-calling loop."""
    # Create a new thread
    thread = project_client.agents.threads.create()
    print(f"\n{'='*60}")
    print(f"Thread: {thread.id}")
    print(f"User:   {user_message}")
    print(f"{'='*60}")

    # Post the user message
    project_client.agents.messages.create(
        thread_id=thread.id,
        role="user",
        content=user_message,
    )

    # Start a run
    run = project_client.agents.runs.create(
        thread_id=thread.id,
        agent_id=agent_id,
    )

    # Poll until complete, handling function calls along the way
    delay = 0.5
    while run.status in ("queued", "in_progress", "requires_action"):
        time.sleep(delay)
        run = project_client.agents.runs.get(
            thread_id=thread.id,
            run_id=run.id,
        )

        if run.status == "requires_action":
            tool_calls = run.required_action.submit_tool_outputs.tool_calls
            handle_tool_calls(project_client, thread.id, run.id, tool_calls)
            delay = 0.5  # reset backoff after action
        else:
            delay = min(delay * 1.5, 5)

    if run.status == "failed":
        print(f"Run failed: {run.last_error}")
        return

    # Print assistant response(s)
    messages = project_client.agents.messages.list(
        thread_id=thread.id,
        order=ListSortOrder.ASCENDING,
    )
    for msg in messages.data:
        if msg.role == "assistant" and msg.text_messages:
            print(f"\nAgent: {msg.text_messages[-1].text.value}")


def main():
    print("Initializing Azure AI Foundry agent...")

    credential = DefaultAzureCredential()
    project_client = AIProjectClient(
        endpoint=PROJECT_ENDPOINT,
        credential=credential,
    )

    # Wrap our tool functions for the agent
    functions = FunctionTool(functions=ALL_TOOLS)

    with project_client:
        # Create the agent
        agent = project_client.agents.create_agent(
            model=MODEL_DEPLOYMENT_NAME,
            name=AGENT_NAME,
            instructions=AGENT_INSTRUCTIONS,
            tools=functions.definitions,
        )
        print(f"Created agent: {agent.id} ({AGENT_NAME})")

        # ---------------------------------------------------------------
        # Demo conversations -- replace or extend with your own
        # ---------------------------------------------------------------
        demo_prompts = [
            "What's the status of order CT-991100?",
            "I want to return order CT-991101 because I changed my mind.",
            "Is the Contoso Pro X15 still under warranty?",
        ]

        try:
            for prompt in demo_prompts:
                run_conversation(project_client, agent.id, prompt)
        finally:
            # Always clean up the agent
            project_client.agents.delete_agent(agent.id)
            print(f"\nDeleted agent: {agent.id}")


if __name__ == "__main__":
    main()
