# PRD-to-Prototype Reconciliation (Angkoro admin)

Session pattern for rebuilding an existing prototype to match a newly approved PRD
version, when the PRD changed scope between versions. Proven moving prototype-v2 from
PRD v5.0 (four roles) to v5.3 (two roles) in the Angkoro admin dashboard.

## Sequence that worked

1. **Audit before editing.** Diff old-PRD vs new-PRD mechanically: role tables,
   out-of-scope lists, section/navigation names, requirement IDs. Produce the change
   list first; do not start deleting files on vibes.
2. **Rewrite the permission model first.** Roles/permissions live in one lib file and
   seed data references it everywhere — changing it last forces rework. Map every
   permission to its new-PRD clause (`source` field) so the UI can show which rules are
   confirmed vs proposed.
3. **Move/rename route folders with `mv`, then rewrite page contents.** Next.js App
   Router: folder name = route. `merchant-accounts/[merchantId]/` →
   `users/[userId]/` including dynamic segment rename and param variable renames inside.
4. **Delete removed modules outright** (page + nav entry + search-palette entries +
   cross-links from other pages). Grep for the old route string across the whole app to
   find stragglers — links from settlements detail pages and store records were the
   ones that survived longest.
5. **Update seed data to demonstrate new semantics**, not just renamed fields: e.g. a
   user holding several account kinds at once, a banned shopper whose restriction did
   NOT cascade to stores — seed data exists to show workflow rules, not fill tables.
6. **Sweep prose**: page headers, callouts, comments, empty states. Old wording
   ("the four fixed roles", module names) survives in copy long after code is correct.
7. **Verify**: typecheck, lint, production build, then live dev server smoke test —
   200 on kept routes, **404 on removed routes** (catches stale generated types:
   delete `.next` if validators reference deleted pages).

## Pitfalls

- `.next/dev/types/validator.ts` keeps type errors for deleted routes after the files
  are gone → `rm -rf .next` and re-run typecheck.
- Component prop shapes drift silently: DataTable filter objects use `label`, not
  `header`. Check the component's exported types before writing new usage.
- sed for ID prefixes across seed data (`MER-` → `USR-`) is safe and fast when the
  prefix is unambiguous; verify with grep counts afterward.
- When re-syncing UI primitives from the production repo, re-apply prototype-only
  extensions afterward (e.g. a dialog that gained an extra prop the command palette
  depends on) — the verbatim copy silently breaks dependent pages otherwise.
- Keep the prototype README's authority pointer updated to the new PRD filename —
  prototypes get rebuilt months later against whatever doc they cite.

## Converting notify-only stubs into working mock state (the "make everything work" pass)

A prototype built to *display* requirements has many handlers that only fire a toast.
The pass that makes everything work follows this order:

1. **One central store before any page edits.** A single seeded in-memory state object
   with typed actions per workflow (`useSyncExternalStore` + module-level state), where
   every action also appends to an audit trail and emits to all subscribers. This gives
   cross-feature reactivity for free: approving a destination unblocks a payout; both
   appear in Overview counts; every action lands in Security & Activity without extra
   wiring. Reset on refresh (no persistence) so reviewers always start from seed.
2. **Server/client boundary is the main build risk.** Detail pages that were server
   components (`async function`, `await params`, `generateStaticParams`) break the
   moment they call a client hook. Convert: add `"use client"`, swap `await params` →
   `use(params)` from React, **delete `generateStaticParams`** (Next refuses both on
   one page). Do this proactively for every `[param]` detail page you touch —
   converting half leaves a confusing mix of 200/500 routes.
3. **ConfirmAction-style dialogs pass the reason as a callback arg**, not children:
   `onConfirm={(reason) => action(..., reason)}`. Don't fight the shared component's
   contract with custom body content unless you extend its props deliberately.
4. **Seed data must demonstrate workflow chains**, e.g. one payout Blocked on a
   destination review so approving the destination visibly unblocks it; a case whose
   outcome was "merchant responsibility" to demo R2.9 routing.
5. Verify with a production build + `next start` route sweep, not just dev mode —
   prerender errors (server component calling client hooks) only surface on build.

### Dev-server zombie pitfall (Windows)

After many restarts, orphaned `next dev` processes hold port 3000 serving a torn
`.next` cache. Symptom: a dark Next.js overlay reading "Jest worker encountered N child
process exceptions, exceeding retry limit", usually on recently-changed routes; curl
returns 404/500 while `npm run build && next start` serves the same routes fine. Fix:
kill all node listeners (`Get-Process node | Stop-Process -Force` or
`Stop-Process -Id <pid> -Force`), `rm -rf .next`, start one clean server. Diagnose by
comparing `curl` against dev vs `next start` — if prod works and dev doesn't, it's the
cache/process, never the code. Note `taskkill //PID x //F` from git-bash silently
fails on some hosts; use PowerShell `Stop-Process`.

**Count check:** after a long session of restarts, run
`Get-Process node | Measure-Object | Select-Object -ExpandProperty Count` — dozens of
orphaned workers means the compile pool is exhausted and pages fail *randomly*
(some 200, some 500, flaky between requests). Kill them all before concluding anything
is wrong with the code. Also: starting a second `next dev` while one runs does NOT take
over port 3000 — Next detects it and silently binds 3003+, so your curl against 3000
hits the stale server no matter how many times you "restart". Always verify which PID
owns the port (`netstat -ano | grep :3000`) before testing.

## Related

- [`design-system-sync-from-production.md`](design-system-sync-from-production.md) —
  when the same reconciliation also requires matching the production app's design system.
