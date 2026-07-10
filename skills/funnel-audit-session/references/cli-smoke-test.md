# CLI Smoke Test — Verify Screenshot Capture After Updates

Run this after any pull, Playwright upgrade, or greenlet error to confirm the
CLI screenshot pipeline is healthy. It's the same test used to distinguish
"broken tooling" from "heavy target URL" in the timeout-diagnosis flow.

## One-Command Test

```bash
cd "$FUNNEL_AUDITOR_HOME"
"$HERMES_VENV/Scripts/python" main.py crawl example.com
```

**What to check in the output:**

| Signal | Pass | Fail |
|---|---|---|
| Desktop SS column | ✓ | ✗ |
| Mobile SS column | ✓ | ✗ |
| Load time | A number (ms) | — or error |
| Error column | — | Any text |

## Filesystem Check

Files land in the repo root `screenshots/` by default:

```bash
ls -la screenshots/
```

Expected files created (timestamp = now, non-zero size):
- `example_com_desktop.png` (~10-15 KB)
- `example_com_mobile.png` (~8-12 KB)

Non-zero size + valid PNG header = screenshot capture is fully functional.

## When to Run

- **After `git pull`** — confirm nothing regressed in the crawler
- **After Playwright upgrade** — confirm Chromium still launches
- **After a greenlet / ModuleNotFoundError** — confirm the fix worked
- **Before a real lead walk in a new Hermes session** — one-time sanity check to
  rule out tooling issues before you burn budget on a real walk
- **When investigating a `crawl` timeout** — if example.com works, the target
  URL is the problem, not the CLI tooling

## Cleanup

Test screenshots are discarded by `git status` (./screenshots/ is not tracked).
No cleanup needed — they'll be naturally replaced next test.

## What If It Fails

1. Confirm Chromium is installed: `python -m playwright install --list`
   - Should show `chromium-1228` under `C:\Users\<user>\AppData\Local\ms-playwright`
2. If missing: `python -m playwright install chromium`
3. If installed but still fails: check for proxy or MITM interference
   (see `_ensure_mitm_friendly_tls()` in `audit/crawler.py`)
4. If all else fails: use the browser-tool fallback (browser_navigate →
   browser_snapshot) instead