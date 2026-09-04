# Frontend / UI / UX Workflow

A repository-local, agent-agnostic system for building, redesigning, critiquing, and
polishing frontend interfaces. Routes each request to one of 16 specialized design
skills via `skill-router`, then executes through a scoped, evidence-backed workflow.

## Install

Copy the contents of `package/` into your target repository root:

```text
target-repository/
├── AGENTS.md
├── REVIEW.md
├── .active/
│   ├── DESIGN_BRIEF.md
│   ├── STATE.md
│   ├── STATE.json
│   ├── DECISIONS.md
│   └── REVIEW.md
├── .agent/
│   ├── WORKFLOW.md
│   ├── QUALITY_GATES.md
│   ├── REFERENCES.md
│   ├── adapters/
│   ├── roles/
│   ├── templates/
│   ├── scripts/validate_workflow.py
│   └── tests/test_validate_workflow.py
└── skills/
    ├── web-design-engineer/
    ├── emil-design-eng/
    ├── animate/
    ├── landing-page-design/
    ├── build-awwwards-quality-sites/
    ├── video-to-superprompt/
    ├── tastemaker/
    ├── better-layout/
    ├── interface-review/
    ├── critique-screen/
    ├── perception-laws/
    ├── popular-web-designs/
    ├── uxpeak-ux-ui-design/
    ├── standalone-html-ui-artifacts/
    ├── iterative-ux-review/
    └── skill-router/
```

If the repository already has `AGENTS.md` or `.active/`, merge rules and state
surgically. Never overwrite project-specific policy or user work.

## Available skills

| Skill | Use when |
|-------|----------|
| `web-design-engineer` | Full websites, dashboards, prototypes, major visual redesigns |
| `emil-design-eng` | Component polish, micro-interactions, UI craft |
| `animate` | Web motion, transitions, scroll/entrance animations |
| `landing-page-design` | Conversion landing pages, marketing sites, copy + layout |
| `build-awwwards-quality-sites` | Premium/Awwwards-level cinematic marketing sites |
| `video-to-superprompt` | Video reference to detailed implementation brief |
| `tastemaker` | Anti-generic visual direction, reference grounding |
| `better-layout` | Spacing, alignment, grouping, responsiveness, visual hierarchy |
| `interface-review` | UI diff / PR / regression review |
| `critique-screen` | Rendered-screen visual critique |
| `perception-laws` | Gestalt, Fitts's Law, Hick's Law, Jakob's Law for UI review |
| `popular-web-designs` | 54 real design systems as HTML/CSS reference |
| `uxpeak-ux-ui-design` | UX audit/redesign (product/conversion psychology) |
| `standalone-html-ui-artifacts` | Portable self-contained HTML deliverables |
| `iterative-ux-review` | Screenshot to analyze to fix loop |
| `skill-router` | Route ambiguous requests to the best skill |

## Workflow stages

```text
IDLE → ROUTE → RESEARCH → DESIGN → BUILD → VALIDATE → REVIEW → [FIX → VALIDATE → REVIEW] → DONE
```

1. **ROUTE** — Use fast-route table or `skill-router` script to pick the right skill.
2. **RESEARCH** — Read skill references, inspect existing code, gather references.
3. **DESIGN** — Produce design direction: layout, typography, color, spacing, motion.
4. **BUILD** — Implement smallest safe vertical slice. Render and verify visually.
5. **VALIDATE** — Run focused checks. Verify in browser.
6. **REVIEW** — Independent review against skill criteria.

## Skill routing

For ambiguous requests, run the router:

```bash
python skills/skill-router/scripts/route_skills.py "<request>"
```

Then load the top-ranked skill's `SKILL.md` before acting.

## Validation evidence

A completion claim requires fresh commands run after the last product edit. Record for each command:

- exact command and working directory;
- exit code and PASS/FAIL result;
- relevant counts or assertions;
- warnings, skips, and limitations;
- confirmation that it ran after the last edit.

No fabricated output, remembered result, or agent summary is evidence.

## Adaptation

Replace generic validation examples with the repository's real commands. Add project-specific
design rules only for durable, consequential behavior.
