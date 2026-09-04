# Design-System Sync from a Production Frontend

Use when a prototype (standalone HTML, Vite, or Next.js) must look and behave like the
user's production app — same colors, fonts, components, and folder conventions. Trigger
phrase to expect: "copy everything from it, we don't want two different platforms."

Proven on Angkoro: `admin/prototype-v2` (Next.js 16 + Tailwind v4 + shadcn/ui) synced
against `Angkoro-Frontend` (production merchant app).

## Audit first — diff, don't assume

Never trust a claim that tokens/components "already match." Diff mechanically:

1. **Token diff:** extract every `--token: value` from `:root` and `.dark` blocks in both
   `globals.css` files and compare key-by-key (a small Python script beats eyeballing —
   the raw diff is hundreds of lines and hides real drift among comment churn).
2. **Primitive diff:** `ls` both `components/ui/` directories; then `diff` each shared
   file. Expect three categories:
   - missing files (production has them, prototype doesn't) → copy over;
   - `"use client"`-only diffs → cosmetic; the prototype needs the directive for Next
     client interop — copy the production file, then re-prepend `"use client"`;
   - real extensions the prototype added (e.g. an extra prop) → copy production
     verbatim, then **re-apply the extension** on top.
3. **Font/layout diff:** compare root `layout.tsx` — `next/font` setup, weights,
   favicon links, metadata. Copy the font stack verbatim (same families, same weight
   arrays) so Khmer/Latin mixed text never falls back differently.
4. **Branding assets:** copy `public/logo.svg`, favicon, etc. into the prototype and add
   the same `<link rel="icon">` references.
5. **Dependency gap:** new primitives import packages the prototype lacks (e.g. embla,
   react-hook-form, extra @radix-ui packages). `npm install` them, then typecheck.

## Rules

- Production `globals.css` is the source of truth. Never re-pick values in the
  prototype; change upstream, copy down.
- Prototype-only additions must be **explicitly documented in-file** (a comment naming
  why it exists, e.g. status-ink tokens added for light-mode AA contrast) so the next
  sync doesn't mistake them for drift and delete them.
- When copying a production primitive that the prototype extended, restore the
  extension immediately after the copy — the diff from step 2 is your checklist.
- Library-shipped code can trip strict lint rules (e.g. `react-hooks/set-state-in-effect`
  inside shadcn carousel). Suppress with a targeted `eslint-disable-next-line` plus a
  comment explaining it is the library's own pattern — do not rewrite vendored code.
- After sync: `tsc --noEmit`, `lint`, `build`, and a live-route smoke test (expect 200 on
  kept routes, 404 on removed ones).

## Folder-structure mirroring

When the user asks for "everything, even the folder structure," mirror the production
conventions (`components/ui`, `components/common`, `components/layout`,
`components/pages` in Angkoro-Frontend) rather than the prototype's ad-hoc layout, so
code ports across without reorganization.

## Identify the RIGHT ancestor pattern before syncing (user push-back signal)

Production apps often carry **multiple in-app patterns for the same class of page**, and
syncing against the wrong one produces "this still looks different" even after tokens,
primitives, and shell all match. Angkoro-Frontend had TWO:

1. **Merchant dashboard** (`app/s/[subdomain]/dashboard/`) — fixed sidebar rail layout.
2. **Existing internal-admin pages** (`app/(pages)/admin/bank-accounts`,
   `admin/activity-logs`, `admin/promo-codes`) — NO sidebar at all: a gradient
   "Super Admin Only Interface" banner (`bg-linear-to-r from-primary to-primary/80`),
   then `container mx-auto px-3 sm:px-4 md:px-6 py-6 sm:py-8 space-y-4 sm:space-y-5`
   content column.

When building an admin/ops prototype inside such a codebase, grep the production repo
for its own existing admin pages FIRST (`grep -rn 'container mx-auto'` /
`ls app/**/admin*`) — those are the true ancestors, and stakeholders will compare your
prototype against them, not against the storefront dashboard. The admin-pattern specifics
that differed from the merchant-dashboard sync:

- Title: `text-2xl sm:text-3xl font-bold` + `mt-2 text-base text-muted-foreground`
  description (not `text-2xl font-extrabold`).
- Filter bar above lists: full-width search stacked on mobile → row on desktop
  (`flex flex-col gap-3 sm:flex-row sm:items-center`), search `max-w-md`, count badge
  hidden below `sm`.
- Lists are bordered tables (`rounded-xl border border-border bg-card` wrapper,
  `bg-muted/50` header, `px-4 py-3` cells, `[11px] uppercase tracking-wider` column
  heads) — FE dashboards use Card-based rows instead; pick per audience.
- KPI ladder: `grid grid-cols-2 gap-3 sm:gap-4` (+ `lg:grid-cols-3/4`), not
  `sm:grid-cols-2 xl:grid-cols-4`.

If you synced against the wrong ancestor, the fix is cheap: adjust only the shell wrapper
and the shared page components (PageHeader / StatCard / DataTable control rows) — tokens
and primitives are unaffected.

## Layer 4 — the application shell (what users actually mean by "still feels different")

A token + primitive sync is necessary but NOT sufficient. After a full token/primitive
sync the user still reported the apps "look and feel very different" — because the
**shell** differed. Read the production dashboard layout and shell components directly
(e.g. `app/.../dashboard/layout.tsx`, `DashboardSidebar.tsx`, `DashboardHeader.tsx`)
and rebuild the prototype shell to match structurally:

- Sidebar model: fixed-width card rail vs collapsible icon rail (match production; if
  production has no collapse button, remove yours).
- Exact nav-row classes: rounding (`rounded-lg px-3 py-2 text-sm sm:text-base`), active
  state (`bg-accent/15 text-accent`), group label style (`text-[10px] font-bold uppercase
  tracking-wider text-muted-foreground/70`). These differ from generic sidebar-token
  classes even when the tokens themselves match.
- Sticky header composition: menu button left / search field / theme+language+account
  right on a `bg-card border-b` bar.
- Account control pattern: avatar-with-fallback plus name/email row vs a bare initials
  circle — small, but instantly recognizable.
- Content offset and padding ladder: `lg:pl-64` + `p-3 sm:p-4 md:p-5 lg:p-6`.
- Shared page components: compare class strings for PageHeader heading
  (`text-2xl font-extrabold`, not `text-xl font-bold`) and KPI/stat cards
  (`text-xs font-semibold muted` label over `text-2xl font-extrabold tabular-nums`
  value). One weight step off reads as "a different platform" even when every color
  matches.

Grep both codebases for the same component names' class strings to catch typography
drift mechanically rather than by eye.

## Diagnosing a "feels different" complaint

When the user says it still feels off after a sync, don't re-diff tokens — open one
production screen beside its prototype equivalent and diff element by element: header
block, first KPI row, first list rows, sidebar hover/active state. The divergence will
be in type weight/step, spacing rhythm, or an app-level wrapper component (PageHeader /
StatCard / EmptyState equivalents) authored fresh with different classes. Structure,
spacing, and weight carry sameness; palette does not.

## Related

- [`shell-parity-checklist.md`](shell-parity-checklist.md) — condensed port-me checklist
  of shell/component anatomy with the FE-proven class strings.
