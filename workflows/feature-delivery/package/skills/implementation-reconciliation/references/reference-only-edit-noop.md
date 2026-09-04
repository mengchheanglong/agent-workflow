# Reference-Only and Mechanism-Only Edit No-Op Handling

## The Bug

A common bug in edit-submission logic is rejecting valid edits as "no-ops" when only one dimension (work fields, mechanisms, or references) changes while others remain the same.

## The Three Dimensions

For an existing-work edit with work-field changes, mechanism changes, and references:

| Scenario | No-op? |
|---|---|
| title changes, refs `[A] → [A]` | **NOT no-op** — title changed |
| mechanisms change, refs `[A] → [A]` | **NOT no-op** — mechanisms changed |
| title changes, mechanisms change | **NOT no-op** |
| refs `[A] → [B]`, everything else same | **NOT no-op** — references changed |
| refs `[A] → [A]`, everything else same | **NO-OP** — reject |

## The Fix

```typescript
// WRONG — rejects reference-only edits
if (Object.keys(changedFields).length === 0) {
  throw new CanonInputError("No changes proposed.");
}

// WRONG — still rejects mechanism-only with unchanged refs
if (Object.keys(changedFields).length === 0 && !referencesChanged) {
  throw new CanonInputError("No changes proposed.");
}

// CORRECT — only reject when ALL dimensions are unchanged
if (Object.keys(changedFields).length === 0 &&
    !referencesChanged &&
    (payload.mechanisms === undefined || payload.mechanisms.length === 0)) {
  throw new CanonInputError("No changes proposed.");
}
```

## Test Cases

Add these to ensure the fix is correct:

1. **Reference-only**: `refs [A] → [B]`, no other changes → accepted
2. **Mechanism-only**: mechanism add/remove/update, refs `[A] → [A]` → accepted
3. **Content + unchanged refs**: title change, refs `[A] → [A]` → accepted
4. **Total no-op**: refs `[A] → [A]`, no field changes, no mechanism changes → rejected
