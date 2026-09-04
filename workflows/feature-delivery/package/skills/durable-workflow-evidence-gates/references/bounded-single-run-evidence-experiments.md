# Bounded Single-Run Evidence Experiments

Use when an experiment has a frozen authority, immutable clock, exact command sequence, committed-source requirement, and a final aggregate that may execute only once.

## Phase separation

Keep four roles and artifacts distinct:

1. **Authority:** freeze scope, topology, oracle, command order, artifact schema, outcome vocabulary, stop rule, and forbidden follow-ons. Obtain independent approval before commit.
2. **Immutable start:** record authority revision/commit, source baseline, UTC start/deadline, provider/model routing, and locked follow-ons. Never reset the clock after an infrastructure or test failure.
3. **Implementation:** permit only the worker file allowlist. The worker may run focused RED/GREEN checks but may not commit, push, write final evidence, or run the sole aggregate.
4. **Control and close:** independently rerun gates, review final source, commit/push exact source, prove remote equality, execute the final aggregate once, validate evidence, classify, and return to hold.

A worker-reported pass is never control-lane evidence.

## Ordered gate discipline

- Run required pre-aggregate commands in the frozen order.
- Stop at the first nonzero exit; do not run later commands for convenience.
- A source repair invalidates the prior sequence. Restart the complete ordered sequence on the final tree.
- Review the final tree only after the last edit. Hash the exact review set before/after review.
- Include untracked files from `git status --porcelain` and `git ls-files --others --exclude-standard`; ordinary `git diff` omits them.
- Commit and push only after every pre-aggregate command and independent review pass.
- Fetch and require local/remote equality before the sole aggregate.
- Never run the final aggregate from an uncommitted tree, and never rerun it after a nonzero result when the authority says once.

## Technically read-only independent review

A prompt saying “do not edit” is not isolation when the reviewer shares the working tree.

Preferred patterns:

- standalone reviewer CLI with an enforced read-only sandbox;
- content-embedded review with no filesystem tools;
- isolated disposable copy/worktree.

For live-file review, hash every reviewed path before and after and fail if any hash changes. Do not fall back to a shared-filesystem write-capable leaf merely because the preferred reviewer launch failed.

## Durable runtime reset trap

Resetting canonical database tables does not reset a durable runtime’s completed workflow result. If the workflow key is derived from a frozen command ID, a later run can receive a stale completion while canonical receipt/history rows remain zero.

Before the first measured submit:

1. query runtime admin using both the exact service name and exact frozen workflow key;
2. fail closed if any same-key invocation is non-terminal;
3. purge only terminal/completed invocations for that exact service/key;
4. do not purge unrelated invocations;
5. reset canonical fixture rows only through the approved fixture helper;
6. still prove exactly one fresh receipt/history consequence after execution.

Test the query filter, terminal classification, narrow purge, and non-terminal fail-closed branch.

## Privacy evidence and disposal ordering

For a frozen raw sentinel, scan the **exact bytes including delimiters/newlines**, not a trimmed marker string. Before deleting temporary state, scan every required surface:

- checkpoint bytes;
- serialized working set;
- selected canonical rows for the exact namespace/case/command;
- captured worker stdout/stderr;
- controller/runner diagnostics;
- final artifact bytes after serialization.

Preserve only booleans/counts needed for the artifact. Emit captured diagnostics before scanning, then clear captured buffers as their final mutation. Any final status output after disposal must use a non-capturing output path; otherwise “buffer bytes after disposal = 0” is false.

Child processes should receive a minimal environment allowlist rather than the entire parent environment. Omit provider/API credential variables by construction and test that omission.

## Local topology identity

A listening port or successful TCP connection does not prove the approved service owns the endpoint. Verify process ownership and protocol/service fingerprint from the runtime/container network namespace. Treat registration failures before invocation as infrastructure evidence. Changing the frozen callback URI to bypass a collision is an authority change, not a test fix.

## Commit-before-checkpoint interruption protocol

For an agent/controller process that receives a durable commit result before writing its local checkpoint, do not infer the interruption window from source order alone. Use a parent-owned process barrier:

1. In phase A, increment adapter and submit counters at the actual call sites—not in the parent and not after the result.
2. After the durable submit returns an accepted result, send an `accepted-before-checkpoint` IPC message containing the frozen receipt fields and actual counters. Await IPC send completion.
3. Block indefinitely waiting for a continuation message that the PASS path never sends.
4. The parent receives and validates the barrier, proves both the final checkpoint and atomic-write temp sibling are absent, then issues `SIGKILL` itself.
5. Require the platform-specific external-kill shape. On Windows Node, parent-issued `child.kill("SIGKILL")` must report `{ exitCode: null, signal: "SIGKILL" }`; child self-termination is not equivalent evidence.
6. After exit, recheck both checkpoint paths, the exact completed durable invocation, canonical receipt/history counts, case version, and phase-child database connection count.

