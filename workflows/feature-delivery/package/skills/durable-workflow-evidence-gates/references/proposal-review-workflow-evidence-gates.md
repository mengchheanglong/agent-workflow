# Proposal-Review Workflow Evidence Gates

Pattern from Organization Contributions V1 (OFD-D84) in OpenFullDive. A contributor submits a proposal (durable journal entry), an editor reviews and decides (accept/reject), and the canonical organization table is only mutated on acceptance. This is a durable workflow where the proposal journal is the source of truth for pending decisions, and the canonical table is the source of truth for published data.

## Architecture

```
Contributor → submitOrganizationProposal() → organization_proposal (journal)
                                                    ↓
Editor → listOrganizationProposals() → review queue
                                                    ↓
Editor → accept/reject → transaction:
  - Lock proposal row (FOR UPDATE)
  - Validate state = 'proposed'
  - On accept: mutate canonical org + mark proposal accepted
  - On reject: mark proposal rejected (org untouched)
  - Conditional update assertion (affected_rows = 1)
```

## Evidence Requirements

For each decision transaction, prove:

1. **Proposal state transition**: `status` changed from `proposed` → `accepted`/`rejected`
2. **Reviewer identity**: `reviewerId` = actual editor (resolved via `getActor()`, never from client)
3. **Timestamp**: `decidedAt` = now
4. **Canonical data integrity**:
   - New org acceptance: `proposedBy` = original proposer, 0 revisions created
   - Update acceptance: only proposed fields changed, exactly 1 revision with correct prev/next
   - Rejection: org completely untouched, 0 revisions
5. **Concurrency**: second decision attempt fails cleanly ("already been decided")

## Stale Conflict Detection

For update proposals, the proposal stores `base` values (authoritative state at submission time). At acceptance:

```typescript
for (const [key, change] of Object.entries(proposal.payload.changes)) {
  if (!areValuesEqual(currentOrg[key], change.base)) {
    staleFields.push(key);
  }
}
if (staleFields.length > 0) {
  throw new OrganizationStaleConflictError(staleFields, changes, currentOrg);
  // Transaction aborts: org unchanged, no revision, proposal remains 'proposed'
}
```

**Critical invariant**: Even if `current === proposed` (someone else independently made the same change), the proposal is STALE because `base !== current`. Accepting it would record false audit provenance.

## No-Op Filtering at Submission

The server reads current authoritative data at proposal creation time and filters out fields where `proposed === current`. If zero fields remain, the submission is rejected:

```typescript
const changes = buildChangesFromSubmission(currentOrg, submittedChanges);
if (!changes) {
  throw new OrganizationInputError("No changes proposed against current organization data.");
}
```

This ensures proposals are never created with `base === proposed` for any field.

## Test Patterns

### DB-Backed Test Harness

```typescript
// Set test URL BEFORE importing service modules
loadEnv();
process.env.DATABASE_URL = testUrl();
const { pool, db } = connect();
const { submitOrganizationProposal } = await import("@/lib/organizations");

beforeEach(async () => {
  await truncateAll(pool);  // Truncate all tables between tests
});
```

### Concurrency Test

```typescript
it("second concurrent decision fails cleanly", async () => {
  // First decision succeeds
  await acceptNewOrganizationProposal({ proposalId, actor: editor1 });
  
  // Second decision fails
  await expect(
    acceptNewOrganizationProposal({ proposalId, actor: editor2 }),
  ).rejects.toThrow(/already been decided/);
});
```

### Stale Conflict Test

```typescript
it("stale conflict aborts transaction", async () => {
  // Change proposed field before acceptance
  await db.update(organizations).set({ status: "Conflicting" }).where(eq(organizations.id, orgId));
  
  await expect(
    acceptUpdateOrganizationProposal({ proposalId, actor: editor, editorReason }),
  ).rejects.toBeInstanceOf(OrganizationStaleConflictError);
  
  // Org unchanged, no revision, proposal remains proposed
  const [org] = await db.select().from(organizations).where(eq(organizations.id, orgId));
  expect(org.status).toBe("Conflicting"); // not the proposed value
  
  const revisions = await db.select().from(organizationRevisions);
  expect(revisions).toHaveLength(0);
  
  const [proposal] = await db.select().from(organizationProposals);
  expect(proposal.status).toBe("proposed");
});
```

## TypeScript + Drizzle Patterns

### JSONB Payload Typing

Database JSONB columns are typed as `unknown` in Drizzle. Cast and narrow before JSX:

```typescript
// ✅ Correct
const payload = proposal.payload as { changes?: Record<string, { base: unknown; proposed: unknown }> } | undefined;
const updateChanges: Record<string, { base: unknown; proposed: unknown }> | null = payload?.changes ?? null;

// ❌ Fails: TS2322 in JSX conditionals
const changes = proposal.payload as { changes?: ... }?.changes;
return (
  {proposal.kind === "update" && changes && (
    <div>{Object.entries(changes).map(...)}</div>  // Error: changes is unknown
  )}
);
```

### Cross-Module Error Imports

Error classes defined in `src/modules/*` are not automatically re-exported from `src/lib/*`. Import from the canonical source:

```typescript
// ✅ Import from module
import { OrganizationInputError, OrganizationStaleConflictError } from "@/modules/organizations";

// ❌ Fails: not re-exported from lib
import { OrganizationInputError } from "@/lib/organizations";
```

### `assertCan` Placement

Service functions accept `Actor | null` and call `assertCan` as their first statement:

```typescript
export async function acceptNewOrganizationProposal({
  proposalId,
  actor,  // Actor | null
}: {...}): Promise<{...}> {
  assertCan(actor, "organization:review");  // throws AuthorizationError if null/unauthorized
  // ... transaction logic
}
```

This keeps services testable and worker-compatible.

## File Organization

```
src/modules/organizations/index.ts    — Pure domain: types, validators, errors, diff engine
src/lib/organizations.ts              — Service layer: DB wiring, transactions, error mapping
src/app/organization-actions.ts       — Server Actions: thin wrappers resolving actor + calling services
src/app/organizations/propose/        — Contributor UI
src/app/admin/organizations/          — Admin review UI
tests/organization-contributions-*.test.ts  — 4 test suites (domain, submission, review, e2e)
```
