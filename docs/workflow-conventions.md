# Workflow Conventions

Cross-cutting conventions shared by all workflows in this repository.

## Bounded fix loops

Every workflow that includes a review step must enforce bounded fix loops.

- Default maximum: **2 broad fix/re-review cycles**.
- After exhaustion with unresolved BLOCKER or MAJOR findings: **STOP** and escalate to human.
- A human may explicitly authorize additional cycles with recorded evidence.
- The fix loop cannot be bypassed by advancing status without resolving findings.

## Independent review

Builder and Reviewer must be separate contexts. The Builder may not approve its own work.

Review should try to **falsify readiness** rather than confirm the Builder's claims.

## Finding severity

All workflows use the same severity scale:

| Severity | Meaning |
|----------|---------|
| `BLOCKER` | Security bypass, data loss/corruption, broken core requirement, or invalid evidence |
| `MAJOR` | Incorrect behavior, important missing validation/test, regression, or compatibility break |
| `MINOR` | Bounded edge case, maintainability issue, documentation drift, or non-critical test gap |
| `NIT` | Optional clarity or polish |

## Finding origin

| Origin | Meaning |
|--------|---------|
| `INTRODUCED` | Created by the current change |
| `PRE_EXISTING` | Already present before the current change |
| `UNCLEAR` | Cannot determine origin from available evidence |

## Review verdicts

| Verdict | Meaning | May ship? |
|---------|---------|-----------|
| `APPROVE` | No unresolved BLOCKER or MAJOR; current snapshot is acceptable | Yes |
| `CHANGES_REQUESTED` | Correctable work remains | No |
| `DO_NOT_MERGE` | Fundamental safety, scope, or design problem | No |

`APPROVE` is the only ship-capable verdict.

## Specification vs engineering quality

Workflows with formal review should separate two concerns:

1. **Specification compliance** — does the implementation satisfy the requirements?
   Verdict: `PASS`, `FAIL`, or `UNVERIFIABLE`.
2. **Engineering quality** — is it correct, safe, tested, and maintainable?
   Verdict: `APPROVE`, `CHANGES_REQUESTED`, or `DO_NOT_MERGE`.

Overall `APPROVE` requires specification `PASS` and engineering-quality `APPROVE`.

## Shipping

Agents do not commit, push, merge, deploy, or publish unless the human or project rules explicitly
authorize that action. Shipping is always a human decision.
