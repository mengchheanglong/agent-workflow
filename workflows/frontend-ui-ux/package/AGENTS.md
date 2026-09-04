# Frontend / UI / UX Workflow

## Mission

Build, redesign, critique, and polish frontend interfaces — from full marketing sites to
single-component micro-interactions — by routing each request to the right specialized
design skill and executing through a scoped, evidence-backed workflow.

This workflow is agent-agnostic. Claude Code, Codex, or another capable engine may perform
a role, but the repository artifacts and gates remain authoritative.

## Instruction precedence

Apply instructions in this order:

1. the human's current explicit direction;
2. applicable repository `AGENTS.md` or `CLAUDE.md` rules;
3. product, architecture, security, data, and operations documentation;
4. the approved active design brief and material decisions;
5. existing source code and tests;
6. assumptions, which must be labeled and resolved when consequential.

Never let generic workflow text override project-specific product facts.

## Available skills

All skills live under `skills/` relative to this workflow's `package/` directory:

| Skill | When to use |
|-------|-------------|
| `web-design-engineer` | Full websites, dashboards, prototypes, major visual redesigns |
| `emil-design-eng` | Component polish, micro-interactions, UI craft, "feel" |
| `animate` | Web motion, transitions, scroll/entrance animations |
| `landing-page-design` | Conversion landing pages, marketing sites, copy + layout |
| `build-awwwards-quality-sites` | Premium/Awwwards-level cinematic marketing sites |
| `video-to-superprompt` | Video reference to detailed implementation brief |
| `tastemaker` | Anti-generic visual direction, reference grounding, "make it look good" |
| `better-layout` | Spacing, alignment, grouping, responsiveness, visual hierarchy |
| `interface-review` | UI diff / PR / regression review (interface quality) |
| `critique-screen` | Rendered-screen visual critique |
| `perception-laws` | Gestalt, Fitts's Law, Hick's Law, Jakob's Law for UI review |
| `popular-web-designs` | 54 real design systems (Stripe, Linear, Vercel) as HTML/CSS reference |
| `uxpeak-ux-ui-design` | UX audit/redesign (product/conversion psychology, Figma, ecommerce) |
| `standalone-html-ui-artifacts` | Portable self-contained HTML deliverables |
| `iterative-ux-review` | Screenshot to analyze to fix loop for refining existing UI |
| `skill-router` | Route ambiguous requests to the best skill |

## Skill routing

Use `skill-router` to determine which skill fits a request. The router ranks skills by
keyword match, phrase boosts, and explicit naming. For ambiguous requests, run:

```bash
python skills/skill-router/scripts/route_skills.py "<request>"
```

Then load the top-ranked skill with its full `SKILL.md` before acting.

### Fast routes (common patterns)

| Request pattern | Skill |
|-----------------|-------|
| "Build the frontend for X" / "redesign this page" / "dashboard" | `web-design-engineer` |
| "Make this component feel alive" / "micro-interaction" | `emil-design-eng` |
| "Add animations" / "scroll effects" / "page transitions" | `animate` |
| "Landing page" / "marketing site" / "conversion page" | `landing-page-design` |
| "Premium site" / "Awwwards" / "cinematic" | `build-awwwards-quality-sites` |
| "Extract from this video" / "recreate this site" | `video-to-superprompt` |
| "Make it look good" / "not generic" / "match this reference" | `tastemaker` |
| "Fix spacing" / "alignment" / "responsive layout" | `better-layout` |
| "Review this PR's UI" / "UI regression check" | `interface-review` |
| "Critique this screenshot" / "why does this look off" | `critique-screen` |
| "Why does this feel wrong" / "Gestalt" / "Hick's Law" | `perception-laws` |
| "Show me Stripe/Linear/Vercel patterns" | `popular-web-designs` |
| "UX audit" / "conversion review" / "ecommerce UX" | `uxpeak-ux-ui-design` |
| "Standalone HTML" / "portable artifact" | `standalone-html-ui-artifacts` |
| "Iterate on this UI" / "screenshot fix loop" | `iterative-ux-review` |

