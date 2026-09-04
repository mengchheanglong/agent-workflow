#!/usr/bin/env bash
# Template: Spawn Codex headless for coding tasks
# Copy to project/.hermes/ and customize for your repo

set -euo pipefail

TASK_ID="${1:?Usage: spawn-codex.sh <task-id> <prompt-file> [model] [reasoning]}"
PROMPT_FILE="${2:?}"
PROMPT_FILE=$(realpath "$PROMPT_FILE")
MODEL="${3:-gpt-5.5}"
REASONING="${4:-high}"
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
codex exec "$PROMPT" \
  --model "$MODEL" \
  -c "model_reasoning_effort=$REASONING" \
  --dangerously-bypass-approvals-and-sandbox \
  -C "$WORKTREE_DIR" \
  --ephemeral \
  > "$WORKTREE_DIR/.codex/output.txt" 2>&1

echo "Done. Output: $WORKTREE_DIR/.codex/output.txt"
