# Next.js + Supabase real-data replacement slice

Use this after the Supabase SSR foundation exists and the user asks to remove static/demo data from public or owner-facing routes.

## Slice boundary

Replace fake arrays with real Supabase-backed reads, but keep the slice read-focused unless the user explicitly asks for editable CRUD/auth in the same step.

Good scope:

- schema/RLS SQL files for the MVP tables;
- deterministic seed SQL for one testing store/owner;
- server-side repository helpers that read Supabase rows;
- pure mapper functions from Supabase rows to existing UI/view models;
- UI route conversion from sync/static helpers to async server reads;
- a visible missing-seed/admin-not-applied state for owner/admin pages;
- public customer routes should still 404 for missing/unpublished stores.

Out of scope unless requested:

- service-role/admin keys in app code;
- Prisma/direct database URLs;
- owner login enforcement;
- create/edit/delete forms;
- image upload/storage;
- orders/payments/analytics breadth.

## Recommended TDD sequence

1. Add mapper tests first. Use plain row fixtures and assert the existing UI shape, sorting, fallback labels, price formatting, and contact links.
2. Replace the old static query tests with async reader-injection tests. Pass a fake `readStore(slug)` so tests do not require live Supabase credentials.
3. Implement mapper + repository behind the old UI-facing helper names where possible.
4. Convert route components to `async` and `await` the helpers.
5. Add missing-data owner/admin UI before removing the final static fallback. Do not silently fall back to demo arrays once the task is to use real data.
6. Delete obsolete static data files and scan for stale imports/labels.
7. Run canonical gates and browser-smoke both the seeded-success expectation and the missing-seed behavior when DB admin credentials are unavailable.

## Client/server boundary pitfall

In Next.js App Router, do not let client components import modules that import server-only Supabase helpers (`next/headers`, cookies, server repositories), even indirectly through a shared helper file.

Pattern:

```text
lib/dashboard/owner-dashboard.ts              server/data helpers; may import Supabase repository
lib/dashboard/owner-dashboard-navigation.ts   client-safe pure navigation/static UI helpers
components/.../client-shell.tsx               imports only client-safe modules
app/.../layout.tsx or page.tsx                server component loads data and passes serializable props to client shell
```

If `next build` reports `next/headers` being pulled into a Client Component Browser/SSR trace, split pure UI helpers from server data helpers and rerun the full build.

## Supabase admin limitation

A publishable key can read rows allowed by RLS; it cannot create tables or seed data. Before claiming live DB setup is complete, verify whether one of these is available:

- Supabase CLI with project linked and auth token;
- database URL/direct URL with privileges;
- service/admin workflow explicitly allowed by repo policy;
- user-run SQL editor path.

If only the publishable key exists, create the migration/seed files and say the remote project still needs those SQL files applied with DB/admin privileges.

## Verification checklist

- `pnpm typecheck && pnpm lint && pnpm test && pnpm build`
- source scan: no old static data imports/references remain;
- browser smoke owner dashboard routes: real data if seeded, clear missing-seed state if not;
- browser smoke public route: public menu loads if seeded; missing/unpublished stores 404;
- console clean for touched browser routes;
- docs/env examples updated without printing secrets.
