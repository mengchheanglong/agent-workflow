---
name: cost-aware-execution-router
description: "Choose the cheapest effective execution path for coding work: direct GPT, spec-to-cheap-implementer-to-GPT-eval, or split the task smaller."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [cost, routing, coding, evaluation, workflow]
    related_skills: [cost-control-agent-workflow, model-task-router, directive-kernel]
---

# Cost-Aware Execution Router

## Purpose

Use this skill **before starting any coding task** to decide whether Hermes should:

1. **Implement directly with GPT**
2. **Write a tight spec, send execution to a cheaper coder, then do a narrow GPT review**
3. **Split the task smaller before choosing**

The goal is **lowest cost per successful merged slice**, not lowest cost per prompt.

## Core Principle

A review loop only saves money when GPT is used as a **narrow architect/reviewer**, not as a second full implementer.

If GPT must read:
- a huge spec,
- a huge diff,
- broad repo context,
- and then fix many issues,

then the cheap-model workflow is not actually cheap.

## Decision Axes

Score the task on these axes before choosing a path:

### 1. Scope size
- **Small**: 1–3 files, likely under ~250 LOC changed
- **Medium**: 2–6 files, likely ~250–800 LOC changed
- **Large**: 6+ files, broad cross-cutting change, or unclear blast radius

### 2. Risk level
Treat as **high risk** if it touches any of:
- shared contracts / schemas / interfaces
- auth, security, trust, permission gates
- routing logic or selection logic
- state machines / lifecycle progression
- caching or invalidation that can corrupt behavior
- cross-module semantics where one subtle mistake cascades

### 3. Clarity
- **Clear**: exact files and behavior are known
- **Medium**: behavior is known but file scope may drift
- **Unclear**: architecture or file scope is not yet bounded

### 4. Review width
Can GPT review only:
- the spec,
- the changed files or diff,
- the test/lint output,
- and one or two risky contracts?

If **no**, the cheap-model workflow is unlikely to save money.

### 5. Retry likelihood
If the first implementation is likely to require more than **one correction pass**, the cheap-model path often loses its cost advantage.

## Routing Rules

## Route 0 — Greenfield instead of refactor

Before choosing an implementation worker, ask whether the task is actually a refactor or a rebuild decision.

Prefer a **new minimal build** over refactoring an old system when most are true:
- the surviving product is much smaller than the old system
- old architecture carries broad historical coupling or product assumptions
- compatibility with old package/API is not required
- a first vertical slice can prove the value cheaply
- the old system can be used as donor/reference material instead of foundation

Prefer **refactor** when compatibility, existing consumers, validated contracts, or migration cost dominate.

Greenfield only saves money if v1 is ruthless: rebuild the surviving core, not every old surface. Write a decision spec first, then an MVP spec, then a bounded BUILD handoff.

## Route A — Direct GPT implementation
Choose this when **most** are true:
- task is **small**
- low or moderate risk
- 1–3 files
- behavior is clear
- likely one-shot implementation
- overhead of writing/reviewing a spec would dominate the task

Also choose Direct GPT for **high-risk work even when small**.

### Examples
- focused bug fix in one module
- small feature in a known file
- narrow test repair
- tightly scoped CLI option change

## Route B — Tight spec → cheap implementer → narrow GPT eval
Choose this when **all** are true:
- task is **medium-sized**
- allowed files can be explicitly listed
- requirements can be made binary and testable
- GPT review can stay narrow
- cheap implementer is likely to get 80–90% right in one pass
- there is a clean verification gate (tests/lint/typecheck/CLI output)

### Required structure for Route B
The spec must be:
- one slice only
- allowed files explicitly listed
- forbidden files explicitly listed
- exact required commands included
- final report format fixed
- easy for GPT to evaluate with a checklist

### Examples
- bounded refactor slice across 3–6 files
- repetitive wiring after the core pattern is already proven
- adding read-model fields plus tests where verification is easy

## Route C — Split first, then route again
Choose this when any are true:
- task is too broad to fit in one slice
- allowed file list is fuzzy
- architecture is unsettled
- cheap implementer would likely improvise
- GPT review would require broad repo reading

If a task cannot be reviewed cheaply, **make the task smaller** before execution.

## Hard override: always use Direct GPT
Even if the task looks small, use Direct GPT when it touches:
- trust gates
- projection eligibility
- auth/security boundaries
- invoke fallbacks
- cross-module contracts
- subtle lifecycle or state transitions

Reason: one wrong assumption here creates expensive evaluation and correction loops.

## Cost Heuristic

### Cheap-model workflow probably saves money when:
- GPT writes a **short spec**, not a long design doc
- cheap implementer changes a **small diff**, not broad architecture
- GPT reviews **changed files only**, not the repo
- there is **one review pass**, maybe one tiny correction
- tests give a strong pass/fail signal

### Cheap-model workflow probably costs more when:
- GPT writes a large spec
- cheap implementer touches too many files
- GPT must read the whole repo or full broad diff
- more than one correction loop is likely
- GPT effectively becomes a second implementer

## Practical Thresholds

Use these defaults unless the user overrides them:

