# Agent Swarm Infrastructure Scripts

Templates for setting up agent orchestration in any project. Copy and adapt for your repo.

## Task Registry Template

```json
{
  "tasks": [],
  "settings": {
    "worktree_root": "REPLACE_WITH_PATH",
    "main_repo": "REPLACE_WITH_PATH",
    "frontend_repo": "REPLACE_WITH_PATH",
    "default_agent": "opencode",
    "max_retries": 3,
    "review_required": true,
    "reviewers": ["codex"],
    "notify_on_complete": true
  },
  "stats": {
    "total_completed": 0,
    "total_failed": 0,
    "total_retried": 0
  }
}
```

## Agent Spawn Commands (Headless)

These are the canonical commands for spawning coding agents non-interactively.
Prefer these over `delegate_task` when the user has a cost-optimized setup
(external agents use the user's existing subscriptions at $0 additional cost;
Hermes `delegate_task` subagents burn the orchestrator's model tokens).

Full worktree-isolated spawn scripts with task registry integration are available as templates:
- `templates/spawn-codex-headless.sh`
- `templates/spawn-opencode-headless.sh`

### Codex (non-interactive, bypasses trust prompt)

```bash
# Simple task
codex exec "your prompt" -C /path/to/project --ephemeral

# With full control
codex exec "your prompt" \
  --model gpt-5.3-codex \
  --dangerously-bypass-approvals-and-sandbox \
  -C /path/to/project \
  --ephemeral \
  --json
```

Key flags:
- `exec` — non-interactive mode (NO trust prompt!). Never use bare `codex` for automation.
- `--ephemeral` — don't persist session files (keeps `~/.codex/sessions/` clean)
- `--json` — structured output for parsing
- `-C, --cd <dir>` — working directory
- `--dangerously-bypass-approvals-and-sandbox` — skip confirmation prompts

### OpenCode (headless with slim plugin)

```bash
opencode run "your prompt" \
  --dir /path/to/project \
  --model opencode-go/deepseek-v4-flash \
  --variant high \
  --format json
```

Key flags:
- `run` — headless mode (no TUI). The oh-my-opencode-slim plugin loads automatically.
- `--model` — any model the OpenCode subscription supports (Go, free, or API key)
- `--variant` — reasoning effort: `minimal`, `low`, `medium`, `high`, `max`
- `--format json` — machine-readable output
- `--agent` — optionally specify which slim agent role to use

### Agent Selection by Cost Tier

When the user's setup includes multiple cost tiers, pick the cheapest viable agent:

| Priority | Tool | Cost | When to Use |
|----------|------|------|-------------|
| 1st | `opencode run` (Free models) | $0 | Mechanical work: file edits, simple fixes, bulk changes |
| 2nd | `opencode run` (Go sub) | Included | Complex work needing better reasoning |
| 3rd | `codex exec` | Own sub | Instructor/evaluator role, spec writing, quality review |
| 4th | `delegate_task` (Hermes) | $$ API tokens | Only when external agents can't handle the task |

**Hermes' role:** Write the task spec, choose the agent tier, spawn it, evaluate results.
Never touch code directly — that burns orchestrator tokens on mechanical work.
