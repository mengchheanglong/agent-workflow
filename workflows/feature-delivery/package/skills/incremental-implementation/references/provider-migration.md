# Provider/API migration checklist

Use this when replacing one LLM/API provider with another across an existing app.

## Workflow

1. Inventory provider references before editing:
   - env vars (`GEMINI_API_KEY`, `OPENAI_API_KEY`, etc.)
   - endpoint URLs and SDK imports
   - response shape interfaces
   - fallback model lists
   - UI/docs strings such as “Powered by …”
2. Add one shared provider client instead of rewriting raw `fetch` calls everywhere. For OpenAI-compatible providers, centralize:
   - base URL default
   - model default
   - auth header
   - request/response shape
   - JSON fence stripping if callers expect JSON
   - fallback model resolution
3. Convert call sites by adapting payload shape, not prompt semantics. Keep existing prompt text and fallback behavior unless the task asks for behavior changes.
4. Update runtime env files and examples together:
   - preserve unrelated secrets/config
   - remove obsolete provider keys from the project env
   - never print secret values in logs or final reports
5. Update docs and visible UI branding strings so source search has zero stale provider references outside ignored/generated dirs.
6. Verify in layers:
   - provider API smoke call using the project env, printing only status/model/non-secret response
   - typecheck
   - test suite
   - production build
   - source scan for old provider strings

## DeepSeek/OpenAI-compatible quirks

- DeepSeek chat uses `/chat/completions` with `Authorization: Bearer <key>`.
- `deepseek-v4-flash` may spend completion budget on `reasoning_content`; very low `max_tokens` can return empty visible `message.content` with `finish_reason='length'`. For smoke tests and app calls, use a safer floor such as `max_tokens >= 1024` unless the endpoint/model is known not to reason internally.
- Treat both `finish_reason='MAX_TOKENS'` and OpenAI-style `finish_reason='length'` as truncated/incomplete.

## Build cache pitfall

If a Next.js production build compiles and generates pages but fails during “Collecting build traces” with a missing `.next/...*.nft.json`, clean `.next` and rebuild before diagnosing source changes:

```bash
npm run clean:next && npm run build
```

Record the clean-rebuild result, not the transient stale-cache failure, as the verification outcome.