## Reference browsing

When the user needs inspiration or reference, use the curated URLs in `references/`:

- **UI Libraries:** `references/ui-libraries.md` — shadcn UI Kit and Atlassian are PRIMARY (go through these first). Magic UI, Aceternity, Uiverse, shadcn/ui are secondary.
- **Component Galleries:** `references/component-galleries.md` — 21st.dev, Refero, Design.md, Open Design, Neuform, TypeUI

These files contain URLs, descriptions, use cases, and installation commands for each source.

## Required startup sequence

Before editing:

1. read this file;
2. read `skills/skill-router/SKILL.md` for routing logic;
3. identify the target skill via fast route or router script;
4. read the target skill's `SKILL.md` in full;
5. read project-specific authority documents and nearby instructions;
6. inspect the repository baseline and pre-existing changes;
7. stop if conflicting with active work unless the human explicitly redirects.

## Workflow stages

```text
IDLE to ROUTE to RESEARCH to DESIGN to BUILD to VALIDATE to REVIEW to [FIX to VALIDATE to REVIEW] to DONE
```

### ROUTE
Determine the right skill. If ambiguous, run the router script and inspect top candidates.

### RESEARCH
Read the skill's references, inspect existing code, gather references (screenshots, URLs,
design systems). For video input, use `video-to-superprompt` first.

### DESIGN
Produce a design direction: layout, typography, color, spacing, motion. For landing pages,
include copy. For components, specify states and transitions.

### BUILD
Implement the smallest safe vertical slice. For browser artifacts, render and verify visually.
For component work, test in isolation first.

### VALIDATE
Run focused checks. For UI work, verify in browser (visual regression, responsive states,
interaction behavior). Record evidence.

### REVIEW
Independent review against the skill's quality criteria. Use `interface-review` for diffs,
`critique-screen` for rendered output, or `perception-laws` for cognitive review.

## Roles

- **Router** — selects the right skill via fast route or router script.
- **Designer** — produces visual direction, layout, and motion decisions.
- **Builder** — implements the smallest safe vertical slice.
- **Reviewer** — independently reviews against skill criteria.

One engine may perform several non-conflicting roles in sequence, but Builder and Reviewer
must use separate contexts.

## Validation evidence

A completion claim requires fresh commands run after the last product edit. Record for each command:

- exact command and working directory;
- exit code and PASS/FAIL result;
- relevant counts or assertions;
- warnings, skips, and limitations;
- confirmation that it ran after the last edit.

No fabricated output, remembered result, or agent summary is evidence.

## Code Review Rules

Review is a separate, read-only gate. The Reviewer must:

1. start from a fresh context independent of the Builder;
2. verify the exact base, current diff, allowed paths, and pre-existing changes;
3. apply the selected skill's review criteria;
4. inspect surrounding code and tests rather than reviewing the patch in isolation;
5. verify candidate findings before reporting them;
6. classify severity as BLOCKER, MAJOR, MINOR, or NIT;
7. cite exact evidence, failure scenario, impact, and required correction/proof;
8. avoid modifying product code during the authoritative pass.

## State authority

`.active/STATE.json` is the machine-checkable state. `.active/STATE.md` is the human-readable journal.
They must agree after every transition.

`.active/DESIGN_BRIEF.md` is the active design contract. `.active/DECISIONS.md` records material decisions.
`.active/REVIEW.md` is the latest authoritative independent review.

If these artifacts conflict, stop in `BLOCKED`, state the mismatch, and repair the records before
continuing product work.

## Adaptation

Replace generic validation examples with the repository's real commands. Add project-specific
design rules only for durable, consequential behavior. Keep deterministic formatting and lint
rules in scripts or CI rather than bloating AI review instructions.

Do not add more roles or process layers unless a real recurring failure proves they are needed.
