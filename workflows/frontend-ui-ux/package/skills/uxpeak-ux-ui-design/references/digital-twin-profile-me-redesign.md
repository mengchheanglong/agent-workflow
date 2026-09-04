# Digital Twin Profile/Me UX Peak Pattern

Session pattern from redesigning `C:/Users/User/archive/retired/digital-twin` Profile/Me screen.

## Screen question shift

Weak Profile/Me screens ask:

> “Here are your stats and settings.”

Better UX Peak framing asks:

> “What should I do next, and can I still manage my data safely?”

For personal-intelligence / habit / quest apps, Profile/Me should not be only identity + metrics + settings. It should include one context-aware next action before secondary management sections.

## Recommended hierarchy

1. Identity/progression summary
   - name, level, XP progress, a few honest metrics
   - level-detail card/header can be clickable if discoverable and accessible
2. Next-best-action card
   - one primary CTA
   - copy explains why this action helps now
   - no fake urgency/progress
3. Momentum/metrics overview
   - compact, low-decision effort
4. Quick routes / settings
   - secondary destinations only
5. Data ownership
   - export and erase controls remain visible and intentional

## Action selection rule

For Digital Twin-like apps:

```text
if no real daily baseline / no meaningful data:
  CTA = Check in now
  message = create today's baseline before reviewing patterns
elif open quests > 0:
  CTA = Open quests
  message = continue the smallest unfinished step
else:
  CTA = View insight
  message = review today's pattern before adding more work
```

Pitfall: do not send a brand-new or no-data user to “insights” just because there are zero open quests. That creates a misleading “all clear” state before the app has earned any value. Treat no baseline/no meaningful activity as an onboarding/value-first state.

## Trust placement

Keep data export and erase controls visible after the next-action card. Add reassurance copy that these controls remain available, but do not let privacy/settings become the first thing the screen asks the user to manage.

## Verification style

For creative UI work:

- visually inspect the screen in a browser/mobile viewport after implementation;
- typecheck/lint/build when ready to commit or when a small compile check is useful;
- if full tests fail outside the touched screen, report that as a blocker/out-of-scope rather than claiming suite green.
