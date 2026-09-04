# Evalora prebuilt assessment seed slice

Use this when the user notices that Evalora has backend template APIs/evaluation rubrics but no actual starter tests for roles like HR, Software Engineer, or Team Leader, or when they ask to expand/refactor the free/prebuilt templates.

## Product distinction

- **Module evaluation profiles** are backend fallback rubrics used by AI evaluation when a module/template omits a rubric.
- **Prebuilt assessment templates** are real selectable starter tests: template + modules + questions + weights + per-question rubrics.
- If the user says “pretests,” first clarify this distinction, then implement prebuilt templates if they want actual starter tests.

## Recommended implementation shape

1. Keep a stable public barrel for callers, e.g. `src/modules/templates/prebuilt-templates.ts`, so seed scripts/tests do not churn when internal files move.
2. For tiny starter banks, one reusable source file is acceptable; once banks grow beyond demo size, split definitions under `src/modules/templates/prebuilt/` by role and module.
3. Include stable IDs for template/module/question rows so seeding is idempotent.
4. Include at least:
   - title, description, roleType, timeLimitMin, scoringRules;
   - modules with type/title/description/weight/orderIndex/settings;
   - questions with questionText/questionType/options/rubric.
5. Add a seed script such as `scripts/seed-prebuilt-templates.ts` and package script `seed:prebuilt`.
6. Seed via Prisma `upsert` and replace nested modules/questions on update so edited seed definitions stay in sync.
7. Create a seed organization/owner only when needed; never print real credentials or tokens.

## Maintainable file layout for researched banks

When the user asks to make the free/prebuilt templates more maintainable, prefer this class-level layout:

```text
src/modules/templates/prebuilt/
  index.ts                 # exports PREBUILT_ASSESSMENT_TEMPLATES
  types.ts                 # shared definition and seed DTO types
  seed-mappers.ts          # buildPrebuiltTemplateCreateData/updateData helpers

  hr-generalist/
    index.ts               # assembles HR template metadata + modules
    behavioral.ts
    communication.ts
    work-style.ts
    problem-solving.ts
    leadership.ts
    ai-ethics.ts

  software-engineer/
    index.ts               # assembles software template metadata + modules
    ai-interview.ts
    coding.ts
    debugging.ts
    system-design.ts
    communication.ts
    work-style.ts
    behavioral.ts

  team-leader/
    index.ts               # assembles leader template metadata + modules
    leadership.ts
    communication.ts
    behavioral.ts
    problem-solving.ts
    work-style.ts
    ai-interview.ts
```

Keep `src/modules/templates/prebuilt-templates.ts` as a backward-compatible re-export from `./prebuilt` unless the whole codebase is updated in the same slice. Add a test that checks the expected role/module files exist; this catches future regressions back to a monolithic question-bank file.

## Research-backed expansion shape

When the user asks whether Evalora needs more questions or says to proceed after company-interview research, keep **one prebuilt template per role** but expand it into a larger editable question bank. Do not create many template variants unless the product explicitly needs template variants.

Recommended bank/subset targets:

- HR Generalist: 25–35 bank questions; candidate sees 10–14.
- Software Engineer: 35–50 bank questions; candidate sees 10–15 plus one practical coding/debugging task.
- Team Leader: 25–35 bank questions; candidate sees 10–14.

Encode subset guidance in `scoringRules.recommendedCandidateQuestionCount` and mark researched banks with a source/version such as `prebuilt-researched-v2` so tests and frontend logic can distinguish them from tiny demo seeds.

Big-company pattern to reflect in the banks:

- Behavioral / STAR questions for evidence of past behavior.
- Situational judgment and case questions for ambiguous real-work scenarios.
- Written communication tasks for candidate/manager/stakeholder messaging.
- Role-specific practical work: coding/debugging/system design for engineers; employee-relations/process cases for HR; prioritization/conflict/performance cases for leaders.
- AI-era judgment questions: AI use disclosure, verification, privacy, bias, security, and human ownership.
- Per-question rubrics with at least 3 criteria; prefer 4–5 criteria for scenario/coding tasks.

For Evalora's current starter roles, the proven expansion landed at:

- HR Generalist: 6 modules / 30 questions.
- Software Engineer: 7 modules / 39 questions.
- Team Leader: 6 modules / 30 questions.

## TDD/verification pattern

- Add a focused test before implementation that verifies:
  - required roles/templates exist;
  - each template has several modules;
  - each module has questions;
  - each question has useful rubrics;
  - seed helpers map API enum strings (`coding`) to Prisma enum values (`CODING`).
- For maintainability refactors, add a focused RED test that verifies the expected `src/modules/templates/prebuilt/<role>/<module>.ts` files exist before splitting the monolith.
- Run RED targeted test first.
- Run GREEN targeted test + `pnpm typecheck`.
- Run real seed against Neon only after schema validation/generation:
  ```bash
  pnpm prisma:validate
  pnpm prisma:generate
  pnpm seed:prebuilt
  ```
- Verify rows directly with Prisma by counting seeded templates/modules/questions; report counts, not connection strings.
- Final verification:
  ```bash
  pnpm test && pnpm typecheck && pnpm lint && pnpm build && pnpm prisma:validate && pnpm prisma:generate && pnpm seed:prebuilt
  ```

## Documentation updates

Update README and docs so future frontend/team members know:

- `pnpm seed:prebuilt` exists;
- prebuilt templates are editable starter tests;
- large researched banks live in `src/modules/templates/prebuilt/` with per-role/per-module files;
- these are separate from AI module-default rubrics;
- frontend may still need a duplicate/copy-from-prebuilt endpoint if it should clone rather than edit seeded templates directly.
