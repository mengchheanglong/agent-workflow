# Frozen LLM Behavioral Release Suites

Use when releasing a prompt/skill/controller package whose behavior is stochastic but whose package identity and acceptance contract must remain auditable.

## 1. Freeze the candidate

Record before execution:

- version and sorted package-file manifest;
- aggregate hash over relative path and per-file digest;
- provider/model and relevant configuration;
- fixtures, prompts, validator, oracle version, and timeout policy;
- required repeated cases and independent-review requirement.

Hash the actual packaged bytes. For controller size limits, decode raw bytes without universal-newline normalization and record CR/LF counts. A Windows CRLF package can exceed a character budget even when `Path.read_text()` appears under it. If stable accounting requires LF, enforce zero CRLF in the package validator.

Any package change invalidates approval for the old hash. A reference/test-only edit still changes the package identity unless the package boundary explicitly excludes it.

## 2. Make test cases isolate one behavior

Define every decision-critical field that is not under test. For example, a causal-restraint case must define grain if the fixture supports both line and order grain. Otherwise a correct semantics-first hard stop conflicts with a required computation.

Before freezing, check each case for:

- explicit source, grain, metric/status rule, period, and comparison when computation is required;
- deterministic fixture landmarks for required arithmetic;
- prohibited behavior and acceptable blocker classes;
- no requirement that conflicts with the controller's own first-response gate.

A test-contract defect is not a controller defect. Repair the test, freeze a new candidate, and rerun the required evidence rather than weakening the safe gate.

## 3. Isolate the harness

Run from a dedicated evidence directory, not the user home or package root. This contains agent-generated drafts and makes cleanup auditable. Keep generated LLM outputs outside the package.

For each case:

1. launch a fresh session with the exact frozen prompt/config;
2. persist a partial manifest immediately after completion;
3. capture complete stdout, stderr, session ID, duration, exit code, and pre/post package hash;
4. scan for secret-value patterns and unexpected generated paths;
5. keep case-specific wall-clock bounds large enough for the permitted output tier.

A timeout/provider/tool failure is `INFRA_INCONCLUSIVE`, not a semantic failure or pass. Preserve partial output.

## 4. Separate oracle triage from semantic authority

Keyword/regex checks are triage. For every flag, read the raw response and classify exactly one:

- `PASS` — every material invariant holds;
- `SEMANTIC_FAIL` — behavior violates the contract;
- `ORACLE_FALSE_POSITIVE` — behavior is correct but wording differs;
- `INFRA_INCONCLUSIVE` — execution evidence is incomplete;
- `NOT_RUN` — no evidence exists.

Preserve the original automated manifest. Append adjudication; never rewrite history.

When a required computation has deterministic fixture values, include a numerical oracle as well as semantic-boundary checks. For wording predicates, accept equivalent behaviors such as explicit non-execution, non-selection, or causal non-identifiability—not one preferred phrase. Replay revised predicates against preserved flagged outputs before the next suite.

Patch runtime guidance only for a semantic defect. Patch the test contract for test ambiguity. Patch the external oracle for wording-only mismatches.

## 5. Targeted recovery

A targeted rerun may close `INFRA_INCONCLUSIVE` only when protocol permits independent case continuation and all of these remain exact:

- package hash;
- provider/model and configuration;
- prompt and fixture;
- oracle contract.

Use a new session, preserve the failed attempt, and label the rerun supplemental. Do not convert the original timeout row to PASS. If any frozen input changed, create a new candidate instead.

## 6. Independent exact-hash review

Review a clean snapshot or two-commit delta under technically enforced read-only isolation. The reviewer should independently verify:

- clean worktree and intended delta;
- exact aggregate hash and package-file count;
- raw controller size/line endings;
- deterministic validator;
- no test weakening or methodology/control regression;
- remaining organization-enforced gates.

On Windows Codex CLI, place all options before the final positional prompt. Load long prompts from a file through Git Bash and verify the startup banner's `workdir`, `sandbox`, model, and prompt. Wrong banner fields mean launch failure, not a review verdict. Capture the final message outside the reviewed repository and read it back.

## 7. Final verdicts

Keep technical qualification separate from real deployment admission:

- package verdict: e.g. `READY_FOR_CONTROLLED_ENTERPRISE_PILOT`;
- organization gate: named owners/reviewers, approved read-only access, query/export/privacy controls, metric authority, audit logging, and change management;
- production prohibition until organization controls are independently enforced.

One concise scorecard should reconcile deterministic gates, immutable automated results, semantic adjudication, targeted recovery, independent review, exact hash, and external gates.
