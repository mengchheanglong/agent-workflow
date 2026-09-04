# Hermes Skill Library Index

This is the curated fast-route index for the user's installed Hermes skills. It does not attempt to list every skill. The generated complete inventory is in `references/skill-catalog.md` / `.json`; use `scripts/route_skills.py "<request>" --top 8` when the fast routes do not clearly resolve the request, then load plausible candidates with `skill_view`.

## Trigger phrases

When the user says any of these, load `skill-router` first:

- “give me your suggestion”
- “suggest” / “recommend”
- “what should I use?”
- “choose the best skill/tool”
- “route this”
- “what now?”
- “use the right skill”
- “pick the workflow”

## Top-level domains

### Hermes / DK / orchestration

- `hermes-agent` — configure, extend, troubleshoot Hermes itself.
- `directive-kernel` — DK/Jarvis capability kernel operation.
- `resume-dk-active-work` — resume DK from `.hermes/active/`.
- `close-dk-session` — close/sync DK active memory and wiki/log.
- `skill-router` — choose the right skill/workflow/tool.
- `skill-router-maintenance` — update `skill-router`, the skill library, and organizer docs when skills or routing defaults change.
- `computer-use` — drive desktop and browser UI in the background; capture first, act by semantic element, and verify every mutation.
- `autonomous-ai-agents` — orchestrate independent coding-agent processes and parallel workstreams.
- `kanban-codex-lane` — run Codex as an isolated implementation lane while Hermes owns durable task lifecycle and verification.
- `project-second-brain` — design file-first AI second brains for projects: AGENTS.md routing, `.active/` state, evergreen context, references/wiki/archive, and selective vector/graph layers only when pain justifies them. Organizer reference: `C:/Users/User/AppData/Local/hermes/profiles/dev/organizer/PROJECT_SECOND_BRAIN_STANDARD.md`.
- `context-engineering` — curate context/rules/spec/source files.
- `cost-aware-execution-router` — pick cheap/effective execution route.
- `model-task-router` — choose model/agent by task type.

### Coding / implementation / review

- `codex` — orchestration, task management, review, and DevOps/test/ship control.
- `claude-code` — available only when explicitly selected for a task.
- `opencode` — retired for this user; do not route new work to it.
- Worker policy: Grok 4.5 for implementation. DeepSeek API is prohibited. No alternate worker is chosen without the user's explicit direction.
- `github-pr-workflow` — branch/commit/push/PR/CI/merge.
- `github-code-review` — review PRs/diffs.
- `github-issues` — create/triage/manage GitHub issues.
- `github-repo-management` — clone/create/fork/releases/remotes.
- `systematic-debugging` — root-cause debugging.
- `test-driven-development` — RED/GREEN/REFACTOR.
- `incremental-implementation` — thin slices with tests.
- `spec-driven-development` — PRD/spec before code.
- `writing-plans` / `plan` — implementation plans.
- `requesting-code-review` — pre-commit review gates.
- `repository-consolidation` — combine repositories into a monorepo or umbrella workspace while preserving history, rollback, and path-dependent tooling.
- `dogfood` — exploratory browser QA with evidence.
- `authenticated-web-smoke` — authenticated owner/admin login and gated CRUD smoke tests.
- `stateful-web-admin-qa` — verify state-changing web/admin workflows and persistence.
- `web-form-flow-debugging` — diagnose auth, server-action, alternate-submit, and phone-first form failures.
- `web-app-ux-pass-verification` — implement or verify a focused UX pass in a real web app.
- `menui` / `menui-dashboard-ux` — Menui repository, git-flow, form, copy, and UI rules.
- `evalora` — Evalora assessment repositories and product constraints.
- `codewave` — CodeWave checks, tests, and error-UX.
- `simplify-code` — multi-agent cleanup of recent code.
- `doubt-driven-development` — adversarial review of decisions.
- `subagent-driven-development` — execute plan with subagents.
- `workflow-reference-evaluation` — evaluate external agent/workflow repos as donor/reference systems, extract only the parts worth importing into Hermes or the user's workflow, and route improvements to the right landing zone.
- `superpowers-workflow` — use obra/superpowers as a repo-specific workflow reference for planning, subagents, review, testing, and capability-control validation on a repo the user actually cares about.

