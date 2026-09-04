# PRD Compliance Refinement Pattern

When an existing feature needs to be verified against a PRD and gaps filled.

## When to use

- Feature already exists but PRD requirements may not be fully met
- User says "work on X tab" where X already has a page
- Gap analysis reveals missing requirements

## Pattern

1. **Read PRD requirements first** — extract the specific requirement IDs (e.g., R3.1-R3.14)
2. **Read existing implementation** — map current code to each requirement
3. **Gap analysis** — produce a table: requirement | status (PASS/FAIL/GAP) | evidence
4. **Plan slices** — one slice per gap, not per requirement that already passes
5. **Implement only gaps** — do not touch passing code
6. **Verify** — typecheck, lint, build, independent review

## Key principle

**Do not redesign what already works.** The existing implementation is the baseline. Only change what fails PRD compliance. This minimizes regression surface and review cost.

## Example from Angkoro Admin

Users tab (R3.1-R3.14): 13/14 requirements already met. Only R3.14 (subscription/billing status separation) needed a new panel. Two minor UX refinements (status counts, status filter) were additive.

Stores tab (R3.7-R3.11): All requirements met. UX/UI consistency refinements applied to match Users/Support quality (cleaner hierarchy, refined filters, consistent ConfirmAction copy).

## Type Migration Pattern

When renaming or removing a type field (e.g., removing `kinds` array, changing `UserAccessKind` values from uppercase to lowercase):

1. Update the type definition
2. Update ALL seed data using the type
3. Update ALL references across the codebase (use `grep -rn` to find every usage)
4. Update derived/comparison logic (e.g., `combinedUserStatus`, `getUserAccesses`)
5. Update UI display (e.g., `capitalize()` helper for display while storing lowercase)
6. Add backwards-compatible tone mapping if needed (e.g., `StatusBadge` needs both `Active` and `active` during migration)

## Pitfalls

- Do not merge distinct access types into one concept (e.g., Merchant vs Store owner are different — one is user-level, one is store-specific)
- Do not make store ownership bannable through generic user-status controls
- Always check all references when renaming types (CommandPalette, mock-store, etc.)
- When changing case (upper↔lower), check: type definitions, seed data, comparison logic, audit messages, filter values, tone mapping
