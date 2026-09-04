# Hackathon Evidence + Business Research Capture Pattern

Use when a hackathon project is actively collecting testing data, competitor prices, business resources, prior-winner decks, or teammate research before the final pitch deck/script is ready.

## Trigger signals

- User says to “note this down,” “we will redo slides later,” “not yet,” or “need more info first.”
- User provides competitor prices, senior/prior-winner decks, business templates, BMCs, or teammate PDFs.
- User asks for testing advice while the physical prototype is still changing.

## Operating rule

Do **not** immediately rewrite the final slide deck/script just because new research arrived. First preserve the source, extract useful lessons, and write a data-needed checklist. Only produce the final deck/script after prototype results + cost + competitor + customer evidence are available.

## Recommended folder layer

Inside the human-readable project folder, add a topic folder such as:

```text
09-COMPETITOR-AND-SENIOR-DECK-RESEARCH/
  README.md
  01-SOURCE-INDEX.md
  02-PRIOR-WINNER-DECK-LESSONS.md
  03-COMPETITOR-RESEARCH-NOTES.md
  04-BMC-REVIEW.md
  05-DATA-NEEDED-BEFORE-SLIDE-REDO.md
  LOCAL-COMPETITOR-PRICE-CHECK-YYYY-MM-DD.md
  LOCAL-COMPETITOR-PRICE-CHECK-YYYY-MM-DD.csv
```

Keep raw extractions under:

```text
90-TECHNICAL-REFERENCE/<topic>-extraction/
```

## What to extract from a prior-winner/senior deck

Capture:

- story arc / slide order;
- validation style and numbers;
- competitor matrix style;
- business model and pricing model;
- TAM/SAM/SOM assumptions;
- traction/roadmap evidence;
- team/advisor credibility;
- appendix/Q&A backup structure;
- weaknesses to avoid, including typos, overloaded slides, and unsourced market math.

Write this as reusable lessons for the current project, not a full transcript.

## Competitor price capture pattern

For each competitor item, save:

```text
category, brand/source, product, pack quantity, pack price, unit, unit price, directness, notes
```

Always calculate unit price. Then write a short strategic interpretation:

- cheapest conventional benchmark;
- eco-alternative range;
- close local analog/plant-fiber benchmark;
- what the current project should **not** claim yet.

Example safe line:

```text
Foam is still the cheapest benchmark. We should not claim cheaper-than-foam until our real unit cost is measured; position against eco/event/story-driven alternatives first.
```

## Testing evidence capture pattern

For physical material prototypes, tell the team to capture:

- photos as main slide evidence;
- short 5–10 second videos as proof/backup, not long pitch content;
- formula, time/temperature, thickness, appearance, water/oil/load/drop/food-test notes;
- failed samples as iteration evidence.

For a 5-minute pitch, photos + result notes usually beat long videos. Keep videos for backup/Q&A or a 10–15 second montage.

## Material-cost estimation pattern

For physical prototypes made from agricultural residue or craft materials, separate **known material cost**, **estimated residue cost**, and **non-material costs**.

Capture:

```text
ingredient, amount used, source price, unit conversion, calculated unit cost, status, notes
```

Rules:

- Always label whether the number is **material-only**; exclude energy/labor/reject rate unless explicitly calculated.
- Keep two cost views when useful:
  - `prototype/local-small-purchase estimate` — what the team actually paid in small quantities;
  - `bulk/source potential estimate` — what the material could cost at scale using sourced bulk prices.
- For volume-only inputs such as tablespoons/spoons, use web research for plausible bulk density ranges, then clearly mark them as estimates.
- For agri-residue inputs, search for both local availability/price and physical-property sources: density, kg/ton price, residue generation, and common uses.
- Save the detailed calculation in a human-facing project file and a CSV; add a one-paragraph business summary separately.
- Highlight cost drivers. If one additive/coating dominates cost, flag it as an R&D/business decision rather than hiding it in the subtotal.

Safe pitch line pattern:

```text
Our current material-only estimate is around <range> before energy and labor. The biggest cost driver is <ingredient/process>, so we will update the model after measuring <missing conversions> and drying energy.
```

Do not claim cheaper-than-competitors until energy, labor, reject rate, and real measured material weights are included.

## Slide redo gate

Only redo final deck/script when this minimum set exists:

```text
prototype result + cost estimate + competitor prices + at least some customer feedback
```

Until then, maintain placeholders and data checklists.

## Pitfalls

- Do not turn every source into a dense command center; keep human-facing notes short and action-first.
- Do not bury competitor prices without unit-price conversion.
- Do not mix direct food-packaging competitors with indirect local-paper benchmarks without labeling them.
- Do not claim “first,” “no competitors,” “waterproof,” “food-safe,” or “cheaper than foam” unless proven.
- Do not spend 5-minute pitch time on long process videos; use photos and one short proof clip if needed.
