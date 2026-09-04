# Next.js reference-screenshot UI matching

Use when the user points at a folder of UI screenshots/assets and asks the frontend to look exactly like it.

## Workflow

1. **Protect current work first**
   - From the requested repo, run `git status --short --branch && git diff --stat` before editing.
   - Treat uncommitted files as potentially user/team work; stage only intended files later.

2. **Inventory the design folder**
   - List all screenshots and assets, including case-sensitive folder names (`Ux-Ui` vs `UX-UI`).
   - Load each screenshot with vision and extract concrete implementation notes: layout grid, typography, colors, spacing, button sizes, logo placement, nav states, and empty states.
   - Do not rely on memory of the screenshot after one glance; compare live browser screenshots against the target after edits.

3. **Use supplied logo/assets, but verify crop**
   - Copy the supplied logo into the app public/static asset path.
   - If an SVG is a large-canvas export with lots of whitespace, crop/position it into a reusable app asset or wrapper.
   - If the SVG is an embedded raster export (common in Figma/Canva exports) with a black/white canvas or mask, do not fight it with CSS transforms. Extract the embedded `data:image/...;base64` image, convert the canvas/background color to transparency, crop to the non-background bounding box with small padding, and save a clean `public/<brand>-mark.png`/SVG asset. Then render it with `h-full w-full object-contain` and no `overflow-hidden` clipping.
   - Browser-render the logo and inspect visually. CSS utilities like `size-[340%]` may be overridden by global `img { max-width: 100% }`; add `max-w-none` or explicit inline width/height when scaling an oversized crop inside a fixed logo box. Prefer a clean cropped asset over fragile oversized transforms.
   - Verify the logo on every surface that uses it: landing header, auth panel, sidebar, favicon/icon if in scope.

4. **Implement in thin visual slices**
   - Start with shared primitives: logo component, button, shell/auth layout, global tokens.
   - Then update one screen family at a time: landing, auth screens, dashboard/shell.
   - For auth-page families, compare every variant separately. Shared layouts can make pages look superficially right while still missing per-page content: left-panel marketing headline, feature rows, page title/subtitle, input labels/placeholders, password helper text, primary button text, secondary links, instruction boxes, resend timers, and footer reassurance copy.
   - For mock dashboard previews, match the screenshot's visible primitives (stats cards, line chart vs bar chart, activity rows, date chip, sidebar active state), not just approximate content.

5. **Visual QA before claiming done**
   - Open the exact live routes in the browser.
   - Compare screenshots against the design folder and any user-attached correction screenshots; correction screenshots often identify missing elements that were not obvious from the first pass.
   - Fix obvious mismatches: cut-off logo, wrong chart type, missing right-side preview details, missing auth form fields/helper text, absent left-panel headline/feature row, spacing drift, too-small/large buttons, stale text.
   - For auth/login pages, treat scale complaints as a shared-primitive problem first: adjust the auth layout positions, logo variant, form width, input min-height/padding/font, checkbox size, divider text, and button height/font across every auth route (`login`, `register`, `forgot`, `reset`, `verify`) instead of one-off zooming a single page. Reopen each route; compact pages should fit in the viewport without clipped bottom content.
   - Do not overcorrect scale feedback. If the user says auth pages are "too big," shrink toward the screenshot but keep a middle checkpoint; if they then say "too small," rebalance by increasing the shared primitives moderately rather than reverting to the original large sizing. Prefer proportional steps (for example form width/input height/font all move together) and visually inspect login plus at least one dense auth page such as register/reset.
   - If Tailwind button/input text sizes do not visually shrink or grow as expected, inspect computed styles in the browser. Shared button base classes such as `text-sm` can override later arbitrary utilities depending on class merge/order; use a clearer base variant or an important arbitrary class (for example `!text-[12px]`) only for the adjusted auth family.
   - Use browser console `getBoundingClientRect()`/computed styles to verify target-like dimensions (field/button heights, form width, logo mark size) when visual scale is disputed; browser screenshots alone can hide class-precedence issues.
   - Check browser console for errors.

6. **Verification and commit**
   - Run the repo's canonical gates (`pnpm lint`, `pnpm typecheck`, `pnpm build`, plus tests if present).
   - Run `git diff --check`, review `git diff --stat`, stage only intended files, commit, and push.

## Pitfalls

- Screenshot folder names may differ from the user's casing; inspect both `Ux-Ui` and `UX-UI` if needed.
- An exported SVG may render as a full white canvas rather than a tight logo. Do not assume it is directly usable in a 64px box.
- If the user repeats that “all pages” do not match, treat it as a route-by-route visual QA failure, not a request for another summary. Re-open each target/live route pair, fix the shared primitive first, and only report after browser screenshots plus canonical build pass.
- Tailwind arbitrary percentage sizing on `<img>` can be neutralized by global responsive image rules; confirm computed width/height in the browser.
- Do not stop after code edits. For visual matching, the deliverable is the live route looking close to the reference, backed by browser visual inspection and build output.
