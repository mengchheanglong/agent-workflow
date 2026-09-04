# Evalora invite-only candidate flow

Use this when continuing Evalora backend work around roles, auth, sessions, or candidate assessment entry.

## Durable role model

- Admin and interviewer/organization users are platform users with JWT login.
- Public registration should create interviewer/organization-user accounts only.
- Admin accounts are private/seeded/team-created, not public self-registration.
- Candidates are invitation/access-code participants, not platform-login users.
- Candidate access should end after session completion or expiry, while admins/interviewers retain candidate/session/response/evaluation/report data.

## Backend implementation pattern

1. Add tests first for the role invariant:
   - public register defaults to interviewer;
   - public admin registration is rejected;
   - public candidate registration is rejected;
   - candidate records cannot log in through `/auth/login`;
   - access-code session lookup/start/complete works without JWT while active;
   - access-code response autosave/listing works without JWT while active;
   - completed/expired access codes are rejected.
2. Keep platform routes scoped to `admin`, `organization`, and `interviewer` roles.
3. Put candidate-facing routes under explicit access-code controllers, e.g.:
   - `GET /api/sessions/access/:accessCode`
   - `PUT /api/sessions/access/:accessCode/start`
   - `PUT /api/sessions/access/:accessCode/complete`
   - `POST /api/responses/access/:accessCode`
   - `GET /api/responses/access/:accessCode`
4. Session creation may accept either an existing `candidateId` or `candidateName` + `candidateEmail`.
5. If creating/reusing candidate rows, store them as invite-only `CANDIDATE` records with random password hashes and block login for that role.
6. For access-code reads/writes, normalize the code, fetch the session, and reject when status is `COMPLETED`/`EXPIRED` or `expiresAt` has passed.
7. Do not expose final AI reports to candidates in the MVP; reports remain admin/interviewer-only.
8. Update docs together: SRS, API contract, API modules, database design, README/member notes.

## Regression tests to add

In addition to service tests, pin route-level access so the intended role model cannot silently drift:

- Add a controller metadata test using `reflect-metadata` + `ROLES_KEY` to assert JWT platform routes list only `admin`, `organization`, and `interviewer`.
- Assert candidate access-code controllers have no `@Roles` metadata and stay public/invite-code based.
- Keep older service ownership tests only if they still represent platform users; if a test mentions candidate JWT ownership, rewrite it around access-code behavior or treat it as legacy coverage that must not drive controller access.

Example route metadata check:

```ts
import "reflect-metadata";
import { ROLES_KEY } from "../src/modules/auth/auth.guard";
import { ResponsesController } from "../src/modules/responses/responses.controller";

assert.deepEqual(Reflect.getMetadata(ROLES_KEY, ResponsesController.prototype.submit), [
  "admin",
  "organization",
  "interviewer",
]);
```

## Live smoke pattern

For high-risk invite-only changes, add a temporary Prisma/tsx smoke script under `scripts/tmp-*.ts`, run it against `.env` without printing secrets, then remove it before the final gate. The smoke should prove:

- interviewer/platform user can create a session from candidate name/email;
- opened access code returns template/modules/questions;
- candidate can save/reload active responses by access code;
- candidate access is blocked after completion/expiry;
- candidate login through `AuthService.login` is blocked;
- admin/interviewer-scoped read still retains the saved response after candidate access closes.

Only report booleans/counts/roles, never tokens, passwords, database URLs, or API keys.

## Verification

Run targeted gates after the slice, then full gates before commit:

```bash
pnpm test -- auth.service sessions.service responses.service templates.service responses.controller
pnpm typecheck
pnpm test
pnpm typecheck
pnpm lint
pnpm build
pnpm prisma:validate
pnpm prisma:generate
pnpm seed:prebuilt
```

Also scan protected route decorators so `candidate` does not remain on JWT platform routes by accident; candidate access should go through `/access/:accessCode` routes. Run `git diff --check`, a staged secret-pattern grep, and remove any temporary smoke files before committing.

## Pitfall

Hermes single-file TypeScript syntax checks may report Nest decorator errors outside the project tsconfig. Treat canonical `pnpm typecheck`, `pnpm lint`, and `pnpm build` from the repo root as authoritative.