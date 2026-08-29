#!/usr/bin/env python3
"""H3707: re-emit only the repaired b1 pages (never the untouched mw-letters)."""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("build", HERE / "build.py")
build = importlib.util.module_from_spec(spec)
spec.loader.exec_module(build)

TARGETS = [
    "anatomy-mw-2026-08-29",
    "editions-timeline-2026-08-29",
    "dict-genealogy-2026-08-29",
    "morph-snowflake-2026-08-29",
    "case-grid-2026-08-29",
    "dict-passport-2026-08-29",
]
fns = {slug: fn for slug, _n, fn, _r in build.PAGES}
for slug in TARGETS:
    build.write(slug, fns[slug]())
    print("re-emitted", slug)
print("ok")
