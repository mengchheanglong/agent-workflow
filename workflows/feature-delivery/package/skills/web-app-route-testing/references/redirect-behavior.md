# 307 Redirects in Next.js Route Testing

## Why 307 redirects are normal

In Next.js with middleware or auth protection, routes often return **307 Temporary Redirect** (not 401 or 403) when the user is not authenticated. This is correct behavior — the route redirects to `/signin`.

Do NOT report these as errors.

## Common auth-gated routes (OpenFullDive)

These return 307 when unauthenticated:
- `/evidence` → redirects to `/signin`
- `/admin` → redirects to `/signin`
- `/methodology` → redirects to `/signin`
- `/library` → redirects to `/signin`
- `/predictions` → redirects to `/signin`
- `/scenarios` → redirects to `/signin`
- `/radar` → redirects to `/signin`
- `/signal` → redirects to `/signin`
- `/sources` → redirects to `/signin`
- `/settings/account` → redirects to `/signin`
- `/canon/contribute` → redirects to `/signin`
- `/admin/canon` → redirects to `/signin`
- `/organizations/propose` → redirects to `/signin`

## Testing auth-gated routes

### Follow redirects to confirm final destination
```bash
curl -s -L -o /dev/null -w "%{http_code} %{url_effective}" --max-time 30 http://localhost:3000/admin
# Output: 200 http://localhost:3000/signin
```

A 307 that resolves to `/signin` is correct behavior.

### Without following redirects
```bash
curl -s -o /dev/null -w "%{http_code}" --max-time 30 http://localhost:3000/admin
# Output: 307
```

This is also normal. A 307 on an auth-gated route = working auth redirect.

## What WOULD be a real error

- 307 that resolves to `/signin` but the route should be public (misconfigured middleware)
- 500 (actual server error) on any route
- 000/connection refused (server not running)
- 404 on a route that should exist (missing page file)

## Summary table

| Status | Meaning | Action |
|--------|---------|--------|
| 200 | Route rendered | ✅ |
| 307 → /signin | Auth gate working | ✅ |
| 307 → something else | Misconfigured redirect | ⚠️ Investigate |
| 500 | Server error | ❌ Fix |
| 000 | Server down | ❌ Start server |
| 404 | Missing route | ❌ Check page file exists |
