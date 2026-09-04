# Authenticated smoke-test checklist

## Preflight

- Confirm target login route and protected route, including `next`/return path.
- Look for documented test-owner credentials, seeded auth users, local auth bypass, or server-only test setup.
- Inspect env key names only; never print secret values.
- Public Supabase keys alone cannot confirm users or bypass email confirmation.

## Disposable signup cautions

- Reserved domains like `example.com` may be rejected by hosted auth providers as invalid.
- A realistic email shape can pass validation but still be blocked by email confirmation.
- If confirmation is required and no confirmation/service-role/test credential path exists, report the blocker rather than continuing with unauthenticated dashboard assumptions.

## Evidence to collect

- Browser URL before and after login/signup.
- Visible error/status message, e.g. invalid email or confirmation-required text.
- Server/dev log evidence of POST/action execution when available.
- Browser console result after auth actions.
- For successful auth: protected page loaded, CRUD/upload/save/publish result, and public page verification.

## Next.js server-action form fallback

If normal browser click does not submit a trusted local Next.js server-action form:

1. Verify there is no POST/route change/server log.
2. Trigger native submission from page context with `form.requestSubmit(button)`.
3. Verify the POST, redirect, and UI state afterward.

Do not use this to skip validation or fabricate auth; it is only a way to exercise the same form submission path when browser automation fails to click-submit reliably.
