# Windows / Git Bash ad-hoc verification scripts

Use this when a coding task needs focused verification but the project has no canonical test suite, or when the runtime asks for a temporary `hermes-verify-` script.

## Pattern

Create the temporary script from the shell that will execute it, then run and clean it from that same shell. On Windows hosts running Git Bash/MSYS, this avoids fragile Python-subprocess path conversion between native `C:\...` paths and `/c/...` paths.

```bash
tmp=$(python - <<'PY'
import os, tempfile
from pathlib import Path

script = r'''#!/usr/bin/env bash
set -euo pipefail
cd '/c/path/to/project'

echo '[ad-hoc] assert changed config shape'
# add focused file/content assertions here

echo '[ad-hoc] run focused verification'
pnpm lint
pnpm typecheck
pnpm build
'''

temp_dir = Path(os.environ.get('TEMP') or tempfile.gettempdir())
fd, p = tempfile.mkstemp(prefix='hermes-verify-', suffix='.sh', dir=str(temp_dir), text=True)
os.close(fd)
Path(p).write_text(script, encoding='utf-8', newline='\n')
os.chmod(p, 0o700)
msys = Path(p).as_posix()
if len(msys) > 1 and msys[1] == ':':
    msys = '/' + msys[0].lower() + msys[2:]
print(msys)
PY
)

echo "TEMP_SCRIPT_MSYS=$tmp"
echo "TEMP_SCRIPT_WIN=$(cygpath -w "$tmp" 2>/dev/null || echo "$tmp")"
bash "$tmp"
rc=$?
rm -f "$tmp" && echo "CLEANED_UP=$tmp"
exit $rc
```

## Reporting language

Call this **ad-hoc verification**, not “suite green”, unless a real project test suite exists and was run. Summarize:

- temp script path and cleanup status;
- assertions performed;
- commands run;
- exit code and important output;
- any blocker if cleanup or execution failed.

## Pitfalls

- Do not claim full verification from config assertions alone; run the focused build/typecheck/lint or a smoke check relevant to the change.
- Do not leave temp scripts behind unless cleanup fails; if cleanup fails, report the exact path.
- On Windows Git Bash, avoid executing a Windows-native tempfile path directly from a Python subprocess. Prefer the same-shell create/run/cleanup pattern above.