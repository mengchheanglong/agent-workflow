# Pitfall: Over-scoping

The user explicitly bounds the task. When the user says "you gone overboard" — stop, report status, and wait for direction.

## What happened

During the Angkoro Admin workflow optimization, the user asked only to update the workflow. The assistant:
- Ran browser evidence generation
- Dispatched independent reviewers
- Created artifacts beyond the requested scope
- Had to be told "no need to roll back, just report status"

## The rule

When the user gives a bounded request:
1. Do exactly what was asked
2. Do NOT expand scope ("while I'm at it")
3. Do NOT add unsolicited reviews, evidence, or browser automation
4. Report status and wait for direction

## Examples

| Request | Do | Don't |
|---------|-----|-------|
| "Update the workflow" | Update workflow files | Run browser evidence, dispatch reviewers |
| "Report status" | Report current state | Make additional changes |
| "Remove this element" | Remove the element | Redesign the whole page |

## Related

- `references/playwright-screenshot-technique.md` — only run when explicitly asked
- Feature Delivery v2 workflow — follow the stage gates, don't skip ahead