### Direct GPT
- 1–3 files
- expected diff <250 LOC
- low ambiguity
- any high-risk logic

### Spec → cheap implementer → GPT eval
- 2–6 files
- expected diff 250–800 LOC
- requirements can be converted into a binary checklist
- review can be narrow
- no more than one correction round expected

### Split first
- 6+ files
- expected diff >800 LOC
- unclear scope
- architecture unclear
- likely repeated review loops

## Refactor vs Greenfield Cost Rule

When the user suspects a rebuild may be cheaper than refactoring, treat it as a first-class cost-routing question, not as resistance to planning.

Prefer **greenfield from scratch** when most are true:
- the surviving product/core is much smaller than the existing codebase
- the existing repo contains old product framing, dead lanes, or broad historical scaffolding
- compatibility with current public APIs/package exports is not required
- the new system can prove value with one thin vertical slice
- old code can be used as reference/donor material rather than preserved in place
- refactoring would force GPT/Codex to understand broad hidden coupling before delivering value

Prefer **in-place refactor** only when one of these is true:
- existing package/API consumers must be preserved
- existing tests/contracts are required compatibility gates
- migration cost is lower than rebuilding the first value slice
- the old repo already has the exact abstractions needed and little dead surface

For DK-like projects, a greenfield MVP spec is often cheaper than a broad shrink refactor when the surviving value is just `verified capability truth under skills`. Do not rebuild old surfaces by default.

## Review Escalation Rule

If Route B was chosen and the first evaluation finds:
- more than one substantive logic issue, or
- scope drift outside the allowed files, or
- GPT would now need broad repo reasoning to continue,

then **stop the cheap loop**.

Do **not** keep paying for repeated cheap retries.
Either:
1. switch to Direct GPT, or
2. split the task into smaller slices.

## Evaluation Cost Tiers

Use the cheapest evaluation tier that still protects correctness.

### Tier 1 — Mechanical acceptance (cheapest)
Use when the slice is low risk and tightly bounded.

Check only:
- allowed file list
- `git diff --name-only`
- `git diff --stat`
- required test/lint/typecheck command output
- maybe one schema or response contract if directly touched

No full model review of the code body unless one of those checks fails.

### Tier 2 — Targeted semantic review
Use when the slice is medium risk.

Review only:
- the spec
- changed files or diff
- command output
- one or two risky seams

Do not re-read the repo broadly.

### Tier 3 — Full semantic review
Use only for high-risk slices:
- trust/projection/invoke/routing logic
- security/auth
- cross-module contracts
- subtle lifecycle/state transitions

Even in Tier 3, prefer **rubric-delta evaluation** before broad rereading: convert each acceptance criterion into a specific check, inspect only the changed line ranges/functions needed for that check, and add 1–3 risky seam spot-checks. Escalate to full-file or repo-wide review only when a criterion fails, evidence is ambiguous, or the diff touches unlisted semantics.

If Hermes is about to do Tier 3 repeatedly on medium-risk slices, the workflow is too expensive and should be redesigned.

## Skip-Full-Review Rule

If a direct Codex/GPT slice is:
- low risk,
- within the allowed files,
- passes required commands,
- and does not touch high-risk logic,

then Hermes should prefer **Tier 1 mechanical acceptance** over a full second-pass semantic review.

The goal is to avoid paying for a second implementer disguised as a reviewer.

## Output Format

When using this skill, Hermes should give a brief routing verdict before execution.
A reusable version lives at `templates/decision-template.md`.

```text
Execution route: Direct GPT | Spec→Cheap Implementer→GPT Eval | Split First
Why:
- scope: ...
- risk: ...
- review width: ...
- retry likelihood: ...
Decision: ...
```

## DK-Specific Guidance

For Directive Kernel work:
- prefer **small allowed-file slices**
- when the target has shrunk far below the old repo shape, explicitly compare **greenfield minimal build vs in-place refactor** before coding; if old DK is mostly historical coupling and the surviving product is only verified capability truth under skills, greenfield is often cheaper
- treat trust/projection/invoke/routing logic as **high risk**
- treat source-classification and routing-policy slices (for example `source-operationalization` or changes to `engine/routing/assessment.ts`) as **direct GPT / Codex** work, not cheap-loop work
- for bounded helper/CLI/UI/read-model slices with explicit allowed files and binary tests, prefer **Spec → Codex `gpt-5.3-codex-spark` implementer → narrow Hermes evaluation** before reaching for 5.4/5.5 implementation
- accept cheap-model execution only when Hermes can evaluate by:
  - spec,
  - changed files,
  - test output,
  - and a short checklist

If Hermes must mentally reconstruct broad architecture during evaluation, the slice was too large or too risky for the cheap path.

## Anti-Patterns

- Writing a giant spec for a small task
- Letting the cheap implementer touch files outside the allowed list
- Using GPT as a full second implementer after review
- Repeating cheap-model retries more than once on the same slice
- Calling a workflow “cost optimized” when GPT still has to re-understand everything

## One-Line Rule

**Use the cheapest path that keeps GPT narrow. If GPT must fully re-think the task, use Direct GPT or split the task smaller.**
