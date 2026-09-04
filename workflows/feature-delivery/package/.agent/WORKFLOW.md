# Feature Delivery Workflow

## Goal

Deliver one coherent feature through scoped requirements, evidence-based research, risk-routed
design, narrow implementation, fresh validation, independent review, and explicit handoff.

## State machine

```text
IDLE
→ SCOPING
→ RESEARCH
→ DESIGN (when required)
→ BUILD
→ INTEGRATE (when required)
→ VALIDATE
→ REVIEW
→ FIX → VALIDATE → REVIEW
→ HUMAN_CHECKPOINT (when required)
→ READY_TO_SHIP
→ SHIPPED
```

At any active stage:

- `→ BLOCKED` when required evidence or external input is unavailable;
- `→ PAUSED` only with a documented safe stop and exact resumption action;
- `→ CANCELLED` when a human ends the feature without shipping.

A small LOW-risk change may use:

```text
SCOPING → RESEARCH → BUILD → VALIDATE → REVIEW → READY_TO_SHIP
```

It still requires baseline capture, fresh evidence, independent review, and validator PASS.

## Invalidation rules

- A material requirement change invalidates Scope and every downstream gate.
- A design change invalidates Design and every downstream gate.
- Any product-code change invalidates affected validation, current snapshot, review, and readiness.
- Any change after `APPROVE` requires a new snapshot and at least a focused delta review.
- Human approval applies only to the named snapshot/commit.
- A background worker report is not evidence until the controller reads the final tree and reruns the
  required commands.

## Stage 0 — Preflight and initialize

1. Read the startup files listed in `AGENTS.md`.
2. Confirm whether `.active/` is `IDLE`, continuing, paused, blocked, or stale.
3. Inspect version-control state from the actual repository root.
4. Record base branch, base commit, pre-existing changes, and allowed change paths.
5. Refuse to overwrite or absorb unexplained pre-existing work.
6. In multi-contributor repositories, set `collaboration.mode` to `GROUP` and record the contributor
   owner, team task/issue reference, and task-owned feature branch. Omit `collaboration` (or use
   `SOLO`) for single-contributor work.
7. Initialize `.active/FEATURE.md` from the template and synchronize `.active/STATE.md` and
   `.active/STATE.json`.

Output:

- feature name and slug;
- repository/base baseline;
- collaboration owner, task, and feature branch when `GROUP`;
- pre-existing changes;
- user-visible goal;
- initial unknowns;
- status `SCOPING`.

## Stage 1 — Router / scope and clarify

Role: `.agent/roles/router.md`

The Router determines the path, not the implementation.

It must:

- split unrelated outcomes;
- define in-scope and out-of-scope behavior;
- write outcome-oriented, testable acceptance criteria;
- identify authoritative requirements and contradictions;
- resolve or block material ambiguity before design;
- classify risk `LOW`, `MEDIUM`, or `HIGH`;
- select roles, review tier, specialist mode/lenses, review budget, human approval, allowed paths,
  and validation commands;
- define dependency-ordered implementation slices when the feature is too large for one safe slice.

Treat the requirements-quality checklist in `FEATURE.md` as unit tests for the specification. The
Builder must not self-approve unresolved checklist items.

Prefer 3-7 acceptance criteria for a normal feature. Select MECHANICAL only for LOW, TARGETED by
default for MEDIUM, and DEEP for HIGH or explicit escalation. Specialist mode defaults to INLINE for
LOW/MEDIUM. Review budgets default to 5/15/30 minutes for LOW/MEDIUM/HIGH unless project evidence
requires another positive bound. `maxBroadReviewCycles` defaults to 1.

Gate: `G0_SCOPE`.

## Stage 2 — Research

Role: `.agent/roles/researcher.md`

Read the existing system before proposing change. Trace actual behavior, entry points, dependencies,
contracts, persistence, authorization, tests, configuration, and regression surface. Identify one or
more existing patterns to reuse and distinguish facts from hypotheses.

Research is read-only and does not implement the feature. Record evidence in `.active/STATE.md`.

Gate: `G1_RESEARCH`.

## Stage 3 — Architecture / design

Role: `.agent/roles/architect.md`

