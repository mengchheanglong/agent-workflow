# Repository Feature-Delivery Policy

## Mission

Ship one coherent feature at a time with explicit scope, fresh evidence, independent review, and no
unexplained change. Code is not complete merely because it exists or a command passed once.

This policy is agent-agnostic. Claude Code, Codex, or another capable engine may perform a role, but
the repository artifacts and gates remain authoritative.

## Instruction precedence

Apply instructions in this order:

1. the human's current explicit direction;
2. applicable repository `AGENTS.md` or `CLAUDE.md` rules;
3. product, architecture, security, data, and operations documentation;
4. the approved active feature contract and material decisions;
5. existing source code and tests;
6. assumptions, which must be labeled and resolved when consequential.

Never let generic workflow text override project-specific product facts. When installing this package
into a repository that already has an instruction file, merge the mandatory feature-delivery rules;
do not replace stronger or more specific project rules.

## Required startup sequence

Before editing:

1. read this file and `REVIEW.md`;
2. read `.agent/WORKFLOW.md` and `.agent/QUALITY_GATES.md`;
3. read `.active/STATE.md`, `.active/STATE.json`, `.active/FEATURE.md`,
   `.active/DECISIONS.md`, and `.active/REVIEW.md`;
4. read project-specific authority documents and nearby instructions;
5. inspect the repository baseline and pre-existing changes;
6. stop if another feature is active unless the human explicitly pauses, cancels, or replaces it.

## One-feature rule

Only one coherent feature may be active in this workflow directory.

Allowed work includes the requested behavior, directly required tests, necessary integration, and
small enabling changes without which the feature cannot work safely. Unrelated cleanup, speculative
abstractions, and adjacent feature families are forbidden. Record useful out-of-scope discoveries as
follow-ups; do not implement them silently.

## State authority

`.active/STATE.json` is the machine-checkable state. `.active/STATE.md` is the human-readable journal.
They must agree after every transition.

`.active/FEATURE.md` is the feature contract. `.active/DECISIONS.md` records material decisions.
`.active/REVIEW.md` is the latest authoritative independent review.

If these artifacts conflict, stop in `BLOCKED`, state the mismatch, and repair the records before
continuing product work. Never infer readiness from chat history alone.

## Lifecycle

Use the state machine in `.agent/WORKFLOW.md`:

```text
IDLE → SCOPING → RESEARCH → [DESIGN] → BUILD → [INTEGRATE] → VALIDATE
→ REVIEW → [FIX → VALIDATE → REVIEW] → [HUMAN_CHECKPOINT]
→ READY_TO_SHIP → SHIPPED
```

`DESIGN`, `INTEGRATE`, and `HUMAN_CHECKPOINT` may be `NOT_REQUIRED` only with recorded reasoning.
`PAUSED`, `BLOCKED`, and `CANCELLED` are explicit states, not informal descriptions.

No agent may skip directly from `BUILD` to completion.

## Roles

- **Router** — defines scope, risk, baseline, path, gates, and review lenses.
- **Researcher** — read-only repository discovery and evidence gathering.
- **Architect** — resolves material design/contract decisions when needed.
- **Builder** — implements the smallest safe vertical slices and tests.
- **Integrator** — verifies cross-boundary behavior when integration is routed in.
- **Reviewer** — independently reviews a frozen snapshot without editing product code.

One engine may perform several non-conflicting roles in sequence, but Builder and Reviewer must use
separate contexts. Record actor identity/session in `.active/STATE.json`. The Builder may not approve
its own work.

## Baseline and change ownership

Before implementation, record:

- repository root;
- base branch and immutable base commit;
- pre-existing modified and untracked files;
- allowed paths and explicit forbidden scope;
- selected validation commands.

Do not reset, overwrite, reformat, stage, commit, or otherwise absorb pre-existing user work. Review
only the active feature delta against its recorded baseline. Any required path outside the allowlist
is a scope change and must return to Router approval.

## Requirements quality

A feature contract must contain:

- problem and user outcome;
- testable acceptance criteria;
- explicit in-scope and out-of-scope boundaries;
- unhappy paths, permissions, data, compatibility, and operational constraints where relevant;
- risk classification and human-checkpoint decision;
- validation plan and definition of done.

Unresolved high-impact ambiguity blocks implementation. Do not invent UI, automation, permissions,
billing behavior, migrations, or external contracts.

## Research and design discipline

Research precedes design and build. Read the smallest high-signal set of files needed to trace
entry points, contracts, data flow, tests, configuration, and failure behavior.

Use Architecture only when the change affects structure, contracts, security boundaries, persistent
data, shared abstractions, or multiple components. Prefer the repository's existing patterns and the
smallest maintainable design.

Material discoveries during Build return the workflow to Research or Architecture. Do not redesign
silently inside implementation.

## Build and test discipline

Implement thin vertical slices. Where behavior can be tested, use RED → GREEN → REFACTOR:

1. demonstrate the missing or incorrect behavior with a focused failing test;
2. make the smallest production change that passes;
3. refactor only while evidence remains green.

If an automated test is impractical, record why and provide the strongest deterministic substitute.
Do not weaken or delete a valid test to make the implementation pass.

Any edit after validation invalidates validation evidence, the delivery snapshot, and the review
verdict. Re-run the affected checks and review the new snapshot.

## Validation evidence

A completion claim requires fresh commands run after the last product edit. Record for each command:

