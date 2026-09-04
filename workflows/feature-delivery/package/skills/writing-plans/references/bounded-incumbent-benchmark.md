# Bounded Incumbent Benchmark Preflight

Use this checklist when comparing maintained frameworks/runtimes under frozen behavioral, time, or code-size bounds. The purpose is to prevent setup friction, shifting expectations, and framework-specific adaptations from contaminating the result.

## 1. Separate preflight from implementation

Preflight may include documentation research, registry metadata lookup, remote image-manifest inspection, candidate selection, and specification writing. It must not include dependency installation, lockfile changes, image pull/start, service registration, executable candidate probes, implementation source, or candidate tests.

Freeze and commit preflight before starting the implementation clock. Define the exact action that starts the clock and create a dated start artifact immediately before it.

## 2. Preserve source hierarchy

Record:

- immutable contract/vector source;
- prior evidence and decision artifact;
- active mission/state files;
- candidate-specific supplement.

Never edit frozen expected outcomes to make an incumbent pass. If wording is temporally ambiguous, add an explicit observation protocol rather than silently replacing the expected result.

## 3. Select one candidate

Compare candidates using official current documentation against mission criteria:

- relevant guarantee;
- supported language/runtime;
- public status, recovery, cancellation, and result APIs;
- external side-effect model;
- local topology and operational components;
- privacy/durable-input behavior;
- likely fit within time and line bounds.

Select one candidate. Keep alternatives as fallbacks, not parallel implementations.

Prefer the newest version pairing explicitly covered by the vendor's compatibility matrix, not merely each package's independent `latest`. Record why a newer release was not selected when compatibility is not explicit.

## 4. Pin reproducible artifacts

Before installation, record:

- exact package versions;
- registry integrity hashes;
- exact server/container version;
- OCI index digest;
- platform-specific image manifest digest;
- host/tool versions;
- application/version marker;
- topology, ports, persistence volumes, and worker count.

Manifest lookup is preflight; pulling or starting the image starts implementation when the bound says it does.

## 5. Keep canonical authority outside transport identity

Workflow IDs, invocation keys, idempotency keys, and runtime journals deduplicate transport/execution. They do not prove semantic request equality.

For external database effects, assume the ambiguous window exists: the database can commit before the runtime records step completion. Require an application/domain idempotency receipt or conditional version committed atomically with the business mutation. Do not claim arbitrary side effects are intrinsically exactly once unless the public contract proves it.

## 6. Freeze external-crash tests

Use a surviving parent observer and one direct child process. Avoid shell/package-manager wrappers between parent and worker. Use native IPC, unique IDs, real timers, and sequential execution.

Each crash gate should combine:

- an IPC phase signal;
- an independent authoritative probe (for example database activity/state);
- external process termination;
- awaited child exit;
- bounded downstream-backend disappearance;
- post-crash state assertions;
- same-version restart/recovery;
- final duplicate/count assertions.

An IPC message alone is not proof that a transaction entered or committed.

## 7. Resolve safety/liveness ambiguity with a barrier

If a frozen vector requires prior state “after restart” while a durable runtime may immediately resume work, use a deterministic test-only recovery barrier:

1. restart the same pinned worker/service version;
2. recovered execution pauses immediately before the external side effect;
3. parent asserts prior canonical state and absence of fragments;
4. parent releases the barrier;
5. require eventual completion exactly once.

The barrier must not enter durable business input or change production semantics. It makes both safety and liveness observable without weakening either.

## 8. Precommit decision taxonomy

Freeze outcomes before execution:

- **PASS:** unchanged guarantee passes; advance only to the next named gate.
- **INCONCLUSIVE:** setup, harness, version, or configuration problem; not evidence for custom infrastructure.
- **INTRINSIC FAILURE:** unchanged boundary fails repeatedly with fresh IDs and independent evidence.
- **BOUND EXPIRED:** stop and record incomplete work; do not reset the clock or hide required lines.

An intrinsic incumbent failure does not automatically authorize a custom implementation. Require the next approved comparison or a dated missing-capability review.

