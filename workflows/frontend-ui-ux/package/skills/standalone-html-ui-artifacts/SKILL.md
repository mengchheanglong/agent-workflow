---
name: standalone-html-ui-artifacts
description: Build and verify standalone HTML UI prototypes/artifacts when protected design skills cannot be edited.
version: 1.3.1
author: Hermes Agent
license: MIT
platforms: [windows, linux, macos]
metadata:
  hermes:
    tags: [html, ui, prototype, design, verification, artifacts]
    related_skills: [claude-design, popular-web-designs]
---

# Standalone HTML UI Artifacts

Use this skill when creating, consolidating, improving, or verifying a local standalone HTML UI artifact: prototypes, dashboards, landing pages, component previews, or multi-screen design demos.

This is a class-level companion to protected design skills such as `claude-design`. Prefer those for design doctrine, then use this skill for artifact integrity and verification details.

## Workflow

1. Inspect the provided source files/screens/tokens first.
2. Build one direct-open HTML artifact when portability matters: embedded CSS, embedded JS, no required build step.
3. Keep the surface composition appropriate:
   - dashboard/status = Monitor
   - admin queues = Operate
   - forms/settings/onboarding = Configure
   - landing/public = Decide/Learn
   - detail/report pages = Command/Inspect
4. Preserve source traceability when consolidating generated screens: include source names/routes in the artifact or notes.
5. Normalize visible brand/product names and shared tokens; avoid leaving legacy brand names in explanatory copy.
6. Use lightweight browser checks for visual work before broad test/lint runs, unless the user is asking for production integration or commit readiness.

For cross-feature redesigns, inventory the live top-level routes before building the preview, include representative management and catalog surfaces rather than only showcase dashboards, and verify each promised destination is actually rendered before asking for approval. On production handoff, preserve the approved hierarchy but reapply the live app's typography, colors, spacing, shell, and responsive tokens. See [`references/cross-feature-preview-production-handoff.md`](references/cross-feature-preview-production-handoff.md).

When choosing between standalone HTML, Vite/React, and Next.js for a functional mock-data shell, use [`references/frontend-shell-framework-selection.md`](references/frontend-shell-framework-selection.md). Default to standalone HTML for small disposable direct-open artifacts, Vite + React + TypeScript for multi-page frontend-only shells, and Next.js only when production reuse or server/auth capabilities are part of the current goal. Resolve overlapping features before creating routes, distinguish current-version pages from future expansions, and verify the live DOM plus representative interactions—not only build output or screenshots.

For plain-HTML products that must become multi-page working applications—with a shared sidebar/mobile shell, licensed local editorial media, clearly fictional community activity, and route-by-route CDP verification—follow [`references/multi-page-static-community-app.md`](references/multi-page-static-community-app.md). That reference distinguishes evidence-review forums from Reddit/X-style general-interest communities; choose the social product mode before styling or generating mock posts.

When a prototype must match a production app's design system exactly (colors, fonts, components, branding), follow [`references/design-system-sync-from-production.md`](references/design-system-sync-from-production.md) — mechanical token/primitive/font diffing against the production repo, not eyeballing. When re-syncing primitives verbatim from the production repo, re-apply prototype-only extensions afterward (e.g. a dialog that gained an extra prop a command palette depends on) — the verbatim copy silently breaks dependent pages otherwise.

When an approved PRD version change requires rebuilding or re-scoping an existing prototype (roles changed or collapsed, modules added/removed/merged into others, navigation renamed), follow [`references/prd-to-prototype-reconciliation.md`](references/prd-to-prototype-reconciliation.md) — audit-first sequencing, permission-model rewrite order, route-move pitfalls, and the sweep list for ghost terminology in prose and seed-data actor strings.

## Shell and component parity (the real source of "feels like two platforms")

Syncing tokens/fonts/ui primitives is necessary but NOT sufficient. When the user still says the prototype "looks and feels very different", audit these next layers:

- **Shell structure**: sidebar width/position/header, sticky topbar contents, content column (`container mx-auto` vs fluid padding), page vertical rhythm. A collapsible icon rail reads differently from FE's fixed 64px card sidebar even with identical colors.
- **Shared app components**: PageHeader title scale, KPI/stat card label-vs-value typography, table header style (uppercase 11px column labels vs sentence case), filter-bar stacking, callout/empty-state/badge construction. Diff these per-component against the production repo's equivalents.
- **A production repo often has MULTIPLE layout patterns** (e.g. a merchant dashboard with a sidebar AND admin pages with a gradient banner + centered container). Match the pattern of the *analogous* pages, not the most visually prominent one — an admin system should copy the repo's existing admin pages.
- **Vertical rhythm**: pages wrapping their own `space-y-*` inside a shell that also applies spacing double up inconsistently. Normalize page-level spacing to one scale across all pages.

