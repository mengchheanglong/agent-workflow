# TypeScript / Next.js diagnostics from editor screenshots

Use when the user points at a VS Code/IDE Problems panel screenshot for a Next.js + TypeScript app.

## Triage pattern

1. Treat the screenshot as a separate source of truth from the original bug report. The visible Problems panel may show a different issue than the UI bug under discussion.
2. Read the referenced config/source file and line numbers before changing anything.
3. Prefer removing or modernizing deprecated options over suppressing warnings. Only use `ignoreDeprecations` after verifying the installed TypeScript accepts the suggested value.
4. Verify with `npx tsc --noEmit --pretty false`, then the project test/build commands.

## Durable fixes seen for Next.js App Router + TS 5.x/6-readiness

When VS Code reports deprecation warnings like:

- `downlevelIteration` is deprecated
- `moduleResolution=node10` / `moduleResolution: "node"` is deprecated
- `baseUrl` is deprecated

A clean Next.js App Router config may be:

```json
{
  "compilerOptions": {
    "module": "esnext",
    "target": "es2020",
    "moduleResolution": "bundler",
    "paths": {
      "@/*": ["./src/*"]
    }
  }
}
```

Notes:

- Remove `downlevelIteration` when modern targets already support the needed iteration semantics.
- Use `moduleResolution: "bundler"` for modern Next.js bundler-based resolution.
- `paths` can work without `baseUrl` in current TypeScript; verify in the project before committing.
- If `ignoreDeprecations: "6.0"` is suggested by the editor but `tsc` rejects it as invalid, do not keep it. Fix the deprecated options instead.

## Next.js build verification quirk

If `next build` fails during page-data collection with a stale `.next`/manifest style `PageNotFoundError` immediately after recent file/route changes, run the project clean step (for example `npm run clean:next`) and rerun the build once. Capture the retry result. Do not encode the transient error as a durable project limitation if the clean rebuild passes.
