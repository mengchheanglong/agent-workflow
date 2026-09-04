---
name: writing-plans
description: "Write implementation plans: bite-sized tasks, paths, code."
version: 1.1.0
author: Hermes Agent (adapted from obra/superpowers)
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [planning, design, implementation, workflow, documentation]
    related_skills: [subagent-driven-development, test-driven-development, requesting-code-review]
---

# Writing Implementation Plans

## Overview

Write comprehensive implementation plans assuming the implementer has zero context for the codebase and questionable taste. Document everything they need: which files to touch, complete code, testing commands, docs to check, how to verify. Give them bite-sized tasks. DRY. YAGNI. TDD. Frequent commits.

Assume the implementer is a skilled developer but knows almost nothing about the toolset or problem domain. Assume they don't know good test design very well.

**Core principle:** A good plan makes implementation obvious. If someone has to guess, the plan is incomplete.

## When to Use

**Always use before:**
- Implementing multi-step features
- Breaking down complex requirements
- Delegating to subagents via subagent-driven-development

**Don't skip when:**
- Feature seems simple (assumptions cause bugs)
- You plan to implement it yourself (future you needs guidance)
- Working alone (documentation matters)

## Bite-Sized Task Granularity

**Each task = 2-5 minutes of focused work.**

Every step is one action:
- "Write the failing test" — step
- "Run it to make sure it fails" — step
- "Implement the minimal code to make the test pass" — step
- "Run the tests and make sure they pass" — step
- "Commit" — step

**Too big:**
```markdown
### Task 1: Build authentication system
[50 lines of code across 5 files]
```

**Right size:**
```markdown
### Task 1: Create User model with email field
[10 lines, 1 file]

### Task 2: Add password hash field to User
[8 lines, 1 file]

### Task 3: Create password hashing utility
[15 lines, 1 file]
```

## Plan Document Structure

### Header (Required)

Every plan MUST start with:

```markdown
# [Feature Name] Implementation Plan

> **For Hermes:** Use subagent-driven-development skill to implement this plan task-by-task.

**Goal:** [One sentence describing what this builds]

**Architecture:** [2-3 sentences about approach]

**Tech Stack:** [Key technologies/libraries]

---
```

### Task Structure

Each task follows this format:

````markdown
### Task N: [Descriptive Name]

**Objective:** What this task accomplishes (one sentence)

**Files:**
- Create: `exact/path/to/new_file.py`
- Modify: `exact/path/to/existing.py:45-67` (line numbers if known)
- Test: `tests/path/to/test_file.py`

**Step 1: Write failing test**

```python
def test_specific_behavior():
    result = function(input)
    assert result == expected
```

**Step 2: Run test to verify failure**

Run: `pytest tests/path/test.py::test_specific_behavior -v`
Expected: FAIL — "function not defined"

**Step 3: Write minimal implementation**

```python
def function(input):
    return expected
```

**Step 4: Run test to verify pass**

Run: `pytest tests/path/test.py::test_specific_behavior -v`
Expected: PASS

**Step 5: Commit**

```bash
git add tests/path/test.py src/path/file.py
git commit -m "feat: add specific feature"
```
````

## Bounded Comparative Benchmarks

When planning a time/line-bounded incumbent or framework comparison, split **preflight** from **implementation**:

1. freeze the unchanged behavioral contract and source hierarchy;
2. compare one candidate at a time from official current documentation;
3. pin an explicitly compatible package/server pairing, registry integrities, and platform-specific image digest;
4. define the exact first action that starts the clock;
5. commit/push the preflight before dependency, image, configuration, source, or executable-test work;
6. classify pass, setup/harness inconclusive, repeated intrinsic failure, and bound expiry before execution;
7. synchronize active state only after the implementation-repository preflight has an immutable commit;
8. if that external state is declared authoritative and still marks the phase locked, commit its approval **before** recording the start clock or creating executable files—never defer reconciliation to the final report.

Do not treat workflow/invocation IDs as semantic request equality or arbitrary external side effects as intrinsically exactly once. Preserve an application/domain receipt at the authoritative transaction boundary.

If a frozen crash vector combines a post-restart prior-state assertion with eventual durable recovery, use a deterministic test-only recovery barrier to observe safety before releasing liveness; do not rewrite the expected outcome.

See `references/bounded-incumbent-benchmark.md` for the complete preflight, crash-harness, reproducibility, authority-sync, evidence-claim layering, exact-clock, aggregate/metrics verification, and dated runtime-semantic amendment checklists.

See `references/evidence-gated-red-checkpoints.md` for the reusable governance order, committable-RED gate, exact negative-vector assertions, and bounded GREEN handoff.

### RED checkpoint quality

Before committing a RED test slice, verify it is red for the intended missing behavior **and independently clean** under lint/format/static checks. A missing implementation is not permission for the test file itself to contain lint, type, fixture, or setup failures.

For negative/security contracts, freeze assertions that close common loopholes:

