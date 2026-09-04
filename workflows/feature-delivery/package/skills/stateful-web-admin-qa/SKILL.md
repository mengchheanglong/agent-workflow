---
name: stateful-web-admin-qa
description: "Use for stateful web/admin QA and mutation verification."
version: 1.0.0
platforms: [windows, macos, linux]
metadata:
  hermes:
    tags: [qa, web, admin, permissions, state, audit, verification, dogfood]
    related_skills: [dogfood, requesting-code-review, doubt-driven-development, incremental-implementation]
---

# Stateful Web/Admin QA

## Purpose

Use this skill for repository-backed web applications—especially admin consoles and mock-backed prototypes—where correctness depends on mutable state, permissions, lifecycle transitions, auditability, and the difference between a reachable UI and a protected mutation seam.

This is a **source-traced plus runtime smoke** workflow. Browser interaction is a separate evidence layer. Never describe source inspection, a successful build, or an HTTP route sweep as complete button-by-button browser coverage.

## Evidence contract

Label every claim with the strongest evidence actually obtained:

| Evidence | Proves | Does not prove |
|---|---|---|
| Source trace | The route, caller, mutation, guards, state update, and audit path are connected | Runtime rendering or visual usability |
| Typecheck/lint/build | The current source compiles, lints, and produces the app | Correct business behavior or browser interaction |
| HTTP route smoke | Valid/invalid routes respond as expected and lack application-error markers | Button behavior, dialogs, keyboard flows, or visual quality |
| Browser interaction | The named interaction worked in the bound browser and state was observed | Unexercised routes or direct backend-call security |

Record unverified areas explicitly. A browser binding/setup failure is a limitation, not evidence that the feature works or fails.

## Workflow

### 1. Establish authority and scope

1. Read the repository instructions, project README, package scripts, and the product authority document before editing.
2. Define the allowed directory and excluded parent changes. If the target is ignored or untracked, plan an explicit scoped add and verify the index afterward.
3. Identify the role model, permissions, mock/backend boundary, state reset behavior, and prototype limitations. Do not invent backend, authentication, money movement, exports, or browser evidence.
4. Build a route and workflow inventory: list/detail pages, sensitive dialogs, mutation actions, invalid identifiers, and intentionally unavailable routes.

### 2. Trace every stateful workflow

For each sensitive workflow, follow this chain:

```text
route → component/caller → mutation function → validation/permission guard
      → state transition → audit/session side effect → rendered result
```

Inspect both the happy path and the direct mutation seam. A visible `PermissionGate` is a UX affordance, not backend authorization.

For every mutation, verify:

- role/permission is checked inside the mutation function;
- the target exists and stale/deleted IDs fail closed;
- user input is trimmed, bounded, type-checked, and semantically valid;
- lifecycle transitions are explicit and forward-only where required;
- the action is idempotent or repeated submission is blocked;
- the operator and reason are attributed without credentials or secrets;
- state changes, audit writes, and emits happen only after validation;
- the function returns an explicit boolean/result that callers can honor;
- list/detail/merchant views consume live mutable state rather than stale seed snapshots;
- cross-kind or cross-entity actions do not cascade beyond their scope;
- referenced records resolve or the UI shows an honest missing-state path.

### 3. Adversarial workflow matrix

At minimum, test or source-prove:

| Case | Expected behavior |
|---|---|
| unauthorized direct mutation | returns false/no-op; no audit or emit |
| unknown target ID | returns false/no-op; no fabricated audit |
| duplicate or rapid confirmation | one state change and one relevant audit entry |
| invalid/empty/oversized reason | rejected before mutation |
| stale dialog target | no success toast, no success session activity |
| multi-kind user | only selected access kind changes |
| already-final state | no illegal backward or duplicate transition |
| failed action callback | no success notification or “performed” activity record |
| historical audit record | remains attributed to original actor, not current session |
| sensitive admin action | no password/token/connection-string preservation |

