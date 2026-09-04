# Bounded Conformance Evidence Workflow

Use for time-boxed implementation gates with frozen contracts, exact conformance vectors, external runtime evidence, and a hard source-size budget.

## Freeze before production

Record and push:

- authoritative contracts and frozen vectors;
- original start time and hard deadline;
- counted production paths and hard cap;
- forbidden paths/dependencies/schema changes;
- exact focused, aggregate, static, privacy, and line-count commands.

If review changes executable scope, create a dated amendment with current content hashes. Keep the original clock. Historical amendments remain evidence; the latest reviewed hashes govern execution.

## One-dimensional slices

For each boundary/error dimension:

1. Add one end-to-end test only.
2. Run it and capture the exact wrong public and persisted result.
3. Also prove negative effects: no sensitive values/paths/IDs in errors, no downstream runtime step or journal entry, no receipt/history/state transition.
4. Implement only that dimension; do not pre-implement adjacent mappings.
5. Run focused GREEN, unchanged neighboring vectors, full aggregate, static gates, frozen/forbidden-path diff, and exact counted-line script.
6. Use REFACTOR only after GREEN to reclaim line budget without behavior changes.
7. Stage only the slice, scan added lines, obtain independent review of the staged diff, commit/push, and verify local HEAD equals remote.

After the first repeated end-to-end case is green, extract a shared test helper, first prove the old case still passes, then add the next RED. This keeps each dimension explicit without duplicating large runtime setup.

## Concurrency proof

Do not equate “two callers” or generic lock waiters with concurrent canonical transactions. A deterministic database proof should:

- establish each serializable snapshot before waiting;
- place the proof barrier before any existing command/resource lock that would serialize contenders;
- identify the parent lock by known PID;
- match child lock rows on exact `(database,classid,objid,objsubid)`, expected mode, and `granted=false`;
- use compatible shared child locks so parent release permits concurrent progress;
- apply a snapshot barrier only on attempt 1 when retries must run normal canonical logic;
- release the parent lock in `finally` and prove zero residual locks/writes.

## Stop and freshness rules

- A verdict applies only to the hashes/diff the reviewer saw.
- Classify late findings as current, stale/already fixed, or newly exposed.
- After three broad cycles, allow at most one narrowly constrained micro-review for exact mechanical corrections; do not reopen settled scope.
- A RED-only commit is acceptable only when the governing plan explicitly authorizes a scope/evidence checkpoint.
- Never claim promotion merely because tests are green; promotion requires every frozen vector, invariant, privacy assertion, budget, and deadline gate.
