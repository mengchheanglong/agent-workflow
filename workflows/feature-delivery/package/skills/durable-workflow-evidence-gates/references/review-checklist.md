# Durable Workflow Review Checklist

## Focused RED

- [ ] Production source unchanged before RED
- [ ] Expected fixed code/type asserted
- [ ] Actual wrong code/type captured
- [ ] Sensitive sentinel, field, path, ID, and value excluded from error text
- [ ] Runtime invocation count/status asserted
- [ ] Application step/journal presence or absence asserted
- [ ] Receipt/history counts asserted
- [ ] Canonical state/version asserted

## Minimal GREEN

- [ ] Caller validates before hash/submission
- [ ] Handler independently validates before hash/step/database
- [ ] Parsed values are the only values used afterward
- [ ] Technical envelope excluded from semantic hash
- [ ] Unsupported dimension has a distinct fixed code
- [ ] Other malformed input retains generic fixed schema code
- [ ] Canonicalization exception becomes fixed canonical-request code
- [ ] Unexpected internal errors are not misclassified

## Privacy

- [ ] No Zod/validator issue serialization
- [ ] No error cause carrying raw input
- [ ] No input-derived metadata
- [ ] No command/workflow ID leakage
- [ ] No optional-payload sentinel or its digest in logs/journal/errors
- [ ] Runtime introspection used in addition to log scans

## Canonicalization boundary

- [ ] Local lone-surrogate/non-I-JSON case returns fixed canonical-request code
- [ ] Local rejection creates zero durable invocation
- [ ] Direct-ingress equivalent returns the same persisted terminal code
- [ ] Direct-ingress error excludes sentinel, field name, IDs, values, and cause
- [ ] Direct-ingress journal has no application-step entry
- [ ] Both routes leave receipt/history/state unchanged

## Serializable concurrency

- [ ] Snapshot established inside the real transaction
- [ ] Barrier enabled only on attempt 1
- [ ] Barrier placed before command/receipt locks that would serialize contenders
- [ ] Parent PID and granted exclusive advisory lock captured
- [ ] Exact `(database,classid,objid,objsubid)` tuple captured
- [ ] Required distinct child PIDs have ungranted `ShareLock` on exact tuple
- [ ] Parent releases in `finally`
- [ ] Child shared locks proceed concurrently after release
- [ ] Retry bypasses barrier and reaches stored-receipt/conflict outcome
- [ ] No residual locks, backends, receipts, or history from rollback-only probes

## Verification and hard cap

- [ ] Focused test passes
- [ ] Surviving-direction aggregate passes
- [ ] Typecheck, lint, build, and diff checks pass
- [ ] Changed-file allowlist passes
- [ ] Frozen paths unchanged
- [ ] Added-line security scan passes
- [ ] Per-file and combined counted lines recorded
- [ ] Planned headroom remains
- [ ] Independent staged-diff JSON review passes
- [ ] If evidence changed after approval, focused delta review passes
- [ ] Reviewer rerun blockers are separated from orchestrator-owned execution output

## Checkpoint

- [ ] RED-only commit is used only when the plan explicitly authorizes an evidence/scope checkpoint
- [ ] RED checkpoint records exact wrong code/type and downstream effects with production unchanged

- [ ] Commit message marks verified slice
- [ ] Push succeeds
- [ ] Fetch remote branch
- [ ] Assert local `HEAD` equals remote branch
- [ ] Working tree contains only the next intentional RED, or is clean
