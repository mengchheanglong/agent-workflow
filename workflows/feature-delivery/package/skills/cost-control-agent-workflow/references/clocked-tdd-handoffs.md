# Clocked TDD Coding-Agent Handoffs

Use this pattern when implementation is governed by a hard deadline, source-size cap, frozen vectors, or evidence-sensitive decision.

## Prompt contract

Require all of the following:

- explicit write allowlist and forbidden-file list;
- one named RED behavior and exact targeted command;
- expected behavioral failure, not merely an expected nonzero exit;
- prohibition on production changes before decisive RED;
- prohibition on changing the test during GREEN;
- exact GREEN, regression, typecheck, lint, and diff-check commands;
- no commit/push permission;
- bounded runtime/stop condition;
- final report containing changed files and exact command outcomes.

## Orchestrator acceptance

Never accept the coding agent's summary as evidence by itself.

1. Inspect `git status` and the complete diff.
2. Confirm every changed file is allowlisted.
3. Rerun the exact targeted command independently.
4. For RED, confirm the failure proves missing behavior rather than a typo, timeout, or setup error.
5. For GREEN, run the targeted test, relevant regression suite, typecheck/lint, frozen-file checks, and source-count gate.
6. Commit only after independent verification.

## Stalled-agent recovery

A coding agent may write a valid draft but spend excessive time running or narrating checks. Do not wait indefinitely inside a frozen evidence clock.

- Stop at the declared agent bound.
- Preserve only in-scope working-tree changes.
- Inspect the draft directly.
- Rerun commands yourself.
- Continue from the last valid TDD state instead of restarting the whole slice.
- If RED was decisive, preserve its exact behavioral evidence in the final artifact even when RED and GREEN ship in one commit.

## Clock-start sequencing

Before candidate services, deployment registration, executable probes/tests, or executable-file changes:

1. freeze and commit the vector matrix, public interfaces, line/time bounds, evidence rules, and stop decisions;
2. create and push a dated start artifact from a clean baseline;
3. record start/deadline, baseline commit, exact dependency/image pins, counted paths, baseline count, and cap;
4. stop honestly at the deadline or cap—never reset the clock, weaken tests, exclude required source, or move production logic into uncounted harness files.

## Useful verdict format

```text
RED/ GREEN command: <exact command>
Expected behavior:   <contract>
Observed behavior:   <concrete state/output>
Scope:               <allowlisted files only / drift>
Static gates:        <pass/fail>
Count:               <baseline/current/cap>
Decision:            ACCEPT / REJECT / CONTINUE FROM VALID DRAFT
```
