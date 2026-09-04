# Evalora dashboard task reporting pattern

Use this when translating Evalora backend engineering slices into the team dashboard.

## Dashboard model

The Evalora team dashboard expects one top-level task to represent roughly a week of work. Daily work is reported as progress updates under that same task, not as a new task per commit or per TDD slice.

Do not create dashboard rows like:

- Authentication
- Templates API
- Sessions API
- Responses API
- Reports API
- DeepSeek adapter

Those are engineering slices/subtasks. Present them as daily reports/checklist items under a broader weekly task.

## Recommended Member 1 umbrella task

Use this wording unless the user changes it:

```text
Backend Development: Core APIs, Database, Authentication, AI Evaluation & Reports
```

This covers the user's Member 1 lane:

- core backend APIs
- Neon/PostgreSQL + Prisma database integration
- JWT authentication, RBAC, ownership/privacy
- assessment-template/session/response/report backend APIs
- DeepSeek-backed AI evaluation
- scoring and candidate report generation

## Daily report style

The user's dashboard report style is concise, one-sentence, and concrete. Prefer a single `Worked on... by...` or `Improved... by...` sentence over multi-paragraph engineering summaries. Do not add extra explanation unless the user asks for detail.

Template:

```text
Worked on <area> by adding/implementing <specific slices>, <specific slices>, and <specific integration/result>.
```

Preferred example for this Member 1 backend task:

```text
Worked on backend development by adding the core API structure, integrating the database, implementing authentication and role-based access control, and connecting DeepSeek V4 Flash for AI evaluation.
```

If the user asks “how far are we” or “be more specific,” then expand into short bullets with status percentages and done/not-yet-done lists. Otherwise keep the report paste-ready and brief.

## Scope boundary

Do not confuse Member 1 with Member 4.

- Member 4: coding assessment UI/code editor/candidate coding flow.
- Member 1: backend evaluation/scoring/report logic that can consume a coding submission or execution result.

Avoid suggesting access-code/candidate UX or coding UI work as Member 1 next task unless the user explicitly asks to help that lane.

## Status wording

If implementation is mostly complete but the weekly task is still open for integration/documentation/bug-fix reports, say:

```text
In Progress — implementation mostly complete; continuing integration, verification, and AI/report polish.
```

Avoid marking a weekly dashboard task done after one engineering slice just because the code for that slice was committed.
