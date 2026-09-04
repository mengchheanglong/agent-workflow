# Agent Swarm — Headless Spawning Commands

## PREFERRED: User spawns agents directly

The user controls timing and monitors output. Hermes writes task specs only.
Never use `delegate_task` for coding — it burns DeepSeek Pro tokens.
External agents cost $0 additional.

## Codex (Instructor / Evaluator)

```bash
codex exec "full task prompt here" \
  -C /path/to/project \
  --model gpt-5.5 \
  -c "model_reasoning_effort=high" \
  --dangerously-bypass-approvals-and-sandbox \
  --ephemeral
```

Key learnings:
- `codex exec` (NOT `codex`) — non-interactive, no trust prompt
- `--ephemeral` — skip session save (keeps ~/.codex clean)
- Model: gpt-5.5 (high reasoning). gpt-5.4 for lighter tasks. gpt-5.3-codex NOT supported on ChatGPT accounts.
- PTY NOT needed for `codex exec` — works in plain terminal

## OpenCode (Bulk Coding — $0 via Go sub + Free models)

```bash
opencode run "full task prompt here" \
  --dir /path/to/project \
  --model opencode-go/deepseek-v4-pro \
  --variant high \
  --format json
```

Key learnings:
- `opencode run` (NOT `opencode`) — headless CLI, no GUI needed
- Model: `opencode-go/deepseek-v4-pro` for complex work, `opencode-go/deepseek-v4-flash` for simple
- Free models: `opencode/deepseek-v4-flash-free`, `opencode/minimax-m3-free`
- `--format json` for structured output
- Server restart NOT needed — runs standalone

## Cost Strategy

| Priority | Agent | Cost | Use Case |
|----------|-------|------|----------|
| 1st | OpenCode (Free models) | $0 | Bulk edits, fixes, simple changes |
| 2nd | OpenCode (Go sub) | Included | Complex tasks, reasoning needed |
| 3rd | Codex | Own sub | Instructor, evaluator, investigation |
| LAST | Hermes subagents | API tokens | Only when agents unavailable |

## Pitfalls

- Codex trust prompt: only appears in interactive mode (`codex`), not `codex exec`
- OpenCode slim config: remove `fallback` fields (not in schema). Schema validates at `C:\Users\User\.config\opencode\oh-my-opencode-slim.json`
- Windows paths: use forward slashes in codex -C, backslashes work but messy
- Cloudflare R2 error 9404: means source image not found at origin — use raw URLs, not `/cdn-cgi/image/`
