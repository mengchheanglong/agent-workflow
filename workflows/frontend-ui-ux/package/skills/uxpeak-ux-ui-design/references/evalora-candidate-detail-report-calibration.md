# Evalora candidate detail/report calibration

Session lesson: when the user provides candidate-detail and candidate-report screenshots, match the route role and information architecture before polishing cards.

## Route ownership

- Candidate list is the main navigation entry for candidate work.
- Do **not** keep a separate top-level `Candidates Reports` sidebar tab for the MVP; it is redundant with Candidates.
- Reports should be reached from candidate/session context, e.g. candidate detail `Report` tab/link -> `/reports/[sessionId]`.
- If a future product needs top-level report navigation, rename/reframe it as a review queue, not a generic candidate reports duplicate.

## Candidate detail target skeleton

Use a no-sidebar detail workspace when the reference shows only a compact topbar:

1. Compact topbar/search/profile only; no left app sidebar.
2. Breadcrumb: `Candidates > <candidate>`.
3. Small page title + short description.
4. Main grid: left content + right summary/actions column.
5. Profile hero card with avatar, name, active badge, role, contact details, candidate metadata, recruiter, tags.
6. Tabs should be only what the screenshot/product needs. In this case: `Overview` and `Report`; remove extra Sessions/Assessments/Notes/Files/Activity tabs when they make the first page redundant.
7. Overview cards: About Candidate, Skills, Latest Session.
8. Recent Activity card under overview cards.
9. Right column: Overall Summary score ring + strengths/improvements, then Quick Actions.

## Candidate report target skeleton

Use a no-sidebar report workspace:

1. Compact topbar/search/profile only; no left app sidebar.
2. Header: `Candidate Report`, one-sentence advisory description, back-to-candidate/report button.
3. Hero card: avatar, name, target role/assessment/status, score ring, recommendation badge, short AI synthesis note.
4. Compact report grid, preferably 4 columns on desktop when the reference shows 4 cards per row.
5. Cards: Core Competency Breakdown, AI Extracted Candidate Signals, Capability Map, Behavioral Pattern Analysis, Module Analysis, Evidence Extracted from Responses, AI Summary, Reviewer Notes.

## Implementation pitfall

When matching screenshots, verify visually after code changes. Typecheck/build passing is not enough: the first candidate/report implementation had the right data but the wrong navigation/skeleton. Browser-check exact routes and compare whether the sidebar, tab count, card grid, avatar, and primary layout match the screenshot at a glance.
