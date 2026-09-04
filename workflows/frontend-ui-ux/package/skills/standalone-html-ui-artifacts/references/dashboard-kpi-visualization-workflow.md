# Dashboard KPI Visualization Workflow

Use this reference when a user asks for dashboard diagrams/charts or an actual dashboard based on KPI proposals.

## Core lesson

Do not turn a dashboard-visualization request into a generic process diagram. For seller/business-owner dashboards, the valuable artifact is usually a KPI-to-visualization map and/or an actual monitor/operate dashboard surface.

## Research-backed chart mapping pattern

Before choosing chart types, sample established dashboard patterns from relevant platforms and apply the logic, not the full complexity:

- Shopify-style analytics: metric cards, labeled sections, date ranges, period comparisons, target/gauge cards.
- Amazon Seller Central-style operations: action queues, order/workload health, SKU/inventory risk, fulfillment/status problems.
- Google Analytics-style ecommerce: purchase/checkout funnels, abandonment/retention between steps, product-event metrics.
- Stripe-style finance/payment analytics: key metric cards, trend lines, reason/category breakdowns, balance/revenue separation.

## Chart rule of thumb

- Time/change over period -> line or area trend.
- Target/progress -> gauge or progress card.
- Ranking/comparison -> horizontal bar ranking.
- Composition/status mix -> donut or stacked bar.
- Journey/drop-off -> funnel.
- Operational urgency -> priority queue/action card, not a decorative chart.
- Inventory risk -> threshold bars and stock-vs-sales quadrant.
- Sensitive finance -> role-gated cards with clear available/pending/escrow separation.

## Recommended artifact sequence

1. If the user asks for a PDF/chart guide, create a separate guide with one KPI per chart recommendation.
2. For each KPI include: chart type, why it fits, decision supported, data needed, check frequency, and whether data is MVP/current/future.
3. Clearly label example values as illustrative/demo data, not real business data.
4. If the user then asks for actual HTML, switch surface to Monitor/Operate, not Decide/Learn/report.
5. Build a direct-open HTML dashboard with realistic sample data, interactions, and role-aware visibility.
6. Verify with browser visual inspection, representative interactions, console checks, and ad-hoc verifier when no canonical suite exists.

## Fit prototype to the user's live frontend design system

When the target product repo is reachable, read its design vocabulary before choosing any tokens — never invent a fresh palette when a real one exists:

1. Find the token source first (`app/globals.css`, theme files, tailwind config) and copy the exact color/token values into the artifact's CSS variables. Example (Angkoro): `--accent:#15c089` mint, `--primary:#013326` deep green, `--chart-1..5`, plus the light/dark inversion block.
2. Mirror the real component semantics, not just colors. If the repo has a `KpiCard` with a rule like "emphasize mint only for money the merchant can act on", honor that rule in the artifact. If the sidebar uses grouped nav with a mint active pill, reproduce that pattern rather than a generic dark sidebar.
3. Check whether the requested surface already exists. If the repo's admin area has only scaffolding (e.g. only a create-store page, no overview), say so — the prototype is then the design target, not a restyle of an existing page.
4. State the mapping in the final report: which repo files the tokens/components came from, so the user can verify the fit.

## Storytelling structure for role dashboards

For analytics/admin dashboards the user calls "senior" or asks to be told as a story, structure the page as ordered numbered acts rather than a flat widget grid:

1. Health first (primary KPIs with sparkline + previous-period comparison + contract-ID badge).
2. Needs attention second (action queues as prioritized work lists with guardrail footnotes — never force operational work into decorative charts).
3. Growth/explanation third (supporting metrics with period-comparison bars and interpretation guardrails).
4. Trust/control last (compact status band: passing states stay quiet; missing/stale/failed shows `Unknown`/`Not connected`, never a fake healthy state).

This mirrors the question-first analytics doc's own `04` wireframe groups, so the artifact and the documentation tell the same story.

## Pitfalls

- Avoid wide tables as the primary dashboard surface; use cards, grids, charts, queues, and drill-downs.
- Do not add mature-platform KPIs like CAC/ROAS/profit as real dashboard metrics until the required data is tracked. Mark them as future data.
- Do not copy Shopify/Amazon/Stripe layouts directly; transform their dashboard logic into the user's product stage.
- Do not produce a static report-like HTML when the user asks for an actual dashboard; include interactive date ranges, action drawers/toggles, or role views when useful.
