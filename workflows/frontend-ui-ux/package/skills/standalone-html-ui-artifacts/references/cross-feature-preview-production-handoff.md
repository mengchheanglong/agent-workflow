# Cross-feature preview coverage and production handoff

## Trigger

Use this when a standalone dashboard or staff-app preview is meant to approve a redesign broader than one page, especially when the user says “other tabs,” “Candidates and others,” or “feature front pages.”

## Preview scope

Do not infer that “other tab” means only another role or a subview of the current feature. Inventory the real top-level navigation and route landing pages, then state which representative surfaces the preview covers.

For a shared staff experience, a review artifact should normally demonstrate:

- operational Overview;
- aggregate Analytics;
- at least one record-management landing page;
- at least one browsable/catalog landing page when the product has one;
- the shared shell/navigation and card/list/table system.

Before asking for approval, statically verify that the artifact actually exposes every promised surface. Navigation labels alone are insufficient if the destination renders no representative content.

## Choose the pattern by the job

- **KPI/status cards:** a small set of decision-relevant summaries; remove totals duplicated below.
- **Attention cards:** emphasize a real nonzero issue; use a quiet state for zero/historical conditions.
- **Lists:** upcoming work, short queues, and recent changes.
- **Tables:** operational records requiring scan, compare, filter, and row actions.
- **Catalog cards:** browseable/selectable work items with description and a clear action.
- **Charts:** only after population, denominator, period, comparison context, exclusions, and caveats are defined.

Do not force a fourth card for symmetry when the approved contract supports only three useful signals.

## Production handoff

A standalone artifact approves information architecture and visual hierarchy; it is not the live product’s token source. Before implementation:

1. Read the production app’s global styles, font setup, shared shell, reusable cards/buttons, and responsive breakpoints.
2. Transfer the approved hierarchy using live tokens rather than copying preview pixel values or colors verbatim.
3. Audit every affected feature landing page that shares the component or pattern.
4. Preserve purpose-based differences: Overview is operational; Analytics is aggregate/comparative; candidate test-taking remains focused and separate from staff management.
5. Verify API semantics before labeling rates, attention states, and comparison charts.

## Evalora calibration example

- Candidates: five equal cards became four task-relevant states; overlapping completion/report cards were removed.
- Interview Sessions: total sessions moved out of the headline strip because the records table already provides it.
- Team: four cards remained, but expiring invitations receive attention only when nonzero.
- Templates: catalog cards remained appropriate; workspace-owned templates remained a table.
- Overview retained three cards because three immediate operational priorities were defensible.

## Verification

- Browser-check every affected top-level feature, not only Overview and Analytics.
- Check card count and table overflow at representative breakpoints.
- Ensure non-clickable status cards do not advertise clickability through hover lift.
- Confirm shared-component changes do not flatten important attention/quiet states.
- Run the production project’s lint, typecheck, build, and relevant backend tests after integration.
