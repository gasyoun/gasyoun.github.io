#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""H5744 wave-b6 estate probes: eight fresh catalog slots (#59-#66).

Python 3.9+. Writes data/h5744.json. Derive-don't-store: every number is
counted here from committed estate files and re-derived on every run.
"""
from __future__ import annotations

import collections
import json
import os
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")


def _estate_root() -> Path:
    """GitHub estate clone root, portable ($GITHUB_ESTATE / auto-detect, H3710)."""
    env = os.environ.get("GITHUB_ESTATE")
    if env and Path(env).is_dir():
        return Path(env)
    here = Path(__file__).resolve()
    for parent in here.parents:
        if parent.name == "GitHub" and (parent / "csl-orig").is_dir():
            return parent
    for cand in (
        Path.home() / "Documents" / "GitHub",
        Path.home() / "GitHub",
    ):
        if (cand / "csl-orig").is_dir():
            return cand
    raise SystemExit(
        "h5744_probe.py: cannot locate the GitHub estate root; set GITHUB_ESTATE"
    )


GH = _estate_root()
HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent  # gasyoun.github.io root (this repo)
OUT = HERE / "data" / "h5744.json"

RESULT: dict = {}


def ok(name: str, cond: bool, detail: str = "") -> None:
    RESULT[name] = {"ok": bool(cond), "detail": detail}
    print(("PASS " if cond else "FAIL ") + name + (f": {detail}" if detail else ""))


def probe_kosha() -> dict:
    p = GH / "kosha" / "data" / "manifest" / "datasets.json"
    d = json.loads(p.read_text(encoding="utf-8"))
    ds = d["datasets"]
    tiers = collections.Counter(x.get("tier", "?") for x in ds)
    formats = collections.Counter(x.get("format", "?") for x in ds)
    out = {
        "path": "kosha/data/manifest/datasets.json",
        "n_datasets": len(ds),
        "tiers": dict(tiers),
        "formats": dict(formats),
        "doi_count": sum(1 for x in ds if x.get("doi")),
        "rows_sum": sum(x.get("rows", 0) or 0 for x in ds),
        "top_formats": formats.most_common(5),
    }
    ok("kosha", len(ds) >= 100, f"datasets={len(ds)}")
    return out


def probe_vote() -> dict:
    sheets = sorted((ROOT / "vote" / "sheets").rglob("*.html"))
    prefixes = collections.Counter(
        re.split(r"[_\d]", p.name.lower(), maxsplit=1)[0] for p in sheets
    )
    out = {
        "path": "vote/sheets/**/*.html",
        "n_sheets": len(sheets),
        "top_prefixes": prefixes.most_common(10),
    }
    ok("vote-hub", len(sheets) >= 200, f"sheets={len(sheets)}")
    return out


def probe_handoffs() -> dict:
    live_dir = GH / "Uprava" / "handoffs"
    arch_dir = live_dir / "archive"
    live = [p for p in live_dir.glob("*.md") if re.match(r"^H\d", p.name)]
    arch = [p for p in arch_dir.glob("*.md") if re.match(r"^H\d", p.name)]
    pools = collections.Counter()
    for p in live + arch:
        m = re.match(r"^H\d+[-_]?([A-Za-z0-9]+)[-_]", p.name)
        pools[m.group(1) if m else "other"] += 1
    out = {
        "path": "Uprava/handoffs[/archive]/*.md (H-numbered)",
        "live": len(live),
        "archived": len(arch),
        "total": len(live) + len(arch),
        "pools": pools.most_common(),
    }
    ok("handoff-lifecycle", len(arch) > 1000,
       f"live={len(live)} archived={len(arch)}")
    return out


def probe_rigveda() -> dict:
    t = (ROOT / "RV" / "index.html").read_text(encoding="utf-8", errors="replace")
    classes = {c: len(re.findall(f'class="{c}"', t)) for c in ("sa", "ru", "de", "en")}
    stamps = len(re.findall(r"rv\d+\.\d+\.\d+", t))
    verses = min(classes.values())
    out = {
        "path": "RV/index.html",
        "classes": classes,
        "stamps": stamps,
        "verses": verses,
        "langs": 4,
    }
    ok("rigveda-4langs", verses >= 1000 and len(set(classes.values())) == 1,
       f"verses={verses} langs=4")
    return out


def probe_modules() -> dict:
    p = GH / "Uprava" / "data" / "module_spread_census_v2.json"
    d = json.loads(p.read_text(encoding="utf-8"))
    uni = d.get("universe", {})
    out = {
        "path": "Uprava/data/module_spread_census_v2.json",
        "declared": uni.get("canonical_declared"),
        "listed": uni.get("listed"),
        "probed": uni.get("probed"),
        "no_clone": len(uni.get("no_clone", [])),
        "classes": d.get("activity_classes"),
        "module_to_handoff": len(d.get("module_to_handoff", {}))
        if isinstance(d.get("module_to_handoff"), dict)
        else len(d.get("module_to_handoff", [])),
    }
    ok("module-spread", (out["declared"] or 0) >= 100,
       f"declared={out['declared']} probed={out['probed']}")
    return out


def probe_outages() -> dict:
    t = (GH / "Uprava" / "SERVER_OUTAGES.md").read_text(encoding="utf-8")
    rows = [
        ln for ln in t.splitlines()
        if ln.startswith("| ") and "---" not in ln
        and not ln.startswith("| Host")
    ]
    hosts = collections.Counter(
        re.sub(r"[`*]", "", ln.split("|")[1]).strip().split(" (")[0]
        for ln in rows
    )
    out = {
        "path": "Uprava/SERVER_OUTAGES.md",
        "rows": len(rows),
        "hosts": hosts.most_common(10),
    }
    ok("outage-ledger", len(rows) >= 10, f"rows={len(rows)} hosts={len(hosts)}")
    return out


def probe_reports() -> dict:
    rep = GH / "Uprava" / "reports"
    per = collections.Counter()
    for p in rep.rglob("*"):
        if p.is_file():
            per[p.relative_to(rep).parts[0]] += 1
    total = sum(per.values())
    out = {
        "path": "Uprava/reports/**",
        "total_files": total,
        "top_dirs": per.most_common(10),
    }
    ok("evidence-reports", total >= 100, f"files={total}")
    return out


def probe_gtd() -> dict:
    t = (GH / "Uprava" / "GTD_NEXT_ACTIONS.md").read_text(encoding="utf-8")
    rows = [
        ln for ln in t.splitlines()
        if ln.startswith("| ") and "---" not in ln
        and not ln.startswith("| Owner")
    ]
    out = {
        "path": "Uprava/GTD_NEXT_ACTIONS.md",
        "table_rows": len(rows),
        "markers": {
            "@DO": t.count("@DO"),
            "@WAITING": t.count("@WAITING"),
            "@DECIDE": t.count("@DECIDE"),
        },
    }
    ok("gtd-queue", len(rows) >= 10,
       f"rows={len(rows)} markers={out['markers']}")
    return out


def main() -> int:
    RESULT.clear()
    data = {
        "counted": "08.10.2026",
        "kosha": probe_kosha(),
        "vote": probe_vote(),
        "handoffs": probe_handoffs(),
        "rigveda": probe_rigveda(),
        "modules": probe_modules(),
        "outages": probe_outages(),
        "reports": probe_reports(),
        "gtd": probe_gtd(),
    }
    OUT.write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print("wrote", OUT.relative_to(HERE.parent.parent))
    bad = [k for k, v in RESULT.items() if not v["ok"]]
    if bad:
        print("FAILED probes:", ", ".join(bad))
        return 1
    print("8/8 probes PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