### Research / finding information

- `online-presence-research` — people/company/org online research.
- `external-validation-research` — validate that a real external problem, solution category, and project-specific pull exist before recommending a build.
- `grounded-citations` — produce claims backed by cited, verifiable sources.
- `last30days` — research what people currently say across Reddit, X, YouTube, TikTok, Hacker News, GitHub, Polymarket, and the web.
- `literature-access` — DK-projected Scientify Literature Access for academic/technical paper search, OpenAlex/arXiv metadata, and DOI/open-access lookup; use before generic web search for literature questions.
- `arxiv` — arXiv paper search fallback or arXiv-specific helper.
- `blogwatcher` — RSS/blog monitoring.
- `polymarket` — markets/prices/orderbooks.
- `llm-wiki` — build/query interlinked markdown KB.
- `youtube-content` — transcripts/summaries/threads/blogs.
- `web-research` — three-stage pipeline: web_search → web_extract (sample 5) → web-crawl (best 1-3). Use for research questions, fact-finding, data gathering. Never deep-crawl without sampling first.
- `simulation-router` — umbrella router for simulation requests. Chooses deterministic rubric, MiroFish, CAMEL/OASIS, future sources, or combined pipelines based on decision frame, stakeholder/social-reaction need, cost, and artifact gates. Skill UX on top; CC should own validated adapters/contracts when implemented.
- `scenario-simulation-evaluation` — source-specific operations for MiroFish and CAMEL/OASIS second-opinion runs; compare against research baseline and do not treat simulated verdicts as ground truth.
- `research-simulation-workflow` — generic source-planning + evidence gathering + GitHub/tooling research + simulation routing + rubric scoring + confidence calibration workflow for strategy reports and option ranking.
- `web-crawl` — deep recursive web crawl via DK-projected Crawl4AI. Use for multi-page extraction with depth/page limits. Single-page fallback: web_extract.
- Hermes tools: `web_search`, `web_extract` for broad/current web research.
- DK local: `recent_research_brief` for exact GitHub repo/source-candidate evidence.

### Documents / productivity

- `report` — produce concise but comprehensive status/technical reports with verdict, changes, improvements, evidence, limits, and next action.
- `document-to-action-items` — extract cited obligations, deadlines, and tasks from documents.
- `docx` — create, read, and edit Word documents and templates.
- `xlsx` — create, read, and edit Excel workbooks and CSVs.
- `pdf` — create, merge, split, fill, and secure PDFs.
- `outbound-communication-operations` — send email/messages only within approved scope and verify delivery.
- `linear` — manage Linear issues, projects, and teams.
- `interview-assessment-design` — create role-based assessments, question banks, rubrics, and benchmark-backed hiring evaluations.
- `markitdown` — capability-control MarkItDown first for local PDFs/docs → Markdown, but treat cc as **refactor-first** truth layer after the 2026-06-17 stress test: live invoke/verify + artifact validation beats trusting stale command/catalog state; DK projection fallback; direct Python/raw or `web_extract` when cc is unavailable or clearly worse (e.g. public URLs).
- `scrapling` — niche helper for selector-based HTML extraction from inline HTML, local files, or safe public HTML URLs; do not treat as a general research/browsing path.
- `ocr-and-documents` — OCR/scanned PDFs.
- `nano-pdf` — edit PDF text/typos/titles.
- `powerpoint` — create/read/edit PPTX.
- `google-workspace` — Gmail/Calendar/Drive/Docs/Sheets.
- `notion` — Notion API/CLI.
- `airtable` — Airtable records CRUD/filter/upsert.
- `maps` — geocode/routes/POIs/timezones.
- `himalaya` — terminal email IMAP/SMTP.
- `teams-meeting-pipeline` — Teams meeting summaries.

### Business

