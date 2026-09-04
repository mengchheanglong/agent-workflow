# Frozen Conformance Benchmark Execution

Use this reference for time-boxed incumbent evaluations with frozen vectors, strict line/time caps, fault injection, and a stop rule that may reject the incumbent.

## Slice order

1. Freeze expected outcomes, topology, versions, line-count rule, deadline, and failure taxonomy before setup.
2. Record a clean baseline and UTC start before installing/configuring anything counted by the benchmark.
3. Implement risk-first vertical slices:
   - deterministic fixtures/canonicalization;
   - canonical database transaction and privilege boundary;
   - incumbent adapter and ordinary concurrency;
   - external crash/recovery, retry watchdog, and privacy scans.
4. For each slice capture genuine RED, targeted GREEN, full gates, counted lines, decisive catalog/runtime evidence, limitations, and a rollback-safe commit.

## Delegated-agent containment

- Give coding agents an explicit write allowlist and forbid commits.
- Split RED-only and GREEN-only handoffs for risky integration work.
- If an agent stalls, violates scope, or exhausts quota: terminate it, inspect all changed paths, restore unauthorized edits, preserve useful allowed files, and independently rerun gates.
- Agent summaries are self-reports. Verify files, commands, process state, database state, and commits directly.
- Never reconstruct a missing RED transcript. Mark it unproven or rerun a genuine RED while the production capability is still absent.

## External fault tests

- Use a separate parent/management process and child worker; capture stdout/stderr and an explicit IPC phase protocol.
- Wait for a deterministic boundary before killing: IPC before transaction/after commit, or database activity/lock state for mid-transaction.
- On Windows, `SIGKILL` maps to process termination, but fixture reset must wait for the child's actual `exit` and database socket/lock release. Do not reject the test immediately after merely sending the kill signal.
- Distinguish caller timeout from bounded recovery: kill the worker, durably cancel via the runtime control plane, confirm terminal cancellation, restart, reconcile from the domain receipt, and observe a no-late-commit window.
- Run each crash boundary in isolation before the aggregate suite so cascading cleanup timeouts cannot obscure the real pass/fail classification.

## Alternative-incumbent start discipline

When an incumbent is rejected and the mission authorizes one bounded alternative:

1. Freeze candidate, exact package/image pins and digests, topology, unchanged vector names, time/line bounds, and decision taxonomy in a preflight document.
2. Commit and push the preflight before installing, configuring, pulling/starting, registering, probing, testing, or implementing the alternative.
3. From a clean pushed baseline, create a dated start artifact containing UTC start/deadline, preflight SHA-256, counted path, exact tests, and explicit custom-persistence prohibition.
4. Commit and push the start artifact immediately before the first counted alternative action.
5. Keep research/manifest inspection before the clock distinct from executable candidate setup after the clock.

If active routing files disagree with the decision artifact, repair Mission Control and agent-routing status in the preflight commit; do not let stale “clock running” instructions govern the next session.

## Recovery-test semantic validity

A missing-module RED is necessary but not sufficient. Before accepting a crash-recovery harness, verify that its topology actually exercises the frozen guarantee:

- submit the durable invocation exactly once before the first kill;
- capture the runtime invocation identity;
- kill only the externally managed worker/endpoint at a deterministic handler or database boundary;
- restart the same pinned worker version and let the runtime automatically redeliver/resume;
- attach to the original invocation identity after restart;
- never call a normal submit API from a “recover” mode, because manual resubmission tests domain idempotency, not durable-runtime recovery;
- place post-restart safety barriers inside the recovered handler/side-effect callback, not in parent code before submission;
- buffer IPC messages so a phase emitted immediately after socket bind is not lost while waiting for a separate readiness event;
- for mid-transaction kills, require an independent database probe such as `pg_stat_activity.wait_event='PgSleep'`, not a worker “ready” message;
- for commit-before-runtime-journal completion, signal after the database commit but before the side-effect callback returns, then kill and attach to the original invocation.

Validate every public HTTP/client shape against the pinned runtime documentation or declarations. In particular, check request-field names, where invocation IDs are returned, and exact attach/output paths; a plausible-looking management call is not evidence.

When delegated agents produce a RED harness, review the test semantics before authorizing GREEN. Agent reports that say “automatic recovery” while code performs resubmission must be rejected. On a hard benchmark clock, if an agent repeatedly reads/probes for several minutes without writing, terminate it, inspect the allowlist diff, and relaunch a narrower write-first single-agent task. Preserve genuine RED output but mark semantically invalid harness versions as rejected rather than evidence.

## Diagnose package/runtime recovery failures

When recovery fails, trace the pinned installed source in this order:

1. durable workflow/status row, recovery count, and stored error;
2. adapter checkpoint table and domain receipt/state;
3. runtime launch order;
4. datasource initialization and checkpoint lookup;
5. public initialization/recovery hooks.

