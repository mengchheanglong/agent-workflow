# Evidence-Gated RED Checkpoints

Use this checklist for bounded security, durability, authorization, privacy, or deterministic-agent experiments.

## Governance sequence

Before executable work:

1. Commit and push the reviewed plan/preflight in the implementation repository.
2. Reconcile every declared external authority (Mission Control, roadmap, task registry) in its own commit, referencing the exact planning commit.
3. Verify locks for later phases remain explicit.
4. Record one immutable UTC start timestamp only after both commits exist.
5. Commit/push the start artifact before creating executable files.

Do not defer authority synchronization to the final report when the external authority still says the phase is locked.

## RED quality gate

A RED checkpoint is committable only when all apply:

- failure is caused by the missing behavior, not syntax, import setup, lint, type, fixture, or environment failure;
- the focused runner collects the exact intended test count;
- the RED test itself passes its applicable lint/format/static checks;
- strict changed-file allowlist and whitespace checks pass;
- hardcoded canonical hashes/digests are independently recomputed from literal fixtures;
- independent review checks test loopholes before the RED commit.

## Negative-vector assertions

Avoid permissive assertions that allow hidden sensitive state.

- For fixed data-free errors, assert the exact own-property/symbol surface, exact name/message/code, and absence of details, cause, payload, input, or metadata.
- For exclusive boundaries such as `<=`, test equality acceptance and one-step-over rejection.
- If every local rejection must bypass a downstream submitter, exercise every rejection category through the adapter and assert total downstream calls remain zero.
- If version errors must precede generic schema errors, combine an unsupported version with another malformed field and assert the version-specific code.
- Distinguish schema rejection, caller-declared consistency, synthetic fixture provenance, and authoritative policy enforcement; test each at its actual layer.

## GREEN handoff

Freeze exact write paths, production line-count paths/command, forbidden imports/APIs, and required static gates. The implementer may fix implementation—not tests—when hardcoded identities differ. Review and commit GREEN separately before integration expansion.

### Schema-to-downstream compatibility

When an adapter transforms a strict representation into an existing downstream request type, the upstream schema must be at least as strict for every copied field. Do not type the emitted request with an assertion and assume compatibility: compare the actual downstream parser constraints. Add RED probes for malformed, missing, and canonical-format edge cases (for example alphabetic, negative, and leading-zero decimal versions), then verify every locally rejected variant produces zero downstream calls.

Within a frozen test-count contract, extend existing test tables/subcases rather than adding nominal tests. This preserves the agreed aggregate count without sacrificing edge coverage. Also pair the successful adapter path with exact call arguments, optional workflow/routing identity, exact consequence shape, and returned-result reference identity.

### Lint-clean RED imports

A deliberately missing dynamic module may be typed as `any` by tooling, causing an otherwise intentional RED test to fail lint independently. Keep the RED focused without disabling rules:

```ts
const loaded: unknown = await import("../future/module.js");
return loaded as ExpectedSurface;
```

Assign to `unknown` first, then perform one necessary narrowing assertion. Avoid a double `as unknown as ...` on the import expression (often flagged as unnecessary), and avoid returning the raw dynamic import (unsafe return/member access). Run the focused test-file lint separately before committing RED.
