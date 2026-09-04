# Source-Mine Salvage Workflow

Use when an old project may contain reusable patterns, but should not necessarily be revived as an active product.

## Trigger

- User asks whether an old project is useful.
- Repo is historically important but likely superseded by newer workflows.
- The useful output is extraction guidance, not immediate product continuation.

## Workflow

1. Inspect and verify the repo before judging it:
   - read README/docs/package scripts/key modules;
   - check git status/branch/remotes;
   - run the smallest trustworthy verification commands (tests/typecheck/build if available);
   - identify generated/runtime state separately from source.
2. Classify contents into:
   - **extract first**: small reusable tools, prompts, harnesses, workflows;
   - **reference only**: architecture/schema/UI/failure taxonomy worth consulting but not copying;
   - **archive after extraction**: generated state, historical reports, obsolete integrations.
3. Write a local `.active/` salvage package in the repo:
   - `.active/<PROJECT>_SALVAGE_MAP.md` with verdict, evidence, file map, extraction tasks, Codex prompts, archive plan;
   - `.active/SESSION-START.md` with resume reading order, completed extractions, next action, verification baseline.
4. Keep `.active/` local unless the user wants it committed:
   - add `.active/` to `.git/info/exclude` rather than editing project `.gitignore` for private Hermes notes.
5. Execute extractions in bounded slices:
   - write a strict handoff for Codex/OpenCode under `.active/`;
   - limit allowed files;
   - require tests and exact verification commands;
   - independently verify the agent output with real commands;
   - dry-run or smoke-test against a second representative repo when the extraction is intended to be reusable.
6. Update the salvage map/session-start after each completed extraction so future sessions do not repeat finished work.
7. Only archive/move the repo after useful extractions are verified and the user explicitly approves the move.

## Good extraction targets

- Framework-free CLIs distilled from app services.
- Verification/smoke harness templates.
- Agent workflow doctrine and paste-ready prompts.
- Admission/evaluation rubrics.
- Failure taxonomies and guardrail vocabulary.

## Avoid

- Reviving a superseded app as a competing source of truth.
- Copying old path assumptions, auth/token behavior, or branding into modern tools.
- Treating generated folders, local DBs, and historical reports as current truth.
- Archiving before extraction outputs are verified.
