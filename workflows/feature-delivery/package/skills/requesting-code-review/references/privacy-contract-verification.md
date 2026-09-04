# Privacy contract verification pattern

Session lesson: a context/export endpoint can avoid selecting raw private columns and still leak sensitive data if allowed user-controlled text fields contain embedded secrets.

Use this when reviewing or implementing privacy-preserving summaries, exports, context packs, memory snapshots, analytics summaries, or agent handoff payloads.

## Risk pattern

Allowed fields such as these can contain sensitive strings:

- display names
- profile bios / locations
- journal tags or moods
- quest names / completed quest themes
- chat signal labels
- synthesized memory summaries / traits / interventions

Selecting only “safe” columns is not enough. The content inside those fields may include emails, API keys, reset tokens, JWTs, bearer tokens, passwords, or pasted raw secrets.

## Required verification

Add regression fixtures that embed unique sensitive strings inside otherwise allowed fields:

```text
leak@example.com
sk-test_1234567890abcdef1234567890abcdef
Bearer abcdef1234567890abcdef
reset-token=abcdef1234567890abcdef1234567890
password=abcdef1234567890
```

Assert the serialized output does **not** contain the original values and does contain redaction markers, e.g.:

```ts
expect(serialized).not.toContain(email);
expect(serialized).not.toContain(apiKey);
expect(serialized).not.toContain(resetToken);
expect(serialized).toContain('[redacted-email]');
expect(serialized).toContain('[redacted-secret]');
```

Also verify raw private records do not appear:

```ts
expect(serialized).not.toContain(rawJournalContent);
expect(serialized).not.toContain(rawChatMessage);
```

## Endpoint cache control

For authenticated sensitive JSON responses, assert:

```ts
expect(res.headers.get('Cache-Control')).toBe('no-store');
```

Runtime smoke should check response headers case-insensitively if using Python/HTTP libraries.

## Review checklist addendum

- Does sanitization redact before truncation?
- Are arrays sanitized item-by-item after aggregation/deduping?
- Are docs/specs honest that output is redacted summary data, not raw export?
- Does the implementation avoid querying raw chat/journal content unless absolutely necessary?
- If helper services are reused, are they read-only and do they avoid selecting secrets? If not, document a follow-up cleanup.
