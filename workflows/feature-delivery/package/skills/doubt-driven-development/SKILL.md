---
name: doubt-driven-development
description: "Adversarial fresh-context review for non-trivial decisions: CLAIM → EXTRACT → DOUBT → RECONCILE → STOP. Catch wrong directions before they compound."
version: 1.2.1
author: Adapted from addyosmani/agent-skills (53K stars)
metadata:
  hermes:
    tags: [review, quality, adversarial, safety, verification]
---

# Doubt-Driven Development

A discipline of **materializing a fresh-context reviewer biased to disprove** before any non-trivial output stands. Long sessions quietly turn assumptions into "facts" — this cross-examines decisions while course-correction is cheap.

**Confident ≠ Correct.**

## When to Use

A decision is non-trivial if ANY of:
- Introduces/modifies branching logic
- Crosses module or service boundaries
- Asserts something the compiler can't verify (thread safety, idempotence, ordering)
- Correctness depends on context the future reader won't have
- Blast radius is irreversible (deploy, migration, public API change)
- Selects a roadmap, platform, custom runtime, data architecture, or multi-month project
- Assumes a new system is necessary before testing an existing incumbent
- Publishes evidence-backed scientific, legal, policy, or strategic conclusions

**Do NOT use for:** Mechanical ops (rename, format), clear user instructions, one-line fixes, pure tooling.

## The Doubt Cycle

```
CLAIM → EXTRACT → DOUBT → RECONCILE → STOP
```

### Step 1: CLAIM — Surface what stands

Write the decision in 2-3 lines:

```
CLAIM: "The new caching layer is thread-safe under read-heavy workload."
WHY: A race here corrupts user data and is hard to detect in QA.
```

If you can't write it compactly, you have a vibe, not a decision.

### Step 2: EXTRACT — Smallest reviewable unit

Isolate the artifact and contract. Strip your reasoning — handing over conclusions biases the reviewer. The unit must be small enough to hold in one read.

For a blocking review, freeze the unit by content hash or commit and include that identifier in the review request. Avoid mutating the reviewed files while the reviewer runs. If a necessary correction changes the hash, the returned verdict is evidence about the old snapshot: reconcile its findings, but do not use an old `EXECUTION_READY` as a pass for the new artifact.

For concurrency, idempotency, or crash claims, include the exact synchronization point and observable proof—not just a test name. A barrier before a transaction, a transaction opened before its first query, and a transaction whose snapshot has observed the required state are three different claims. Identify the exact lock/resource being awaited rather than counting generic waiters, and trace what happens on retry: a proof-only first-attempt barrier must not silently re-run and block the required terminal outcome. See `references/concurrency-evidence-review.md` for reusable review checks and a retry-safe shared-advisory-barrier pattern.

For time-boxed conformance gates with frozen vectors, hard source budgets, and repeated RED→GREEN checkpoints, use `references/bounded-conformance-evidence.md`. It covers scope hashes, one-dimensional error slices, negative-effect evidence, line-budget refactors, staged independent review, remote-sync verification, and promotion stop conditions.

For a **read-only authority-package review** where execution, mutation, credentials, sessions, providers, Git inspection, or unrelated-file inspection is prohibited, use `references/read-only-authority-review.md`. It covers negative-scope discipline, runtime-default tracing, pass-predicate completeness, event/marker provenance, aggregate bounds, fail-closed cleanup, and verdict-first exact-line reporting. Do not import a generic pre-commit workflow's diff, test, auto-fix, or commit steps into such a review.

For a **governance-document or external-model PR review**, use `references/governance-document-external-model-review.md`. It adds exact-SHA/state freshness checks, sealed-vocabulary comparison, reproducible source-label audits, live-system versus repository-state verification, PII-safe template review, monorepo outsider-access boundaries, public-exposure triage, and the switch from pre-merge findings to corrective-PR/revert guidance when a PR merges during review.

### Step 3: DOUBT — Invoke fresh-context reviewer

Use `delegate_task` in Hermes with an adversarial prompt:

```
Adversarial review. Find what is wrong with this artifact.
Assume the author is overconfident. Look for:
- Unstated assumptions
- Edge cases not handled
- Hidden coupling or shared state
- Ways the contract could be violated
- Failure modes under unexpected input
Do NOT validate. Do NOT summarize. Find issues, or state
explicitly you cannot find any after thorough examination.

ARTIFACT: [code/diff/decision]
CONTRACT: [constraints it must satisfy]
```

**Pass only ARTIFACT + CONTRACT — never the CLAIM.** The reviewer must independently determine correctness.

For roadmap, research, or architecture selection, use **separate review lenses** rather than one broad reviewer:

1. source-to-claim and citation quality;
2. necessity and incumbent alternatives;
3. technical contracts, invariants, and failure modes.

A reviewer that accepts the proposed architecture can still miss the more important question: whether any custom implementation is needed. For custom-platform claims, run an incumbent-first counterexample before comparing bespoke designs. See `references/roadmap-architecture-falsification.md` for the reusable experiment and synchronization checklist.

Treat blocking background reviews as pending evidence. Keep the verdict preliminary until they return or are explicitly declared non-blocking. A timeout supplies no independent evidence; a late material finding reopens the verdict even if a prior answer called it final.

### Step 4: RECONCILE — Classify every finding

First run a **freshness check**. Background reviewers judge the snapshot they read, not necessarily the current artifact. Re-read the cited lines and regenerate the diff before acting. If implementation changed during review, classify each item as **still present**, **stale/already fixed**, or **newly exposed by the latest state**; never apply a fix against an obsolete snapshot. Material drift may require a focused re-review of the latest artifact.

For each current finding:
- **Accepted** → fix the artifact and every canonical routing/state/task file that repeats the old decision
- **Rejected** → document why, with counter-evidence
- **Deferred** → create a tracking item with an explicit gate

When a finding changes project selection, re-run stale-instruction searches, machine-readable-state parsing, structural checks, and source reachability. Preserve historical/raw sources with a supersession notice rather than rewriting them.

### Step 5: STOP — Meet the stop condition

Stop when findings are trivial OR 3 broad cycles completed OR user overrides. Do not declare a final verdict while a reviewer designated as blocking is still pending. For roadmap/platform decisions, the stop condition is the smallest experiment that resolves the necessity claim—not completion of a preferred architecture.

After three broad cycles, do not start another open-ended review loop. If the final reviewer returns one or two exact, mechanical corrections with no strategic ambiguity, apply only those deltas and allow one **focused micro-review** constrained to verifying the named corrections and checking for direct contradictions they introduce. It must not reopen settled scope. If the correction is architectural, expands scope, or the micro-review finds another material blocker, stop and escalate rather than iterating indefinitely.

## Hermes Integration

Use `delegate_task` with a separate subagent for Step 3. The subagent's isolated context ensures true fresh-context review. For cross-model review: run the same adversarial prompt through `terminal` with a different model via OpenCode or Codex CLI.

## Anti-Patterns

- Don't use inside a subagent (nested spawning blocked). Escalate to user instead.
- Don't skip the CLAIM step — unstated assumptions are the whole point.
- Don't share your reasoning with the reviewer.
- Don't compare only two bespoke implementations when an existing incumbent could falsify the need for both.
- Don't treat green engineering tests as evidence of novelty, market demand, product value, or scientific significance.
- Don't imply reviewer consensus when one or more reviewers timed out or returned no usable result.
- Don't silently absorb a late contradiction; issue a superseding correction and synchronize canonical artifacts.
