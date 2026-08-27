# Workflow Reference Sources

This workflow borrows narrow, verified patterns from several systems. They are donors, not runtime
dependencies or authorities over the target repository.

## Anthropic Claude Code

- Code Review: https://code.claude.com/docs/en/code-review
- Custom subagents: https://docs.anthropic.com/en/docs/claude-code/subagents

Borrowed:

- dedicated review-only repository guidance (`REVIEW.md`);
- specialized/fresh reviewers with constrained tools;
- full-codebase context around an explicit diff;
- candidate verification, deduplication, severity, and pre-existing classification;
- review findings as advisory evidence that does not replace CI or human approval.

Not copied:

- vendor-specific subscription, GitHub App, cloud, pricing, or multi-agent fleet requirements;
- automatic mutation/fix during the authoritative review pass;
- neutral/non-blocking PR conclusions as the local readiness policy.

## OpenAI Codex

- Local code review: https://developers.openai.com/codex/code-review
- GitHub pull-request review: https://developers.openai.com/codex/third-party/github

Borrowed:

- dedicated reviewer against a selected base branch, commit, or uncommitted diff;
- prioritized actionable findings without modifying the working tree;
- repository-specific review rules in `AGENTS.md`;
- consequential domain rules in review guidance while deterministic formatting/lint stays in CI;
- optional detached/fresh review context.

Not copied:

- automatic PR review or cloud integration as a requirement;
- treating AI review as a replacement for tests, branch protection, or required approvals.

## GitHub Spec Kit

- Agentic SDD reference: https://github.com/github/spec-kit/blob/main/docs/reference/agentic-sdd.md

Borrowed:

- separate specification (`what/why`) from design (`how`);
- targeted clarification before planning;
- requirements-quality checklist as "unit tests for requirements";
- read-only cross-artifact consistency analysis before implementation;
- return contradictions to the artifact/stage that owns them;
- dependency-ordered, vertical implementation slices.

Not copied:

- a large command suite, generated directory tree, or separate artifact for every small feature;
- convergence loops without a bounded stop condition.

## obra/superpowers

- Requesting code review:
  https://github.com/obra/superpowers/blob/main/skills/requesting-code-review/SKILL.md
- Verification before completion:
  https://github.com/obra/superpowers/blob/main/skills/verification-before-completion/SKILL.md

Borrowed:

- explicit base/head review scope;
- fresh reviewer context rather than Builder session history;
- review early enough to prevent compounding errors;
- no completion claim without fresh proving commands;
- controller verification of agent-reported success;
- RED → GREEN evidence for behavioral changes.

Not copied:

- dogmatic process where a repository lacks an executable test route;
- unlimited review/fix loops;
- tool- or harness-specific commands as universal requirements.

## Local synthesis principles

1. Keep the core agent-agnostic and file-first.
2. Use native Claude Code, Codex, or another reviewer when available, but normalize the result into
   `.active/REVIEW.md`.
3. Tie review and human approval to a content snapshot so later edits invalidate stale evidence.
4. Let scripts/CI prove deterministic facts; use reviewers for requirement, behavior, risk, and
   cross-file reasoning.
5. Prefer one strong review contract and one validator over more roles or orchestration layers.