## Production-readiness pass ("refine everything, it looks underdeveloped")

When the user asks to make a prototype production-ready, sweep for:

- **Prototype-only metadata rendered in the UI**: build-priority tags (P0/P2 chips in page headers), "prototype affordance" labels, reviewer notes. The PRD usually says priorities are "not necessarily labels shown in the final UI" — remove them everywhere, then typecheck (the prop removals cascade).
- **Badges/status indicators rebuilt on ad-hoc ring classes**: rebuild them through the shared shadcn `Badge` variants with a leading status dot so they match production exactly.
- **Role switchers / demo toggles the user hasn't asked for**: when told to remove one (e.g. "just Super Admin as default"), also delete the dead plumbing (`setRole`, context fields, switcher component) — leaving it causes TS errors later.
- **Inconsistent spacing/type scales** between pages — normalize to one ladder in a single scripted pass.

When the user asks to "make everything work with mock data" — i.e. convert a screens-only prototype whose buttons fire placeholder toasts into a functioning app where every action mutates shared state — follow [`references/mock-state-wiring-nextjs.md`](references/mock-state-wiring-nextjs.md): one seeded external store (`useSyncExternalStore`), one typed action per PRD workflow with automatic audit entries and cross-feature side effects inside the actions, per-page wiring checklist, and the shared-confirm-dialog contract pitfall (`onConfirm(reason)` — don't pass your own reason input).

## Print-ready PDF artifacts

When converting Markdown, reports, or standalone HTML into a polished PDF, follow `references/print-ready-html-to-pdf.md`. Treat the PDF—not the intermediate HTML—as the deliverable: refine pagination, preserve source URLs, add metadata/bookmarks/page furniture when useful, inspect representative rendered pages, and clean temporary build files. Avoid forcing every major heading onto a new page; render first and relax page breaks that create sparse carry-over pages.

For clickable directories, follow lists, and curated resource PDFs, lock the inclusion rule before designing. Remove weakly related, inactive, duplicated, unverified, or overly broad entries; prefer a focused official technical/team account when the corporate feed would add noise. Make the whole card clickable, then verify exact equality between the approved URL set and the final PDF URI set—not merely that the links return HTTP success.

## Dashboard KPI visualization artifacts

When a user asks for dashboard diagrams/charts or an actual dashboard based on KPI proposals, do not default to a generic process diagram. First map each KPI to the chart type that supports a seller/business decision, then build the artifact requested. See `references/dashboard-kpi-visualization-workflow.md` for the reusable workflow and chart-selection rules.

Key rules:
- PDF/chart guide requests should explain chart type, rationale, decision supported, data needed, check frequency, and MVP/future status for each KPI.
- Actual dashboard HTML requests should be Monitor/Operate surfaces with KPI cards, chart panels, queues, role-aware sections, and interactions such as date ranges or action drawers.
- If the user asks for an “actual dashboard with all KPIs”, make every proposed KPI visible as a real dashboard widget/card near the top. Do not collapse the proposal into only a few summary cards plus detail panels; that reads as a command-center summary, not the requested full KPI dashboard. See `references/full-kpi-dashboard-correction.md` for the concrete correction pattern.
- Use detail panels to expand/interpret the KPI cards, not to substitute for missing KPI cards.
- Clearly label sample values as illustrative/demo data, not real business data.
- When a prototype includes demo states such as **New / Healthy / Urgent**, treat each as a semantic dashboard contract rather than a cosmetic toggle: New is setup-only with analytics controls disabled, Healthy uses a distinct consistent dataset plus an all-caught-up zero-state with health first, and Urgent restores prioritized queues with attention first. Keep derived metrics, badges, notifications, and section numbering consistent with the active state.
- For the reusable role-aware implementation and browser assertion matrix, read [`references/demo-scenario-state-dashboards.md`](references/demo-scenario-state-dashboards.md).

## Ad-hoc verification for standalone HTML

When no canonical test/lint/build command exists, do not claim “suite green”. Run and report **ad-hoc verification** instead.

If a verification gate asks for fresh evidence after editing:

1. Create a temporary verifier script under the OS temp directory using a `hermes-verify-` filename prefix.
   - On this Windows host, use native temp paths like `C:/Users/User/AppData/Local/Temp` inside Python.
   - Use `tempfile.mkstemp(prefix='hermes-verify-', suffix='.py', dir=temp_dir)` or equivalent; on Windows, immediately close the returned raw descriptor with `os.close(fd)` before reopening or deleting the path.
   - Do not hard-code a collision-prone filename.
2. In the verifier, check the artifact-specific invariants, for example:
   - file exists and is readable
   - expected number of screens/routes/source references are present
   - embedded `<style>` and `<script>` exist when artifact is meant to be self-contained
   - unwanted CDN dependencies are absent when portability was required
   - known fixes/selectors/strings are present
   - legacy brand names are absent from visible copy when brand normalization was part of the task
   - extracted embedded JavaScript passes `node --check` when Node is available
3. Run the temporary verifier.
4. Clean up the temporary script and any temporary extracted JS.
5. Summarize as: “Ad-hoc verification: PASS/FAIL”, with the checked items and cleanup result.

## Browser verification

For high-fidelity UI artifacts, supplement script checks with browser checks when available:

- open the local `file:///...` artifact
- check browser console for JS errors
- click at least one representative navigation/action path
- use a visual screenshot/inspection for the primary viewport
- if a visual issue is found, patch it and rerun the focused check

On high-DPI Windows hosts, do not trust a shell screenshot's pixel dimensions as proof of the CSS viewport. Use Chrome DevTools Protocol device emulation to assert the requested CSS width, no unintended horizontal overflow, representative card bounds, and mobile/desktop control visibility before inspecting a CDP-captured screenshot. Always pass `--force-device-scale-factor=1` for plain `--screenshot` runs, or `--window-size=390` will not mean 390 CSS px. See [`references/chrome-cdp-mobile-verification.md`](references/chrome-cdp-mobile-verification.md) for the CDP recipe, including the dependency-free `requests` + `websockets` path, retained-log reset, favicon handling, interaction assertions, touch-target audit, settled smooth-anchor checks, and visual-defect patterns. See [`references/dashboard-kpi-visualization-workflow.md`](references/dashboard-kpi-visualization-workflow.md) for dashboard composition (storytelling acts, fitting the artifact to the user's live frontend design tokens) before building.

