# Demo Scenario States for Operational Dashboards

Use this pattern when a dashboard prototype needs a segmented **New / Healthy / Urgent** demo control. The scenarios must change dashboard semantics and story order—not just colors, labels, or sample numbers.

## State contract

| Scenario | Primary purpose | Data/controls | Story order |
|---|---|---|---|
| New | Configure prerequisites before analytics are trustworthy | Show setup/readiness only; hide performance and action queues; disable period/export controls | Setup only |
| Healthy | Monitor performance when no immediate work exists | Use a distinct healthy dataset; set action counts to zero; remove queue cards; show an explicit all-caught-up state | Health/performance → current work zero-state → explanation → controls |
| Urgent | Operate against immediate work | Populate prioritized queues and notification/badge counts | Needs attention → health/performance → explanation → controls |

## Role-aware adaptation

Do not reuse the same New checklist across roles:

- **Seller/business owner:** store activation, sellable products, checkout, payout bank, notifications, contact/fulfillment settings.
- **Platform admin:** authoritative order/subscription sources, payout-provider callbacks, bank-verification workflow, independent recomputation, wallet–ledger reconciliation.

Healthy and Urgent also remain role-aware: seller queues concern order decisions, fulfillment, and inventory; platform-admin queues concern payouts, bank verification, grace renewals, onboarding failures, and integrity controls.

## Data integrity rules

1. Healthy should use its own internally consistent demo dataset rather than reusing Urgent values.
2. Derived metrics must recompute from the active scenario. Example: AOV = Paid Sales / Paid Orders for the same currency and population.
3. New must not display zeros as if they were measured business performance; hide analytics until prerequisites are complete.
4. Scenario changes should update all related UI state: section order/numbers, queue counts, sidebar badges, notification dot/message, status copy, and disabled controls.
5. Preserve semantic boundaries such as Paid Sales ≠ wallet balance ≠ payout ≠ profit and never merge USD/KHR without an approved conversion rule.

## Implementation pattern

- Keep one state field such as `scenario: 'urgent'`.
- Generate the segmented buttons from a fixed source list (`['new','healthy','urgent']`).
- Centralize count resets/restores in an `applyScenario()` function.
- Compose sections conditionally rather than merely hiding random cards after render.
- In Urgent, concatenate attention before health; in Healthy, concatenate health before the all-caught-up section; in New, render only the setup panel.
- Disable period/export controls in New and hide filters that imply analyzable data.

## Verification

Static checks:

- Embedded JavaScript passes `node --check`.
- Scenario source list, click binding, setup-only branch, healthy zero-state, urgent reorder, and disabled New controls are present.
- Contract IDs remain in the artifact even if some widgets are scenario-conditional.
- No prototype/demo labels: toasts are clean ("Order accepted" not "Order accepted (demo)"), no "illustrative demo data" notice, no "interactive prototype" in page title.

Browser checks for **each role**:

1. Click Urgent: active button is Urgent, first section is Needs attention, queues exist, period is enabled.
2. Click Healthy: active button is Healthy, health is first, all-caught-up exists, queues do not exist, period is enabled.
3. Click New: active button is New, setup heading exists, KPIs/filters/queues do not exist, period is disabled.
4. Emulate 390 CSS px and assert `documentElement.clientWidth === documentElement.scrollWidth`.
5. Capture representative screenshots and visually inspect the segmented control, first viewport, whitespace, and queue/card stacking.

### Pitfall: generated controls

If buttons are generated from a source array, a verifier that searches for literal `data-scenario="new"` in the HTML source will fail incorrectly. Validate the source list statically and validate the three rendered buttons in the browser DOM.

## Production-grade presentation rules

When the artifact is a "final" dashboard rather than a prototype:

- **Single currency:** If the user wants USD only, remove all KHR data, labels, and logic. Do not leave KHR as a hidden or disabled option — strip it entirely.
- **Clean toasts:** Drop "(demo)" suffixes. "Order accepted" is the production text.
- **Compact money entry:** Replace educational strips ("Money is a journey, not one number…") with a single compact link row: "Available to withdraw: $X · Pending: $Y | [Manage payments →]". The Payments page owns the detailed money-state explanation.
- **Notification indicators:** The bell dot should only appear in Urgent state. Healthy state removes it.
- **No prototype notice:** Remove the green info banner that says "interactive prototype · illustrative demo data." The artifact stands on its own.
- **Setup items as conditional banners, not KPI cards:** Do not place Store Readiness, platform setup checks, or configuration-status items in the headline KPI row. They have no trend, and a "Ready" value wastes a premium card forever. Instead:
  1. Render a yellow alert banner above the main content when any check fails — e.g., "2 setup issues need attention — your store can't accept payouts. [Fix now →]"
  2. Keep the detailed checklist in a secondary section at the bottom of the page.
  3. Hide the banner entirely when all checks pass (Healthy state).
  4. The KPI row should contain only performance metrics that move period-over-period.
