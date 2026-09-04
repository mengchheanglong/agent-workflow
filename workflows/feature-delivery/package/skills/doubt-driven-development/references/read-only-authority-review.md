# Read-only authority-package review

Use this for proposed experiments, migrations, deployments, or other authority packages when the reviewer is explicitly prohibited from executing or mutating anything.

## Method

1. Read only the named authority files first. Inspect installed/runtime source only where needed to validate a claimed mechanism or default.
2. Respect negative scope literally: no driver execution, service startup, credentials, sessions, providers, Git mutation/status, or unrelated dirty-file inspection when prohibited.
3. Trace every frozen requirement to mechanical enforcement. Model/operator prose is not enforcement.
4. Verify the PASS predicate gates on every required observation. A recorded check that is omitted from PASS is not protective.
5. Check exact runtime defaults. An omitted async/background flag can bypass the shared queue the experiment claims to test.
6. Validate evidence provenance: require the exact event type/kind, and prove markers originate in result data rather than echoed prompts, goals, progress, or error text.
7. Check aggregate budgets mechanically, including parent and child defaults, retries, and blocking calls that can escape nominal deadlines.
8. Check cleanup fail-closed: termination errors must not skip deletion, and success evidence must not be emitted while sensitive temporary state remains.
9. Return the requested verdict token first, then only concise blockers with exact authority-path lines and, where needed, exact runtime-source lines.

## Reusable blocker patterns

- Async behavior specified, but the call defaults to synchronous.
- Oracle scans all status text instead of direct `kind=process` events.
- Expected markers are embedded in goals and echoed into completion/error notifications.
- Distinct IDs, exact dispatch count, successful completion, or cleanup are recorded but not included in PASS.
- Global provider-call ceiling claimed while only per-agent iteration limits exist.
- Exact shell command authorized only by prompt while a general terminal remains available and unaudited.
- Deadline loop contains a blocking read or ignores the immutable external deadline.
- Cleanup failure still writes evidence or leaves auth/session/log artifacts.

## Verdict discipline

`APPROVE` means no blocking mismatch remains. `REJECT` findings must be actionable, mechanically grounded, and line-addressed. Do not run tests merely because a general code-review workflow suggests it when the authority request forbids execution.
