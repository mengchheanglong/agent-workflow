# Finalizing a Fragmented Vision into One Canonical Goal

Use when a user says their goals have become fragmented, promotes a definitive vision/roadmap, and asks to finalize or update the current goal.

The output must **replace fragmented command state**, not add another competing roadmap.

## Target outcome

```text
one canonical GOAL.md
+ one active mission
+ old missions explicitly completed/parked/componentized
+ all routers and machine state agree
+ one bounded next action
```

## Workflow

### 1. Inspect the promoted source first

If the user provides a file/path/attachment, read that original source before relying on session history or old summaries.

Extract five decisions:

1. ultimate purpose;
2. scientifically honest boundary;
3. single present mission;
4. North Star/evaluation criterion;
5. immediate build order and explicit non-goals.

Do not promote every phase into a simultaneous project.

### 2. Inspect existing command state

Read:

```text
AGENTS.md
README.md
.active/CURRENT.md
.active/NEXT.md
.active/STATE.json
.active/DECISIONS.md
.active/VISION-SPLIT-MAP.md
mission-control/README.md
mission-control/missions/README.md
```

Identify:

- the stale active mission;
- stale next actions;
- old candidate branches that should become components;
- historical work that should remain as evidence but stop routing agents.

### 3. Write one canonical `GOAL.md`

Keep it human-readable and decisive. Include:

- one-sentence long-term vision;
- scientific/ethical uncertainty boundary;
- one active mission;
- North Star;
- foundational architecture rule;
- founder/operator role if relevant;
- anti-fragmentation operating policy;
- component consolidation map;
- first proof and build order;
- milestone gates;
- explicit non-goals;
- honest public positioning.

Use language such as `canonical until explicitly revised`, not claims of permanent immutability.

### 4. Consolidate old branches instead of deleting history

For each prior direction, assign one role:

- completed/parked proof;
- future component;
- evaluation environment;
- adapter;
- commercial/career bridge;
- long-horizon gated research;
- reference only.

Patch the previous active mission's status and next action so it cannot continue driving work.

Do not delete useful historical reviews or evidence.

### 5. Replace every active router

Update the same decision in:

```text
AGENTS.md
README.md
.active/CURRENT.md
.active/NEXT.md
.active/STATE.json
.active/DECISIONS.md
.active/RESEARCH.md
.active/VISION-SPLIT-MAP.md
mission-control/README.md
mission-control/missions/README.md
```

`STATE.json` should contain only current machine state plus compact component status. Move stale commit inventories and detailed history into historical mission reviews.

When future agents ask “what next?”, router order should be:

```text
GOAL.md
→ .active/CURRENT.md
→ .active/NEXT.md
→ .active/STATE.json
→ active mission package
```

### 6. Create exactly one active mission package

Recommended files:

```text
MISSION.md
SPEC.md
TASKS.md
EVIDENCE-GATES.md
BUILDER-HANDOFF.md
REVIEW.md
artifacts/README.md
```

The first package should define:

- artifact;
- bounded implementation slice;
- acceptance/evidence gates;
- non-goals;
- stop/review boundary;
- honest current evidence level.

If implementation has not started, say so explicitly. Do not let a complete specification imply working software exists.

### 7. Preserve the promoted source honestly

Prefer copying the original source into `references/` when still accessible.

If an attachment reader exposed the document but the underlying file later disappears, create a **promoted-source note** containing:

- original title/date;
- provenance;
- decisive strategy and architecture;
- explicit statement that it is a distilled record, not a byte-for-byte archive.

Never leave a broken source pointer or falsely claim an exact copy.

### 8. Update durable user/profile context compactly

Replace the stale mission entry rather than adding another. Store only:

- finalized North Star;
- single active mission;
- core architecture rule;
- status of the previously active product;
- major later-stage gates.

Implementation status and commit IDs remain in project/session state, not memory.

### 9. Run ad-hoc routing verification

When no canonical docs test exists, create a temporary script under the OS temp directory using a `hermes-verify-` prefix.

Verify:

- `STATE.json` parses;
- required files exist;
- exactly one active mission is named;
- every router points to that mission;
- stale next-action phrases are absent;
- previous active mission is completed/parked;
- required invariant/gate count is correct where applicable;
- evidence level does not overclaim implementation;
- promoted-source provenance is honest.

Use **semantic/behavior-level assertions**, not brittle exact prose. Examples:

```text
Good: canonical rule contains both "kernel owns reality" and model proposal boundary.
Bad: require one exact sentence or punctuation form.
```

If a verifier fails only because its expected wording was too specific, treat it as verifier failure, clean it up, correct the assertion, and rerun. Do not edit correct project prose merely to satisfy a brittle checker.

Always delete the temp script in `finally` and report the result as ad-hoc/static verification.

## Pitfalls

- Adding `FINAL-ROADMAP-v2.md` while leaving the old active mission unchanged.
- Making every roadmap phase an active project.
- Updating Markdown but leaving `STATE.json` stale.
- Parking a mission in an index while its own `MISSION.md` still says `active`.
- Preserving old “next action” text that resurrects completed work.
- Calling an app or UI proof the whole long-term mission.
- Claiming software exists because a detailed spec exists.
- Using machine-specific absolute paths in shareable routing docs.
- Exact-string verifier assertions for prose.

## Closeout format

```text
Final vision
Single active mission
What old branches became
Current evidence level
Only next action
Verification result
```
