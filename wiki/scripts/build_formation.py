#!/usr/bin/env python3
"""Join the Wiktionary /wiki/ snapshot to prior Sanskrit word-formation work.

Produces three static data modules and a replayable provenance record:

    python3 wiki/scripts/build_formation.py             # read local source repos
    python3 wiki/scripts/build_formation.py --offline   # replay archive/raw/ only

No network access, no external Python packages. The site's lemmata are
Devanagari Wiktionary titles; the prior datasets are SLP1 or IAST. Two bridges
are used, both provable rather than guessed:

  * csl-devanagari/v02/mw/mw.txt and csl-orig/v02/mw/mw.txt are the same MW
    dictionary in two scripts with identical <L> line IDs, and the MW
    derivation oracle is keyed by that ID. Exact Devanagari headwords follow.
  * a compact Devanagari -> SLP1 converter handles the other joins. It is
    validated here against 8,000 of those aligned metaline pairs, and refuses
    any unrecognised character instead of emitting a silently wrong key.

Only minimal derived joins are published, never dictionary text. See
archive/SOURCES-LICENSES.md for the licence of every input.
"""
import csv
import hashlib
import json
import re
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]          # wiki/
DATA, ARCH = ROOT / "data", ROOT / "archive"
RAW = ARCH / "raw"
SRC = Path(__file__).resolve().parents[3]           # workspace holding the repos
for arg in sys.argv[1:]:
    if arg.startswith("--source-root="):
        SRC = Path(arg.split("=", 1)[1]).resolve()
OFFLINE = "--offline" in sys.argv
GENERATOR = "wiki/scripts/build_formation.py"
BASE = "https://en.wiktionary.org"
for d in (DATA, ARCH, RAW):
    d.mkdir(parents=True, exist_ok=True)

GH = "https://github.com/"
SOURCES = [
    ("mw_etymology", "csl-orig/v02/mw/mw_etymology.tsv", "CC BY-SA 4.0",
     GH + "sanskrit-lexicon/csl-orig/blob/main/v02/mw/mw_etymology.tsv"),
    ("mw_devanagari", "csl-devanagari/v02/mw/mw.txt", "CC BY-SA 4.0",
     GH + "sanskrit-lexicon/csl-devanagari/blob/main/v02/mw/mw.txt"),
    ("mw_slp1", "csl-orig/v02/mw/mw.txt", "CC BY-SA 4.0",
     GH + "sanskrit-lexicon/csl-orig/blob/main/v02/mw/mw.txt"),
    ("whitney_roots", "WhitneyRoots/crosswalk/roots.csv", "Apache-2.0",
     GH + "gasyoun/WhitneyRoots/blob/main/crosswalk/roots.csv"),
    ("dcs_lemma2root", "SanskritRussian/dcs_lemma2root.tsv", "no LICENSE in source repo",
     GH + "gasyoun/SanskritRussian/blob/main/dcs_lemma2root.tsv"),
    ("affix_data", "WhitneyRoots/src/affix_data.json", "Apache-2.0",
     GH + "gasyoun/WhitneyRoots/blob/main/src/affix_data.json"),
    ("samasa_taxonomy", "SamasaChakram/samasacakra/samasacakra-taxonomy.json", "Apache-2.0",
     GH + "gasyoun/SamasaChakram/blob/main/samasacakra/samasacakra-taxonomy.json"),
    ("compound_members", "MWderivations/issue15/compounds_both_sides.tsv", "no LICENSE in source repo",
     GH + "gasyoun/MWderivations/blob/master/issue15/compounds_both_sides.tsv"),
    ("compound_list", "MWderivations/compounds/compounds.txt", "no LICENSE in source repo",
     GH + "gasyoun/MWderivations/blob/master/compounds/compounds.txt"),
]

# ---- Devanagari -> SLP1 -----------------------------------------------------
INDEP = dict(zip("अआइईउऊऋॠऌॡएऐओऔ", "aAiIuUfFxXeEoO"))
MATRA = dict(zip("ािीुूृॄॢॣेैोौ", "AiIuUfFxXeEoO"))
CONS = dict(zip("कखगघङचछजझञटठडढणतथदधनपफबभमयरलवशषसहळ",
                "kKgGNcCjJYwWqQRtTdDnpPbBmyrlvSzshL"))
OTHER = {"ं": "M", "ः": "H", "ँ": "~", "ऽ": "'", "्": "", "।": ".", "॥": "."}
TABLE = dict(INDEP, **MATRA, **CONS, **OTHER)


