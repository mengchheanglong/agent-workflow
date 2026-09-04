# Graceful API and Runtime Error Boundaries

Use this reference when a web form or page displays raw HTML, a framework error page, a stack trace, a network exception, or internal upstream details.

## Boundary model

Trace the failure through every layer instead of suppressing the visible symptom:

1. **User interface** — form/page catches the failure, stops loading/submitting, shows safe recovery copy, and provides retry/navigation.
2. **Shared API client** — converts only explicitly public API messages into user text. Arbitrary `Error`, `TypeError`, browser fetch errors, and unknown exceptions use the caller's safe fallback.
3. **Application proxy/BFF** — never forwards raw upstream error bodies. It owns content-type validation, JSON parsing, minimal response reconstruction, and upstream protocol-failure status codes.
4. **Upstream or mock API** — returns the intended status and structured public error contract. Mock exceptions must be caught at the same boundary as live-backend exceptions.
5. **Framework runtime** — page-level and root-level error boundaries render recovery UI without `error.message`, digest, stack, paths, or configuration details.

## Reproduction sequence

1. Inspect the screenshot or visible alert before assuming the source.
2. Record the page route, request method/path, response status, content type, and body shape.
3. Reproduce the request directly against the proxy and through the browser form.
4. Capture browser exceptions, failed network requests, form submitting state, and the visible alert.
5. Use a controlled upstream fixture that intentionally returns HTML/invalid JSON to make the failure deterministic.
6. After the failure test, restore a healthy backend/mock and verify the same form plus representative authenticated routes.

## Fail-closed proxy policy

- Preserve the upstream HTTP status for structurally valid, explicitly public JSON errors.
- Treat all upstream `5xx` bodies as private. Return generic JSON; never relay upstream `message`, `stack`, HTML, paths, hostnames, tokens, or configuration.
- Treat missing/non-JSON error content types as an upstream protocol failure (normally `502`) with generic JSON.
- Do not trust a JSON content type by itself. Parse the body; malformed or falsely labeled JSON fails closed.
- Reconstruct the response as a minimal object such as `{ "message": "..." }`; do not spread or forward extra upstream keys.
- Safe `4xx` text must use an explicit public error code/message allowlist. **Do not use a growing blacklist of technical strings.** Blacklists miss novel DNS names, relative source paths, exception names, URLs, and credential formats.
- If no public code/message is approved, keep the original safe status and substitute a status-specific generic message.
- Network failures in live-only mode should return generic `502`; mock-handler exceptions should return generic JSON rather than a framework HTML page.

## Client policy

- `getErrorMessage` should reveal only messages produced by the trusted API-error policy.
- Arbitrary JavaScript errors always use the caller fallback.
- Keep technical payloads out of rendered state. If diagnostics are retained for development, never display them or serialize them back to the browser.
- Ensure `finally` or equivalent resets form/page loading state.
- Preserve useful recovery context: explain that retry is possible and that entered/saved data remains where true.

## Runtime boundaries

For Next.js App Router, add both:

- `app/error.tsx` for route-segment failures, with `reset()` and a safe return path.
- `app/global-error.tsx` for root-layout failures, with its own `<html>`/`<body>` and inline styling because global CSS/layout may be unavailable.

Never interpolate the caught error, digest, stack, request path, host, or environment values into these screens. Do not `console.error(error)` even only in development when the security contract forbids diagnostic exposure: the browser console is still a caller-visible channel. If observability is required, emit a fixed data-free event or use an explicitly redacted server-side path.

Add a source-level regression for both boundaries that rejects references to `error.message`, `error.stack`, or `error.digest` and rejects raw console logging. Keep the assertion broad enough to catch any `console.error`, `console.warn`, or `console.log` call in boundary files, not only a call whose first argument is literally named `error`.

## Regression matrix

Pin behavior at both client and proxy layers:

- HTML `500` with framework stack -> generic JSON and generic UI.
- JSON `5xx` containing message/stack -> generic JSON and generic UI.
- Missing content type -> generic `502`.
- HTML/plaintext mislabeled as JSON -> generic `502`.
- Malformed JSON -> generic `502`.
- Safe approved JSON `4xx` -> same status and approved public message.
- JSON `4xx` with extra stack/token fields -> only minimal public message survives.
- Unapproved JSON `4xx` containing Windows/POSIX paths, DNS names, source locations, URLs, SQL, exceptions, or credentials -> status-specific generic.
- Browser `Failed to fetch`, refused connection, and arbitrary errors -> caller fallback.
- Mock handler throw and live fetch rejection -> structured generic JSON.
- Form exits submitting state and exposes retry/recovery.
- Healthy login and representative desktop/mobile routes still work after the failure test.

## Process-state hygiene during smoke tests

- Treat a background watch-pattern notification as evidence that the pattern occurred, **not** that the process is still running when the notification is delivered.
- Before reporting server/browser state, check the tracked process list and, when relevant, the current port listener. Delayed readiness notifications may arrive after cleanup.
- After stopping a Windows dev-server wrapper, verify the application port is free before restart or production build; a child Node process can outlive its shell wrapper.
- Keep failure fixtures, dev servers, and headless browsers tracked separately. Stop each one after the corresponding failure/recovery assertion so stale processes cannot contaminate the next mode.
- On Windows/Git Bash, a long-lived Node fixture that exits or detaches under a normal background shell may stay reliable with a tracked PTY background process and a unique readiness marker. Probe the port after the marker; readiness text alone is not proof of a live listener.
- If a delayed notification arrives after verified cleanup, acknowledge it as stale rather than restarting, killing, or re-running tests based on that notification alone.

## Verification order

1. RED focused tests for the exact leak and malformed variants.
2. GREEN focused tests.
3. Direct proxy probe against the controlled failing upstream.
4. Browser form failure smoke: safe alert, no internals, submit re-enabled, no unhandled exception.
5. Healthy authenticated recovery smoke.
6. Lint, typecheck, production build, and full relevant tests.
7. Restore build-generated route-type churn such as `next-env.d.ts` before staging when the repository tracks a development import.
8. Run the read-only fail-closed review against the **exact current diff**. If the review causes another RED/GREEN patch, rerun the relevant full gate and review again; an earlier approval does not cover later changes.
9. Stage only intended files, verify the cached diff, commit/push, confirm local and remote hashes, then clean every test-owned listener. Restart only the user-requested app.
