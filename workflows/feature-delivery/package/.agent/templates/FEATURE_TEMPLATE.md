# Active Feature

## Identity

- Name:
- Slug:
- Owner:
- Branch:
- Risk: UNASSESSED

## Change baseline

- Repository root:
- Base branch:
- Base commit:
- Pre-existing modified/untracked files:
  - None recorded.
- Allowed change paths:
  -
- Prohibited/touch-only-with-approval paths:
  -

## Authority

- Applicable project rules:
- Product/architecture/security/data sources:
- Material contradictions:
  - None known.

## Problem

What user, business, operational, or developer problem exists now? Cite evidence rather than a
solution preference.

## Goal

What observable outcome must be true when this feature is complete?

## In scope

-

## Out of scope

-

## Acceptance criteria

- [ ] AC1 — Given / when / then or equivalent observable behavior:
- [ ] AC2 — Negative, permission, or failure behavior when applicable:
- [ ] AC3 — Compatibility, documentation, or operational behavior when applicable:

## Requirements-quality checklist

The Builder must not self-approve unresolved material items.

- [ ] Each criterion describes an outcome, not an implementation.
- [ ] Scope boundaries and non-goals are explicit.
- [ ] Roles/permissions and affected data are explicit where applicable.
- [ ] Error, empty, retry, and partial-failure behavior is defined where applicable.
- [ ] Compatibility and migration expectations are explicit where applicable.
- [ ] No authoritative source contradiction remains unresolved.
- [ ] Every important open question has an owner or blocks progress.

## Planned vertical slices

Use only when the feature needs more than one implementation slice.

1. Slice:
   - Behavior proved:
   - Dependencies:
   - Expected files:
   - Test/proof:

## Constraints and invariants

-

## Non-functional requirements

- Security/authorization:
- Privacy/data handling:
- Reliability/failure behavior:
- Performance:
- Compatibility/migration:
- Accessibility/UI:
- Observability/operations:

## Validation plan

- Targeted RED/GREEN command:
- Focused tests:
- Full relevant tests:
- Type/static analysis:
- Lint:
- Build:
- Integration/migration/security checks:
- Manual acceptance:

## Review plan

- Independent reviewer identity/session:
- Review scope: base commit → current working snapshot
- Specialist lenses:
- Review artifact: `.active/REVIEW.md`
- Maximum broad fix cycles: 2
- Additional-cycle authorization/decision: None

## Human checkpoint

- Required: UNKNOWN
- Trigger/reason:
- Approval requested:

## Definition of done

- [ ] Acceptance criteria pass line by line.
- [ ] Required tests/checks pass after the last edit.
- [ ] Current snapshot is recorded.
- [ ] Independent review verdict is `APPROVE` for that snapshot.
- [ ] Human approval is recorded for that snapshot when required.
- [ ] State Markdown/JSON and documentation agree.
- [ ] No unrelated, unexplained, debug, secret, or temporary change remains.
- [ ] `python .agent/scripts/validate_workflow.py` exits 0.
- [ ] Ship evidence is recorded before status `SHIPPED`.
