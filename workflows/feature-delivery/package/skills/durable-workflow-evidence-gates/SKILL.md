---
name: durable-workflow-evidence-gates
description: Evidence-gated TDD and pre-commit verification for durable workflow boundaries backed by journals and canonical databases.
version: 1.8.1
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [tdd, durable-workflows, concurrency, evidence, privacy, code-review]
---

# Durable Workflow Evidence Gates

Use this skill when implementing or reviewing request boundaries, version compatibility, recovery, idempotency, cancellation, or concurrency for a durable workflow runtime backed by a canonical database.

## Core rule

A response assertion is not enough. Prove the outcome at every relevant layer: caller, runtime invocation, durable journal, canonical receipt/history, and canonical state.

## Workflow

1. Freeze the authoritative vector, invariant, write scope, line budget, clock/deadline, artifact schema, validator, and package command. Reconcile preflight and plan mechanically before implementation; treat the frozen validator as executable specification.
2. Establish one focused RED before production changes. Capture the exact wrong code/type and downstream effects.
3. Implement only the smallest GREEN for that behavior.
4. After the implementation worker exits, snapshot the final tree and read back changed test/fixture/runtime boundaries before trusting its report; compare interface arity/order, namespace filters, return shapes, and cleanup scope.
5. Run focused tests, surviving-direction aggregate, typecheck, lint, build, diff checks, changed-file allowlist, and exact line count **yourself on the final tree after the last edit**.
6. Run an added-line security scan and independent staged-diff review.
7. Commit/push the verified slice and assert local/remote equality.
8. Add the next RED. Compact only already-proven behavior during GREEN refactor.

A worker-reported GREEN is not evidence when the final tree has not been rerun. If orchestrator verification reproduces RED, explicitly invalidate the stale claim, preserve the real failing output, resume narrowly against the existing diff, and forbid test weakening.

## Boundary requirements

- Validate caller input before semantic hashing and durable submission.
- Independently validate direct/tampered handler input before hashing, durable steps, or database work.
- Keep technical compatibility metadata outside the semantic request hash.
- Use strict root and nested schemas.
- Return distinct fixed codes for unsupported dimensions and a generic fixed code for malformed shapes.
- Convert canonicalization failures to a fixed canonical-request error.
- Errors must be data-free: no values, paths, field names, IDs, sentinels, causes, or input-derived metadata.

## Evidence requirements

- **Local rejection:** zero durable invocation and zero canonical effects.
- **Direct-ingress terminal rejection:** a terminal invocation may exist, but prove no application step/journal entry and no canonical effects.
- Always assert receipt/history counts and canonical state/version.
- Logs supplement privacy evidence; supported runtime/database introspection is authoritative.
- Audit cross-process privacy in **both directions**. Sanitized child output does not prove the parent avoided sending a private request, payload reference, grant, or hash inbound. Recheck captured stdout/stderr after behavior and process termination; checking immediately after spawn misses later leakage.

## Concurrency requirements

For serializable race evidence, establish snapshots inside the real transaction. Test barriers must be attempt-1-only, precede locks that would serialize the intended contenders, and release in `finally`. Prove exact lock identity and distinct backend PIDs; generic waiter counts are insufficient. Retries must bypass the barrier.

## Hard-cap discipline

Count every authorized production path, including new files. Record per-file and combined nonblank/noncomment lines after each slice. Preserve planned headroom; never weaken tests or omit a source file from counting. Refactor only proven GREEN behavior.

## Runtime freshness and test-selection proof

Before a long durable-runtime integration gate, revalidate the deployment URI from the runtime/container network namespace. Fingerprint the expected protocol and service (including h2/h2c when applicable): a successful TCP or HTTP response may be an unrelated host service, and a previously verified host IP may become stale after network changes. Treat registration or connectivity failures before invocation as infrastructure evidence, not vector failures. Retry acceptance only after endpoint identity is proven.

After filtered test runs, inspect selected, passed, skipped, and named tests—not only the exit code. If a planned filter misses a supporting assertion, run that assertion explicitly and report the split honestly; never infer “N/N” from tests the runner skipped.

## Independent review discipline

A reviewer unable to rerun an integration check because of transient environment state must not claim it ran. Separate code-review findings from execution evidence, and use independently captured parent-run results for claims the reviewer could not execute.

If an approving reviewer suggests additional regression evidence and you add it before commit, the staged diff has changed. Run the new focused/aggregate gates, restage and rescan, then request a focused delta review. Preserve the prior production verdict unless the new test reveals a direct contradiction; do not silently append tests after approval or reopen unrelated settled scope.

For canonicalization boundaries, test both routes when both are promised:

- local caller rejection proves zero durable invocation;
- direct public-ingress rejection proves handler-side normalization, persisted terminal code, no application-step journal entry, and zero canonical effects.

A reviewer-side environmental rerun failure is context, not contrary execution evidence, when the orchestrator has real successful output from the canonical command.

## Explicit RED evidence checkpoints

Normally commit only GREEN slices. A failing RED may be committed separately only when the frozen plan explicitly authorizes a scope/evidence checkpoint. Record the exact expected failure and downstream effects, keep production unchanged, label the checkpoint clearly, push it, and verify local/remote equality before GREEN.

## Detailed checklist

See `references/scope-discipline-and-stopping.md` for the mandatory user-defined scope discipline
rule: when the user explicitly bounds the task, do exactly that and stop — do not add unsolicited
browser evidence, extra reviews, server management, or rollback discussions.

