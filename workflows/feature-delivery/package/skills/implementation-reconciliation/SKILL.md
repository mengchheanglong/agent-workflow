---
name: implementation-reconciliation
description: "Reconcile code against an approved architecture spec."
version: 1.0.0
author: Session-derived
metadata:
  hermes:
    tags: [reconciliation, spec-compliance, implementation, review, architecture]
---

# Implementation Reconciliation

After an architecture spec passes independent review, a separate **reconciliation pass** brings existing runtime implementation into compliance with the approved spec. This is NOT a rebuild from scratch — it preserves correct work while eliminating deviations.

## When to Use

- Architecture spec has passed independent review (`APPROVE` verdict)
- Runtime code already exists in the working tree (possibly from earlier implementation attempts)
- Spec is authoritative — do NOT redesign the architecture

## The Reconciliation Workflow

```
SPEC PASSES REVIEW → RECONCILE EXISTING CODE → VALIDATE → HANDOFF
         ↓                    ↓                      ↓          ↓
   Authoritative         Compare vs spec        Typecheck    Independent
   reference             Fix deviations         Build        review
                         Remove workarounds     Tests
```

## Step 1: Read Current Truth

Read in order:
1. `AGENTS.md`, `.active/CURRENT.md`, `.active/NEXT.md`, `.active/STATE.json`, `.active/DECISIONS.md`
2. The approved spec (`docs/specs/<feature>-v1.md`)
3. ALL existing implementation files (domain, service, actions, UI, tests)
4. Current schema and migrations
5. `git status`, `git branch --show-current`, `git diff --stat`

Confirm you are on the correct feature branch and the spec is the authoritative reference.

## Step 2: Reconciliation Principle

For every existing implementation area:

| Condition | Action |
|---|---|
| Implementation matches spec | Keep it as-is |
| Implementation partially matches | Minimally correct it |
| Implementation violates spec | Replace the violating behavior |
| Required behavior is missing | Implement it |

**Avoid unrelated refactors.** Do not expand scope beyond the approved feature.

## Step 3: Schema & Migration

If the spec requires schema changes:
1. Update `src/db/schema.ts` to match the approved spec exactly
2. Generate migration: `npm run db:generate` (or equivalent)
3. Inspect generated SQL carefully
4. Apply to dev/test database: `npm run db:migrate`
5. **Do NOT apply to production. Do NOT deploy.**

Remove ALL temporary pre-migration workarounds:
- `sql`\`null\` placeholders
- `// TODO after migration` comments
- `editId: null` placeholders
- Timestamp/author/work heuristics for record lookup

## Step 4: Provenance & Audit

If the spec defines durable relationships (e.g., `canon_revision.edit_id → canon_edit.id`):
- The FK is the single authoritative link
- Never find records by: `createdAt` proximity, same contributor, latest revision, `workId + actor`, ordering heuristics
- Query exactly: `WHERE table.edit_id = :editId`

## Step 5: Snapshot & Revision Format

If the spec mandates a canonical snapshot format (e.g., `prev/next` for mechanisms):
- Submission payloads may use operations (`add`/`update`/`remove`)
- BUT persisted revisions MUST use the normalized snapshot format
- Normalize before persistence: sort by UUID, deterministic ordering
- DB row ordering must NOT affect equality comparisons

## Step 6: Explicit Mutation Dispatch

If the spec requires discriminated dispatch:
```typescript
// CORRECT — explicit kind field
interface RejectInput {
  kind: "new" | "existing";
  editId: string;
  reason: string;
}

// WRONG — try/catch routing
try {
  await rejectNewCanonProposal(...);
} catch {
  await rejectExistingCanonEdit(...);  // A real failure in new-work reject could trigger wrong mutation
}
```

Server must verify declared `kind` against authoritative row shape (e.g., `canonWorkId IS NULL` for new, `IS NOT NULL` for existing). Forged mismatch fails cleanly.

## Step 7: Service-Level Authorization

Every mutation service MUST call `assertCan()` at the start. Server Action authentication and UI guards are NOT substitutes — the service is the trusted boundary.

| Operation | Permission |
|---|---|
| Submit new proposal | `canon:edit` |
| Submit existing edit | `canon:edit` |
| Accept new proposal | `canon:review` |
| Reject new proposal | `canon:review` |
| Accept existing edit | `canon:review` |
| Reject/revert existing edit | `canon:review` |

## Step 8: Prohibited Pattern Audit

Before stopping, search the entire `src/` and `tests/` trees for prohibited leftovers:

- `TODO after migration`
- `editId: null` placeholder (only valid for revert/manual revisions)
- `createdAt proximity` / `latest revision` / `workId + actor` lookups
- `try/catch` reject dispatch
- `orgId` in non-Organization features
- Optional direct-edit references (when spec requires ≥1)
- `added/updated/removed` persisted mechanism revision format (should be `prev/next`)
- `mock fallback` in public DB readers
- Missing `assertCan()` in mutation services

Remove or correct every match. Do not remove unrelated TODOs.

