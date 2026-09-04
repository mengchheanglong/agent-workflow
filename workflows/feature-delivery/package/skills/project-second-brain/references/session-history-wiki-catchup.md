# Session History → Wiki Catch-up Workflow

Use when the user says they forgot to wiki recent work, asks to "wiki everything", or wants recent sessions converted into durable project context.

## Goal

Create durable, class-level wiki/context pages from past Hermes sessions without dumping transcripts or creating one narrow page per session.

## Workflow

1. **Load project routing first**
   - Read the local `AGENTS.md` / `.active/` context if present.
   - Identify the wiki/root knowledge base that should receive the updates.
   - If an existing wiki has `SCHEMA.md`, `index.md`, and `log.md`, follow them.

2. **Search session history broadly, then by topic**
   - Use recent-session browse for recency.
   - Use topic searches for known active workstreams.
   - Use scroll/read only when the discovery result is insufficient.
   - Keep session ids in the catch-up page for exact future retrieval.

3. **Classify into umbrella pages**
   - Create/update project or workflow pages such as `menui`, `evalora`, `digital-twin`, not one page per session.
   - Use a catch-up index page for the session-id table and cross-links.
   - Preserve durable artifacts, decisions, paths, verification results, and next-action state.
   - Do not copy raw transcripts, temporary todos, or stale blow-by-blow progress.

4. **Respect source freshness**
   - Session history is evidence of what was said/done, not proof of current external state.
   - When a page references a repo/file/artifact, phrase it as "captured in session" unless you verify live state.
   - Include source session ids so future agents can re-open exact context.

5. **Update navigation and schema**
   - Add every new page to `index.md`.
   - Append one log entry to `log.md` summarizing the catch-up.
   - Extend `SCHEMA.md` taxonomy only for durable new domains/tags.

6. **Verify statically**
   - Count wiki pages and ensure `index.md` total matches.
   - Check every new page has YAML frontmatter.
   - Resolve `[[wikilinks]]` among local markdown stems.
   - Confirm the log entry exists.

## Good catch-up page shape

```markdown
---
title: Recent Session Catch-up — YYYY-MM-DD
created: YYYY-MM-DD
updated: YYYY-MM-DD
type: session-notes
tags: [session-catchup, ...]
---

# Recent Session Catch-up — YYYY-MM-DD

## Sessions checked
| Date | Session | Topic | Wiki result |
|---|---|---|---|

## Durable updates made
- [[project-a]] — one-line durable summary

## Highest-value recovered decisions

## What was not exhaustively done
This pass did not dump every transcript line. Use `session_search(session_id=...)` for exact middle-of-session details.
```

## Pitfalls

- Do not create a long flat list of one-session pages when the work belongs under class-level project/workflow pages.
- Do not treat old session-search results as current proof of live repo or website state.
- Do not skip verification because the files are "just markdown"; catch broken links/page counts immediately.
- Do not store secrets, IDs, passwords, tokens, or government-ID material from privacy/identity sessions.
