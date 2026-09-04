---
name: code-traced-qa
description: "Use when QA traces prototype source instead of clicking."
version: 1.0.0
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [qa, testing, code-review, prototypes, web]
    related_skills: ["dogfood"]
---

# Code-Traced QA of Running Prototypes

## Overview

Sibling to the browser-driven `dogfood` pass (bundled skill). Use THIS variant
when the target is a running prototype backed by an in-memory mock store
(typical shape: Next.js App Router + client store via `useSyncExternalStore`,
seeded from a seed file) and the brief says to verify routes with curl and
trace logic by reading source — common for delegated subagent QA batches
("batch A/B/C") where only code-traced defects count as findings.

The core insight: in a mock-store app, **store actions define what CAN happen;
pages define what is REACHABLE**. Reading both layers and diffing them finds
bugs no click-through would.

## Workflow

1. Confirm the dev server is up WITHOUT restarting it:
   `curl -s -o /dev/null -w "%{http_code}" http://localhost:3000/<path>` per scoped route.
   200 = route compiled. Do not restart servers you didn't start.
2. Read in order: shared store/action layer (`lib/*-store.ts`) → scoped pages →
   shared components they use (confirm dialog, command palette, data table) → seed data.
3. Grep call sites of every exported action. An action imported but never
   rendered (or with zero call sites) is itself a finding: the UI implies
   management the app cannot perform.
4. Check ID-generation schemes against removal paths: `id = prefix + length+1`
   collides only if rows are ever deleted. Don't report hypotheticals.
5. Report format (typical batch contract):
   `[BUG-n] severity(Critical|High|Medium|Low) | files | what breaks | repro | one-line fix`
   plus `[OK-n]` verified-working items. Only REAL code-traced defects; cite
   line-level evidence.

## Coordinated implementation and evidence gates

For a broad pass, split work into bounded class-level lanes (routes/navigation,
core workflows, finance, security/admin, and adversarial/accessibility checks)
with an explicit file/route scope and report contract. Do not send one
unbounded “fix everything” prompt when the project is large: use a focused
repair lane for compile errors and one focused pass for remaining unreachable
UI actions.

A subagent summary is a lead, not evidence. Re-read the changed source and
rerun the project's own typecheck, lint, build, and route checks before
claiming a fix. When the project directory is untracked, `git diff` alone is
not a scope check: inspect `git status --untracked-files=all`, confirm the
repository root, and stage only the requested project directory.

For Next.js prototypes on Windows, a dynamic-route `500` containing a worker
retry/resource exception can be a dev-server failure rather than an app
failure. Build and start a clean production server on an alternate port; sweep
all top-level routes, representative *real seed IDs*, invalid IDs (expected
`404`), removed routes, and rendered-error markers. Keep the dev-server issue
as an environment note unless it reproduces in the clean production build.
Do not use guessed record IDs: derive valid IDs from the seed data first.

The reusable route-sweep and handoff details are in
`references/windows-nextjs-agent-qa.md`.

## Bug-class checklist (check every one)

See `references/prototype-code-qa.md` for the full checklist with examples from
real passes. Headliners:

- Unreachable actions / dead imports (enable/re-enable, role change never wired)
- Missing self-action guard (disable your own admin account)
- Group-label mismatch between palette item groups and render-order array → results silently dropped from search
- Hardcoded per-session badges mapped over cloned seed history
- No double-submit guard on confirm dialogs → duplicate audit entries
- Confirm-dialog effect copy promising revocation the store action never performs
- Stale denormalized counters after partial mutations (revoke vs disable)
- Missing duplicate/uniqueness validation; whitespace-only input passing/failing trim checks
- User query reaching `new RegExp` in search filters (safe: `.includes`, cmdk matching)
- Unbounded text fields without maxLength or `break-words` rendering

## False-positive traps

- Buttons hidden for unreachable states mean double-execution is often NOT
  reachable even when the store action lacks a guard — verify reachability
  before reporting "can run twice".
- Idempotent store actions neutralize double-clicks.
- Seeded data cloned into live state makes "seed vs live" bugs look like live bugs — check whether the mislabeled entry came from seed.

## References

- `references/prototype-code-qa.md` — full checklist + verified-OK patterns.
- `references/angkoro-admin-batch-c.md` — worked example: Angkoro Admin prototype-v2 batch C (admin accounts, audit, recovery, health, command palette), 10 findings.
