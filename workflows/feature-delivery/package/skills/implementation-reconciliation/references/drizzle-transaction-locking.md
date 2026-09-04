# Drizzle Transaction Locking Patterns

## SELECT ... FOR UPDATE

In Drizzle ORM, use `.for("update")` on a select query to acquire a row-level lock:

```typescript
const [row] = await tx
  .select()
  .from(schema.table)
  .where(eq(schema.table.id, id))
  .for("update");
```

The lock is held until the transaction commits or rolls back.

## Transaction Wrapper

Use `db().transaction(async (tx) => { ... })` for atomic operations:

```typescript
await db().transaction(async (tx) => {
  // All queries use tx, not db()
  const [row] = await tx.select().from(...).for("update");
  await tx.update(...).set(...);
  await tx.insert(...).values(...);
});
```

## Critical: Lock Before Compare

For stale-check/write patterns, the lock must be acquired BEFORE reading the current state:

```typescript
await db().transaction(async (tx) => {
  // 1. Lock the row
  const [current] = await tx.select().from(schema.table)
    .where(eq(schema.table.id, id))
    .for("update");

  // 2. Compare (stale check)
  if (current.field !== expectedBase) {
    throw new StaleConflictError(...);
  }

  // 3. Mutate (safe — lock prevents concurrent changes)
  await tx.update(schema.table).set({ field: newValue });
});
```

## Multiple Row Locks

When stale checks involve multiple rows, lock them all at the start:

```typescript
await db().transaction(async (tx) => {
  const [work] = await tx.select().from(schema.canonWorks)
    .where(eq(schema.canonWorks.id, workId))
    .for("update");

  const mechanisms = await tx.select().from(schema.canonMechanisms)
    .where(eq(schema.canonMechanisms.canonWorkId, workId))
    .for("update");

  // Now safe to compare and mutate
});
```

## Unique Partial Index for 1:1 Relationships

When a FK should be unique only when non-null (e.g., one originating edit → one revision):

```typescript
uniqueIndex("canon_revision_edit_id_unique")
  .on(table.editId)
  .where(sql`${table.editId} is not null`)
```

This enforces uniqueness for non-null values while allowing multiple NULLs (for revert/manual revisions).

## Test Database Setup

DB-backed tests in this repository use a derived `_test` database. The test setup:

```typescript
import { connect, loadEnv, testUrl, truncateAll } from "./db";

loadEnv();
process.env.DATABASE_URL = testUrl();
const { pool, db } = connect();

beforeEach(async () => {
  await truncateAll(pool); // truncates all tables
});

afterAll(async () => {
  await pool.end();
});
```

**IMPORTANT**: Never run multiple DB-backed Vitest processes concurrently — they share the same `_test` database and will interfere with each other.
