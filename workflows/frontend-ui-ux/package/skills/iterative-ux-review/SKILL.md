---
name: iterative-ux-review
description: Screenshot→analyze→fix loop for refining existing UI.
version: 1.0.0
author: Hermes Agent
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [ux-review, visual-qa, screenshot, iteration, polish, refinement]
    related_skills: [web-design-engineer, critique-screen, interface-review]
---

# Iterative UX Review

Use this skill when refining or polishing existing UI. The core pattern is a deterministic screenshot→analyze→fix loop — not memory, not assumptions, not "looks fine to me."

## Trigger

Load this skill when:
- User asks to "review the vision" or "make it perfect"
- User says "keep making changes until the UX/UI is perfect"
- User corrects visual quality ("this looks off", "not consistent", "fix this")
- After initial implementation, before declaring done
- When consistency with other pages matters

## The Loop

```
Screenshot → Analyze → Fix → Repeat
```

### 1. Screenshot

Capture the current state at target viewports:
- Desktop: 1440×900
- Laptop: 1024×768
- Mobile: 390×844

Use Playwright (headless) for deterministic screenshots. Store in `.active/evidence/<feature>/`.

```javascript
const { chromium } = require('playwright');
const browser = await chromium.launch({ headless: true });
const ctx = await browser.newContext({ viewport: { width: 1440, height: 900 } });
const page = await ctx.newPage();
await page.goto('http://127.0.0.1:3000/stores', { waitUntil: 'networkidle' });
await page.screenshot({ path: 'stores-list-1440x900.png' });
```

### 2. Analyze

Use `vision_analyze` to identify specific issues. Ask structured questions:
- Visual hierarchy: Does the eye flow where intended?
- Spacing: Consistent scale? Internal vs external spacing correct?
- Badge consistency: Same component style for all statuses?
- Responsive behavior: No overflow/clipping at any viewport?
- Touch targets: ≥44px on mobile?
- Empty/null handling: Dashes for missing data, not zeros?

### 3. Fix

Address ONLY the issues found. Do not expand scope. Do not "improve" unrelated elements.

### 4. Repeat

Screenshot again to verify the fix. Continue until no issues remain.

## Pitfall: Over-scoping

The user explicitly bounds the task. When the user says "you gone overboard" — stop, report status, and wait for direction.

Do NOT:
- Add unsolicited features or pages
- Restart servers or run browser automation unless asked
- Expand to "perfect" beyond what the user requested
- Modify unrelated components "while you're in there"
- Mark review gates PASS without actually doing the review

## Tools

| Tool | Use |
|------|-----|
| Playwright | Deterministic screenshots at exact viewports |
| vision_analyze | Structured issue identification from screenshots |
| computer_use | Interactive browser verification (login flows, dialogs, hover states) |
| terminal | Run dev server, typecheck, lint, build |

## Output Naming

Store screenshots in `.active/evidence/<feature>/` with descriptive names:
- `stores-list-1440x900.png`
- `store-detail-suspended-390x844.png`
- `merchant-view-1440x900.png`

## Verification Checklist

Before declaring done:
- [ ] Screenshots captured at all target viewports
- [ ] vision_analyze run on each screenshot
- [ ] Every identified issue fixed
- [ ] No new issues introduced
- [ ] typecheck + lint + build pass
- [ ] No horizontal overflow at any viewport
- [ ] Status badges consistent style
- [ ] Touch targets ≥44px on mobile
- [ ] Empty states handled (dashes, not zeros)
