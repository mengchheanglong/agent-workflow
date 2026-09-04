# Windows/Next.js Agent QA Reference

Use this reference when a prototype QA pass combines source tracing, delegated fixes, and route checks.

## Bounded agent lanes

Split large work by defect class rather than asking one worker to inspect and fix the whole app at once:

- routes, navigation, and invalid IDs;
- core records and state persistence;
- finance and permission gates;
- security, admin accounts, and recovery;
- adversarial input, shared components, and keyboard behavior.

Give each worker an allowlist of files/routes and a report contract. A worker's summary is not proof: verify the changed source and rerun gates in the parent checkout. If a broad worker times out, preserve its partial edits, inspect the actual diff/state, and use a smaller repair prompt rather than restarting the whole pass.

## Production route evidence

1. Confirm the seed IDs before probing dynamic routes. Do not invent an ID from memory.
2. Run `npx tsc --noEmit`, `npm run lint`, and `npm run build` from the prototype directory.
3. Start `next start`/the project's start script on a clean alternate port.
4. Sweep top-level routes, real seeded detail IDs, invalid IDs, and retired routes.
5. For each response record status, body size, and whether the rendered body contains a real application-error marker (`>Application error<` or a digest marker).
6. Treat a development-only worker/resource `500` as a test-environment signal until the clean production build reproduces it.

A compact Python/urllib sweep is more reliable than a shell loop when Windows path translation makes temporary output files ambiguous: catch `HTTPError`, retain its body, and print a JSON row per route.

## State/action verification

For mock-store prototypes, compare exported actions with page call sites. An action that exists in `lib/mock-store.ts` but has no reachable UI is a real feature-reachability finding unless the product explicitly documents the boundary as read-only. For each fix, verify:

- the page reads `useMockState()` when the action mutates that entity;
- action guards reject missing, invalid, repeated, or unauthorized requests;
- `emit()` runs after successful mutation;
- audit/history entries are append-only and accurately attributed;
- detail, list, counters, and related views use the same live record.

## Git scope for untracked prototypes

Before committing, inspect the repository root and `git status --untracked-files=all`. An untracked prototype produces no useful `git diff` until staged/intent-to-added. Stage only the requested prototype directory (plus an explicitly requested QA report); do not absorb unrelated parent-worktree changes. Run `git diff --cached --stat` and `git diff --cached --check` before pushing.

## Coverage honesty

HTTP/source checks establish route and logic evidence, not proof that every button, dialog, keyboard interaction, or visual state was clicked. Report browser-level coverage separately and do not convert a route sweep into a claim of complete interaction testing.
