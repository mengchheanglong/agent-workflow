# Capability-stack project brain pattern

Use when the user wants to build or organize a demand-driven capability stack, skill library, agent harness, or “JARVIS-like” roadmap without bloating into future domains.

## Goal

Turn a strategic capability roadmap into a file-first project brain that agents can resume, route through, test, and extend.

This is not for a one-off project note. Use it when the work has multiple capability lanes such as:

- AI harness / skill routing;
- research evidence engine;
- business workflows;
- hackathon/judge workflows;
- coding orchestration;
- future/parked capability domains.

## Core principle

```text
Capability should follow demand, not imagination.
```

Park future domains until a real project demands them. Do not build CAD/physics/lab/HPC lanes just because they sound impressive.

## Recommended folder shape

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
    <capability>.md
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
    simulation-packet.md
    builder-handoff.md
  evaluations/
    golden-requests.md
    smoke-cases.md
    score-rubric.md
    <smoke-run>.md
  context/
    MEMORY-HYGIENE.md
  backlog/
    tier-3-future-lab.md
    ideas.md
```

## Universal capability card

Each durable capability should have:

- trigger;
- inputs;
- step-by-step process;
- output artifact/template/schema;
- verification gate;
- escalation rule;
- memory/storage rule;
- known failure modes;
- smoke case.

If any are missing, treat the capability as draft.

## Universal artifact contract

For non-trivial outputs, capture:

```json
{
  "capability": "",
  "request": "",
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
  "next_action": ""
}
```

## Golden routing tests

Before adding more capabilities, define golden requests that should route correctly. Example classes:

- broad suggestion request → skill-router + specific domain skill;
- research question → web-research/evidence workflow;
- business workflow → business skill + evidence if needed;
- hackathon critique → form/judge-defense skill;
- coding request → cost-aware routing + builder handoff + verification;
- “remember this” → memory vs skill vs `.active/` classification.

Record expected route, actual route, artifact, and pass criteria in `evaluations/golden-requests.md`.

## Smoke-case sequence

Build in this order:

1. Phase 0: project brain and active files.
2. Phase 1: capability cards, contracts, templates, golden routing tests, memory hygiene.
3. First real research evidence smoke case.
4. Domain-specific smoke case.
5. Builder/coding orchestration smoke case.
6. Only then promote Tier 2 source catalogs, monitoring, or deeper automation.

## Storage rule

- Current state → `.active/`.
- Durable routing/project shape → `AGENTS.md`, `CAPABILITY-INDEX.md`, capability files.
- Evidence and test runs → `evaluations/`.
- Reusable output shapes → `templates/`.
- Machine contracts → `contracts/`.
- Future/unadmitted domains → `backlog/`.

## Verification

After creating the project brain:

1. list files;
2. read back `AGENTS.md`, `.active/NEXT.md`, `.active/STATE.json`;
3. validate JSON contracts/state;
4. write a first golden routing run or smoke-case run;
5. update `NEXT.md` and `STATE.json` to the next slice.
