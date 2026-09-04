---
name: incremental-implementation
description: "Build in thin vertical slices: implement → test → verify → commit. Each slice leaves the system working. Never write >100 lines before testing."
version: 1.0.0
author: Adapted from addyosmani/agent-skills (53K stars)
metadata:
  hermes:
    tags: [implementation, incremental, slicing, quality, workflow]
---

# Incremental Implementation

Build in thin vertical slices — implement one piece, test, verify, commit. Each increment leaves the system in a working, testable state. Never write > ~100 lines before testing.

## When to Use

- Multi-file changes
- New feature from a task breakdown
- Refactoring existing code
- Any time you're tempted to write a lot before testing

**When NOT:** Single-file, single-function changes with minimal scope.

## The Increment Cycle

```
Implement → Test → Verify → Commit → Next slice
```

For each slice:
1. **Implement** the smallest complete piece
2. **Test** — run the suite or write a test
3. **Verify** — tests pass, build succeeds
4. **Commit** — descriptive message
5. **Next slice** — carry forward

When a delegated coding agent times out, stalls after writing files, loses its final report, or leaves incomplete TDD evidence, follow [`references/bounded-agent-slice-recovery.md`](references/bounded-agent-slice-recovery.md): preflight CLI/model compatibility, preserve and inspect the partial diff, independently run every gate, make only narrow scoped repairs, and label missing RED console evidence as unproven rather than reconstructing it.

For frozen, time-boxed incumbent/conformance benchmarks with strict line caps, fault injection, privacy scans, and rejection stop rules, follow [`references/frozen-conformance-benchmark.md`](references/frozen-conformance-benchmark.md). It covers RED/GREEN evidence, delegated-agent containment, Windows external-kill cleanup, runtime/datasource recovery-order diagnosis, isolated-versus-cascading failure reporting, and `INCUMBENT_REJECTED_PENDING_ALTERNATIVE` decisions without authorizing custom infrastructure.

For strict semantic-request and technical-envelope boundaries, follow [`references/contract-boundary-tdd-slices.md`](references/contract-boundary-tdd-slices.md): prove approved-client and raw-ingress paths separately, require fixed data-free errors plus zero-side-effect oracles, add one compatibility dimension per RED, preserve hard line-budget headroom during REFACTOR, and freshness-check delegated-agent evidence before commit.

## Slicing Strategies

### Vertical Slices (Preferred)
One complete path through the stack per slice:

```
Slice 1: Create task (DB + API + UI) → user can create
Slice 2: List tasks (query + API + UI) → user can view
Slice 3: Edit task → user can modify
Slice 4: Delete task → full CRUD
```

### Risk-First Slicing
Implement the riskiest piece first:

```
Slice 1: Prove WebSocket works (highest risk)
Slice 2: Build real-time updates on proven connection
Slice 3: Add offline support
```

If Slice 1 fails, you avoid wasting effort on later slices.

## Implementation Rules

### Provider/API Migration Slice

When replacing an API provider across an app (for example Gemini → DeepSeek), treat it as an implementation slice with explicit inventory and verification. Use `references/provider-migration.md` for the checklist and known quirks:

- inventory env vars, endpoint URLs, SDK imports, response interfaces, fallback models, docs, and UI branding before editing;
- add one shared provider client instead of duplicating raw `fetch` calls;
- preserve existing prompt/fallback behavior unless the user asked for behavior changes;
- update project `.env`, `.env.example`, docs, and visible strings together, without printing secrets;
- verify with provider smoke call, typecheck, tests, production build, and a source scan showing zero stale provider references outside ignored/generated dirs.

### Reference-project adaptation

When the user points at an existing project and asks to copy/adapt the logic, inspect that reference but preserve the target project's architecture. See `references/reference-project-adaptation.md` for the detailed checklist.

Core sequence:

