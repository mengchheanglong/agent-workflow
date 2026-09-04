# Local synthetic durability measurement harnesses

Use when a durable-workflow benchmark requires bounded local measurements after correctness evidence is GREEN.

## Measurement contract

- Measurements are local synthetic observations, never production SLOs or capacity claims.
- Record raw samples and deterministic min/median/max summaries.
- Label harness-inclusive timings honestly. Recovery-vector and cancellation-vector durations often include process startup, registration, fixture reset, and test-runner overhead.
- Represent unsupported concepts explicitly (for example, `NOT_APPLICABLE_NO_EVENT_REPLAY`) instead of inventing throughput.
- A configured and asserted observation interval may be recorded as such, but must not be mislabeled as independently measured runtime latency.

## Recommended sample classes

1. Endpoint process spawn to the real ready signal, with multiple samples.
2. Canonical database commit latency using fixture reset and fresh command IDs.
3. One bounded completion sample per frozen crash/recovery vector.
4. Cancellation-vector completion or cancellation-confirmation timing, with the included phases named precisely.
5. The asserted post-cancellation no-late-effect window.

Every reported numeric measurement—including a one-sample V4 recovery result or fixed evidence window—uses the same `rawMs` plus `minMs`/`medianMs`/`maxMs` shape. A scalar singleton is a schema gap, not a harmless shorthand.

Do not label the elapsed duration of an entire cancellation test as `cancellationConfirmation`. A full test may include setup, the watchdog interval, endpoint restart, and the later no-late-effect observation. If exact confirmation latency is required, instrument the verified test at the semantic boundaries: start immediately before the public cancellation request and stop only after all required terminal SQL and public attachment assertions pass, but before the post-cancellation observation. An opt-in numeric-only marker is a practical bridge to the metrics process; parse only the marker and never export captured test output.

## Safe execution pattern

- Reuse the verified focused vectors rather than reimplementing crash/cancellation semantics in the metrics script. The focused test remains the correctness oracle; opt-in instrumentation should emit only one fixed-prefix numeric marker at the frozen semantic boundary.
- Validate marker parsing, exact artifact keys, limitation strings, validator token compatibility, and package-command wiring before the first authoritative run. A benchmark rerun caused only by a schema/key mistake must be reported honestly and never hidden as “debugging.”
- For Node-based projects, invoke a known JavaScript module entry with `process.execPath` when possible. This avoids platform-specific command-wrapper and shell behavior while keeping arguments explicit.
- Give every subprocess an outer hard timeout in addition to test-level timeouts. On timeout, terminate the child, wait for its `close`, then reject; do not reject first and leave delayed cleanup running. Put kill/wait in `finally` so proposal timeout, marker parse failure, or pre-close assertion failure cannot orphan the child.
- Bound captured stdout and stderr with one **combined byte counter** when the contract specifies a total cap. Per-stream or per-chunk caps can silently double or exceed the budget. Capture only what is needed for a fixed numeric marker, and never serialize raw subprocess output.
- Sanitize unexpected exceptions before they can reach stderr or the artifact. The top-level failure path should emit one fixed data-free code and delete/refuse any partial artifact.
- Reject nonzero exits and do not write an artifact after a partial run.
- Always terminate spawned endpoint children in `finally` and close database pools.
- Do not stop or recreate shared benchmark containers as routine measurement cleanup. If cleanup is required, preserve named volumes and verify runtime identity before later tests.

## Export boundary

The measurement implementation may use synthetic requests, hashes, payload references, credentials already required by the harness, and environment configuration internally. The exported artifact must contain only approved numeric samples, labels, timestamps, and limitations.

Scan the exported artifact separately from the implementation. Require absence of:

- request bodies and semantic request fields;
- command/request hashes and payload references;
- sentinels and derived digest representations;
- database URLs, passwords, tokens, API keys, deployment URIs, host addresses, and environment values;
- logs or raw subprocess output.

An implementation scan that flags an internal identifier such as `requestHashes` is not evidence of export leakage. Inspect the generated artifact itself, then independently review whether internal values can flow into serialization.

## Verification

1. Execute the metrics command successfully from a clean verified topology.
2. Parse the JSON with a strict parser.
3. Verify each summary against its raw samples.
4. Run the export leakage scan.
5. Run typecheck/lint/build and diff checks.
6. Review generated values for impossible zeros, missing samples, or mislabeled harness overhead.
7. Commit the executable script and its generated artifact together.
