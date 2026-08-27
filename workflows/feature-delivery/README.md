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

## Continue review fixes

Use `REVIEW_FIX_PROMPT.md`. The agent must read `.active/REVIEW.md`, fix only validated findings,
re-run fresh checks after the last edit, compute a new snapshot, and request a new independent review.

## Validate workflow state

```bash
python .agent/scripts/validate_workflow.py
```

A valid `IDLE` state confirms package structure. A valid `READY_TO_SHIP` or `SHIPPED` state also
proves the recorded gate evidence, split review verdicts, snapshot, human approval, fix-cycle
authorization, and validation invariants are coherent.

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

Review is deliberately separate from implementation:

1. **Specification compliance** — did the implementation satisfy the feature contract without scope
   creep? Verdict: `PASS`, `FAIL`, or `UNVERIFIABLE`.
2. **Engineering quality** — is it correct, safe, tested, maintainable, and operationally sound?
   Verdict: `APPROVE`, `CHANGES_REQUESTED`, or `DO_NOT_MERGE`.

Overall `APPROVE` requires specification `PASS` and engineering-quality `APPROVE` for the current
snapshot. `CHANGES_REQUESTED` always requires fix and re-review.

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