Required for MEDIUM/HIGH risk or changes spanning modules, persistence, permissions, contracts,
external integrations, security boundaries, finance, privacy, or architecture.

The design must define behavior, boundaries, data flow, contracts, persistence/migration impact,
authorization, failure modes, compatibility, test strategy, rollout/reversal, and rejected
alternatives. Check the design against every acceptance criterion and planned implementation slice.
Return contradictions to the stage that owns them instead of patching around them.

Material decisions go to `.active/DECISIONS.md`.

Gate: `G2_DESIGN`, or `NOT_REQUIRED` with Router rationale.

## Stage 4 — Build

Role: `.agent/roles/builder.md`

1. Re-read the feature contract, research, decisions, allowed paths, and current baseline.
2. Implement one vertical behavior slice at a time.
3. When an automated test is feasible, establish RED for the missing or broken behavior, implement
   the smallest GREEN, then refactor while green.
4. Run focused checks during implementation.
5. Record changed files, tests, deviations, and discoveries.
6. Stop and return to Research/Design if the approved contract no longer fits reality.

The Builder may self-check but may not create the authoritative review verdict.

Gate: `G3_BUILD`.

## Stage 5 — Integrate

Role: `.agent/roles/integrator.md`

Use when work crosses modules, repositories, generated contracts, migrations, configuration, or
multiple implementation workers. Verify producers/consumers, types, schemas, authorization,
errors, configuration, docs, and boundary tests agree.

The Integrator may make narrow glue corrections. Material behavior changes return to Design/Build.

Gate: `G4_INTEGRATION`, or `NOT_REQUIRED` with Router rationale.

## Stage 6 — Validate the final tree

Validation belongs to the controller/orchestrator, not only the Builder.

1. Confirm the final changed-file set is within allowed paths and pre-existing changes remain intact.
2. Read back changed boundary files and tests after the last worker/edit.
3. Run focused behavior checks throughout implementation/fix work and after the last edit.
4. Run canonical full project gates once after the candidate final product edit: tests, typecheck,
   lint/static analysis, build, migration or API/integration checks, and security checks as routed.
   After a later narrow edit, rerun a canonical gate only when that edit can affect it; otherwise
   retain its passing evidence with a concrete unaffected rationale.
5. Run browser/manual acceptance for routed user-visible UI.
6. Inspect test selection, pass/fail/skip counts, warnings, and exit codes—not only command names.
7. Record exact evidence in both state files, including at least one affected check after the last
   edit.
8. Compute the delivery snapshot:

```bash
python .agent/scripts/validate_workflow.py --snapshot
```

A failure cannot be hidden. Fix it or set `BLOCKED`.

Gate: `G5_VALIDATION`.

## Stage 7 — Independent review

Role: `.agent/roles/reviewer.md`; review-only policy: `REVIEW.md`.

Freeze the review unit using the current snapshot. Use a fresh, read-only reviewer. Native Claude
Code, Codex, or another review engine may be used, but it must receive the same contract and scope.

Review in order:

1. freeze review type, tier, budget, baseline/allowlist, pre-existing changes, and snapshot;
2. apply the selected tier to acceptance-criterion deltas, changed files, validation evidence, and
   applicable quality dimensions;
3. for TARGETED, inspect the 1-3 risky seams selected at Scope;
4. apply specialist mode in this same artifact (INLINE by default for LOW/MEDIUM);
5. record specification, engineering-quality, and overall verdicts first, followed by concise rubric
   deltas.

Tier meanings:

- MECHANICAL: LOW-only compact independent scope/evidence review.
- TARGETED: default MEDIUM review of changed criteria/files/evidence and 1-3 risky seams.
- DEEP: full specification/engineering review, required HIGH or explicit escalation.

The reviewer inspects controller evidence and reruns expensive commands only when evidence is
missing, inconsistent, stale, or suspect. Budget defaults are LOW 5, MEDIUM 15, HIGH 30 minutes. At
the bound, insufficient proof becomes `UNVERIFIABLE` / `CHANGES_REQUESTED` with an escalation reason,
never approval.

The reviewer verifies candidate issues, classifies introduced versus pre-existing findings, and
records three results: specification `PASS` / `FAIL` / `UNVERIFIABLE`, engineering-quality
`APPROVE` / `CHANGES_REQUESTED` / `DO_NOT_MERGE`, and the overall verdict.

