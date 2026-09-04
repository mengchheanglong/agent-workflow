# Scope Discipline and Stopping at User-Defined Boundaries

Use this when the user explicitly defines a narrow task scope. The failure mode this
references: the agent expands the task with unsolicited verification, browser evidence,
extra reviews, server management, or rollback discussions — then the user has to correct
it back to the original scope.

## The pattern

User says: "just update the workflow" / "no need to roll back, just report status" /
"only do X". Agent does X + Y + Z (browser checks, extra reviews, server startup,
additional evidence). User: "you gone overboard i only ask you to update the workflow."

## Rule

**When the user explicitly bounds the task, do exactly that and stop.**

If the user says:
- "just update the workflow" → update the workflow, report status, stop
- "no need to roll back, just report status" → report current state, do not repair, stop
- "only do X" → do X, do not add Y or Z even if you think they improve quality

Do not add:
- unsolicited browser evidence or screenshot matrices
- extra independent reviews beyond what was asked
- server startup/teardown the user didn't request
- rollback/repair discussions when the user said don't roll back
- additional verification layers beyond the explicit ask

## Why this matters

The user is paying for tokens and time. Unsolicited expansion:
- burns their budget on work they didn't want
- delays the actual deliverable
- forces them to correct the agent back to the original scope
- signals the agent isn't listening to explicit bounds

## How to apply

1. When the user gives a narrow scope, restate it back implicitly by doing only that.
2. If you believe additional work (browser evidence, reviews) would help, **ask first** or
   offer it as a next step after the explicit deliverable is done — do not bundle it in.
3. When the user corrects scope ("you gone overboard", "just do X"), acknowledge, trim back,
   and deliver only what was asked.
4. Status reports describe current state — they do not launch repair workflows unless the
   user explicitly asks.

## Session example

User asked to optimize a reusable workflow and report status. The agent additionally:
started a production server, ran Playwright, dispatched independent reviewers, and discussed
rollback. User: "you gone overboard i only ask you to update the workflow. no need to roll
back, just report our current status." The correct response was to report status and stop.
