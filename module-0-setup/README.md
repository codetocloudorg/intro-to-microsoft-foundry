# Module 0: Deploy & Connect

**Time:** ~15 minutes, mostly Azure deployment time · **Needs:** an Azure subscription where you are
Owner, Python 3.10+, the Azure CLI

## Objective

A Foundry resource, a project and a model, reachable from your terminal with no API keys.

## What you'll learn

- How to deploy a Foundry environment as code (Bicep)
- Why key-based access is disabled, and how Entra ID plus the **Foundry User** role replaces it
- How to find your project endpoint

> **Windows:** every command in this workshop is bash. Install
> [WSL2](https://learn.microsoft.com/windows/wsl/install) and work inside its terminal, including
> the Azure CLI and `az login`. Native PowerShell has not been tested.

## 1. Install

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

This installs `azure-ai-projects` 2.x, the **Foundry projects (new) API**. Microsoft's docs state that
2.x is incompatible with 1.x, so if an environment already pins an older version, use a fresh virtual
environment.

**Check:** `pip list` shows `azure-ai-projects` 2.x.

## 2. Deploy the environment

`infra/main.bicep` creates one Foundry resource, one project and one `gpt-5-mini` deployment in the
region you pick. It is adapted from Microsoft's own
[00-basic template](https://github.com/microsoft-foundry/foundry-samples/tree/main/infrastructure/infrastructure-setup-bicep/00-basic)
with three deliberate changes:

- **Key-based access is disabled.** Only Microsoft Entra ID works.
- **You are granted the Foundry User role.** Owner and Contributor cannot call the project's data
  plane. That role was formerly named "Azure AI User" (same role ID), so older guides use the old name.
- **The model deployment waits for the project.** Creating them in parallel can fail with
  `RequestConflict`.

```bash
az login
az group create -n rg-foundry-workshop -l eastus2
az deployment group create -g rg-foundry-workshop --template-file infra/main.bicep \
  --parameters principalId=$(az ad signed-in-user show --query id -o tsv)
```

**Check:** the output ends with `"provisioningState": "Succeeded"` and includes `projectEndpoint`.

Takes a few minutes. `eastus2` has the broadest model availability. Check your model per region before
changing it:

```bash
az cognitiveservices model list --location <region> \
  --query "[?model.name=='gpt-5-mini'].{v:model.version,sku:model.skus[].name}" -o json
```

## 3. Set your endpoint

The deployment prints `projectEndpoint`. Set it once as an environment variable:

```bash
export FOUNDRY_PROJECT_ENDPOINT="https://<resource>.services.ai.azure.com/api/projects/intro-workshop"
```

We read the endpoint from the environment instead of hardcoding it, so a real endpoint never gets
committed to a repository.

## Troubleshooting

| Symptom | Likely cause | Fix |
| --- | --- | --- |
| `FOUNDRY_PROJECT_ENDPOINT is not set` | Variable not exported in this shell | Run the `export` above |
| `403` / `PermissionDenied` | Missing **Foundry User** role, or it has not propagated yet | Confirm the role assignment, wait a few minutes, retry |
| `404` on the model | Deployment name differs from `gpt-5-mini` | Set `MODEL_NAME` to your deployment name |
| `AccountNameInvalid` | Resource name taken or invalid | Leave the default name, or pick a globally unique one (lowercase letters, numbers, hyphens) |
| `RequestConflict` | Old template creating project and model in parallel | Use this repository's `infra/main.bicep` |
| Quota error on the model | No capacity in that region | Lower `modelCapacity` or try another region |

## Clean up

```bash
az group delete -n rg-foundry-workshop --yes
```

## Next

[Module 1: Chat with a model](../module-1-chat-with-a-model/README.md)
