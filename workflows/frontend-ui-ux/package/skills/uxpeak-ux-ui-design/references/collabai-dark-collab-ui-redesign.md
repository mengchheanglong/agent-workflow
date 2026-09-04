# CollabAI dark collaborative-project UI redesign note

Session learning for future UX Peak-style collaborative/project-management screens.

## User direction that mattered

- User explicitly wanted the redesign to rely heavily on **Trello + Notion + ChatGPT** references.
- User wanted **dark theme as the main UI**, not a light UI with dark accents.
- Repeated instruction signaled that a subtle polish pass would be insufficient; the screen needed to look visibly different at first glance.

## Durable design pattern

For AI-powered collaborative project management products, combine the metaphors this way:

1. **Trello = execution surface**
   - Kanban columns with clear status groups.
   - Dense but readable task cards.
   - Drag/drop affordance and selected-card state.
   - Task detail drawer beside the board, not a modal unless mobile.

2. **Notion = workspace/database structure**
   - Project pages, task database/table view, document-like hierarchy.
   - Calm headings, whisper borders, generous row rhythm.
   - Tags/status pills and page tabs.
   - Keep metadata scannable rather than decorative.

3. **ChatGPT = AI action surface**
   - Prompt/composer should be prominent and recognizable.
   - Use example prompt chips: generate subtasks, summarize blockers, find risky deadlines.
   - Ask an easier screen question such as “What should this team do next?”
   - Avoid hiding AI behind a generic assistant card if AI is a selling point.

4. **Linear-style dark foundation**
   - Dark-native canvas, subtle grid/ambient gradients, translucent surfaces.
   - Semi-transparent borders and luminance stacking instead of heavy shadows.
   - Accent color reserved for active states, CTAs, selected cards, and AI affordances.

## UX Peak application

- Start with the screen question: avoid passive dashboards that only show counts. Reframe as a command center that helps the user decide the next action.
- The first viewport should show value: current focus, risk, team load, and AI composer.
- Use recognition over recall: avatars, status dots, tags, columns, prompt chips.
- Make the redesign visually obvious through composition, scale, and dark-native palette — not just minor color/token changes.

## Implementation/QA pattern

- Do not stop at a conceptual skin. If the user asks for “Trello/Notion level” or says the UI still looks horrible, make a visibly structural redesign: sidebar/workspace shell, project pages, board/database tabs, polished cards, drawers, and route-specific layouts.
- Use good libraries already in the project for interaction polish instead of custom-only CSS. In Angular CollabAI, `@angular/cdk` drag/drop stayed for Kanban and Angular Material `MatRippleModule` added tactile feedback to nav/buttons/cards.
- After redesigning, run typecheck/build.
- Open the live screen and use visual browser inspection, not just code review.
- Check each major route/screen: dashboard, board, task database, team, AI.
- Iterate on screenshot findings before reporting completion; user-visible defects count even when build passes.
- Fix visual regressions found in screenshots, especially:
  - Kanban columns overflowing behind the detail drawer; tune drawer width and column `minmax()` rather than accepting accidental clipping.
  - Database/table rightmost columns clipping beside the drawer; use fixed/table-layout columns, narrower detail panels, and ellipsis for tags.
  - Status/priority/tag pills wrapping awkwardly; set `white-space: nowrap` and give columns enough width.
  - Team/member tables clipping their status column in split layouts; give team tables their own compact column map instead of reusing generic table widths.
  - Tab counts rendered as raw text; style them as small badges.
  - Dark theme contrast for form controls and table metadata.

## Pitfalls from the CollabAI correction

- Avoid a giant “AI dashboard hero” as the default answer to every collaborative product UI. It can look gimmicky even if dark and high-contrast. For project-management products, the execution/workspace metaphor should lead: board, database, pages, team, and AI as an action layer.
- “Dark theme” is not enough. World-class dark UI needs hierarchy, restraint, balanced widths, clean metadata, tactile states, and no clipped/wrapped table content.
- A screen can pass typecheck/build and still be unacceptable. Browser screenshot QA is mandatory for UI-quality claims.
