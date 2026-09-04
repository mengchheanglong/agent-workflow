# Vision corpus → Mission Control extraction

Use when the user points at a folder of personal vision/research files and asks the agent to understand what they are trying to achieve, then turn it into an executable project brain or Mission Control system.

## Trigger examples

- “Analyze all files here; this is my vision.”
- “Understand what I’m trying to achieve.”
- “Can we make a Paperclip/Mission Control for this?”
- Folder contains many PDFs/DOCX/diagrams/roadmaps rather than a runnable repo.

## Workflow

1. **Inventory without modifying the source folder**
   - Count files by extension and top-level folder.
   - Record total size, largest files, duplicates by hash, and unsupported/image-only documents.
   - Preserve source paths exactly.

2. **Extract to a Hermes-owned analysis cache**
   - Write extracted text and derived summaries under a profile-local knowledge folder, not into the user’s original source folder unless explicitly asked.
   - Suggested path shape:
     `C:/Users/User/AppData/Local/hermes/profiles/dev/knowledge/<topic>-analysis-YYYY-MM-DD/`
   - Create at least:
     - `inventory.json` — machine-readable records.
     - `inventory.md` — human-readable file capsules.
     - `VISION_SYNTHESIS.md` — durable synthesis and execution recommendation.

3. **Use mixed-format extraction**
   - PDFs: PyMuPDF text extraction; if a PDF has zero text, render representative pages to images and inspect visually.
   - DOCX: `python-docx` paragraph/table extraction.
   - HTML: parse text content where possible.
   - drawio/XML: extract visible labels from `value="..."` attributes.
   - SQL/text/code: read as plain text.
   - Images/screenshots: use vision analysis for meaning, not OCR-only assumptions.

4. **Synthesize into architecture, not a file-by-file summary**
   - Identify repeated concepts, acronyms, long-term goals, product candidates, learning paths, funding paths, and ethics/risk themes.
   - Separate:
     - long-horizon ambition;
     - near-term buildable proxy;
     - current proof target;
     - side products/funding routes;
     - research-only/watchlist domains.
   - Name the user’s intended role if it recurs (for example architect/operator/research director), because that shapes execution style.

5. **Convert to Mission Control**
   - Recommend a file-first Mission Control before building an app UI.
   - Proposed structure:
     ```text
     mission-control/
       AGENTS.md
       .active/{CURRENT.md,NEXT.md,STATE.json,DECISIONS.md}
       missions/<mission-name>/{MISSION.md,SPEC.md,TASKS.md,EVIDENCE-GATES.md,BUILDER-HANDOFF.md,REVIEW.md}
       contracts/{mission.schema.json,artifact.schema.json,evidence-pack.schema.json}
       templates/{mission.md,builder-handoff.md,evidence-report.md,review.md}
       evaluations/{golden-requests.md,smoke-cases.md,score-rubric.md}
     ```
   - Pick 1–4 candidate missions, but recommend one active mission only.
   - Every mission needs an evidence gate, not just a roadmap.

6. **Ground ambition without killing it**
   - Treat speculative end-states as horizon language, not near-term product claims.
   - Reframe the next build as a proxy that creates evidence toward the vision.
   - Example: “digital consciousness transfer” → near-term proxy “persistent AI avatar/digital twin with memory and world interaction.”

## Output style

Return a verdict-first synthesis:

- what was analyzed;
- the compressed vision statement;
- the architecture map;
- execution ladder;
- recommended active mission;
- where the synthesis artifact was saved;
- major risks/corrections.

Avoid dumping all file capsules into chat. Save detailed inventory to disk and summarize the durable insight.

## Pitfalls

- Do not write into the personal source folder during analysis unless requested.
- Do not treat many roadmaps as many simultaneous active projects.
- Do not promote speculative DCT/BCI/robotics claims as near-term deliverables.
- Do not let a Mission Control idea become a full SaaS/app build before the file-first version proves useful.
- Do not skip image-only PDFs or screenshots; render/analyze representative images when text extraction is empty.
