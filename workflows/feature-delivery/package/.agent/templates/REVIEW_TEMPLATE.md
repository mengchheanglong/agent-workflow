# Independent Review Report

## Review identity

- Review ID:
- Feature:
- Builder:
- Reviewer:
- Engine/model/session:
- Independent from Builder: YES / NO
- Read-only for product code: YES / NO
- Review date/reference:

## Frozen review scope

- Repository root:
- Base branch:
- Base commit:
- Head commit or working tree:
- Reviewed snapshot:
- Allowed paths:
- Pre-existing changes excluded:
- Diff command/source:

If scope or snapshot is unavailable or changes during review, verdict is `DO_NOT_MERGE` or the review
is marked stale.

## Pass 1 — Specification compliance

- Specification verdict: PASS / FAIL / UNVERIFIABLE

| AC | PASS / FAIL / NOT VERIFIED | Evidence | Notes |
|---|---|---|---|
| AC1 | | | |
| AC2 | | | |
| AC3 | | | |

### Scope assessment

- Missing required behavior:
- Unapproved behavior/scope creep:
- Changed paths outside allowance:
- Documentation/behavior contradictions:

## Pass 2 — Engineering quality

- Engineering-quality verdict: APPROVE / CHANGES_REQUESTED / DO_NOT_MERGE

| Dimension | PASS / FINDING / NOT APPLICABLE | Evidence/notes |
|---|---|---|
| Logic and edge cases | | |
| Authorization/security | | |
| Data/migrations/concurrency | | |
| Input/error/failure behavior | | |
| Privacy/secrets/logging | | |
| API/backward compatibility | | |
| Tests and false-confidence risk | | |
| Configuration/operations/docs | | |
| Maintainability/conventions | | |
| Unrelated/pre-existing changes | | |

## Specialist lenses

- Required lenses:
- Results:

## Findings

### FINDING-001

- Severity: BLOCKER / MAJOR / MINOR / NIT
- Origin: INTRODUCED / PRE_EXISTING / UNCLEAR
- Acceptance criterion/invariant:
- Area/file:
- Evidence:
- Failure scenario and impact:
- Required correction or proof:
- Status: OPEN / FIXED / ACCEPTED / REJECTED_WITH_EVIDENCE

## Validation-evidence assessment

| Command | Exit/result | After last edit? | Reviewer assessment |
|---|---:|---:|---|
| | | | |

- Test selection/skips/warnings checked:
- Missing or stale evidence:

## Finding counts

- Open BLOCKER: 0
- Open MAJOR: 0
- Open MINOR: 0
- Open NIT: 0
- Pre-existing observations: 0

## Residual risks and accepted MINOR items

For each accepted item record finding ID, owner/approver, rationale, and follow-up if any.

-

## Human checkpoint

- REQUIRED / NOT REQUIRED
- Reason:
- Snapshot approval must name:

## Verdict

`APPROVE` / `CHANGES_REQUESTED` / `DO_NOT_MERGE`

Overall `APPROVE` requires specification `PASS` and engineering-quality `APPROVE`. Only that
combination for the current snapshot may permit shipping.
