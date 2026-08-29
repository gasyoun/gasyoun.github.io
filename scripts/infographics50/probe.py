#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Count estate facts for the remaining 40 infographics (H3705).

Derive-don't-store: every number in data/infographics50.json is produced here
from local clones under GitHub/. Re-run to refresh. Python 3.9+.
"""
from __future__ import annotations

import collections
import json
import os
import re
import subprocess
import sys
from datetime import date
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

GH = Path(r"C:\Users\user\Documents\GitHub")
HERE = Path(__file__).resolve().parent
OUT = HERE / "data" / "infographics50.json"
SU = GH / "sanskrit-util" / "py"
if SU.exists():
    sys.path.insert(0, str(SU))
from sanskrit_util import from_slp1, slp1_to_devanagari  # noqa: E402

TODAY = date.today().isoformat()
COUNTED = "29.08.2026"

SLP1_HK = {
    "A": "A", "I": "I", "U": "U", "f": "R", "F": "RR", "x": "lR", "X": "lRR",
    "E": "ai", "O": "au", "M": "M", "H": "H",
    "K": "kh", "G": "gh", "N": "G", "C": "ch", "J": "jh", "Y": "J",
    "w": "T", "W": "Th", "q": "D", "Q": "Dh", "R": "N",
    "T": "th", "D": "dh", "P": "ph", "B": "bh",
    "S": "z", "z": "S",
}
SLP1_WX = {
    "A": "A", "I": "I", "U": "U", "f": "q", "F": "Q", "x": "L", "X": "LY",
    "E": "E", "O": "O", "M": "M", "H": "H",
    "K": "K", "G": "G", "N": "f", "C": "C", "J": "J", "Y": "F",
    "w": "t", "W": "T", "q": "d", "Q": "D", "R": "N",
    "t": "w", "T": "W", "d": "x", "D": "X",
    "P": "P", "B": "B", "S": "S", "z": "R",
}


def slp_to_hk(s: str) -> str:
    return "".join(SLP1_HK.get(ch, ch) for ch in s)


def slp_to_wx(s: str) -> str:
    return "".join(SLP1_WX.get(ch, ch) for ch in s)


def run_git(repo: Path, *args: str, timeout: int = 40) -> str:
    r = subprocess.run(
        ["git", "-C", str(repo), *args],
        capture_output=True, text=True, encoding="utf-8",
        errors="replace", timeout=timeout,
    )
    return r.stdout or ""


def count_L(path: Path) -> int:
    n = 0
    with path.open("r", encoding="utf-8", errors="replace") as f:
        for line in f:
            if line.startswith("<L>"):
                n += 1
    return n


def parse_header_date(header: Path) -> str:
    if not header.exists():
        return ""
    t = header.read_text(encoding="utf-8", errors="replace")
    m = re.search(r'<title type="short">.*?<date>([^<]+)</date>', t, re.S)
    if m:
        return m.group(1).strip()
    m = re.search(r"<date>([0-9][^<]{3,20})</date>", t)
    return m.group(1).strip() if m else ""


def parse_header_title(header: Path) -> str:
    if not header.exists():
        return ""
    t = header.read_text(encoding="utf-8", errors="replace")
    m = re.search(r'<title type="main">([^<]+)</title>', t)
    return m.group(1).strip() if m else ""


def dict_lang(title: str) -> str:
    tl = title.lower()
    if "russian" in tl or "русск" in tl:
        return "RU"
    if "german" in tl or "deutsch" in tl or "wörterbuch" in tl or "worterbuch" in tl:
        return "DE"
    if "french" in tl or "français" in tl or "francais" in tl or "dictionnaire" in tl:
        return "FR"
    if "english" in tl:
        return "EN"
    if "sanskrit" in tl and "english" not in tl and "german" not in tl:
        return "SA"
    return "other"


def probe_dicts() -> dict:
    v02 = GH / "csl-orig" / "v02"
    rows = []
    for d in sorted(p for p in v02.iterdir() if p.is_dir() and not p.name.startswith(".")):
        txt = d / (d.name + ".txt")
        if not txt.exists():
            continue
        header = d / (d.name + "header.xml")
        entries = count_L(txt)
        bytes_ = txt.stat().st_size
        title = parse_header_title(header)
        rows.append({
            "code": d.name,
            "entries": entries,
            "bytes": bytes_,
            "print_date": parse_header_date(header),
            "title": title,
            "lang": dict_lang(title),
            "script": str(txt.relative_to(GH)).replace("\\", "/"),
        })
    rows.sort(key=lambda r: -r["entries"])
    return {
        "n_dicts": len(rows),
        "total_entries": sum(r["entries"] for r in rows),
        "total_bytes": sum(r["bytes"] for r in rows),
        "rows": rows,
    }


def probe_mw() -> dict:
    mw = GH / "csl-orig" / "v02" / "mw" / "mw.txt"
    letters = collections.Counter()
    k1s = collections.Counter()
    ls = collections.Counter()
    n_L = 0
    n_s = 0
    n_lex = 0
    n_ls = 0
    sample = None
    k1_re = re.compile(r"<k1>([^<]+)")
    ls_re = re.compile(r"<ls(?:\s[^>]*)?>([^<]+)</ls>")
    s_re = re.compile(r"<s>")
    lex_re = re.compile(r"<lex")
    buf = []
    capture = False
    with mw.open("r", encoding="utf-8", errors="replace") as f:
        for line in f:
            if line.startswith("<L>"):
                n_L += 1
                m = k1_re.search(line)
                if m:
                    k1 = m.group(1)
                    k1s[k1] += 1
                    if k1:
                        letters[k1[0]] += 1
                    if sample is None and k1 == "kfzRa" and "<h>1" in line:
                        capture = True
                        buf = [line.rstrip("\n")]
                continue
            if capture:
                buf.append(line.rstrip("\n"))
                if line.startswith("<LEND>"):
                    capture = False
                    sample = "\n".join(buf)
            n_s += len(s_re.findall(line))
            n_lex += len(lex_re.findall(line))
            for hit in ls_re.findall(line):
                key = hit.strip()
                if key:
                    ls[key] += 1
                    n_ls += 1
    letter_rows = []
    for ch, n in letters.most_common():
        letter_rows.append({
            "slp1": ch,
            "iast": from_slp1(ch),
            "deva": slp1_to_devanagari(ch),
            "n": n,
        })
    cite_rows = [{"ls": k, "n": v} for k, v in ls.most_common(20)]
    anatomy = {}
    if sample:
        anatomy = {
            "k1": "kfzRa",
            "iast": from_slp1("kfzRa"),
            "deva": slp1_to_devanagari("kfzRa"),
            "n_s_tags": len(s_re.findall(sample)),
            "n_lex_tags": len(lex_re.findall(sample)),
            "n_ls_tags": len(ls_re.findall(sample)),
            "n_senses": sample.count("¦"),
            "chars": len(sample),
            "lines": sample.count("\n") + 1,
        }
    return {
        "path": "csl-orig/v02/mw/mw.txt",
        "entries": n_L,
        "unique_k1": len(k1s),
        "n_s_tags": n_s,
        "n_lex_tags": n_lex,
        "n_ls_tags": n_ls,
        "letters": letter_rows,
        "top_ls": cite_rows,
        "anatomy_kfzRa": anatomy,
        "word_encodings": {
            "slp1": "kfzRa",
            "iast": from_slp1("kfzRa"),
            "deva": slp1_to_devanagari("kfzRa"),
            "hk": slp_to_hk("kfzRa"),
            "wx": slp_to_wx("kfzRa"),
        },
    }


def probe_gam() -> dict:
    tables = GH / "MWinflect" / "verbs" / "pysanskritv2" / "tables" / "calc_tables.txt"
    forms = []
    n_rows = 0
    with tables.open("r", encoding="utf-8", errors="replace") as f:
        for line in f:
            parts = line.rstrip("\n").split("\t")
            if len(parts) >= 5 and parts[1] == "gam":
                n_rows += 1
                if parts[0] == "1,a,pre" and parts[3] == "gacC":
                    forms = parts[4].split(":")
    return {
        "path": "MWinflect/verbs/pysanskritv2/tables/calc_tables.txt",
        "gam_rows": n_rows,
        "present_para_gacC": [
            {"slp1": x, "iast": from_slp1(x), "deva": slp1_to_devanagari(x)}
            for x in forms
        ],
    }


def probe_rama() -> dict:
    tables = GH / "MWinflect" / "nominals" / "pysanskritv2" / "tables" / "calc_tables.txt"
    hit = None
    n = 0
    with tables.open("r", encoding="utf-8", errors="replace") as f:
        for line in f:
            n += 1
            if "\trAma\t" in line or line.startswith("m\trAma") or "\trAma," in line:
                if hit is None:
                    hit = line.rstrip("\n")
                if "rAma:" in line or line.count(":") >= 7:
                    hit = line.rstrip("\n")
                    break
    forms = []
    if hit:
        last = hit.split("\t")[-1]
        forms = last.split(":")
    labels = [
        "N sg", "N du", "N pl",
        "A sg", "A du", "A pl",
        "I sg", "I du", "I pl",
        "D sg", "D du", "D pl",
        "Ab sg", "Ab du", "Ab pl",
        "G sg", "G du", "G pl",
        "L sg", "L du", "L pl",
        "V sg", "V du", "V pl",
    ]
    cells = []
    for i, form in enumerate(forms[:24]):
        cells.append({
            "slot": labels[i] if i < len(labels) else str(i),
            "slp1": form,
            "iast": from_slp1(form),
            "deva": slp1_to_devanagari(form),
        })
    return {
        "path": "MWinflect/nominals/pysanskritv2/tables/calc_tables.txt",
        "table_rows": n,
        "raw_hit": bool(hit),
        "cells": cells,
    }


def probe_samasa() -> dict:
    p = GH / "SamasaChakram" / "samasacakra" / "samasacakra-taxonomy.json"
    data = json.loads(p.read_text(encoding="utf-8"))
    classes = []
    n_leaves = 0
    for c in data.get("classes", []):
        leaves = 0
        for fam in c.get("families", []):
            leaves += len(fam.get("leaves", []))
        n_leaves += leaves
        classes.append({
            "id": c.get("id"),
            "name": c.get("name"),
            "leaves": leaves,
            "pradhana": c.get("pradhana", ""),
        })
    return {
        "path": "SamasaChakram/samasacakra/samasacakra-taxonomy.json",
        "n_classes": len(classes),
        "n_leaves": n_leaves,
        "classes": classes,
    }


def probe_sandhi() -> dict:
    p = GH / "kosha" / "data" / "sandhi" / "corpus_sandhi.tsv"
    rows = []
    with p.open("r", encoding="utf-8", errors="replace") as f:
        next(f, None)
        for i, line in enumerate(f):
            if i >= 15:
                break
            cols = line.rstrip("\n").split("\t")
            if len(cols) >= 3:
                rows.append({
                    "rule": cols[0],
                    "category": cols[1],
                    "n": int(cols[2]) if cols[2].isdigit() else cols[2],
                })
    return {
        "path": "kosha/data/sandhi/corpus_sandhi.tsv",
        "top": rows,
    }


def probe_gita() -> dict:
    p = GH / "kosha" / "data" / "gita" / "gita_gold_master.tsv"
    by_ch = collections.Counter()
    lemmas = collections.Counter()
    n = 0
    with p.open("r", encoding="utf-8", errors="replace") as f:
        next(f, None)
        for line in f:
            cols = line.split("\t")
            if len(cols) < 4:
                continue
            n += 1
            verse = cols[0]
            ch = verse.split(".")[0]
            try:
                by_ch[int(ch)] += 1
            except ValueError:
                pass
            lemmas[cols[3]] += 1
    total = n
    running = 0
    curve = []
    for i, (_w, c) in enumerate(lemmas.most_common(), 1):
        running += c
        if i in (1, 10, 25, 50, 100, 200, 500, 1000) or i == len(lemmas):
            curve.append({"k": i, "coverage": round(100.0 * running / total, 2)})
    chapters = [{"ch": k, "n": by_ch[k]} for k in sorted(by_ch)]
    return {
        "path": "kosha/data/gita/gita_gold_master.tsv",
        "n_tokens": total,
        "n_lemmas": len(lemmas),
        "n_chapters": len(by_ch),
        "chapters": chapters,
        "coverage_curve": curve,
        "top100_coverage": next((x["coverage"] for x in curve if x["k"] == 100), None),
    }


def probe_sundara() -> dict:
    p = GH / "CommentaryStrategies" / "data" / "leonov_own_notes.json"
    meta = {}
    with p.open("r", encoding="utf-8", errors="replace") as f:
        # only the _meta object — never load note bodies into the page pipeline
        chunk = f.read(4000)
    m = re.search(r'"total_notes":\s*(\d+)', chunk)
    s = re.search(r'"sargas_covered":\s*(\d+)', chunk)
    v = re.search(r'"verses_with_note":\s*(\d+)', chunk)
    k = re.search(r'"kostina":\s*(\d+)', chunk)
    nul = re.search(r'"null":\s*(\d+)', chunk)
    meta = {
        "total_notes": int(m.group(1)) if m else None,
        "sargas_covered": int(s.group(1)) if s else None,
        "verses_with_note": int(v.group(1)) if v else None,
        "kostina": int(k.group(1)) if k else None,
        "unattributed_in_json": int(nul.group(1)) if nul else None,
    }
    return {
        "path": "CommentaryStrategies/data/leonov_own_notes.json",
        "meta_only": True,
        **meta,
    }


def probe_corpora() -> dict:
    out = {}
    dcs = GH / "dcs-conllu"
    if dcs.exists():
        n = 0
        for p in dcs.rglob("*.conllu"):
            n += 1
        out["dcs_conllu_files"] = n
        out["dcs_path"] = "dcs-conllu"
    pc = GH / "Parallel-Sanskrit-Corpora"
    if pc.exists():
        n = 0
        for p in pc.rglob("*"):
            if p.is_file() and p.suffix.lower() in {".txt", ".tsv", ".json", ".xml"}:
                n += 1
        out["parallel_text_files"] = n
        out["parallel_path"] = "Parallel-Sanskrit-Corpora"
    tg = GH / "telegram-sanskrit-corpus"
    if tg.exists():
        n = 0
        for p in tg.rglob("*"):
            if p.is_file():
                n += 1
        out["telegram_files"] = n
        out["telegram_path"] = "telegram-sanskrit-corpus"
    return out


def probe_registry() -> dict:
    readme = GH / "Uprava" / "handoffs" / "README.md"
    archive = GH / "Uprava" / "handoffs" / "REGISTRY_ARCHIVE.md"
    fam = collections.Counter()
    n_rows = 0
    pat = re.compile(r"\| H(\d+) \|")
    fam_pat = re.compile(r"H\d+-([A-Za-z0-9]+)_")
    for path in (readme, archive):
        if not path.exists():
            continue
        for line in path.open("r", encoding="utf-8", errors="replace"):
            if not pat.search(line):
                continue
            n_rows += 1
            m = fam_pat.search(line)
            if m:
                fam[m.group(1)] += 1
    gtd = GH / "Uprava" / "GTD_NEXT_ACTIONS.md"
    tags = {"@DO": 0, "@DECIDE": 0, "@WAITING": 0}
    if gtd.exists():
        text = gtd.read_text(encoding="utf-8", errors="replace")
        for t in tags:
            tags[t] = text.count(t)
    return {
        "handoff_rows": n_rows,
        "by_family": dict(fam.most_common()),
        "gtd": tags,
        "paths": [
            "Uprava/handoffs/README.md",
            "Uprava/handoffs/REGISTRY_ARCHIVE.md",
            "Uprava/GTD_NEXT_ACTIONS.md",
        ],
    }


def probe_ci_and_git() -> dict:
    repos = [
        "Uprava", "kosha", "SanskritGrammar", "SanskritLexicography",
        "CommentaryStrategies", "SanskritKaraoke", "SanskritSpellCheck",
        "Systema-Sanscriticum", "IndologyScholars", "gasyoun.github.io",
        "ORS-FAQ", "SamudraManthanam",
    ]
    wf = 0
    wf_repos = 0
    by_day = collections.Counter()
    by_repo = []
    first_dates = []
    for name in repos:
        repo = GH / name
        if not (repo / ".git").exists() and not (repo / ".git").is_file():
            continue
        wdir = repo / ".github" / "workflows"
        n_wf = 0
        if wdir.exists():
            n_wf = len(list(wdir.glob("*.yml"))) + len(list(wdir.glob("*.yaml")))
            if n_wf:
                wf_repos += 1
                wf += n_wf
        try:
            log = run_git(repo, "log", "--since=2025-01-01", "--pretty=%ad",
                          "--date=short", timeout=25)
        except Exception:
            log = ""
        days = [ln.strip() for ln in log.splitlines() if ln.strip()]
        for d in days:
            by_day[d] += 1
        by_repo.append({"repo": name, "commits_since_2025": len(days), "workflows": n_wf})
        try:
            first = run_git(repo, "log", "--reverse", "--pretty=%ad",
                            "--date=short", "-1", timeout=20).strip()
        except Exception:
            first = ""
        if first:
            first_dates.append({"repo": name, "first": first})
    # weekday heatmap 2025-2026
    heat = [[0] * 53 for _ in range(7)]
    for d, n in by_day.items():
        try:
            y, m, dd = (int(x) for x in d.split("-"))
            dt = date(y, m, dd)
        except Exception:
            continue
        if dt.year < 2025:
            continue
        week = min(dt.isocalendar()[1] - 1, 52)
        heat[dt.weekday()][week] += n
    return {
        "repos": by_repo,
        "n_workflows": wf,
        "n_repos_with_workflows": wf_repos,
        "commits_since_2025": sum(r["commits_since_2025"] for r in by_repo),
        "first_dates": first_dates,
        "heat_weekday_week": heat,
        "note": "commit census is the 12 named public/local clones, not the full ~85 estate",
    }


def probe_systema() -> dict:
    root = GH / "Systema-Sanscriticum"
    decks = 0
    csvs = 0
    seed = root / "database" / "seeders" / "data"
    if seed.exists():
        for p in seed.rglob("manifest.json"):
            decks += 1
        for p in seed.rglob("*.csv"):
            csvs += 1
    return {
        "path": "Systema-Sanscriticum/database/seeders/data",
        "manifests": decks,
        "csv_files": csvs,
    }


def probe_indology() -> dict:
    root = GH / "IndologyScholars"
    md = 0
    if root.exists():
        for p in root.rglob("*.md"):
            if ".git" in p.parts:
                continue
            md += 1
    return {
        "path": "IndologyScholars",
        "md_files": md,
    }


def probe_countvowels() -> dict:
    root = GH / "SanskritSpellCheck" / "CountVowels"
    rows = []
    for p in sorted(root.glob("*-CVC-SLP1.txt")):
        n = 0
        with p.open("r", encoding="utf-8", errors="replace") as f:
            for _ in f:
                n += 1
        rows.append({"file": p.name, "lines": n})
    return {
        "path": "SanskritSpellCheck/CountVowels",
        "rows": rows,
    }


def probe_prefaces() -> dict:
    names = ["prefaces_ieg", "prefaces_lan", "prefaces_pe", "prefaces_pgn",
             "prefaces_ae", "prefaces_gst", "prefaces_snp"]
    rows = []
    for name in names:
        d = GH / name
        n = 0
        if d.exists():
            for p in d.rglob("*"):
                if p.is_file() and ".git" not in p.parts:
                    n += 1
        rows.append({"repo": name, "files": n, "present": d.exists()})
    return {"rows": rows}


def probe_bookindex() -> dict:
    d = GH / "BookIndex"
    n = 0
    if d.exists():
        for p in d.rglob("*.md"):
            if ".git" in p.parts:
                continue
            n += 1
    return {"path": "BookIndex", "md_files": n}


def probe_typos() -> dict:
    p = GH / "SanskritSpellCheck" / "detectors" / "gold_corrections.tsv"
    n = 0
    kinds = collections.Counter()
    if p.exists():
        with p.open("r", encoding="utf-8", errors="replace") as f:
            header = f.readline()
            cols = header.strip().split("\t")
            kind_i = 0
            for i, c in enumerate(cols):
                if "type" in c.lower() or "kind" in c.lower() or "class" in c.lower():
                    kind_i = i
            for line in f:
                n += 1
                parts = line.split("\t")
                if kind_i < len(parts):
                    kinds[parts[kind_i].strip() or "unspecified"] += 1
    top = [{"kind": k, "n": v} for k, v in kinds.most_common(12)]
    return {
        "path": "SanskritSpellCheck/detectors/gold_corrections.tsv",
        "n": n,
        "top_kinds": top,
    }


def probe_sanhw1_letters() -> dict:
    p = GH / "SanskritSpellCheck" / "sanhw1.txt"
    letters = collections.Counter()
    n = 0
    with p.open("r", encoding="utf-8", errors="replace") as f:
        for line in f:
            n += 1
            tok = line.split(":")[0].strip() if ":" in line else line.split()[0] if line.strip() else ""
            if tok:
                letters[tok[0]] += 1
    rows = []
    for ch, c in letters.most_common():
        if not re.match(r"[A-Za-z]", ch):
            continue
        rows.append({
            "slp1": ch,
            "iast": from_slp1(ch),
            "deva": slp1_to_devanagari(ch),
            "n": c,
        })
    return {
        "path": "SanskritSpellCheck/sanhw1.txt",
        "n_headwords": n,
        "letters": rows[:50],
    }


def probe_grammar_chapters() -> dict:
    root = GH / "SanskritGrammar"
    n = 0
    if root.exists():
        for p in root.rglob("*.md"):
            if ".git" in p.parts:
                continue
            n += 1
    return {"path": "SanskritGrammar", "md_files": n}


def probe_astadhyayi_sandhi() -> dict:
    p = GH / "kosha" / "data" / "sandhi" / "astadhyayi_sandhi.tsv"
    rows = []
    total = 0
    with p.open("r", encoding="utf-8", errors="replace") as f:
        next(f, None)
        for i, line in enumerate(f):
            cols = line.split("\t")
            if len(cols) >= 3 and cols[2].isdigit():
                n = int(cols[2])
                total += n
                if i < 12:
                    rows.append({"rule": cols[0], "category": cols[1], "n": n})
    return {
        "path": "kosha/data/sandhi/astadhyayi_sandhi.tsv",
        "top": rows,
        "sum_top_file_counts": total,
        "full_8book_text": False,
    }


def main() -> int:
    print("probing dicts…", flush=True)
    dicts = probe_dicts()
    print("  %s dicts, %s entries" % (dicts["n_dicts"], dicts["total_entries"]), flush=True)
    print("probing MW…", flush=True)
    mw = probe_mw()
    print("  MW L=%s k1=%s ls=%s" % (mw["entries"], mw["unique_k1"], mw["n_ls_tags"]), flush=True)
    blob = {
        "counted": COUNTED,
        "iso": TODAY,
        "dicts": dicts,
        "mw": mw,
        "gam": probe_gam(),
        "rama": probe_rama(),
        "samasa": probe_samasa(),
        "sandhi": probe_sandhi(),
        "gita": probe_gita(),
        "sundara": probe_sundara(),
        "corpora": probe_corpora(),
        "registry": probe_registry(),
        "git": probe_ci_and_git(),
        "systema": probe_systema(),
        "indology": probe_indology(),
        "countvowels": probe_countvowels(),
        "prefaces": probe_prefaces(),
        "bookindex": probe_bookindex(),
        "typos": probe_typos(),
        "sanhw1": probe_sanhw1_letters(),
        "grammar": probe_grammar_chapters(),
        "astadhyayi_sandhi": probe_astadhyayi_sandhi(),
        "external_cited": {
            "oed_entries": 520779,
            "oed_source": "https://en.wikipedia.org/wiki/Oxford_English_Dictionary (as of January 2026)",
            "dwb_headwords": 330000,
            "dwb_source": "https://en.wikipedia.org/wiki/Deutsches_W%C3%B6rterbuch (first completed DWB)",
            "duden_27_words": 145000,
            "duden_source": "Welt, 19.08.2017, Duden 27. Auflage",
        },
        "replacements": {
            "18": {
                "reason": "no verified full 8-book sūtra text on this box",
                "instead": "countvowels epic CVC census + astadhyayi_sandhi.tsv top rules (not a city of 8 books)",
            },
            "27": {
                "reason": "no anonymized public ORS funnel aggregates in-repo without personal-data risk",
                "instead": "prefaces_* 7-repo file census",
            },
        },
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(blob, ensure_ascii=False, indent=2), encoding="utf-8")
    print("wrote", OUT, flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
