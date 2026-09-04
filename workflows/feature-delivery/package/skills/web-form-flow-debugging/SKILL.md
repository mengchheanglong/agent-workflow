---
name: web-form-flow-debugging
description: Debug and verify web form flows, especially auth forms, server actions, alternate submit buttons, and phone-first viewport issues.
version: 1.1.0
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [web, forms, auth, qa, debugging, nextjs]
    related_skills: [systematic-debugging, test-driven-development, dogfood]
---

# Web Form Flow Debugging

Use this skill when a user reports that a web form, create-account page, login/signup flow, submit button, server action, or form validation "doesn't work".

## Core rules

A reported successful browser click is not proof that the user flow worked. Verify the observable effect: URL change, status/error message, form submission, server log, network request, database write, or redirect.

A visible raw error is usually a boundary failure, not only a presentation bug. Trace UI → shared API client → application proxy/BFF → live/mock upstream → framework runtime. Fix every boundary that can leak or hang, then verify both the deterministic failure and healthy recovery path.

For user-facing API errors, prefer an explicit public error code/message allowlist. Never grow a blacklist of stack/path/credential strings: novel DNS names, source paths, URLs, and exception formats will bypass it. Unknown messages must become status-specific generic copy.

## Workflow

1. **Reproduce the exact visible flow**
   - Start from the user-facing route, not from internal assumptions.
   - Click the same visible link/button the user would click.
   - Test both empty/invalid input and valid-looking input.

2. **Check whether the click reached the intended element**
   - If `browser_click` reports success but nothing changes, inspect more deeply.
   - On trusted local pages, use temporary probes to verify click/submit events.
   - Check `getBoundingClientRect()` for the target element and compare it with `innerHeight`/viewport bounds.
   - Use hit-testing (`elementFromPoint`) to detect overlays, off-screen controls, or misleading accessibility refs.

3. **Verify form submit effects**
   - Check the current URL and visible status/error message after submit.
   - Check browser console for JS errors.
   - Check dev-server logs or network traces for POST/server-action calls where available.
   - For Next.js Server Actions, inspect rendered `form`/`button` wiring: `action`, `formAction`, hidden `$ACTION_ID_*` inputs, submitter button name, and method.

4. **Prefer explicit critical flows**
   - If account creation/signup is a core flow, make it an explicit page state or route, not only a secondary submit button inside the login form.
   - Good pattern: `/login?next=...` for sign-in and `/login?mode=signup&next=...` for account creation.
   - Keep validation errors and provider messages on the same mode/page that produced them.
   - Preserve safe return paths across both modes.

5. **Pin with a small pure test first**
   - Add a pure helper test for mode parsing/path building before changing the UI.
   - Watch it fail (RED), implement the helper/page change (GREEN), then run full checks.
   - Browser-smoke the real flow after automated checks.

## Common root causes

- Secondary submit button is below the fold or hard to reach on the target viewport.
- Multiple submit buttons/server actions are wired, but the actual click path hits nothing or the wrong submitter.
- Browser-native validation blocks the submit, but the UI gives no obvious mode change.
- Signup errors/messages redirect back to login mode, making account creation look broken.
- Auth provider requires email confirmation; this is a real external state blocker, not a UI success.

## Reference notes

- See `references/nextjs-supabase-signup-mode.md` for the concrete Next.js/Supabase create-account-mode bug pattern, investigation steps, durable fix, and regression checklist.
- See `references/graceful-api-error-boundaries.md` when forms or pages expose HTML, framework errors, stacks, network details, or unsafe upstream messages; it includes the layered fail-closed policy, deterministic reproduction method, and regression matrix.
- See `references/nextjs-15-searchparams-mode-switch.md` for the pattern where a single route handles both "create new" and "edit existing" modes via `searchParams`, with server-side data loading for edit mode and server-controlled trusted base values.
- See `references/playwright-fallback.md` for the Playwright-based browser testing fallback when `computer_use` is blocked (full-screen games, SSH, focus-steal refusals).

## Verification checklist

- Login/protected route redirect still preserves `next`.
- Create-account link opens a distinct create-account mode/page.
- The create-account page has one primary create-account submit button.
- Valid signup submit reaches the auth provider/server action.
- Error/confirmation message remains in signup mode.
- Console is clean.
- Full project gate passes before commit/push.