## Dashboard section ordering

When building a dashboard from a canonical wireframe (`04_Dashboard_Grouping_and_Wireframe.md`), follow the wireframe's section order exactly — do not invent a scenario-dependent reordering:

- The wireframe specifies a fixed reading order (e.g., Business health → Needs attention → Supporting → Conditional).
- Do not flip the order based on scenario state (e.g., moving attention before health in "urgent" mode). The content inside each section changes with state; the section order does not.
- When the user questions the order ("do other companies do it like this?"), research the industry pattern (KPIs-first is standard for Shopify, Amazon, Stripe) but defer to the canonical wireframe if it already matches.
- On mobile, the wireframe may specify a different order; apply that as a media-query change, not a scenario-state change.

## Section header style

- **No numbering.** Section headers like "1 · Business health" or "2 · Needs attention" look like a wireframe spec, not a production product. Use clean, descriptive titles without numeric prefixes.
- **Section headers are title-only.** Do not add long explanatory subtitles to every section. A single short subtitle is acceptable; a full sentence of documentation prose is not.
- The visual hierarchy (size, weight, spacing) is enough to communicate order — numbering adds nothing.

## Period selector placement

Do not put the period selector (7D / 30D / 90D) in the global topbar. Place it in the section header of the data it controls — "Business health" or "Platform health" — as a right-aligned segmented control. This makes it clear which data changes when the user switches periods, and keeps the topbar clean.

## Attention indicators vs full queue cards

Do not duplicate full queue cards from dedicated pages (Orders, Payouts, etc.) onto the Overview dashboard. The overview should show compact attention indicators — a horizontal strip of count badges — that give the user a quick glance and link to the dedicated page for action.

- **On the overview:** compact inline strip like `3 to decide | 4 to fulfill | 5 stock items` with bold counts and muted labels
- **On the dedicated page:** full queue cards with individual items, accept/reject/fulfill buttons, and detailed metadata
- Each indicator in the strip is clickable and links to the relevant page or action
- Zeroes show in muted gray; non-zero counts show in warning/destructive color
- Use thin pipe separators (`border-right: 1px solid var(--border)`) between indicators, not cards or backgrounds
- Use SVG icons from the design system, never emoji

