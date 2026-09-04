# Feature Delivery Workflow

A repository-local, agent-agnostic system for delivering **one feature at a time** through scoped
requirements, repository research, risk-based design, narrow implementation, fresh validation,
independent review, human approval for high-impact changes, and machine-checked readiness.

It is intentionally small: Markdown is the interface; one standard-library Python validator enforces
the critical state invariants.

## Install

Copy the contents of `package/` into your target repository root:

```text
target-repository/
├── AGENTS.md
├── REVIEW.md
├── START_FEATURE_PROMPT.md
├── REVIEW_FIX_PROMPT.md
├── .active/
│   ├── FEATURE.md
│   ├── STATE.md
│   ├── STATE.json
│   ├── DECISIONS.md
│   └── REVIEW.md
└── .agent/
    ├── WORKFLOW.md
    ├── QUALITY_GATES.md
    ├── REFERENCES.md
    ├── adapters/
    ├── roles/
    ├── templates/
    ├── scripts/validate_workflow.py
    └── tests/test_validate_workflow.py
```

If the repository already has `AGENTS.md`, `REVIEW.md`, or `.active/`, merge rules and state
surgically. Never overwrite project-specific policy or user work.

### Subdirectory install

To keep the workflow files out of the target repository's tree (for example, a git-ignored
`agent-workflow/` folder), install `package/` into that subdirectory and set
`baseline.repositoryRoot` in `.active/STATE.json` to the delivery repository root relative to the
workflow home (typically `".."`). The validator then computes the delivery snapshot against the real
repository while state and evidence stay under the workflow home. When `repositoryRoot` is unset, the
workflow home is the delivery repository (root install).

## Start one feature

1. Open `START_FEATURE_PROMPT.md`.
2. Replace the placeholder with one coherent feature request.
3. Give it to the coding agent from the target repository root.
4. The agent initializes `.active/FEATURE.md`, captures the Git/change baseline, selects the minimum
   safe workflow, and updates both human and machine state.

Recommended branch names:

```text
feature/<short-slug>
fix/<short-slug>
```

Branching, commits, pushes, and merges still follow the repository's own rules and human approval.

### Solo vs group mode

`collaboration` in `.active/STATE.json` is optional and defaults to `SOLO` (single contributor). In a
multi-contributor repository, set `collaboration.mode` to `GROUP` and record the `owner`, `taskRef`,
and `featureBranch`; the validator then requires those once scope passes. Group mode also means fixes
stay on the task-owned branch, shared branches are never rewritten or force-pushed, and independent AI
review supplements — never replaces — the repository's human PR review. It hardcodes no branch names,
so `baseBranch` remains whatever the repository uses.

## Continue review fixes

Use `REVIEW_FIX_PROMPT.md`. The agent fixes only validated findings, reruns affected checks after the
last edit, computes a new snapshot, and requests an independent DELTA review when materiality rules
permit. A narrow DELTA does not reopen the full rubric or increment `fixCycles`.

## Validate workflow state

```bash
python .agent/scripts/validate_workflow.py
```

A valid `IDLE` state confirms package structure. A valid `READY_TO_SHIP` or `SHIPPED` state also
proves schema-v2 review policy, recorded gate evidence, split review verdicts, snapshot, human
approval, broad-cycle authorization, and validation invariants are coherent.

Run validator tests:

```bash
python -B -m unittest discover -s .agent/tests -p "test_*.py" -v
```

Compute the current delivery snapshot from the recorded base commit:

```bash
python .agent/scripts/validate_workflow.py --snapshot
```

The snapshot covers tracked changes relative to `baseline.baseCommit` plus untracked files and
excludes `.active/` so recording evidence does not invalidate itself.

## Review model

Review is deliberately separate from implementation but proportional to risk:

- **MECHANICAL** - LOW-only compact scope/evidence review.
- **TARGETED** - MEDIUM default: changed criteria, changed files, validation, and 1-3 risky seams.
- **DEEP** - HIGH or explicit escalation: full specification and engineering review.

Specialist critique is INLINE in the same independent context/artifact by default for LOW/MEDIUM.
SEPARATE is reserved for HIGH, genuinely independent expertise, or explicit human request.

Default budgets are LOW 5, MEDIUM 15, and HIGH 30 minutes. The budget caps review work, not the
approval standard: insufficient proof at the limit becomes `UNVERIFIABLE` / `CHANGES_REQUESTED` with
a concrete escalation reason.

The fast path is one FULL review at the selected tier, one bounded narrow correction if needed, then
a DELTA review anchored to the prior reusable review basis. FULL review reopens only for requirement
or scope changes, shared contracts, auth/security/data/migration/lifecycle behavior, dependencies,
broad refactors, or ambiguous evidence. Raising the default one broad-cycle allowance requires
explicit human evidence.

Overall `APPROVE` still requires specification `PASS` and engineering-quality `APPROVE` for the
current snapshot, with no open BLOCKER/MAJOR. Browser acceptance remains required when routed for UI.
Human visual feedback normally receives focused browser/visual DELTA review unless it changes scope
or requirements.

During implementation/fixes, run focused checks. Run canonical full project gates once after the
candidate final product edit, then rerun only gates a later narrow edit can affect. The Reviewer
inspects fresh controller evidence and reruns expensive commands only when it is suspect or missing.

Native review systems can act as the independent engine:

- **Claude Code:** local `/code-review`, a read-only custom reviewer subagent, or managed PR review;
  repository-specific guidance can come from `REVIEW.md`.
- **Codex:** `/review` against the recorded base branch/commit or uncommitted changes; repository
  rules come from the `## Code Review Rules` section in `AGENTS.md`.
- **Other agents:** use a fresh context with read-only tools and the contract in
  `.agent/roles/reviewer.md`.

Native AI review does not replace tests, static analysis, branch protection, or human approval. Its
findings must be reconciled into `.active/REVIEW.md` and tied to the reviewed snapshot.

## State lifecycle

```text
IDLE
→ SCOPING
→ RESEARCH
→ DESIGN (when required)
→ BUILD
→ INTEGRATE (when required)
→ VALIDATE
→ REVIEW
→ FIX → VALIDATE → REVIEW (bounded)
→ HUMAN_CHECKPOINT (when required)
→ READY_TO_SHIP
→ SHIPPED
```

At any active stage the feature may become `BLOCKED`, `PAUSED`, or `CANCELLED` with a documented
reason and exact next action.

## Why these pieces exist

- `AGENTS.md` — durable policy and review rules.
- `REVIEW.md` — review-only instructions consumable by dedicated review tools.
- `.agent/WORKFLOW.md` — state machine and stage procedure.
- `.agent/QUALITY_GATES.md` — pass/fail evidence contracts.
- `.agent/roles/` — narrow role responsibilities.
- `.agent/adapters/` — optional Claude Code, Codex, and generic reviewer launch guidance.
- `.active/` — current feature contract, evidence, decisions, and review.
- `validate_workflow.py` — fail-closed readiness validation.

## Adaptation

Replace generic validation examples with the repository's real commands. Add project-specific review
rules only for durable, consequential behavior. Keep deterministic formatting and lint rules in
scripts or CI rather than bloating AI review instructions.

Do not add more roles or process layers unless a real recurring failure proves they are needed.
