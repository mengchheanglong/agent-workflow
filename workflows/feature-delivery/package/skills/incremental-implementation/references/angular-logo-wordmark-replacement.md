# Angular logo/wordmark replacement notes

Use when a user provides image/SVG brand assets and asks to replace an existing Angular app logo, especially in a sidebar/header.

## Workflow

1. Inspect every supplied asset before choosing one. If multiple files are attached, determine whether each is icon-only, full wordmark, light/dark background, or has excessive canvas whitespace.
2. For SVG attachments, if direct vision/image tools cannot read them, render them in the browser (file:// URL) and screenshot/inspect visually rather than guessing from the XML.
3. Commit/copy the selected asset under Angular's public asset path (usually `public/`) with a stable lowercase filename, e.g. `public/collab-ai-wordmark.svg`.
4. If the user says to replace “the icon and the name,” use a single `<img>` wordmark in the brand container instead of keeping separate icon + text nodes.
5. Update desktop and responsive/mobile brand markup together so old branding does not reappear at small breakpoints.
6. Search for leftover brand classes/assets/text (`brand-mark`, old PNG/SVG names, literal old app name nodes) and remove unused CSS/assets.
7. Verify with the canonical Angular check/build command and browser visual inspection of the exact touched area. Check console errors.

## CSS pattern for large-canvas wordmark SVGs

Some generated wordmark SVGs have a wide 16:9 canvas and lots of padding. Avoid displaying them tiny by sizing the image container and cropping with `object-fit: cover` / centered positioning:

```scss
.brand, .mobile-brand { display: flex; align-items: center; min-height: 52px; }
.brand-wordmark { width: 206px; height: 58px; display: block; object-fit: cover; object-position: center; }
```

Tune width/height against the actual sidebar width; verify visually rather than relying on the SVG viewBox alone.

## Iterative visual tuning

When the user gives short visual corrections like “too big,” “smaller,” “a bit left,” or “more left,” treat them as direct pixel-tuning instructions rather than a request for a new design proposal.

- Make one small CSS change at a time, then verify visually in the browser.
- Preserve the last accepted dimension when the user only asks for position, and preserve position when the user only asks for size.
- For sidebar-only nudges, scope the rule to the sidebar brand instead of the shared mobile/header wordmark, e.g. `.brand .brand-wordmark { margin-left: -14px; }`.
- Use modest increments: shrink by roughly 10–15% per “smaller” request, and move by roughly 6–10px per “more left/right” request unless the screenshot clearly needs more.
- Confirm the wordmark remains readable and not clipped after every adjustment.

## Pitfalls

- Do not assume the newest/first attachment is the right one; compare icon-only vs full wordmark variants.
- Do not keep both old text and new wordmark unless the user explicitly asks for that layout.
- Do not change unrelated brand surfaces when the correction names one area, e.g. “top left on the sidebar.”
- Do not remove favicons unless they are truly obsolete for the current request; if changing favicon, verify `src/index.html` points to the committed asset.
