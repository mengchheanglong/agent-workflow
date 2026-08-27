# Active Delivery State

Human-readable operational journal. `.active/STATE.json` is the machine-checkable mirror; both must
agree. Update this after every state transition, invalidating event, validation run, review, and human
approval.

## Status

IDLE

## Feature and workflow

- Feature: None
- Risk: UNASSESSED
- Workflow path: Not selected
- Fix cycles: 0 / 2 authorized
- Additional-cycle authorization: None

## Actors

- Router: None
- Researcher: None
- Architect: None
- Builder: None
- Integrator: None
- Reviewer: None
- Review independence: NOT_ESTABLISHED

## Change baseline

- Repository root: Not recorded
- Base branch: Not recorded
- Base commit: Not recorded
- Pre-existing changes: None recorded
- Allowed paths: None

## Research findings

None.

## Design summary and decisions

None. Material decisions belong in `.active/DECISIONS.md`.

## Implementation progress

None.

## Changed files and current snapshot

- Changed files: None
- Current snapshot: Not computed

## Validation evidence

No commands run.

For each command record exact command, result/exit code, relevant pass/fail/skip/warning counts, and
whether it ran after the last edit.

## Review

- Artifact: `.active/REVIEW.md`
- Reviewed snapshot: None
- Specification verdict: NOT_REVIEWED
- Engineering-quality verdict: NOT_REVIEWED
- Overall verdict: NOT_REVIEWED
- Open BLOCKER: 0
- Open MAJOR: 0
- Open MINOR: 0
- Open NIT: 0

## Human approval

- Required: UNKNOWN
- Status: NOT_REQUESTED
- Evidence/snapshot: None

## Gates

The evidence/rationale column must also be represented under `gateEvidence` in `.active/STATE.json`
when a gate is `PASS`, `FAIL`, or `NOT_REQUIRED`.

| Gate | State | Evidence/rationale |
|---|---|---|
| G0_SCOPE | NOT_RUN | |
| G1_RESEARCH | NOT_RUN | |
| G2_DESIGN | NOT_RUN | |
| G3_BUILD | NOT_RUN | |
| G4_INTEGRATION | NOT_RUN | |
| G5_VALIDATION | NOT_RUN | |
| G6_REVIEW | NOT_RUN | |
| G7_HUMAN | NOT_RUN | |
| G8_SHIP_READY | NOT_RUN | |

## Blockers, assumptions, and invalidated evidence

None.

## Ship evidence

None.

## Next action

Initialize one feature.