Example durable class of defect: runtime recovery invokes a pending datasource step before the exported datasource provider is initialized. If the only workaround requires private registry access, SDK modification, a custom datasource, manual resubmission that bypasses automatic recovery, or changing the frozen topology, classify it as an intrinsic pinned-incumbent limitation rather than patching around the vector.

Repeat the unchanged vector with a fresh ID. Preserve source paths, stack, durable status, and the exact public-API gap as evidence.

## Late blocking reviews and scope correction

A blocking review that returns after the clock starts, after RED, or after a provisional verdict reopens the benchmark. Do not treat it as stale background trivia.

1. Freshness-check every cited finding against the current files; classify it as accepted, stale/already fixed, partially applicable, or rejected with evidence.
2. Pause production GREEN immediately and terminate/quarantine any coding agent implementing against the invalid plan. Verify that no production changes survived.
3. Create a dated scope-review artifact that records the original start/deadline, decisive RED, finding-by-finding disposition, amended authority, explicit non-authorizations, and superseding document hashes.
4. Keep the original clock, frozen fixtures, line cap, and stop taxonomy. Never reset the clock because planning was incomplete.
5. Amend every executable task, file allowlist, counted path, evidence matrix, and final scan rule affected by the review—not just the narrative preflight.
6. Run a mechanical coverage audit for required vectors/invariants, planned write scopes, counted files, exact error codes, cancellation fields, and scope-artifact hashes.
7. Require a fresh-context review of the final hashes before resuming GREEN. If files changed while that review ran, treat its result as snapshot evidence and re-review the latest unit.

### Correcting a test contract after genuine RED

A genuine RED may remain behaviorally valid while a late review shows one assertion encodes an unsafe contract—for example expecting a raw validation-library exception when durable/privacy boundaries require a fixed data-free application error.

- Amend the governing spec through the dated scope review first.
- Change only the obsolete assertion; preserve stronger assertions such as zero runtime invocation, zero receipt/history, and prior canonical state.
- Rerun the focused test and observe RED again for the same missing production behavior.
- Only then implement minimal GREEN.

This is a contract correction, not permission to weaken a failing test. Record both RED forms and why the assertion changed.

### Mechanical plan-feasibility checks

Before GREEN, verify details that prose reviews commonly miss:

- every planned production file is included in the line-count formula;
- every test file that must change is explicitly writable in its task;
- unchanged crash vectors may update transport envelopes only when failpoints, kill points, barriers, outcomes, and assertions remain frozen;
- same-key durable-runtime submissions may coalesce to one invocation, so prove overlap with two independent submitters without requiring two handler signals; require two signals only for distinct-key/two-invocation cases;
- cancellation proof names executable public introspection fields and a cancellation-specific outcome, not merely “terminal” or “completed”;
- intentional sentinel declarations in frozen docs/tests are allowlisted while production/runtime/log/evidence surfaces remain zero-match;
- raw-JSON duplicate-key rejection and already-parsed object validation are assigned to their actual ingestion boundaries.

Probe the pinned runtime’s public schema/source before freezing assertions. Record exact management response variants, status/result/failure fields, deployment/version fields, and cleanup/quiescence bounds; plausible generic status checks are not evidence.

## Honest aggregate reporting

Report isolated outcomes separately from aggregate-suite artifacts:

- `PASS`: independently reproduced targeted behavior;
- `FAIL`: unchanged vector repeatedly fails for the same intrinsic reason;
- `HARNESS ARTIFACT`: later tests timed out only because an earlier forced-kill child/socket had not finished cleanup;
- `UNPROVEN`: not run or evidence incomplete.

Never convert isolated passes to failures because of cascading hook timeouts, and never hide the decisive intrinsic failure because other vectors pass.

## Stop rule

If one mission-defining vector repeatedly fails intrinsically:

1. stop adapting expected outcomes;
2. record `INCUMBENT_REJECTED_PENDING_ALTERNATIVE` (or the project’s frozen equivalent);
3. do not authorize custom infrastructure;
4. freeze a separate bound before testing the approved alternative incumbent;
5. keep passing slices and the failing conformance harness as reusable evidence.

## Final evidence checklist

- UTC time remains within the hard deadline.
- Exact package/image versions and digest are recorded.
- Targeted passes and repeated failures are reproducible.
- Typecheck, lint, build, diff check, role/catalog proof, and line count are recorded.
- Privacy scans cover domain tables, runtime/system tables, captured logs, and configured exports; unconfigured backups/WAL/replicas remain explicit limitations.
- Final verdict distinguishes project/harness defects, setup/config errors, missing domain constraints, intrinsic incumbent limits, intrinsic database limits, and time/complexity failure.
