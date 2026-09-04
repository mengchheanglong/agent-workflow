# Optimized Agent Prompt Template

Use this format for tasks delegated to OpenCode/DeepSeek. Proven to reduce review loops from 5-6 to 1.

## Template

```
Do only this: <exact 1-sentence scope>.

Files allowed:
- <file 1>
- <file 2>
- <file 3>

Required exact changes:
- <change 1 with exact behavior>
- <change 2 with exact behavior>
- <change 3 with exact behavior>

Self-check before final:
| Check | Pass/Fail | Evidence |
| --- | --- | --- |
| <binary check 1> | | |
| <binary check 2> | | |
| <binary check 3> | | |

Final output must include:
1. Changed snippets (exact lines)
2. pnpm build result
3. Self-check table filled in

Do not modify unrelated files. Do not write narrative reports.
```

## Example: Rate Limit Fix

```
Do only this: fix rate-limit.service.ts logging and route key patterns.

Files allowed:
- src/infra/redis/rate-limit.service.ts

Required exact changes:
- Change ipAndRouteKey and userAndRouteKey to use req.route.path (route pattern), not req.path (concrete URL)
- Log every rate-limit block: key, IP/user, method, route, maxRequests, windowSeconds, retryAfter

Self-check before final:
| Check | Pass/Fail | Evidence |
| --- | --- | --- |
| 429 response logs the block? | | |
| /news/123 and /news/456 share same rate bucket? | | |
| Existing auth limiters unchanged? | | |

Final output must include:
1. Changed snippets
2. pnpm build result
3. Self-check table
```

## Why This Works

- **Binary checks** — the agent can't hand-wave. It either passes or it doesn't.
- **Scope locked** — "files allowed" prevents scope creep across the codebase.
- **Snippet output** — Codex can evaluate without re-reading all files.
- **One review pass** — if it fails, the fix is specific enough to apply directly.
