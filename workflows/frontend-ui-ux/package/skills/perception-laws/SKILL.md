---
name: perception-laws
description: Use when applying perception laws to interface design.
version: 1.0.0
author: Owl-Listener; adapted for Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [perception, gestalt, hierarchy, interaction-design, ui-design]
    related_skills: [critique-screen, better-layout, web-design-engineer]
---

# Perception Laws

## Purpose

Apply the perception-law workflow highlighted in the AIAs video: use established visual and interaction principles to explain how people group, scan, remember, and acquire interface elements.

This is a Hermes routing layer over the relevant law skills in Owl-Listener's `https://github.com/Owl-Listener/designer-skills`. It is intentionally one recommended workflow, not an installation of the repository's full skill catalog.

## Route to the relevant law

Read only the references needed for the current problem:

| Problem | Law | Reference |
|---|---|---|
| Related elements do not read as a group | Proximity | `references/law-of-proximity.md` |
| Grouping must survive a dense layout | Common Region | `references/law-of-common-region.md` |
| A repeated category or relationship is unclear | Similarity | `references/law-of-similarity.md` |
| Eye flow, sequence, alignment, or path is unclear | Continuity | `references/law-of-continuity.md` |
| Borders create too much visual weight | Closure | `references/law-of-closure.md` |
| Foreground, background, modal, or overlay depth is unclear | Figure-Ground | `references/law-of-figure-ground.md` |
| One primary action must stand out | Von Restorff Effect | `references/von-restorff-effect.md` |
| Too many simultaneous choices slow decisions | Hick's Law | `references/hicks-law.md` |
| Important targets are too small or too far away | Fitts's Law | `references/fitts-law.md` |

## Workflow

1. Inspect the real screen, interaction, or code-backed layout.
2. State the observed user problem before naming a law.
3. Select the smallest applicable set—usually one to three laws.
4. Read those references and translate them into a concrete layout, spacing, hierarchy, or target change.
5. Preserve product conventions, accessibility behavior, and the user's approved scope.
6. Render and verify the change at representative widths and input methods.

## Guardrails

- Laws diagnose and constrain; they do not replace product evidence or user research.
- Do not cite a law merely to justify a personal style preference.
- Do not maximize every law simultaneously. For example, excessive common regions create box-heavy UI, and several Von Restorff exceptions destroy the intended focal point.
- Prefer spacing and alignment before adding borders or decorative containers.
- Reduce choice complexity before hiding essential options.
- Fitts's Law never overrides semantic structure, keyboard access, or safe touch-target spacing.

## Output

```markdown
**Observed problem:** ...
**Applicable law(s):** ...
**Evidence:** ...
**Change:** ...
**Expected user effect:** ...
**Verified:** ...
```

When reviewing rather than implementing, separate confirmed findings from hypotheses and state any missing rendered or behavioral evidence.
