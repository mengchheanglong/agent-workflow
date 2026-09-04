# Multi-page Static Community App Pattern

Use this reference when plain HTML/CSS/JavaScript must feel like a real product rather than a landing page, especially when the product includes evidence/news records, organizations, culture/editorial content, or a simulated community.

## Target architecture

Keep normal relative links and one HTML file per primary destination:

```text
app/
  index.html                 overview/dashboard
  evidence.html              durable records
  organizations.html         directory/profiles
  updates.html               dated change ledger
  community.html             discussions/events
  contribute.html            non-sending or real submission flow
  policy.html                editorial/safety rules
  about.html                 mission, boundaries, credits
  assets/
    app.css                  shared shell and responsive tokens
    data.js                  inspectable demo/seed data
    app.js                   shell, rendering, delegated interactions
    images/                  locally stored reviewed media
```

Add domain-specific routes such as `radar.html`, `culture.html`, or `roadmap.html` only when they answer distinct user jobs. Every navigation destination must map to a real page, unique `<title>`, unique `<h1>`, and `body[data-page]` value.

## Make it a working app, not a landing page

- Use a persistent desktop sidebar, compact sticky app header, route-specific actions, and content shaped around the current job.
- Make `index.html` an operational overview: changed records, attention items, saved collections, review state, or activity—not a marketing hero.
- Keep primary navigation stable. On phone, convert the sidebar to a drawer and expose only 3–5 daily destinations in bottom navigation.
- Use image-led context sparingly. A large photograph that consumes the first viewport pushes actual work below the fold and makes the page read like editorial marketing. Prefer a compact banner/card with records or discussions visible in the same viewport.
- Use the design system consistently across pages through shared CSS/JS. Normal `<a href="...">` links preserve direct-open and local-server behavior.

## Shared shell pattern

A dependency-free shared shell can be injected into placeholders such as:

```html
<body data-page="community">
  <aside id="sidebar"></aside>
  <header id="app-header"></header>
  <main id="main-content">...</main>
  <aside id="mobile-drawer"></aside>
  <nav id="bottom-nav"></nav>
  <script defer src="assets/data.js"></script>
  <script defer src="assets/app.js"></script>
</body>
```

Build navigation from one route table and mark the active route with `aria-current="page"`. Use delegated `data-action` events; do not use inline handlers. Keep demo mutations in memory unless persistence is explicitly authorized.

## Real-media provenance

When the user asks for real images:

1. Select official or permissively licensed sources; inspect the actual source page and reuse terms.
2. Download local copies so the prototype does not depend on hotlinks.
3. Resize/compress to web-friendly files and verify each file decodes.
4. Preserve a `docs/MEDIA_CREDITS.md` ledger containing subject, creator, source page, license link, and local processing.
5. Add accurate `alt` text and nearby context when an image could be misconstrued as evidence.
6. Never reuse photographed people as mock avatars or imply they are members, employees, researchers, or endorsers.
7. Avoid unreviewed copyrighted covers, screenshots, logos, and manga/anime art. Use textual culture records or licensed editorial context instead.

## Choose the community product mode before styling it

Do not assume every evidence/news product needs an evidence-gated forum. Identify the social job from the user's language:

### Evidence-review community

Use when the product's core job is source correction, claim review, expert Q&A, or editorial collaboration. Attach discussions to records, corrections, sources, organizations, or defined technical questions. General conversation is secondary.

### General-interest social community

Use when the user asks for Reddit/X-like discussion, general talk, fandom, world ideas, games, identity, hopes, or everyday conversation around the domain. Build a central social feed with:

- a compact post composer near the top;
- topic tabs and Reddit-like communities/spaces;
- aliases/handles, timestamps, post bodies, and category badges;
- X-like replies, reposts, likes, views, and bookmarks;
- trends and communities-to-explore in a secondary rail;
- optional evidence links for technical claims, not mandatory citations for casual talk.

