# Routing maintenance checklist

Use this when a session changes how strongly a tool/capability should be recommended.

## Trigger

Apply this checklist when a capability is:

- verified to work, but
- no longer the preferred default route, or
- better framed as a niche helper/substrate than a headline path.

## Required propagation surfaces

Update all of these together:

1. `SKILL.md` routing table entry
2. `references/skill-library.md`
3. `C:/Users/User/AppData/Local/hermes/profiles/dev/organizer/SKILL_LIBRARY.md`
4. the affected skill's own description and priority-rule wording
5. DK active memory (`CURRENT.md`, `NEXT.md`, `TASKS.md`, `HANDOFF.md`, `STATE.json`, `DECISIONS.md`) when the strategic next action changes
6. wiki/project-memory surfaces (`wiki/entities/...`, `wiki/log.md`, `wiki/index.md`) if they still present the old default

## Verification checklist

- Router wording no longer says "first" or implies default use unless that is still true.
- Organizer shortcut library matches the router.
- The underlying skill no longer overclaims priority.
- Active memory next-action text matches the new strategic stance.
- Machine-readable state files still parse after edits.
- Wiki/log/index describe the capability accurately: usable if true, but not over-promoted.

## Common pitfall

Do not stop after editing only the main router table. If the reference library, organizer library, underlying skill, active memory, and wiki still disagree, future sessions will reintroduce the wrong route.
