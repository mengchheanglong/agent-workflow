# Supabase / Next.js authenticated smoke pitfalls

Concise notes from authenticated owner-dashboard smoke tests. Use this as a checklist before creating users or reporting upload/auth blockers.

## Avoid hosted-auth bounce damage

- Do not generate fake external email addresses against hosted Supabase Auth.
- Real-looking but nonexistent addresses can still receive attempted confirmation emails and bounce, putting Supabase project email-sending privileges at risk.
- Prefer, in order:
  1. an already-confirmed owner/test account;
  2. a real controlled inbox or plus-address;
  3. local Supabase mail capture for dev signup/password-reset testing;
  4. temporary dev-only email-confirmation bypass;
  5. custom SMTP/test mail tooling.
- If signup requires confirmation and there is no inbox/service-role/test bypass, stop and report the blocker rather than creating more users.

## Honest partial-pass reporting

When the authenticated loop mostly passes but one subsystem is blocked, separate the result:

- Passed: login redirect, protected dashboard load, settings save, CRUD, publish, public page verification.
- Blocked: the exact subsystem, exact UI/API message, and exact migration/config/input needed.

Do not say the whole smoke passed if uploads, email confirmation, or publish verification were not actually exercised.

## Storage migrations vs app bugs

If Supabase Storage upload returns a bucket/policy missing style error:

1. Inspect committed migrations for `storage.buckets` / `storage.objects` policies.
2. Check whether the app message names an unapplied migration or missing bucket.
3. Report the exact migration file or SQL to apply.
4. Only debug app upload code after the remote bucket/policies are present.

## Next.js server-action forms

- A normal browser automation click can fail to trigger a Next.js server-action form even when the page is otherwise usable. If trusted/local and there is no POST, redirect, or visible state change, use `form.requestSubmit(button)` as an automation fallback and verify the result.
- Do not add manual `method` or `encType` to forms whose `action` is a server function. React/Next supplies these automatically. Console warning to fix:

```text
Cannot specify a encType or method for a form that specifies a function as the action.
```

Patch by removing the manual attribute, then rerun typecheck/tests/build and browser console smoke.
