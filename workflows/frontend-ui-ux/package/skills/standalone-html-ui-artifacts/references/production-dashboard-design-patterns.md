# Production Dashboard Design Patterns

Sourced from `popular-web-designs` skill templates (Stripe, Linear, Vercel). Apply these when a user says a dashboard "doesn't look production grade" or "looks like a prototype."

## Shadow system (Stripe-inspired)

Replace flat box-shadows with multi-layer tinted shadows. Tint with the brand's primary color, not neutral gray/black.

```css
/* Before — flat, generic */
box-shadow: 0 1px 3px rgba(0,0,0,0.1);

/* After — multi-layer, brand-tinted (Angkoro green example) */
--shadow-card: 0 0 0 1px rgba(1,51,38,0.06), 0 2px 8px rgba(1,51,38,0.04);
--shadow-raised: 0 0 0 1px rgba(1,51,38,0.08), 0 8px 28px rgba(1,51,38,0.08);
```

The first layer (`0 0 0 1px`) is Vercel's shadow-as-border technique — it replaces opaque CSS borders with a shadow edge. The second layer provides ambient depth. Stripe uses the same technique with blue-tinted `rgba(50,50,93,0.25)`.

## Borders (Linear-inspired)

Use semi-transparent borders instead of opaque ones.

```css
/* Before — opaque, harsh */
border: 1px solid #e2e8e4;

/* After — semi-transparent, brand-tinted */
--border: rgba(1,51,38,0.07);

/* Dark mode */
--border: rgba(255,255,255,0.06);
```

Linear uses this pattern throughout: `rgba(255,255,255,0.05)` to `rgba(255,255,255,0.08)` on dark backgrounds.

## Border radius (Stripe/Linear/Vercel)

Keep cards and buttons at 4-8px. Do not use pill shapes (9999px) on primary interactive elements — pills are for badges/tags only (Vercel rule). Segmented controls should use subtle rounding (4-5px), not pills.

```css
--radius: 6px;           /* cards, panels */
--radius-lg: 8px;        /* featured elements */
border-radius: 5px;      /* buttons */
border-radius: 4px;      /* inputs */
border-radius: 99px;     /* badges/tags ONLY — never on primary actions */
```

## Typography (Vercel/Linear)

Apply compressed negative letter-spacing at display sizes. Use a strict weight hierarchy.

```css
/* KPI values — most compressed */
letter-spacing: -0.04em;
font-weight: 700;

/* Headings */
letter-spacing: -0.035em;   /* h1 */
letter-spacing: -0.02em;    /* section titles */

/* Body */
letter-spacing: normal;
font-weight: 400-450;
```

Weight hierarchy: 400 (body/read), 500 (UI/interact), 600 (headings), 700 (data values only). Do not use 300 or 800 within dashboard chrome.

## Color system (Linear-inspired)

Use a single chromatic accent. All other colors are grayscale or status-only.

```css
--accent: #15c089;       /* Primary accent — money/data, CTAs, active states ONLY */
--success: #0b8a5e;      /* Status indicators only */
--warning: #b45309;      /* Status indicators only */
--destructive: #c2410c;  /* Status indicators only */
```

The accent should appear sparingly: on KPI values representing money, on primary CTA buttons, and on active navigation. It should NOT appear on borders, section headings, labels, or decorative elements.

## Surface luminance stepping (Linear-inspired, dark mode)

On dark backgrounds, use background luminance steps to create depth, not drop shadows.

```css
--bg: #080d0b;           /* canvas — darkest */
--surface: #0f1713;      /* cards — one step up */
--soft: #141d18;         /* hover states — another step up */
```

In dark mode, shadows should use `rgba(0,0,0,X)` (dark-on-dark), not `rgba(255,255,255,X)`. Linear's dark-mode card shadow example: `0 0 0 1px rgba(255,255,255,0.05), 0 2px 8px rgba(0,0,0,0.25)`.

## Dashboard composition rules

### Section ordering
Follow the canonical wireframe's order exactly. Do not reorder sections based on scenario state. The content inside each section changes with state; the section order is fixed. Industry pattern (Shopify, Amazon, Stripe) puts KPIs first, then action queues, then supporting context.

### Headline KPI row
Only performance metrics that move period-over-period belong here. Setup gates, readiness checks, and conditional statuses do NOT belong — use a conditional alert banner instead. Supporting metrics stay in the supporting section.

### No educational strips
"Money is a journey" / large explanatory blocks do not belong on an operational dashboard. Replace with a compact entry point ("Available to withdraw · $X" + link to Payments). The dedicated finance surface owns the detailed breakdown.

### No duplicate metrics
A metric should appear exactly once on the dashboard. If AOV is in the supporting section, it must not also appear in the KPI row.

### Conditional items
- Store Readiness: conditional yellow banner at top when checks fail, hidden when passing. Not a KPI card.
- Admin trust controls: compact chip band. Passing stays quiet. Missing shows "Unknown" — never a silent healthy state.

### Scenario toggle behavior
New / Healthy / Urgent demonstrates how the dashboard adapts to different operating states. The toggle itself is clean UI, not scaffolding. In production, these states are driven by real data.
- **New:** setup checklist only, period/analytics disabled.
- **Healthy:** all queues zero, "all caught up" state, distinct healthy dataset.
- **Urgent:** populated queues.

## Applying to an artifact

When converting a prototype to production grade:

1. Replace all opaque borders with semi-transparent equivalents
2. Replace flat shadows with multi-layer tinted stacks
3. Tighten border-radius on cards and buttons (6px from 12px)
4. Add negative letter-spacing to headings and KPI values
5. Audit color usage — move everything non-status to grayscale, reserve accent for money/CTAs
6. For segmented controls, replace pill-shaped buttons (9999px) with subtle 4-5px rounded segments
7. On dark mode, step surfaces by luminance not by adding more borders
8. Remove all prototype/demo labels and educational strips
9. Verify section order matches the canonical wireframe

## Research sources

- `popular-web-designs` skill → `templates/stripe.md`, `templates/linear.app.md`, `templates/vercel.md`
- Applied to Angkoro with green-tinted brand palette (`#013326` primary, `#15c089` accent)