See `references/post-agent-final-tree-verification.md` for the mandatory final-tree readback sequence, stale-GREEN invalidation, interface-drift checks, evidence hierarchy, and safe interrupted-worker recovery.

See `references/review-checklist.md` for reusable RED/GREEN, durable absence, concurrency-lock, privacy, line-budget, and checkpoint assertions.

See `references/durable-receipt-concurrency-evidence.md` for attempt-1 snapshot barriers, exact advisory-lock identity, same-key versus distinct-key submitter proof, stored-receipt comparison, supported purge/restart, sanitized IPC, and cleanup traps.

See `references/authorization-rejection-evidence.md` when porting authorization vectors through an existing durable runtime. It covers passing-first regression evidence, rejected-receipt/audit/state oracles, revocation-first ordering, and retaining a separate command-first transaction-lock proof.

See `references/proposal-review-workflow-evidence-gates.md` for a durable proposal-review workflow (journal → queue → accept/reject) with stale-conflict detection, no-op filtering, zero-revision-on-create, and TypeScript + Drizzle patterns for JSONB typing and cross-module error imports.

See `references/durable-cancellation-runtime-semantics.md` when cancellation requires endpoint-side signal consumption or pinned internal error constants differ from supported SQL/HTTP representations. It covers reproducible mismatch evidence, dated scope amendments, exact cancellation assertions, watchdog/quiescence ordering, and explicit retry proof.

See `references/local-synthetic-measurement-harness.md` for bounded local endpoint/commit/recovery/cancellation measurements, portable subprocess execution, raw-summary schemas, harness-overhead labeling, and exported-artifact privacy scans.

See `references/frozen-benchmark-decision-audit.md` when reviewing an agent-authored pass decision. It covers live-state recovery, frozen checkpoint/deadline enforcement, bidirectional IPC/privacy review, artifact timestamp truth, consumer/doctor overclaims, truth-surface reconciliation, and external-evidence hygiene.

See `references/corrective-reopening-after-bounded-failure.md` after a false pass is superseded or a bound expires. It covers preserving history, separately named corrective experiments, contradictory IPC/privacy requirements, untracked-file validation, complete line/allowlist caps, exact test-title evidence, strict metrics export validation, non-circular final-push evidence, and post-approval delta review.

See `references/bounded-prerequisite-experiments.md` when a behavioral gate first depends on proving that an existing regression or toolchain can execute. It covers exact source/blob attribution, host-valid command review, disposable and credential-scrubbed environments, total outcome vocabulary, cleanup-only recovery without reruns, exact staged allowlists during concurrent repository activity, and final truth-surface reconciliation.

See `references/live-concurrent-session-routing-experiments.md` when reproducing asynchronous result ownership across concurrent parent sessions in one shared backend process. It covers explicit validation predicates, installed-source fidelity (`source=tui`, forced async path), exact event/DB oracles, provenance-gated fail outcomes, request ceilings, nonblocking readiness, clock rechecks, AST-dedented source probes, split authority/start/evidence commits, TIMEOUT→INCONCLUSIVE seal path, orphan reviewer detection, exact staged allowlists, and mandatory re-review after concurrent writes.

See `references/bounded-single-run-evidence-experiments.md` when a frozen experiment has an immutable clock, an ordered stop-on-failure gate sequence, a committed-source requirement, and a sole final aggregate. It covers technically read-only reviewer isolation with before/after hashes, untracked-file review, full-sequence invalidation after repairs, exact durable-key cleanup, parent-owned commit-before-checkpoint kill barriers, complete Restate-attach/PostgreSQL receipt comparison, byte-level privacy scans, atomic checkpoint-temp detection, final buffer-disposal ordering, child environment allowlisting, remote-equal source execution, live-identity closeout checks, reserved closeout budget, exact all-only artifact contract compilation, machine-enum versus human-classification separation, and artifact-only repair without rerunning a one-shot aggregate.

See `references/independent-authority-review-launch.md` when an authority unit or
documentation-only authority/routing change needs independent `APPROVE`/`REJECT`
before commit. It covers parked/capital-gated state guards, live-versus-historical
routing, scheduler/cadence boundaries, dated source claims, relative links, and
excluded-file checks. Prefer a technically enforced read-only Codex review or
content-embedded tool-free review; never treat a shared-filesystem write-capable
leaf as independent merely because its prompt says “read-only.” On Windows, use a
file-backed final positional prompt, put all Codex options before it, verify the
startup banner, and compare exact reviewed-file hashes before and after.

See `references/frozen-llm-behavioral-release-suites.md` when releasing a stochastic prompt/skill/controller package. It covers raw-byte and CRLF-sensitive freezing, test-contract isolation, evidence-directory harnesses, semantic adjudication versus oracle triage, exact-hash targeted timeout recovery, Windows-safe independent delta review, and separate package-versus-organization verdicts.

See `references/dual-verdict-production-readiness.md` when a user asks whether “production can start” from a research-grade harness. It covers separate DEPLOY versus BUILD verdicts, finite comprehensive scope, external-evidence non-substitution, intentionally retained negative suites, lost-ack reconciliation oracles, separate decision/delegation artifacts, import-lineage traps, two-pass non-circular closure review, advisory-source fallback, executable migration/backup/restore/clean-checkout/restart gates, sealed-metrics preservation, and honest interrupted-program closeout.

See `references/post-foundation-external-packaging.md` when the foundation/correction is sealed, later product gates are locked, and the next work is outsider-readable packaging plus local topology smoke—not new vectors, custom persistence, or Agent OS expansion. Includes demand-label hygiene, frozen-artifact non-rewrite, and Restate synthetic volume/node-name recovery.
