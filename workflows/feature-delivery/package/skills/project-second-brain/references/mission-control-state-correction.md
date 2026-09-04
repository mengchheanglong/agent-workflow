# Mission Control State Correction Pattern

Use when a project second brain / Mission Control workspace points to stale work after the implementation has moved on.

## Trigger signals

- User says the current task is wrong, stale, or refers to different project folders.
- `.active/CURRENT.md` / `.active/NEXT.md` says to run a mission, but implementation repo history or mission `REVIEW.md` shows it already landed.
- `.active/STATE.json` names an active mission but `mission-control/missions/<mission>/` does not exist.
- The user corrects a broad product path, e.g. “PWA was already tried; native Android is why we are here.”

## Procedure

1. Read routing state first:
   - `AGENTS.md`
   - `.active/CURRENT.md`
   - `.active/NEXT.md`
   - `.active/STATE.json`
   - relevant mission `REVIEW.md` files
2. Cross-check implementation repos with real evidence:
   - `git status -sb`
   - recent commits
   - completed artifacts/review docs
3. State the conflict explicitly: “Mission Control says X, but repo/review shows X is already done.”
4. Patch active files:
   - `.active/CURRENT.md`
   - `.active/NEXT.md`
   - `.active/STATE.json`
   - `.active/DECISIONS.md` if this is a durable path correction
5. If the corrected active mission has no package, create:
   - `MISSION.md`
   - `SPEC.md`
   - `TASKS.md`
   - `EVIDENCE-GATES.md`
   - `BUILDER-HANDOFF.md`
   - `REVIEW.md`
   - `artifacts/README.md`
6. Patch indexes:
   - `mission-control/README.md`
   - `mission-control/missions/README.md`
7. Verify with an ad-hoc temp script when no canonical test exists:
   - create under OS temp dir with `hermes-verify-` prefix;
   - parse `.active/STATE.json`;
   - assert active mission path exists;
   - assert routing files agree;
   - assert stale paths are blocked;
   - delete the temp script;
   - report as “ad-hoc static verification only.”

## Pitfalls

- Do not answer “what next?” from recent chat momentum; routing files may be stale and implementation may be newer.
- Do not only patch `.active/STATE.json`; Mission Control README/index files can still route future agents to the old path.
- Do not create a narrow one-session skill for a specific project. Put project-specific details in this reference and keep the umbrella skill class-level.
- Do not claim suite-green for markdown/JSON routing changes when only static consistency was checked.
