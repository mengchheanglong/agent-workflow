# Free Model Rotation

Free models in OpenCode rotate out frequently. Always check before starting work.

## Check Procedure

```bash
# 1. List available free models
opencode models 2>&1 | grep -i free

# 2. Compare against current config
grep -E "free|mimo|nemotron|minimax" ~/.config/opencode/oh-my-opencode-slim.json

# 3. If a model in config is NOT in the available list → replace immediately
```

## Known Rotations

| Date | Removed | Replaced With | Reason |
|------|---------|---------------|--------|
| 2026-06-08 | `minimax-m3-free` | `nemotron-3-ultra-free` | Time-limited free period expired |
| 2026-06-08 | `deepseek-v4-flash-free` (Explorer/Fixer) | `opencode-go/deepseek-v4-flash` | Free models throttled, causing orchestrator hangs |

## Pitfalls

- **Free models throttle hard** — Explorer/Fixer on free models can hang the orchestrator. Test with a quick `opencode run "hi"` before assigning them to roles.
- **Time-limited models vanish** — minimax-m3-free worked one day, gone the next. Don't rely on free models for critical roles.
- **Go sub models are stable** — prefer Go sub for Explorer/Fixer if free models are unreliable.

## Current Free Model Quality (as of 2026-06-08)

| Model | Quality | Best For |
|-------|---------|----------|
| `nemotron-3-ultra-free` | Strong (55B MoE, NVIDIA) | Librarian, Observer |
| `deepseek-v4-flash-free` | Unreliable (throttled) | Avoid for now |
| `mimo-v2.5-free` | Weak | Last resort |
