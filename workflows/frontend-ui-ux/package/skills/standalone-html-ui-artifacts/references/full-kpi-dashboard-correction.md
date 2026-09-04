# Full KPI Dashboard Correction Pattern

Session lesson: when a user asks for an actual dashboard based on a KPI proposal, especially with wording like “with all the KPI you suggested,” the deliverable must expose every proposed KPI as a first-class dashboard widget/card. Do not build only a few top summary cards with the rest represented indirectly in lower sections.

## Failure mode to avoid

A dashboard that has:
- a small command-center summary at the top;
- only 3–4 KPI cards;
- detail panels/sections for the remaining KPI themes;
- action drawer logic;

can still be useful, but it may not satisfy “actual dashboard with all KPIs.” The user may read it as a summary prototype rather than the requested full KPI dashboard.

## Correct pattern

For full-KPI dashboard HTML artifacts:

1. Put all proposed KPIs in a visible KPI grid near the top.
2. Each KPI card should include:
   - KPI name;
   - current sample value;
   - chart type label;
   - mini visualization matching the KPI logic;
   - one action/decision sentence;
   - optional “View KPI logic” detail action.
3. Below the KPI grid, add richer panels grouped by decision area:
   - sales/revenue;
   - order/action center;
   - product/inventory;
   - customer/checkout/payment;
   - finance/readiness.
4. Detail panels should expand the KPI cards, not replace missing KPI cards.
5. Keep role-gated finance visible for owner/manager and hidden for staff/limited roles across both KPI card and lower finance panel.
6. Use date range controls to update KPI values and chart examples.
7. Label values as demo/illustrative if not from live data.

## Verification additions

Focused ad-hoc verifier should check:
- exact KPI card count matches expected KPI list;
- all KPI names appear;
- all chart type labels appear;
- role-gated finance selector/classes exist;
- embedded JS syntax passes `node --check` when available;
- sample/demo data notice exists;
- no secret-sensitive strings are embedded.
