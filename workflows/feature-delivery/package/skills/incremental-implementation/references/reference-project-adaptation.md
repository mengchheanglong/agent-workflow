# Reference-project adaptation pattern

Use when the user points at an existing project and says to copy/adapt the logic even if the framework differs.

## Pattern

1. Read the active repo's `AGENTS.md` / project guide first.
2. Inspect the reference repo's local routing docs if present, but do not modify the reference repo.
3. Read only the relevant source files from the reference project. Avoid `.env*`, credentials, generated files, and dependency folders.
4. Extract durable logic or UX structure, not framework shape. Example for auth:
   - normalize email before lookup;
   - hash password before storing;
   - verify password with bcrypt/argon before login;
   - sign JWT with user id/email/role claims;
   - never return password hashes;
   - use generic auth errors where practical;
   - keep refresh tokens, lockout, verification, and reset flows as separate slices unless asked.
5. When adapting a reference UI/dashboard, map the reference features into the target product's current scope before coding:
   - list the reference patterns to copy (for example sidebar/header, KPI cards, card panels, list shape, settings/share layout);
   - list reference modules to exclude (for example orders, payments, analytics, team/roles, inventory, subscriptions) when they exceed the target wedge;
   - add a regression test or helper assertion that the target navigation/scope does not expose excluded modules;
   - keep reference paths out of user-facing production docs except in explicit internal learning notes.
6. For reference assessment/test-taking UIs, preserve the target product's role/access model before copying layout. If candidates join by invite/access code only, adapt the reference into a focused candidate surface with no normal dashboard/app sidebar, no candidate account links, and copy that says AI/automated scoring supports human review rather than making final hiring decisions. If a member/reference repo has a coding module, prefer extracting durable behavior (challenge navigator, prompt/test cases, editor, run/submit, hidden-test result review, progress) into a target-native component instead of importing the whole standalone app shell.
7. Preserve the target project's architecture. For NestJS, wrap logic in services/repositories and wire controllers/providers through the module instead of copying Express controllers directly. For UI projects, create target-native primitives/components instead of importing reference component trees wholesale.
7. Keep secrets out of docs and output. Use placeholders or `[REDACTED]`.
8. Add tests before implementation that pin the adapted logic or scope boundary. Prefer repository boundaries/fakes so tests do not require live database credentials.
9. Update the target repo's API/module/docs with what was adapted and what remains out of scope.
10. Run full verification from the target repo after the slice: tests, typecheck, lint, build, and browser smoke for touched routes/UI when relevant.

## Pitfalls

- Do not blindly copy reference framework code. Copy behavior and security invariants.
- Do not include reference paths in committed docs if the target project will be used by multiple machines.
- Do not collapse large mature auth systems into one slice. Refresh tokens, token blacklist, login lockout, email verification, and password reset should be separate tested slices.