1. Read the active repo's `AGENTS.md` / project guide first.
2. Read any routing docs for the reference workspace, but do not modify it.
3. Inspect only relevant source files; avoid `.env*`, generated files, dependencies, and secrets.
4. Extract behavior, security invariants, or UX structure — not framework-specific controller/component trees.
5. Before coding, map the reference features into the target product's current scope and explicitly list mature reference modules that remain out of scope.
6. Add tests against the target project's desired behavior/scope before implementation.
7. Use target-appropriate seams such as services/repositories or local UI primitives so tests can run without live credentials and the app remains target-native.
8. Document what was adapted and what mature reference features remain out of scope.
9. Verify with the target repo's canonical gates plus browser smoke for touched UI routes when relevant.

For auth specifically: normalize email, hash passwords, verify login password, sign JWT with role claims, never return password hashes, and split refresh tokens / lockout / email verification / password reset into separate slices unless explicitly requested.

### Rule -1: Prove Utility Before Integration

When the user asks whether to adapt/integrate an external tool, reference project, UI surface, or optional subsystem, run a thin usefulness gate before investing in implementation:

1. Create an isolated temporary checkout/sandbox; do not modify the core project first.
2. Run the tool's own health/help/doctor path, then one bounded smoke run against a small representative input.
3. Judge by produced artifacts, not by successful setup alone. A useful gate should produce the artifact class the core project would consume.
4. If the smoke run fails to produce useful artifacts, do not integrate. Document the gate result and add a no-go note in the agent/operator docs so future agents do not retry blindly.
5. Only after the gate passes should you implement the smallest adapter or workflow slice.

This is especially important when removing or avoiding UI work: delete stale frontend/code paths and stale docs/specs together, then verify the remaining CLI/artifact path end-to-end.

### Rule 0: Simplicity First

Before writing: *"What is the simplest thing that could work?"*

```
✗ Generic EventBus for one notification → ✓ Direct function call
✗ Abstract factory for two components    → ✓ Two components with shared utils
✗ Config-driven form builder for 3 forms → ✓ Three form components
```

### Rule 0.5: Scope Discipline

Touch ONLY what the task requires. If you notice something worth improving outside scope:

```
NOTICED BUT NOT TOUCHING:
- src/utils/format.ts has unused import (unrelated)
→ Want me to create a task for this?
```

### Rule 1: One Thing at a Time

Each increment changes one logical thing. Don't mix a new feature with a refactor and a config change in one commit.

### Rule 2: Keep It Buildable

After each increment, the project MUST build and existing tests MUST pass.

### Rule 3: Feature Flags

If the feature isn't ready for users but needs merging:

```python
ENABLE_FEATURE = os.getenv("ENABLE_FEATURE", "0") == "1"
if ENABLE_FEATURE:
    new_feature()
```

### Rule 4: Commit Often

Each slice gets its own commit. If a slice breaks something, you can revert one commit instead of unpicking a mega-commit.

### Dirty-worktree scoped commits

When unrelated work is already modified—or requested and unrelated hunks overlap in the same files—do not stage whole files blindly. Follow [`references/staged-snapshot-verification.md`](references/staged-snapshot-verification.md): isolate mixed-file content in the Git index, export the staged diff into a detached worktree at clean `HEAD`, run the canonical gate there, then commit only after that exact snapshot passes. This is the required proof that the commit does not secretly depend on unstaged work.

For this user, when a slice is verified as correct in a GitHub-backed project, commit and push immediately without pausing for permission, then continue to the next documented task. The expected closeout loop is: full project gate + relevant smoke checks → remove generated artifacts → stage only intended files → `git diff --cached --check` + staged stat review → conventional commit with verification evidence → `git push` → confirm clean status and pushed hash → continue.

## Ad-hoc verification scripts

When a project has no canonical suite, or the runtime explicitly asks for a focused temporary verifier, create a `hermes-verify-*.sh` script under the OS temp directory, run targeted assertions plus the smallest relevant lint/typecheck/build/smoke commands, and clean it up. Report this as **ad-hoc verification**, not “suite green.”

On Windows hosts using Git Bash/MSYS, create, execute, and clean the temp script from the same shell so native temp paths and `/c/...` paths do not drift. See `references/windows-temp-verification.md` for the known-good pattern and reporting checklist.

## Multi-repository project scaffolds

