# Required-Field Persistence Pattern

When a spec requires a field (like `references` for existing-work edits), the requirement must be enforced at THREE layers simultaneously. Fixing only one or two layers leaves the violation intact.

## The Three Layers

### 1. Type Layer

```typescript
// WRONG — optional field
type UpdatePayload = {
  references?: CanonReference[];
};

// CORRECT — required field
type UpdatePayload = {
  references: CanonReference[];
};
```

### 2. Parser Layer

```typescript
// WRONG — conditional parsing allows undefined
if (raw.references !== undefined) {
  references = validateReferences(raw.references);
}

// CORRECT — required validation
if (!raw.references || !Array.isArray(raw.references)) {
  throw new InputError("References are required for existing-work edits.");
}
const references = validateReferences(raw.references);
```

### 3. Service Layer

```typescript
// WRONG — conditional persistence omits revision snapshot
if (referencesChanged && payload.references) {
  revisionChangedFields.references = { prev, next };
}

// CORRECT — unconditional persistence
revisionChangedFields.references = {
  prev: currentReferences,
  next: payload.references,
};
```

## Why All Three Matter

| If you fix only... | The bug that remains |
|---|---|
| Type | Parser still returns `undefined`, service crashes or skips |
| Parser | Type still allows `undefined`, service conditionally omits |
| Service | Type/parser allow missing data, validation bypassed |

## Detection Pattern

Search for these patterns to find violations:

```bash
# Optional field in type
grep -n "references?:" src/modules/*/index.ts

# Conditional parsing
grep -n "if.*references.*!==.*undefined" src/modules/*/index.ts

# Conditional persistence
grep -n "if.*referencesChanged" src/lib/*.ts

# Conditional revision snapshot
grep -n "if.*references.*!==.*undefined" src/lib/*.ts
```

## CANON-IMPL-003 Example

The spec required: "A complete normalized replacement reference set for EVERY existing direct Canon edit."

The violation was:
1. Type: `references?: CanonReference[]` (optional)
2. Parser: `if (raw.references !== undefined)` (conditional)
3. Service: `if (referencesChanged && payload.references)` (conditional)

All three were fixed:
1. Type: `references: CanonReference[]` (required)
2. Parser: `if (!raw.references || !Array.isArray(raw.references))` (required)
3. Service: `revisionChangedFields.references = { prev, next }` (unconditional)

## Test Coverage

Add tests for each layer:

1. **Missing field**: Omit `references` entirely → expect validation error
2. **Empty array**: `references: []` → expect validation error
3. **Undefined**: `references: undefined` → expect validation error
4. **Unchanged with content edit**: `[A] → [A]` alongside title change → revision contains references
5. **Mechanism-only with unchanged refs**: Mechanism changes, refs `[A] → [A]` → revision contains references
6. **Reference-only**: `[A] → [B]` → revision contains references
7. **Every edit has references**: Assert across all edits in a suite
