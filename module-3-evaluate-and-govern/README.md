# Module 3: Evaluate & Govern

An agent that responds and an agent that is safe to ship are different bars. This module closes the
gap with Microsoft's open-source [AgentOps Accelerator](https://github.com/Azure/agentops).

> **Status:** AgentOps Accelerator is pre-1.0 (0.15.1 when this was tested on 2026-09-26). The version
> is pinned in `requirements-module3.txt`. Commands and output can change between releases, so check
> its README if something differs.

**Time:** ~25 minutes · **Needs:** Module 2 complete, so the agent `code-to-cloud-intro-agent` exists

## Objective

Prove the agent is fit to ship, with a repeatable score, a pass/fail gate and a release-readiness
report, instead of a one-time "it seemed to work".

## What you'll learn

- How to baseline an agent with an evaluation you can re-run on demand
- How a threshold turns a score into a gate with a real exit code (`0` pass, `2` fail)
- How to read a release-readiness report and act on its findings

## 1. Install and initialise

```bash
pip install -r requirements-module3.txt
export FOUNDRY_PROJECT_ENDPOINT="https://<resource>.services.ai.azure.com/api/projects/intro-workshop"

agentops init --no-prompt \
  --project-endpoint "$FOUNDRY_PROJECT_ENDPOINT" \
  --agent code-to-cloud-intro-agent:1
```

This writes `agentops.yaml` and a `.agentops/` folder with a three-row starter dataset
(`.agentops/data/smoke.jsonl`). It does not create anything in Azure.

> Do not use `agentops eval init` for this. It is a different command that scaffolds cloud
> evaluation assets with `azd`.

## 2. Run the baseline evaluation

AgentOps scores answers with a judge model. Point it at a deployment in your project:

```bash
export AZURE_OPENAI_DEPLOYMENT=gpt-5-mini
agentops eval run
```

It calls the agent for each dataset row, then scores coherence, fluency, similarity and response
completeness, plus latency. Results land in `.agentops/results/latest/` (`results.json`, `report.md`).

## 3. Add a pass/fail gate

A score with no limit is a number, not a gate. Add thresholds to `agentops.yaml`:

```yaml
thresholds:
  coherence: ">=4"
  similarity: ">=4"
  response_completeness: ">=4"
```

Run `agentops eval run` again. It prints `Threshold status: PASSED` and exits `0`. Change one limit to
something unreachable (`coherence: ">=6"`) and it prints `FAILED` and exits `2`. That exit code is what
lets a CI job block a release.

## 4. Check release readiness

```bash
agentops doctor --evidence-pack
```

Doctor checks your workspace, Azure sign-in and the Foundry project, then writes:

- `.agentops/agent/report.md`, the findings
- `.agentops/release/latest/evidence.md` and `evidence.json`, an evidence pack you can keep as a
  compliance artifact

On a fresh workshop project the result is `ready_with_warnings`. Its warnings are real and worth
reading. Typical ones are: no agreed thresholds (fixed in step 3), no baseline result to gate
regressions against, no production telemetry (Application Insights not connected to the project), no
continuous-evaluation rules, and no red-team evidence. Fix what applies, re-run doctor, and watch the
list shrink.

## 5. Open the cockpit

```bash
agentops cockpit
```

A read-only local dashboard on `http://127.0.0.1:8090` combining evaluation history and doctor
findings. Leave the terminal open. Press Enter to stop it.

## What you have at the end

- A working multi-turn Foundry agent (Module 2)
- A repeatable baseline evaluation
- A pass/fail gate with a real exit code
- A release-readiness report and evidence pack
- A local dashboard

## Where to go next

- **Put the gate in CI.** `agentops workflow --help` covers generating CI/CD workflows.
- **Red-team the agent.** `agentops redteam` runs Foundry's AI Red Teaming agent (requires
  `azure-ai-evaluation` and a `redteam:` block in `agentops.yaml`).
- **Move from a workshop to a platform.** Private networking, policy, identity and cost controls are
  what [Azure AI Landing Zones](https://github.com/Azure/AI-Landing-Zones) covers. We wrote up its
  design checklist at
  [codetocloud.io/blog/azure-ai-landing-zones](https://codetocloud.io/blog/azure-ai-landing-zones/).