Persist the completed artifact at `.active/REVIEW.md`; synchronize all three verdicts, reviewer
identity, open counts, and reviewed snapshot into `.active/STATE.json`.

Gate: `G6_REVIEW`. Only `APPROVE` can pass it for shipping.

## Stage 8 — Fix loop

For `CHANGES_REQUESTED`:

1. Reconcile every finding as accepted, rejected with evidence, or deferred with an explicit gate.
2. Builder fixes only accepted current findings and directly necessary regressions.
3. Classify materiality before editing. Requirement changes, scope expansion, shared contracts,
   auth/security/data/migration/lifecycle behavior, new dependencies, broad refactors, or ambiguous
   evidence require another FULL review and therefore a broad reopening.
4. For a named accepted finding or human-requested polish with unchanged requirements/contracts,
   approved files, narrow diff, and explicit affected criteria/invariants, use DELTA.
5. Re-run affected focused checks after the last edit. Rerun canonical gates only if the edit can
   affect them, then compute a new snapshot.
6. Have the same independent gate review the new snapshot read-only. DELTA inspects the correction,
   affected criteria/files/checks, and regression seams, carrying forward only conclusions the prior
   review explicitly marked reusable.

The default is one broad FULL review cycle (`maxBroadReviewCycles: 1`) plus one bounded DELTA
correction. `fixCycles` counts broad FULL reopenings only; DELTA does not increment it. Increasing the
broad-cycle allowance above 1 requires explicit human `fixCycleOverrideEvidence`. Otherwise, a
correction needing FULL sets `BLOCKED`. Status advancement cannot bypass the bound.

`DO_NOT_MERGE` returns to the owning stage or blocks the feature; it is not an invitation to patch
blindly.

In `GROUP` mode, keep fixes on the task-owned feature branch. Never reset, rewrite, or force-push a
branch other contributors may share. Independent AI review is additional evidence, not a substitute
for the repository's human PR review; the author never self-merges.

For user-visible UI, browser acceptance remains required when routed. LOW/MEDIUM visual critique is
INLINE. Human visual feedback after review uses focused visual/browser DELTA plus affected checks
unless it changes requirements or scope.

## Stage 9 — Human checkpoint

Required when `AGENTS.md` or Router says so. Present:

- feature and current snapshot/commit;
- behavior and high-risk effects;
- migrations/configuration/permission impact;
- validation evidence;
- independent verdict and accepted MINOR risks;
- rollback/reversal notes;
- exact approval requested.

Record the approver, timestamp/reference, snapshot, and conditions. No implicit approval.

Gate: `G7_HUMAN`, or `NOT_REQUIRED`.

## Stage 10 — Ready to ship

Verify every acceptance criterion, gate, review count, approval condition, state field, changed path,
and temporary artifact. Set `G8_SHIP_READY` and status `READY_TO_SHIP`, then run:

```bash
python .agent/scripts/validate_workflow.py
```

If it fails, readiness is false. Correct state/evidence or return to the owning stage.

Gate: `G8_SHIP_READY`.

## Stage 11 — Ship / close

Shipping means the repository-defined action: approved handback, commit, PR, merge, release, or
deployment. Do not invent authorization.

After the action:

1. record concrete `shipEvidence`;
2. set status `SHIPPED`;
3. run the validator again;
4. archive the completed feature/review/state if the repository keeps history;
5. reset `.active/` to `IDLE` only after preserving required durable decisions and follow-ups.

Follow-up work is a new feature; do not silently extend the shipped scope.

## Pause, block, and cancel

Every safe stop records:

- reason;
- current snapshot and dirty files;
- gates passed/invalidated;
- unresolved decisions/findings;
- exact next action and responsible actor.

`PAUSED` requires human direction or a deliberate safe handoff. `BLOCKED` names the missing evidence
or decision. `CANCELLED` records whether changes must be preserved, reverted, or handed back; agents
must not revert user work without authorization.

## Emergency rule

Urgency reduces scope, not evidence. Use the smallest safe change, focused RED/GREEN proof when
feasible, fresh final-tree validation, independent review, and an explicit follow-up for intentionally
deferred non-critical work.
