---
name: subagent-driven-development
description: "Execute plans via delegate_task subagents (2-stage review)."
version: 1.1.0
author: Hermes Agent (adapted from obra/superpowers)
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [delegation, subagent, implementation, workflow, parallel]
    related_skills: [writing-plans, requesting-code-review, test-driven-development]
---

# Subagent-Driven Development

> **Prefer the `autonomous-ai-agents` skill over this skill for implementation tasks.** External coding agents (Codex, OpenCode, Claude Code) run on their own subscriptions at $0 additional token cost. `delegate_task` subagents burn DeepSeek Pro tokens. Use this skill only when external agents aren't configured, or when the task genuinely needs orchestration-level reasoning that a coding agent can't provide.

## Overview

Execute implementation plans by dispatching agents with systematic two-stage review.

**Core principle:** Fresh agent per task + two-stage review (spec then quality) = high quality, fast iteration.

**CRITICAL — Orchestrator, not implementer:** Your role is to write task specs, propose agent commands, and evaluate results. The user spawns agents themselves — this is more effective because they control timing and monitor output. NEVER open files, run patches, edit code, or use `write_file`/`search_files` to fix things yourself. Doing so burns your own model tokens at API rates when external agents (Codex, OpenCode) run on the user's existing subscriptions at $0 additional cost.

### Agent Selection by Cost Tier

Pick the cheapest viable agent for the task:

| Priority | Tool | Cost | When to Use |
|----------|------|------|-------------|
| 1st | `opencode run` (Free models) | $0 | Mechanical work: file edits, simple fixes, bulk changes |
| 2nd | `opencode run` (Go sub) | Included | Complex work needing better reasoning |
| 3rd | `codex exec` | Own sub | Instructor/evaluator role, spec writing, quality review |
| 4th | `delegate_task` | $$ API tokens | Only when external agents can't handle the task |

See `references/agent-swarm-infrastructure.md` for exact headless commands.

For orchestrating external coding agents (Codex, OpenCode, Claude Code) with worktree isolation, tmux sessions, and cron monitoring, see the agent-swarm-infrastructure reference.

## When to Use

Use this skill when:
- You have an implementation plan (from writing-plans skill or user requirements)
- Tasks are mostly independent
- Quality and spec compliance are important
- You want automated review between tasks

**Prefer external coding agents (Codex, OpenCode) over `delegate_task` for implementation work.** Hermes subagents burn the same DeepSeek Pro tokens as the main conversation. External agents (Codex via own subscription, OpenCode via Go+Free models) cost $0 additional. Only use `delegate_task` when the task genuinely needs orchestrator-level reasoning, or when the external agents are unavailable/blocked.

See `autonomous-ai-agents` skill for headless spawn commands and agent orchestration patterns.

**vs. manual execution:**
- Fresh context per task (no confusion from accumulated state)
- Automated review process catches issues early
- Consistent quality checks across all tasks
- Subagents can ask questions before starting work

## The Process

### 1. Read and Parse Plan

Read the plan file. Extract ALL tasks with their full text and context upfront. Create a todo list:

```python
# Read the plan
read_file("docs/plans/feature-plan.md")

# Create todo list with all tasks
todo([
    {"id": "task-1", "content": "Create User model with email field", "status": "pending"},
    {"id": "task-2", "content": "Add password hashing utility", "status": "pending"},
    {"id": "task-3", "content": "Create login endpoint", "status": "pending"},
])
```

**Key:** Read the plan ONCE. Extract everything. Don't make subagents read the plan file — provide the full task text directly in context.

### 2. Per-Task Workflow

For EACH task in the plan:

#### Step 1: Dispatch Implementer Subagent

Use `delegate_task` with complete context:

```python
delegate_task(
    goal="Implement Task 1: Create User model with email and password_hash fields",
    context="""
    TASK FROM PLAN:
    - Create: src/models/user.py
    - Add User class with email (str) and password_hash (str) fields
    - Use bcrypt for password hashing
    - Include __repr__ for debugging

    FOLLOW TDD:
    1. Write failing test in tests/models/test_user.py
    2. Run: pytest tests/models/test_user.py -v (verify FAIL)
    3. Write minimal implementation
    4. Run: pytest tests/models/test_user.py -v (verify PASS)
    5. Run: pytest tests/ -q (verify no regressions)
    6. Commit: git add -A && git commit -m "feat: add User model with password hashing"

    PROJECT CONTEXT:
    - Python 3.11, Flask app in src/app.py
    - Existing models in src/models/
    - Tests use pytest, run from project root
    - bcrypt already in requirements.txt
    """,
    toolsets=['terminal', 'file']
)
```

#### Step 2: Dispatch Spec Compliance Reviewer

After the implementer completes, verify against the original spec:

```python
delegate_task(
    goal="Review if implementation matches the spec from the plan",
    context="""
    ORIGINAL TASK SPEC:
    - Create src/models/user.py with User class
    - Fields: email (str), password_hash (str)
    - Use bcrypt for password hashing
    - Include __repr__

    CHECK:
    - [ ] All requirements from spec implemented?
    - [ ] File paths match spec?
    - [ ] Function signatures match spec?
    - [ ] Behavior matches expected?
    - [ ] Nothing extra added (no scope creep)?

    OUTPUT: PASS or list of specific spec gaps to fix.
    """,
    toolsets=['file']
)
```