- `simpleweb-kh` — SimpleWeb KH Facebook web-design business direction, prompts, pricing, content.
- `founder-thinking-mode` — direct founder-mode stress tests, hard calls, and pursue/park decisions.
- `question-first-product-analytics` — derive KPIs and dashboards from atomic business decisions and questions.
- `stakeholder-product-requirements` — synthesize stakeholder context and decisions into a copy-ready PRD.
- `hackathon-competition-playbook` — hackathon/startup idea selection, proof, storytelling, Q&A, and postmortems.
- `live-pitch-scripting` — turn evidence and transcripts into a natural founder-led spoken pitch.
- `social-commerce-trust-systems` — design trust, order, payment-proof, and reputation layers for social commerce.
- `unipreneur-season4-form` — UniPreneur Season 4 idea critique and submission-form helper; checks locked category fit, Rule of ONE, Cambodia-first evidence, and judge-safe wording.

### Creative / design / media

- `web-design-engineer` — reference-grounded workflow for polished browser pages, dashboards, prototypes, slide-like artifacts, and major visual redesigns; includes implementation and browser acceptance checks.
- `emil-design-eng` — UI component craft, polish, interaction decisions, and the invisible details that make software feel deliberate.
- `landing-page-design` — conversion-focused landing-page intake, structure, copy, SEO, typography, spacing, hero, icons, and motion rules.
- `animate` — purpose-gated workflow for implementing or refining UI motion and micro-interactions; includes reusable recipes.
- `build-awwwards-quality-sites` — premium, cinematic, motion-led marketing/editorial/portfolio sites with original art direction, GSAP choreography, accessibility, performance, and static fallbacks.
- `video-to-superprompt` — inspect a reference video and produce an evidence-backed, section-by-section recreation or inspiration brief.
- `tastemaker` — anti-generic, on-brand visual direction from real references, deterministic palettes, structural diversification, asset curation, and mechanical anti-slop checks.
- `interface-review` — review the interface impact of an exact diff, branch, or PR and classify introduced, regression, and pre-existing findings.
- `better-layout` — targeted spacing, grouping, alignment, reading-order, breakpoint, safe-area, and adaptivity guidance.
- `critique-screen` — review a rendered screen across hierarchy, brand, composition, typography, colour, affordance, and information density, then prioritize P1/P2/P3 fixes.
- `perception-laws` — route UI grouping, eye-flow, focal-point, choice-count, and target-acquisition problems to the relevant perceptual law.
- `popular-web-designs` — named real-world visual vocabularies such as Apple, Linear, Stripe, and Vercel; use only when the user requests a named style rather than as the default design workflow.
- `standalone-html-ui-artifacts` — build and verify portable standalone HTML prototypes and demos.
- `claude-design` — one-off HTML landing/deck/prototype artifact.
- `sketch` — throwaway HTML variants for direction comparison.
- `uxpeak-ux-ui-design` — product/conversion/ecommerce UX audit and redesign through psychology, hierarchy, trust, and friction reduction.
- `phone-first-pwa-ux` — phone-first PWA/mobile UX direction and implementation gates.
- `simple-universal-ux` — simplify interfaces for non-technical or elderly users.
- `copywriting-agent-workflow` — professional audience-aware copy with research, framework choice, drafting, and review.
- `humanizer` — remove AI-writing tells and restore a natural voice.
- `design-md` — author, validate, and export DESIGN.md token specifications.
- `pretext` — text/ASCII/typographic browser demos.
- `architecture-diagram` — dark SVG architecture diagrams.
- `excalidraw` — hand-drawn diagrams.
- `baoyu-infographic`, `baoyu-comic`, `baoyu-article-illustrator` — visuals/knowledge comics/article art.
- `ascii-art`, `ascii-video` — ASCII generation/conversion.
- `pixel-art`, `p5js`, `manim-video`, `comfyui`, `touchdesigner-mcp` — visual generation/creative coding.
- `songwriting-and-ai-music`, `heartmula`, `songsee`, `gif-search`, `spotify` — music/audio/GIF/media.

### UI component systems

- `shadcn-ui-components`
- `react-bits-components`
- `daisyui-components`
- `react-bootstrap-components`
- `tremor-dashboard-components`

