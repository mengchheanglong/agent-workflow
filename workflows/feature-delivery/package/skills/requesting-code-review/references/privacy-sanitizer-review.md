# Privacy Sanitizer Review Patterns

Use this when reviewing features that export, summarize, or package user context (profile packs, memory packs, AI-agent context, analytics summaries, exports, integrations).

## Core lesson

Field allowlists are not enough. A feature can exclude raw `email`, `password`, `token`, raw journal content, and raw chat messages but still leak secrets when user-controlled allowed fields contain sensitive substrings.

Examples of allowed fields that still need content-level redaction:

- display name
- profile bio/location/timezone-like strings
- quest goals and completed goal themes
- journal tags and mood labels
- chat signal labels/types
- memory summaries, struggles, interventions, traits
- URLs embedded in any allowed text

## Required adversarial probes

Add or manually run tests for sensitive values embedded inside otherwise allowed text fields:

```text
leak@example.com
password=abc123xyz789
passwd: abc123xyz789
secret=abc123xyz789
apiKey: abc123xyz789
api_key=abc123xyz789
token=abc123xyz789
?token=abc123xyz789&next=ok
?token=abc123xyz789;next=ok
#token=abc123xyz789
jwt=abc123xyz789
access_token=abc123xyz789
refresh_token=abc123xyz789
reset_token=abc123xyz789
session_token=abc123xyz789
id_token=abc123xyz789
Bearer abc123xyz789abc123
sk-test_1234567890abcdef1234567890abcdef
eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIxMjM0NTY3ODkwIn0.abcdef1234567890abcdef1234567890
```

## Good test shape

Prefer a dedicated sanitizer test plus one end-to-end propagation test.

1. `sanitize.test.ts` or equivalent:
   - proves individual redaction patterns work
   - proves plain aliases are covered, not just compound names (`token`, `jwt`, `session_token`/`session-token`, `id_token`/`id-token`)
   - proves URL query secrets redact only the secret value and preserve safe params, e.g. `?token=[redacted-secret]&next=ok`
   - proves delimiter behavior for `&`, `;`, and `#` so the sanitizer neither leaks secrets nor consumes safe neighboring text
   - proves array sanitizers call the same redaction path
2. Context/export builder test:
   - puts the same secret into profile bio, goal, journal tag/mood, chat signal type, and memory fields
   - serializes the output and asserts the raw secret is absent
   - asserts redaction markers are present
3. Runtime smoke, when cheap:
   - create temporary account/data
   - call the real authenticated endpoint
   - assert raw token/email/content absent and redaction marker present
   - delete temporary account/data

## Review checklist

- Verify both projection-level exclusion and content-level redaction.
- Search implementation for raw-model queries such as `ChatMessage`, `ChatConversation`, raw journal `title`/`content`, or broad `.select()` calls.
- Check response headers for authenticated context/export endpoints: `Cache-Control: no-store`.
- Treat docs claiming “tokens/passwords/emails excluded” as requiring tests for embedded values, not just omitted database fields.
- If a sanitizer uses regexes, test both assignment syntax (`token=...`, `apiKey: ...`) and URL query syntax (`?token=...&next=ok`).
