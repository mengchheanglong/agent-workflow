---
name: skill-router
description: Route ambiguous frontend/UI/UX requests to the best design skill. Scoped to 16 design skills in this workflow.
version: 1.0.0
author: Frontend UI UX Workflow
license: MIT
---

# Skill Router

## Purpose

Route ambiguous frontend, UI, and UX requests to the best design skill from the 16 skills in this workflow.

## Trigger phrases

Load this skill when the user says any variant of:
- "give me your suggestion"
- "suggest" / "recommend"
- "what should I use?"
- "choose the best skill"
- "route this"
- "what now?"
- "use the right skill"
- "which skill for this?"

Also load it when the user gives a broad goal and does not name a specific skill.

## Core rule

Do **not** answer from memory if a relevant skill exists.

Procedure:

1. Parse the request into domain, artifact, verb, phase, constraints, and requested output.
2. If the user explicitly names a skill, verify that skill's scope.
3. Check the fast-route table below for a clear artifact-and-phase match.
4. When the route is broad or ambiguous, consult the design skills catalog in `references/design-skills-catalog.md`.
5. Load the plausible candidates and compare triggers, exclusions, deliverables.
6. Select one primary owner and at most two non-overlapping support skills.
7. If one route is obvious, act directly. If there is a real trade-off, give a short default recommendation and explain the alternative.

## Fast-route table

| User intent | First skill(s) to load | Default action |
|---|---|---|
| Build full website / dashboard / prototype / major redesign | `web-design-engineer` | Ground in references, lock visual system, implement, verify rendered |
| Component polish / micro-interactions / "feel" | `emil-design-eng` | Improve hierarchy, component behavior, invisible craft |
| Landing page / marketing site / conversion page | `landing-page-design` | One audience, one offer, one primary action; verify copy, SEO, layout |
| Premium / cinematic / Awwwards-style site | `build-awwwards-quality-sites` | Art-direct original imagery, restrained motion, verify a11y + performance |
| Extract design brief from reference video | `video-to-superprompt` | Inspect video, produce section-by-section superprompt with originality boundary |
| Anti-generic / "make it look good" / match reference | `tastemaker` | Lock palette, type, structure, assets, anti-slop gates |
| Add animations / scroll effects / transitions | `animate` | Decide purpose, choose cheapest mechanism, implement interruptible + reduced-motion-safe |
| Fix spacing / alignment / responsive layout | `better-layout` | Apply narrowest layout principle, verify on real screen |
| Review UI diff / PR / regression | `interface-review` | Resolve exact change scope, classify introduced/regression/pre-existing |
| Critique rendered screenshot | `critique-screen` | Review seven dimensions, rank P1/P2/P3 fixes |
| Why does this feel wrong / Gestalt / Hick's Law | `perception-laws` | Apply narrowest perception principle, verify on real screen |
| Show me Stripe/Linear/Vercel patterns | `popular-web-designs` | Reference real design systems as HTML/CSS |
| UX audit / conversion review / ecommerce UX | `uxpeak-ux-ui-design` | Reframe user question, reduce friction, strengthen trust |
| Standalone HTML artifact / portable prototype | `standalone-html-ui-artifacts` | Build self-contained HTML deliverable |
| Iterate on existing UI / screenshot fix loop | `iterative-ux-review` | Screenshot → analyze → fix → repeat |

## Skill composition rules

Choose:
1. one **primary skill** that owns the requested artifact and phase;
2. optionally one **specialist** for a distinct concern;
3. optionally one **verification skill** when the primary does not cover it.

Do not load several overlapping primary workflows. A landing page with motion is `landing-page-design` + `animate`; it is not every installed web-design skill.

## Reference browsing

When the user needs inspiration or reference, direct them to the curated URLs in `references/`:

- **UI Libraries:** `references/ui-libraries.md` — shadcn UI Kit and Atlassian are PRIMARY (go through these first). Magic UI, Aceternity, Uiverse, shadcn/ui are secondary.
- **Component Galleries:** `references/component-galleries.md` — 21st.dev, Refero, Design.md, Open Design, Neuform, TypeUI

## Supporting files

- `references/design-skills-catalog.md` — scoped catalog of the 16 design skills
- `references/ui-libraries.md` — curated UI component libraries with URLs
- `references/component-galleries.md` — curated component galleries and marketplaces
