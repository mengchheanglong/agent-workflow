# Durable cancellation evidence and runtime-semantic amendments

Use when a frozen cancellation vector conflicts with the pinned runtime’s documented state machine or supported representations.

## Diagnose before changing the vector

1. Reproduce the unchanged procedure with fresh invocation IDs and preserve canonical state/receipt evidence.
2. Separate an application bug from runtime semantics using pinned-version source and supported public APIs.
3. Inspect the exact lifecycle transition: some runtimes append a cancel signal for an active/backing-off invocation rather than marking it terminal immediately.
4. Query the exact invocation ID; never accept an older invocation, generic failure, or service-wide status.
5. Compare internal constants with supported API normalization. A runtime may define an internal symbolic code/message but expose numeric or spelling-normalized SQL/HTTP forms.

## Dated scope amendment gate

Never silently reorder a frozen procedure to make the incumbent pass. When the pinned runtime makes the original order impossible:

- record at least two unchanged failures with fresh IDs;
- record pinned source/API evidence for the incompatibility;
- obtain operator authorization to continue;
- write a dated scope review before accepting GREEN;
- amend only the impossible sequencing or representation detail;
- retain the semantic outcome, original watchdog, quiescence, reconciliation ordering, no-late-effect window, privacy rules, deadline, and line cap;
- update authoritative execution docs and hash them in the scope record;
- require independent review to classify the amendment as semantic correction rather than weakened evidence.

## Cancellation sequence for signal-consuming runtimes

A strong sequence is:

1. start a deliberately retrying invocation and capture its ID;
2. observe sanitized attempt counters and measure the watchdog from submission;
3. externally kill the endpoint at the deadline;
4. prove direct-child exit and datasource/backend quiescence;
5. call the documented cancel API for the exact invocation;
6. if cancellation appends a signal, restart/register without the failpoint so it can be consumed;
7. within the bounded window, require exact cancellation-specific SQL and public attachment results;
8. only then reconcile canonical state, receipts, and history;
9. observe the recovered endpoint for the full no-late-effect interval and reconcile again.

Do not substitute caller abort, generic `failed`, hard kill, private storage inspection, or an unbounded sleep.

## Watchdog timing proof

A green cancellation test can still violate a frozen deadline if it waits for retry evidence before arming or executing the watchdog. Reject this false-green control flow:

```text
await waitForAttempt()
await delay(max(0, deadline - elapsed))
killEndpoint()
```

If `waitForAttempt()` returns after the deadline, the endpoint is killed late and every later state assertion may still pass. Instead:

1. define the contract start event precisely (for example, submission initiation rather than response attachment);
2. arm the watchdog immediately and independently from retry/IPC observation;
3. collect attempt evidence concurrently;
4. have the watchdog initiate the external kill without waiting for evidence collection;
5. record and assert both a lower and a reasonable upper elapsed-time bound around the frozen deadline;
6. preserve separate bounds for child exit, datasource disappearance, cancellation confirmation, and the no-late-effect interval.

A `>5 attempts` assertion proves retry activity, not five-second watchdog timing. Require both.

## Representation proof

When internal and public forms differ, document the mapping from pinned source and assert the exact supported surfaces. For example, an internal `ABORTED` constant may be represented publicly as numeric code `409` and a normalized `Cancelled` message. Require both exact SQL and HTTP/attachment forms when available; do not use a broad regex that could accept unrelated failures.

## Retry/race instrumentation

Attempt IPC should contain only a fixed shape such as `{type, vector, count}`. For a concurrency vector, prove an actual later attempt (for example `count: 2`) after exact attempt-1 snapshot/lock evidence; final winner/conflict outcomes alone can be manufactured sequentially.
