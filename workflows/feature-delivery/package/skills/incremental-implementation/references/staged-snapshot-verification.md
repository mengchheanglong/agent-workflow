# Verifying a Scoped Commit in a Dirty Worktree

Use this when a user asks for a commit while unrelated work is already modified or untracked—especially when intended and unrelated changes overlap in the same files.

## Goal

Commit only the requested slice and prove that the staged snapshot works from clean `HEAD`, without resetting, stashing, or rewriting the user's other work.

## Procedure

1. Inspect `git status --short`, unstaged diff/stat, and staged diff/stat.
2. List intended files and trace imports/exports; a UI file may depend on unrelated uncommitted helpers.
3. Stage wholly owned files with `git add -- <paths>`.
4. For mixed files, stage an index-only version:
   - construct desired content in a temporary file from `git show HEAD:<path>` plus the requested hunk, or from the working-tree file with unrelated hunks removed;
   - update only the index:
     ```bash
     blob=$(git hash-object -w /path/to/temp-file)
     git update-index --add --cacheinfo 100644,$blob,path/in/repo
     ```
   The working tree stays untouched; `MM` is expected.
5. Validate the index:
   ```bash
   git diff --cached --check
   git diff --cached --name-only
   git diff --cached --stat
   ```
6. Prove the exact staged snapshot independently:
   ```bash
   verify_dir="$(mktemp -d)"
   patch_file="$(mktemp)"
   git diff --cached --binary > "$patch_file"
   git worktree add --detach "$verify_dir" HEAD
   git -C "$verify_dir" apply "$patch_file"
   ```
   Install with the repository's package manager, then run its canonical full gate. For pnpm, use `CI=true pnpm install --frozen-lockfile --dir "$verify_dir"`.
7. Remove the temporary worktree/patch, commit the staged index, and verify unrelated work remains unstaged.

## Pitfalls

- Never use `git add .` in a noisy worktree.
- Do not reset, checkout, or stash user work merely to obtain a clean-looking status.
- Passing tests in the dirty working tree is not proof: unstaged files may satisfy hidden dependencies.
- Every new import/export in staged files must exist in the staged snapshot.
- If a mixed hunk cannot be isolated confidently, stop rather than bundling another workstream.

## Report

Give the commit hash/message, staged file count, isolated verification result, confirmation that unrelated changes remain unstaged, and whether anything was pushed.
