#!/usr/bin/env python3
"""Check every live vote/sheets/*.html for a stale (or missing) csl-pyutil
``<meta name="generator">`` tag, versus the latest sanskrit-lexicon/csl-pyutil
GitHub release.

Part of H2854 step 5 (vote-platform build, tracked in Uprava). Companion of
the meta-generator layer added to csl-pyutil in v0.10.1
(Uprava/docs/ARCHITECTURE_UPRAVA_VOTE_PLATFORM.md, section "meta generator")
and the regen wave tracked by H2852
(Uprava/handoffs/H2852-Sonnet_Uprava_review-sheets-regen-wave-v0100_15.08.26.md).

Usage:
    python scripts/check_sheet_staleness.py

Exit codes:
    0 - every live (non-excluded) sheet carries a generator meta tag whose
        version matches the latest csl-pyutil release
    1 - at least one live sheet is stale or missing the meta tag entirely
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

LATEST_RELEASE_API = (
    "https://api.github.com/repos/sanskrit-lexicon/csl-pyutil/releases/latest"
)

# Excluded/frozen/archived sheets — kept in sync with the "НЕ трогать" list in
# H2852 (Uprava/handoffs/H2852-Sonnet_Uprava_review-sheets-regen-wave-v0100_15.08.26.md)
# and Uprava/docs/PLAN_UPRAVA_VOTE_PLATFORM_2026Q3.md. These sheets are
# deliberately not regenerated, so they are never scanned for staleness here.
# Update this constant if the exclusion list in H2852 changes.
EXCLUDED_SHEETS = {
    # Frozen pending a human decision (@DECIDE H2778) — do not touch.
    "h1210_ab_blind_40": "frozen pending @DECIDE H2778 (H2852)",
    # Archived / superseded by a newer version — do not re-publish.
    "h180_learner": "archived/outdated (H2852)",
    "h180_reglue": "archived — superseded by h180_reglue_v2 (H2852: \"h180_reglue v1\")",
    "h180_typology": "archived/outdated (H2852)",
}

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


def extract_generator_version(html_path: Path) -> str | None:
    text = html_path.read_text(encoding="utf-8", errors="replace")
    match = GENERATOR_META_RE.search(text)
    return match.group(1) if match else None


def main() -> int:
    if not SHEETS_DIR.is_dir():
        print(f"ERROR: sheets directory not found: {SHEETS_DIR}", file=sys.stderr)
        return 2

    try:
        latest_version = fetch_latest_csl_pyutil_version()
    except (urllib.error.URLError, urllib.error.HTTPError, KeyError, ValueError) as exc:
        print(f"ERROR: could not fetch latest csl-pyutil release: {exc}", file=sys.stderr)
        return 2

    latest_tuple = parse_version(latest_version)
    print(f"Latest csl-pyutil release: {latest_version}")

    sheet_files = sorted(SHEETS_DIR.glob("*.html"))
    if not sheet_files:
        print(f"ERROR: no sheet HTML files found under {SHEETS_DIR}", file=sys.stderr)
        return 2

    excluded_count = 0
    stale = []  # list of (sheet_id, detected_version_or_None)
    current = []

    for sheet_path in sheet_files:
        sheet_id = sheet_path.stem
        if sheet_id in EXCLUDED_SHEETS:
            excluded_count += 1
            continue

        version = extract_generator_version(sheet_path)
        if version is None:
            stale.append((sheet_id, None))
            continue

        try:
            version_tuple = parse_version(version)
        except ValueError:
            stale.append((sheet_id, version))
            continue

        if version_tuple < latest_tuple:
            stale.append((sheet_id, version))
        else:
            current.append((sheet_id, version))

    live_count = len(sheet_files) - excluded_count
    print(
        f"Live sheets scanned: {live_count} "
        f"(excluded/frozen/archived: {excluded_count} of {len(sheet_files)} total)"
    )
    print(f"Up to date: {len(current)}")
    print(f"Stale or missing meta: {len(stale)}")

    if excluded_count:
        print("\nExcluded (frozen/archived, not scanned):")
        for sheet_id, reason in sorted(EXCLUDED_SHEETS.items()):
            marker = "found" if (SHEETS_DIR / f"{sheet_id}.html").exists() else "not present"
            print(f"  - {sheet_id} ({marker}): {reason}")

    if stale:
        print("\nSTALE sheets (regenerate against latest csl-pyutil):")
        for sheet_id, version in sorted(stale):
            detected = version if version else "no meta tag"
            print(f"  - {sheet_id}: {detected} (latest: {latest_version})")
        return 1

    print("\nAll live sheets are current.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
