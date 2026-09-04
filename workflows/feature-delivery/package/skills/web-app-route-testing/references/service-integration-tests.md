# Service-Layer Integration Tests (Fallback for Browser Testing)

## When to use

When browser/computer use testing is unavailable (game running, focus blocked, headless environment), test services directly against the `_test` database using Vitest. This validates the same invariants the browser would exercise — without the browser.

## Pattern

```typescript
import { afterAll, beforeEach, describe, expect, it } from "vitest";
import { eq } from "drizzle-orm";
import { connect, loadEnv, testUrl, truncateAll } from "./db";
import * as s from "../src/db/schema";

loadEnv();
process.env.DATABASE_URL = testUrl();
const { pool, db } = connect();

// Import the service functions that Server Actions call
const { signUp } = await import("../src/lib/identity");

describe("feature workflow", () => {
  beforeEach(async () => {
    await truncateAll(pool);  // Clean slate per test
  });

  afterAll(async () => {
    await pool.end();
  });

  it("creates entity via service", async () => {
    const result = await someService({ actor, input });
    expect(result.id).toBeTruthy();
    
    // Verify DB state directly
    const [row] = await db.select().from(s.table).where(eq(s.table.id, result.id));
    expect(row).toBeTruthy();
  });
});
```

## Key techniques from this session

### 1. Dynamic imports for ESM modules
Use `await import(...)` inside tests for modules that use ESM exports. Vitest's top-level imports work for most, but dynamic imports handle edge cases.

### 2. Truncate between tests
```typescript
beforeEach(async () => {
  await truncateAll(pool);
});
```
Every test gets a clean database. Prevents cross-test contamination.

### 3. Random handles for signUp
Better Auth caches handle availability. Use random suffixes to avoid collisions:
```typescript
const rnd = Math.random().toString(36).slice(2, 8);
await signUp({ handle: `user_${rnd}`, email: `user_${rnd}@example.com`, password: "validpassword123" });
```

### 4. Test pure domain logic separately
Domain tests (no DB) can run in parallel and are faster. DB tests should be sequential (`fileParallelism: false` in vitest.config.mts) because they truncate shared tables.

## Coverage achieved this session

- **138 tests total** across 8 test files
- All permission boundaries (role × action)
- All validation boundaries (length, format, uniqueness)
- Transaction integrity (stale detection, concurrent edits)
- Reference requirement enforcement
- All-no-op detection

## When this is NOT enough

Service tests don't verify:
- Visual rendering (HTML structure, CSS)
- Client-side form validation
- Cookie/session flow through Next.js runtime
- Email delivery

For those, use computer use or a headless browser — but only when the desktop is free.
