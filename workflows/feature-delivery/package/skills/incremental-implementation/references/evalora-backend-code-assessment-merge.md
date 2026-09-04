# Evalora backend code-assessment branch merge notes

Use this when merging a backend branch that adds or changes the code-assessment/code-execution module, especially branches named like `code-assesment` / `code-assessment`.

## Safe merge sequence

1. Work from the backend repo, not frontend:
   ```bash
   cd C:/Users/User/Internship/evalora-backend
   git status --short --branch
   git fetch origin --prune
   git branch --all | grep -Ei 'code|assess|coding' || true
   ```
2. Confirm the target branch and base branch. The historical Evalora branch was misspelled `origin/code-assesment`.
3. Before merging, inspect impact and possible conflicts:
   ```bash
   BASE=$(git merge-base backend-core origin/code-assesment)
   git log --oneline backend-core..origin/code-assesment
   git diff --stat backend-core...origin/code-assesment
   git merge-tree "$BASE" backend-core origin/code-assesment | sed -n '1,220p'
   ```
4. Merge with no auto-commit, resolve conflicts, then verify:
   ```bash
   git merge --no-ff --no-commit origin/code-assesment || true
   git diff --name-only --diff-filter=U
   ```

## Known conflict resolution pattern

When the branch adds Piston-backed code execution while backend-core already has DeepSeek/auth/report work:

- `.env.example`: keep existing Neon + DeepSeek V4 settings, and add Piston/rate-limit keys. Do not remove current `DEEPSEEK_*` values. Keep sample values redacted/placeholders only.
- `src/app.module.ts`: keep backend-core providers/controllers (`AiService`, DeepSeek provider factory, auth guards, reports/templates/sessions/responses services), but import/register the new `CodeModule`. Do **not** also keep the old direct `CodeController` registration if `CodeModule` owns it.
- `docs/API-CONTRACT.md` may auto-merge; inspect code endpoint descriptions after merge.

## Prisma client pitfall

If the branch changes `prisma/schema.prisma` (for example adding `CodeSubmission.questionId`), run Prisma generate before tests/typecheck. Otherwise tests can fail with stale generated client errors such as:

```text
Object literal may only specify known properties, and 'questionId' does not exist in type 'CodeSubmissionCreateInput'
```

Fix:

```bash
pnpm prisma generate
```

Then run canonical verification:

```bash
pnpm test && pnpm typecheck && pnpm lint && pnpm build && pnpm prisma:validate
```

## Commit hygiene

- Leave unrelated untracked `.agents/` folders untouched unless the user explicitly asks.
- Run `git diff --cached --check`; Figma/exported HTML or markdown often carries trailing whitespace.
- Secret-scan staged diffs before committing. `.env.example` should contain placeholders only.
- Commit and push the merge only after the canonical verification passes.