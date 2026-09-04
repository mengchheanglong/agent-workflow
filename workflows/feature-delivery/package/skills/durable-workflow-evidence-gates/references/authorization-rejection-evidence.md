# Authorization-rejection evidence for durable workflows

Use this pattern when porting frozen authorization vectors through a durable runtime whose canonical database already implements the behavior.

## Test-only porting rule

Write the runtime-facing regression test first and run it alone. If it passes immediately, record that the existing implementation already satisfies the vector, add no production code, and continue with focused plus aggregate verification. A passing-first test is acceptable here because the work item is evidence porting, not a new behavior claim.

## Layered rejection oracle

For each authorization rejection, prove all relevant layers rather than checking only the returned code:

1. Submit through the approved real runtime client or public ingress.
2. Assert a typed rejected canonical receipt and the expected command identity/hash binding.
3. Assert exactly one rejected receipt, zero accepted-history rows, and no accepted transition.
4. Assert canonical state and version remain at the prior frozen values.
5. Assert exactly one privacy-limited decision-audit row with the expected command/hash, actor, grant/version, validator version, decision code, and opaque payload reference—never private payload bytes.
6. For revocation-first, commit the new revoked grant version before runtime submission and read it back before judging the result.
7. Retain a separate deterministic command-first database lock test; do not replace transaction-linearization proof with runtime timing.

## Review and commit gate

Run the focused runtime authorization tests together with the unchanged command-first database barrier, then the full surviving-direction aggregate, static gates, diff/allowlist checks, security scan, and independent staged-diff review. A test-only slice must leave the counted production total unchanged.
