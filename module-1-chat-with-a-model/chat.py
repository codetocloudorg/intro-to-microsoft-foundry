# Copyright (c) Code To Cloud Inc. Licensed under the MIT License.
"""
Module 1 — Chat With a Model

Your first Microsoft Foundry API call: send a prompt, get a response.
No agent, no state — just the model.

Verified against Microsoft's current Foundry SDK quickstart
(learn.microsoft.com/en-us/azure/foundry/quickstarts/get-started-code,
updated 2026-09-04) and run against a live project on 2026-09-26 with
azure-ai-projects 2.7.0. Requires Module 0's setup to be complete.
"""
import os

from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential

FOUNDRY_PROJECT_ENDPOINT = os.environ.get("FOUNDRY_PROJECT_ENDPOINT")
if not FOUNDRY_PROJECT_ENDPOINT:
    raise SystemExit(
        "FOUNDRY_PROJECT_ENDPOINT is not set. See module-0-setup/README.md, step 3."
    )

# Matches the deployment created by infra/main.bicep. Override if you deployed under another name.
MODEL_NAME = os.environ.get("MODEL_NAME", "gpt-5-mini")


def main() -> None:
    project = AIProjectClient(
        endpoint=FOUNDRY_PROJECT_ENDPOINT,
        credential=DefaultAzureCredential(),
    )
    openai = project.get_openai_client()

    response = openai.responses.create(
        model=MODEL_NAME,
        input="What is the size of France in square miles?",
    )

    if not response.output_text or not response.output_text.strip():
        raise RuntimeError("Response output text was empty.")

    print(f"Response output: {response.output_text}")


if __name__ == "__main__":
    main()
