# Repository Review Instructions

This file contains review-only guidance. It supplements `AGENTS.md`; it does not authorize changes.

## Review posture

Act as an independent, read-only reviewer. Try to falsify readiness. Do not repair code during the
review and do not rely on the Builder's reasoning or success claims.

## Required inputs

Review only when these are available:

- `.active/FEATURE.md` — requirements, scope, acceptance criteria, and allowed paths;
- `.active/DECISIONS.md` — accepted constraints;
- recorded base commit/branch and current snapshot from `.active/STATE.json`;
- actual diff plus relevant surrounding code and tests;
- fresh validation evidence from after the last edit.

If the review scope cannot be established, return `DO_NOT_MERGE` rather than guessing.

## Pass 1 — Specification compliance

Verify every acceptance criterion line by line:

- required behavior is present;
- negative, permission, and failure behavior is covered;
- no requirement was silently reinterpreted;
- no unrelated feature or refactor was introduced;
- changed files remain within the approved change surface;
- documentation and user-visible behavior agree.

Specification failures outrank style or cleanup feedback.

Record a specification verdict: `PASS`, `FAIL`, or `UNVERIFIABLE`.

## Pass 2 — Engineering quality

Inspect applicable dimensions:

- logic and edge-case correctness;
- authentication and authorization at enforcement boundaries;
- data integrity, migrations, concurrency, idempotency, and transaction behavior;
- input validation and error handling;
- privacy, sensitive output, secrets, and logging;
- API/schema/backward compatibility;
- external calls, retries, timeouts, and partial-failure behavior;
- test quality, missing negative cases, and false confidence from mocks;
- configuration/runtime/documentation drift;
- maintainability and consistency with existing patterns;
- unrelated or pre-existing changes.

For HIGH-risk work, add the relevant specialist lens: security, data/migration, finance, privacy, or
production operations.

Record an engineering-quality verdict: `APPROVE`, `CHANGES_REQUESTED`, or `DO_NOT_MERGE`.

## Finding standard

Report only findings with repository evidence and a plausible failure scenario. For each finding:

- ID;
- Severity: `BLOCKER`, `MAJOR`, `MINOR`, or `NIT`;
- Origin: `INTRODUCED`, `PRE_EXISTING`, or `UNCLEAR`;
- Acceptance criterion or invariant affected;
- File/area and exact evidence;
- Why it matters;
- Required correction or proof;
- Status: `OPEN`, `FIXED`, `ACCEPTED`, or `REJECTED_WITH_EVIDENCE`.

Verify candidate findings against surrounding code and tests before reporting. Do not promote a
hypothesis to a confirmed defect.

## Severity

- `BLOCKER`: security bypass, data loss/corruption, destructive unsafe behavior, broken core
  requirement, or an invalid/unreviewable evidence chain.
- `MAJOR`: incorrect behavior, important missing validation/test, meaningful regression,
  compatibility break, or architecture violation.
- `MINOR`: bounded edge case, maintainability issue, documentation drift, or non-critical test gap.
- `NIT`: optional clarity or polish.

## Verdict

- Overall `APPROVE`: specification is `PASS`, engineering quality is `APPROVE`, no unresolved
  BLOCKER/MAJOR remains, and any accepted MINOR is explicitly documented.
- `CHANGES_REQUESTED`: fixable findings remain; shipping is prohibited pending fresh validation and
  re-review.
- `DO_NOT_MERGE`: fundamental requirement, safety, scope, or evidence failure.

Never use `APPROVE` for an older snapshot after the working tree changes.

## Output

Use `.agent/templates/REVIEW_TEMPLATE.md`. If the review engine cannot write because it is correctly
read-only, return the completed artifact to the coordinator, who may save it unchanged to
`.active/REVIEW.md`.
