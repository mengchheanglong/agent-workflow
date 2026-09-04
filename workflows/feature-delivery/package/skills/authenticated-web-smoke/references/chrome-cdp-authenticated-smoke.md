# Dependency-light Chrome CDP smoke harness

Use this pattern when an authenticated browser smoke is required and a project-local automation package is unavailable or would be inappropriate to add as a dependency.

## Lifecycle

1. Locate an installed Chromium-family browser without changing project dependencies.
2. Launch it through Hermes as a **tracked background process** with:
   - headless mode;
   - a temporary, isolated `--user-data-dir`;
   - an explicit `--remote-debugging-port`;
   - `--remote-allow-origins=*` when the local CDP client requires it.
3. Wait for the `DevTools listening` log and verify `/json/version` before running the harness.
4. Start or reuse the app only after a real HTTP readiness probe. If a port is listening but requests hang, identify the owning process, confirm it is the stale app process, restart only that process, and repeat the readiness check.
5. Terminate the browser and app processes started by the smoke unless the user requested otherwise.

Do not use shell-level `&` to evade process tracking. Use Hermes background processes so readiness, logs, and cleanup remain observable.

## Minimal Node CDP client

Modern Node can drive Chrome directly with `fetch` plus the built-in `WebSocket` client:

- create a temporary page target through `/json/new`;
- enable `Page`, `Runtime`, `Network`, and `Log` domains;
- set desktop/mobile dimensions with `Emulation.setDeviceMetricsOverride`;
- navigate with `Page.navigate`;
- inspect state with `Runtime.evaluate`;
- capture evidence with `Page.captureScreenshot`.

A small request-ID map is enough to pair CDP responses with commands. Keep the harness in the OS temp directory, not the repository.

## Authenticated form flow

For controlled local/test credentials:

1. Navigate to the login page and wait for both DOM readiness and expected visible copy.
2. Set React-controlled inputs through the native `HTMLInputElement.prototype.value` setter.
3. Dispatch both `input` and `change` events with `bubbles: true`.
4. Submit through `form.requestSubmit()`.
5. Wait for the protected pathname and one page-specific anchor phrase; do not treat the submit click itself as success.

Never print credential values in the report or persist them in screenshots/log artifacts.

## Route matrix and assertions

For every route/viewport pair, record:

- expected section labels and whether each is present;
- pathname after navigation;
- page title or main heading;
- visible application error-state text;
- document-level horizontal overflow (`scrollWidth > innerWidth`);
- local-origin HTTP responses with status `>= 400`;
- local-origin `Network.loadingFailed` events;
- `Runtime.exceptionThrown`, error-level console calls, and error-level log entries;
- screenshot path.

Test the smallest meaningful matrix: major protected feature routes at desktop width plus the most layout-sensitive routes at a phone width. Filter network failures to the app origin so unrelated browser-service noise does not create false failures.

## Evidence and failure handling

Write one machine-readable JSON report containing the authenticated flag, browser identity, per-route results, screenshot paths, and a final failures array. Exit nonzero when any expected phrase is missing, the app shows an error state, local network/console errors occur, or page-level overflow appears.

If the first run fails because the tracked app/browser process ended or became stale, repair the lifecycle and rerun. Preserve the lesson as process/readiness discipline; do not encode a permanent claim that a browser tool is unavailable.
