# Extracting Standalone HTML from Next.js Source

When the user wants faithful standalone HTML replicas of Next.js dashboard pages:

## Process

1. **Read the source `page.tsx` files** — understand the component structure, data fetching, and rendered output. Focus on the JSX return block, not the hooks/state management.

2. **Identify the key visual sections** — wallet cards, KPI grids, action sections, tables, charts. Map each to plain HTML with the same CSS tokens.

3. **Match the design tokens** — pull colors, shadows, borders, radius, typography from the real `globals.css` or tailwind config. Convert to CSS custom properties.

4. **Use `<article>`, `<section>`, `<div>` structure** that mirrors the original component hierarchy without React. Every section that was a `<Card>` becomes a `<div class="panel">`.

5. **Hardcode mock data** that matches the real API response shapes (same field names, same value ranges). Use the real TypeScript interfaces as the data schema.

6. **Preserve navigation structure** — keep the sidebar with all real routes, even if linked pages don't exist in the standalone version. Use toast notifications for navigation stubs.

7. **One file for multi-page navigation** — when combining pages, use `data-*` attributes with delegated event handlers (see skill pitfalls). Show/hide views with `.view { display:none } .view.active { display:block }`.

## Common page patterns

### Overview/Dashboard
- Greeting + store domain live indicator
- 3-4 KPI cards (revenue, orders, pending, average)
- Recent orders list with status badges
- Store info card (domain, currency, contact)

### Orders
- Action sections at top: Awaiting Decision, Ready to Fulfill, COD Collection
- KPI row: total orders, awaiting, ready to fulfill
- Full order table: order number, amount, date, status

### Products
- Search + filter toolbar
- Product table: name/SKU, price, stock, status, actions

### Analytics
- KPI row: total revenue, orders, average order, products sold
- Revenue by Month bar chart
- Top Selling Products (by revenue)
- Orders by Status breakdown with progress bars

### Payments
- 4 wallet cards: Available, Pending, In Escrow, Total Paid Out
- Bank accounts list with verification status
- Payout history
- Transaction ledger

## Data conventions

All monetary values in cents (matching the real API). Convert to display dollars with:
```js
const Fmt = n => '$' + (n/100).toLocaleString('en-US', {minimumFractionDigits: 2});
```

Status badges follow the real app's color mapping:
- COMPLETED/PAID → green (success)
- PENDING/COD → amber (warning)
- ACCEPTED/SHIPPED → blue (info)
