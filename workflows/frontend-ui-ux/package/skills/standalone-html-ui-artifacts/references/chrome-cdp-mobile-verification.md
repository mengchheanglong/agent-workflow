# Chrome CDP Mobile Verification for Standalone HTML

Use this when a standalone HTML artifact needs credible mobile verification on Windows or another high-DPI host.

## Why shell screenshots can mislead

A headless Chrome command such as `--window-size=390,844 --screenshot=...` may produce a 390-pixel image while the live CSS viewport is wider because of display scaling. A screenshot can therefore look clipped even when the page has no CSS overflow—or hide a real responsive defect.

Do not diagnose from that image alone.

## Reliable sequence

1. Start a temporary headless Chrome instance with a unique remote-debugging port and temporary user-data directory.
2. Locate the local `file:///` page through `http://localhost:<port>/json/list`.
3. Connect to the page WebSocket debugger URL.
4. Call `Emulation.setDeviceMetricsOverride` with the intended CSS width, height, and `deviceScaleFactor: 1`.
5. Use `Runtime.evaluate` to assert:
   - `window.innerWidth` equals the requested width;
   - `document.documentElement.clientWidth === document.documentElement.scrollWidth` when horizontal scrolling is not intended;
   - a representative card lies within the viewport;
   - mobile-only and desktop-only controls have the expected computed `display` values.
6. Call `Page.captureScreenshot` through CDP, then inspect that screenshot.
7. Exercise at least two representative interactions through `Runtime.evaluate` or input events, such as a primary navigation route and a drill-down/tab. Assert the resulting heading or visible content.
8. Stop Chrome and delete the temporary profile, screenshots, and probe scripts.

## Dependency-free interaction audit

When Playwright or Puppeteer is unavailable, do not install a browser framework just to verify one standalone artifact. Chrome's native DevTools protocol plus Python's `requests` and `websockets` modules is enough:

1. Serve the artifact locally when `file://` behavior is not the subject of the test.
2. Launch a temporary headless Chrome with a unique `--remote-debugging-port`, temporary `--user-data-dir`, and `--force-device-scale-factor=1`.
3. Read `/json` or `/json/list`, select the exact page, and connect to its `webSocketDebuggerUrl`.
4. Enable `Runtime`, `Log`, and `Page`, then clear the client's accumulated event list **before** the fresh reload. `Log.enable` may replay retained entries from an older page load; without this reset, a historical favicon 404 can be misreported as a new failure.
5. Reload with cache ignored and poll `document.readyState` rather than sleeping blindly.
6. Use `Runtime.evaluate` to exercise and assert real behavior: filter counts and `aria-pressed`, dialog open/submit/close/field clearing, navigation hashes/headings, mobile/desktop control visibility, and local-only form behavior.
7. Assert `performance.getEntriesByType('resource')` contains no unexpected external resources when the artifact promises offline/self-contained behavior.
8. Measure every visible `a`, `button`, `input`, and `textarea` with `getBoundingClientRect()` at the mobile viewport; report any target with width or height below the required threshold (typically 44px).
9. Capture desktop and mobile screenshots through `Page.captureScreenshot`, then inspect the pixels; numeric checks do not replace visual QA.
10. Stop Chrome and the local server and delete the temporary profile.

For strict zero-console-error checks, declare a favicon explicitly. A dependency-free artifact can use `<link rel="icon" href="data:,">` to prevent Chrome's automatic `/favicon.ico` request. This avoids hiding a real error behind an "expected favicon 404" exception.

Smooth anchor navigation must be measured after scrolling settles (for example, six stable `requestAnimationFrame` samples). The invariant is that the target is not hidden behind a sticky header; do not fail an otherwise correct page because the clearance exceeds an arbitrary maximum.

## Dashboard-specific checks

For an interactive dashboard prototype, also assert:

- every approved KPI/content item is visible in the intended route or drill-down;
- illustrative values are visibly labeled as demo/sample data when no live source is connected;
- finance values are not presented as interchangeable with sales, profit, or payout history;
- mobile bottom navigation has an active state and content has enough bottom padding;
- no desktop toolbar duplicates the mobile header controls.

## Visual defect patterns the screenshot check should catch

- **Unconstrained injected SVG icons** — an SVG template injected into a button/link with no CSS size rule renders at the default replaced-element width (~300px), appearing as a giant black triangle. Fix with a component-scoped size rule (e.g. `.text-link svg{width:14px;height:14px}`), not by deleting the icon.
- **Overflow-x** — `scrollWidth > innerWidth` on mobile. Common culprit: a `margin-left:auto` metadata element (freshness/"last updated" indicator) pushed off the right edge. Fix with a `@media` rule making it `margin-left:0;width:100%`.
- **Duplicate mobile controls** — hiding only a toolbar's non-icon children while the parent toolbar stays visible leaves stray icon buttons beside a dedicated mobile header. Hide the whole desktop toolbar under the breakpoint instead.
- **Right-edge text truncation** — clipped text in a 390px shot usually shares the overflow root cause; re-measure after fixing rather than trimming the text.

## Vision-model screenshot review can produce overflow false alarms

When a vision pass on a mobile screenshot reports "horizontal overflow / clipped text", do not patch CSS based on that report alone. A headless `--window-size=390 --screenshot` image is not proof of a 390px CSS viewport (see top of this file), and elements intentionally scrolled horizontally (chip rails) or wrapped to a second row can read as "cut off" to a vision model. Measure first via CDP, then only fix what measurement confirms:

```js
window.innerWidth                                  // actual CSS viewport
document.documentElement.scrollWidth               // must be <= innerWidth when no overflow intended
getComputedStyle(document.querySelector('.genre-chips')).flexWrap  // wrapping rails are fine
nav element .getBoundingClientRect().right <= window.innerWidth    // nav visibility
```

In one session the vision review flagged overflow and undersized touch targets; CDP measurement showed zero overflow and correct wrapping — the only real fix was bumping chip/nav padding toward 44px touch targets. The measured numbers, not the visual impression, defined the fix.

## Scripted end-to-end flow test (single-page artifact)

For artifacts with a real multi-step flow (browse → select → form → submit → result), static checks and screenshots are not enough — drive the whole flow through one temporary Python script using `requests` + `websockets` against a throwaway Chrome instance:

1. Launch temp headless Chrome (`--remote-debugging-port`, unique `--user-data-dir`, `--force-device-scale-factor=1`), poll `/json` for the page's `webSocketDebuggerUrl`.
2. Enable `Page` + `Runtime`; wrap evaluation in a small helper returning `result.result.value` with `returnByValue: true`.
3. Drive each step with `Runtime.evaluate(...).click()` on real selectors, sleeping briefly between steps.
4. Assert per-step state as data: card counts, view-specific headings, disabled/enabled buttons, computed totals (`textContent` of the total node), validation error counts after an intentional empty submit, formatted input values after dispatching `input` events, localStorage contents after persistence actions.
5. This catches bugs invisible to screenshots: silent no-op submits, state lost on re-render, totals not recomputing, badges not updating.

Real catch from this pattern: a promo-code apply that re-rendered checkout wiped entered payment details, so Pay silently failed — every screenshot looked perfect. Also verify cleanup: kill the temp Chrome process in a `finally` block and delete probe scripts afterward.

## Interpretation

This is **ad-hoc browser verification**, not a production end-to-end test. Report the exact checks performed and preserve the distinction between an interactive prototype and a backend-connected product.

