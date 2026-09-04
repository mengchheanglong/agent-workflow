# Playwright as Fallback for Computer Use

## When `computer_use` fails

`computer_use` fails with `code: "background_unavailable"` when:
- A full-screen game or DirectInput application is running (e.g., World War Z)
- The user is actively working in another window and refuses focus steal
- The session is over SSH (Session 0 on Windows)
- The desktop is locked or on a different virtual desktop

**Do NOT retry `computer_use` in a loop.** Instead, switch to **Playwright** for headless browser testing.

## Setup

```bash
npm install -D @playwright/test
npx playwright install chromium
```

Create `playwright.config.ts`:

```typescript
import { defineConfig } from '@playwright/test';

export default defineConfig({
  testDir: './tests',
  testMatch: ['browser.spec.ts'],
  timeout: 30000,
  retries: 1,
  workers: 1,
  use: {
    baseURL: 'http://localhost:3000',
    headless: true,
  },
  webServer: {
    command: 'npm run build && npm run start',
    url: 'http://localhost:3000',
    reuseExistingServer: true,
    timeout: 120000,
  },
});
```

## Test pattern for Next.js apps with DB

```typescript
import { test, expect } from '@playwright/test';
import { connect, loadEnv, testUrl, truncateAll } from './db';

loadEnv();
process.env.DATABASE_URL = testUrl();
const { pool, db } = connect();

const BASE_URL = 'http://localhost:3000';
let counter = 0;
function unique(prefix: string): string {
  return `${prefix}_${Date.now()}_${counter++}`;
}

test.beforeEach(async () => {
  await truncateAll(pool);
});

test.afterAll(async () => {
  await pool.end();
});

test('Example: sign up flow', async ({ page }) => {
  await page.goto(`${BASE_URL}/signup`);
  await page.fill('input[name="handle"]', unique('user'));
  await page.fill('input[name="email"]`, `${unique('u')}@example.com`);
  await page.fill('input[name="password"]', 'validpassword123');
  await page.click('button[type="submit"]');
  await page.waitForLoadState('networkidle');
  await expect(page).toHaveURL(BASE_URL + '/');
});
```

## Common pitfalls and fixes

### 1. Strict mode violations
```
Error: strict mode violation: getByText('foo') resolved to 3 elements
```
**Fix:** Scope to a locator: `page.getByLabel('Conversation').getByText('foo')` or use `.first()`.

### 2. TypeScript literal comparison errors
```
Error: This comparison appears to be unintentional because the types '"validpassword123"' and '"differentpassword"' have no overlap.
```
**Fix:** Cast to `string` or restructure the test. Better: test that the validation function exists rather than testing literal comparison.

### 3. Form blocked by client-side validation
Browser-native validation (`required`, `minLength`, `type="email"`) prevents submission before the Server Action runs.

**Fix:** Test both paths:
- **Client validation:** Form stays on page (check URL unchanged after click)
- **Server validation:** Error message appears (fill valid-looking but invalid data)

### 4. Import path errors
Services may be in `src/lib/` (wiring) or `src/modules/` (domain). Check imports:
- `signUp` → `src/lib/identity.ts`
- `checkHandleShape`, `describeHandleProblem` → `src/modules/identity/index.ts`

### 5. Auth state between tests
Use `page.context().clearCookies()` to sign out between tests. Do NOT navigate to `/signout` (may not exist as a route).

### 6. Dynamic data insertion
When seeding test data:
- Check the schema for NOT NULL columns (e.g., `organization` has `type`, `direction`, `invasiveness`, `status` — not just `name` and `description`)
- Use valid enum values (e.g., `direction: 'Read'` not `'input'`)

## Advantages over computer_use

- Runs in its own browser instance — doesn't care about the user's desktop state
- Can seed/truncate the test database between tests
- Fast iteration (no screenshot capture overhead)
- CI/CD friendly
- Works over SSH / in containers

## Disadvantages

- Requires the app to be running (auto-started via `webServer` config)
- Can't test native OS dialogs, drag-and-drop between apps, or desktop integration
- Can't test the user's actual browser state (cookies, extensions, etc.)

## Integration with vitest

Keep Playwright tests in separate files (`browser.spec.ts`) with a separate config (`playwright.config.ts`). The existing `vitest.config.mts` should NOT include Playwright tests.

```bash
npm test -- --run                 # vitest suites
npx playwright test --config=playwright.config.ts  # browser suites
```

## Vision-based browser inspection

When Playwright is not available and you only have `computer_use` with `mode="vision"`, use the screenshot to:

1. Verify the page rendered (check for expected text elements)
2. Identify form fields by their labels
3. Check for error messages
4. Verify responsive layout

The `vision_analyze` tool can load a screenshot and describe what it sees. This is slower than Playwright but works when the user's desktop is occupied.
