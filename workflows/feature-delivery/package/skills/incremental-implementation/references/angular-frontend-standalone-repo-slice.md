# Angular frontend standalone repo slice

Use when scaffolding a frontend repo that will be pushed/cloned independently from backend/shared docs.

## Workflow

1. Make the frontend folder a standalone repo root:
   - `package.json`
   - lockfile for the chosen package manager
   - `.gitignore`
   - `.env.example`
   - `README.md`
   - `AGENTS.md`
   - compact `PROJECT-CONTEXT.md`
   - local `docs/` copies of API contract / SRS extracts needed by frontend agents.
2. Replace machine-local paths before finalizing:
   - bad: `C:/Users/User/projects/collabai-frontend`
   - good: `.` for this repo, `../collabai-backend` for sibling backend, `../collabai` only if a shared-docs repo exists.
3. Verify by scanning text files for local absolute path fragments before handoff.
4. If the user says to use a specific package manager, encode it in `packageManager` and docs/run commands. Do not leave npm commands in a pnpm repo.
5. Extract attached SRS/reference docs into `docs/` when they define the project requirements, then summarize current scope in `PROJECT-CONTEXT.md`.

## pnpm + Angular package pinning pattern

When using pnpm for Angular:

- clean interrupted npm artifacts first: `rm -rf node_modules .angular dist package-lock.json`;
- pin Angular packages to a mutually published set across `@angular/core`, `@angular/cli`, `@angular/build`, `@angular/compiler-cli`, `@angular/cdk`, and `@angular/material`;
- Material/CDK may lag core patch versions, so query versions and pin to a common stable patch rather than assuming all Angular packages publish the latest core patch;
- run `pnpm install`, `pnpm typecheck`, and `pnpm build` before claiming the scaffold works.

## Visual QA gates for dashboard/project-management UIs

After build passes, run the dev server and click through the main surfaces. Check for:

- project cards clipping inside dashboard panels;
- Kanban columns overflowing behind a sticky task drawer instead of scrolling within the board area;
- task list tables becoming unreadable beside a drawer;
- team/invite side panels overflowing;
- AI suggestions list/button columns clipping.

Common CSS fixes:

- use `grid-template-columns: minmax(0, 1fr) <drawer-width>` for content + side drawer;
- set the horizontally scrollable board region to `min-width: 0`;
- use `repeat(auto-fit, minmax(..., 1fr))` for dashboard card grids;
- narrow desktop chrome/drawer/sidebar before sacrificing table readability;
- for mobile, collapse side drawers below content and use bottom navigation with 3–5 primary destinations.

## Reporting

Report real verification evidence:

```bash
pnpm install
pnpm typecheck
pnpm build
```

Also mention visual browser smoke checks if performed, and name any UX issues fixed during the pass.
