---
name: skill-router
description: Route ambiguous feature-delivery requests to the best skill. Scoped to 28 skills in this workflow.
version: 1.0.0
author: Feature Delivery Workflow
license: MIT
---

# Skill Router

## Purpose

Route ambiguous feature-delivery requests to the best skill from the 28 skills in this workflow.

## Trigger phrases

Load this skill when the user says any variant of:
- "give me your suggestion"
- "suggest" / "recommend"
- "what should I use?"
- "choose the best skill"
- "route this"
- "what now?"
- "use the right skill"
- "which skill for this?"

Also load it when the user gives a broad goal and does not name a specific skill.

## Core rule

Do **not** answer from memory if a relevant skill exists.

Procedure:

1. Parse the request into domain, artifact, verb, phase, constraints, and requested output.
2. If the user explicitly names a skill, verify that skill's scope.
3. Check the fast-route table below for a clear artifact-and-phase match.
4. When the route is broad or ambiguous, consult the feature skills catalog in `references/feature-skills-catalog.md`.
5. Load the plausible candidates and compare triggers, exclusions, deliverables.
6. Select one primary owner and at most two non-overlapping support skills.
7. If one route is obvious, act directly. If there is a real trade-off, give a short default recommendation and explain the alternative.

## Fast-route table

| User intent | First skill(s) to load | Default action |
|---|---|---|
| Build with tests / TDD | `test-driven-development` | RED → GREEN → REFACTOR |
| Review this PR / code review | `github-code-review` or `requesting-code-review` | Inspect diff, verify findings |
| Open a PR / git workflow | `github-pr-workflow` | Branch, commit, open, CI, merge |
| Debug this bug / root cause | `systematic-debugging` | Diagnose before patching |
| Write a spec / specification first | `spec-driven-development` | Create actionable spec |
| Build in slices / thin vertical slices | `incremental-implementation` | Implement → test → verify → commit |
| Review this decision / challenge this | `doubt-driven-development` | Adversarial fresh-context review |
| Simplify this code / cleanup | `simplify-code` | Parallel cleanup |
| Manage context / curate context | `context-engineering` | Structure context to prevent hallucination |
| Cheapest path / cost aware | `cost-aware-execution-router` | Choose cheapest effective route |
| Execute via subagents | `subagent-driven-development` | 2-stage review subagents |
| Write a plan | `writing-plans` | Bite-sized tasks, paths, code |
| Reconcile with spec | `implementation-reconciliation` | Verify code against architecture |
| QA this web app / find bugs | `dogfood` or `code-traced-qa` | Exploratory QA |
| Debug form flow | `web-form-flow-debugging` | Debug and verify web form flows |
| Test routes | `web-app-route-testing` | Batch HTTP route testing |
| Admin QA / stateful QA | `stateful-web-admin-qa` | Stateful web/admin QA |
| Authenticated smoke test | `authenticated-web-smoke` | Authenticated browser smoke tests |
| Extract tasks from doc | `document-to-action-items` | Extract obligations, deadlines, tasks |
| Stakeholder requirements | `stakeholder-product-requirements` | Stakeholder PRDs |
| Second brain / project memory | `project-second-brain` | File-first AI second brains |

## Skill composition rules

Choose:
1. one **primary skill** that owns the requested artifact and phase;
2. optionally one **specialist** for a distinct concern;
3. optionally one **verification skill** when the primary does not cover it.

Do not load several overlapping primary workflows.

## Supporting files

- `references/feature-skills-catalog.md` — scoped catalog of the 28 feature-delivery skills
