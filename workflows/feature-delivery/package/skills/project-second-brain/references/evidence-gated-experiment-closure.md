# Evidence-Gated Experiment Closure

Use this after a bounded experiment reaches a reviewed decision and its implementation repository has a sealed artifact/commit.

## Authority order

1. Frozen preflight/plan and immutable clock.
2. Newest valid sealed decision artifact.
3. Pushed/fetched implementation commit with `HEAD == origin/main`.
4. Machine-readable active state.
5. Human routing views and mission/task prose.

Never let stale `.active/` wording override a sealed implementation result. Do not let later green tests rewrite an earlier expired experiment; preserve the old bounded outcome and record the correction as a separate experiment.

## Closure sequence

1. Complete the frozen aggregate exactly, including mandated reruns; number retries/runs honestly.
2. Run strict artifact/schema/privacy/cleanup validators before review.
3. Obtain independent security/spec review.
4. Obtain a separate independent final review.
5. Fetch and prove pre-decision local/remote equality.
6. Create one conditional decision artifact. Do not claim its future commit is already pushed.
7. Stage only the approved final artifact/evidence files; run cached-diff scope, secret, and whitespace checks.
8. Commit, push, fetch, and prove equality before the deadline. Only then is a conditional pass effective.
9. Stop experiment services and verify project containers/workers are gone. Identify port owners before treating a listener as an orphan; unrelated system services can share the same port on a different interface.
10. Reconcile Mission Control and root routing without automatically opening later gates.

## Reconciliation surfaces

At minimum inspect and update:

- `.active/STATE.json`
- `.active/CURRENT.md`
- `.active/NEXT.md`
- `.active/DECISIONS.md`
- repository `AGENTS.md`
- mission `MISSION.md` and `TASKS.md`
- workspace `WORKSPACE_CONTEXT.md` and root `AGENTS.md`

Machine state and human views must agree on:

- the exact decision and effective timestamp;
- sealed commit/artifact;
- preserved prior outcomes;
- locked/parked later gates;
- the next action as a hold or separate decision, not automatic continuation.

## Verification

Run a temporary ad-hoc verifier that:

- parses machine JSON;
- confirms implementation `HEAD == origin/main` and clean status;
- checks required decision/commit/artifact strings across live routing files;
- searches for stale phrases such as “redesign pending” or “final decision not recorded”;
- validates relative links by resolving them from the file that contains them;
- runs `git diff --check` in each clean repository boundary;
- distinguishes root files outside a clean Git boundary from sealed evidence.

Obtain read-only review of the reconciliation before committing it. If the research repository has no remote, commit locally but do not invent or automatically add a remote; report the local commit and zero-remotes state.

## Pitfalls

- Do not put host addresses, environment-key names, raw subprocess output, or sensitive fixture values into committed closure artifacts when the privacy contract forbids persisted launch evidence.
- Do not infer an orphan worker from a port alone. Resolve PID/image, interface binding, project cleanup counters, and the actual registered endpoint.
- Do not swallow timeout cleanup outcomes. Bounded waits must preserve success/error/timeout status and require process-tree termination, child close, and zero cleanup before evidence publication.
- Do not regenerate benchmark artifacts repeatedly while debugging. Fix statically, then run the mandated final execution once; if the frozen aggregate requires another run, number it explicitly.
- Do not let closure promote a candidate consumer, memory phase, custom persistence, or product claim unless a separate gate explicitly authorizes it.
