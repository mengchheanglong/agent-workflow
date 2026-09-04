# Next.js 15 searchParams Pattern: New/Edit Mode Switching

How to handle a single route that serves both "create new" and "edit existing"
modes via `searchParams`, with server-side data loading for the edit case.

## When to use

- One route (`/items/new` or `/items/propose`) handles both creation and editing
- The edit target is identified by a query parameter (`?id=` or `?orgId=`)
- Edit mode needs authoritative server data to pre-populate the form
- The client must NOT be able to forge trusted fields (base values, ownership)

## Pattern

### 1. Server Component accepts `searchParams`

```tsx
export default async function Page({
  searchParams,
}: {
  searchParams: Promise<{ orgId?: string }>;
}) {
  const params = await searchParams;
  const orgId = params.orgId;
  // ...
}
```

`searchParams` is a `Promise` in Next.js 15 — `await` it before use.

### 2. Load authoritative data server-side (edit mode only)

```tsx
if (orgId) {
  // Validate UUID format before querying
  const UUID = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i;
  if (!UUID.test(orgId)) notFound();

  const [org] = await db()
    .select({ id, name, slug, ... })
    .from(schema.organizations)
    .where(eq(schema.organizations.id, orgId))
    .limit(1);

  if (!org) notFound();
  // Pass to client component for pre-population
}
```

### 3. Client component receives initial data as props

```tsx
export function Form({ existingOrg }: { existingOrg: ExistingOrg | null }) {
  const isEditMode = existingOrg !== null;
  const [name, setName] = useState(existingOrg?.name ?? "");
  // ... initialize all fields from existingOrg or empty
}
```

### 4. Submit path branches on mode

```tsx
if (isEditMode && existingOrg) {
  await submitAction({
    kind: "update",
    organizationId: existingOrg.id,
    payload: { changes: { name: { proposed: name }, ... } },
    rationale, sourceUrl,
  });
} else {
  await submitAction({
    kind: "new",
    payload: { name, slug, type, ... },
    rationale, sourceUrl,
  });
}
```

### 5. Server constructs trusted base values

For update proposals, the server reads the current authoritative row and
populates `base` from it. The client only sends `proposed` values.

```typescript
// Server-side
const changes = buildChangesFromSubmission(currentOrg, submittedChanges);
// buildChangesFromSubmission: for each field, if proposed !== current,
//   store { base: currentValue, proposed: submittedValue }
// If all fields are no-ops, return null → reject with OrganizationInputError
```

## Key rules

- **Never trust client-supplied base values** — always read from DB server-side
- **Validate UUID format** before querying (avoid injection, give clean 404)
- **Use `notFound()`** for invalid/missing targets (not a redirect or error page)
- **Slug is NOT editable** for existing records — omit the field entirely in edit mode
- **No-op filtering is server-side** — the UI doesn't need to detect unchanged fields
- **All authorization checks remain server-side** — the page gate is separate from data loading

## Common pitfalls

- Forgetting to `await searchParams` (it's a Promise in Next.js 15)
- Passing too much data to the client (only send fields the form needs)
- Letting the client construct `{ base, proposed }` pairs (server owns base)
- Running multiple DB-backed Vitest processes concurrently (shared `_test` database)
- TypeScript errors from `unknown` JSONB payloads — cast explicitly at the point of use

## Real-world example

See Organization Contributions V1 (`docs/specs/organization-contributions-v1.md`):
- `src/app/organizations/propose/page.tsx` — Server Component with searchParams
- `src/app/organizations/propose/_components/ProposeOrganizationForm.tsx` — Client form with mode branching
- `src/lib/organizations.ts` — `submitOrganizationProposal` with server-side base construction
- `tests/organization-contributions-edit-flow.test.ts` — Tests for the edit flow
