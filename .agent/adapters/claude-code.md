# Claude Code Review Adapter

Use Claude Code as an optional independent review engine. The repository workflow remains the
authority.

Official references:

- https://code.claude.com/docs/en/code-review
- https://docs.anthropic.com/en/docs/claude-code/subagents

## Preferred local flow

1. Finish controller-owned validation and compute the current snapshot.
2. Start a fresh Claude Code review context from the repository root.
3. Review the recorded feature diff, not an unspecified "recent change".
4. Keep the review read-only. Do not use `--fix` for the authoritative pass.
5. Normalize findings into `.agent/templates/REVIEW_TEMPLATE.md` and save the result as
   `.active/REVIEW.md`.
6. Record reviewer identity/session, snapshot, verdict, and counts in `.active/STATE.json`.

Interactive Claude Code can use its local review command:

```text
/code-review <recorded base branch or commit>
```

Use the command form supported by the installed Claude Code version. Confirm the displayed scope
before launch.

## Review guidance

Claude Code reads root `CLAUDE.md` for broad project context and can use root `REVIEW.md` for
review-only rules. This package supplies `REVIEW.md`; do not duplicate it into a large vendor-specific
prompt.

Managed PR review and ultrareview may use multiple specialist agents and verification passes, but
they are optional. Their neutral GitHub check does not become `G6_REVIEW` automatically. Reconcile
actual findings and apply this workflow's verdict rules.

## Custom subagent fallback

When native review is unavailable, use a fresh project subagent with read-only tools. Give it:

- `.active/FEATURE.md`;
- `.active/DECISIONS.md`;
- `REVIEW.md`;
- base/head scope and current snapshot;
- actual diff and relevant surrounding code;
- fresh validation evidence.

Do not pass Builder conversation history. If the subagent cannot access Git safely, the coordinator
must provide the frozen diff explicitly.

## Do not copy

- vendor subscription/cloud setup into repository policy;
- auto-fix in the same pass as authoritative review;
- every Claude reviewer agent as a permanent local role;
- a managed review's severity vocabulary without mapping it to BLOCKER/MAJOR/MINOR/NIT.
