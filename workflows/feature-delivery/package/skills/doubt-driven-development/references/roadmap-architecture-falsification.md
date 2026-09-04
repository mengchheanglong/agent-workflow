# Roadmap and Architecture Falsification Playbook

Use this for roadmap selection, platform creation, persistence architecture, and other decisions where implementation can quietly assume its own necessity.

## Three independent review lenses

Run these separately so one framing does not contaminate the others:

1. **Source-to-claim audit** — Do citations entail each claim, with correct date, jurisdiction, study status, and limitations? Use the `web-research` skill's `references/source-to-claim-audit.md`.
2. **Necessity audit** — Is the proposed custom system needed, or can an existing capable incumbent plus a thin domain layer satisfy the contract?
3. **Technical-contract audit** — Are invariants, failure modes, deterministic boundaries, privacy rules, concurrency, recovery, versioning, and observability explicit?

Agreement between reviewers is useful; disagreement is evidence. Record both rather than averaging them into a vague consensus.

## Incumbent-first counterexample

When the claim is “we need a custom X”:

1. State the necessity claim explicitly.
2. Select one strong incumbent that matches the intended language/database/deployment shape. Do not compare five frameworks initially.
3. Choose one narrow vertical scenario that exercises a recognizable costly failure, not an abstract storage demo.
4. Freeze 5–8 executable tests before implementation.
5. Precommit a short timebox and complexity bounds, such as non-test application code, operational components, framework internals bypassed, and whether a generic custom subsystem had to be recreated.
6. Run the incumbent with only a thin deterministic domain adapter.
7. Decide from the precommitted rule:
   - **Incumbent passes:** custom-first is falsified; keep the contract/harness and continue on existing infrastructure.
   - **Intrinsic incumbent limitation:** name the exact missing capability and build only that capability.
   - **Benchmark does not discriminate:** revise the contract or park the mission.

Setup errors, missing domain rules, aesthetic preference, and speculative future needs are not intrinsic framework limitations.

## Vertical scenario qualities

Prefer a fixture that combines several mission-defining properties in one flow:

- scoped identity or tenancy;
- authorization rejection with no canonical mutation;
- duplicate suppression;
- conflicting concurrency;
- crash/restart recovery;
- deterministic/versioned reconstruction;
- optional sensitive-payload deletion without retaining content;
- no real personal data unless governance is already approved.

## Async reviewer discipline

- Mark a verdict **preliminary** while blocking reviewers are pending.
- Do not call the review final merely because the main research is complete.
- If a late result arrives after publication, reopen the verdict, classify every finding, correct canonical artifacts, and issue an explicit superseding correction.
- A timed-out reviewer contributes no independent evidence. Do not imply consensus from a missing result.

## Reconciliation and canonical synchronization

For each accepted finding:

1. Correct the main report.
2. Update canonical goal/decision/state files.
3. Update task order, evidence gates, and builder handoff.
4. Update root and project routing instructions so future agents do not follow stale architecture rules.
5. Search active files for superseded phrases and old task boundaries.
6. Parse machine-readable state and rerun structural/citation checks.
7. Preserve historical/raw sources with a clear supersession notice rather than rewriting history.

## Stop rule

Stop after the smallest experiment that resolves the decision. Green tests prove that implementation, not novelty, user demand, product value, or scientific significance.
