# Codex Review Adapter

Use Codex as an optional dedicated reviewer while keeping the repository workflow agent-agnostic.

Official references:

- https://developers.openai.com/codex/code-review
- https://developers.openai.com/codex/third-party/github

## Preferred local flow

1. Record the base branch/commit, allowed paths, fresh validation, and current snapshot.
2. Start a dedicated review against that exact scope using Codex `/review` in the CLI, IDE, or app.
3. Choose review against the base branch/commit or uncommitted changes as appropriate.
4. Use detached/separate review context when available.
5. Codex review should report prioritized findings without changing the working tree.
6. Normalize the result into `.active/REVIEW.md` and synchronize `.active/STATE.json`.

## Repository guidance

Codex reads applicable `AGENTS.md` files. Keep durable, consequential review checks in a concise
`## Code Review Rules` section near the code they govern. State the unsafe behavior and safe path.
Leave deterministic formatting, lint, generated-file, and dependency checks to scripts/CI.

This package's root `REVIEW.md` remains the full review contract; reference it from `AGENTS.md` when
Codex is the engine.

## Pull-request review

GitHub `@codex review` can provide another pass, but it does not replace tests, branch protection,
required human approval, or local snapshot freshness. A later push changes the snapshot and requires
a current review under this workflow.

## Do not copy

- cloud/PR integration as a prerequisite;
- automatic fixes before findings are reconciled;
- broad generic style rules that create noise;
- a Codex PASS without checking that it covered the recorded feature diff and current snapshot.
