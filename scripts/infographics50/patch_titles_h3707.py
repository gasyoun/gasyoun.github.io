#!/usr/bin/env python3
"""H3707 one-shot: re-derive time-invariant fields of data/infographics50.json.

The committed JSON is the counted-29.08.2026 state; counts stay untouched.
Only fields that are pure functions of file content (titles, languages, the
raw anatomy record) are re-derived here with the FIXED parse_header_title /
dict_lang from probe.py. Run from repo root:
    python3 scripts/infographics50/patch_titles_h3707.py
"""
from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("probe", HERE / "probe.py")
probe = importlib.util.module_from_spec(spec)
spec.loader.exec_module(probe)

OUT = HERE / "data" / "infographics50.json"
data = json.loads(OUT.read_text(encoding="utf-8"))

changed = []
for row in data["dicts"]["rows"]:
    header = probe.GH / "csl-orig" / "v02" / row["code"] / (row["code"] + "header.xml")
    title = probe.parse_header_title(header)
    lang = probe.dict_lang(title, header)
    if title != row["title"] or lang != row["lang"]:
        changed.append((row["code"], row["title"], row["lang"], title, lang))
        row["title"] = title
        row["lang"] = lang

a = data["mw"]["anatomy_kfzRa"]
raw = a.get("raw")
if not raw:
    # re-extract the counted record and verify it against the counted counts
    mw = probe.GH / "csl-orig" / "v02" / "mw" / "mw.txt"
    buf = []
    capture = False
    with mw.open("r", encoding="utf-8", errors="replace") as f:
        for line in f:
            if line.startswith("<L>"):
                capture = "<k1>kfzRa<" in line and "<h>1" in line
                if capture:
                    buf = [line.rstrip("\n")]
                continue
            if capture:
                buf.append(line.rstrip("\n"))
                if line.startswith("<LEND>"):
                    break
    raw = "\n".join(buf)
    n_s = len(__import__("re").findall(r"<s>", raw))
    n_lex = len(__import__("re").findall(r"<lex", raw))
    n_ls = len(__import__("re").findall(r"<ls(?:\s[^>]*)?>[^<]+</ls>", raw))
    assert raw.count("¦") == a["n_senses"], "sense drift in counted record"
    assert len(raw) == a["chars"], f"char drift: {len(raw)} != {a['chars']}"
    assert (raw.count("\n") + 1) == a["lines"], "line drift"
    assert n_s == a["n_s_tags"] and n_lex == a["n_lex_tags"] and n_ls == a["n_ls_tags"], "tag drift"
    a["raw"] = raw
    changed.append(("mw.anatomy_kfzRa", "-", "-", "raw record added", f"{a['chars']} chars verified"))

OUT.write_text(json.dumps(data, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
for code, ot, ol, nt, nl in changed:
    print(f"{code}: '{ot}'/{ol} -> '{nt}'/{nl}")
print(len(changed), "fields updated")
