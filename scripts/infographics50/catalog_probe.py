#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""catalog_probe.py — probe the canonical 50-idea infographic catalog.

Revival of Uprava tools/infographics_catalog_probe.py (retired 28-09-2026 by
the 0K8 orphan-tool census) co-located with the catalog it guards, per H5744.
Extension (H5744): --links derives EVERY catalog link from the catalog HTML
itself, so new waves (b6 #59-#66 and beyond) are covered without edits.

Checks, all against real data:
  1. somadeva: 18 SAN + 18 RUS Kathasaritsagara chapter files, non-empty (#18).
  2. ORS-FAQ/Tukan_stats.md: funnel anchor numbers present (#27).
  3. Catalog HTML: #18 replaced, #27 unblocked, #51 registered, zero
     "нужны данные" chips, and the b6 group present when #59 exists.
  4. --links: every infographics link in the catalog returns HTTP 200.

Usage:
    python3 scripts/infographics50/catalog_probe.py \
        [--catalog <path-or-URL>] [--estate <GitHub-dir>] [--links]

Exit 0 = all probes PASS; exit 1 = any FAIL (never silent).
"""
from __future__ import annotations

import argparse
import os
import pathlib
import re
import sys
import time
import urllib.request

sys.stdout.reconfigure(encoding="utf-8")

CATALOG_URL = (
    "https://gasyoun.github.io/infographics/sanskrit-infographics-catalog/index.html"
)

RESULTS: list[tuple[str, bool, str]] = []


def record(name: str, ok: bool, detail: str) -> None:
    RESULTS.append((name, ok, detail))
    print(("PASS " if ok else "FAIL ") + f"{name}: {detail}")


def fetch(url: str, tries: int = 3, timeout: int = 30) -> tuple[int, str]:
    """GET with 3-try backoff; returns (status, body-or-error)."""
    last = ""
    for attempt in range(1, tries + 1):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "catalog-probe/2"})
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                return resp.status, resp.read().decode("utf-8", "replace")
        except Exception as exc:  # noqa: BLE001 - report the last error
            last = f"{type(exc).__name__}: {exc}"
            if attempt < tries:
                time.sleep(2 * attempt)
    return 0, last


def load_catalog(source: str) -> str:
    if re.match(r"^https?://", source):
        status, body = fetch(source)
        if status != 200:
            raise SystemExit(f"FAIL catalog fetch {source}: HTTP {status} {body[:200]}")
        return body
    return pathlib.Path(source).read_text(encoding="utf-8")


def estate_root(arg: str) -> pathlib.Path:
    if arg:
        return pathlib.Path(arg).expanduser()
    env = os.environ.get("GITHUB_ESTATE")
    if env and pathlib.Path(env).is_dir():
        return pathlib.Path(env)
    for cand in (
        pathlib.Path.home() / "Documents" / "GitHub",
        pathlib.Path.home() / "GitHub",
    ):
        if (cand / "csl-orig").is_dir():
            return cand
    return pathlib.Path.home() / "Documents" / "GitHub"


def probe_somadeva(estate: pathlib.Path) -> None:
    san = sorted((estate / "somadeva" / "chapters_san").glob("*.txt"))
    rus = sorted((estate / "somadeva" / "chapters_rus").glob("*.txt"))
    ok = len(san) == 18 and len(rus) == 18
    detail = f"chapters_san={len(san)}, chapters_rus={len(rus)}"
    if ok:
        san_lines = sum(
            len(p.read_text(encoding="utf-8", errors="replace").splitlines())
            for p in san
        )
        detail += f", san_lines={san_lines}"
        ok = san_lines > 0
    record("somadeva-18plus18", bool(ok), detail)


def probe_tukan(estate: pathlib.Path) -> None:
    path = estate / "ORS-FAQ" / "Tukan_stats.md"
    if not path.is_file():
        record("ors-tukan-stats", False, f"{path} missing")
        return
    text = path.read_text(encoding="utf-8")
    anchors = ["3 064", "2 794", "46 325", "38 280"]
    missing = [a for a in anchors if a not in text]
    record("ors-tukan-stats", not missing, f"anchors missing={missing or 'none'}")


def probe_catalog(text: str, source: str) -> None:
    where = "live" if re.match(r"^https?://", source) else "local"
    checks = [
        ("row18-somadeva", "Сомадева" in text and "somadeva/chapters_san" in text),
        ("row27-tukan", "Tukan_stats" in text and "46 325" in text),
        ("row51-prefaces", "№ 51" in text and "prefaces-seven-2026-08-29" in text),
        ("row59-b6", "№ 59" in text and "kosha-manifest-2026-10-08" in text),
        ("no-blocked-chips", "нужны данные" not in text),
    ]
    for name, ok in checks:
        record(name, ok, f"catalog {where}")


def catalog_links(text: str) -> list[str]:
    """Every unique infographics URL carried by the catalog (H5744: derived,
    auto-extends to new waves). The exact linked path is probed — a catalog
    may link all-styles.html instead of index.html."""
    paths = sorted(set(re.findall(r"gasyoun\.github\.io/infographics/([a-z0-9-]+/[\w.\-]+)", text)))
    return [f"https://gasyoun.github.io/infographics/{p}" for p in paths]


def probe_links(text: str) -> None:
    urls = catalog_links(text)
    record("links-derived", len(urls) >= 60, f"{len(urls)} links from catalog")
    for url in urls:
        status, _ = fetch(url, timeout=20)
        record(f"link-{url.split('/infographics/')[1].rstrip('/')}", status == 200,
               f"HTTP {status}")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--estate", default="")
    ap.add_argument("--catalog", default=CATALOG_URL)
    ap.add_argument("--links", action="store_true",
                    help="HTTP-check every catalog link (derived, H5744)")
    args = ap.parse_args()

    text = load_catalog(args.catalog)
    probe_catalog(text, args.catalog)
    estate = estate_root(args.estate)
    probe_somadeva(estate)
    probe_tukan(estate)
    if args.links:
        probe_links(text)

    failed = [name for name, ok, _ in RESULTS if not ok]
    print(
        f"\n{len(RESULTS) - len(failed)}/{len(RESULTS)} probes PASS"
        + (f"; FAILED: {', '.join(failed)}" if failed else "")
    )
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
