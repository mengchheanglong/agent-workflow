# Evidence-Gated Experiment Authority

Use this reference when a bounded experiment could unlock implementation, promotion, publication, or another costly phase. The authority must be mechanically decidable before any worker receives implementation permission.

## 1. Freeze roles and execution routes

Record exact roles and provider/model identifiers, not brand-level labels:

```text
authority owner = <human/Hermes>
control driver = <provider + model/auth route>
implementation worker = <provider + model/auth route>
final verifier = <independent actor>
prohibited routes = <explicit list>
```

If the user corrects the hierarchy, update the active spec, worker handoff, router skill, and project instructions together. Never leave an older provider/model alias in a control file.

Distinguish two different claims:

- the model used to **implement** the experiment;
- providers integrated or called by the **runtime being tested**.

A provider-backed coding worker can implement a provider-free runtime, but the evidence must state that boundary explicitly.

## 2. Freeze byte-exact vectors

Semantic identity descriptions are insufficient when hashes, IDs, deduplication, or canonicalization decide PASS.

Freeze all of:

- exact source bytes (hex is preferred);
- encoding, BOM, newline, and trailing-newline behavior;
- canonical serialization algorithm or exact serialized byte sequence;
- key order, whitespace, escaping, and number/string representation;
- padded vs unpadded base64/base64url;
- expected digest, observation ID, command ID, and request hash literals.

Mechanically recompute every literal before review. If two compliant implementations could derive different bytes, the vector is not frozen.

## 3. Define a complete mechanical oracle

A robust authority specifies:

- exact input/event identity and full submitted command body;
- exact timing target plus an explicit measured tolerance;
- exact working-set/checkpoint schemas: all keys required, types/enums, no extras, size limits;
- exact final artifact schema: required fields, types, allowed values, and additional-properties policy;
- ordered command-result semantics, including NOT_RUN behavior after an early failure;
- exact allowed network endpoints and validation before any side effect;
- static checks for provider imports, credentials, dependencies, and unapproved URLs;
- raw-content/log boundaries and byte scans;
- cleanup ordering: terminate workers/connections, scan logs, clear buffers, delete temp state, then emit evidence;
- exact source identity: the remote-equal implementation commit actually executed by the final aggregate;
- PASS, FAIL, and INCONCLUSIVE as disjoint mechanically decidable outcomes.

A list of artifact key names is not a schema. “Local network only” is not enforceable without exact endpoints and a validator. A self-reported cleanup boolean is weak unless the cleanup sequence and observed zero state are frozen.

## 4. Separate ownership

Use distinct allowlists:

- **authority/control owner:** spec, state transition, start/deadline, worker handoff, evidence, final decision;
- **implementation worker:** only new/approved implementation and test files.

The worker must not edit authority, final evidence, commits, pushes, promotion state, or its own scope. Control documents named by the plan must also appear in the authorized-file list.

## 5. Use revision-stable independent review

1. Finish one numbered authority revision.
2. Re-read the live files after interrupted tools or async work.
3. Hash the reviewed file set, wait briefly, hash again, and require equality when concurrent writers are plausible.
4. Dispatch independent review against exact paths and revision.
5. Do not modify reviewed files while review is running.
6. Any post-dispatch change invalidates the verdict: bump revision and re-review.
7. Seal only after `APPROVE`; then reconcile canonical state and preserve unrelated locks.
8. Commit/push/fetch/verify remote equality before creating immutable start/deadline.

Never treat user authorization as an implicit state-file mutation. Authorization starts the authority process; sealing and canonical state reconciliation make implementation legal.

## 6. Source and evidence sequence

A useful sequence for one final aggregate run is:

1. worker completes RED/GREEN within allowlist;
2. control runs pre-final verification;
3. independent verifier checks scope and evidence;
4. control commits and pushes exact implementation source;
5. fetch and remote equality pass with a clean worktree;
6. record that implementation commit as `sourceCommit`;
7. run the sole final aggregate on that exact commit;
8. clean worker/log/temp state;
9. write typed evidence and final decision in a later evidence commit.

This avoids claiming that an uncommitted or pre-implementation baseline was the source actually executed.

## 7. Probe cross-platform crash observability

Do not freeze a crash predicate from API naming alone. Before authority review, run a throwaway child-process probe on the actual host/runtime and record the observable `(exitCode, signal)` tuple.

For agent-process interruption experiments, prefer a parent-owned kill barrier:

1. child completes the last authorized pre-crash effect;
2. child sends an IPC barrier message using send-completion semantics;
3. child blocks before the forbidden next effect (for example, checkpoint write);
4. parent receives and validates the barrier and verifies pre-crash state;
5. parent issues the kill and records the child exit tuple;
6. tests pin that exact platform-observable tuple.

This is stronger than a child self-termination claim. For example, Windows Node may expose self-`process.kill(pid, "SIGKILL")` as a nonzero exit with no signal while parent `child.kill("SIGKILL")` is observed as `exitCode=null, signal="SIGKILL"`. Probe rather than generalize, and distinguish an agent-process kill from a database, workflow-runtime, host, or machine crash.

## Common blocking mistakes

- Composing the final evidence artifact from an inferred or renamed schema instead of the sealed all-and-only field contract.

- “Fixed sentinel” without its exact bytes.
- “Canonical JSON” without defining serialization bytes.
- Hash placeholders instead of expected literals.
- `duration >= N` when the authority claims an exact interval.
- Artifact key allowlist without required fields/types/enums.
- Environment-provided callback URI accepted without local-topology validation.
- Sentinel scan followed by retained in-memory or file logs.
- Worker handoff files omitted from the authority allowlist.
- Review performed on files that changed before the verdict returned.
- Marketing model name used where the verified provider/model ID differs.
- PASS overgeneralized into crash recovery, general exactly-once behavior, external usefulness, or product readiness.
