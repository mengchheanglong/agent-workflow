#!/usr/bin/env bash
# Template: Spawn OpenCode headless for bulk coding
# Copy to project/.hermes/ and customize for your repo

set -euo pipefail

TASK_ID="${1:?Usage: spawn-opencode.sh <task-id> <prompt-file> [model] [variant]}"
PROMPT_FILE="${2:?}"
PROMPT_FILE=$(realpath "$PROMPT_FILE")
MODEL="${3:-opencode-go/deepseek-v4-pro}"
VARIANT="${4:-high}"
REPO="${5:-$(pwd)}"

WORKTREE_ROOT="${REPO}-worktrees"
WORKTREE_DIR="$WORKTREE_ROOT/$TASK_ID"
BRANCH="feat/$TASK_ID"

# Create worktree
mkdir -p "$WORKTREE_ROOT"
cd "$REPO"
git worktree add "$WORKTREE_DIR" -b "$BRANCH" 2>/dev/null || echo "Reusing worktree"
cd "$WORKTREE_DIR"
pnpm install --frozen-lockfile 2>&1 | tail -1

# Run headless
PROMPT=$(cat "$PROMPT_FILE")
opencode run "$PROMPT" \
  --dir "$WORKTREE_DIR" \
  --model "$MODEL" \
  --variant "$VARIANT" \
  --format json \
  > "$WORKTREE_DIR/.opencode/output.jsonl" 2>&1

echo "Done. Output: $WORKTREE_DIR/.opencode/output.jsonl"