A user correction such as “this should be like Reddit or X for general discussion” changes the **information architecture**, not just the visual styling. Remove evidence-first gates and oversized editorial imagery from the community route; keep evidence as one topic among several. The current prototype can still be local-only and fictional while demonstrating a credible populated social experience.

## Honest community simulation

A populated prototype may use realistic mock data, but the boundary must be visible:

- label community surfaces **Demo community data**, **Illustrative prototype data**, or equivalent;
- use invented aliases and generated initials, not real profile photos;
- include plausible posts, replies, reposts, likes/votes, saves, views, trends, topic communities, events, moderation outcomes, notifications, and collections;
- match the mock content to the selected community mode: record-linked review for an evidence community, or broad domain conversation for a general-interest social community;
- state that accounts, posts, counts, trends, spaces, events, and engagement are not live;
- for non-sending forms, say nothing is sent, uploaded, stored, or published and reset state on reload;
- do not let mock operational metrics appear as demand validation or external evidence.

## Verification matrix

### Static

- Assert the exact route inventory exists.
- Parse every HTML file: unique title/H1, correct `data-page`, internal script/style paths, valid linked page targets, non-empty image alt text, and no inline event attributes.
- Run `node --check` on shared JavaScript.
- Evaluate or parse the shared data layer and compare canonical evidence records record-for-record with the source dataset.
- Reject trackers, cookies, hidden persistence, `fetch`, XHR, or external scripts when the artifact promises local-only behavior.
- Decode every local image and preserve attribution.

### HTTP/browser

- Request every route and shared asset over the local server.
- For each route, assert exactly one active desktop destination, expected rendered-record count, and no horizontal overflow.
- Exercise global search, one data filter, one navigation path, one dialog/detail view, and one contribution preview.
- For a social community, also exercise a topic tab/filter, reply/detail open, like/vote, repost, save, and non-sending composer preview; assert each count/state changes exactly once and resets on reload.
- On phone, assert the desktop sidebar is hidden, the menu control is visible, the drawer opens/closes, bottom navigation has 3–5 destinations, and content reserves bottom safe-area space.
- Audit every visible `a`, `button`, `input`, `select`, and `textarea` at the phone viewport; each touch target should be at least 44×44 CSS pixels.
- Capture representative desktop and 390×844 screenshots and inspect them after numeric checks pass.
- Confirm zero fresh console errors.

## CDP pitfalls that matter for multi-page shells

- A page can contain two copies of navigation—desktop sidebar plus mobile drawer. Scope assertions to `.sidebar .nav-link` or `.mobile-drawer .nav-link`; do not assume a document-wide count equals the route count.
- Disable cache before fresh reloads after CSS/JS edits (`Network.enable` plus `Network.setCacheDisabled`). Otherwise CDP can measure the previous stylesheet even when files changed.
- Python `websockets.sync.client.connect` defaults to a 1 MB receive limit. CDP screenshots can exceed that; set `max_size=None` for trusted local Chrome sessions.
- After closing a CSS-transitioned drawer/dialog, wait or poll until the transition settles before screenshot capture. State attributes may already be closed while pixels still show the exiting surface.
- A basic static server may use a conservative MIME type for WebP. Verify HTTP success, file decode, and browser `naturalWidth`; do not reject an otherwise valid local image solely because the development server reports `application/octet-stream`.

## Common mistakes

- Keeping a marketing hero and merely adding sidebar links.
- Representing tabs as anchors on one long page when separate routes were requested.
- Allowing a real photograph to dominate the working surface or imply community membership.
- Hiding mock-data caveats in About instead of placing them next to the simulated activity.
- Treating a requested Reddit/X-like general community as an evidence-review forum; broad domain conversation is a distinct product mode, not a weaker evidence workflow.
- Testing only the overview page while promised destinations remain empty shells.
- Measuring only buttons and missing sub-44px anchor links in shared chrome.
- Capturing a screenshot immediately after a drawer closes and misdiagnosing the transition frame as a layout defect.
