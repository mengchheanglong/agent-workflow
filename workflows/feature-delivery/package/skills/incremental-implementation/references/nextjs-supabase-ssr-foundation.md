# Next.js + Supabase SSR foundation slice

Use this when wiring Supabase into a Next.js App Router project that already has routing/proxy logic.

## Scope boundary

Implement only the SSR/client foundation unless the user explicitly asks for schema/auth CRUD in the same task:

- install `@supabase/supabase-js` and `@supabase/ssr` using the repo's declared package manager;
- add local public env vars and safe `.env.example` placeholders;
- create browser/server Supabase helper clients;
- refresh sessions in the existing Next route boundary (`proxy.ts` in Next 16, `middleware.ts` in older setups);
- preserve existing rewrites/tenant routing;
- verify routes still load.

Do **not** add Prisma, direct database URLs, server/admin packages, service-role keys, or migrations just because Supabase setup docs mention them. Treat those as later slices unless the current task explicitly needs database schema/admin access.

## File pattern

Preferred helper shape:

```text
utils/supabase/client.ts       browser client via createBrowserClient
utils/supabase/server.ts       server component/client helper via createServerClient + cookies()
utils/supabase/middleware.ts   request/session refresh helper via createServerClient
proxy.ts or middleware.ts      calls updateSession while preserving existing rewrites
```

For Next 16 projects using `proxy.ts`, integrate session refresh there instead of creating a competing `middleware.ts`.

## Proxy integration rule

If the app already rewrites host/path for tenants or subdomains:

1. compute the existing rewrite response first;
2. pass that response into the Supabase session-refresh helper;
3. return the helper's response;
4. otherwise call session refresh with a normal `NextResponse.next()`.

This preserves both auth cookies and route rewrites.

## Dashboard auth redirect pitfall

When protecting `/dashboard/*` or another route subtree and you need to preserve the exact post-login return path, do the unauthenticated redirect at `proxy.ts`/`middleware.ts` using `request.nextUrl.pathname + request.nextUrl.search`. A server layout guard can protect the subtree, but it usually only knows its own segment and may redirect `/dashboard/menu` back to `/dashboard` unless you pass the exact path from the request boundary.

Keep a defense-in-depth server helper for dashboard pages/layouts, but let proxy/middleware own the precise `next=` value. Add a focused test for the pure return-path builder and browser-smoke a nested route such as `/dashboard/menu?category=coffee` → `/login?next=%2Fdashboard%2Fmenu%3Fcategory%3Dcoffee`.

## Env and secret hygiene

- `.env.local` may contain local `NEXT_PUBLIC_SUPABASE_URL` and `NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY`; it must be gitignored.
- `.env.example` should contain placeholders only.
- Do not echo secret values in the final response.
- Do not commit service-role keys, `SUPABASE_SECRET_KEY`, database passwords, `DATABASE_URL`, or `DIRECT_URL` unless a server-only admin slice explicitly requires them and the repo policy allows it.
- Run a redacted scan after writing env/docs. Expected committed hits should be placeholders/imports only; real project refs/keys should appear only in ignored local env files.

## Verification

Run the canonical project gates, not single-file TypeScript diagnostics produced by file-write tools:

```text
pnpm typecheck
pnpm lint
pnpm test
pnpm build
```

Then smoke at least:

```text
/
/dashboard or protected owner shell
one public route that crosses proxy/rewrite logic
```

Check browser console for errors when UI routes are affected.

## Reporting

Report:

- packages installed/verified;
- helper files added;
- whether `proxy.ts` or `middleware.ts` was used;
- verification commands and pass/fail;
- route smoke results;
- explicit note that secrets are not repeated and service/database/admin setup was not added unless it was in scope.
