# Windows/MSYS Bash Quirks for Route Testing

## The core problem

On Windows, Hermes terminal runs through **git-bash/MSYS**, not cmd.exe or PowerShell. This causes several common failures when starting dev servers and running batch tests.

## Common failure modes

### 1. `bash: no job control in this shell`

Cause: MSYS bash doesn't support job control (the `&` operator) inside `terminal()` calls.

**Wrong:**
```bash
npx next dev -p 3000 &
```

**Right:** Use `terminal(command="npx next dev -p 3000", background=true)` and poll with `process(action="wait")`.

### 2. `setsid` not found, `nohup` unreliable

MSYS doesn't have `setsid`. `nohup` exists but often doesn't detach properly from the terminal session.

**Don't use:** `setsid`, `nohup`, trailing `&` in foreground commands.

### 3. `EADDRINUSE` after kill

After `taskkill /F /IM node.exe`, TCP connections enter TIME_WAIT state. The port may still appear in `netstat` output.

**Fix:** Wait 3-5 seconds after taskkill before starting a new server. If still in use:
```bash
netstat -ano | grep 3000 | grep LISTEN
# Get PID, then:
taskkill //PID <pid> //F
```

### 4. Foreground command with `&` rejected

Hermes explicitly rejects foreground commands with trailing `&`:
> "Foreground command uses '&' backgrounding. Re-send WITHOUT the '&' as terminal(command=\"<cmd>\", background=true)"

**Fix:** Always use `background=true` instead of `&`.

### 5. `curl` hangs on first route hit (dev mode)

Next.js dev mode compiles routes on first request (3-8s). With many routes, sequential curl calls can take 5+ minutes total.

**Fix:** Use `--max-time 30` and test in batches. Accept that dev mode is slow.

## Next.js production build + start

Some repos use a custom build output directory (`.next-build` via `NEXT_DIST_DIR`). To test the production build:

```bash
# Build (outputs to .next-build)
npm run build

# Copy to .next (what next start expects)
rm -rf .next && cp -r .next-build .next

# Start production server
npx next start -p 3000
```

## Kill all Node processes

```bash
taskkill //F //IM node.exe 2>nul
```

Multiple Node processes accumulate during testing. Kill them all between test runs to prevent port conflicts.

## Port checking

```bash
# Check if port is in use
netstat -ano | grep 3000 | grep LISTEN

# Kill by port
taskkill //PID $(netstat -ano | grep 3000 | grep LISTEN | awk '{print $5}' | head -1) //F
```
