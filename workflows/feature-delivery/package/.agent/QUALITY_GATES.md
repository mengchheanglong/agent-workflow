# Quality Gates

A gate is `PASS` only when every condition is satisfied by current evidence. Optional stages are
`NOT_REQUIRED`, never silently skipped. `FAIL` identifies a real blocker; `NOT_RUN` means no claim.

## Gate lifecycle

Each gate records:

- status: `NOT_RUN`, `PASS`, `FAIL`, or `NOT_REQUIRED`;
- owner/actor;
- evidence or rationale;
- snapshot/commit when applicable;
- timestamp/reference if the repository requires it;
- failure action and stage to resume.

For machine verification, every `PASS`, `FAIL`, or `NOT_REQUIRED` gate must have at least one matching
entry under `.active/STATE.json` `gateEvidence`. `NOT_REQUIRED` evidence is the Router's rationale.

A downstream edit or decision invalidates affected gates according to `.agent/WORKFLOW.md`.

## G0_SCOPE

- One coherent feature is identified.
- Problem, goal, in-scope, and out-of-scope behavior are explicit.
- Acceptance criteria are observable and testable, including applicable negative/failure behavior.
- Requirements-quality checklist has no unresolved material ambiguity.
- Authoritative sources and contradictions are identified.
- Repository root, base branch/commit, pre-existing changes, and allowed paths are recorded.
- Risk, roles, specialist review lenses, validation plan, and human checkpoint are decided.
- Large work is split into dependency-ordered slices without widening the feature.

Failure action: remain `SCOPING` or set `BLOCKED` for human clarification.

## G1_RESEARCH

- Relevant entry points, call paths, dependencies, and surrounding behavior were inspected.
- Existing patterns and tests were identified.
- Data, API, auth, configuration, migration, integration, and operational constraints are known where
  applicable.
- Facts cite repository evidence; hypotheses are labeled.
- Regression surface and pre-existing problems are recorded.
- Research did not mutate product code.

Failure action: remain `RESEARCH`.

## G2_DESIGN

Required when routed; otherwise record `NOT_REQUIRED` with rationale.

- Design satisfies each acceptance criterion.
- Interfaces, data flow, persistence, authorization, errors, and failure behavior are explicit.
- Backward compatibility and rollout/reversal are considered.
- Test strategy covers happy, negative, permission, and failure paths as applicable.
- Planned slices align with the feature and dependencies.
- Alternatives and material decisions are recorded.
- Cross-artifact analysis found no unresolved conflict between feature, research, design, and slices.

Failure action: return to Scope, Research, or Design—the stage that owns the contradiction.

## G3_BUILD

- Implementation matches approved scope and allowed paths.
- No unrelated refactor or formatting churn is mixed in.
- Changed behavior has RED → GREEN evidence where an automated test is feasible.
- Inputs, authorization, errors, and failure paths are handled at real boundaries.
- No debug code, bypass, weakened type/test/control, or secret remains.
- Changed files, tests, deviations, and discovered assumptions are recorded.
- Builder has not self-approved the feature.

Failure action: remain `BUILD` or return to Research/Design.

## G4_INTEGRATION

Required when routed; otherwise record `NOT_REQUIRED` with rationale.

- Producers/consumers, interfaces, types, schemas, and contracts agree.
- Authorization and business rules are consistently enforced.
- Configuration, migrations, generated artifacts, docs, and runtime behavior align.
- Errors and partial failures propagate intentionally.
- Integration-specific tests pass.
- No duplicate/contradictory implementation was introduced across workers or modules.

Failure action: narrow glue correction or return to Design/Build.

## G5_VALIDATION

- Controller verified the final tree after the last edit; worker reports were not trusted alone.
- Changed files stay within allowed paths and pre-existing user changes remain intact.
- Targeted tests pass for the actual behavior.
- Full relevant repository commands pass with exact exit codes and inspected warnings/skips.
- Manual acceptance is recorded for user-visible behavior when applicable.
- Validation entries are fresh and marked `afterLastEdit: true`.
- Current delivery snapshot was computed after validation inputs stabilized.
- Failures are fixed or the feature is blocked; none are hidden or reclassified for convenience.

Failure action: return to Build/Integrate or set `BLOCKED`.

## G6_REVIEW

- Reviewer is independent, fresh-context, and read-only for product code.
- Review scope is frozen by current snapshot and explicit baseline.
- Specification-compliance pass checked every acceptance criterion and scope boundary.
- Engineering-quality pass checked applicable correctness, security, data, compatibility, failure,
  test, configuration, and maintainability dimensions.
- Required specialist lenses were applied.
- Candidate findings were verified and classified by severity and origin.
- `.active/REVIEW.md` and machine state agree.
- Specification verdict is `PASS`.
- Engineering-quality verdict is `APPROVE`.
- Overall verdict is `APPROVE` for the current snapshot.
- No unresolved BLOCKER/MAJOR remains; accepted MINOR risk is explicit.

`CHANGES_REQUESTED` and `DO_NOT_MERGE` make this gate `FAIL`, never PASS.

Failure action: bounded Fix loop or return to the owning stage.

## G7_HUMAN

Required only when policy or Router says so; otherwise `NOT_REQUIRED`.

- Human received a concise approval packet.
- Explicit approval identifies the snapshot/commit.
- Approver/reference and attached conditions are recorded.
- Conditions are satisfied.
- No later change invalidated approval.

Failure action: remain `HUMAN_CHECKPOINT` or `BLOCKED`.

## G8_SHIP_READY

- All required prior gates are PASS or explicitly NOT_REQUIRED.
- Acceptance criteria are line-by-line verified.
- Review verdict is `APPROVE` for the current snapshot.
- Required human approval is current.
- State Markdown and JSON agree.
- No unexplained, unrelated, debug, secret, or temporary artifact remains.
- Rollback/reversal or safe handback is understood.
- `python .agent/scripts/validate_workflow.py` exits 0.

Failure action: readiness is false; return to the gate that owns the failure.

## Ship evidence

`SHIPPED` is not a quality gate. It is a factual state requiring concrete evidence such as an
approved handback, commit, pull request, merge, release, or deployment reference. `READY_TO_SHIP`
without ship evidence must not be relabeled `SHIPPED`.