- exact data-free error surface rather than permissive partial-object matching;
- equality acceptance plus one-step-over rejection for inclusive boundaries;
- every listed local-rejection category through the adapter when the submitter must remain untouched;
- mixed unsupported-version + malformed input to prove version precedence;
- independent recomputation of hardcoded canonical identities;
- exact collected test count and strict changed-file allowlist.

Obtain test-quality review before the RED commit; only then hand production files to the GREEN implementer with tests immutable.

## Evidence-Boundary Discipline for Bounded Agent Experiments

When planning a deterministic actor, agent, authorization, privacy, or recovery experiment, freeze **what each layer can actually prove** before writing tests:

1. **Representation/schema validation** proves only that an input has declared fields and rejects undeclared fields. It does not prove the caller lacked prohibited knowledge.
2. **Observation provenance** requires an identified trusted producer or fixture. A test-only authoritative join can prove provenance for a synthetic benchmark, but must not be described as a production observation service.
3. **Local consistency checks** between caller-supplied fields are fail-fast ergonomics, not authorization.
4. **Authoritative authorization** must remain at the real policy/transaction boundary. Add adapter-path integration vectors for revoked, wrong-actor, wrong-scope, and stale-version inputs, with exact rejection codes, receipt/audit behavior, and no accepted state change.
5. **Process-loss reproduction** is not autonomous recovery. If a parent re-supplies identical input to a fresh child, claim deterministic recomputation only—not observation reacquisition, prior-submission detection, pending-work recovery, or mid-commit recovery.

For time-bounded work, define one authoritative UTC timestamp inside the committed start artifact. The deadline is exactly timestamp plus bound; writing, committing, and pushing the artifact count after that timestamp. Never leave commit time, first edit, and artifact timestamp as competing start events.

Freeze verification mechanics before implementation:

- exact aggregate command and exact expected collected test count;
- exact counted source paths and reproducible line-count command;
- scripts included in both TypeScript project coverage and typed ESLint file matching;
- metrics subprocess timeout/cleanup;
- raw/min/median/max schema for singleton and repeated measurements;
- precise metric interval labels (for example, cancellation request-to-confirmation must exclude a later observation window);
- explicit failed/skipped-check inventory and unproven-boundary section in the final artifact.

If the bound becomes tight, mandatory vectors, regression evidence, cleanup, and independent review take priority over measurements or report polish. Stop incomplete rather than weaken evidence, compress review, or obscure code to meet a line cap.

### Progressive authority for uncertain experiments

When the eventual experiment has several vectors but later commands, fixtures, or oracles are not yet known, do **not** pretend the whole matrix is frozen. Authorize the smallest executable learning slice and treat later vectors as a non-executable roadmap.

For each bounded slice:

1. Freeze one question, one exact invocation, one changed-file/evidence allowlist, one cleanup oracle, and slice-specific outcomes.
2. State which broader conclusions are unavailable from this slice. A source/unit baseline does not equal a black-box reproduction, and an environment/setup outcome does not equal a behavioral failure.
3. Start the immutable clock before collecting authoritative baseline facts. Pre-clock observations used for drafting are provisional and must be recollected under the clock.
4. Decide the prerequisite policy before execution. If the frozen runner cannot import or launch required tooling, classify setup/environment inconclusive unless a dated amendment explicitly authorizes repair; do not silently switch interpreters, install dependencies, or broaden the command.
5. Separate command execution from evidence formatting. A post-processing/formatter defect must not overwrite or misclassify the already-captured command result.
6. If the source checkout is pre-existing dirty, freeze a status count/digest and verify target-file cleanliness instead of persisting a huge unrelated path list. Recompute the same digest after execution.
7. Require independent read-only review before committing the outcome. Reviewer approval applies to the exact current artifact/diff; substantive repairs require a fresh review.
8. Reconcile every canonical state surface back to hold after the outcome. Update non-versioned workspace routers too, or explicitly report them as the only remaining stale pointers.
9. No outcome automatically opens the next vector, implementation phase, persistence layer, or product claim. Each requires a separate reviewed decision.

See `references/progressive-bounded-experiment-authority.md` for the reusable preflight, clock, classification, review, and reconciliation checklist.

## Writing Process

### Step 1: Understand Requirements

Read and understand:
- Feature requirements
- Design documents or user description
- Acceptance criteria
- Constraints

### Step 2: Explore the Codebase

Use Hermes tools to understand the project:

```python
# Understand project structure
search_files("*.py", target="files", path="src/")

# Look at similar features
search_files("similar_pattern", path="src/", file_glob="*.py")

# Check existing tests
search_files("*.py", target="files", path="tests/")

# Read key files
read_file("src/app.py")
```

If the user gives an existing project path after you drafted a greenfield plan, stop and re-anchor the plan to that implementation. Inspect its README/package/config, git top-level, status/diff, and verification scripts before writing new tasks. Do not create a duplicate repo just because the first plan assumed one.

### Step 3: Design Approach

Decide:
- Architecture pattern
- File organization
- Dependencies needed
- Testing strategy

### Step 4: Write Tasks

Create tasks in order:
1. Setup/infrastructure
2. Core functionality (TDD for each)
3. Edge cases
4. Integration
5. Cleanup/documentation

