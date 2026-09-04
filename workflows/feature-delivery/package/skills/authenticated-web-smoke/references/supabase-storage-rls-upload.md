# Supabase Storage RLS upload smoke pitfall

Use this when a Next.js/Supabase authenticated owner dashboard can read owner rows but Storage upload fails with row-level-security errors.

## Symptom

- Browser/server action returns an owner-friendly RLS message such as: `You can only upload images for your own menu items.`
- Bucket exists and public reads work, but authenticated upload is rejected.
- App upload path is owner-scoped, e.g. `<store_id>/<item_id>/<filename>.png`.

## Root-cause check

Inspect the applied Storage policies, not just the local migration file:

```bash
npx supabase migration list --linked
npx supabase db query --linked "select policyname, cmd, qual, with_check from pg_policies where schemaname='storage' and tablename='objects' order by policyname;"
```

In Storage policies, unqualified `name` inside a subquery can resolve to a column on the joined/subqueried table (for example `public.stores.name`) instead of the Storage object path. That makes checks compare a store UUID to a display name and rejects valid uploads.

Bad pattern:

```sql
where stores.id::text = (storage.foldername(name))[1]
```

Correct pattern:

```sql
where stores.id::text = (storage.foldername(storage.objects.name))[1]
```

## Repair pattern

1. Write a regression test or SQL-text assertion that local migrations contain `storage.foldername(storage.objects.name)` and do not contain `storage.foldername(name)`.
2. Patch the original migration for fresh installs.
3. Add a new repair migration for already-applied remote projects that drops/recreates the affected Storage policies.
4. Push from the actual project repo, not a parent directory:

```bash
npx supabase link --project-ref <project-ref>
npx supabase db push
npx supabase migration list --linked
```

5. Retry the authenticated browser upload.
6. Verify public output both ways:
   - page HTML contains the uploaded filename/URL on public menu/detail routes;
   - direct object URL returns `200` and the expected image content type.

## Evidence to collect

- Remote migration list showing the repair migration applied.
- `pg_policies` output showing `storage.foldername(objects.name)` / explicitly-qualified object name.
- Dashboard success message after upload.
- Public menu and item detail showing the uploaded image instead of an emoji/placeholder.
- Direct public object URL `200 image/png` (or relevant MIME type).
