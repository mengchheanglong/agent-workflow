# Angular logo asset replacement

Use when a user provides an image and asks to use it as the app logo in an Angular frontend.

## Checklist

1. Inspect the provided image before wiring it in.
   - Some PNGs that look transparent may contain a baked checkerboard background and no alpha channel.
   - If the mark is white/light, preview it on the app's actual dark/gradient background before accepting it.
2. Create committed assets under `public/` rather than referencing transient attachment paths.
   - Typical names: `public/<app>-logo.png` and `public/favicon.png`.
   - Remove temporary preview/debug images before finishing.
3. Update every visible brand surface in one slice.
   - Sidebar/desktop brand mark.
   - Mobile brand mark if present.
   - Browser favicon in `src/index.html`.
4. CSS expectations for small brand marks:
   - Put the image inside the existing brand tile if that matches the design system.
   - Use `object-fit: contain` and explicit width/height percentages so the mark remains legible at 32-40px.
   - Decorative logo images inside text brand labels should use `alt="" aria-hidden="true"`; keep the text app name as the accessible label.
5. Verification:
   - Run the canonical check (`pnpm check`, or typecheck + build for the repo).
   - Browser-load the app and visually inspect the logo in the actual sidebar/header.
   - Check the browser console for missing asset/404 errors.

## Pitfalls

- Do not use `.hermes/desktop-attachments/...` directly in app markup; teammates will not have that file after clone.
- Do not trust an apparent checkerboard as transparency. Verify the image mode/alpha or inspect on a dark background.
- Do not update only the large app logo and forget the favicon/mobile header.
