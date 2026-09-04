# Private Multi-Repository Agent Portability

Use this when a user wants to continue work from another laptop or let an AI coding agent work directly from private GitHub repositories.

## Repository boundaries

- Resolve the exact current repository root and identify required sibling repositories.
- Keep independent research, implementation, frontend, and infrastructure repositories independent; do not push a noisy parent directory or flatten Git histories for transport.
- Verify each required repository has the intended GitHub remote, upstream branch, authenticated access, and private visibility.

## Safe interpretation of “entire directory”

Push all intended Git-tracked project content, not every physical file. Inspect tracked, modified, staged, untracked, and ignored state. Never force-add credentials, `.env`, auth stores, editor state, agent caches, build output, private attachments, or machine-local configuration merely for portability. Report exclusions explicitly.

## Rules-file preparation

For each repository used by Claude Code or another agent:

1. Preserve the detailed `AGENTS.md` routing when present.
2. Verify whether `CLAUDE.md` is already tracked even if a read/search tool reports it missing.
3. Inspect live and `HEAD` versions before writing.
4. Preserve useful legacy/domain instructions and prepend a short active-authority header instead of replacing them.
5. Explain sibling repository roles without embedding credentials or machine-specific absolute paths.
6. Keep normal commit/push restrictions in the rules even when the current session is explicitly authorized to push.

## Push verification

- Fetch and check divergence before editing.
- Validate changed governance JSON/schema/drift and run relevant repository checks.
- Secret-scan the changed files and inspect suspicious tracked filenames.
- Stage exact paths and commit logical changes separately where practical.
- Push without history rewrite.
- Fetch again and prove local `HEAD` equals the upstream branch.
- Re-query repository visibility after push.

## Portability proof

Create disposable authenticated shallow clones of every required private repository. Verify expected routing, active state, manifests, migrations, tests, and implementation paths; compare cloned commits to pushed commits; delete the disposable clones; confirm source worktrees are clean.

## Handoff

Provide exact clone commands and preserve the sibling layout:

```bash
gh auth login
mkdir -p ~/projects && cd ~/projects
gh repo clone OWNER/research-repo
gh repo clone OWNER/implementation-repo
```

State which repository is for strategy/research and which is for implementation. Private access must be granted to the GitHub account or AI integration used on the other machine.
