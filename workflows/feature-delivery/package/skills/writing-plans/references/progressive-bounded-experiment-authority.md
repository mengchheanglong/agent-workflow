# Progressive Bounded Experiment Authority

Use this reference when a larger diagnostic or benchmark has uncertain later vectors. The goal is to preserve forward movement without granting speculative authority.

## 1. Separate roadmap from executable authority

A plan may describe the larger sequence, but mark every later vector `NOT AUTHORIZED` until it has:

- exact question and claim boundary;
- exact command or harness entry point;
- fixtures and overlap/barrier rules;
- trial count and timeout;
- pass, behavioral-fail, setup-inconclusive, privacy-stop, and bound-expiry oracles;
- cleanup trap;
- evidence fields;
- independent review gate.

Authorize only the first slice whose full matrix is known.

## 2. Slice-specific outcome vocabulary

Do not reuse a broad experiment outcome for a prerequisite slice. Example classes:

```text
BASELINE_PASSES
BASELINE_FAILS
INCONCLUSIVE
INCOMPLETE_AT_BOUND
```

A prerequisite/import/runner failure is `INCONCLUSIVE`, not evidence that the target behavior failed. A passing source/unit regression is not a live black-box reproduction.

## 3. Immutable clock sequence

1. Commit reviewed planning authority.
2. Capture one UTC start timestamp first.
3. The clock is active immediately.
4. Recollect authoritative version/source/repository facts under the clock.
5. Write and commit the start artifact.
6. Never recapture the timestamp after setup or commit delay.
7. Execute only the frozen invocation.

Planning-time observations may guide the spec but are provisional.

## 4. Prerequisite policy

Freeze before execution:

- exact executable/interpreter;
- exact dependency policy;
- whether setup repair is allowed;
- fixed failure category if the runner cannot launch/import;
- whether a dated amendment may authorize repair.

Never silently install, switch interpreters, change flags, or broaden tests to force a result.

## 5. Dirty-checkout integrity

If unrelated generated/untracked files already exist:

- record status-entry count and status-code counts;
- hash NUL-delimited `git status --porcelain=v1 -z` output;
- prove named target files are clean;
- avoid persisting the full unrelated path list;
- recompute the same count/digest after execution.

This proves non-modification without requiring destructive cleanup.

## 6. Evidence separation

Keep three layers distinct:

1. **Raw execution capture** in a bounded temporary file.
2. **Sanitization/formatting** after execution.
3. **Committed evidence** containing only approved fields.

If formatting fails, preserve and classify the already-captured command result. Do not rerun merely because presentation failed.

## 7. Review sequence

- Planning review before authority commit.
- Evidence review after execution and cleanup.
- Final reconciliation review after drafting the outcome and state changes.
- Any substantive repair after `REJECT` requires a fresh review of the repaired files.
- Reviewers are read-only and did not author or execute the slice.

Use an exact staged-path allowlist before each commit.

## 8. Required artifacts

```text
PREFLIGHT.md
PLAN.md
artifacts/YYYY-MM-DD-<slice>-start.md
artifacts/YYYY-MM-DD-<slice>-evidence.md
artifacts/YYYY-MM-DD-<slice>-final.md
```

The final artifact should include:

- immutable timing and elapsed duration;
- planning/start/evidence commit chain;
- exact fixed outcome;
- decisive sanitized output;
- cleanup/source-integrity proof;
- independent review verdict;
- unproven boundaries;
- explicit locks and no-auto-advance rule.

## 9. Reconciliation checklist

After the outcome:

- update canonical machine-readable state;
- update current/next human views;
- append the decision log;
- update mission status and task status;
- return mode to hold unless separately authorized;
- keep all later gates explicitly locked;
- record the final decision commit in a mechanical follow-up if the artifact cannot name its own commit;
- update workspace-level routers outside the repository, or report them as the only stale pointers before stopping.

## 10. Anti-drift rule

A result can close only the slice it actually ran. It cannot automatically authorize:

- the next diagnostic vector;
- production implementation;
- durable infrastructure;
- persistence or memory layers;
- consumer promotion;
- demand or safety claims.
