# Corrective Reopening After a Bounded Experiment Fails

Use after a frozen benchmark was incorrectly marked passed and its original deadline has elapsed.

## Preserve history before fixing code

1. Record the precommitted incomplete-at-bound outcome. Do not reset the old clock or rewrite/delete the false-pass artifact.
2. Add a newer correction artifact that explicitly supersedes decision authority while preserving historical evidence.
3. Downgrade adjacent gates that depended on the invalid pass (for example, consumer gates) to candidate-only.
4. Synchronize implementation README/AGENTS, artifact index, Mission Control, `.active` state, and root routing before reopening executable work.
5. Keep still-valid lower gates explicit; a failed actor layer does not invalidate an independently proven foundation.

## Reopen under a new experiment identity

A correction needs a new name, preflight, plan, approval, immutable start artifact, clock, decisions, and final artifact. It cannot retroactively change the old outcome.

Required order:

```text
old bound correction
→ corrective preflight/plan review
→ planning commit + push + fetched equality
→ separate Mission Control approval commit
→ immutable corrective start artifact + push
→ focused RED
→ independent RED review + commit/push/equality
→ minimal GREEN
→ focused GREEN review + commit/push/equality
→ measurements and aggregate evidence
→ independent security/spec review
→ independent final review
→ conditional decision commit/push/fetch/equality
```

Do not start executable work merely because the user said “proceed” if the frozen governance requires separate approval and a new start artifact. The user instruction authorizes progress through the gates, not bypassing them.

## Resolve contradictory privacy requirements honestly

If an old vector simultaneously requires a parent to supply a private observation and forbids that observation from crossing any child channel, do not hide the contradiction behind output-only tests.

For a narrow synthetic recomputation proof, a defensible correction is:

- parent and child independently import one immutable test-only fixture;
- parent launches the child and sends zero inbound IPC;
- child gets an explicitly empty environment and non-semantic runner argv;
- child has a fixed data-free fail-closed path if any inbound message arrives;
- child emits exactly one sanitized proposal message;
- actual `ChildProcess.spawnargs` are inspected;
- stdout/stderr are rechecked after the child `close` event, not merely `exit`;
- claims are narrowed to process-independent recomputation for that fixture—not observation reacquisition or autonomous recovery.

Run a non-modifying platform spike before freezing an unusual launch constraint such as `env: {}`.

### Child-process evidence implementation traps

- Keep the shared child fixture self-contained: direct immutable synthetic literals plus domain types only. Do not transitively import database helpers, clients, configuration, environment readers, or network code merely to reuse constants.
- A zero-message counter must be paired with a static absence check for parent `child.send`/equivalent paths; a hard-coded zero alone is not persuasive runtime evidence.
- Derive the environment-key count from the exact object supplied to `fork`, and pass an explicit empty object rather than inherited `process.env`.
- Bound stdout/stderr by **total bytes across chunks**. For each chunk, compute `remaining = cap - capturedBytes` and store only `chunk.subarray(0, remaining)`. Per-chunk slicing to the full cap can exceed the cap after multiple chunks; string-length caps are not byte caps.
- Await the child `close` event before final stdout/stderr assertions. A helper may retain an old “waitForExit” name only if its implementation and callers demonstrably await `close`; prefer accurate naming when scope permits.
- Count untracked fixture files separately before staging, because `git diff` omits them. Recompute the additive cap after staging the exact allowlist.
- Test-runner soft assertions may report several assertion instances when the same mismatch classes are checked across repeated children and post-close rechecks. Report both the number of failing test vectors and the distinct mismatch classes; do not conflate them.

## Planning-file validation traps

`git diff` does not include ordinary untracked files. A green `git diff --check -- new-file` may have checked nothing.

For newly created planning files:

1. run a direct trailing-whitespace validator;
2. inspect scoped `git status --short --untracked-files=all`;
3. stage exact paths;
4. run `git diff --cached --check`;
5. verify exact staged names;
6. unstage only if another checkpoint must be committed first.

Never infer allowed scope from an empty unstaged diff.

## Cap every newly allowed file

If a new fixture/helper is optional in the plan, include it in:

- the changed-file allowlist;
- the additive line-count command;
- static type/lint coverage;
- privacy scans.

Otherwise an “optional helper” becomes an uncapped escape hatch.

## Exact test inventory proof

Substring counts do not prove frozen test names. Use the test runner’s JSON output and compare the exact unique title set:

