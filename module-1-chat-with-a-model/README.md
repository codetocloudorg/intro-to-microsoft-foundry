# Module 1: Chat with a Model

**Time:** ~5 minutes · **Needs:** Module 0 complete

## Objective

Make your first Microsoft Foundry call and confirm that your sign-in, endpoint and model deployment
all work, before adding any agent complexity.

## What you'll learn

- How `AIProjectClient` connects to a project using `DefaultAzureCredential` (no API keys)
- How `project.get_openai_client()` gives you a client for the **Responses API**
- That a model call is stateless: one prompt in, one response out

## Run it

```bash
python module-1-chat-with-a-model/chat.py
```

## What you should see

An answer about the size of France. Wording varies between runs, but it should look like this:

```text
Response output: It depends whether you include overseas territories:
- Total: about 248,573 square miles (643,801 km²)
- Metropolitan France: about 213,011 square miles (551,695 km²)
```

**Success check:** the script prints a non-empty `Response output:` and exits without an error.

## What just happened

1. `DefaultAzureCredential` used your `az login` session to get a token. Nothing secret is in the code.
2. The client sent your prompt to the `gpt-5-mini` deployment through the Responses API.
3. Nothing was saved. Ask a follow-up and the model would not remember the first question. Module 2
   fixes that.

## If it fails

See the troubleshooting table in [Module 0](../module-0-setup/README.md#troubleshooting). The two
common causes are an unset `FOUNDRY_PROJECT_ENDPOINT` and a missing Foundry User role.

## Try it yourself

Change the `input` in `chat.py` to your own question. Then set `MODEL_NAME` to a different deployment
if you have one.

## Next

[Module 2: Build an agent](../module-2-build-an-agent/README.md)
