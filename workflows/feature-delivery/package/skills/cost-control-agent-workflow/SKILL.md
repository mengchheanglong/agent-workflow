---
name: cost-control-agent-workflow
description: Cost-optimized Codex-orchestrated workflow with Grok 4.5 via xAI OAuth (`xai-oauth`, `grok-4.5`) as the sole implementation worker. DeepSeek API and OpenCode are prohibited. Small slices, binary checklists, one review pass.
version: 2.1.0
---

# Cost-Control Agent Workflow

Reduce review loops and token cost. Hermes owns final independent verification; Codex orchestrates/manages the work and owns review plus DevOps/test/ship control; Grok 4.5 via xAI OAuth (`xai-oauth`, `grok-4.5`) implements bounded slices. DeepSeek API and OpenCode are prohibited. If an authorized driver is unavailable, stop and report the blocker.

## First Rule: freeze the lane, then choose the route

Before coding, load both:

- `model-task-router` to freeze Codex control + exact Grok 4.5 worker identity and prohibited routes;
- `cost-aware-execution-router` to choose the cheapest safe execution shape.

Hermes must choose one route before execution starts:
- **Codex control-plane repair** — tiny orchestration/verification repair only, not routine implementation;
- **Codex spec → Grok 4.5 implementation → Codex narrow review**;
- **Split first**.

Use the reusable template from `cost-aware-execution-router/templates/decision-template.md` and emit a short routing block. Before sealing a model-specific handoff, require the exact no-tool provider/model identity smoke from `model-task-router`.

If Hermes cannot state scope, risk, review width, retry likelihood, and exact worker identity clearly, the task is not scoped enough yet and should be split smaller.

## Roles

**Codex:** Orchestrator, task manager, reviewer, and DevOps/test/ship controller. Codex decomposes work, writes bounded worker prompts, evaluates diffs, runs or directs verification, and controls commit/push readiness.

**Grok 4.5 via xAI OAuth (`xai-oauth`, `grok-4.5`):** Sole authorized implementation worker. Grok edits only the allowed files and returns required TDD/test evidence to Codex/Hermes.

**DeepSeek API:** Prohibited. Do not read, invoke, or spend its key.

**OpenCode:** Retired. Do not route new work to it.

**Hermes:** Top-level owner and independent verifier. Hermes protects Mission Control authority, checks real artifacts/tool output, and accepts or rejects Codex-managed delivery.

## Branching

One branch per major workstream. Commit after each completed slice.

## Prompt Template

Use this only after `cost-aware-execution-router` chooses the spec→cheap-implementer path.

Every prompt MUST include: task name, repo path, primary spec path, allowed files (1-3, or at most a very small bounded list), forbidden files/behavior, exact implementation requirements, required command(s), binary self-check table, and final report format.

## Review Rules

One review per slice. No issues → complete. One tiny issue → direct GPT/Codex fixes directly. Multiple issues → one narrow correction prompt.

Choose the cheapest review tier that preserves correctness:
- **Tier 1 mechanical acceptance**: allowed files + diff names/stats + required command output only
- **Tier 2 targeted semantic review**: changed files/diff + tests + risky seam check
- **Tier 3 full semantic review**: only for high-risk slices

For routine LOW/MEDIUM user-visible work, keep visual/accessibility critique **INLINE** in the same independent reviewer context and artifact. A separate specialist reviewer is reserved for HIGH risk, truly distinct expertise, or explicit human request. Default to one broad review; a narrow accepted finding or human-requested polish receives one focused **DELTA** review of changed criteria, affected files/checks, and regression seams. Requirement, scope, contract, auth/security/data/lifecycle, dependency, or broad-refactor changes require a new FULL review.

When only commit/tracking state or evidence representation changes after an approved product tree, prove product-byte equivalence, current snapshot, clean product paths, and reusable validation/browser evidence; then bind the new snapshot with a DELTA review instead of rerunning full engineering plus visual review. **Never trust the active-state claim that a change is representation-only:** inspect the actual commit/diff for every previously reviewed product seam. If product bytes changed, invalidate only the affected conclusions, capture focused exact-snapshot proof, and run one bounded DELTA re-review. Any prior human approval is stale after a rendered product change and must not be silently rebound. See `references/proportional-review-and-delta-revalidation.md`.

If the first review finds broad drift, multiple logic mistakes, or the need for repo-wide reasoning, stop the cheap loop. Switch to direct GPT or split the task smaller instead of paying for repeated retries.

If a direct Codex slice is low risk and passes all hard gates, Hermes should stop at Tier 1 instead of doing a second expensive code reading pass.

## Bounded Agent Execution and Independent Evidence

For clocked, frozen-contract, security-sensitive, or evidence-gated slices, the execution prompt must add:

- an explicit write allowlist and forbidden-file list;
- one exact RED command with the expected behavioral failure;
- no production changes before decisive RED;
- no test edits during GREEN unless a new RED cycle is authorized;
- exact GREEN, regression, static, frozen-file, and size-gate commands;
- no commit/push permission until Hermes independently verifies the result;
- a bounded agent runtime or stop condition.

