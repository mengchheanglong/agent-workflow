# Route Testing Patterns

## Basic curl pattern

```bash
curl -s -o /dev/null -w "%{http_code} %{time_total}s" --max-time 30 http://localhost:3000/route
```

Output: `200 4.517312s` — parse as `status time`

## Capture response body for error detection

```bash
curl -s --max-time 30 http://localhost:3000/route | head -100
```

Look for:
- `Application error` (Next.js runtime error)
- `Unhandled Runtime Error`
- `Error: ...` stack traces
- `Cannot read properties of undefined`

## Follow redirects

```bash
curl -s -o /dev/null -w "%{http_code} %{redirect_url}" --max-time 30 -L http://localhost:3000/route
```

## Batch testing with execute_code

```python
import subprocess

BASE = "http://localhost:3000"
routes = ["/", "/about", "/evidence/[slug]"]

results = []
for route in routes:
    r = subprocess.run(
        ["curl", "-s", "-o", "/dev/null", "-w", "%{http_code} %{time_total}s", "--max-time", "30", f"{BASE}{route}"],
        capture_output=True, text=True, timeout=35
    )
    output = r.stdout.strip()
    parts = output.split()
    status = parts[0] if parts else "000"
    time_taken = parts[1] if len(parts) > 1 else "N/A"
    results.append({"route": route, "status": status, "time": time_taken})
```

## Parallel testing (faster)

```python
import subprocess
from concurrent.futures import ThreadPoolExecutor

def test_route(route):
    r = subprocess.run(
        ["curl", "-s", "-o", "/dev/null", "-w", "%{http_code} %{time_total}s", "--max-time", "30", f"{BASE}{route}"],
        capture_output=True, text=True, timeout=35
    )
    return route, r.stdout.strip()

with ThreadPoolExecutor(max_workers=5) as executor:
    results = list(executor.map(test_route, routes))
```

## JSON output for structured reports

```bash
curl -s -o /dev/null -w '{"status": %{http_code}, "time": %{time_total}, "url": "%{url_effective}"}' --max-time 30 http://localhost:3000/route
```

## Check if route exists (404 detection)

```bash
curl -s -o /dev/null -w "%{http_code}" --max-time 30 http://localhost:3000/nonexistent
# Returns: 404
```

## Server not running detection

```bash
curl -s -o /dev/null -w "%{http_code}" --max-time 5 http://localhost:3000/
# Returns: 000 (connection refused)
```