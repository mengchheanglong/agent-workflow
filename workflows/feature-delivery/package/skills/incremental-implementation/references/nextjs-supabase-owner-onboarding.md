# Next.js + Supabase owner onboarding slice

Use this after a protected owner dashboard exists and authenticated users can reach the dashboard but may not yet own a store/workspace.

## Slice boundary

Good scope:

- show a create-first-store/workspace form only for authenticated users with no owned row;
- upsert the owner profile row for `auth.uid()`;
- insert one draft owner-scoped store/workspace row with `owner_id = auth.uid()`;
- revalidate protected dashboard routes and redirect back to the dashboard;
- keep the public customer route account-free;
- test payload normalization and write sequencing through injected seams so live Supabase credentials are not required.

Out of scope unless explicitly requested:

- category/item/product CRUD;
- image upload/storage;
- publish controls;
- team/RBAC, ownership transfer, or claim flows;
- service-role/admin keys in app code.

## Recommended TDD sequence

1. Write a pure helper test that turns owner + form input into the exact profile/store payload.
   - Assert slug normalization, trimmed strings, draft status, and `owner_id`.
   - Include contact normalization such as Telegram handles if relevant.
2. Implement only the pure helper.
3. Write a service test with an injected writer:
   - `hasStoreForOwner(ownerId)` runs first;
   - `upsertProfile(profile)` runs second;
   - `insertStore(store)` runs third;
   - result returns the created slug or a user-safe error.
4. Implement the injected service.
5. Add a Supabase writer adapter using the normal server client and existing RLS, not service-role credentials.
6. Add a server action that requires the owner user, calls the writer adapter, handles duplicate slugs with a safe message, revalidates dashboard paths, and redirects.
7. Replace the no-store placeholder with a phone-first onboarding form.
8. Run canonical gates and browser-smoke unauthenticated dashboard redirect plus one public route.

## Server action pitfall

In Next.js server actions, `redirect()` throws internally. If you wrap the whole action in `try/catch`, compute `nextPath` inside the `try/catch`, catch only real write errors there, then call `redirect(nextPath)` after the `try/catch`. This avoids accidentally converting a successful redirect into a generic error branch.

## RLS and security notes

- The insert should rely on authenticated RLS checks such as `with check (owner_id = auth.uid())`.
- Do not use service-role/admin keys for normal owner onboarding.
- Check for an existing owner store before insert to keep the first-store flow idempotent from the UI perspective.
- Keep public menu reads separate from owner-scoped dashboard reads.

## Verification checklist

- Focused tests for payload normalization and writer call order pass.
- Full `pnpm check` (or project equivalent lint/typecheck/test/build) passes.
- Browser smoke: `/dashboard?...` redirects unauthenticated users to `/login?next=...` while preserving query strings.
- Browser smoke: a known public route still renders.
- Docs/state updated so the next slice is text CRUD, not onboarding.
