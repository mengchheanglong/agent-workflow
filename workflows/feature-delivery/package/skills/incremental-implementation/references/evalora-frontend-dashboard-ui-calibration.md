# Evalora frontend dashboard/UI calibration

Use this reference when building or polishing Evalora dashboard/auth pages from screenshots.

## Product-fit before copying a reference

When the user supplies a polished analytics/dashboard reference, first map each visible widget to Evalora's real product model:

- Admin + interviewer are platform users.
- Candidates are invite/access-code participants, not normal dashboard users.
- Backend-aligned entities: templates, interview sessions, candidate responses, evaluations, candidate reports, reviewer notes.
- AI output is advisory; do not imply final hiring decisions.

Approved analytics structure for Evalora MVP:

- Admin and Interviewer use one shared Overview and Analytics page structure; authorization may change accessible records but not the metric catalog.
- Candidate has no dashboard or analytics access.
- Overview is operational: assessments in progress, invitations awaiting start, reports pending, next active assessments, newly ready reports, and recent session updates.
- Analytics is explanatory: closed-session completion, report coverage, comparable-group score distribution, comparable-group module evaluation, completion duration, and template usage.
- Score `0` is `No assessable evidence`, not ordinary weak performance.
- Candidate identity belongs in candidate/session/report views, not aggregate analytics payloads.
- Candidate report scores remain advisory and must not be presented as final hiring rankings.

Avoid unless the backend and approved metric contract explicitly support it:

- Mixed-template or mixed-role average score headline cards.
- `Top Performing Candidates` or highest-score leaderboards.
- Raw AI strength/improvement phrase counts without a governed taxonomy.
- Time trends without approved period, cohort/event basis, and comparison rules.
- Separate Admin and Interviewer analytics products when only record permissions differ.
- Candidate acquisition source such as LinkedIn/referral/company website.
- Rejected/withdrawn hiring outcome counts.
- SaaS upsell cards such as `Upgrade to Pro`.
- Export actions that imply report export if only individual report export exists.

## Visual calibration loop

For screenshot-matching pages, use a middle-size visual tuning loop rather than one big resize:

1. Implement the closest structure using existing shared shell/components first.
2. Browser-open the exact route and inspect a screenshot.
3. If user says `too big`, reduce by one step only: card padding, type, icon sizes, field/button heights, max widths.
4. If user then says `too small`, rebalance upward to the midpoint; do not keep shrinking.
5. Re-check all sibling pages affected by shared components.
6. Run `pnpm lint && pnpm typecheck && pnpm build`.
7. Stage only intended files; leave unrelated modified files untouched.

## Desktop dashboard layout lessons

For Evalora dashboard/analytics pages:

- Use `AppShell` so sidebar, top search, profile, and active nav stay consistent.
- Use one shared page structure for Admin and Interviewer; do not fork layouts by technical API scope.
- Keep the Overview compact and operational. Do not force six equal KPI cards when queues and prioritized lists better answer the selected questions.
- Keep Analytics separate from Overview and restrict comparisons to approved comparable groups.
- Header action buttons must use `whitespace-nowrap` and short labels if the top bar is tight (`May 2026`, `Export`).
- If a table beside an activity panel becomes cramped, keep the table full-width until a larger breakpoint (`xl`) rather than forcing a split at `lg`.
- Prefer plain CSS/SVG chart mockups over adding new chart dependencies for MVP static dashboards.

## Commit hygiene

Evalora frontend often has unrelated local changes. Before committing a UI slice:

- Check status.
- Commit only the files touched for the current request.
- Run `git diff --cached --check` and a secret scan.
- Push verified commits immediately when the slice passes.
