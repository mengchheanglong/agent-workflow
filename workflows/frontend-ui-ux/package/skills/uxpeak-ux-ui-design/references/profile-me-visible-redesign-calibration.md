# Profile/Me visible redesign calibration

Session lesson from Digital Twin web/PWA Profile/Me redesign.

## Trigger

User asked to redesign a screen using UX Peak principles, then corrected the result with: “dont see much dif one the website”.

## Lesson

When the user asks for a redesign — especially with phrasing like “spectacular”, “world-class”, “UX Peak”, or “don’t see much difference” — do not only add a modest next-action card or copy-level hierarchy change. UX Peak principles still apply, but the redesign must be visibly obvious in the first viewport.

## Practical correction

For Profile/Me or personal dashboard screens, a stronger pass should usually include at least three visible structural/visual changes:

1. A new screen-level framing panel that tells the user what this screen is for.
2. A reworked identity/progression hero with different composition, not just tweaked metrics.
3. A dominant next-best-action card with clear CTA and support chips explaining why/effort/trust.
4. A visibly different layout rhythm, e.g. wider `max-w-*`, hero + side signal panel, or content grouped into a command-center flow.
5. Keep trust/ownership controls visible, but do not let them dominate the first action.

## Pitfall

A UX-correct but subtle change can still fail the user's request if the user is judging the live website visually. After implementation, open the exact URL and inspect a screenshot. If the old and new first viewport look broadly similar, push the redesign further before reporting completion.

## Verification language

For creative UI work, report both:

- functional verification: typecheck/lint/build when appropriate;
- visual verification: exact URL inspected and whether the difference is obvious.

Do not claim “redesigned” if the change is mainly text or a single extra card.