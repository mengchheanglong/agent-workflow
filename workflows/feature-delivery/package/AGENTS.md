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

## Available skills

All skills live under `skills/` relative to this workflow's `package/` directory:

| Skill | When to use |
|-------|-------------|
| `test-driven-development` | Build with tests — RED → GREEN → REFACTOR |
| `github-code-review` | Review PRs: diffs, inline comments |
| `requesting-code-review` | Pre-commit review: security scan, quality gates, auto-fix |
| `github-pr-workflow` | GitHub PR lifecycle: branch, commit, open, CI, merge |
| `github-repo-management` | Clone/create/fork repos; manage remotes, releases |
| `github-auth` | GitHub auth setup: HTTPS tokens, SSH keys, gh CLI login |
| `systematic-debugging` | 4-phase root cause debugging |
| `spec-driven-development` | Write specification before any code |
| `incremental-implementation` | Build in thin vertical slices |
| `doubt-driven-development` | Adversarial fresh-context review for non-trivial decisions |
| `simplify-code` | Parallel cleanup of recent code changes |
| `context-engineering` | Curate what the agent sees |
| `cost-aware-execution-router` | Choose cheapest effective execution path |
| `cost-control-agent-workflow` | Cost-optimized workflow with implementation worker |
| `durable-workflow-evidence-gates` | Evidence-gated TDD and pre-commit verification |
| `subagent-driven-development` | Execute plans via delegate_task subagents |
| `writing-plans` | Write implementation plans |
| `implementation-reconciliation` | Reconcile code against approved architecture spec |
| `code-traced-qa` | QA traces prototype source |
| `dogfood` | Exploratory QA of web apps |
| `web-form-flow-debugging` | Debug and verify web form flows |
| `web-app-route-testing` | Batch HTTP route testing for web apps |
| `stateful-web-admin-qa` | Stateful web/admin QA and mutation verification |
| `authenticated-web-smoke` | Authenticated browser smoke tests |
| `document-to-action-items` | Extract cited obligations, deadlines, tasks from documents |
| `stakeholder-product-requirements` | Stakeholder PRDs from context and decisions |
| `project-second-brain` | Design and maintain file-first AI second brains |
| `skill-router` | Route ambiguous requests to the best skill |

## Skill routing

Use `skill-router` to determine which skill fits a request. For ambiguous requests, run:

```bash
python skills/skill-router/scripts/route_skills.py "<request>"
```

Then load the top-ranked skill with its full `SKILL.md` before acting.

### Fast routes (common patterns)

| Request pattern | Skill |
|-----------------|-------|
| "Build with tests" / "TDD" | `test-driven-development` |
| "Review this PR" / "code review" | `github-code-review` or `requesting-code-review` |
| "Open a PR" / "git workflow" | `github-pr-workflow` |
| "Debug this bug" / "root cause" | `systematic-debugging` |
| "Write a spec" / "specification first" | `spec-driven-development` |
| "Build in slices" / "thin vertical slices" | `incremental-implementation` |
| "Review this decision" / "challenge this" | `doubt-driven-development` |
| "Simplify this code" / "cleanup" | `simplify-code` |
| "Manage context" / "curate context" | `context-engineering` |
| "Cheapest path" / "cost aware" | `cost-aware-execution-router` |
| "Execute via subagents" | `subagent-driven-development` |
| "Write a plan" | `writing-plans` |
| "Reconcile with spec" | `implementation-reconciliation` |
| "QA this web app" / "find bugs" | `dogfood` or `code-traced-qa` |
| "Debug form flow" | `web-form-flow-debugging` |
| "Test routes" | `web-app-route-testing` |
| "Admin QA" / "stateful QA" | `stateful-web-admin-qa` |
| "Authenticated smoke test" | `authenticated-web-smoke` |
| "Extract tasks from doc" | `document-to-action-items` |
| "Stakeholder requirements" | `stakeholder-product-requirements` |
| "Second brain" / "project memory" | `project-second-brain` |

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

Prefer 3-7 acceptance criteria for normal features. Exceed that range only when distinct risk or
behavior truly requires separate proof; do not fragment prose into artificial criteria.

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

Run focused checks during implementation and fix loops. Run canonical full project gates once after
the candidate final product edit before ship readiness. A later edit invalidates the snapshot and
review, but rerun only affected focused checks plus any canonical gate the edit can affect; record a
concrete unaffected rationale for retained canonical evidence.

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
3. apply the selected MECHANICAL, TARGETED, or DEEP tier and FULL or DELTA review type;
4. inspect the tier-required surrounding code and tests rather than reviewing the patch in isolation;
5. verify candidate findings before reporting them;
6. classify severity as BLOCKER, MAJOR, MINOR, or NIT;
7. classify origin as INTRODUCED, PRE_EXISTING, or UNCLEAR;
8. cite exact evidence, failure scenario, impact, and required correction/proof;
9. write findings to `.active/REVIEW.md` and synchronize `.active/STATE.json`;
10. avoid modifying product code during the authoritative pass.

Review policy is selected at `G0_SCOPE`:

- `MECHANICAL` is LOW-only and compact;
- `TARGETED` is the MEDIUM default and covers criterion deltas, changed files, validation evidence,
  and 1-3 named risky seams;
- `DEEP` is required for HIGH or explicit escalation and performs full specification/engineering
  review.

Specialist mode is `INLINE` by default for LOW/MEDIUM, keeping UX/visual/accessibility or another
lens inside the one independent reviewer context and artifact. Use `SEPARATE` only for HIGH risk,
genuinely independent expertise, or explicit human request. `NOT_REQUIRED` needs rationale and is
forbidden for HIGH.

Default review budgets are LOW 5, MEDIUM 15, and HIGH 30 minutes unless project evidence justifies a
different positive bound. Budget exhaustion never permits approval: stop `UNVERIFIABLE` /
`CHANGES_REQUESTED` with a concrete escalation reason. Reviewer output is verdict-first and
rubric-delta based; do not repeat the full PRD/design prose.

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
acceptance criterion. The default is one broad FULL review cycle, which may yield one bounded narrow
correction. Re-run affected validation, compute a new snapshot, and obtain a focused DELTA review of
the named findings/criteria without reopening settled rubric areas.

`fixCycles` counts broad FULL reopenings only; a named DELTA correction does not increment it.
`reviewPolicy.maxBroadReviewCycles` defaults to 1. Raising it above 1 requires explicit human
override evidence in `fixCycleOverrideEvidence`. Without that authorization, a material correction
requiring another FULL review sets `BLOCKED` and requests direction.

FULL review is required for requirement changes, scope expansion, shared contracts,
auth/security/data/migration/lifecycle behavior, new dependencies, broad refactors, or ambiguous
evidence. DELTA is allowed only for named accepted findings or human-requested polish with unchanged
requirements/contracts, approved files, a narrow diff, explicit affected criteria/invariants, and a
named reusable base snapshot.

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

- any product-code, test, configuration, dependency, migration, or generated-artifact edit, which
  always invalidates the snapshot/review and invalidates only validation gates it can affect;
- base branch or commit change;
- scope, acceptance-criterion, risk, or material-decision change;
- stale or mismatched snapshot;
- new BLOCKER or MAJOR finding.

Invalidate downstream gates immediately and return to the earliest affected stage.

For routed user-visible UI, browser acceptance remains required. LOW/MEDIUM visual and accessibility
critique is INLINE by default. Human visual feedback after review uses focused browser/visual DELTA
review and affected checks unless it changes requirements or scope.

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
