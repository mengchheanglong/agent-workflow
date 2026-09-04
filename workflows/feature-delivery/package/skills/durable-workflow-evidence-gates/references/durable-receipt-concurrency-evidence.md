# Durable receipt authority and snapshot-barrier evidence

Use this reference for idempotency tests where a durable workflow runtime fronts a canonical serializable database.

## Attempt-1 snapshot barrier

- A dedicated parent database session records its PID and holds an exclusive advisory lock on a fixed test key.
- On serializable attempt 1 only, set a transaction-local test failpoint.
- Inside the canonical function, before command-ID locks or receipt lookup, perform a non-locking case-version read and require the expected version.
- Then request the compatible shared advisory lock on the parent key.
- Retries must bypass the barrier so a loser can read the stored receipt or return the real expected-version conflict.
- Release the parent lock in `finally`.

## Exact concurrency proof

Capture the parent’s complete advisory identity `(database, classid, objid, objsubid)` from `pg_locks`. Child evidence must match that exact tuple, use `ShareLock`, have `granted=false`, and use distinct backend PIDs where two transactions are required. Generic connection counts, `wait_event_type='Lock'`, or unmatched advisory rows can accidentally count the command-ID lock and are insufficient.

Before release, require canonical state to remain at the expected version and every submitter to remain outstanding.

- **Same workflow key:** two independent child processes, one supported runtime invocation, and one exact datasource waiter are valid because the runtime may coalesce submissions.
- **Distinct workflow keys:** retain the same semantic command ID and request hash, but require two distinct invocation IDs and two exact datasource waiter PIDs.

## Stored receipt authority

Do not prove authority by comparing endpoint responses only to each other. Read the canonical receipt directly and compare attached runtime results to it. If the endpoint adds a deterministic derived field not stored in the receipt (for example a projection digest), exclude only that named field from stored-result equality and verify it independently.

For different-hash reuse, distinguish:

- same-key caller/runtime replay handling; and
- a fresh workflow key that reaches the database and leaves a mismatch audit while preserving the original receipt.

## Supported purge and restart

1. Capture the invocation ID and attach until completion.
2. Query both supported invocation and journal tables directly by that ID.
3. Call the supported purge endpoint.
4. Poll both tables directly by captured ID until each is absent; a journal query through a now-missing invocation subquery is vacuous.
5. Prove the old endpoint exited and datasource backends disappeared.
6. Start a new endpoint and verify ready from the runtime’s network namespace.
7. With no fixture reset, replay the same command under a fresh workflow key and compare it to the stored database receipt; then submit a different hash under another fresh key and require canonical reuse rejection.

Never delete runtime volumes or inspect private storage for this proof.

## Submitter privacy and cleanup

Child IPC should contain only a submitted invocation ID and terminal status/code. Do not send request bodies, payload references, hashes, raw results, raw errors, or sentinels. Ignore or capture child stdout/stderr without exposing request data. After every run, require zero submitter/endpoint children, datasource backends, barrier sessions, and advisory locks.

## Verification traps

- Revalidate the container-to-host endpoint identity before long runs.
- Inspect selected and skipped test names after regex-filtered runs; execute any missed supporting assertion explicitly.
- Compare the final changed-file set to an exact allowlist.
- Recount all production paths under the hard cap after the slice.
