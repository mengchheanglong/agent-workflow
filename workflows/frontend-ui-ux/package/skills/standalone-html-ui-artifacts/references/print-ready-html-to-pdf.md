# Print-ready Markdown/HTML to PDF workflow

Use this reference when a user wants a polished PDF from Markdown, a report, or another structured text source. The deliverable is a visually reviewed PDF, not a raw browser print.

## Output strategy

1. Keep generated PDF/build artifacts outside a source repository unless the user explicitly asks to track them. Prefer the user's Documents or requested export folder.
2. Convert the source into one self-contained HTML file with embedded CSS, system fonts, no required network assets, and preserved hyperlinks.
3. Render a raw PDF with a known Chromium executable or another deterministic HTML-to-PDF engine.
4. Post-process with PyMuPDF when useful for metadata, bookmarks, and restrained page furniture.
5. Verify structure, links, pagination, and representative rendered pages before delivery.
6. Remove temporary HTML, CSS, raw PDFs, and preview images after the final artifact passes.

## Print design defaults

- Use A4 unless the user specifies another paper size.
- Include a designed cover, concise contents page, clear section hierarchy, and a deliberate closing page when the final section is short.
- Use a restrained palette, system fonts, strong contrast, and comfortable body line-height.
- Keep links clickable; do not print raw URLs when descriptive link text exists.
- Use `@page` margins and `@page:first` for a full-bleed or distinct cover.
- Apply `break-after: avoid` to headings, `break-inside: avoid` to callouts/list items/table rows, and `thead { display: table-header-group; }` so table headers repeat.
- Use fixed table layouts and explicit column widths. About 8–9 pt can work for dense A4 tables if verified at full resolution; do not infer legibility from a thumbnail.
- Avoid forcing every top-level heading onto a fresh page. Forced breaks often create sparse carry-over pages. Start only major bands on new pages, render, then relax break rules where a preceding section leaves excessive whitespace.
- If a naturally short final page looks accidental, make it intentional with a closing decision standard or summary card derived from the source rather than padding it with new claims.

## Curated clickable directories and follow lists

When the PDF is a company/resource directory, curation quality controls the design quality. Do not polish a broad source list before proving that every entry belongs.

1. Restate the user's goal and define a concrete inclusion test. Useful tests include direct career access, repeated target-skill evidence, or a direct technical/scientific relationship to the long-term goal.
2. Remove institutions, regulators, generic prestige entries, weakly related companies, duplicate targets, and inactive or unverified profiles when the request is specifically for companies to follow.
3. Verify account identity in layers:
   - official-site social links first;
   - current profile title/content extraction second;
   - targeted web search for unresolved handles;
   - exclude rather than guess when identity or activity remains uncertain.
4. Prefer a focused official technical/team account over a noisy corporate or storefront feed when that better matches the user's stated purpose (for example, a cloud, AI research, or engine account).
5. Store the approved entries as structured data and assert unique company names and unique target URLs before rendering.
6. Make the entire visual card an `<a href="...">`, while also displaying the handle and a small action label. This produces a more usable PDF than linking only tiny handle text.
7. Keep category counts visible and make category navigation clickable when the user plans to follow every item.
8. Treat a scope correction such as “only entries related to my goal” as a content-model correction: regenerate the approved set and PDF rather than merely restyling the earlier broad list.

Final verification must establish exact set equality:

```text
approved_target_urls == final_pdf_external_uri_set
```

Check for both missing and extra URLs. HTTP success alone does not prove that a profile is the intended official account.

## Chromium rendering pattern

Use a local `file:///...` URL and a tracked Chromium executable. A typical headless invocation is:

```bash
"$CHROME" \
  --headless=new \
  --disable-gpu \
  --no-sandbox \
  --disable-dev-shm-usage \
  --allow-file-access-from-files \
  --run-all-compositor-stages-before-draw \
  --no-pdf-header-footer \
  --print-to-pdf="$RAW_PDF" \
  "$HTML_URL"
```

Use native Windows paths inside Python. Bash/MSYS paths are fine in shell commands, but `pathlib.Path('/c/...')` is not a native Windows path.

## PyMuPDF finishing

PyMuPDF can add:

- title, author, subject, keyword, creator, and producer metadata;
- a bookmark outline derived from source headings;
- small footers/page numbers in the bottom margin;
- rendered page previews for visual inspection.

Do not place footer text blindly. Check the raw PDF's maximum body-text bounding box first and reserve a footer zone below it. Skip footer furniture on a full-bleed cover.

When mapping headings to pages, skip the contents page; otherwise heading text in the contents can be mistaken for the real section destination.

## Verification gates

### HTML integrity

Check:

- doctype and embedded `<style>` exist;
- no unintended external scripts/styles/assets;
- expected section, table, and link counts;
- source guardrails and critical text remain present;
- no line-number prefixes or conversion artifacts entered the HTML.

### Raw PDF

Check:

- non-empty output;
- expected A4 dimensions on every page;
- no blank or nearly blank carry-over pages;
- repeated table headers and intact rows;
- total link annotations and text density by page;
- representative page samples to understand where sections landed.

### Final PDF

Check:

- metadata and bookmark count;
- every source URL appears in the PDF URI set;
- contents links resolve to concrete destinations;
- footer coverage and final page number;
- no body block enters the reserved footer zone;
- visual previews of at least the cover, densest table page, and closing page.

Chromium may encode internal contents links as named destinations rather than ordinary `LINK_GOTO` annotations. Verify `nameddest` plus a valid target page instead of assuming one link kind.

A useful URL-preservation gate is:

1. parse all Markdown `https://...` link targets into a set;
2. collect all PDF link annotation URIs into a set;
3. fail if `source_urls - pdf_urls` is non-empty.

## Visual review loop

1. Render a contact sheet of representative pages for whole-document rhythm.
2. Inspect high-resolution individual images for the cover, a dense table, and the final page.
3. Look for clipping, tiny text, row splits, repeated-header failure, awkward whitespace, inconsistent margins, weak contrast, and footer collisions.
4. Patch only the responsible print rule and rerender.
5. Re-run structural checks after every final PDF post-processing step.

Do not claim “clean PDF” from text extraction alone; visual inspection is required.