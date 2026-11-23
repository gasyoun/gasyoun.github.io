# console-popup-watch

Catch and fix the 1-second console windows that Windows tooling flashes.

- **`index.html`** — the guide: symptom → cause → fix patterns (Node, Python, PowerShell/scheduled tasks) → 15-minute verification protocol → traps.
- **`console_watch_cal.py`** — reads the interactive desktop every 80 ms, logs only NEW visible windows with class, title, pid, PEB command line and full parent chain; writes a JSONL receipt with 30-s heartbeats. Includes the A/B canary (`--negctl`) that proves the watcher is not blind.
- **`byte_match_3way.py`** — compares a file across live / deploy / repo-HEAD with CRLF→LF normalization; exit 0 or a named drift list. Run before and after the interception window.
- **`report.html`** — client-side JSONL report renderer (no upload, zero dependencies): timeline strip, flash table, heartbeat coverage, canary verdict. Accepts plain watch and `--negctl` receipts in one parse; a 0/0 canary renders as *inconclusive*, never clean.

`demo/` — synthetic demo feeds (Load-demo fixtures, `demo: true`); `figures/` — guide figures generated from the feeds; `smoke/` — browser-smoke evidence screenshots for the renderer.

## Quickstart

```sh
# 1) prove the watcher sees real windows in YOUR session (console-less parent!)
pythonw console_watch_cal.py --negctl --out negctl.jsonl
#    expected: watcher_not_blind=true  (default spawn caught, CREATE_NO_WINDOW not)

# 2) ≥15 minutes of live estate activity
pythonw console_watch_cal.py --duration 900 --out watch.jsonl

# 3) no-revert check of the fixed files, before and after
python byte_match_3way.py --live C:/live --deploy C:/deploy --repo C:/src --file path/to/fixed.ts
```

## Requirements

Windows, Python 3.8+, git on PATH for the byte-match. No third-party packages. Read-only; writes only the `--out` JSONL you name.

## License

MIT — see the header of each script.
