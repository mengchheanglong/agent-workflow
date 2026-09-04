# Next.js subdomain-first public-route slice

Use when building a small Next.js app that needs Angkoro-style tenant/business subdomain routing plus a path fallback.

## Slice shape

1. Add tests first for pure routing behavior:
   - root domain stays platform context;
   - reserved subdomains such as `www`, `app`, `api`, `dashboard`, `auth`, `m`, and `s` stay platform context;
   - `<slug>.<rootDomain>/path` rewrites to `/s/<slug>/path`;
   - `<slug>.localhost:3000` works for local dev;
   - invalid/reserved business slugs are rejected.
2. Implement a pure helper such as `resolveTenantRoute({ host, pathname, rootDomain })` outside Next runtime so Vitest can cover it without a running server.
3. Add `proxy.ts` for Next.js 16+ rather than `middleware.ts`; export `function proxy(request: NextRequest)` and `config.matcher`.
4. Keep both route families working:
   - external primary: `https://<slug>.domain/...` → internal `/s/[slug]/...`;
   - fallback: `/m/[slug]/...`.
5. Smoke-test both forms in browser:
   - `http://localhost:3000/m/demo`;
   - `http://demo.localhost:3000/`.

## Next.js 16 notes

- Next.js 16 deprecates `middleware.ts` in favor of `proxy.ts`. If both exist, Next errors; keep only `proxy.ts`.
- If `typedRoutes` was enabled and then removed, stale `.next/types/link.d.ts` can keep causing `RouteImpl` string-href type errors. Remove the stale `.next` folder, then rerun `pnpm typecheck`/`pnpm build`.
- If the app lives under a parent directory with another lockfile, set `turbopack.root: process.cwd()` in `next.config.ts` to stop workspace-root inference warnings.
- If deleting `.next` while a dev server is running, restart the dev server before browser QA. Otherwise the dev server can return empty/500 pages from missing `.next/dev/*` manifests.

## Verification pack

Run:

```bash
pnpm test
pnpm typecheck
pnpm lint
pnpm build
```

Then browser-smoke:

```text
/m/<slug>
/m/<slug>/item/<itemSlug>
http://<slug>.localhost:3000/
```

Inspect console errors after each smoke route.