When the user says folders will be pushed separately, make each folder a standalone repo: its own `package.json`, lockfile, `.gitignore`, README, `AGENTS.md`, and copied/adapted shared docs. Remove parent-relative doc links such as `../docs/...` and verify each folder independently from its own working directory.

If the repo is intended for GitHub/team sharing, remove machine-local absolute paths from docs/state files before handoff. Prefer `.` for the current repo and sibling paths like `../frontend-repo` / `../backend-repo`; then scan text files for local path fragments to verify portability.

If you initially created a combined parent workspace and the user clarifies they need sibling repos, move/archive the combined folder out of the active workspace so only the intended repo roots remain visible. Add a compact `PROJECT-CONTEXT.md` in each repo explaining ownership boundaries, tech stack, run/verify commands, and "read AGENTS.md first" for future agents.

When provider/database choices change during scaffolding, capture them in `.env.example`, `AGENTS.md`, README, source-of-truth docs, and a typed runtime/config helper that redacts secrets. Add tests for default provider/model and secret redaction before implementing the helper.

For Next.js 16 subdomain-first public-route slices, use `references/nextjs-subdomain-first-slice.md`: write pure routing tests first, implement `proxy.ts` host rewrites to internal `/s/[slug]` routes while preserving `/m/[slug]` fallback routes, account for reserved platform subdomains, and clear stale `.next` route types/restart dev server when changing typed route/proxy config.

For Next.js + Supabase SSR foundation slices, use `references/nextjs-supabase-ssr-foundation.md`: install the Supabase SSR packages with the repo's package manager, add browser/server/session-refresh helpers, integrate session refresh into the existing `proxy.ts`/`middleware.ts` without breaking rewrites, keep service/database/admin setup out of scope unless explicitly requested, redact secrets, and verify with canonical gates plus route smoke tests.

For Next.js + Supabase real-data replacement slices, use `references/nextjs-supabase-real-data-slice.md`: write mapper tests and async reader-injection tests first, add schema/RLS plus deterministic seed SQL, replace static/demo reads with server-side Supabase repositories, add owner/admin missing-seed states instead of silently falling back to fake data, split client-safe UI helpers from server data helpers to avoid `next/headers` entering client bundles, and verify with canonical gates plus browser smoke.

For protected owner dashboards where authenticated users may not yet own a store/workspace, use `references/nextjs-supabase-owner-onboarding.md`: TDD the pure first-store payload and injected writer order, upsert the owner profile, insert one draft `stores`/workspace row with `owner_id = auth.uid()` under normal RLS, keep category/item CRUD and image uploads out of scope, and avoid catching Next.js `redirect()` as a generic server-action error.

For Next.js + Supabase owner menu/catalog dashboards, use `references/nextjs-supabase-owner-menu-crud.md`: build thin TDD-backed slices for category CRUD, menu-item text CRUD, publish/unpublish controls, and item image upload/storage; keep writes owner-scoped through `stores.owner_id = auth.uid()`, validate child ownership in pure helper seams before Supabase writes, add Storage bucket/policies for public item images only when media is in scope, and verify each slice with `pnpm check` plus protected-route/public-route browser smoke before committing and pushing.

For Angular frontend standalone repos, pnpm package-manager preference, SRS extraction, common Angular package pinning, and visual QA gates for dashboard/Kanban/task-drawer layouts, see `references/angular-frontend-standalone-repo-slice.md`. When hardening a repo for teammates after clone, treat onboarding as a verified slice: add/verify `packageManager`, Node/pnpm `engines`, `.nvmrc`, clear README quick-start commands, `dev` and `check` scripts, and pnpm v10 `onlyBuiltDependencies` approvals for Angular/Vite native packages such as `esbuild`, `@parcel/watcher`, `lmdb`, and `msgpackr-extract` when install warns about ignored build scripts. Remove stale scaffold instructions like `ng new` once the repo already contains the app. Verify `pnpm install --frozen-lockfile`, `pnpm check`, and a real `pnpm dev` smoke run.

