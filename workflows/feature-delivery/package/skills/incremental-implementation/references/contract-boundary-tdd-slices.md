# Contract-Boundary TDD Slices

Use this pattern when a public API or durable workflow validates both a semantic request and a technical compatibility envelope.

## Test two independent boundaries

One path cannot prove the other.

### Approved local client

- Pass malformed or undeclared input through the normal client.
- Require a fixed application error before canonical hashing, workflow submission, network I/O, or persistence.
- Assert zero invocation records and zero canonical receipt/history/state effects.

### Direct or tampered ingress

- Bypass the approved builder and call the public ingress with a raw envelope.
- Require the exact terminal HTTP/application code.
- Use supported runtime introspection to require the same terminal failure code.
- Assert no canonical receipt/history/state transition.

## Data-free errors

Failures must expose only a fixed code/type. Assert they do not contain:

- request values, command/workflow IDs, or private sentinels;
- undeclared private field names;
- validator issue paths/messages;
- parser causes, stacks, or copied metadata.

Map expected validation failures to fixed local errors. At durable ingress, map only known validation errors to terminal failures and rethrow unexpected errors.

## One compatibility dimension per slice

Use vertical RED→GREEN cycles:

```text
unsupported domain version → exact fixed mapping
unsupported request-hash version → exact fixed mapping
unsupported authorization model → exact fixed mapping
validator → projection → serializer → runtime
```

Do not pre-implement sibling mappings. A strict literal schema returning a generic error is an acceptable first GREEN; subsequent REDs refine exact dimension-specific behavior.

A decisive RED captures both the wrong current response (for example generic `INVALID_REQUEST_SCHEMA`) and the required fixed `UNSUPPORTED_*` code while proving canonical side effects remained zero.

### Refactor the shared integration helper safely

When later dimensions repeat the same real-ingress setup and assertions:

1. Finish and verify the current RED→GREEN slice first.
2. Extract the repeated setup/oracle into a shared test helper while all existing cases are green.
3. Re-run one existing case through the helper and require it to remain green.
4. Only then add and run the next dimension to capture its RED.

Do not combine an unverified helper rewrite with a new failing case; otherwise the failure cannot distinguish a broken harness from missing production behavior.

Strengthen the helper once, then inherit the stronger oracle for every later case. Where supported, require the immediate HTTP failure, persisted terminal failure, data-free text, zero canonical state effects, and absence of the downstream durable step/journal entry. The last assertion proves rejection happened before the canonical execution boundary rather than after a partial attempt.

### Consolidate only proven mappings

Under a hard production-line budget, implement each mapping minimally after its own RED. Once several sibling mappings have individually failed and gone green, use the REFACTOR phase to consolidate only those proven mappings into a table or registry. Re-run every existing mapping case and the full suite after consolidation.

Do not pre-populate the table with future codes merely because their names are known. Track remaining headroom against all mandatory future production work—not just the next slice—and reclaim budget before a checkpoint if later required behavior would otherwise be crowded out.

## Side-effect oracle

For every rejection, inspect all authoritative layers available:

- public status/body;
- durable invocation status/failure via supported introspection;
- receipt/history counts;
- entity version/status/projection;
- process/backend cleanup when relevant.

This prevents message-only tests from passing after a forbidden invocation or write.

## Hard implementation budgets

Count the exact governed production path after each GREEN. If mandatory future slices will not fit, use the REFACTOR phase to compact structure only while the suite stays green.

Never respond to budget pressure by:

- excluding a new production file from the count;
- weakening vectors or privacy assertions;
- pre-implementing untested behavior;
- compressing code into unreadable forms.

Report total and remaining headroom at each checkpoint.

## Delegated-agent containment

For each GREEN or REFACTOR handoff:

1. Pin the base commit.
2. Give an explicit write allowlist and protected test list.
3. Require actual RED, targeted GREEN, full-suite, static, diff, and budget evidence.
4. Independently inspect the live diff and rerun gates.
5. Reject stale reports when the base commit, reviewed hashes, or current diff changed.
6. Independently review the staged diff before commit/push.

For long-running background agents, enable completion notification; do not blindly poll or treat an old asynchronous review as authoritative over newer reviewed hashes.