For phase-B recovery, keep database authority out of the recovery child:

1. Derive the same deterministic service/workflow key from the watched bytes and frozen observation contract.
2. Query the durable runtime for exactly one completed same-service/same-key invocation, then attach exactly once.
3. Validate the complete attached receipt with an exact key set, exact nested projection, and recomputed canonical projection digest. Selected-field equality is insufficient.
4. Report the complete validated receipt to the parent; phase B performs zero adapter calls, zero submit calls, and receives no database credentials.
5. The parent independently reads PostgreSQL, recomputes the stored projection digest, and deep-compares the complete stored+digest object with phase B's attached result.
6. Only then may phase B's seven-key privacy-safe checkpoint count as recovered. Derive duplicate/recovery consequence counts mechanically from canonical counts; never hardcode zero.

Any scan/query used to establish privacy or canonical truth must fail closed. A caught query error must become an explicit failed/dirty predicate, never an empty string that looks clean.

## Control-script identity and closeout budget

One-shot experiments often fail after the aggregate because verification wrappers guess live identities. Derive, do not guess:

- compose service/container and database names from the live compose/config authority;
- dependency baselines from the executed source commit's parent or the frozen authority commit, whichever the contract names;
- endpoint allowlists from the exact authority constants, including both base URLs and composed routes;
- changed paths from staged plus untracked-file views.

A wrapper error after a successful sole aggregate does not authorize rerunning it. Correct only the wrapper and continue artifact-only closeout from preserved output.

Reserve execution budget before command 7 for: post-run process/connection/temp verification, static proofs, artifact generation, all-only schema validation, independent evidence review, evidence commit/push/fetch, state reconciliation, and service restoration. Do not spend the final available tool calls on optional diagnostics; if closeout is interrupted, report the aggregate as a PASS candidate but the experiment as not yet sealed.

## Exact artifact contract compilation

Before writing final evidence, compile the sealed authority into an executable artifact contract. Copy—not paraphrase:

- the exact all-only top-level key list;
- field types and enum values;
- timestamp syntax and clock bounds;
- the exact ordered command array and command-object keys;
- the PASS/FAIL/INCONCLUSIVE conjunction;
- the semantic meaning of `sourceCommit`.

Reject both missing **and extra** keys. Do not invent friendlier aliases (`idleMeasuredMs` versus required `idleDurationMs`, for example), and do not substitute a human-facing classification such as `SUPPORTED` where the machine artifact requires a specific PASS enum. Human decision language and machine outcome vocabulary may coexist, but they are different layers.

`sourceCommit` is the remote-equal implementation source executed by the sole aggregate, not the later evidence or closure commit. Self-attesting fields such as `artifactSchemaValid: true` become valid only after the complete candidate artifact passes the external validator.

Cross-check each artifact value against the captured aggregate output and any required independent canonical-state query. Byte-scan both artifact and captured output for the exact sentinel. Run the all-only schema validator before asking for final review.

If the aggregate observation is complete but the JSON has wrong field names, enums, or formatting, regenerate **only the artifact** from the preserved aggregate log. Never rerun a one-attempt aggregate to repair evidence serialization.

## Host-service restoration after topology overrides

When a frozen callback port requires temporarily stopping an unrelated host service, treat restoration as a named closeout obligation rather than an informal courtesy:

1. Before the experiment, record the exact service identity, initial running/stopped state, why it owns the conflicting port, and whether stopping/starting it requires elevation.
2. Stop only the named service; never change the frozen experiment port merely to avoid the collision.
3. After evidence is sealed and experiment containers are down, restore the service to its recorded initial state.
4. If the agent lacks elevation, issue one exact administrator command to the user and keep host restoration visibly pending. Do not claim end-to-end cleanup complete merely because repository/evidence closure is complete.
5. After the elevated action, verify both service state and expected port ownership. A user saying “done” is permission to verify, not verification itself.
6. Distinguish two truths in status reporting: the research experiment may be sealed/closed while host-environment restoration is still outstanding. Do not rerun the one-shot aggregate for a restoration issue.

This avoids the common failure mode where a successful experiment leaves an unrelated audio, proxy, or development service disabled after the research state has already returned to hold.

## Closeout

The evidence artifact must distinguish:

- command not run;
- command failed;
- fact not observed;
- observed false;
- observed true.

Do not substitute plausible defaults. If source cannot be committed/remote-equal or the sole aggregate cannot execute under the frozen contract, classify according to the frozen vocabulary (usually `INCONCLUSIVE`) and return every locked follow-on to hold.
