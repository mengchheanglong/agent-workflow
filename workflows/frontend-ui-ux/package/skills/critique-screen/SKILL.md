---
name: critique-screen
description: Use when critiquing a rendered interface screen.
version: 1.0.0
author: Owl-Listener; adapted for Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [design-critique, screen-review, hierarchy, typography, color, affordance]
    related_skills: [interface-review, better-layout, perception-laws]
---

# Critique Screen

## Purpose

Run the full screen-critique workflow highlighted in the AIAs video. Review an actual rendered screen across seven dimensions and return one evidence-based, prioritized fix list.

This is a Hermes adaptation of Owl-Listener's `/critique-screen` command and its seven supporting critique skills from `https://github.com/Owl-Listener/designer-skills`.

## Use when

Use for a screenshot, Figma frame, live browser route, prototype, or other rendered interface when the user asks to critique, review, improve, or diagnose the screen.

Do not substitute source-code inspection for a visual critique. If no rendered artifact is available, request or produce one, or mark visual claims `Not verified`.

## Required evidence

Inspect the actual artifact with vision or a browser. Record the viewport or image dimensions when available. Every finding must identify visible evidence, user impact, and a specific repair. A dimension may pass; do not invent issues to fill the checklist.

## Seven review passes

Read the matching reference before each pass:

1. **Visual hierarchy** — `references/critique-visual-hierarchy.md`
2. **Brand consistency** — `references/critique-brand-consistency.md`
3. **Composition** — `references/critique-composition.md`
4. **Typography** — `references/critique-typography.md`
5. **Colour** — `references/critique-color.md`
6. **Affordance** — `references/critique-affordance.md`
7. **Information density** — `references/critique-information-density.md`

Review the dimensions independently before combining results so one early impression does not distort every category.

## Prioritize

- **P1 Critical** — breaks usability, accessibility, truthful brand behavior, or the primary task; fix before shipping.
- **P2 Important** — materially weakens comprehension, hierarchy, consistency, or responsiveness; fix in the current pass.
- **P3 Polish** — isolated craft improvement with limited task impact.

Deduplicate overlapping findings and assign each issue to the dimension that best explains its root cause.

## Output

```markdown
| Priority | Dimension | Evidence | User impact | Specific fix |
|---|---|---|---|---|
```

Conclude with:

- strongest dimension;
- weakest dimension;
- next three fixes in order;
- what was not verified.

## Verification

After changes are made, reopen the same route or artifact at the same representative viewport and verify each P1/P2 repair. Check keyboard focus, text wrapping, contrast, and the primary action when applicable.
