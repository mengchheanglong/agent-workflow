# Wiring a Next.js prototype to a working mock-data layer

Use when a prototype has real screens but its buttons only fire toasts ("not built in this prototype") and the user asks to "make everything work with mock data". Goal: every action mutates shared in-memory state so queues, counts, badges, and record pages update everywhere — closing a case removes it from Overview, approving a destination unblocks the blocked payout.

## The pattern: one external store, seeded from existing seed data

Create `lib/mock-store.ts`:

```ts
"use client"
import { useSyncExternalStore } from "react"
import { NOW } from "@/lib/format"

let state = initialState()            // structuredClone(SEED_*_ARRAYS)
const listeners = new Set<() => void>()
function emit() { for (const l of listeners) l() }

export function useMockState() {
  return useSyncExternalStore(
    (onChange) => { listeners.add(onChange); return () => listeners.delete(onChange) },
    () => state, () => state,
  )
}

export function resetMockData() { state = initialState(); emit() }
```

Then one exported action per PRD workflow. Each action:

1. Maps/immutably updates the affected slice(s) — **including downstream slices** (approve destination ⇒ unblock settlements waiting on it).
2. Appends an audit entry (id, action, human-readable target, actor, role, ISO time, reason).
3. Calls `emit()`.

Do NOT persist to localStorage: refresh-resets-to-seed is a feature — reviewers always start from known state.

## Wiring checklist (per page)

- Replace seed-array reads (`rows={CASES}`) with `useMockState()` reads. Pages reading both stale out.
- Server components can't call the hook: convert to client by adding `"use client"` at line 1, using React `use(params)` instead of `await params`, and dropping `async`.
- **Remove `generateStaticParams` from any page converted to `"use client"`.** Next.js refuses both together: "App pages cannot use both \"use client\" and export function generateStaticParams()". The route renders dynamically — fine for a prototype. (Earlier guidance said keep it on seed constants; that only applies to pages that stay server components.)
- Convert ALL detail/record pages in one sweep (`head -1 app/**/**/page.tsx` loop), not just the one being edited. Partial conversion builds but 500s on the unconverted routes at runtime, which masquerades as a data bug.
- Swap each `onConfirm={() => notify.recorded(...)}` for the matching store action; keep a `notify.*` call for user feedback.
- Detail-page action components often need new props (e.g. `channel`) once they do real work — thread them from the page.
- Delete `.next` after moving/renaming route directories; stale generated route-type validators otherwise fail typecheck with phantom "Cannot find module .../page.js" errors.

## Verify against a production server, not the dev server

`tsc --noEmit` + `next build` + `next start -p <fresh-port>`, then curl every detail route expecting 200.

**Stale-server trap:** an orphaned dev server still holding port 3000 serves OLD compiled modules. Symptom: some routes 500 with no matching error in your code, or two servers racing ("Port 3000 is in use... using 3003", then EADDRINUSE). Fix: find the PID (`netstat -ano | grep :3000`) and kill it, or verify on a fresh port. Turbopack dev logs are at `.next/dev/logs/next-development.log`; ignore `EPIPE` entries (background-process kill artifacts).

## Reusable dialog component contract

If the prototype has a shared confirm-dialog, learn its exact contract before using it in N places. Common shape: `onConfirm(reason: string)` — the dialog owns the reason textarea and disables confirm until the reason has substance. Do not pass your own reason input as `children`; just consume the reason argument. One wrong assumption here produces a cascade of TS errors across every page you wired.

## Bulk renames

For id-prefix or path migrations across a large seed file, prefer one `sed -i 's/OLD-/NEW-/g'` over hand edits, then grep to confirm zero occurrences of the old prefix remain.

## New user-visible surfaces this pattern typically needs

- A "record a request" intake dialog on the queue page (channel, priority, reporter, linked record) — for support-style apps where off-platform requests are manually recorded before follow-up.
- A read-only "view the subject's own context" page behind assisted-access sessions (e.g. Support Access → open the merchant's store), wrapped in a persistent banner naming whose account you are in and whether the session is read-only or elevated. No edit buttons on that page by design; changes route back through elevation approval. Every view logs an action entry.