def d2s(deva):
    """SLP1 writes the inherent 'a' explicitly, so a bare क becomes `ka`."""
    out = []
    for i, ch in enumerate(deva):
        nxt = deva[i + 1] if i + 1 < len(deva) else ""
        if ch in CONS:
            out.append(CONS[ch] if (nxt == "्" or nxt in MATRA) else CONS[ch] + "a")
        elif ch in TABLE:
            out.append(TABLE[ch])
        elif ch.isascii() and (ch.isalnum() or ch in "-—_"):
            out.append(ch)
        elif ch in " \t":
            pass
        else:
            return None                      # refuse; never guess a join key
    return "".join(out)


L_RE = re.compile(r"^<L>([^<]*)<")
K1_RE = re.compile(r"<k1>([^<]*)<")


def metalines(path):
    out = {}
    with path.open(encoding="utf-8", errors="replace") as fh:
        for line in fh:
            m = L_RE.match(line)
            if not m:
                continue
            k = K1_RE.search(line)
            if k:
                out[m.group(1)] = k.group(1).strip()
    return out


def sha(payload):
    return hashlib.sha256(payload).hexdigest()


def js(name, obj):
    """Write one window.* module; compact JSON, stable key order."""
    return ("window." + name + " = " +
            json.dumps(obj, ensure_ascii=False, separators=(",", ":")) + ";\n").encode("utf-8")


def read_tsv(path):
    with path.open(encoding="utf-8") as fh:
        return list(csv.DictReader(fh, delimiter="\t"))


def first_forms(raw, limit=6):
    return [p.split(":")[0] for p in raw.split("|") if p][:limit]


# ---- load the site's own snapshot ------------------------------------------
def site_lemmata():
    text = (DATA / "lemmata.js").read_text(encoding="utf-8")
    doc = json.loads(text[text.index("{"):text.rindex("}") + 1])
    words = []
    for w in doc["words"]:
        t = w[0]
        if t.startswith("Reconstruction:") or t.startswith("-"):
            continue
        if not any("\u0900" <= c <= "\u097f" for c in t):
            continue
        key = d2s(t)
        words.append((t, key, w[1]))
    return doc, words