Coding-agent summaries are self-reports, not proof. Hermes must inspect status/diff, reject scope drift, and rerun the exact commands before accepting or committing. If an agent stalls after writing an in-scope draft, stop at the bound, preserve the valid working tree, and continue from the last verified TDD state rather than restarting or waiting indefinitely.

For the full prompt contract, stalled-agent recovery, clock-start sequence, and compact verdict template, read `references/clocked-tdd-handoffs.md`.

## Workflow Cutover Rule

When a slice was already built under an older workflow and the user asks to start a new workflow, do **not** retroactively re-route or re-implement that completed slice. First evaluate the already-produced artifact using the cheapest safe review tier (usually mechanical gate → rubric-delta checks). If it passes, accept it and start the new execution workflow on the **next** task. Update active state so future sessions know exactly where the workflow changed.

## Rubric Delta Evaluation

For GPT-5.5/Hermes evaluation, prefer a **question-specific rubric** over broad rereading. The evaluator should not re-understand the whole task from scratch when the prompt already contains binary acceptance criteria.

Default evaluation flow:
1. **Mechanical gate first:** `git status --short`, `git diff --name-only`, `git diff --stat`, required command output. Stop early on scope drift or new failures.
2. **Criterion-specific checks:** turn every acceptance criterion into one row: `criterion → exact probe → evidence → pass/fail`.
3. **Targeted file reads only:** read the changed line ranges or functions needed to answer each row. Do not read whole files unless the criterion cannot be evaluated otherwise.
4. **Spot-check risky seams:** for high-risk code, inspect 1–3 boundary paths (caller → ledger/write/read path → trust/reliability output). Do not inspect every path unless a spot-check fails.
5. **Escalate only on failure:** broad semantic review is triggered by failed criteria, ambiguous evidence, scope drift, or safety/trust changes not covered by the rubric.

The output should be a compact verdict-first table, not a narrative code review. Evidence must be concrete: command output, `file:line`, or grep/read snippets.

## Anti-Patterns

- NEVER do broad or medium-risk implementation directly when a bounded cheaper path exists.
- Avoid direct Hermes code edits for anything beyond tiny, low-risk, tightly scoped repairs that can be verified immediately.
- NEVER cherry-pick git commits manually. Let Codex handle merge/resolution.
- NEVER debug spawn scripts by fixing them yourself when the issue is part of a larger execution slice. Write the fix prompt, let Codex apply it.
- NEVER restart servers manually after agent changes when that is part of the delegated execution path. Delegate server management too.
- NEVER use `delegate_task` as an unapproved substitute implementation worker. Grok 4.5 via xAI OAuth (`xai-oauth`, `grok-4.5`) is the only implementation worker; Codex controls the lane.
- **NEVER over-deliver beyond the explicit ask.** When the user asks for a workflow update, do ONLY that — do not run browser verifications, launch servers, start extra reviews, or capture evidence unless explicitly authorized. "Update the workflow" means update the workflow. "Report status" means report status. Doing more wastes model cost and burns the user's time. If a step is not in the user's request, skip it.
- **NEVER assume batching or grouping.** When the user asks about one feature, do not assume they want to batch multiple features together. Ask before grouping work into batches.
- **NEVER assume branch naming conventions.** Always confirm the user's preferred branch naming pattern (`feature/*` vs `feat/*` vs other) before creating branches. Do not guess or switch conventions without explicit confirmation.

See `references/scope-discipline-and-stopping.md` for the full scope discipline rule and recovery pattern.
See `references/prd-compliance-refinement.md` for the PRD gap-analysis and refinement pattern.
See `references/type-migration-pattern.md` for the type-field removal pattern.

## When Codex May Repair Directly

Codex normally controls rather than implements. A direct Codex edit is allowed only for a tiny surgical control-plane repair where another Grok loop would cost more than the change and the repair stays inside the already-approved files. Examples: correcting a handoff label, fixing a verification wrapper, or repairing a schema typo before seal.

Architecture, auth/security, trust boundaries, cross-module contracts, and lifecycle semantics remain Codex judgment/review work, but bounded production implementation goes to Grok 4.5. If the work cannot be split safely for Grok, stop and rescope rather than silently turning Codex into the routine worker.

Hermes may make only narrow verification-side repairs that immediately unblock the frozen acceptance criteria and are independently rerun.

## Pitfalls

- **Broad specs → repeated review loops.** A spec like "implement cache everywhere" will fail. Split into slices: "Cache helper hardening" → "Cache news module" → "Cache research module."
- **Do not improvise another worker.** Grok 4.5 via xAI OAuth (`xai-oauth`, `grok-4.5`) is the implementation worker. DeepSeek API is prohibited and OpenCode is retired. If Grok is unavailable, stop and report the blocker.
- **Do not seal stale authority.** Background agents may rewrite revision or model labels after review. Reread and stale-scan every authority/control file immediately before independent review and again before commit/seal; any changed live file invalidates the prior approval.
- **Do not confuse build-time and runtime providers.** Grok may build a provider-free experiment. Prove worker identity and runtime provider absence separately.

## Commit Style

`type(scope): short description` — types: feat, fix, refactor, perf, test, docs, chore.