**If spec issues found:** Fix gaps, then re-run spec review. Continue only when spec-compliant.

#### Step 3: Dispatch Code Quality Reviewer

After spec compliance passes:

```python
delegate_task(
    goal="Review code quality for Task 1 implementation",
    context="""
    FILES TO REVIEW:
    - src/models/user.py
    - tests/models/test_user.py

    CHECK:
    - [ ] Follows project conventions and style?
    - [ ] Proper error handling?
    - [ ] Clear variable/function names?
    - [ ] Adequate test coverage?
    - [ ] No obvious bugs or missed edge cases?
    - [ ] No security issues?

    OUTPUT FORMAT:
    - Critical Issues: [must fix before proceeding]
    - Important Issues: [should fix]
    - Minor Issues: [optional]
    - Verdict: APPROVED or REQUEST_CHANGES
    """,
    toolsets=['file']
)
```

**If quality issues found:** Fix issues, re-review. Continue only when approved.

#### Step 4: Mark Complete

```python
todo([{"id": "task-1", "content": "Create User model with email field", "status": "completed"}], merge=True)
```

### 3. Final Review

After ALL tasks are complete, dispatch a final integration reviewer:

```python
delegate_task(
    goal="Review the entire implementation for consistency and integration issues",
    context="""
    All tasks from the plan are complete. Review the full implementation:
    - Do all components work together?
    - Any inconsistencies between tasks?
    - All tests passing?
    - Ready for merge?
    """,
    toolsets=['terminal', 'file']
)
```

### 4. Verify and Commit

```bash
# Run full test suite
pytest tests/ -q

# Review all changes
git diff --stat

# Final commit if needed
git add -A && git commit -m "feat: complete [feature name] implementation"
```

## Task Granularity

**Each task = 2-5 minutes of focused work.**

**Too big:**
- "Implement user authentication system"

**Right size:**
- "Create User model with email and password fields"
- "Add password hashing function"
- "Create login endpoint"
- "Add JWT token generation"
- "Create registration endpoint"

## Red Flags — Never Do These

- Start implementation without a plan
- Skip reviews (spec compliance OR code quality)
- Proceed with unfixed critical/important issues
- Dispatch multiple implementation subagents for tasks that touch the same files
- Make subagent read the plan file (provide full text in context instead)
- Skip scene-setting context (subagent needs to understand where the task fits)
- Ignore subagent questions (answer before letting them proceed)
- Accept "close enough" on spec compliance
- Skip review loops (reviewer found issues → implementer fixes → review again)
- Let implementer self-review replace actual review (both are needed)
- **Start code quality review before spec compliance is PASS** (wrong order)
- Move to next task while either review has open issues
- **CRITICAL: Do implementation work yourself** — your role is orchestrator, not coder. Write the task spec, spawn the agent, monitor progress, evaluate results. Never open files, run patches, or edit code directly. If you catch yourself reaching for `patch`, `write_file`, or `search_files` to fix something, stop — write a prompt and delegate it. The user's feedback of "your job is not to work on it" means you violated this rule.

- **CRITICAL: Do not loop fixes** — if OpenCode fails a task, do NOT send "fix all issues" and then review again, and again. One fix pass max. If the second attempt fails, the spec was too broad or the task was too complex — let Codex implement directly or split into smaller tasks. Broad specs + multiple review loops cost MORE than using a stronger model from the start.

