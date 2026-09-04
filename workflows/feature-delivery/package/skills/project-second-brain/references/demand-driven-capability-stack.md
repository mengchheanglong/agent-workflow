# Demand-Driven Capability Stack Pattern

Use this when the user wants to build an AI/Hermes/JARVIS-like capability system, skill library, research operator, or tiered roadmap.

## Core principle

```text
Capability should follow demand, not imagination.
```

Do not build a general “JARVIS for everything.” Build the current battlefield first, and park exciting future domains until a real project demands them.

## When to use

Use this pattern for:

- Hermes/skill-router/library improvement roadmaps
- project-local capability stacks
- research/evidence/operator systems
- business/hackathon/coding orchestration workflows
- deciding whether a new tool deserves a skill, adapter, DK/capability-control backing, or only backlog status

## Recommended structure

```text
project-root/
  AGENTS.md
  README.md
  .active/
    README.md
    SESSION-START.md
    CURRENT.md
    NEXT.md
    DECISIONS.md
    STATE.json
    CAPABILITY-INDEX.md
  capabilities/
    <class-level-capability>.md
  contracts/
    universal-artifact.schema.json
    source-score.schema.json
    simulation-packet.schema.json
    builder-handoff.schema.json
    verification-report.schema.json
  templates/
    capability-card.md
    artifact-contract.md
    evidence-brief.md
    source-scorecard.md
    builder-handoff.md
  evaluations/
    golden-requests.md
    smoke-cases.md
    score-rubric.md
  context/
    MEMORY-HYGIENE.md
  backlog/
    tier-3-future-lab.md
    ideas.md
```

## Capability admission rule

A new capability enters the active stack only if at least one is true:

1. The user has already needed it repeatedly.
2. It removes a current bottleneck.
3. It reduces future steering/corrections.
4. It produces a reusable verified artifact.
5. It backs a current business, hackathon, research, or coding-orchestration workflow.

Otherwise, park it in `backlog/`, not the active stack.

## Universal capability card

Each durable capability should have:

- Trigger
- Inputs
- Step-by-step workflow
- Output artifact/template/schema
- Verification gate
- Smoke case
- Known failure modes
- Escalation rule
- Memory/storage rule
- Example output

If any are missing, treat the capability as draft.

## Artifact discipline

Prefer checkable artifacts over chat-only answers:

```json
{
  "capability": "string",
  "request": "string",
  "inputs": [],
  "sources": [],
  "assumptions": [],
  "artifact_paths": [],
  "confidence": 0.0,
  "verification": {
    "level": "V0-chat-only|V1-sourced|V2-artifact|V3-tested|V4-externally-validated",
    "checks_run": [],
    "passed": false,
    "limitations": []
  },
  "next_action": "string"
}
```

Default target for serious Tier 1/Tier 2 workflows: V2 artifact; use V3 for code/tool workflows.

## Golden routing tests

Before expanding a capability stack, write golden requests that prove routing works. Example classes:

- suggestion/recommendation request → skill-router first
- research/market reality request → evidence engine
- domain business request → domain skill
- hackathon/form critique → hackathon/judge skill
- repo bug/fix request → cost-aware router + builder handoff
- “remember this” request → memory vs skill vs `.active/` classification

Patch router/skills only after a concrete golden test or live request exposes a real gap.

## Escalation rule

- Skill = user-facing workflow/UX.
- Project `.active/` = current state and recovery.
- Template/schema = repeatable artifact shape.
- External builder = implementation/design execution.
- DK/capability-control = only when proof, contracts, portability, or verified adapters matter.

## Pitfalls

- Do not create one narrow skill per session; update a class-level umbrella or add a reference file.
- Do not activate CAD/physics/lab/science domains just because they are exciting; backlog them until needed.
- Do not save raw feed dumps or temporary task status as memory.
- Do not claim a capability works until a smoke case or verification artifact exists.
