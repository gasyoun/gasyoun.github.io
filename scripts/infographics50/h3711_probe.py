#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""H3711 estate probes for the 8-idea fresh pool + #18/#27 resolution.

Python 3.9+. Writes data/h3711.json. Derive-don't-store.
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

def _estate_root() -> Path:
    """Locate the GitHub estate clone root, portable across boxes (H3710).

    Order: $GITHUB_ESTATE env var, then known checkout locations, then the
    first parent of this repo whose directory name is 'GitHub'."""
    env = os.environ.get("GITHUB_ESTATE")
    if env and Path(env).is_dir():
        return Path(env)
    here = Path(__file__).resolve()
    for parent in here.parents:
        if parent.name == "GitHub" and (parent / "csl-orig").is_dir():
            return parent
    for cand in (
        Path.home() / "Documents" / "GitHub",
        Path("C:/Users/user/Documents/GitHub"),
        Path.home() / "GitHub",
    ):
        if (cand / "csl-orig").is_dir():
            return cand
    raise SystemExit(
        "h3711_probe.py: cannot locate the GitHub estate root; set GITHUB_ESTATE"
    )


GH = _estate_root()
HERE = Path(__file__).resolve().parent
OUT = HERE / "data" / "h3711.json"


def count_files(p: Path, glob: str = "*") -> int:
    if not p.exists():
        return 0
    if p.is_file():
        return 1
    return sum(1 for x in p.rglob(glob) if x.is_file())


def count_lines(p: Path) -> int:
    n = 0
    with p.open("r", encoding="utf-8", errors="replace") as f:
        for _ in f:
            n += 1
    return n


def probe_somadeva() -> dict:
    san = sorted((GH / "somadeva" / "chapters_san").glob("*.txt"))
    rus = sorted((GH / "somadeva" / "chapters_rus").glob("*.txt"))
    san_lines = sum(count_lines(p) for p in san)
    rus_lines = sum(count_lines(p) for p in rus)
    chapters = []
    for p in san:
        chapters.append({"file": p.name, "lines": count_lines(p)})
    return {
        "path": "somadeva/chapters_san + chapters_rus",
        "san_files": len(san),
        "rus_files": len(rus),
        "san_lines": san_lines,
        "rus_lines": rus_lines,
        "chapters": chapters,
        "ok": len(san) == 18 and len(rus) == 18 and san_lines > 0,
    }


def probe_ors() -> dict:
    path = GH / "ORS-FAQ" / "Tukan_stats.md"
    text = path.read_text(encoding="utf-8") if path.is_file() else ""
    anchors = {
        "dialogs": "3 064",
        "students": "2 794",
        "messages": "46 325",
        "pairs": "38 280",
        "pay": "2 553",
        "price": "1 744",
        "signup": "967",
    }
    missing = [k for k, v in anchors.items() if v not in text]
    return {
        "path": "ORS-FAQ/Tukan_stats.md",
        "present": path.is_file(),
        "missing": missing,
        "ok": path.is_file() and not missing,
        "numbers": {
            "dialogs": 3064,
            "students": 2794,
            "messages": 46325,
            "pairs": 38280,
            "pay": 2553,
            "price": 1744,
            "signup": 967,
        },
        "personal_data": False,
        "note": "public aggregates only; no names",
    }


def probe_ashtadhyayi() -> dict:
    """Fail closed: do not build #18 as a city without full 8-book text."""
    candidates = [
        GH / "ashtadhyayi-com-data",
        GH / "ashtadhyayi",
        GH / "csl-json" / "ashtadhyayi.com",
    ]
    found = [{"path": str(p.relative_to(GH)) if p.exists() else str(p), "exists": p.exists()} for p in candidates]
    sutra = list((GH / "SanskritGrammar").rglob("*ashtadhyayi*") )[:20] if (GH / "SanskritGrammar").exists() else []
    return {
        "full_8book_text": False,
        "candidates": found,
        "sanskritgrammar_hits": [str(p.relative_to(GH)) for p in sutra],
        "decision": "REPLACE with somadeva Kathasaritsagara 18+18 (H3706)",
    }


def probe_prefaces() -> dict:
    names = ["prefaces_ieg", "prefaces_lan", "prefaces_pe", "prefaces_pgn", "prefaces_ae", "prefaces_gst", "prefaces_snp"]
    rows = []
    for name in names:
        plain = GH / name
        promote = GH / (name + "-promote")
        if plain.exists():
            p, via = plain, name
        elif promote.exists():
            p, via = promote, name + "-promote"
        else:
            rows.append({"repo": name, "files": 0, "present": False, "via": None})
            continue
        rows.append({"repo": name, "files": count_files(p), "present": True, "via": via})
    return {"rows": rows, "ok": all(r["present"] and r["files"] > 0 for r in rows)}


