# Next.js + Supabase owner menu CRUD and media slices

Use this reference for phone-first owner dashboards that manage a public menu/catalog with Supabase Auth, RLS, and Storage.

## Slice order that worked

1. Protected owner dashboard + create-first-store onboarding.
2. Category text CRUD.
3. Menu-item text CRUD.
4. Store publish/unpublish controls.
5. Menu-item image upload/storage.
6. Store profile/contact editing next.

Keep each as a separate TDD-backed vertical slice with its own commit/push after verification.

## Service seam pattern

Write pure domain helpers first with injected writers/readers so tests do not need live Supabase credentials:

- `createOwnerCategory` / `updateOwnerCategory` resolve owner store and write only `store_id` owned by `auth.uid()`.
- `createOwnerMenuItem` / `updateOwnerMenuItem` verify the selected category belongs to the owner-owned store before inserting/updating.
- `setOwnerStorePublication` checks publish readiness in the helper: publish requires at least one active category and one available item; unpublish only requires an owner-owned store.
- `setOwnerMenuItemImage` validates file type/size before any DB/storage calls, verifies item ownership, uploads, then persists `image_url`.

Targeted RED examples:

```bash
pnpm vitest run lib/dashboard/owner-menu-item-crud.test.ts
pnpm vitest run lib/dashboard/owner-store-publication.test.ts
pnpm vitest run lib/dashboard/owner-menu-item-image.test.ts lib/menu/supabase-menu-mapper.test.ts
```

## Supabase/RLS rules

- Resolve the signed-in owner's first store via `stores.owner_id = auth.uid()`.
- Insert children with the owner-owned `store_id`; update children using both child `id` and `store_id` filters.
- For menu items, check `category_id` belongs to the same owner store before write.
- Prefer normal RLS-backed clients for owner actions; do not jump to service-role/admin clients for MVP CRUD.
- Revalidate owner and public paths after writes: `/dashboard`, `/dashboard/menu`, `/dashboard/settings`, and affected `/m/[slug]`/`/s/[slug]` routes.

## Storage pattern for item images

Schema may already have `menu_items.image_url`; if so, add mapper/model/UI support rather than another column.

Recommended bucket/policy shape:

- bucket: `menu-item-images`
- public read for menu images
- allowed MIME types: `image/jpeg`, `image/png`, `image/webp`, `image/gif`
- file size limit: 5 MB
- path: `<store_id>/<item_id>/<slugified-file-name>.<extension>`
- owner policies check `(storage.foldername(name))[1]` against an owner-owned `stores.id`

In the app model, add `imageUrl` to `MenuItem`, include `image_url` in Supabase selects, map it to `imageUrl`, and make public card/detail image containers prefer `imageUrl` with emoji/tone fallback.

## UI pattern

- Dashboard menu page can host both category manager and menu-item manager.
- Use server-rendered forms and server actions for create/update/upload.
- Keep image upload as a separate post-create action per item; do not couple media upload to item text CRUD.
- Add status query params like `item_message` / `item_error` or `publish_message` / `publish_error` and render a single status banner.
- Do not require live authenticated smoke if no owner session is available; verify unauthenticated redirect plus public route rendering, and rely on TDD seams/typecheck/build for owner action correctness.

## Verification gate

Before each commit:

```bash
pnpm check
```

Then browser smoke touched routes, usually:

- `/dashboard/menu?...` redirects unauthenticated users to `/login?next=...`
- `/dashboard/settings?...` redirects unauthenticated users to `/login?next=...`
- `/m/<seed-slug>` renders public menu
- `/m/<seed-slug>/item/<seed-item-slug>` renders item detail
- browser console is clean

After verification, stage intended files only, run `git diff --cached --check`, commit, push, confirm clean status, then continue to the next slice.
