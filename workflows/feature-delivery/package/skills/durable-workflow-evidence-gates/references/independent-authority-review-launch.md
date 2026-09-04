# Independent Authority Review Launch

Use when a frozen preflight/plan/driver (or equivalent authority unit) must receive independent `APPROVE` or `REJECT` before scoped commit and live execution.

Also use this pattern for **documentation-only authority changes**. Markdown/JSON is not
"just docs" when it controls project activation, permissions, scheduled jobs,
current state, scientific/regulatory claims, or sealed-evidence routing.

## Documentation authority review checklist

For parked, capital-gated, monitoring-only, or otherwise restricted projects, give
the reviewer the intended state transition and require checks for:

- the milestone signal versus a separate reviewed activation decision;
- explicit machine-readable false guards for implementation, recruitment,
  purchases/licensing, outreach/partnerships, clinical or human activity, and
  autonomous watchers where applicable;
- every live root/nested router, current/next/research view, machine state, and
  selected mission/status surface;
- historical decisions and sealed experiments remaining historical rather than
  being rewritten to look retrospectively consistent;
- expired windows and zero-job scheduler observations not being promoted into a
  final outcome without source verification and reconciliation;
- cadence selection not silently becoming automation authorization;
- dated technology/regulatory claims checked against first-party sources through
  the claimed review date, with designation, approval, upcoming trial, and
  demonstrated result kept distinct;
- unsupported qualitative labels (for example high/low bandwidth) removed unless a
  reviewed source supports them;
- relative links resolved from each containing file;
- implementation repositories, sealed artifacts, and named excluded user-owned
  files unchanged.

If search/extract tooling fails transiently, the reviewer may inspect known
first-party URLs through direct HTTP retrieval. Preserve the verified fact and
source boundary; do not encode the temporary tool failure as a durable limitation.

After a `REJECT`, repair every blocking contradiction and rerun the same state,
link, source, diff, and semantic-review gates. An approving second review does not
retroactively validate the rejected tree.

## Prefer content-embedded, tool-free review

For a small frozen file set, embed the full authority files and only the minimal frozen-source excerpts needed. Instruct the reviewer:

- no tools, shell, network, or live filesystem exploration;
- first line exactly `APPROVE` or `REJECT`;
- must-fix blockers only, with path/function and exact repair;
- optional improvements separately;
- model prose is non-authoritative.

This avoids Windows reviewers that stall on exploratory metadata probes while never reading the authority.

## Codex launch patterns

Preferred when Codex CLI works:

```bash
PROMPT_FILE='/c/path/to/review-prompt.md'
REPO='C:/path/to/clean-review-repo'
OUTPUT='C:/path/to/evidence/codex-final.md'
PROMPT="$(<"$PROMPT_FILE")"

codex exec \
  --sandbox read-only \
  -C "$REPO" \
  --ephemeral \
  -c 'model_reasoning_effort=high' \
  --output-last-message "$OUTPUT" \
  "$PROMPT"
```

Put **every option before the final positional prompt**. Do not place `-C`, sandbox, model, or output flags after the prompt. On Windows, a multiline prompt passed before options through the npm `.cmd` shim can be truncated at a blank line while later flags are silently ignored.

Before treating the run as review evidence, verify Codex's startup banner shows the intended `workdir`, `sandbox`, model/configuration, and full task. If it starts in the user home, shows a permissive sandbox, or asks for a target already specified, classify the attempt as a launch failure and rerun correctly. Capture the final message outside the reviewed repository and read it back.

Prefer writing long review prompts and multi-file repair scripts to a temp `.py`/`.md` file. Nested bash heredocs with JSON/AST/Python quotes frequently abort with `unexpected EOF while looking for matching quote` on Windows Git-Bash; file-backed positional prompts avoid that quoting class and preserve the full prompt.

## Launch failures are not verdicts

If Codex returns account/model errors for every tried model:

1. stop thrashing model names after one or two probes;
2. treat it as a launch failure, not a review outcome;
3. retry through another **technically read-only** path: content-embedded tool-free review, an enforced read-only sandbox, or an isolated disposable copy/worktree;
4. never invent `APPROVE` from a failed launch.

Do **not** fall back to a write-capable Hermes leaf on the same working tree merely because its prompt says “read-only.” Prompt-level restraint is not isolation. If a live-file reviewer is used, freeze the exact reviewed path allowlist—including untracked files—and compare before/after hashes. Any changed hash invalidates the verdict.

```bash
git status --porcelain
git ls-files --others --exclude-standard
sha256sum <exact reviewed files...> > review-before.sha256
# run enforced read-only review
sha256sum <exact reviewed files...> > review-after.sha256
cmp -s review-before.sha256 review-after.sha256
```

If a tool-using Codex process hangs after reading files but before answering, kill only that task-scoped process, invalidate any partial output, verify reviewed-file hashes, and relaunch through an enforced read-only or content-embedded path.

Evidence review after a live attempt uses the same launch discipline: path-limit the start artifact, sanitized run JSON, final decision draft, preflight, and routing truth surfaces; forbid live rerun/auth/session/provider actions in the prompt.

## After REJECT

1. repair only listed blockers;
2. rerun offline compile/validate/self-test and scoped `git diff --check`;
3. request a fresh independent review of the final tree;
4. do not stage or commit authority until the new review returns `APPROVE`.

## After APPROVE

Commit only the exact frozen path allowlist. Concurrent dirty worktrees are never reviewed authority. Create the immutable start artifact only after the authority commit exists.
