# Type Migration: Removing a Field from a Shared Type

When you remove or rename a field on a shared type (like `UserAccount`), you MUST find and update ALL references across the codebase.

## Pattern

1. **Update the type definition** in `shared/constants/mock-data.ts`
2. **Update all seed data** — every object of that type
3. **Update all consumers** — grep for the field name across `app/`, `components/`, `lib/`, `shared/`
4. **Update derived helpers** — functions like `getUserAccesses()` that may reference the old field
5. **Typecheck** — `pnpm exec tsc --noEmit` will catch any you missed

## Common consumer locations

- Page components (`app/(admin)/feature/page.tsx`)
- Shared components (`components/pages/feature/FeatureControls.tsx`)
- Command palette (`components/layout/CommandPalette.tsx`)
- Mock store (`lib/mock-store.ts`)
- Other features that reference the same data

## Example: Removing `kinds` from `UserAccount`

Before:
```ts
export type UserAccount = {
  // ...
  kinds: UserKind[]
  access?: UserAccess[]
}
```

After:
```ts
export type UserAccount = {
  // ...
  access?: UserAccess[]
}
```

Consumers updated:
- `app/(admin)/users/page.tsx` — `row.kinds.join(", ")` → `accessKinds(row).join(", ")`
- `app/(admin)/users/[userId]/page.tsx` — `user.kinds.join(" · ")` → `access.map(a => a.kind).join(" · ")`
- `components/layout/CommandPalette.tsx` — `user.kinds.join(", ")` → `user.access?.map(a => a.kind).join(", ")`
- `lib/mock-store.ts` — `getUserAccesses()` simplified

## Pitfall

The `kinds` field was also used in the seed data for `USERS`. Every seed object needed its `kinds: [...]` replaced with `access: [...]`.
