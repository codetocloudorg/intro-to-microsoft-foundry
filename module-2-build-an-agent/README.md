# Module 2: Build an Agent

**Time:** ~10 minutes · **Needs:** Module 1 working

## Objective

Build a named, versioned agent that keeps instructions and remembers earlier turns of a conversation.
This is the step up from Module 1's one-shot model call.

## What you'll learn

- An agent is a **named, versioned definition**: `project.agents.create_version(...)` creates version 1,
  and calling it again creates version 2. Nothing is overwritten.
- `PromptAgentDefinition` holds the model and the standing instructions.
- Multi-turn memory comes from a **conversation** object, not from the agent itself. Pass the same
  conversation ID to each response call.

## Run it

```bash
python module-2-build-an-agent/agent.py
```

## What you should see

```text
Agent created (id: code-to-cloud-intro-agent:1, name: code-to-cloud-intro-agent, version: 1)
France's total area (including overseas regions) is about 248,573 square miles (643,801 km²).
The capital of France is Paris ...
```

**Success check:** the agent is created, and the second answer is about the **capital**, which shows it
understood "the capital" from the first question. That is the conversation memory working.

## What just happened

1. A new agent version was registered in your project. Run the script again and the version number goes
   to 2.
2. A conversation was created. The first question and the follow-up ("And what is the capital city?")
   share it, so the follow-up makes sense without repeating "France".
3. You can see the agent in the Foundry portal under your project's agents.

## If it fails

See [Module 0's troubleshooting table](../module-0-setup/README.md#troubleshooting). If
`create_version` is missing, you likely have `azure-ai-projects` 1.x installed. Run
`pip install -r requirements.txt` in a fresh virtual environment.

## Try it yourself

- Change the `instructions` (for example, "Answer in one sentence") and run it again. You get version 2.
- Add a third question to the conversation that depends on the previous two.

## Next

[Module 3: Evaluate & govern](../module-3-evaluate-and-govern/README.md)
