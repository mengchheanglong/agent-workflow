# Bounded Agent Slice Recovery and Evidence Discipline

Use this when a delegated coding slice has a fixed runtime, strict TDD evidence requirements, or may leave a useful partial diff.

## Agent compatibility preflight

Before starting a timed slice with an external coding CLI:

1. Check the CLI version.
2. If the configured model rejects an old CLI, classify it as setup/launch failure, not product failure.
3. Inspect the worktree before retrying.
4. If no implementation occurred, upgrade through the tool's official package channel, verify the new version, and relaunch the unchanged handoff.

For Codex CLI:

```bash
codex --version
npm view @openai/codex version
npm install -g @openai/codex@latest
codex --version
```

Persist the fix procedure, not a negative claim that the model or tool is broken.

## Bounded monitoring

Launch with a real timeout and a final-output artifact. Monitor sparingly:

1. Allow enough time for dependency/setup work.
2. Distinguish silence from progress by checking process status/log advancement and read-only `git status --short`.
3. If logs and files stop advancing beyond the slice budget, terminate instead of consuming the parent benchmark indefinitely.

## Recover a partial diff

After timeout or termination:

1. Preserve the diff; do not blindly rerun the original broad prompt.
2. Read every allowed changed file.
3. Run the targeted test and all required project gates independently.
4. Diagnose from actual compiler/linter/test output.
5. Make only narrow repairs inside the original scope, with a small retry cap.
6. Re-run the identical gates.
7. Write an evidence artifact and commit only the verified slice.
8. If substantial work remains, issue a smaller continuation handoff against the existing diff.

## TDD evidence rule

Test-first file order is not proof that RED executed.

If the delegated process did not preserve RED console output:

- report test-first file order only if observed;
- label independent RED console evidence as **not proven**;
- never reconstruct or fabricate the missing failure;
- do not create an artificial later failure and present it as historical RED;
- record independently verified GREEN results separately.

## Runtime-pass/typecheck-fail package imports

If tests pass but TypeScript rejects a dependency import:

1. inspect the installed package's `package.json` and `.d.ts`;
2. confirm the actual runtime export shape;
3. prefer a narrow documented type bridge for a known CommonJS/ESM declaration mismatch;
4. do not weaken strict compiler/linter settings or silently change frozen package versions.

## Evidence artifact minimum

Record:

- CLI version and compatibility upgrades;
- launch/setup failures separately from implementation failures;
- timeout/termination and preserved files;
- exact targeted and full verification commands/results;
- line counts or other frozen limits;
- unproven evidence explicitly;
- limitations and next slice.
