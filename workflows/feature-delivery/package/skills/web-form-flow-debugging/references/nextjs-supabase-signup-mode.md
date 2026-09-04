# Next.js/Supabase signup mode bug pattern

## Symptom

A login page has a secondary "Create owner account" submit button inside the same form as sign-in. Users report that create account does not work. Browser automation may report the click as successful, but the page does not change and no POST/server action appears in logs.

## Investigation pattern

1. Reproduce from the user-facing route, e.g. `/login?next=%2Fdashboard%2Fsettings`.
2. Click create account with empty fields and with valid-looking fields.
3. Verify actual effects, not click success:
   - URL/status message changed?
   - browser console clean?
   - dev-server log shows POST/server action?
4. Inspect rendered form wiring on trusted local pages:
   - `form.method`, `form.action`
   - hidden `$ACTION_ID_*` inputs
   - submit button `name`/`formAction`
5. Inspect viewport/hit testing if clicks report success but events do not fire:
   - `getBoundingClientRect()` vs `innerHeight`
   - `elementFromPoint()` at button center

## Durable fix

Make account creation an explicit route/page mode instead of a fragile secondary submit:

```text
/login?next=/dashboard/...              # sign in
/login?mode=signup&next=/dashboard/...  # create account
```

The page can keep one route, but it should render a distinct signup state with:

- Create Account heading;
- email/password inputs;
- one primary "Create owner account" submit;
- alternate "Sign in" link;
- mode-preserving redirects for validation errors and email-confirmation messages.

## Regression coverage

Add a pure helper test before touching the page:

- `getOwnerAuthMode(undefined) -> "login"`
- `getOwnerAuthMode("signup") -> "signup"`
- invalid modes fall back to `"login"`
- `buildOwnerAuthPath("signup", "/dashboard/settings") -> "/login?mode=signup&next=%2Fdashboard%2Fsettings"`

Then run:

```bash
pnpm vitest run lib/auth/owner-auth.test.ts
pnpm typecheck
pnpm check
```

Browser smoke:

1. protected route redirects to `/login?next=...`;
2. login page shows a visible Create account link;
3. link opens `/login?mode=signup&next=...`;
4. valid signup reaches Supabase/Auth provider;
5. provider confirmation/error stays on signup mode;
6. console stays clean.