### Step 5: Add Complete Details

For each task, include:
- **Exact file paths** (not "the config file" but `src/config/settings.py`)
- **Complete code examples** (not "add validation" but the actual code)
- **Exact commands** with expected output
- **Verification steps** that prove the task works

### Step 6: Review the Plan

Check:
- [ ] Tasks are sequential and logical
- [ ] Each task is bite-sized (2-5 min)
- [ ] File paths are exact
- [ ] Code examples are complete (copy-pasteable)
- [ ] Commands are exact with expected output
- [ ] No missing context
- [ ] DRY, YAGNI, TDD principles applied

### Step 7: Save the Plan

For durable implementation plans that should travel with the codebase:

```bash
mkdir -p docs/plans
# Save plan to docs/plans/YYYY-MM-DD-feature-name.md
git add docs/plans/
git commit -m "docs: add implementation plan for [feature]"
```

For local working strategy/planning notes that should **not** become product source, create a dedicated ignored folder instead:

```bash
mkdir -p project-plan
# Save plan to project-plan/PLAN.md
printf '\n# Local project planning notes\nproject-plan/\n' >> .gitignore
git check-ignore -v project-plan/PLAN.md
```

Commit `.gitignore` if requested, but do not stage the ignored `project-plan/` contents. This is useful for phone/PWA/deployment roadmaps, private operating plans, or exploratory AI-system notes where the user wants a folder on disk but not in Git.

When the user says to clean the local planning folder, preserve only the durable roadmap (`PLAN.md`) plus the active handoff/spec being worked on. Remove stale Codex `*-final.md`, `*-last-message.txt`, and superseded one-off specs before creating the next spec. Keep the folder legible and small; `project-plan/` should be a working command center, not an archive of every agent run.

## Principles

### DRY (Don't Repeat Yourself)

**Bad:** Copy-paste validation in 3 places
**Good:** Extract validation function, use everywhere

### YAGNI (You Aren't Gonna Need It)

**Bad:** Add "flexibility" for future requirements
**Good:** Implement only what's needed now

```python
# Bad — YAGNI violation
class User:
    def __init__(self, name, email):
        self.name = name
        self.email = email
        self.preferences = {}  # Not needed yet!
        self.metadata = {}     # Not needed yet!

# Good — YAGNI
class User:
    def __init__(self, name, email):
        self.name = name
        self.email = email
```

### TDD (Test-Driven Development)

Every task that produces code should include the full TDD cycle:
1. Write failing test
2. Run to verify failure
3. Write minimal code
4. Run to verify pass

See `test-driven-development` skill for details.

### Frequent Commits

Commit after every task:
```bash
git add [files]
git commit -m "type: description"
```

## Common Mistakes

### Vague Tasks

**Bad:** "Add authentication"
**Good:** "Create User model with email and password_hash fields"

### Incomplete Code

**Bad:** "Step 1: Add validation function"
**Good:** "Step 1: Add validation function" followed by the complete function code

### Missing Verification

**Bad:** "Step 3: Test it works"
**Good:** "Step 3: Run `pytest tests/test_auth.py -v`, expected: 3 passed"

### Missing File Paths

**Bad:** "Create the model file"
**Good:** "Create: `src/models/user.py`"

## Execution Handoff

After saving the plan, offer the execution approach:

**"Plan complete and saved. Ready to execute using subagent-driven-development — I'll dispatch a fresh subagent per task with two-stage review (spec compliance then code quality). Shall I proceed?"**

### Plan-to-finish mode

If the user explicitly says **"Plan first then Proceed"**, **"plan the entire things to a finish"**, **"make sure after this it is finished and we can start testing"**, or later says **"continue"** after that instruction, do not stop at the handoff question. Write/save the complete finish-to-testing plan, then immediately execute it in bounded slices until the artifact is genuinely ready for testing.

For this mode, the plan must include a final verification pack, not just implementation tasks:

- exact commands for tests/typecheck/build;
- expected success and expected-failure smoke cases;
- paths where smoke outputs/logs will be saved;
- a final readiness report path;
- explicit non-goals/scope boundaries to prevent platform creep;
- remaining future work after testing begins.

During execution, keep each slice small and independently verified. If a delegated coding agent times out or returns partial work, inspect the diff, run the stated verification commands yourself, and make only narrow repairs that directly unblock the plan’s acceptance criteria.

When a slice is safety/privacy/prompt-context related, plan a small post-review hardening step before the next feature if reviewers produce cheap non-blocking regression suggestions. Capture it as a separate scoped `v0.1` handoff with its own tests and commit rather than silently folding it into a larger next mission.

When executing, use the `subagent-driven-development` skill or the relevant coding-agent skill:
- Fresh `delegate_task` or bounded coding-agent handoff per task with full context
- Spec compliance review after each task
- Code quality review after spec passes
- Proceed only when both reviews approve

## Remember

```
Bite-sized tasks (2-5 min each)
Exact file paths
Complete code (copy-pasteable)
Exact commands with expected output
Verification steps
DRY, YAGNI, TDD
Frequent commits
```

**A good plan makes implementation obvious.**
