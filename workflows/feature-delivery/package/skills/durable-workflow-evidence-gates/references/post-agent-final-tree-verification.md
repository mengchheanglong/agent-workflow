# Post-Agent Final-Tree Verification

Use this after an autonomous coding worker finishes a bounded durable-workflow or TDD slice.

## Failure mode

A worker can run GREEN gates and then make a final edit that breaks the delivered tree. Its narrative report may still quote the earlier passing output. Treat the report as a hypothesis, not as final evidence.

A common boundary defect is interface drift between a typed test façade and its runtime implementation: argument count/order, namespace filtering, return fields, or cleanup queries differ. Type assertions or casts can hide this until execution.

## Required order

1. Wait for the worker to exit.
2. Snapshot final `HEAD`, `origin`, status, diff names/stat, and untracked files.
3. Enforce the allowed-write list before running gates.
4. Read every changed boundary file and compare:
   - declared interface versus implementation;
   - function call arity and parameter order;
   - tenant/namespace/key filters;
   - result and receipt field names;
   - fixture/mocks versus runtime implementations;
   - cleanup counters and process/backend/lock scope.
5. Run the canonical focused command yourself on the final tree.
6. Run the required regression, typecheck, lint, build, diff, frozen-file, line-cap, privacy, and cleanup gates.
7. Re-read status after tests because harnesses can generate files or leave runtime state.
8. Accept GREEN only from orchestrator-run commands executed after the final edit.

## When the worker's GREEN is invalidated

- State explicitly that the earlier GREEN claim is invalid.
- Preserve the orchestrator-reproduced command and decisive failure as the authoritative RED.
- Resume narrowly against the existing diff; do not restart or discard good work.
- Name the observed contract mismatch, keep the original deadline and allowed files, and forbid test weakening.
- Require the corrected report to acknowledge the stale claim.
- Re-run the full canonical pack after repair.

## Evidence hierarchy

1. Orchestrator-run output from the final tree.
2. Durable raw artifacts captured after the final edit.
3. Current source/Git/runtime readback.
4. Worker narrative summary.

Keep test-first ordering separate from retained RED-console proof. If the official artifact says RED output was not retained, do not promote a plausible later narrative into proven evidence.

## Interrupted workers

- Partial diff after timeout/interruption: inspect and explicitly resume from current state.
- Explicit process kill with no diff: treat the stop as intentional; require renewed direction before relaunch.
- Never run two workers against the same files. Reconcile active processes, final Git state, and remote equality first.