- **Discuss git before acting** — propose branch names and commit messages to the user before touching git. Format: `type(scope): description`. Allowed types: feat, fix, refactor, perf, test, docs, chore. Branches: main=prod, feature/*, fix/*, hotfix/*. Never commit or branch without user approval.

- **Check free models before coding sessions** — free models (minimax-m3-free, etc.) rotate out frequently. Before starting implementation work, run `opencode models | grep -i free` and update the OpenCode slim preset if any free models are no longer available. See `references/free-model-rotation.md`.

## Handling Issues

### If Subagent Asks Questions

- Answer clearly and completely
- Provide additional context if needed
- Don't rush them into implementation

### If Reviewer Finds Issues

- Implementer subagent (or a new one) fixes them
- Reviewer reviews again
- Repeat until approved
- Don't skip the re-review

### If Subagent Fails a Task

- Dispatch a new fix subagent with specific instructions about what went wrong
- Don't try to fix manually in the controller session (context pollution)

## Efficiency Notes

**Why fresh subagent per task:**
- Prevents context pollution from accumulated state
- Each subagent gets clean, focused context
- No confusion from prior tasks' code or reasoning

**Why two-stage review:**
- Spec review catches under/over-building early
- Quality review ensures the implementation is well-built
- Catches issues before they compound across tasks

**Cost trade-off:**
- More subagent invocations (implementer + 2 reviewers per task)
- But catches issues early (cheaper than debugging compounded problems later)

## Optimized Workflow: Tiny Specs + Binary Checklists

**When cost matters (always):** Broad specs with multiple review loops burn more tokens than just using a stronger model directly. Use this instead:

### Task Routing by Risk

| Risk Level | Who | Task Size |
|------------|-----|-----------|
| **High** (shared infra, auth, security) | Codex directly | 1-3 files |
| **Low** (per-module repetition) | OpenCode/DeepSeek | 1-3 files |

### Prompt Format for Low-Risk Tasks

```
Do only this: <exact scope>.

Files allowed:
- file A
- file B

Required exact changes:
- change 1
- change 2

Self-check before final:
| Check | Pass/Fail | Evidence |
|---|---|---|

Final output must include:
1. Changed snippets
2. pnpm build result
3. Self-check table

Do not modify unrelated files.
```

### Review: One Pass Max

After OpenCode completes:
1. Codex reviews once — PASS or FAIL
2. If FAIL: Codex gives one specific correction prompt OR applies fix directly if <10 lines
3. Do NOT loop "fix → review → fix again"

**Why:** 5-6 review loops on a broad spec costs MORE than just having Codex do the task directly. Small prompts with binary acceptance checks get it right the first time, or fail fast with a clear fix.

### With writing-plans

This skill EXECUTES plans created by the writing-plans skill:
1. User requirements → writing-plans → implementation plan
2. Implementation plan → subagent-driven-development → working code

### With test-driven-development

Implementer subagents should follow TDD:
1. Write failing test first
2. Implement minimal code
3. Verify test passes
4. Commit

Include TDD instructions in every implementer context.

### With requesting-code-review

The two-stage review process IS the code review. For final integration review, use the requesting-code-review skill's review dimensions.

### With systematic-debugging

If a subagent encounters bugs during implementation:
1. Follow systematic-debugging process
2. Find root cause before fixing
3. Write regression test
4. Resume implementation

## Example Workflow

```
[Read plan: docs/plans/auth-feature.md]
[Create todo list with 5 tasks]

--- Task 1: Create User model ---
[Dispatch implementer subagent]
  Implementer: "Should email be unique?"
  You: "Yes, email must be unique"
  Implementer: Implemented, 3/3 tests passing, committed.

[Dispatch spec reviewer]
  Spec reviewer: ✅ PASS — all requirements met

[Dispatch quality reviewer]
  Quality reviewer: ✅ APPROVED — clean code, good tests

[Mark Task 1 complete]

--- Task 2: Password hashing ---
[Dispatch implementer subagent]
  Implementer: No questions, implemented, 5/5 tests passing.

[Dispatch spec reviewer]
  Spec reviewer: ❌ Missing: password strength validation (spec says "min 8 chars")

[Implementer fixes]
  Implementer: Added validation, 7/7 tests passing.

[Dispatch spec reviewer again]
  Spec reviewer: ✅ PASS

[Dispatch quality reviewer]
  Quality reviewer: Important: Magic number 8, extract to constant
  Implementer: Extracted MIN_PASSWORD_LENGTH constant
  Quality reviewer: ✅ APPROVED

[Mark Task 2 complete]

... (continue for all tasks)

[After all tasks: dispatch final integration reviewer]
[Run full test suite: all passing]
[Done!]
```

## Remember

```
Fresh subagent per task
Two-stage review every time
Spec compliance FIRST
Code quality SECOND
Never skip reviews
Catch issues early
You are the ORCHESTRATOR — not the implementer
Write specs, spawn agents, evaluate results — never touch code
```

**Quality is not an accident. It's the result of systematic process.**

## Further reading (load when relevant)

When the orchestration involves significant context usage, long review loops, or complex validation checkpoints, load these references for the specific discipline:

- **`references/context-budget-discipline.md`** — Four-tier context degradation model (PEAK / GOOD / DEGRADING / POOR), read-depth rules that scale with context window size, and early warning signs of silent degradation. Load when a run will clearly consume significant context (multi-phase plans, many subagents, large artifacts).
- **`references/gates-taxonomy.md`** — The four canonical gate types (Pre-flight, Revision, Escalation, Abort) with behavior, recovery, and examples. Load when designing or reviewing any workflow that has validation checkpoints — use the vocabulary explicitly so each gate has defined entry, failure behavior, and resumption rules.

Both references adapted from gsd-build/get-shit-done (MIT © 2025 Lex Christopherson).

For orchestrating external coding agents (Codex, OpenCode, Claude Code) with worktree isolation, task registries, and cron monitoring, load these references:

- **`references/agent-swarm-spawning.md`** — **PREFERRED.** Exact headless CLI commands, cost strategy, Windows pitfalls. Use this instead of `delegate_task` for all coding work.
- **`references/agent-swarm-infrastructure.md`** — Task registry JSON schema, cron setup, monitoring script patterns.

For reusable starter scripts, copy from these templates:
- **`templates/spawn-codex-headless.sh`** — Copy to `.hermes/` and customize for your repo.
- **`templates/spawn-opencode-headless.sh`** — Copy to `.hermes/` and customize for your repo.

For the optimized prompt format proven to reduce review loops:
- **`references/optimized-prompt-template.md`** — Binary checklist + scope-locked prompt template. Use for all OpenCode tasks.
