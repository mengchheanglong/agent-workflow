# Frozen Benchmark Decision and Evidence Audit

Use this after another agent claims a bounded durable-workflow experiment passed. Green tests are necessary but do not validate the decision by themselves.

## Live-state recovery

1. Inspect live branch, `HEAD`, upstream ref, status, commit timestamps, and every commit since the approved baseline.
2. Inspect sibling Mission Control/state repositories separately; never assume shared remotes or Git boundaries.
3. Treat reports and chat summaries as claims until reconciled with source, commit objects, runtime output, and frozen plans.
4. When concurrent agents create unexplained files, preserve/hash them before removal or replacement. Audit the final live tree, not a stale review snapshot.

## Frozen-sequence audit

Build a checklist directly from preflight and plan:

- RED, GREEN, measurement, final-review, commit, push, and synchronization checkpoints;
- exact commands, allowlists, test counts, line caps, static-inclusion rules, and stop outcomes;
- immutable start/deadline and whether commit **and push** must finish inside the bound.

A later commit cannot retroactively satisfy a requirement that had to exist at the decision commit. Required measurements or independent review cannot be renamed "optional" in the final artifact.

## Semantic channel audit

Trace every direction of every cross-process channel:

- parent → child IPC/stdin/argv/environment/files;
- child → parent IPC/stdout/stderr/errors;
- worker/runtime journal, logs, and durable inputs/outputs.

A test validating only sanitized child output can miss a full private request sent inbound. Recheck stdout/stderr after behavior, stream flushing, and termination; an assertion immediately after spawn proves almost nothing.

Harness-reported launch evidence is not automatically authoritative. Cross-check it against the actual `spawn`/`fork` call. Avoid assertions that print environment values or secrets on failure.

## Side-effect and cleanup evidence

- Query by full composite identity (for example namespace + command ID).
- When a child must submit nothing under any ID, also assert zero global receipts/history/audits.
- Compare returned consequences to directly read canonical receipts.
- Fail if cleanup exceeds its timeout. A polling loop that falls through silently is not cleanup proof.

## Artifact truth audit

Cross-check:

- decision time against author/committer timestamps;
- elapsed/remaining arithmetic;
- baseline/final commit IDs;
- raw decisive output and exact test totals;
- topology and route identity;
- measurements and skipped/not-applicable inventory;
- local/upstream equality.

Reject approximate future seal times and `Updated` timestamps older than content they claim to include.

## Adjacent-tool honesty

For a claimed public consumer or doctor:

- detect imports from internal tests/fixtures/workers;
- distinguish an in-repo demonstration from an independently consumable client;
- ensure the doctor probes the critical endpoint, registration, and route rather than neighboring services only;
- isolate duplicate evidence to the duplicated command;
- require outer timeouts and fail-closed backend cleanup.

## Truth-surface reconciliation

Compare immutable artifacts, repo README/AGENTS, `.active/{CURRENT,NEXT,STATE.json}`, Mission Control tasks, and root workspace routing. Search for contradictions such as `active next` versus `parked`. Treat root files outside a clean Git boundary as weak-provenance state.

## External-evidence hygiene

Fetch primary URLs before accepting desk claims. Prefer regulator filings, official postmortems, and official product documentation. Label vendor marketing/social posts as discovery evidence—not prevalence, demand, or PMF. Founder self-report is internal signal, not external Tier-A customer/operator evidence.

## Verdict rule

When implementation tests pass but the frozen process/privacy contract fails, state both:

```text
Implementation tests are green.
The experiment decision is invalid under its frozen contract.
```

Use `REVISE` while the immutable bound remains open. If required closure/review/commit/push misses the deadline, use the precommitted incomplete-at-bound outcome rather than resetting the clock.