## Admin dashboard scope

When building an admin/operations dashboard vs a business-owner dashboard:

- **Growth metrics (first subscriptions, first paid orders) belong on Analytics, not the admin Overview.** An admin opens the overview to process payouts, verify banks, and handle renewals — not to review month-over-month acquisition trends.
- **Rare transient events (failed onboarding, stuck jobs) are conditional alerts, not permanent overview items.** Show them only when an explicit failure occurs; hide them when resolved.
- The admin overview should answer: "What needs my action right now?" and "Is the platform healthy?" — not "How is the platform growing?"

## Production-grade dashboards vs prototypes

When the user asks for a "final" or "production-grade" dashboard (as opposed to a prototype), apply these rules:

- **Remove all prototype/decorative labeling.** No “illustrative demo data,” "interactive prototype," "(demo)" toasts, or "Prototype" in the page title. The artifact should look like it ships.
- **Remove educational/decorative strips from the main surface.** Do not add onboarding banners, "X is a journey" explanations, or multi-paragraph concept primers as permanent dashboard sections. The overview is for monitoring and decision-making, not education. Move explanations to detail drawers, tooltips, or dedicated pages (e.g., a Payments page owns money-state explanations, not the overview).
- **Keep the surface compact.** A production dashboard prioritizes: (1) what needs action right now, (2) headline health, (3) supporting context. Everything else is secondary.
- **Prefer single currency when the user asks.** Do not force dual-currency (USD/KHR) display onto a dashboard that the user wants in one currency. Remove all traces of the unused currency from data, labels, and logic — not just hide it.
- **Setup/readiness items are conditional banners, not KPI cards.** Store readiness, platform setup checks, configuration completeness, and similar gate-status items do not belong in the headline KPI row. They have no period-over-period trend, and when everything works they display one static value forever, wasting premium space. Instead, render them as a yellow alert banner above the main content that appears only when checks fail and disappears entirely when all pass. The detailed checklist can live in a secondary section at the bottom of the page, but the call-to-action lives in the banner.
- **Scenario toggles are production behavior, not prototyping.** A New/Healthy/Urgent toggle demonstrates how the dashboard adapts to different operating states. Keep it when the user values it; the toggle itself is clean UI, not scaffolding.

## Pitfalls

- Do not say "verified" without stating the verification type.
- Do not confuse ad-hoc artifact checks with canonical project tests.
- Do not keep stale temporary verifier files in the user's temp directory.
- Do not leave contradictory product names in "before/after" explanatory copy; they still count as visible brand inconsistency.
- Do not add educational strips, concept primers, or decorative labeled sections to a production dashboard surface. The overview is a Monitor/Operate surface — move explanations to drawers, tooltips, or dedicated pages.
- Do not put setup/readiness/configuration-status items in the headline KPI row. They are conditional gates, not performance metrics. Use a yellow alert banner that hides when all checks pass.
- **Do not add unapproved items to the dashboard.** If a metric (e.g., "Available to withdraw") is not in the approved `03_Dashboard_Content.md`, do not add it as a navigation link, compact card, or any other form on the overview — even if it seems useful as a shortcut to another page. Scope creep erodes trust in the dashboard spec.
- When a user says a dashboard "doesn't look production grade" or "looks like a prototype," load `popular-web-designs` (Stripe, Linear, Vercel templates) and apply the patterns in `references/production-dashboard-design-patterns.md`: multi-layer tinted shadows, semi-transparent borders, tight radius, compressed typography, and single-chromatic-accent color systems.

## Reference

