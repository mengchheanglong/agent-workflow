# Shared Resources

Extract patterns here only when two or more workflows genuinely reuse them.

Do not pre-emptively abstract from a single workflow. Move something into `shared/` only when a
second workflow demonstrates the same need.

## Structure

```text
shared/
├── schemas/     — shared JSON schemas
├── templates/   — shared markdown templates
└── scripts/     — shared utility scripts
```
