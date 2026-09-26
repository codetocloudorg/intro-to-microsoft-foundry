# Copyright (c) Code To Cloud Inc. Licensed under the MIT License.
"""
Module 2 — Build an Agent

A named, versioned agent that holds instructions and maintains a multi-turn
conversation — the step up from Module 1's one-shot model call.

Verified against Microsoft's current Foundry SDK quickstart
(learn.microsoft.com/en-us/azure/foundry/quickstarts/get-started-code,
updated 2026-09-04) and run against a live project on 2026-09-26 with
azure-ai-projects 2.7.0. Requires Module 0's setup to be complete.
"""
import os

from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import PromptAgentDefinition
from azure.identity import DefaultAzureCredential

FOUNDRY_PROJECT_ENDPOINT = os.environ.get("FOUNDRY_PROJECT_ENDPOINT")
if not FOUNDRY_PROJECT_ENDPOINT:
    raise SystemExit(
        "FOUNDRY_PROJECT_ENDPOINT is not set. See module-0-setup/README.md, step 3."
    )
FOUNDRY_AGENT_NAME = "code-to-cloud-intro-agent"
MODEL_NAME = os.environ.get("MODEL_NAME", "gpt-5-mini")


def main() -> None:
    project = AIProjectClient(
        endpoint=FOUNDRY_PROJECT_ENDPOINT,
        credential=DefaultAzureCredential(),
    )

    # Creates the agent, or a new version if it already exists.
    agent = project.agents.create_version(
        agent_name=FOUNDRY_AGENT_NAME,
        definition=PromptAgentDefinition(
            model=MODEL_NAME,
            instructions="You are a helpful assistant that answers general questions",
        ),
    )
    print(f"Agent created (id: {agent.id}, name: {agent.name}, version: {agent.version})")

    # An OpenAI client pre-bound to this agent.
    openai = project.get_openai_client(agent_name=FOUNDRY_AGENT_NAME)

    # A conversation object is what makes this multi-turn — the agent
    # remembers the first question when answering the second.
    conversation = openai.conversations.create()

    response = openai.responses.create(
        conversation=conversation.id,
        input="What is the size of France in square miles?",
    )
    print(response.output_text)

    follow_up = openai.responses.create(
        conversation=conversation.id,
        input="And what is the capital city?",
    )
    print(follow_up.output_text)


if __name__ == "__main__":
    main()