For Angular UI polish that includes clickable-looking controls, also use `references/angular-interaction-qa.md`: before claiming the slice is functional, browser-test every visible control in the touched area (workspace switchers, `+` buttons, cards, menus, tabs, submit/cancel actions), confirm the expected user-visible state change, check console errors, and rule out stale dev servers when behavior does not match edited source. When smoke-testing documented npm/pnpm scripts, run the exact command teammates will run; do not test custom extra args through a preconfigured script unless that usage is documented and verified, because CLI arg forwarding can fail differently from the normal path. For replacing app logos from user-provided images, see `references/angular-logo-asset-replacement.md`: inspect whether transparency is real or a baked checkerboard, create committed assets under Angular's public asset path, update all visible brand marks and favicons together, then verify with build plus browser visual inspection. For replacing a sidebar/header icon + text with a supplied full wordmark SVG, also see `references/angular-logo-wordmark-replacement.md`: compare multiple attachments visually, render SVGs in-browser if vision cannot read them directly, copy the chosen wordmark into `public/`, replace separate icon/text nodes with one `<img>`, update responsive/mobile brand markup, and search for stale brand classes/assets before verifying. For SVG favicons from large-canvas logo exports, see `references/angular-favicon-svg-crop.md`: copy to `public/favicon.svg`, link it as `image/svg+xml`, tighten the root `viewBox` until the logo is recognizable at tab size, and verify the crop from the app origin plus `pnpm check`.

For screenshot-driven UI cleanup, treat the visible target literally: remove exactly the requested card/control/text, scan for leftover template/styles/state (`search_files` for visible labels and class/function names), delete now-unused state/imports/styles, and avoid replacing the removed element unless the user explicitly asks for a replacement. If the user does ask for a replacement (for example “remove this and add a + button”), wire it to an existing behavior when available, then verify with typecheck/build plus a browser click showing the expected visible state change.

For screenshot-driven polish complaints like “don’t really like this part,” first inspect the screenshot and make a narrow local correction to the visible issue instead of redesigning the whole page. If the complaint is about hero/landing typography looking cramped or words visually merging, prefer shorter copy, looser letter spacing, and slightly more relaxed line-height before changing layout rails or the rest of the page. Verify with both desktop and mobile screenshots plus simple metrics such as overflow and touch-target size.

For owner/admin dashboards, remove stale internal roadmap/status copy from user-facing chrome immediately when spotted (for example “next slice,” “auth/roles later,” or implementation notes). Keep useful business context only where it helps the owner act; scan exact visible labels afterward to prove the internal text is gone.

For Next.js frontend work where the user points to a folder of screenshots/assets and says the app should look exactly like it, use `references/nextjs-reference-screenshot-ui-match.md`: inventory the design folder, vision-inspect every screenshot, copy supplied logos into `public/`, verify/crop large-canvas SVG exports in-browser, update shared primitives before screens, compare live browser screenshots route-by-route, then run lint/typecheck/build before commit/push. For Evalora dashboard/auth polish specifically, also use `references/evalora-frontend-dashboard-ui-calibration.md`: map dashboard widgets to the real backend/product model before copying references, use midpoint resizing when the user alternates between "too big" and "too small", keep analytics honest/advisory, and commit only the touched UI slice when the repo has unrelated local changes.

