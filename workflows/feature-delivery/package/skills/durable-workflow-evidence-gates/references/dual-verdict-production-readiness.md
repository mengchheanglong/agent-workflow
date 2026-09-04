# Dual-Verdict Production-Readiness Validation

Use this pattern when a research harness has strong local correctness evidence but the user asks whether “production can start.” Separate two questions that are often conflated.

## Freeze two verdicts

1. `DEPLOY_GO | DEPLOY_CONDITIONAL | DEPLOY_NO_GO`: can the current artifact serve real workloads now?
2. `BUILD_GO | BUILD_CONDITIONAL | BUILD_NO_GO`: is the evidence sufficient to begin one narrowly scoped production implementation?

A research harness can be technically useful while still receiving `DEPLOY_NO_GO`. Missing service/operator surfaces—authn/authz, tenant boundary, TLS/config, secrets, observability, backup/restore, migration/rollback, incident recovery, and defined SLO/load evidence—are deployment blockers, not vague future polish.

## Bound “comprehensive” before execution

Freeze:

- finite gate families and final outcome vocabulary;
- one immutable clock;
- allowed repositories/files and remediation cap;
- synthetic/real-data boundary;
- provider/network/public-action permissions;
- worker/controller/verifier roles;
- what remains outside current evidence (third-party penetration test, legal certification, internet-scale load, independent organization evidence).

Do not let “test everything” become an unbounded claim of certainty.

## External evidence is a distinct gate

Local tests, synthetic probes, operator reproductions, and AI-agent reviews cannot satisfy an external-value or independent-adoption gate. State this mechanically in the authority package. A substitute signal must be external, produced by a non-project actor, source-verifiable, and meet the separately frozen Tier-A definition.

A technically green program may therefore close `BUILD_CONDITIONAL` when exactly one external/nontechnical gate remains. Do not relabel local success as demand.

## Classify intentionally retained negative tests

A full repository suite may remain red because it intentionally preserves a rejected incumbent or negative control. Do not hide or delete those failures to make the aggregate green.

Report separately:

- selected/surviving direction aggregate;
- retained incumbent-negative tests and their sealed expected failure class;
- infrastructure-selection failures that were repaired before invocation;
- new regressions.

Require source/history evidence before treating a repeated red as an expected counterexample.

## Unknown external outcomes

For lost acknowledgements, freeze the safe invariant:

```text
external submissions = 1
physical consequences <= 1
recovery submissions = 0
status/reconciliation queries are allowed
UNKNOWN never becomes claimable solely because local TTL elapsed
```

Use distinct primary/replacement processes, parent-owned kill barriers, exact PID/signal cleanup, and a parent-owned fake authority. Include an unsafe TTL-reclaim negative control that produces a second recovery submission and—when native dedupe is absent—a second physical consequence. Count submissions separately from consequences and queries.

Safe state progression should remain explicit, e.g. `SUBMITTED_UNKNOWN -> RECONCILING -> ACCEPTED | REJECTED | MANUAL_REVIEW`. Never encode `UNKNOWN -> TTL delete -> blind resubmit` as recovery.

## Keep decision semantics separate

An execution receipt answers whether a consequence completed. A decision artifact answers who authorized/refused it, under which rule/source, which human confirmation bound to the original invocation, and which principal governed each delegation hop.

For a bounded append-only provenance spike, test:

- confirmation binding;
- agent-auth versus user-auth;
- contiguous delegation hops and explicit governing-principal policy;
- genesis/sequence/previous-ID/previous-hash adjacency;
- every historical link, missing prefix, reorder, tamper, and general cycle;
- imported artifacts must extend the existing ledger tip, not introduce a fresh genesis;
- untrusted rationale cannot mutate attested fields.

Hash chaining is structural integrity only unless an external trust anchor/signature exists. It is not authenticity against an attacker who can rewrite and recompute the whole chain.

## Review discipline

Every post-review edit invalidates approval, even a “small” repair. Rerun the exact final tree and obtain a fresh review over exact paths/hashes. Review import/attach paths separately from append/create paths; self-consistent fresh genesis and tip-only validation are common false-green gaps.

Use a two-pass closeout when the repository must record the closure review without circularly claiming that the reviewer reviewed its own verdict:

1. Stage the complete final evidence/routing diff with closure fields explicitly `PENDING`.
2. Run closure review 1 read-only over that exact staged diff.
3. If approved, record the compact verdict in a separate closure artifact and change only the pending fields to `APPROVE`.
4. Restage, validate JSON/drift/diff checks, and hash the exact final allowlist.
5. Run closure review 2 over that exact final tree.
6. Make no content edits after review 2; only commit, push, fetch, and equality checks are allowed.

The closure artifact should say that review 2 is required before commit; it need not claim that review 2 reviewed its own capture. Preserve the actual review-2 output externally as execution evidence.

If an execution/tool limit interrupts the program, issue an explicitly interim verdict and list unrun gates. Never present partial PRV output as a completed production decision.

## Dependency and license evidence

A failed package-manager audit transport is not a clean dependency audit. Record the transport failure, then query the resolved production package names/versions against another current advisory source such as OSV. Preserve the package count, finding count, query source, and any unavailable secondary source separately. Inventory license groups from the resolved dependency graph; do not infer legal approval from permissive labels.

## Operability and data-lifecycle exercises

For a research harness, run concrete disposable exercises rather than merely checking that scripts exist:

- detached clean checkout at the remote-equal baseline;
- frozen install plus static gates and provider-free unit pack;
- topology doctor and reference consumer from that checkout;
- empty-database migration twice;
- transactional migration rollback proving zero residual schema;
- synthetic canonical seed, backup, restore into a second database, and deterministic row-snapshot comparison;
- graceful database/runtime restart followed by readiness, route-identity, and real commit smoke;
- cleanup of disposable databases and worktrees after evidence is sealed.

On Windows, create the worktree from an existing directory, then invoke package commands with explicit `--dir`; a process cannot start with a workdir that does not exist yet.

These exercises do not substitute for production migration-down strategy, WAL/retention policy, incident recovery, independent consumer ownership, or representative load/SLO evidence.

## Preserve sealed historical artifacts

Measurement commands may overwrite tracked dated metric files that are already sealed historical evidence. Before restoring those tracked paths, copy the fresh outputs into experiment-specific evidence storage and record their hashes. Summarize the fresh measurements in a new closeout artifact, then restore the historical tracked files before staging. Never silently commit a new run over a sealed historical path.