def probe_observatory() -> dict:
    p = GH / "csl-observatory"
    if not p.exists():
        return {"present": False, "ok": False}
    md = list(p.rglob("*.md"))
    html = list(p.rglob("*.html"))
    jsons = list(p.rglob("*.json"))
    reports = [x for x in md if "report" in x.name.lower() or "REPORT" in x.name]
    return {
        "present": True,
        "md": len(md),
        "html": len(html),
        "json": len(jsons),
        "reportish_md": len(reports),
        "sample": [x.name for x in (md + html)[:12]],
        "ok": (len(md) + len(html) + len(jsons)) > 0,
    }


def probe_visualdcs() -> dict:
    p = GH / "VisualDCS"
    if not p.exists():
        return {"present": False, "ok": False}
    derived = p / "derived-data" if (p / "derived-data").exists() else p / "derived"
    files = [x for x in p.rglob("*") if x.is_file() and x.suffix.lower() in {".tsv", ".csv", ".json", ".jsonl", ".txt", ".parquet"}]
    by_ext: dict[str, int] = {}
    for f in files:
        by_ext[f.suffix.lower()] = by_ext.get(f.suffix.lower(), 0) + 1
    return {
        "present": True,
        "derived_dir": derived.exists(),
        "data_files": len(files),
        "by_ext": by_ext,
        "sample": [str(x.relative_to(p)) for x in files[:12]],
        "ok": len(files) > 0,
    }


def probe_countvowels() -> dict:
    p = GH / "SanskritSpellCheck" / "CountVowels"
    if not p.exists():
        return {"present": False, "ok": False}
    rows = []
    for f in sorted(p.glob("*.txt")):
        rows.append({"file": f.name, "lines": count_lines(f)})
    return {"path": "SanskritSpellCheck/CountVowels", "rows": rows, "ok": bool(rows)}


def probe_o_vs_O() -> dict:
    hits = []
    ssc = GH / "SanskritSpellCheck"
    if ssc.exists():
        for p in ssc.rglob("*"):
            name = p.name.lower()
            if p.is_file() and ("o_vs_o" in name or "ovsO" in name or "ortho" in name):
                hits.append({"path": str(p.relative_to(GH)), "lines": count_lines(p) if p.suffix in {".tsv", ".txt", ".csv"} else p.stat().st_size})
    return {"hits": hits, "ok": bool(hits)}


def probe_fuzzyalpha() -> dict:
    hits = []
    for root_name in ("SanskritSpellCheck", "hwnorm1", "hwnorm2", "alternateheadwords"):
        root = GH / root_name
        if not root.exists():
            continue
        for p in root.rglob("*"):
            if p.is_file() and "fuzzy" in p.name.lower():
                hits.append({"path": str(p.relative_to(GH)), "bytes": p.stat().st_size})
    return {"hits": hits, "ok": bool(hits)}


def probe_bookindex() -> dict:
    p = GH / "BookIndex"
    if not p.exists():
        return {"present": False, "ok": False}
    md = list(p.rglob("*.md"))
    html = list(p.rglob("*.html"))
    jsons = list(p.rglob("*.json"))
    return {
        "path": "BookIndex",
        "md": len(md),
        "html": len(html),
        "json": len(jsons),
        "ok": len(md) > 0,
    }


def probe_sorting() -> dict:
    p = GH / "SanskritSorting"
    if not p.exists():
        return {"present": False, "ok": False}
    files = [x for x in p.rglob("*") if x.is_file()]
    return {
        "path": "SanskritSorting",
        "files": len(files),
        "sample": [x.name for x in files[:12]],
        "ok": len(files) > 0,
    }


def main() -> int:
    data = {
        "counted": "29.08.2026",
        "ashtadhyayi": probe_ashtadhyayi(),
        "somadeva": probe_somadeva(),
        "ors": probe_ors(),
        "prefaces": probe_prefaces(),
        "observatory": probe_observatory(),
        "visualdcs": probe_visualdcs(),
        "countvowels": probe_countvowels(),
        "o_vs_O": probe_o_vs_O(),
        "fuzzyalpha": probe_fuzzyalpha(),
        "bookindex": probe_bookindex(),
        "sorting": probe_sorting(),
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("wrote", OUT)
    for k, v in data.items():
        if k == "counted":
            continue
        ok = v.get("ok") if isinstance(v, dict) else None
        print(("PASS " if ok else "FAIL " if ok is False else "NOTE ") + k + ": " + json.dumps({x: v[x] for x in v if x not in {"chapters", "rows", "hits", "sample", "sanskritgrammar_hits", "candidates"}} , ensure_ascii=False)[:240])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
