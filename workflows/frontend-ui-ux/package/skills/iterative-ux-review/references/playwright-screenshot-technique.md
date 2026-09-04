# Playwright Screenshot Script for UX Review

Use this script to capture deterministic screenshots at exact viewports for UX review.

```javascript
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const outDir = path.resolve(__dirname, '../../../agent-workflow/.active/evidence/<feature>');
fs.mkdirSync(outDir, { recursive: true });

async function capture(page, name) {
  const file = path.join(outDir, `${name}.png`);
  await page.screenshot({ path: file, fullPage: false });
  return file;
}

(async () => {
  const browser = await chromium.launch({ headless: true });

  // Desktop
  let ctx = await browser.newContext({ viewport: { width: 1440, height: 900 } });
  let page = await ctx.newPage();
  await page.goto('http://127.0.0.1:3000/<route>', { waitUntil: 'networkidle' });
  await page.waitForTimeout(500);
  await capture(page, '<feature>-1440x900');
  await ctx.close();

  // Mobile
  ctx = await browser.newContext({ viewport: { width: 390, height: 844 } });
  page = await ctx.newPage();
  await page.goto('http://127.0.0.1:3000/<route>', { waitUntil: 'networkidle' });
  await page.waitForTimeout(500);
  await capture(page, '<feature>-390x844');
  await ctx.close();

  await browser.close();
  console.log('Done');
})();
```

## Viewport Reference

| Viewport | Width | Height | Use |
|----------|-------|--------|-----|
| Desktop | 1440 | 900 | Primary review |
| Laptop | 1024 | 768 | Secondary check |
| Mobile | 390 | 844 | iPhone 14 Pro |

## Naming Convention

`<feature>-<viewport>.png` — e.g., `stores-list-1440x900.png`, `store-detail-390x844.png`
