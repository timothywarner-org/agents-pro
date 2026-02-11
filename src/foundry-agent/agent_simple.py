"""
Minimal Foundry agent -- no function tools, just chat.

Use this as the absolute simplest starting point. The agent uses only its
built-in model knowledge (no custom tools, no knowledge sources).

Run:
  python agent_simple.py "What laptops do you recommend for software development?"
"""

import os
import sys

from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.agents.models import ListSortOrder

load_dotenv()

PROJECT_ENDPOINT = os.environ["PROJECT_ENDPOINT"]
MODEL_DEPLOYMENT_NAME = os.environ.get("MODEL_DEPLOYMENT_NAME", "gpt-4o-mini")


def main():
    user_input = " ".join(sys.argv[1:]) or "Hello! What can you help me with?"

    project_client = AIProjectClient(
        endpoint=PROJECT_ENDPOINT,
        credential=DefaultAzureCredential(),
    )

    with project_client:
        # Create agent
        agent = project_client.agents.create_agent(
            model=MODEL_DEPLOYMENT_NAME,
            name="Contoso Quick Agent",
            instructions="You are a helpful support agent for Contoso Electronics. Be concise.",
        )
        print(f"Agent: {agent.id}")

        # Create thread, send message, run
        thread = project_client.agents.threads.create()
        project_client.agents.messages.create(
            thread_id=thread.id, role="user", content=user_input,
        )
        run = project_client.agents.runs.create_and_process(
            thread_id=thread.id, agent_id=agent.id,
        )

        if run.status == "failed":
            print(f"Error: {run.last_error}")
            return

        # Print response
        messages = project_client.agents.messages.list(
            thread_id=thread.id, order=ListSortOrder.ASCENDING,
        )
        for msg in messages.data:
            if msg.role == "assistant" and msg.text_messages:
                print(f"\n{msg.text_messages[-1].text.value}")

        # Cleanup
        project_client.agents.delete_agent(agent.id)


if __name__ == "__main__":
    main()
