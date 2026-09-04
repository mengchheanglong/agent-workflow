# Source-Traced Stateful QA Reference

## Risk matrix

| Surface | Probe | Pass evidence |
|---|---|---|
| Permission | Call the mutation path with a role lacking the UI permission | `false`/no-op, no audit, no emit |
| Target integrity | Unknown, stale, duplicate, or already-final ID | No fabricated record or success state |
| Input contract | Empty, whitespace, oversized, non-finite, or illegal enum values | Rejected before state mutation |
| Lifecycle | Backward, repeated, or cross-kind transition | Explicit transition table blocks it |
| Idempotency | Rapid double submit or repeated confirm | One state change and one relevant audit |
| Audit | Actor, role, reason, target, historical/current session labeling | Attribution matches the actual operator and outcome |
| Caller outcome | Mutation returns false after stale state or permission failure | No success toast, dialog-success cleanup, or activity record |
| Referential integrity | Every linked case/store/settlement/user exists | Link resolves or honest missing-state is rendered |
| Snapshot freshness | Mutate a record, then inspect list/detail/merchant view | All views read the live state source |

## Review-recovery recipe

1. Freeze the review input by commit or content hash.
2. If the diff is large, send only one risk slice per reviewer request: permissions/mutations first, then state/audit, then references/routes, then UI.
3. Require structured output with separate security concerns, logic errors, suggestions, and a boolean verdict.
4. Treat timeout, malformed output, or a self-report without evidence as **no verdict**.
5. Re-read every cited line against the current source; child output is a lead, not proof.
6. If the current artifact changed, discard the old approval and review the new hash.
7. After a confirmed fix, rerun typecheck, lint, build, relevant route smoke, staged-scope, and secret checks.

## Evidence report checklist

- Authority and allowed path stated.
- Source-traced workflows and direct mutation guards listed.
- Typecheck/lint/build commands and exit statuses recorded.
- Valid and invalid HTTP routes listed separately.
- Browser-tested flows named exactly; unverified flows and binding limitations stated.
- Known non-fatal warnings separated from failures.
- Commit, pushed HEAD, PR URL, and CI/check availability verified.
- No credentials, generated dependencies/build output, or unrelated parent changes included.
