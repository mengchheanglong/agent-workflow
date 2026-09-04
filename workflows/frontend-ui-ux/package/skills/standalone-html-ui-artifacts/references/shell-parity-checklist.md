# Shell parity checklist — port these structures from production

Condensed, class-string-exact checklist for making a prototype's shell and shared
components match a production app. Proven on Angkoro (prototype-v2 vs
Angkoro-Frontend). Full context lives in
[`design-system-sync-from-production.md`](design-system-sync-from-production.md).

> **First: pick the right ancestor.** Production apps may carry multiple in-app
> patterns (Angkoro-Frontend has both a merchant sidebar dashboard AND sidebar-less
> admin pages using `container mx-auto` + gradient banner). Check the production repo
> for its own existing admin pages before defaulting to the storefront dashboard as
> the sync target — see "Identify the RIGHT ancestor pattern" in the main reference.

## Sidebar (merchant-dashboard ancestor)

- Model: fixed full-height `w-64` card rail (`bg-card border-r border-border`), NOT a
  dedicated sidebar-token surface — FE merchant dashboard uses plain card colors.
- Header: brand icon (`h-5 w-5 sm:h-6 sm:w-6 text-primary`) + wordmark
  (`text-base font-semibold sm:text-lg`), container `p-3 sm:p-4 md:p-5 border-b`.
- Group labels: `px-3 pb-1 pt-4 text-[10px] font-bold uppercase tracking-wider
  text-muted-foreground/70`.
- Nav rows: `flex items-center gap-3 rounded-lg px-3 py-2 text-sm sm:text-base
  font-medium`; active `bg-accent/15 text-accent`; inactive `text-muted-foreground
  hover:bg-muted hover:text-foreground`. Icons `h-4 w-4 sm:h-5 sm:w-5`.
  A different active treatment reads as a different product even with identical colors.
- Role-limited rows: dimmed (`opacity-40`) + lock icon replacing the icon; keep the row
  clickable-or-not per PRD but never silently hide it.
- Mobile: backdrop `bg-background/80 backdrop-blur-sm`, slide via `-translate-x-full`
  ↔ `translate-x-0`, hamburger in header only `lg:hidden`.
- If production has no collapse button, remove yours.

## Top bar

- `sticky top-0 z-30 flex items-center gap-2 border-b border-border bg-card p-3 px-3
  sm:gap-4 sm:px-4 md:px-5 lg:px-6`.
- Left (mobile only): menu button. Then search field (`max-w-md flex-1 h-9 rounded-lg
  border border-input bg-background`). Right cluster: theme toggle, language toggle,
  account control.
- Account control: avatar-with-fallback (`size-8`, `bg-primary/10 text-xs font-semibold
  text-primary`) + name/email two-line block (`hidden min-w-0 md:block`) in a
  `hover:bg-muted rounded-lg p-1` button — not a bare initials circle.

## Layout

- Fixed sidebar ⇒ `<div className="lg:pl-64">` around header + main.
- Main padding ladder (merchant-dashboard ancestor): `p-3 sm:p-4 md:p-5 lg:p-6`.
- Page wrapper: `min-h-screen bg-background`.
- **Admin-page ancestor alternative (no sidebar):** gradient banner
  (`bg-linear-to-r from-primary to-primary/80 text-primary-foreground py-2.5 sm:py-3`)
  with "Super Admin Only Interface" label, then
  `container mx-auto px-3 sm:px-4 md:px-6 py-6 sm:py-8 space-y-4 sm:space-y-5`.

## Shared page components

- **PageHeader h1:** merchant ancestor: `text-2xl font-extrabold tracking-tight`;
  admin ancestor: `text-2xl sm:text-3xl font-bold` with
  `mt-2 text-base text-muted-foreground` description.
- **KPI/stat card:** label ABOVE value — `text-xs font-semibold text-muted-foreground`
  then `mt-1 text-2xl font-extrabold tracking-tight tabular-nums`; tone colors use the
  `-ink` tokens. Card shell `rounded-xl border bg-card p-4 shadow-(--shadow-card)`.
- **Status badge:** leading dot inside the pill (`span size-1.5 rounded-full bg-current`)
  before the label; variant from a lowercase-keyed status map, unknown → muted.
- **Empty state:** dashed panel `border-[1.5px] border-dashed border-border rounded-xl
  px-6 py-10 text-center`; optional icon in tinted square (`bg-accent/15`).

## Method

Diff one production screen beside its prototype equivalent element by element — header,
first KPI row, first list rows, sidebar hover/active. Structural diffs are visible in
seconds; token diffs are not. Grep both codebases for the same component names' class
strings to catch typography drift mechanically.