- exact total count;
- no duplicate titles;
- exact set equality with all frozen titles;
- every status passed.

A statement such as “six T4R tests” is wrong when one preserved integration title intentionally lacks that prefix. Prefer “six frozen integration titles.”

## Metrics contract authority before implementation

Before writing a metrics runner, mechanically reconcile every authoritative planning surface: preflight schema, implementation plan, package command, file allowlist, sample names/counts, booleans, limitations, cleanup keys, and validator token rules. Do not translate the contract into a simplified handoff from memory. If documents disagree, stop and resolve the authority order before executing a benchmark; a valid-looking artifact under the wrong schema is rejected evidence.

Treat the frozen validator as executable specification. Derive serializer keys and exact limitations from it, then run the validator against a synthetic shape before the first authoritative measurement. In particular:

- preserve required marker fields such as `equal: true` and `distinctWorkflowIds: true`;
- distinguish harness-inclusive durable vectors from pure deterministic timing;
- use the exact runtime-version key names and package script promised by the preflight;
- never introduce a schema key containing a token the same frozen validator forbids;
- do not rerun an authoritative measurement merely to debug schema mechanics—validate schema and marker plumbing first.

When the contract requires reuse of focused verified vectors, do not copy their durable semantics into the metrics script. Add opt-in fixed-prefix numeric-only instrumentation at the verified semantic boundary, execute the focused vector under a hard outer timeout, parse only the marker, discard bounded test output, and retain the original vector assertions as the correctness oracle. Any instrumentation added to a capped test file still counts against the frozen additive budget.

## Metrics export boundary

Known-sentinel searches are supplemental, not authoritative. Freeze a strict external validator that permits only:

- exact top-level and nested keys;
- numeric/boolean measurements;
- exact sample counts;
- recomputed min/median/max;
- approved short tool-version strings;
- one UTC timestamp and one commit hash;
- exact fixed limitations;
- zero cleanup and persisted-output counters.

Reject every extra key/string class. Do not scan for required schema words such as `stdout` when the approved schema itself contains `stdoutCapturedBytesPersisted`; validate that key and require its value to be zero instead.

Shell scan semantics matter: `rg` exits 0 when it finds a forbidden value and 1 when clean. Wrap it so matches fail and no matches pass.

Metrics should reuse focused verified vectors with opt-in numeric-only markers. Parse only the fixed marker, bound captured output, and never serialize raw subprocess output.

### Measurement-window and timeout review traps

For measurements labelled `harnessInclusive: false`, prepare or clone the fixture **before** starting the timer. Time only the named deterministic operation; otherwise the flag is false evidence even when the schema passes.

A hard subprocess timeout is incomplete unless every cleanup outcome is bounded and checked:

- spawn Windows `taskkill.exe` with an argument array and no shell interpolation;
- distinguish helper exit code 0, nonzero exit, spawn error, and timeout;
- if the helper times out, kill it and bound the second helper-close wait;
- attempt the direct child-kill fallback;
- require the focused test child `close` promise to settle within a bounded wait;
- require final zero evidence for actor children, workers, datasource backends, and advisory locks;
- do not coerce rejected promises into success or ignore boolean/tagged outcomes;
- collapse details only at the external fixed data-free failure boundary;
- remove both temporary and final artifacts on every partial failure.

Use fresh read-only review contexts for metrics semantics and timeout cleanup. Schema success and green vectors are insufficient when timing windows or orphan handling are wrong. When review rejects code **after** an artifact was generated, repair surgically, rerun affected static gates, regenerate the artifact from the reviewed script, and increment the successful execution count honestly. Count successful but later-rejected schema/review attempts and any frozen final-aggregate rerun; never relabel the latest run as the first accepted attempt.

After external-model review, absorb only repository-verified operational lessons into canonical guidance. Remove redundant temporary briefs instead of letting advisory narratives become competing authority.

## Avoid circular push evidence

An uncommitted final artifact cannot truthfully contain proof that its own future commit was pushed. Freeze this instead:

1. prove local/remote equality immediately before creating the decision artifact;
2. make the decision explicitly conditional on its own commit being pushed, fetched, and equal before deadline;
3. capture post-commit equality in execution evidence/final report;
4. if that final equality is missing at deadline, the pass never becomes effective and the outcome is incomplete-at-bound.

## Review-delta discipline

When a reviewer approves but suggests a cheap wording or safety correction, the reviewed diff changes. Apply the correction and obtain a focused delta review. Do not silently carry the old approval forward.
