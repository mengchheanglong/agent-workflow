# Vision Mission Control: Correcting to an Existing Active Implementation

Use when a vision/research corpus has been organized into Mission Control, but the user corrects that an implementation already exists elsewhere.

## Durable lesson

Do not let the Mission Control scaffold create duplicate implementation targets. If the user names an existing active repo/path, immediately promote that path as the implementation target, even if the folder name suggests archive/retired status.

## Procedure

1. Treat the user's correction as authoritative active-state correction.
2. Inspect the named implementation repo before planning new work:
   - verify path exists;
   - read README/package/config;
   - check git top-level and status;
   - inspect active diff before editing;
   - run existing verification scripts if safe.
3. Patch Mission Control:
   - `.active/STATE.json` gets `implementation_repo` and next action;
   - `.active/CURRENT.md` states the correction;
   - `.active/NEXT.md` points at the existing repo;
   - mission `SPEC.md`, `TASKS.md`, `EVIDENCE-GATES.md`, `BUILDER-HANDOFF.md`, and `REVIEW.md` stop telling agents to create a new repo.
4. Add lightweight local context to the implementation repo only when useful:
   - `AGENTS.md` if it should be committed/shared;
   - `.active/` for local Hermes recovery, ideally ignored via `.git/info/exclude` if private.
5. Verify against the existing app, not the imagined greenfield target:
   - run test/lint/build commands from the real repo;
   - perform browser/manual smoke if relevant;
   - record results back into Mission Control `REVIEW.md`.

## Pitfalls

- Do not infer inactive status from folder names like `archive`, `retired`, or `old` when the user says the project is current.
- Do not create a duplicate app just because the mission scaffold originally proposed one.
- Do not reset or overwrite uncommitted work while correcting context.
- Do not let raw vision-corpus documents override the active mission state.

## Example pattern

A research workspace says the first mission should create a clean `digital-twin-v0` app. The user corrects: the active app is actually `C:/Users/User/archive/retired/digital-twin`. Correct response:

- update Mission Control to target that path;
- add repo-local agent context;
- run its existing `pnpm test`, `pnpm lint`, `pnpm build`;
- browser-smoke the existing app;
- record evidence and remaining manual smoke gaps.