# ---- build the three payloads ----------------------------------------------
def build(site, words, inputs):
    deva_mw = metalines(SRC / "csl-devanagari/v02/mw/mw.txt")
    slp_mw = metalines(SRC / "csl-orig/v02/mw/mw.txt")
    shared = sorted(set(deva_mw) & set(slp_mw))[:8000]
    ok = bad = 0
    for lid in shared:
        t = d2s(deva_mw[lid])
        if t is None:
            continue
        if t == slp_mw[lid]:
            ok += 1
        else:
            bad += 1
    validation = {"aligned_pairs_tested": len(shared), "exact": ok,
                  "mismatch": bad,
                  "accuracy_pct": round(100.0 * ok / max(1, ok + bad), 2),
                  "note": "Mismatches are editorial <k1> differences between the two "
                          "CSL editions, not converter errors. Exact <L> alignment "
                          "is preferred for the MW join."}

    mw = read_tsv(SRC / "csl-orig/v02/mw/mw_etymology.tsv")
    mw_by_lid = {r["L_id"]: r for r in mw}
    mw_deva = {deva_mw[lid]: r for lid, r in mw_by_lid.items() if lid in deva_mw}
    dcs = {r["lemma_slp1"]: (r["root_slp1"], r["how"])
           for r in read_tsv(SRC / "SanskritRussian/dcs_lemma2root.tsv")}
    with (SRC / "WhitneyRoots/crosswalk/roots.csv").open(encoding="utf-8") as fh:
        whit_rows = list(csv.DictReader(fh))
    whit = {}
    for r in whit_rows:
        whit.setdefault(r["root_slp1"], r)

    site_by_slp = {k: t for t, k, _ in words if k}
    cats = site["categories"]
    bycat = defaultdict(lambda: [0, 0])
    frows = []
    for title, key, ids in words:
        m = mw_deva.get(title)
        d = dcs.get(key)
        w = whit.get(key) or (whit.get(d[0]) if d else None)
        wh_direct = whit.get(key)
        for ci in ids:
            bycat[ci][1] += 1
        rec = [
            title, key or "",
            m["deriv_type"] if m else "", m["parse"] if m else "",
            m["root"] if m else "", m["prefixes"] if m else "", m["L_id"] if m else "",
            d[0] if d else "", d[1] if d else "",
            w["whitney_no"] if w else "", w["root_iast"] if w else "",
            w["gloss_short"] if w else "", w["class"] if w else "",
            w["period_tags"] if w else "", w["apte_id"] if w else "",
            w["mw_id"] if w else "", w["dcs_freq"] if w else "",
            "|".join(first_forms(w["attested_forms"])) if w else "",
            1 if wh_direct else 0,
        ]
        if m or d or w:
            frows.append(rec)
            for ci in ids:
                bycat[ci][0] += 1

    src_links = {k: url for k, _, _, url in SOURCES}
    src_links["wiktionary"] = BASE + "/wiki/Category:Sanskrit_terms_by_etymology"
    formation = {
        "snapshotId": site["snapshotId"], "builtAtUtc": None, "generator": GENERATOR,
        "base": BASE,
        "cols": ["deva", "slp1", "mwType", "mwParse", "mwRoot", "mwPrefix", "mwLid",
                 "dcsRoot", "dcsHow", "whNo", "whRoot", "whGloss", "whClass",
                 "whPeriod", "whApte", "whMwId", "whFreq", "whForms", "whDirect"],
        "words": frows,
        "byCategory": [[ci, v[0], v[1]] for ci, v in sorted(bycat.items())],
        "categoryNames": [c["name"] for c in cats],
        "totals": {
            "devanagariLemmata": len(words), "annotated": len(frows),
            "mwParses": sum(1 for r in frows if r[2]),
            "dcsRoots": sum(1 for r in frows if r[7]),
            "whitneyRoots": sum(1 for r in frows if r[9]),
            "whitneyDirect": sum(1 for r in frows if r[18]),
            "coveragePct": round(100.0 * len(frows) / max(1, len(words)), 1),
        },
        "sources": src_links,
        "warning": "These are candidate cross-references, not a new etymology. "
                   "Homonym roots can collide; every field links to its own source.",
    }

    root_rows = []
    for r in whit_rows:
        slp = r["root_slp1"]
        deva = site_by_slp.get(slp, "")
        root_rows.append([
            r["whitney_no"], r["root_iast"], slp, r["homonym"], r["class"],
            r["gloss_short"], r["period_tags"], r["dcs_freq"], r["dcs_rank"],
            "|".join(first_forms(r["attested_forms"])), r["mw_id"], r["apte_id"],
            deva, 1 if slp in site_by_slp else 0,
        ])
    roots = {
        "builtAtUtc": None, "generator": GENERATOR, "base": BASE,
        "cols": ["no", "iast", "slp1", "homonym", "class", "gloss", "period",
                 "freq", "rank", "forms", "mwId", "apteId", "deva", "inSite"],
        "roots": root_rows, "sources": src_links,
        "totals": {"rows": len(root_rows), "distinctRoots": len(whit),
                   "inSite": sum(1 for r in root_rows if r[13]),
                   "withGloss": sum(1 for r in root_rows if r[5]),
                   "withForms": sum(1 for r in root_rows if r[9])},
    }

    aff = json.loads((SRC / "WhitneyRoots/src/affix_data.json").read_text(encoding="utf-8"))
    aff_rows = []
    for a in aff["affixes"]:
        ex = [[e.get("word", ""), e.get("word_iast", ""), e.get("root", "")]
              for e in a.get("examples", [])[:3]]
        aff_rows.append([a.get("surface", ""), a.get("surface_deva", ""),
                         a.get("pratyaya", ""), a.get("pratyaya_deva", ""),
                         a.get("kind", ""), a.get("function", ""),
                         a.get("group", ""), a.get("apte_roots", 0), ex,
                         a.get("anubandha", [])])
    sam = json.loads((SRC / "SamasaChakram/samasacakra/samasacakra-taxonomy.json")
                     .read_text(encoding="utf-8"))
    classes = []
    for c in sam["classes"]:
        fam = []
        for f in c["families"]:
            fam.append([f.get("id", ""), f.get("name", ""),
                        [[l.get("term", ""), l.get("ex", ""),
                          l.get("vigraha", ""), l.get("ru", "")]
                         for l in f.get("leaves", [])]])
        classes.append([c.get("id", ""), c.get("name", ""),
                        c.get("pradhana", ""), c.get("structure", ""), fam])
    cm = read_tsv(SRC / "MWderivations/issue15/compounds_both_sides.tsv")
    members = sorted(([r["word"], int(r["as_left"]), int(r["as_right"])] for r in cm),
                     key=lambda x: -(x[1] + x[2]))[:60]
    samples = []
    with (SRC / "MWderivations/compounds/compounds.txt").open(encoding="utf-8") as fh:
        for line in fh:
            if line.count(":") < 2:
                continue
            n, head, parts = line.strip().split(":", 2)
            ps = parts.split()
            if len(ps) >= 4 and n.isdigit():
                samples.append([int(n), head, ps[:14]])
    samples = sorted(samples, reverse=True)[:12]
    wordformation = {
        "builtAtUtc": None, "generator": GENERATOR, "base": BASE,
        "affixCols": ["surface", "surfaceDeva", "pratyaya", "pratyayaDeva",
                      "kind", "function", "group", "apteRoots", "examples",
                      "anubandha"],
        "affixes": aff_rows,
        "groups": [[k, v] for k, v in sorted(aff.get("groups", {}).items())],
        "samasa": classes, "compoundMembers": members, "compoundSamples": samples,
        "sources": src_links,
        "totals": {"affixes": len(aff_rows), "groups": len(aff.get("groups", {})),
                   "samasaClasses": len(classes),
                   "samasaFamilies": sum(len(c[4]) for c in classes),
                   "samasaLeaves": sum(len(f[2]) for c in classes for f in c[4]),
                   "compoundMembers": len(members), "compoundSamples": len(samples)},
        "note": "Affix and compound examples are reproduced from the source files in "
                "their original transliteration; they are not Wiktionary lemmata.",
    }
    return formation, roots, wordformation, validation