## 9. Commit and synchronize in dependency order

1. Commit/push the implementation repository's preflight.
2. Capture its exact commit and preflight hash.
3. Update active state and mission-control files with that immutable reference.
4. Commit the state repository separately.
5. Leave unrelated untracked files untouched.

Before commit, verify frozen-file diff count, implementation/package/config diff count, JSON validity, authority links, static gates, and working-tree scope.

If mission control says the next phase is locked, a local approval artifact is not enough. The authoritative mission-control state must separately record approval and reference the immutable planning commit before any start artifact, executable test, or source change. Final-decision synchronization is a second, later state update; do not confuse it with pre-start authorization.

## 10. Layer evidence claims by authority

Separate claims that are easy to conflate:

1. **Representation/schema evidence:** strict parsing proves only which fields and versions a component accepts.
2. **Local consistency evidence:** comparisons among caller-supplied fields prove only that the declaration is self-consistent.
3. **Trusted provenance evidence:** identify the producer and authoritative source used to construct the benchmark input. A test-only fixture proves provenance only for that synthetic fixture, not a production observation/read service.
4. **Authoritative domain evidence:** authorization, revocation, scope, version, and canonical-state decisions belong to the canonical transaction or other named authority.

Never claim “authorized,” “permitted observation,” “knowledge confinement,” or “recovery” from strict-object rejection, matching self-declared IDs, or deterministic recomputation alone. Add an end-to-end vector that carries apparently valid but authoritatively wrong inputs through the real commit boundary and asserts exact rejection, receipts/audit, and unchanged state.

Name process-loss evidence narrowly. Recomputing the same proposal after a parent supplies the same input proves process-independent determinism; it does not prove autonomous restart, observation reacquisition, prior-submission detection, pending-work recovery, or mid-commit recovery.

## 11. Make the bounded clock mechanically unambiguous

Use one authoritative UTC timestamp written inside a separately committed start artifact. Define deadline = timestamp + bound. State explicitly that artifact writing/commit/push, executable tests, harness/source changes, debugging, measurements, reviews, implementation commits/pushes, final evidence, and final decision must all complete by that deadline. The clock never resets.

Freeze this order:

1. reviewed planning commit pushed;
2. authoritative mission-control approval committed when required;
3. start timestamp captured and start artifact written/committed/pushed (all counted);
4. only then create executable files.

Approaching the bound means record the predeclared incomplete outcome. Never drop vectors, weaken parsing, compress required review, or hide lines to finish.

## 12. Freeze aggregate and measurement verification

Preflight must name:

- exact aggregate script value and exact collected test count;
- every required test file, so a passing script cannot silently omit one;
- exact counted production paths and a reproducible line-count command;
- whether block comments are permitted by that counter;
- metrics execution command;
- hard subprocess timeout/cleanup behavior;
- raw/min/median/max schema, including singleton samples;
- static coverage for evidence scripts.

Check both the TypeScript project include and ESLint file match. Adding `scripts/**/*.ts` to only one is insufficient. Run the generated evidence command for real and scan exported evidence separately from internal synthetic inputs.

Measure the named interval, not a larger enclosing test. If cancellation confirmation is required, instrument from the public cancellation request through exact supported terminal confirmation and report any later no-effect observation window separately.

## 13. Handle runtime-semantic conflicts with dated amendments

A public cancellation or management API acknowledgement may mean “durable signal accepted,” not “terminal state reached.” If a frozen order is impossible under pinned runtime semantics:

1. run the unchanged vector repeatedly with fresh IDs;
2. inspect supported status surfaces and pinned source/docs;
3. record exact failures and user authorization in a dated scope review;
4. amend only the impossible sequencing/representation detail;
5. preserve quiescence, terminal outcome, reconciliation, and no-late-effect requirements;
6. require exact runtime-specific terminal evidence rather than generic failure.

Do not silently rewrite the test. The amendment must preserve the original clock and outcome, and independent review must explicitly judge that it is a semantic correction rather than a weakened vector.