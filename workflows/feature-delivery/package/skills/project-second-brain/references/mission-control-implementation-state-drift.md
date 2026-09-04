# Mission Control implementation-state drift

Use when a file-first Mission Control workspace points to a stale next action while a separate implementation repo has moved on.

## Trigger signals

- User says the proposed next task is already done.
- `.active/NEXT.md` says "wait for X" but implementation repo has commits/reports/CI for X.
- Mission files say a handoff is pending, but `.hermes/evaluations/`, docs, tests, or GitHub Actions show the handoff landed.
- The agent keeps answering from Mission Control without checking the implementation repo.

## Correction workflow

1. Treat the user's correction as likely true; do not argue from stale `.active/` text.
2. Inspect the implementation repo before changing Mission Control:
   - `git status -sb`
   - recent commits relevant to the named task
   - final reports under `.hermes/evaluations/` or project-plan output
   - docs/tests added by the completed task
   - CI run status when available
3. Decide the real state:
   - completed
   - active next task
   - blocked
   - parked
4. Patch the active state together:
   - `.active/CURRENT.md`
   - `.active/NEXT.md`
   - `.active/STATE.json`
   - relevant mission `MISSION.md` / `SPEC.md` / `TASKS.md` / `REVIEW.md`
   - indexes such as `mission-control/README.md` if routing would otherwise remain stale
5. Convert pending handoffs to historical references, not active blockers.
6. Promote the actual next gate in explicit terms.
7. Run a focused ad-hoc verifier when no canonical suite exists:
   - create temp script under the OS temp dir with `hermes-verify-` prefix;
   - parse/check the machine-readable state;
   - cross-check human routing files agree;
   - delete the temp script;
   - report as ad-hoc/static verification, not suite green.

## Example state transition

Bad stale state:

```text
Companion UX v2 is delegated; wait for it to return.
```

Implementation evidence:

```text
b367f3d feat: refine companion daily ux
 d903d72 feat: polish companion check-in controls
CI green for d903d72
```

Corrected state:

```text
Companion UX v2/v3 complete.
Active next task: Real Native Phone Loop Validation.
Do not start another UI polish pass before validation unless validation exposes a blocker.
```

## Pitfalls

- Do not keep a completed handoff in `delegated_work` as if it is pending; move it to `completed_*` or historical reference.
- Do not update only `.active/STATE.json`; stale Markdown routing will still mislead future sessions.
- Do not claim canonical tests passed for Markdown/JSON Mission Control edits. Use explicit ad-hoc/static verification wording.
- Do not hard-code a transient tool failure as durable truth. Capture the retry/verification pattern, not the failed first attempt.