Use these when building or specifying React/Tailwind/dashboard UI. Pick based on stack and desired style.

### Data science / ML / MLOps

- `data-analytics` — decision-first data analysis; hard-stop vague requests before computation.
- `jupyter-live-kernel` — iterative Python/Jupyter.
- `huggingface-hub` — HF search/download/upload.
- `llama-cpp` — local GGUF inference.
- `segment-anything-model` — image segmentation.
- `dspy` — declarative LM programs/RAG optimization.
- `weights-and-biases` — experiments/sweeps/registry.

### DevOps / automation / systems

- `windows-system-diagnostics` — Windows disk/memory/CPU/I/O performance.
- `local-agent-runtime-operations` — operate and recover local AI runtimes, gateways, pairing, and channels with end-to-end verification.
- `container-host-network-debugging` — diagnose container-to-host endpoint identity, port ownership, protocol, and readiness failures.
- `webhook-subscriptions` — event-driven agent runs.
- `quantum-free-router` — free LLM fallback router.
- `opencode-model-audit` — retired; historical recovery documentation only, never a default route.
- `native-mcp` — MCP servers/tools.
- `hermes-s6-container-supervision` — Hermes Docker s6 services.

### Cybersecurity

- `security-checklist` — security hygiene.
- `online-identity-removal` — privacy cleanup for social-profile impersonation, duplicate accounts, recovery, and evidence-safe takedowns.
- `unbroker` — autonomous data-broker removal.
- `windows-installer-extraction` — inspect Windows installer packages without executing them.
- `safeline-waf` — WAF/reverse proxy.
- `wazuh-xdr-siem` — Wazuh SIEM/XDR.
- `x64dbg-debugger` — Windows debugger/reversing.
- `cybersec-ai-skills` — broad ATT&CK/NIST cybersecurity skills.

### Smart home / games / integrations

- `openhue` — Philips Hue.
- `pokemon-player` — play Pokémon via emulator/RAM reads.
- `yuanbao` — Yuanbao groups.

## Default recommendation algorithm

1. If user mentions DK/Jarvis/capability/active state → load `directive-kernel` + `resume-dk-active-work`.
2. If user mentions Hermes setup/config/skills/tools/models/MCP/gateway → load `hermes-agent`.
3. If user asks for “suggestion” and the task is code → load `model-task-router` + `cost-aware-execution-router`; Codex controls orchestration/review/DevOps and verified `xai-oauth` / `grok-4.5` performs bounded implementation.
4. If user asks to run a simulation, choose simulation source, use MiroFish/OASIS/CAMEL, simulate judges/stakeholders, or forecast public reaction → load `simulation-router` first.
5. If user asks for research → choose between Hermes web tools, `literature-access` for academic/technical papers, `online-presence-research`, `youtube-content`, or DK `recent_research_brief`.
6. If user asks to extract or convert a document/PDF → load `markitdown` first; for creation or editing, choose the native `docx`, `xlsx`, `pdf`, or `nano-pdf` skill.
7. If user asks for business SimpleWeb KH → load `simpleweb-kh`; for a founder hard call or idea validation, load `founder-thinking-mode` and optionally `external-validation-research`.
8. If user asks for web or UI design, route by the actual job: `web-design-engineer` for full browser artifacts/redesigns, `emil-design-eng` for component craft, `landing-page-design` for conversion pages, `animate` for motion, `build-awwwards-quality-sites` for cinematic sites, `video-to-superprompt` for video analysis, `tastemaker` for anti-generic/reference-led direction, `critique-screen` for rendered-screen critique, `interface-review` for code changes, and `better-layout` or `perception-laws` for targeted diagnoses. Add `popular-web-designs` only when the user requests a named visual vocabulary.
9. If user asks for data analysis → load `data-analytics` before choosing notebooks or charts.
10. If no match: use `skills_list`, then load the closest skills before answering.

## How to answer the user

Prefer:

```text
Verdict: use <skill/workflow>.
Why: ...
I’ll do: ...
```

Then act if obvious.
