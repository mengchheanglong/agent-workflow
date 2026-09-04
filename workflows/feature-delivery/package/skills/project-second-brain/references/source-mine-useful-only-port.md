# Source-mine useful-only port pattern

Use when an old repo has one or two genuinely useful artifacts but most of the project should not be revived.

## Trigger

The user says variants of:

- "take what only useful for us"
- "is this actually useful?"
- "don't revive the whole thing"
- "salvage only the useful part"

## Pattern

1. **Name the actual useful home first.** Do not leave reusable artifacts stranded in the old repo if the user has a current system where they belong.
2. **Port only the artifact that matches the current workflow.** For this user, prefer small Hermes/Codex/project-state utilities over old dashboards, backend runtimes, DB schemas, or broad orchestration surfaces.
3. **Preserve the old repo as source/reference, not product.** If the artifact is ported into the current system, remove duplicate untracked copies from the old repo so it stays clean.
4. **Write a stop rule into the salvage notes.** Future agents should not continue extracting lower-value pieces just because the salvage map lists them.
5. **Verify in the destination system.** Run its native tests/typecheck and at least one real smoke/dry-run against the old repo plus the destination repo.
6. **Update the old repo’s local `.active/` notes.** Record what was taken, where it now lives, what was intentionally not taken, and the next action.

## What to avoid

- Do not continue extraction because a previous plan had Tasks 2/3 if the user narrows scope to "only useful for us".
- Do not keep two copies of the same utility unless the old repo itself is the product.
- Do not promote old UI/backend/orchestration code into current systems without a live demand signal.
- Do not archive/move the old repo until useful ports are verified and the user explicitly approves archival.

## Useful final report shape

```text
Kept:
- <artifact> -> <destination path/command>

Did not take:
- <explicitly rejected surfaces>

Verified:
- <destination test/typecheck/smoke commands>

Old repo:
- clean/dirty status
- local salvage notes updated
```