## Step 9: Validation

Run in order:
1. `npm run typecheck` — must be clean
2. `npm run build` — must pass
3. Focused domain tests first
4. All feature suites sequentially (NOT concurrently for DB-backed suites)
5. Affected regression suites (e.g., `admin-console-foundation` if module availability changed)

## Step 10: Commit Boundary

**Do NOT commit, push, merge, or deploy.** Leave implementation ready for independent review.

---

## Pitfall: Heuristic Record Lookup

The most common reconciliation failure is leaving timestamp/author heuristics in place of exact FK relationships. The pattern to eliminate:

```typescript
// WRONG — unsafe heuristic
const [revision] = await tx
  .select()
  .from(schema.canonRevisions)
  .where(
    and(
      eq(schema.canonRevisions.canonWorkId, workId),
      eq(schema.canonRevisions.editorId, proposerId),
    ),
  )
  .orderBy(desc(schema.canonRevisions.createdAt))
  .limit(1);
// If same contributor edits same work twice, this finds the WRONG revision

// CORRECT — exact FK linkage
const [revision] = await tx
  .select()
  .from(schema.canonRevisions)
  .where(eq(schema.canonRevisions.editId, proposalId));
```

## Pitfall: Mechanism Snapshot Non-Determinism

When revisions store mechanism snapshots, DB row ordering can vary. Always normalize:

```typescript
function normalizeSnapshot(mechanisms) {
  return [...mechanisms].sort((a, b) => a.id.localeCompare(b.id));
}
```

Use normalized snapshots for both persistence AND comparison (revert conflict checks).

## Pitfall: Conditional Optional-Field Persistence

When a field is REQUIRED by spec but the runtime treats it as optional, the violation often hides in three places simultaneously:

1. **Type**: `references?: CanonReference[]` (optional) vs `references: CanonReference[]` (required)
2. **Parser**: `if (raw.references !== undefined) { ... }` conditional parsing
3. **Service**: `if (referencesChanged) { revision.references = ... }` conditional persistence

All three must be fixed together. A type-only fix leaves the parser returning `undefined`. A parser-only fix leaves the service conditionally omitting the revision snapshot.

```typescript
// WRONG — optional field allows missing data
type UpdatePayload = {
  references?: CanonReference[];
};

// WRONG — conditional persistence omits revision snapshot
if (referencesChanged && payload.references) {
  revisionChangedFields.references = { prev, next };
}

// CORRECT — required field, unconditional persistence
type UpdatePayload = {
  references: CanonReference[];
};
// ...
revisionChangedFields.references = { prev: current, next: payload.references };
// (always present, even when prev === next)
```

The spec pattern: "complete normalized replacement set for EVERY edit" means:
- The field is required in the type
- The parser rejects missing/empty
- The service always persists (even when unchanged)
- The revision always contains the snapshot

## Pitfall: Transaction Lock Safety for TOCTOU Stale Protection

> See `references/drizzle-transaction-locking.md` for concrete Drizzle patterns.

When implementing stale-check/write critical sections, the stale comparison and mutation MUST occur within the same transaction with proper row locking. A common bug is reading the current state OUTSIDE the transaction, comparing, then writing inside a transaction — this creates a TOCTOU (Time-Of-Check-Time-Of-Use) race condition.

```typescript
// WRONG — TOCTOU race condition
const [currentWork] = await db()
  .select()
  .from(schema.canonWorks)
  .where(eq(schema.canonWorks.id, workId));
// ... another transaction can change the row here ...
const staleFields = detectStaleFields(currentWork, payload.base);
await db().transaction(async (tx) => {
  await tx.update(schema.canonWorks).set(...); // writes stale data
});

// CORRECT — lock row before comparing and mutating
await db().transaction(async (tx) => {
  const [currentWork] = await tx
    .select()
    .from(schema.canonWorks)
    .where(eq(schema.canonWorks.id, workId))
    .for("update"); // row lock held until commit
  const staleFields = detectStaleFields(currentWork, payload.base);
  if (staleFields.length > 0) {
    throw new CanonStaleConflictError(staleFields, ...);
  }
  // mutations here are safe — no other tx can change the row
  await tx.update(schema.canonWorks).set(...);
});
```

The lock must cover the ENTIRE stale-check/write critical section — from reading current state through applying mutations.

For every mutation that depends on current state, identify ALL rows that must be locked:
- The target row itself (`canon_work`, `canon_edit`, `canon_revision`)
- Child rows involved in stale checks (`canon_mechanism`)

Apply `SELECT ... FOR UPDATE` on all affected rows at the START of the transaction, before any comparisons.

## Pitfall: Incomplete No-Op Detection

A total no-op is NOT just "no field changes." It must also check mechanisms AND references:

```typescript
const isNoOp =
  Object.keys(changedFields).length === 0 &&
  !hasMechanismChanges &&
  JSON.stringify(proposedRefs) === JSON.stringify(currentRefs);
```

But `references [A] → [A]` alongside a title change is valid — only reject when ALL three dimensions are unchanged.
