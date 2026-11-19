#!/usr/bin/env python3
"""Check every LIVE vote/sheets/*.html for a stale (or missing) csl-pyutil
``<meta name="generator">`` tag, versus the latest sanskrit-lexicon/csl-pyutil
GitHub release.

Part of H2854 step 5 (vote-platform build, tracked in Uprava). Scope bound to
the LIVE registry by the YL3 regen wave (19-11-2026, MG ruling A —
strict-on-live):

* **live** (scripts/live_vote_sheets.json) — open voting surfaces awaiting
  MG. A stale or meta-less LIVE sheet FAILS the job (exit 1).
* **live_parked** — LIVE sheets that cannot be re-rendered today, each with a
  reason and a resolution path. Staleness is reported as a loud WARN, never a
  fail, so the parked debt stays visible every run instead of redding master
  forever.
* **frozen / archived** — never scanned (unchanged from H2852's "НЕ трогать").
* Everything else hosted under vote/sheets/ — closed decision records,
  superseded drafts, pre-vote triage pipelines — is logged as a regen queue
  and never fails the job (the H3848 finding: ~100 closed records as hard reds
  carried zero signal).

New sheets are hosted current by construction; register a sheet under "live"
in scripts/live_vote_sheets.json in the SAME pass that hosts it, and drop the
entry the moment its vote applies. The fail-closed property lives in the
registry: a sheet nobody classified is queue, so the register step is the
enforcement point.

Usage:
    python scripts/check_sheet_staleness.py

Exit codes:
    0 - every LIVE sheet carries a generator meta tag whose version matches
        the latest csl-pyutil release (parked sheets may WARN)
    1 - at least one LIVE sheet is stale or missing the meta tag entirely
    2 - could not determine the latest csl-pyutil release (network/API error)

No GitHub token is required: sanskrit-lexicon/csl-pyutil is a public repo and
the unauthenticated GitHub API rate limit (60 req/hour per IP) is more than
enough for a weekly/on-push CI check.
"""

from __future__ import annotations

import json
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

REPO_ROOT = Path(__file__).resolve().parent.parent
SHEETS_DIR = REPO_ROOT / "vote" / "sheets"
REGISTRY_PATH = Path(__file__).resolve().parent / "live_vote_sheets.json"

LATEST_RELEASE_API = (
    "https://api.github.com/repos/sanskrit-lexicon/csl-pyutil/releases/latest"
)

GENERATOR_META_RE = re.compile(
    r'<meta\s+name=["\']generator["\']\s+content=["\']csl-pyutil/([0-9]+\.[0-9]+\.[0-9]+)["\']',
    re.IGNORECASE,
)


def fetch_latest_csl_pyutil_version() -> str:
    """Return the latest csl-pyutil release tag (without the leading 'v')."""
    req = urllib.request.Request(
        LATEST_RELEASE_API,
        headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": "gasyoun.github.io-sheet-staleness-check",
        },
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        data = json.load(resp)
    tag = data["tag_name"]
    return tag.lstrip("v")


def parse_version(version: str) -> tuple[int, ...]:
    return tuple(int(part) for part in version.split("."))


def load_registry() -> dict[str, dict[str, str]]:
    with REGISTRY_PATH.open(encoding="utf-8") as fh:
        return json.load(fh)


def extract_generator_version(html_path: Path) -> str | None:
    text = html_path.read_text(encoding="utf-8", errors="replace")
    match = GENERATOR_META_RE.search(text)
    return match.group(1) if match else None


def main() -> int:
    if not SHEETS_DIR.is_dir():
        print(f"ERROR: sheets directory not found: {SHEETS_DIR}", file=sys.stderr)
        return 2

    try:
        registry = load_registry()
    except (OSError, ValueError) as exc:
        print(f"ERROR: could not load {REGISTRY_PATH.name}: {exc}", file=sys.stderr)
        return 2
    live = registry.get("live", {})
    parked = registry.get("live_parked", {})
    excluded: dict[str, str] = {}
    excluded.update(registry.get("frozen", {}))
    excluded.update(registry.get("archived", {}))

    try:
        latest_version = fetch_latest_csl_pyutil_version()
    except (urllib.error.URLError, urllib.error.HTTPError, KeyError, ValueError) as exc:
        print(f"ERROR: could not fetch latest csl-pyutil release: {exc}", file=sys.stderr)
        return 2

    latest_tuple = parse_version(latest_version)
    print(f"Latest csl-pyutil release: {latest_version}")
    print(
        f"Registry: {len(live)} live · {len(parked)} live-parked · "
        f"{len(excluded)} frozen/archived"
    )

    sheet_files = sorted(SHEETS_DIR.glob("*.html"))
    if not sheet_files:
        print(f"ERROR: no sheet HTML files found under {SHEETS_DIR}", file=sys.stderr)
        return 2

    live_stale: list[tuple[str, str | None]] = []
    live_current = 0
    parked_stale: list[tuple[str, str | None]] = []
    queue_stale: list[tuple[str, str | None]] = []
    missing_live: list[str] = []

    for sheet_path in sheet_files:
        sheet_id = sheet_path.stem
        if sheet_id in excluded:
            continue

        version = extract_generator_version(sheet_path)
        stale = True
        if version is not None:
            try:
                stale = parse_version(version) < latest_tuple
            except ValueError:
                stale = True

        if sheet_id in live:
            if stale:
                live_stale.append((sheet_id, version))
            else:
                live_current += 1
        elif sheet_id in parked:
            if stale:
                parked_stale.append((sheet_id, version))
        else:
            if stale:
                queue_stale.append((sheet_id, version))

    for sheet_id in sorted(live):
        if not (SHEETS_DIR / f"{sheet_id}.html").exists():
            missing_live.append(sheet_id)

    print(f"Live sheets current: {live_current} of {len(live)}")
    if parked_stale:
        print(f"\nLIVE-PARKED but stale (WARN — never a fail; unblock each):")
        for sheet_id, reason in sorted(parked.items()):
            version = dict(parked_stale).get(sheet_id)
            detected = version if version else "no meta tag"
            print(f"  ! {sheet_id} ({detected}): {reason}")
    if queue_stale:
        print(f"\nRegen queue (closed records / superseded / pre-vote pipelines — no fail): {len(queue_stale)}")
        for sheet_id, version in sorted(queue_stale):
            detected = version if version else "no meta tag"
            print(f"  - {sheet_id}: {detected} (latest: {latest_version})")

    if missing_live:
        print("\nLIVE sheets MISSING from vote/sheets/:")
        for sheet_id in missing_live:
            print(f"  - {sheet_id}")

    if live_stale:
        print("\nSTALE LIVE sheets (open voting surfaces — regenerate against latest csl-pyutil):")
        for sheet_id, version in sorted(live_stale):
            detected = version if version else "no meta tag"
            print(f"  - {sheet_id}: {detected} (latest: {latest_version})")
        return 1

    if missing_live:
        return 1

    print("\nAll LIVE sheets are current.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
