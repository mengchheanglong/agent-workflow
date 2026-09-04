# Session record: Angkoro admin prototype-v2 — PRD reconciliation, mock wiring, design sync, production pass

Context: Next.js App Router prototype of an internal admin system (PRD v5.3, two roles Admin/Super Admin) that must share a design system with a separate merchant storefront repo (`Angkoro-Frontend`). Workspace: `dashboard/admin/prototype-v2`.

## What the session did, in order

1. **PRD v5.3 alignment** — collapsed four roles → two, replaced `merchant-accounts` module with multi-kind `users`, folded shopper support into Support & Concierge, deleted standalone Exports. Old routes verified 404.
2. **Design-system sync** — copied FE's globals.css tokens, all 28 `components/ui/*` primitives verbatim, logo/favicon, fonts already matched.
3. **Mock-state wiring** — one seeded store (`useSyncExternalStore`), ~30 typed actions, every page live.
4. **Shell parity round 1** — copied FE *merchant dashboard* shell (sidebar + sticky card topbar). User still said "feels very different".
5. **Shell parity round 2** — discovered FE also has *admin pages* (`admin/bank-accounts`, `admin/activity-logs`) with a different pattern (gradient banner, `container mx-auto` centered column, `text-2xl sm:text-3xl` titles, uppercase table headers). Applied THAT pattern to content area; kept sidebar shell.
6. **Production-readiness pass** — removed P0/P2 priority chips from 25 page headers, rebuilt badges on shadcn Badge variants with status dots, callout icon chips, FE-style empty states, normalized spacing to one ladder.
7. **Role switcher removal** — fixed Super Admin session, deleted `setRole` plumbing.

## Key learnings (beyond what's in SKILL.md pitfalls)

### The "two platforms" complaint is layered
User feedback "the ui/ux looks and feel very different" persisted after token+primitive sync. Only resolved after matching: sidebar structure (fixed w-64 bg-card, Store icon header, `bg-accent/15 text-accent` active rows), topbar contents order, `container mx-auto px-3 py-6 sm:px-4 sm:py-8 md:px-6` content column, per-component typography (KPI label `text-xs font-semibold muted` over `text-2xl font-extrabold tabular-nums`), and page spacing rhythm. Lesson: budget for a component-by-component diff pass, not just a token diff.

### Production repos have multiple shells — match the analogous one
Angkoro-Frontend has a sidebar-based merchant dashboard AND banner-based super-admin pages (`Super Admin Only Interface` gradient strip + container layout). An internal admin prototype should mirror the existing *admin* pages' pattern where they exist.

### Server/client conversion recipe (repeated 5×)
Pages needing client store hooks that were originally server components:
```
"use client" at top
export default function X({ params }: { params: Promise<{id:string}> }) {
  const { id } = use(params)   // from react, not await
```
and DELETE `generateStaticParams` (build error: "App pages cannot use both use client and export generateStaticParams"). Build error signature for forgetting: "Attempted to call useMockState() from the server".

### Bulk prop removal across pages
Removing `priority="P?"` from PageHeader across ~15 files: first python regex sweep caught multi-line occurrences but missed same-line ones; second `sed -i 's/ priority="P[0-9]"//g' $(grep -rl ...)` via explicit file list finished it. Always re-grep + typecheck after.

### Zombie dev servers (Windows)
After many restarts: 71 orphaned node processes; port 3000 held by a stale PID serving torn cache; overlay showed "Jest worker encountered 2 child process exceptions". Production build passing cleanly while dev 500s = environment, not code. Full fix needs user-run mass kill (`Get-Process node | Stop-Process -Force`) because agent-initiated mass kills are consent-gated and kill unrelated apps. Workaround during session: run verification builds + `next start -p 30xx` on alternate ports.

### PRD-driven feature moves
Support Access removed; its read-only merchant view moved into Stores as `[storeId]/merchant-view` with attribution banner + audit logging per R1.8/R3.8; Super Admin direct-change dialog (change + consent-method + reason, all required) added per R3.9/R3.10 with history panel. Ghost-term sweep after removals: grep for old feature names in seed audit actors, role summaries, callout copy, permission sources — not just routes.

### Verification loop that worked
`tsc --noEmit` after every file batch → `npm run lint` → `npm run build` → background `npx next start -p <free-port>` → curl route matrix (all lists + representative detail routes + removed routes expecting 404) → kill server. Dev server used only at the end for user's manual review.
