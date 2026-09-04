---
name: authenticated-web-smoke
description: "Authenticated browser smoke tests for owner/admin web apps: credential preflight, login redirects, gated CRUD, and honest blocker reporting."
version: 1.0.0
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [qa, browser, auth, smoke-test, supabase, nextjs]
    related_skills: [dogfood, systematic-debugging]
---

# Authenticated Web Smoke Tests

## When to use

Use this skill when testing login-gated web flows such as owner dashboards, admin panels, authenticated CRUD, uploads, publish controls, or protected-route redirects.

This complements general dogfood testing by adding auth-specific preflight and blocker handling.

## Core principle

Do not pretend an authenticated smoke test passed unless the browser actually has an authenticated session and the protected flow was exercised end-to-end. If auth setup blocks the test, report the blocker and the exact credential/config needed.

## Workflow

1. **Auth preflight**
   - Identify the login route and intended return path, e.g. `/login?next=/dashboard/settings`.
   - Check whether the project documents test-owner credentials, a local auth bypass, seeded auth users, or a server-only service-role setup.
   - Check available environment key names without printing secret values.
   - If only public auth keys are available, assume you cannot programmatically confirm users.

2. **Start and verify the app**
   - Start the dev server as a tracked background process if it is not already running.
   - Probe the target route before browser work.
   - Keep server logs available as evidence for POSTs, redirects, and action execution.

3. **Exercise auth honestly**
   - Test protected-route redirect and `next` preservation.
   - Sign in with provided confirmed credentials when available.
   - Do not create new hosted-auth users unless signup itself is the scope and the address is a real controlled inbox. Never generate fake external inboxes for hosted Supabase Auth; confirmation emails can bounce and put project email-sending privileges at risk.
   - If signup requires email confirmation and no confirmation channel/service-role key is available, stop the authenticated portion and report the blocker.

4. **Run the protected flow**
   - Once authenticated, exercise the smallest complete owner/admin loop requested: create/load resource, edit settings, CRUD records, upload file if in scope, publish/save, then verify public output if relevant.
   - Check browser console after navigation and significant interactions.
   - Capture visual evidence for layouts or failures.

5. **Clean up**
   - Stop any dev server/process you started unless the user asked to keep it running.
   - Verify the final tracked-process list after cleanup. Readiness/watch notifications can arrive after termination; treat them as historical output, not proof that a process is still running.
   - Do not commit credentials or `.env` changes.
   - Summarize what passed, what was blocked, and the exact next input needed.

## Next.js server-action form pitfalls

- Browser automation may sometimes click a submit button without causing a POST on Next.js server-action forms. If the page is trusted/local and a normal click produces no server log, no redirect, and no UI change, use native form submission from page context as a fallback, e.g. `form.requestSubmit(button)`. Then verify through server logs and visible UI state.
- React/Next server-action forms should not manually specify `method` or `encType`; React supplies those automatically. If console shows `Cannot specify a encType or method for a form that specifies a function as the action`, patch the form to remove the invalid attribute and rerun checks plus browser console smoke.
- Server-action forms serialize the action into hidden `$ACTION_REF_*`/`$ACTION_*` inputs, so real email/password fields may carry plain ids (e.g. `#owner-email`, `#password`) — locate by id, not by `input[type=email]` assumptions, and click the submit button by visible text (`button:has-text("Sign in")`) wrapped in `Promise.all` with `waitForLoadState("networkidle")`. A bare `page.click` without the wait can race the redirect and land the assertion on the pre-submit URL.
- For authenticated screenshot passes, prefer signing in through the real login form over injecting session cookies. `@supabase/ssr` stores the session as chunked cookies (`sb-<project-ref>-auth-token{,.0,.1}` with a `base64-` prefixed JSON payload); hand-building that shape via CDP `Network.setCookie` repeatedly bounced back to `/login?next=...`. Form login creates the session exactly as production does and just works.
- Next.js dev servers render a red "N Issue" dev-tools badge (`data-next-badge-root`) that overlays the bottom nav in screenshots. Inspect the DOM for that attribute before treating it as an app bug — it never ships to production builds.
- `next-env.d.ts` flips its `.next/types` import between dev and build runs; revert it rather than committing the flip.

## Supabase-specific notes

- Public `NEXT_PUBLIC_SUPABASE_*` keys are not enough to confirm or manage auth users.
- A service-role key must stay server-side and should only be used if the user/project explicitly provides it for testing.
- Hosted Supabase can require email confirmation; in that case, the valid outcomes are: confirmed test credentials, access to the confirmation email/link, temporary test config change, or a server-side test user setup.
- Do **not** generate fake external email addresses against hosted Supabase Auth during smoke tests. Real-looking but nonexistent inboxes can bounce confirmation emails and put the project's email-sending privileges at risk. Prefer an already-confirmed owner account, a real controlled inbox/plus-address, local Supabase mail capture, temporary dev-only confirmation bypass, or custom SMTP test tooling.
- When a Supabase-backed feature says a bucket/storage object is missing, distinguish app-code failure from remote migration state. Inspect the committed Storage migration and report the exact SQL/migration that must be applied before claiming upload is broken.

## Playwright Fallback for computer_use

When `computer_use` is blocked (full-screen app, game, video) or the user
asks not to use it, Playwright provides headless Chromium browser testing
that doesn't disrupt the user's desktop.

See `references/playwright-fallback.md` for:
- Installation and config (`playwright.config.ts`)
- Test pattern with DB seeding (`truncateAll` before each test)
- Auth flow testing (sign up → verify → sign in)
- Next.js form validation gotchas (required/minLength, TypeScript strict mode)

## References

- `references/chrome-cdp-authenticated-smoke.md` — dependency-light authenticated Chrome CDP harness: tracked browser lifecycle, React form submission, route/viewport assertions, console/network capture, screenshots, and JSON evidence.
- `references/authenticated-smoke.md` — concise checklist and evidence notes from a Supabase/Next.js owner-dashboard smoke test.
- `references/supabase-auth-smoke-pitfalls.md` — Supabase/Next.js pitfalls learned from authenticated owner smoke tests: bounce-risk emails, missing Storage migrations, server-action form warnings, and honest partial-pass reporting.
- `references/supabase-storage-rls-upload.md` — Supabase Storage RLS upload debugging: inspect remote policies, avoid unqualified `name` in Storage object path checks, add repair migrations, and verify public object URLs.
- `references/menui-dashboard-ux-pass.md` — full worked example (Menui 2026-08): universal-simplicity dashboard redesign plus the verified authenticated screenshot recipe at 390px, including the real-form-login-over-cookie-injection lesson and dev-tools-badge false alarm.
- `references/playwright-fallback.md` — Playwright as browser-testing fallback when computer_use is blocked: setup, config, test patterns, Next.js gotchas.
