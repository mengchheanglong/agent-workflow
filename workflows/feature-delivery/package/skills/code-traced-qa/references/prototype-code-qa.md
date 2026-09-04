# Code-Traced Prototype QA — Full Checklist

For QA passes where the target is a running prototype backed by an in-memory
mock store (e.g. Next.js App Router + `useSyncExternalStore` client store
seeded from a seed file) and the brief says "verify with curl, trace logic by
reading source". Every reported defect must be traced to real code, not guessed.

## Workflow detail

1. Confirm the dev server is up WITHOUT restarting it:
   `curl -s -o /dev/null -w "%{http_code}" http://localhost:3000/<path>` for each scoped route. 200 means the route compiled.
2. Read the shared store/action layer first (`lib/*-store.ts`), then the scoped
   pages, then shared components they use (confirm dialog, command palette,
   data table), then the seed data.
3. Grep call sites of each exported action. An exported action with zero call
   sites (or imported-but-unused in a page) is itself a finding: the UI
   promises management the app cannot perform.
4. Cross-check seed IDs against ID-generation schemes (`id = prefix +
   length+1`) by asking: does anything ever REMOVE rows? If not, no collision;
   if yes, collision. Don't report hypotheticals.
5. Report format: `[BUG-n] severity | files | what breaks | repro | one-line fix`
   plus `[OK-n]` verified-working items. Only code-traced defects.

## Recurring bug classes (check every one)

- **Unreachable actions / dead imports** — page imports a mutation but never
  renders its control (e.g. enable/re-enable, role change). High: functional gap.
- **Missing self/last-admin guard** — destructive row actions (Disable) offered
  on the signed-in operator's own account because the table maps every row.
- **Group-label mismatch in searchable palettes** — items pushed with group name
  X but the render-order array lists Y; those results silently vanish from search.
- **Hardcoded per-session badges on cloned seed data** — mapping seed history
  with `thisSession: true` mislabels old entries. Flag state should be derived,
  not hardcoded in a map over the full list.
- **No double-submit guard on confirm dialogs** — onClick runs side-effect +
  close-via-parent-state; rapid double-click fires twice before re-render →
  duplicate audit/log entries. Check for a submitted ref or disabled flag.
- **Dialog claims vs store reality** — confirm-dialog "effects" text promising
  revocation/notification the mock action never performs. Compare effect copy to
  what the action function actually mutates.
- **Stale denormalized counters** — one mutation zeroes/decrements counts in one
  place only (disable clears session count; revoke-session doesn't). Trace every
  writer of each counter.
- **Missing uniqueness/format validation** — duplicate email/name checks absent;
  weak regex OK for prototypes if uniqueness exists. Boundary-test trim+minLength
  rules with whitespace-only input and exact-boundary lengths.
- **Regex safety of search filters** — safe if filtering uses
  `.toLowerCase().includes` or cmdk-style subsequence matching; unsafe if user
  query reaches `new RegExp`. Verify before reporting.
- **Layout overflow from unbounded text** — no maxLength on reason/note fields +
  rendered output lacking `break-words` → long unbroken strings overflow panels.

## Verified-OK patterns worth recognizing (don't false-positive these)

- Append-only audit implemented as unshift-prepend with no delete controls anywhere.
- Buttons hidden (not just disabled) for unreachable states (own current session,
  already-decided approvals, Healthy processes) — double-execution often NOT
  reachable even when the store action lacks a guard; check reachability first.
- Idempotent store actions (mark-provided style) neutralize double-clicks.
