# Frontend Shell Prototype Framework Selection

Use this when a user wants a functional mock-data shell that explains how many product features work together, but does not yet need production backend integration.

## Decide by artifact goal

| Goal | Default |
|---|---|
| One disposable, direct-open screen or a few static views | Standalone HTML/CSS/JS |
| Multi-page functional shell with reusable tables, drawers, dialogs, routing, roles, and local state | Vite + React + TypeScript |
| Prototype is expected to become part of an existing Next.js product, or needs SSR/server routes/auth integration now | Next.js |

Do not choose Next.js only because the production app uses Next.js. If the prototype is deliberately frontend-only, Vite keeps the review artifact isolated and lighter while preserving React component portability.

## Scope before scaffolding

1. Read the current approved feature inventory rather than stale SRS/prototype files.
2. Resolve overlapping concepts before creating routes. Prefer one owning feature with embedded capabilities over duplicate pages.
3. Separate current-version destinations from future-version expansions.
4. Keep contextual workflows—support access, recovery, retries, incident escalation—inside or launched from the records that own them unless independent navigation is needed for review discoverability.
5. Write a bounded build brief that states allowed directory, routes, required interactions, mock-data boundary, prohibited routes, and verification commands.

## Functional-shell standard

A feature is represented only when the reviewer can understand its purpose and perform a representative interaction. Avoid dead “coming soon” pages.

Minimum reusable system:

- responsive application shell and grouped navigation
- visible sample-data label
- global search that opens the owning module
- role selector with visibly different permissions
- page-specific mock records, statuses, and actions
- drawers/modals for record context
- stateful local workflows and user-visible feedback
- shared audit/event history for sensitive mock actions
- future-version panel that is informative but not presented as working navigation

For sensitive support access, begin read-only, require case context and consent for an exact low-risk elevation, and never model unrestricted impersonation.

## Verification

Run all applicable gates:

1. Typecheck, tests, and production build.
2. Assert exact equality between approved route inventory and route/page registry.
3. Assert prohibited or deferred concepts are absent as routes.
4. Scan source for accidental network calls when the shell must remain local-only.
5. Start the real dev or preview server and confirm HTTP success.
6. Inspect the rendered DOM/body text and browser console, not only screenshots.
7. Exercise representative state changes and permission differences.
8. Check desktop and mobile layouts, overflow, navigation, and touch targets.

A blank native browser capture is not enough to conclude that the app failed. Confirm the live DOM and console through an exact browser/debugging connection. Conversely, a passing production build is not enough to claim browser verification.

## Review communication for this user

When explaining proposed features or prototype decisions, use short plain language:

- **What it is:** one or two sentences.
- **Where it is used:** one concrete example tied to a real workflow.
- **Why now/later:** one sentence only when needed.

Do not lead with long state diagrams or implementation detail. Expand only after the user asks.