# Menui dashboard UX pass — session record (2026-08)

Worked example of a universal-simplicity UX pass on a phone-first owner
dashboard (Next.js + Supabase, Tailwind, Phosphor icons). Kept here as
session-specific detail; the general rules live in the UX skill.

## Context

Menui (launched Telegram-first digital menu for Cambodian businesses). User's
brief: product must be usable by owners whose tech comfort is Facebook +
Messenger only — but explicitly NOT a dumbed-down mode: "I meant this product to
be used by everyone so it shouldn't compromise on modern looks either." The
public customer menu was already strong; the owner dashboard was the problem.

## What changed, per surface

### Overview
- "Draft"/"Live" → outcome words: "Hidden — customers can't see your menu yet" /
  "Live — customers can see your menu". Readiness blockers reworded with
  examples ("Add a category first — like Drinks, Food, or Dessert").
- One gold primary action per state: hidden → Publish + Preview; live →
  Share menu + View menu. Previously "View menu" (secondary) out-shouted Publish.
- Zero-count stats bar and Customer attention analytics render ONLY when the
  store is published. Pre-launch zeros read as failure; setup progress is the
  only honest metric pre-launch.
- Next-steps copy concrete: "Take a photo, give it a name and a price."

### Share
- Rebuilt around one QR hero card on the dark brand surface: EC-level H,
  margin 4, 512px (survives folding/stains; quiet zone baked into PNG download).
- Exactly ONE link field ("This is the link") replacing three competing URL
  fields that caused decision paralysis.
- Telegram/native share collapsed into one secondary card; print jargon renamed
  ("Print Table Tent & Counter Stand" → "Print a table sign") plus practical
  print guidance (2×2 cm minimum, don't fold across modules, test-scan first).

### Business (settings)
- Logo upload collapsed from two buttons (one disabled — read as broken) to one
  tap: choosing a valid photo submits immediately via `formRef.requestSubmit()`.
- Facebook/Maps URL fields moved behind "More contact options (optional)"
  `<details>`; Telegram + phone promoted as primary pair (`inputMode="tel"`).
- Slug field relabeled "Menu link ending" with plain explanation sentence.
- Visibility card: Live/Hidden + "Hiding is always safe — nothing is deleted."

### Menu
- "Sections" → "Categories" everywhere user-visible; URLs/props untouched
  (`?tab=sections` stays), so zero behavior change.
- QuickActionButton gained optional `text` prop rendering a short visible word
  (Show/Hide) next to the icon; icon-only eye/arrow rows required memorization.
- Drag-handle instructions replaced ("Tap a row to edit · use the buttons below
  it"); empty states teach with examples.

## Verification recipe

1. `pnpm check` (lint + strict TS + vitest + next build) green BEFORE dogfood.
2. Seed QA owner through the app's own script (`seed:test-owner`) using process
   env credentials; confirm email once via a service-role admin helper script.
3. Playwright at 390×844, isMobile, hasTouch, deviceScaleFactor 2; full-page
   shots of all five routes; judge each critically (overflow, truncation,
   hierarchy, tap targets).
4. Login through the real form (#owner-email / #password / submit-by-text).
   Cookie injection for @supabase/ssr chunked sessions bounced repeatedly —
   do not go down that path again.
5. Red "N Issue" overlay in shots = Next.js dev-tools badge
   (`data-next-badge-root`), dev-only; verify in DOM before treating as a bug.

## Commit discipline

Atomic commits per surface following the repo's new GIT-GUIDELINE.md:
feat(overview)…, feat(share)…, feat(settings)…, refactor(menu)…,
chore(scripts)… Revert the dev/build flip in next-env.d.ts instead of committing
it. PR to develop, never merge own PR.