- exact command and working directory;
- exit code and PASS/FAIL result;
- relevant counts or assertions;
- warnings, skips, and limitations;
- confirmation that it ran after the last edit.

No fabricated output, remembered result, or agent summary is evidence. Deterministic checks belong in
scripts or CI, not in subjective review prose.

After validation, compute the delivery snapshot:

```bash
python .agent/scripts/validate_workflow.py --snapshot
```

Record it in `.active/STATE.json`. The Reviewer must review that same snapshot.

## Code Review Rules

Review is a separate, read-only gate governed by `REVIEW.md` and
`.agent/templates/REVIEW_TEMPLATE.md`.

The Reviewer must:

1. start from a fresh context independent of the Builder;
2. verify the exact base, current diff, allowed paths, and pre-existing changes;
3. perform specification compliance before engineering-quality review;
4. inspect relevant surrounding code and tests rather than reviewing the patch in isolation;
5. verify candidate findings before reporting them;
6. classify severity as BLOCKER, MAJOR, MINOR, or NIT;
7. classify origin as INTRODUCED, PRE_EXISTING, or UNCLEAR;
8. cite exact evidence, failure scenario, impact, and required correction/proof;
9. write findings to `.active/REVIEW.md` and synchronize `.active/STATE.json`;
10. avoid modifying product code during the authoritative pass.

Record specification (`PASS` / `FAIL` / `UNVERIFIABLE`) and engineering-quality
(`APPROVE` / `CHANGES_REQUESTED` / `DO_NOT_MERGE`) results separately. Overall `APPROVE` requires
specification `PASS` plus engineering-quality `APPROVE`.

Review verdicts:

| Verdict | Meaning | May ship? |
|---|---|---:|
| `APPROVE` | No unresolved BLOCKER or MAJOR; current snapshot is acceptable | Yes, after all gates |
| `CHANGES_REQUESTED` | Correctable work remains | No |
| `DO_NOT_MERGE` | Fundamental safety, scope, or design problem | No |

`APPROVE` is the only ship-capable verdict. Review comments, a neutral GitHub check, or a native tool's
PASS do not become `G6_REVIEW` until findings are reconciled into repository state.

Native Claude Code or Codex review may be used through `.agent/adapters/`, but vendor output never
replaces tests, human approval, snapshot freshness, or these verdict rules.

## Findings and fix loops

Fix findings in severity order. Make the smallest correction that addresses the cited invariant or
acceptance criterion. Re-run affected validation, compute a new snapshot, and obtain focused
re-review.

The default maximum is two broad fix/re-review cycles. If BLOCKER or MAJOR findings remain after two,
set `BLOCKED` and request human direction. Do not evade the bound by advancing the status. A human may
explicitly authorize a revised scope or additional cycle. Record that decision in
`fixCycleOverrideEvidence` and raise `maxFixCycles`; an unexplained higher limit is invalid.

## Risk and human checkpoints

Classify risk as LOW, MEDIUM, or HIGH before Build. HIGH risk includes auth/permissions, secrets,
payments/finance, destructive or irreversible operations, persistent-data migrations, privacy,
public API compatibility, production infrastructure, and safety-critical behavior.

HIGH risk requires a human checkpoint. MEDIUM risk requires one when rollback, monitoring, authority,
or user-visible behavior remains uncertain. Evidence must identify who approved what snapshot and
any conditions. Silence is not approval.

## Gate truth and invalidation

A gate is `PASS` only when its current evidence satisfies `.agent/QUALITY_GATES.md`. Optional gates
use `NOT_REQUIRED` with a reason; they are never silently skipped.

Every `PASS`, `FAIL`, or `NOT_REQUIRED` gate must have matching machine-readable `gateEvidence` in
`.active/STATE.json`.

Invalidating events include:

- any product-code, test, configuration, dependency, migration, or generated-artifact edit;
- base branch or commit change;
- scope, acceptance-criterion, risk, or material-decision change;
- stale or mismatched snapshot;
- new BLOCKER or MAJOR finding.

Invalidate downstream gates immediately and return to the earliest affected stage.

## Shipping and repository side effects

Before `READY_TO_SHIP`, run:

```bash
python .agent/scripts/validate_workflow.py
```

It must pass against the live repository state. `SHIPPED` additionally requires concrete ship
evidence such as commit, merge request, merge, release, deployment, or accepted handoff, as applicable.

Do not commit, push, merge, deploy, publish, or alter external systems unless project rules or the
human explicitly authorize that action. Never call work shipped merely because local validation
passed.

## Pause, cancel, and close

- **PAUSED** — preserve artifacts and record a concrete resume condition.
- **BLOCKED** — record blocker, owner, evidence, and next decision required.
- **CANCELLED** — record human authority and do not ship partial work.
- **SHIPPED** — record ship evidence, promote durable decisions to project documentation, archive the
  feature artifacts, then reset `.active/` to the clean IDLE templates.

Do not erase decisions or review evidence before they are archived or deliberately discarded by the
human.

## Final response contract

Report only verified facts:

- delivered behavior and explicit non-goals;
- files/change surface;
- exact validation evidence;
- review verdict and remaining accepted MINOR/NIT findings;
- human approval where required;
- ship evidence or the precise reason shipping has not occurred.

If any required evidence is missing, say the work is partial or blocked. Never substitute confidence
for proof.