- `references/menui-session-record.md` — the Menui dashboard pass this skill was distilled from: exact changes per surface, working verification pipeline, and the false alarms identified along the way.
- `references/angkoro-admin-prototype-session-record.md` — full session record for a Next.js admin prototype: PRD-driven feature moves, multi-round shell parity against a production repo with two layout patterns, mock-state wiring, server/client conversion recipe, zombie dev-server recovery, and the production-readiness sweep.
- Browser caching can show stale local files. Use a cache-busting query string such as `?rev=2` when re-opening a local artifact after edits.
- **SVGs in flex containers need explicit size constraints.** An inline SVG with a `viewBox` but no `width`/`height` will render at its default viewport (300×150) inside a flex container, breaking the layout. Wrap in a `<span>` with explicit `width`, `height`, and `flex:none`, or add `width`/`height` directly to the SVG element. This is especially common in section headings that pair an icon SVG with text.
- **Inline onclick inside IIFEs breaks after innerHTML re-render.** When building multi-page HTML with an IIFE `(()=>{...})()`, functions defined inside the IIFE are not globally accessible. After `element.innerHTML = ...` rebuilds the DOM, any `onclick="fn()"` handlers referencing IIFE-scoped functions will fail silently. **Fix:** replace all inline `onclick`/`onsubmit`/`onchange` with `data-*` attributes (`data-nav`, `data-act`, `data-theme-toggle`), then attach a single delegated event handler on the root element after each `innerHTML` assignment. Use `addEventListener('click',...)` with a manual `parentElement` walk-up loop rather than `closest()` which can fail on SVG child elements.
- **Never full-re-render a view that contains user-entered form input.** In a render-per-view SPA artifact, calling the page's render function from an in-form action (apply promo code, toggle a summary option) rebuilds the whole view and silently wipes everything the customer typed — name, email, card fields. The failure is sneaky: validation then blocks submit and the user doesn't know why; it only surfaced in this session via scripted CDP end-to-end testing (promo applied → pay → silent no-op). **Fix:** in-form mutations must be targeted DOM updates — keep stable element ids for each mutable node (`#discLine`, `#grandTotal`, `#payBtn`) and create-or-update just those; reserve full `render*()` calls for route changes only.
- **Conditional string-concatenated markup can emit broken tags per state.** Building element HTML through nested ternary concatenation makes it easy to put the closing tag inside only one branch (e.g. `"Pay "+total+"</button>"` in the else branch only). The browser recovers silently and the defect only appears in the other state (spinner shows inside a malformed button). Keep open/close tags outside the conditional expression entirely.
- **Server Component + client hook = prerender failure.** A Next.js page converted from `async`/`await params` server style to `use(params)` + a client store hook MUST get `"use client"` at the top and lose `generateStaticParams`. Build error signature: `Attempted to call useMockState() from the server but useMockState is on the client`, failing while prerendering specific record routes.
- **Stale generated route types after moving/renaming route directories**: `.next/**/types/validator.ts` keeps phantom "Cannot find module .../page.js" errors for deleted routes → delete `.next`, re-run typecheck.
- **Check shared-component contracts before bulk usage.** A confirm-dialog may own the reason textarea itself (`onConfirm(reason: string)`) — wiring pages against an assumed `children`-based reason input produces a cascade of TS errors across every page at once. Read the component's exported types first; DataTable filters likewise use `label`, not `header`.
- **Large multi-edit turns can mangle JSX structure** when a patch's replacement text is inserted mid-file with mismatched indentation or duplicated blocks. After any large patch to a TSX file, run typecheck immediately and inspect the diff for duplicated JSX sections before continuing — a structurally broken file compounds errors across subsequent edits.
- **Zombie dev-server pile-ups masquerade as app bugs.** Symptom: Next.js dev overlay "Jest worker encountered 2 child process exceptions, exceeding retry limit", random 500s on recently-edited detail routes while the production build passes cleanly, and stale content served on port 3000. Cause: orphaned `next dev` processes from repeated restarts holding a torn `.next` cache (check with `netstat -ano | grep LISTEN | grep :300` — dozens of node PIDs is the tell). Fix requires killing ALL node processes + `rm -rf .next` + one fresh server; a single restart is not enough because the old listener still owns port 3000. Never diagnose code from a dev server whose port you didn't just start.
- **`taskkill //PID <pid> //F` in git-bash fails with "Invalid argument"** (`//F` mangling). Working alternatives: `powershell -Command "Stop-Process -Id <pid> -Force"` or start the new server on a different port (`npx next start -p 3011`) instead of fighting for 3000.
- **Mass-killing all node processes is consent-gated** on this host — it also kills unrelated user apps. When cleanup requires it, hand the exact commands to the user instead of running them.
- **Removing a prop used in ~25 call sites**: a regex sweep over `app/**/*.tsx` catches most occurrences but misses same-line variants; re-grep after the sweep (`grep -rn 'priority="P' app`) and sed the remaining files by explicit path list. Verify with typecheck before moving on.