For shared confirmation components, invoke the action before recording the operator activity and record only when the callback does not return `false`. Re-scan all callers after changing the callback contract; ignored booleans are a common source of false success.

### 4. Reachability and route smoke

1. Search for every mutation function and confirm a permitted UI caller exists when the product requires reachability. Do not add uncontrolled UI for intentionally out-of-scope seams.
2. Run the project typecheck, lint, and production build.
3. Start a clean production server on a temporary port and sweep representative valid routes plus invalid IDs and intentionally absent routes.
4. Assert status codes and scan responses for real application-error markers/digests; distinguish framework error-boundary template text from an actual failure.
5. Treat known non-fatal warnings separately from failed gates.

### 5. Browser verification, if available

Use the current desktop/browser binding workflow, capture before and after mutations, and verify:

- keyboard focus and Enter/Space activation for row navigation;
- dialogs require and preserve reasons;
- success/failure toasts match the observed state;
- repeated clicks do not duplicate the mutation;
- list/detail values update from live state;
- visual and responsive behavior for the tested viewport.

Report exactly which flows were browser-tested. Do not infer browser coverage from source or HTTP checks.

### 6. Independent review and timeout recovery

Freeze the review unit by commit or content hash. Give an independent reviewer only the relevant diff/current files, contract, and static-scan results—not the implementer’s conclusion.

For a large or newly tracked snapshot, partition review by risk surface:

1. permissions/authz and sensitive mutations;
2. state transitions, idempotency, and audit/session effects;
3. referential integrity and route reachability;
4. UI behavior and remaining files.

Require a structured fail-closed verdict: security or logic errors make `passed=false`; malformed or incomplete output is not approval. A reviewer timeout is **no evidence**, not a pass. If it times out:

1. do not claim independent approval;
2. keep the current artifact/hash explicit;
3. dispatch a bounded narrow review of the highest-risk files;
4. independently inspect every reported finding against the current source;
5. fix confirmed issues, rerun gates, and review the new hash if the artifact changed.

Never treat a late verdict about an old snapshot as approval for a newer commit.

### 7. Staged scope and delivery

Before commit:

```bash
git add -A -- <target>
git diff --cached --check
git diff --cached --name-only
```

Assert every staged path is inside the approved target. Scan staged content for credentials, generated artifacts, dependency/build directories, and accidental QA outputs. Prefer a parser-backed scan over a broad shell regex that can flag legitimate code such as `.exec()` calls.

Only after source inspection, independent review evidence (or an explicitly documented narrow fallback), gates, staged-scope checks, and report creation:

1. commit the target-only changes;
2. push the branch;
3. open or update the PR;
4. verify the pushed HEAD and PR metadata;
5. report commit, PR, commands, warnings, limitations, and exact evidence levels.

## Fix loop

Fix concrete security/logic defects in small batches. After each batch, rerun typecheck, lint, build, and the relevant route/source checks. Do not broaden scope to speculative product decisions. If a reviewer finds a false-success path, trace all sibling callers before stopping; the shared component contract often exposes more than the first named page.

## Common pitfalls

- UI-only permissions: direct callers can bypass them unless the mutation seam also checks role.
- Stale seed snapshots: mutable list/detail pages appear correct until a mutation is performed.
- Ignored prototype directories: a clean parent status does not mean the intended files are tracked; verify the staged index.
- False success: callers ignore a boolean mutation result and close dialogs, toast success, or record activity anyway.
- Audit-before-action: recording activity before the mutation succeeds creates an inaccurate operator history.
- Reviewer self-report: “fixed” or “passed” is a claim; inspect the diff and rerun the gates.
- Reviewer timeout: no verdict; use a bounded risk-partitioned fallback, not an invented approval.
- Browser limitation: report source/HTTP evidence separately and do not claim complete interaction coverage.
- Prototype limitations: document missing file generation or backend behavior instead of inventing it.

## Related references

- `references/source-traced-stateful-qa.md` — compact risk matrix, review recovery recipe, and evidence/report checklist.