For standalone NestJS/Prisma backend slices adapted from a reference project, see `references/evalora-nest-member1-slices.md`: use repository seams for TDD without live credentials, copy auth invariants rather than framework shape, document out-of-scope mature auth features, smoke-test non-DB routes with an explicit database-connect skip flag, commit each logical slice on a feature branch instead of `main`, and add ownership hardening as a separate tested slice after basic persistence is green. The reference includes the Evalora Member 1 slice order, fake-Prisma service test pattern, scoped ownership-query pattern, smoke-test/kill-server pattern, and the project-level verification commands. Scope pitfall: when continuing Evalora work for the Member 1 user, keep next-task selection inside Member 1 backend ownership (database/core APIs, assessment modules, AI evaluation, scoring, reports, backend auth/privacy needed for those routes); do not drift into Member 4 candidate/frontend UX such as access-code/reconnect unless the user explicitly asks for that lane. If merging a code-assessment/code-execution backend branch into Evalora, use `references/evalora-backend-code-assessment-merge.md`: identify branch spelling variants, do a no-commit merge/conflict check, preserve DeepSeek/auth setup while adding Piston `CodeModule`, regenerate Prisma Client after schema changes, run canonical verification, whitespace-check Figma exports, and secret-scan `.env.example`. If the user explicitly sets or asks to fix the Evalora role model so admins/interviewers are platform users and candidates use invite/access-code only, use `references/evalora-invite-only-candidate-flow.md`: block public candidate/admin registration, make candidate records invite-only, add access-code session/response routes, close access after completion/expiry, keep reports admin/interviewer-only, and update SRS/API/database docs together. If the user says Evalora lacks “pretests” for HR/software/leader roles, or asks to expand templates after researching big-company interviews, use `references/evalora-prebuilt-assessment-seeds.md`: distinguish AI evaluation profiles from real prebuilt assessment templates, add idempotent Prisma seed definitions/scripts, keep one template per role but expand each into a researched question bank with candidate subset sizing, run TDD, seed Neon, and verify template/module/question row counts without exposing secrets.

When the user asks to stop using `main` after work already exists in the worktree, create/rename to the requested feature branch immediately, then stage and commit files by logical slice (config, AI/service logic, persistence, auth, docs, next feature) before continuing. Do not squash all prior work into one catch-up commit if the user requested clean commits for each step. For ongoing Evalora/Nest backend slices, when the user says "proceed" without asking for a plan, continue the next documented slice using TDD service seams, run targeted RED/GREEN evidence, full verification (`pnpm test && pnpm typecheck && pnpm lint && pnpm build && ... prisma:validate`), smoke-test non-DB routes with `SKIP_DATABASE_CONNECT=true`, kill the smoke server, and make one clean conventional commit on the feature branch.

Planning/dashboard pitfall: distinguish engineering slices from team-dashboard tasks. For Evalora, the user/team prefers dashboard tasks that are about one week of work and read as broad deliverables with daily progress reports underneath, not many one-day commit-sized rows like auth, templates, sessions, responses, reports, or a provider adapter. Keep fine-grained TDD/commit slices internally, but present them as daily reports/subtasks under the weekly umbrella unless the user explicitly asks for per-slice task rows. For the user's Member 1 lane, the preferred umbrella wording is `Backend Development: Core APIs, Database, Authentication, AI Evaluation & Reports`; see `references/evalora-dashboard-task-reporting.md` for wording, daily-report examples, and the Member 1 vs Member 4 boundary.

Pitfall: Hermes file-write syntax checks may show Nest decorator errors when checking a single file without the project `tsconfig`; immediately run the canonical project commands (`pnpm typecheck`, `pnpm lint`, `pnpm build`) and treat only those as authoritative before committing. After using temporary smoke files or background smoke servers, delete temp files, kill the server, then run fresh canonical verification (`pnpm test && pnpm typecheck && pnpm lint && pnpm build && pnpm prisma:validate`) before claiming the workspace is verified; stale verifier warnings should be handled by rerunning the relevant commands, not by citing earlier output.

## Hermes Integration

Pairs with `test-driven-development` (test-first per slice), `subagent-driven-development` (delegate slices to subagents when safe), and `context-engineering` (load only relevant context). For git commits, use `terminal` with `git add -A -- <files> && git diff --cached --check && git commit -m "<msg>"`.

Commit hygiene pitfall for standalone repos nested under broad parent worktrees: first verify the repo boundary from the intended project directory (`git rev-parse --show-toplevel`) and inspect both the project repo status and any parent-repo status for that path. If source-of-truth docs are ignored accidentally (for example `docs/` while `AGENTS.md` points to it), fix `.gitignore` before the initial commit. Gate commits with `git diff --cached --check && git commit ...`; do not run the whitespace check on a separate newline before `git commit`, because warnings can print while the commit still proceeds. If that happens, fix the whitespace, rerun the canonical project check, then `git commit --amend --no-edit`.
