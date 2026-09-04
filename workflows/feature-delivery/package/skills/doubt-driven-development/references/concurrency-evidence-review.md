# Reviewing Concurrency Evidence

Use this when a claim depends on races, idempotency, transaction ordering, crash recovery, or watchdog cancellation.

## Ask what the barrier actually proves

Do not accept “both tasks reached a barrier” without locating it precisely.

- **Before transaction creation:** proves only handler overlap.
- **After transaction creation but before the first statement:** often proves no database snapshot; PostgreSQL establishes the snapshot on the first snapshot-taking statement.
- **After a state read in each transaction:** can prove both snapshots observed the required prior state.
- **After an existing exclusive lock:** may accidentally serialize the contenders and invalidate the race proof.

Require the barrier before any command/key/row lock that would prevent all intended contenders from reaching it.

## Account for runtime coalescing

Two callers do not always imply two handler invocations. Workflow IDs, idempotency keys, actors, or virtual-object keys may coalesce duplicate submissions.

For a same-key case:

1. use two independent submitter processes/connections;
2. block the single admitted invocation at the proof point;
3. confirm the second submission is outstanding;
4. allow both callers to share one invocation identity;
5. prove both obtain the same durable result.

Require two handler/database barriers only for a distinct-key case where two invocations should exist.

## Shared advisory barrier pattern for PostgreSQL

A reusable test-only pattern for proving two serializable snapshots observed the same version:

1. A dedicated parent connection records its PID and acquires an **exclusive session advisory lock** on a fixed test key.
2. On transaction attempt 1 only, each serializable transaction performs a non-locking state/version read and validates the expected prior value.
3. Each attempt-1 transaction requests the **shared transaction advisory lock** on the same key.
4. A separate observer locates the parent's granted `ExclusiveLock` in `pg_locks` by known PID and captures its exact advisory tuple `(database, classid, objid, objsubid)`.
5. Require each contender as a distinct PID with `mode='ShareLock'`, `granted=false`, and the identical advisory tuple. Generic `pg_stat_activity` or lock-wait counts are insufficient because they can mistake an existing command/key lock for the test barrier.
6. Parent verifies canonical state is still unchanged and all required submitters remain outstanding.
7. Parent releases its exclusive lock in `finally`.
8. Shared waiters proceed concurrently because their locks are compatible.
9. Serialization retries run **without** the snapshot failpoint, allowing the loser to observe the winner's commit and return the required stored receipt or typed version conflict.
10. Normal production locking/serialization determines the winner; verify retry count and terminal loser outcome.

The test-only branch must execute before any existing command-ID lock, receipt lookup, or row lock that would prevent all intended contenders from reaching it. This is especially important when distinct runtime workflow IDs still carry the same domain command ID.

Transaction-local failpoint configuration should end with the first transaction. Do not reapply the snapshot barrier on retries: a retry is expected to see the new version, so forcing the original-version assertion again prevents the very terminal outcome the test is meant to prove.

## Verification and cleanup

- Use independent processes/connections when the contract says so; two promises on one client are weaker evidence.
- Instrument only phase/attempt/status metadata. Do not put request bodies, hashes, payload references, or sentinels into IPC/logs.
- Validate the synchronization mechanism with a rollback-only spike before relying on it.
- Release parent locks in `finally` and verify no advisory locks, workers, or datasource backends remain.
- Distinguish cancellation acknowledgement from cancellation completion, endpoint-process death from datasource-backend disappearance, and generic terminal failure from the cancellation-specific result.
- Never treat a queue or concurrency-one configuration as proof of unqueued conflict handling.
