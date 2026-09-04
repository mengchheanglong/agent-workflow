---
name: spec-driven-development
description: "Write a specification before any code — PRD with objectives, commands, structure, code style, testing, and boundaries. Four gated phases: SPECIFY → PLAN → TASKS → IMPLEMENT."
version: 1.0.0
author: Adapted from addyosmani/agent-skills (53K stars)
metadata:
  hermes:
    tags: [spec, planning, prd, design, requirements]
---

# Spec-Driven Development

Write a specification before any code. The spec is the shared source of truth between AI and human — defining what's being built, why, and when it's done.

## When to Use

- New project or feature start
- Ambiguous, incomplete, or vague requirements
- Changes touching multiple files or modules
- Tasks estimated to take > 30 minutes

**When NOT:** Single-line fixes, typos, unambiguous self-contained changes.

## The Gated Workflow

Four phases — do not advance until current phase is validated:

```
SPECIFY → PLAN → TASKS → IMPLEMENT
   ↓        ↓       ↓         ↓
  Human    Human   Human     Human
 reviews  reviews reviews   reviews
```

### Phase 1: SPECIFY — Surface Assumptions First

Before writing the spec, list assumptions and ask for correction:

```
ASSUMPTIONS I'M MAKING:
1. This targets the CLI, not the web UI
2. Python 3.11+ only
3. Uses the existing Hermes config system
→ Correct me now or I'll proceed with these.
```

Then write the spec with six sections:

1. **Objective** — What, why, for whom, success
2. **Commands** — Full executable commands with flags
3. **Project Structure** — Source, tests, docs
4. **Code Style** — One real snippet > paragraphs of description
5. **Testing Strategy** — Framework, location, coverage
6. **Boundaries** — Always do / Ask first / Never do

Reframe vague requirements into measurable success criteria:

```
REQUIREMENT: "Make it faster"
→ SUCCESS: API response < 200ms p95, cold start < 2s
```

### Phase 2: PLAN

Generate a technical plan: components, dependencies, ordering, risks, parallel vs sequential work, verification checkpoints.

### Phase 3: TASKS

Break into discrete tasks, each:
- Completable in one focused session
- Has explicit acceptance criteria
- Includes verification step
- Touches ≤5 files

### Phase 4: IMPLEMENT

Execute tasks one at a time. Use companion skills:
- `incremental-implementation` — thin vertical slices
- `test-driven-development` — test-first
- `context-engineering` — load only relevant context

## Evidence-Gated Experiments

When a spec governs a bounded experiment, promotion gate, immutable clock, or worker handoff, use [`references/evidence-gated-experiment-authority.md`](references/evidence-gated-experiment-authority.md). It adds byte-exact test vectors, typed evidence schemas, exact provider/model routing, owner/file allowlists, cleanup/privacy predicates, source-commit identity, canonical state reconciliation, and revision-stable independent review.

Treat any modification after review dispatch as a new revision requiring re-review. User authorization begins the authority process; it does not silently seal the spec or mutate canonical project state.

## Keeping the Spec Alive

- Update when decisions or scope change
- Commit the spec alongside code
- Reference in PRs — link to the section each PR implements

## Hermes Integration

Use `write_file` to create the spec at `.hermes/specs/<name>.md`. Use `clarify` for Phase 1 assumption validation when interactive. The spec feeds into Hermes's `plan` and `writing-plans` skills for Phases 2-3.
