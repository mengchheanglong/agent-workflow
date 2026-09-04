# Playwright as Browser-Testing Fallback

## When to Use

When `computer_use` is blocked (full-screen app running, game, video) or
when the user explicitly asks not to use it, Playwright can drive a
headless Chromium to test the same web UI — forms, auth flows, page
rendering — without touching the user's desktop.

## Setup

```bash
npm install -D playwright @playwright/test
npx playwright install chromium
```

## Configuration

Create `playwright.config.ts`:

```ts
import { defineConfig } from '@playwright/test';

export default defineConfig({
  testDir: './tests',
  testMatch: 'browser.spec.ts',
  timeout: 30000,
  retries: 1,
  workers: 1,
  use: {
    baseURL: 'http://localhost:3000',
    headless: true,
    viewport: { width: 1280, height: 720 },
    ignoreHTTPSErrors: true,
  },
  webServer: {
    command: 'npm run build && npm run start',
    url: 'http://localhost:3000',
    reuseExistingServer: true,
    timeout: 120000,
  },
});
```

## Test Pattern

```ts
import { test, expect } from '@playwright/test';
import { connect, loadEnv, testUrl, truncateAll } from './db';

loadEnv();
process.env.DATABASE_URL = testUrl();
const { pool, db } = connect();

test.beforeEach(async () => { await truncateAll(pool); });
test.afterAll(async () => { await pool.end(); });

test('form submission works', async ({ page }) => {
  await page.goto('http://localhost:3000/signup');
  await page.fill('input[name="handle"]', 'testuser');
  await page.fill('input[name="email"]', 'test@example.com');
  await page.fill('input[name="password"]', 'validpassword123');
  await page.click('button[type="submit"]');
  await page.waitForLoadState('networkidle');
  await expect(page).toHaveURL('http://localhost:3000/');
});
```

## Key Differences from browser_* / computer_use

| Aspect | browser_* / computer_use | Playwright |
|--------|--------------------------|------------|
| Requires user's GUI browser | Yes | No |
| Can disrupt user's active window | Possible | No |
| Runs headless | No | Yes |
| Parallel-safe | No | Yes (with workers) |
| Visual verification | Yes | Via screenshots |
| DB seeding before tests | Manual | Easy (truncateAll) |

## When computer_use is Blocked

If you see `code: "background_unavailable"` repeatedly, the user is
running a full-screen application (game, video). Options:

1. Ask the user to Alt+Tab or close the full-screen app
2. Switch to Playwright (this guide)
3. Use `vision` mode to capture and analyze screenshots of the user's
   screen without interacting

## Gotchas

- **Next.js 15 searchParams**: Must be awaited in Server Components. Tests
  that hit pages with searchParams should verify they don't 500.
- **Better Auth email verification**: `requireEmailVerification` defaults
  to off unless `REQUIRE_EMAIL_VERIFICATION=true`. Tests may need to
  handle verification redirects.
- **Form client-side validation**: `required` and `minLength` attributes
  prevent submission in real browsers. Test both the client validation
  AND the server-side error messages separately.
- **Type errors in test files**: TypeScript strict mode may flag literal
  string comparisons. Use `as string` or template concatenation to widen
  types when comparing passwords/strings.
