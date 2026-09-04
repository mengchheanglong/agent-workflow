# Coding workspace redesign calibration

Session lesson from Evalora candidate coding assessment UI.

## Trigger

Use this when a user says a coding assessment/workspace UI looks chaotic, not close enough to a reference, or too much like a generic product dashboard.

## What went wrong

A coding workspace became visually noisy because it mixed multiple competing design systems:

- outer assessment module chrome plus inner coding workspace chrome;
- big horizontal module/challenge cards plus a coding editor layout;
- a branded sidebar, progress card, badges, uppercase labels, and heavy active states all competing at once;
- large problem title/header, large editor buttons, and a harsh black editor block with strong borders;
- redundant instructional copy (`Introduction`, `How this works`, progress helper text) that did not help the candidate solve the problem.

## Better pattern

For coding-workspace screens, bias toward a calm IDE-like task surface:

1. Pick one navigation model only: either the parent assessment nav or an internal challenge rail. Do not make both visually dominant.
2. Use a compact internal challenge rail when multiple coding problems exist.
3. Keep the active challenge state calm: light tinted background, subtle border, no harsh black outline unless it is the product style.
4. Make the current problem and editor the only high-priority regions.
5. Remove explanatory copy unless it directly affects the next action.
6. Prefer small utility buttons in the editor toolbar (`Reset`, `Run`, `Submit`) and one clear footer CTA.
7. Balance columns by task: problem/test cases readable on the left, editor/terminal stable on the right.
8. Browser-check the exact screen and compare screenshots; if the first impression is still card-heavy or dashboard-like, simplify further.

## Quick audit questions

- Can the user immediately identify the current challenge and start coding?
- Are there more than two navigation systems fighting for attention?
- Are badges/progress cards/header labels louder than the problem or editor?
- Does the active state look selected without looking aggressive?
- Is helper text necessary, or is it product-theater copy?
- Are challenge labels fitting without truncation?
