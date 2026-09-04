# Split Vision Corpus → Mission Control

Use when a user has a large folder of research/vision docs that has evolved into multiple branches, and they ask what is next or ask to organize it before executing.

## Lesson

Do not treat the entire corpus as the user's current canonical vision. Long-lived personal research folders often contain old roadmaps, experiments, speculative branches, and split visions. First organize and promote only the stable/current thread into active Mission Control.

## Workflow

1. State the correction explicitly: the corpus is an evolving/split vision corpus, not one canonical plan.
2. Build a `VISION-SPLIT-MAP.md` or equivalent before creating implementation tasks.
3. Classify branches:
   - current active branch;
   - stable core themes;
   - parked future branches;
   - reference-only old roadmaps;
   - speculative/research-only material.
4. Create/update `.active/CURRENT.md`, `.active/NEXT.md`, `.active/STATE.json`, and `DECISIONS.md` so future agents do not revive the wrong branch.
5. Only after the split map exists, create Mission Control tasks/specs for the current active branch.
6. If the user names an existing implementation path later, treat it as authoritative and repoint Mission Control immediately.

## Useful file shape

```text
.active/
  CURRENT.md
  NEXT.md
  STATE.json
  DECISIONS.md
  RESEARCH.md
  VISION-SPLIT-MAP.md
mission-control/
  missions/<active-mission>/
    MISSION.md
    SPEC.md
    TASKS.md
    EVIDENCE-GATES.md
    BUILDER-HANDOFF.md
    REVIEW.md
```

## Pitfall

Avoid answering “what should we build next?” directly from the whole folder. Answer from the promoted active branch in `.active/STATE.json` / Mission Control.
