# Evalora NestJS Member 1 backend slices

Use this reference when continuing Evalora backend work or a similar standalone NestJS + Prisma backend where the user wants steady feature slices on a non-main branch.

## Operating mode

- Work on the feature branch requested by the user (`backend-core` in the Evalora session), not `main`.
- When the user says "proceed" / "to the next task", continue the next documented backend slice immediately; do not ask for another confirmation.
- Make one clean conventional commit per completed slice after verification.
- If the branch is ahead of origin after a completed slice and the user says to continue with the next recommendation, push the clean verified commit before starting the next slice so GitHub stays current.
- Keep secrets redacted in reports and commands shown to the user. Use placeholders such as `DATABASE_URL='[REDACTED]'` in summaries.

## Slice loop

1. Read repo guide first: `AGENTS.md`.
2. Confirm branch and clean state: `git status --short --branch`.
3. Pick the next documented Member 1 slice from `docs/MEMBER-1-CORE-SYSTEM.md` / `docs/API-MODULES.md`.
4. Add a focused service-level test first, using a fake Prisma-shaped object so tests do not require Neon credentials.
5. Run the targeted test and verify RED. Expected first failure is usually a missing service/module import.
6. Implement the service and DTO mapping behind a repository/service seam.
7. Wire controller + `AppModule` provider only after service tests pass.
8. Update API/module/member docs when route shape or behavior changes.
9. Run full verification:
   ```bash
   pnpm test && pnpm typecheck && pnpm lint && pnpm build && DATABASE_URL='postgresql://user:password@ep-demo.neon.tech/evalora?sslmode=require' pnpm prisma:validate
   ```
10. Smoke-test non-DB routes with `SKIP_DATABASE_CONNECT=true`, then kill the server.
11. Check for absolute local paths in committed docs.
12. Commit only the files for that logical slice.

## TDD service seam pattern

For Prisma-backed slices, tests should instantiate the service directly:

```ts
const service = new FeatureService({
  modelName: {
    create: async (args) => { /* assert/store args */ return row; },
    findMany: async (args) => [row],
  },
});
```

This validates Prisma `data`, `where`, `include`, and `orderBy` shapes without live database credentials.

## Completed Evalora slice order that worked

- Runtime config: DeepSeek V4 Flash + Neon Postgres, safe redaction.
- AI evaluation/report aggregation.
- Report persistence (`Evaluation` + `CandidateReport`) with graceful skipped/failed persistence.
- Persisted report readback: `GET /api/reports/:sessionId` should check access first, read `CandidateReport` with session candidate/template metadata when present, map Json fields back to the report DTO, and fall back to generated report data only when no persisted row exists or readback is unavailable.
- Auth register/login adapted from Coorad: normalize email, bcrypt hash/verify, JWT role claims, no password hash in responses.
- JWT guard/RBAC helpers.
- Template persistence: nested `AssessmentTemplate -> AssessmentModule -> Question` create/update/list/get/delete.
- Session persistence: generated access codes, candidate/template linkage, status/timestamps.
- Response persistence/autosave: create or update by `sessionId + questionId`, list by session.
- Ownership hardening: reusable access context helper; scoped template/session/response Prisma `where` clauses by `role`, `organizationId`, and `candidateId`.

## Ownership hardening pattern

For persisted NestJS + Prisma resources, add ownership after basic persistence is green:

1. Extend JWT/auth context to include optional `organizationId` when users belong to an organization.
2. Add a shared access helper rather than duplicating controller logic. Evalora used `src/modules/auth/access-control.ts` with:
   - `toAccessContext(request.user)`;
   - `buildTemplateOwnershipWhere(access)`;
   - `buildSessionOwnershipWhere(access)`;
   - `mergeWhere(...)`.
3. Keep ownership checks in services, not only controllers, so tests can assert exact Prisma query scopes.
4. TDD expected Prisma shapes with fake clients:
   - templates: organization/interviewer users add `{ organizationId: access.organizationId }`; admins add no extra scope;
   - sessions: candidates add `{ candidateId: access.userId }`; organization/interviewer users add `{ organizationId: access.organizationId }`;
   - responses: list with `{ session: <session ownership scope> }` and check parent session access before autosave writes.
5. Controllers should only convert `request.user` to access context and pass it through.
6. Smoke-test with a JWT that includes `organizationId`, then verify `/api/auth/me` returns it and protected routes still return `401` without a token.

Pitfall: organization/interviewer scoping depends on a durable `organizationId` in the JWT/user record. If absent, fail closed with `403` rather than querying broadly.

## Persisted report readback pattern

For report APIs that already generate and persist `CandidateReport` rows, make readback the next slice:

1. RED: add a service test where `getReport(sessionId, access)` first calls `interviewSession.findFirst` for ownership and then `candidateReport.findUnique({ where: { sessionId }, include: { session: { select: { completedAt, candidate: { select: { name } }, template: { select: { title } } } } } })`.
2. GREEN: map the persisted row into the existing report DTO (`candidateName`, `assessmentName`, `completedAt`, `overallScore`, `moduleScores`, `summary`, `strengths`, `improvementAreas`, `evidence`, `reviewerSummary`, advisory notice).
3. Preserve fallback behavior: if there is no persisted row or the readback fails, return the generated fallback report shape rather than crashing the UI path.
4. Keep the authorization order strict: check JWT/RBAC ownership before reading report data.
5. Update API/member docs to state that `GET /reports/:sessionId` prefers persisted data and falls back only when no saved report exists.

## Nest/TypeScript verification pitfall

Hermes file writes may run single-file TypeScript checks that report decorator-signature errors because they are not using the project `tsconfig` context. Treat those as a warning only if the canonical project checks pass:

```bash
pnpm typecheck
pnpm lint
pnpm build
```

Do not stop on the single-file decorator noise; run the full project command immediately and fix only real project-level failures.

## Smoke-test pattern

Use Hermes background process tracking, not shell `&` in a foreground terminal call:

```bash
SKIP_DATABASE_CONNECT=true DATABASE_URL='postgresql://user:password@ep-demo.neon.tech/evalora?sslmode=require' JWT_SECRET='smoke-secret' PORT=4307 pnpm start
```

Then verify:

```bash
curl -s http://localhost:4307/api/health
curl -s -o response.json -w '%{http_code}' http://localhost:4307/api/protected-route
```

For protected routes, an unauthenticated `401 Authentication required.` is a valid smoke check that guards are active. Always kill the background server after the check.

## Commit pattern

Use conventional commits matching the slice:

```bash
git add <slice files> && git commit -m "feat(responses): persist candidate autosaves"
```

Avoid catch-all commits after the user asked for clean step commits. If earlier uncommitted work exists, split it by logical slice before continuing.