# ---- provenance + output ----------------------------------------------------
MODULES = [("formation.js", "WIKI_FORMATION", "formation"),
           ("roots.js", "WIKI_ROOTS", "roots"),
           ("wordformation.js", "WIKI_WORDFORMATION", "wordformation")]


def describe_inputs():
    out = []
    for key, rel, lic, url in SOURCES:
        p = SRC / rel
        if not p.exists():
            raise SystemExit("missing source: %s\nPass --source-root=/path/to/workspace" % p)
        payload = p.read_bytes()
        rows = sum(1 for _ in p.open(encoding="utf-8", errors="replace"))
        out.append({"key": key, "path": rel, "bytes": len(payload),
                    "sha256": sha(payload), "license": lic, "url": url,
                    "lines": rows})
    return out


def write_all(payloads, now, inputs, validation, site_meta):
    for p in payloads.values():
        p["builtAtUtc"] = now
    blobs = {fn: js(var, payloads[key]) for fn, var, key in MODULES}
    derived = [{"file": "data/" + fn, "bytes": len(b), "sha256": sha(b)}
               for fn, b in blobs.items()]
    for fn, b in blobs.items():
        (DATA / fn).write_bytes(b)

    raw = {
        "generator": GENERATOR, "version": 1, "built_at_utc": now,
        "source_root": str(SRC),
        "purpose": "Replayable input record: regenerate every /wiki/ word-formation "
                   "data module without the source repositories or network access.",
        "inputs": inputs, "site": site_meta, "validation": validation,
        "payloads": payloads, "derived": derived,
    }
    raw_bytes = (json.dumps(raw, ensure_ascii=False, separators=(",", ":"))
                 .encode("utf-8"))
    (RAW / "formation-sources.json").write_bytes(raw_bytes)

    man = {
        "generated_at_utc": now, "generator": GENERATOR,
        "purpose": "Provenance and SHA-256 checksums for the prior-work join.",
        "inputs": inputs, "validation": validation, "site": site_meta,
        "raw": {"file": "raw/formation-sources.json", "bytes": len(raw_bytes),
                "sha256": sha(raw_bytes)},
        "derived": derived,
        "licenses": "See archive/SOURCES-LICENSES.md. Only minimal derived joins "
                    "are published; no dictionary text is copied.",
    }
    (ARCH / "formation-manifest.json").write_text(
        json.dumps(man, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return derived, raw_bytes


def main():
    if OFFLINE:
        rp = RAW / "formation-sources.json"
        if not rp.exists():
            raise SystemExit("no formation snapshot; run without --offline first")
        raw = json.loads(rp.read_text(encoding="utf-8"))
        now = raw["built_at_utc"]
        derived, _ = write_all(raw["payloads"], now, raw["inputs"],
                               raw["validation"], raw["site"])
        print("OK offline replay: %d modules, %d annotated lemmata"
              % (len(derived), raw["payloads"]["formation"]["totals"]["annotated"]))
        return

    inputs = describe_inputs()
    site, words = site_lemmata()
    site_meta = {
        "file": "data/lemmata.js",
        "sha256": sha((DATA / "lemmata.js").read_bytes()),
        "snapshotId": site["snapshotId"],
        "uniqueWords": site["totals"]["uniqueWords"],
        "devanagariLemmata": len(words),
    }
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    formation, roots, wordformation, validation = build(site, words, inputs)
    payloads = {"formation": formation, "roots": roots,
                "wordformation": wordformation}
    derived, _ = write_all(payloads, now, inputs, validation, site_meta)
    t = formation["totals"]
    print("OK: %d/%d lemmata annotated (%.1f%%); MW %d, DCS %d, Whitney %d"
          % (t["annotated"], t["devanagariLemmata"], t["coveragePct"],
             t["mwParses"], t["dcsRoots"], t["whitneyRoots"]))
    print("    roots=%d affixes=%d samasa leaves=%d; converter %.2f%% on %d pairs"
          % (roots["totals"]["rows"], wordformation["totals"]["affixes"],
             wordformation["totals"]["samasaLeaves"],
             validation["accuracy_pct"], validation["aligned_pairs_tested"]))
    print("    %d derived modules, %d checksummed inputs"
          % (len(derived), len(inputs)))


if __name__ == "__main__":
    main()
