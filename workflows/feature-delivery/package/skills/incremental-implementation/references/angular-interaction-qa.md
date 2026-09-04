# Angular interaction QA: styled controls must prove behavior

Use this when polishing Angular dashboards, sidebars, Kanban boards, task drawers, or other UI that looks finished but may still be static.

## Durable lesson

A successful typecheck/build and polished screenshot do not prove an interactive UI slice works. For each visible control that looks clickable, verify the user-visible state change in the browser before saying it is done.

## Checklist

1. Inventory controls in the touched area: navigation rows, workspace/project switchers, `+` buttons, cards that look clickable, profile menus, tabs, filters, submit/cancel actions.
2. For every control, define the expected visible result:
   - active state changes;
   - breadcrumb/header changes;
   - list/table/card data filters;
   - panels/forms open and close;
   - created item appears and becomes selected;
   - route/page changes;
   - dropdown/menu appears and dismisses.
3. Browser-test each interaction, not just accessibility snapshots:
   - click the control;
   - refresh the snapshot/visual view;
   - confirm the expected text/count/state changed;
   - check the browser console for runtime errors.
4. If a form submit path is flaky, simplify the slice:
   - avoid relying on `ngSubmit` when a plain inline panel is enough;
   - wire explicit `(input)` value capture and explicit button handlers;
   - keep keyboard handling (`Enter`) for accessibility.
5. Beware stale dev servers:
   - if browser behavior does not match edited source and builds pass, check whether the port is served by an old process;
   - restart/kill the stale server or run the current repo on a fresh port;
   - verify against the known-current server before final reporting.
6. When the user asks to remove a UI area, remove the whole feature path, not just the visible text:
   - delete the template block and navigation entry;
   - remove the page key/route state and component properties/handlers that only supported it;
   - remove stale CSS selectors and responsive/mobile references;
   - scan for the exact visible strings and deleted symbols (`currentPage() === ...`, handler names, class names) before finalizing.
7. When the user says a profile/account card should “go straight to profile page,” do not preserve an intermediate dropdown/menu:
   - make the whole card navigate to the profile page/state;
   - remove menu state, menu template, `aria-expanded`, and dropdown styles;
   - add a simple profile view if the app has no existing destination;
   - browser-test the click lands on the profile page and does not open a menu.
8. For VS Code/Angular language-service diagnostics, treat canonical project commands as authoritative:
   - if `pnpm typecheck` and `pnpm build` pass but VS Code still shows unknown standalone imports/directives, report that the editor language service may be stale/misconfigured;
   - do not churn working imports solely to satisfy stale editor diagnostics without reproducing the issue in the canonical commands.

## Reporting rule

Do not claim an area is “functional” because it compiles or because controls are visible. Report interaction evidence, for example: “clicked School Project → breadcrumb changed to School Project and project cards changed,” “clicked + → creator opened,” “created Design Lab → sidebar row appeared and breadcrumb selected it.”
