#!/usr/bin/env python3
"""Add the missing EXTERNAL channels to the DSG core-term study.

The question this answers
-------------------------
    "Does the 3 include frequency in grammars? DCS as well 4th?"

Short answer: **no**, and DCS is not a fourth channel *of the same kind*.

The original three (``pc`` / ``an`` / ``ad``) are three STRUCTURAL POSITIONS
inside one text, the 3,983 sūtras of the Aṣṭādhyāyī:

    pc  explicitly written in the padaccheda
    an  carried forward by anuvṛtti
    ad  supplied by a governing adhikāra

They are not three corpora, so they cannot contain "frequency in grammars".
Frequency in grammatical treatises was never measured. DCS was used only
indirectly -- the estate's DIFFICULTY_ORDERING_RESULT.md supplied the
function-word-exclusion principle -- and never appeared as a column in
core_terms.tsv.

This script measures three genuinely external dimensions:

    G  vyākaraṇa corpus frequency
       12,627 Sanskrit passages from Mahābhāṣya, Siddhāntakaumudī,
       Laghukaumudī, Bālamanoramā, Vākyapadīya + vṛttis, Bhūṣaṇasāra,
       Phitsūtras (ashtadhyayi-com/data). Unit = one passage/chunk/verse;
       document frequency (df) and token frequency (tf).

    L  DSG lexicographic salience
       mentions of the term across all 4,383 Abhyankar entries, measured in
       three independent fields: English prose (diacritic-folded), Russian
       prose (collision control for short Latin stems) and Devanāgarī
       headwords (with class-nasal <-> anusvāra variants). Plus citation
       counts (P., M.Bh., Kāśikā, Vārttika, Prātiśākhya) and entry length.

    D  DCS literary-corpus frequency
       the locally available DCS-2026 lemma ranking table
       (sanskrit-util/tools/KeySwap/data/dcs_freq.txt; 50,474 keys).
       Used as a REGISTER CONTROL / negative control, not as a co-equal
       fourth structural channel.

Data-quality fix (this revision)
--------------------------------
DSG's column labelled ``slp1`` is Harvard-Kyoto, NOT SLP1.  See
``slp1_keys.py`` and ``dsg_dcs_join.tsv``.  All DCS joins now use derived
SLP1 keys with class-nasal <-> anusvāra spelling variants.  The ten short
stems (``ca``, ``na``, ``vā``, ``iti``, ``api``, ``it``, ``bha``, ``sup``,
``tiṅ``, ``kṛt``) are no longer reported as "not measurable": they are
measured with a documented rule in three fields, with the English-prose
collision shown explicitly rather than hidden.

Outputs (all in this folder):
       external_channels.tsv    119 terms x every channel
       external_channels.json   metadata, corpus inventory, rank correlations
       external_channels.html   printable companion deck

No network calls at run time; all sources are local snapshots.
"""
from __future__ import annotations

import collections
import csv
import datetime
import hashlib
import html
import json
import math
import os
import re
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import build_batches as bb  # noqa: E402  (curated term inventory + match prefixes)
import measure              # noqa: E402  (DSG parser)
import slp1_keys as sk      # noqa: E402  (HK / IAST / SLP1 + spelling variants)

# Re-export the canonical helpers so existing call sites keep working, but
# there is now exactly ONE implementation of each conversion.
DEV_PAIRS = sk.DEV_PAIRS
dev_variants = sk.dev_variants
fold = sk.fold
SLP_MAP = sk.SLP_MAP
iast_to_slp1 = sk.iast_to_slp1
slp1_variants = sk.slp1_variants
dcs_lookup = sk.dcs_lookup

e = lambda s: html.escape(str(s))


# --------------------------------------------------------------------------- utils
def sha(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()


# --------------------------------------------------------------- source inventory
GRAMMAR = [
    ("Mahābhāṣya, āhnika 1", "mahabhashyam__1.txt", "Mahābhāṣya"),
    ("Mahābhāṣya, āhnika 2", "mahabhashyam__2.txt", "Mahābhāṣya"),
    ("Siddhāntakaumudī", "sutraani__kaumudi.txt", "Kaumudī / Bālamanoramā"),
    ("Laghukaumudī", "sutraani__laghukaumudi.txt", "Kaumudī / Bālamanoramā"),
    ("Bālamanoramā", "sutraani__balamanorama.txt", "Kaumudī / Bālamanoramā"),
    ("Vākyapadīya (mūla)", "vakyapadeeyam__data.txt", "Vākyapadīya + vṛtti"),
    ("Vākyapadīya, svopajñā vṛtti", "vakyapadeeyam__swopajna.txt", "Vākyapadīya + vṛtti"),
    ("Vākyapadīya, ambākartrī", "vakyapadeeyam__ambakartri.txt", "Vākyapadīya + vṛtti"),
    ("Bhūṣaṇasāra", "bhushanasara__data.txt", "Bhūṣaṇasāra / Phitsūtras"),
    ("Phitsūtras (with SK gloss)", "fit__data.txt", "Bhūṣaṇasāra / Phitsūtras"),
]
# courses__sk_with_bm.json is a structured duplicate of Kaumudī + Bālamanoramā;
# deliberately excluded to avoid double-counting the same passages.
GROUPS = ["Mahābhāṣya", "Kaumudī / Bālamanoramā", "Vākyapadīya + vṛtti",
          "Bhūṣaṇasāra / Phitsūtras"]

TOK = re.compile(r"[\u0900-\u097F]+")


def load_grammar_units():
    units, inventory = [], []
    for disp, fn, group in GRAMMAR:
        p = os.path.join(HERE, "grammar_corpus", fn)
        obj = json.load(open(p, encoding="utf-8-sig"))
        n0 = len(units)

        def walk(x):
            if isinstance(x, str):
                if TOK.search(x):
                    units.append({"group": group, "src": disp,
                                  "text": x, "tokens": None})
            elif isinstance(x, dict):
                for v in x.values():
                    walk(v)
            elif isinstance(x, list):
                for v in x:
                    walk(v)

        walk(obj)
        for u in units[n0:]:
            u["tokens"] = [bb.norm(t) for t in TOK.findall(u["text"])]
        inventory.append({
            "source": disp, "file": "grammar_corpus/" + fn, "group": group,
            "bytes": os.path.getsize(p), "sha256": sha(p),
            "passages": len(units) - n0,
            "devanagari_chars": sum(len(TOK.findall(u["text"]) and "".join(TOK.findall(u["text"])))
                                    for u in units[n0:]),
        })
    return units, inventory


# --------------------------------------------------------------------- matchers
def make_matcher(prefixes):
    """Same semantics as build_batches.py, applied to prose tokens."""
    exact0 = [bb.norm(x[1:]) for x in prefixes if x.startswith("=")]
    excl0 = [bb.norm(x[1:]) for x in prefixes if x.startswith("!")]
    pref0 = [bb.norm(x) for x in prefixes
             if not x.startswith(("=", "!"))]

    def expand(lst):
        out = set()
        for w in lst:
            out |= dev_variants(w)
        return {x for x in out if x}

    exact, excl, pref = expand(exact0), expand(excl0), expand(pref0)

    def m(tok):
        if any(tok.startswith(x) for x in excl):
            return False
        return tok in exact or any(tok.startswith(p) for p in pref)

    return m


def dsg_stems(term, dsg_by_id):
    """Folded IAST stems for searching Abhyankar's transliterated prose.

    Every stem is returned, including the ten short ones (``ca``, ``na``,
    ``vā``, ``iti``, ``api``, ``it``, ``bha``, ``sup``, ``tiṅ``, ``kṛt``).
    Short stems are matched with exact token boundaries, and are additionally
    measured in the Russian prose and in the Devanāgarī headword index, where
    English function words cannot collide.  Nothing is dropped and nothing is
    guessed: see ``L_MATCH_RULE``.
    """
    raw = [term["iast"]]
    ent = dsg_by_id.get(term.get("dsg_id") or "")
    if ent:
        raw.append(ent["iast"])
    stems = set()
    for r in raw:
        for part in re.split(r"\s*/\s*", r):
            f = fold(part.strip())
            if f:
                stems.add(f)
    return stems


L_MATCH_RULE = (
    "Document frequency over the 4,383 DSG entries. For folded stems of "
    "<=4 characters an exact token match (?<![a-z])stem(?![a-z]) is used; "
    "longer stems use substring matching so that inflected forms count. "
    "Applied identically to the folded English and Russian definitions. "
    "Devanagari headwords are matched by substring against dev_variants() "
    "(class-nasal <-> anusvara). English prose is an UPPER BOUND for short "
    "Latin stems because English 'it', 'ca', 'na' collide; the Russian-prose "
    "and headword counts are reported alongside as collision controls."
)


def stem_patterns(stems):
    """One compiled matcher per stem; short stems get exact token boundaries."""
    return [(s, re.compile(r"(?<![a-z])" + re.escape(s) + r"(?![a-z])"), None)
            if len(s) <= 4 else
            (s, None, s)
            for s in sorted(stems)]


def count_matches(bodies, pats):
    n = 0
    for body in bodies:
        if any((p.search(body) if p is not None else sub in body)
               for _, p, sub in pats):
            n += 1
    return n


# ------------------------------------------------------------------- correlations
def avg_ranks(v):
    order = sorted(range(len(v)), key=lambda i: v[i])
    r = [0.0] * len(v)
    i = 0
    while i < len(order):
        j = i
        while j + 1 < len(order) and v[order[j + 1]] == v[order[i]]:
            j += 1
        avg = (i + j) / 2.0 + 1
        for k in range(i, j + 1):
            r[order[k]] = avg
        i = j + 1
    return r


def pearson(x, y):
    n = len(x)
    if n < 2:
        return 0.0
    mx, my = sum(x) / n, sum(y) / n
    num = sum((a - mx) * (b - my) for a, b in zip(x, y))
    dx = math.sqrt(sum((a - mx) ** 2 for a in x))
    dy = math.sqrt(sum((b - my) ** 2 for b in y))
    return num / (dx * dy) if dx and dy else 0.0


def spearman(x, y):
    return pearson(avg_ranks(x), avg_ranks(y))


def kendall_tau_b(x, y):
    n = len(x)
    conc = disc = 0
    for i in range(n):
        for j in range(i + 1, n):
            dx, dy = x[i] - x[j], y[i] - y[j]
            if dx == 0 or dy == 0:
                continue
            if dx * dy > 0:
                conc += 1
            else:
                disc += 1
    n0 = n * (n - 1) / 2.0
    tx = sum(c * (c - 1) / 2.0 for c in collections.Counter(x).values())
    ty = sum(c * (c - 1) / 2.0 for c in collections.Counter(y).values())
    den = math.sqrt((n0 - tx) * (n0 - ty))
    return (conc - disc) / den if den else 0.0


def corr(x, y):
    return {"spearman": round(spearman(x, y), 4),
            "kendall_tau_b": round(kendall_tau_b(x, y), 4), "n": len(x)}


# --------------------------------------------------------------------------- main
def main():
    core = json.load(open(os.path.join(HERE, "core_terms.json"), encoding="utf-8"))
    terms = core["terms"]
    assert len(bb.T) == len(terms), "term inventory / matcher misalignment"
    for t, row in zip(terms, bb.T):
        assert t["deva"] == row[0], (t["deva"], row[0])

    rep = json.load(open(os.path.join(HERE, "report.json"), encoding="utf-8"))
    dsg = measure.parse_dsg()
    dsg_by_id = {str(x["id"]): x for x in dsg}
    dsg_tsv = {r["id"]: r for r in csv.DictReader(
        open(os.path.join(HERE, "dsg_entries.tsv"), encoding="utf-8"), delimiter="\t")}

    # --- D: DCS ranking table -------------------------------------------------
    dcs_path = os.path.join(ROOT, "sanskrit-util/tools/KeySwap/data/dcs_freq.txt")
    dcs, _ = measure.load_dcs()
    sorted_counts = sorted(dcs.values(), reverse=True)

    # --- L: DSG fields, folded once each -------------------------------------
    dsg_en = [fold(x["en"]) for x in dsg]
    dsg_ru = [fold(x["ru"]) for x in dsg]
    dsg_deva = [x["deva"] for x in dsg]

    # Difficulty-ordering rank lookup, indexed by SLP1 key (variants allowed).
    diff_path = os.path.join(ROOT, "SanskritGrammar/data/difficulty_ordering/"
                             "core_vs_frequency.tsv")
    diff_rows = {}
    if os.path.exists(diff_path):
        for r in csv.DictReader(open(diff_path, encoding="utf-8"), delimiter="\t"):
            diff_rows.setdefault(r["lemma_slp1"], r["rank_freq_sub"])

    # --- G: grammar corpus ----------------------------------------------------
    units, inventory = load_grammar_units()

    rows = []
    for t, spec in zip(terms, bb.T):
        matcher = make_matcher(spec[5])
        gdf = collections.Counter()
        gtf = 0
        per_group = collections.Counter()
        for u in units:
            hit = sum(1 for tok in u["tokens"] if matcher(tok))
            if hit:
                gdf["all"] += 1
                per_group[u["group"]] += 1
                gtf += hit

        # L: three independent, fully deterministic measurements. No term is
        # dropped and no value is left blank, including the ten short stems.
        stems = dsg_stems(t, dsg_by_id)
        pats = stem_patterns(stems)
        stem_short = int(all(len(s) <= 3 for s in stems))
        dsg_m = count_matches(dsg_en, pats)
        dsg_ru_m = count_matches(dsg_ru, pats)
        dev_stems = set()
        for d in re.split(r"\s*/\s*", t["deva"]):
            dev_stems |= dev_variants(d.strip())
        dev_stems = {d for d in dev_stems if d}
        dsg_head = sum(1 for h in dsg_deva if any(d in h for d in dev_stems))

        # D: canonical SLP1 + every class-nasal <-> anusvara variant. The DSG
        # headword's own derived SLP1 key is a second base when it differs.
        ent = dsg_tsv.get(str(t["dsg_id"]), {}) if t.get("dsg_id") else {}
        iast_first = re.split(r"\s*/\s*", t["iast"])[0].strip()
        key = iast_to_slp1(iast_first)
        bases = {key} | ({ent["slp1"]} if ent.get("slp1") else set())
        tried, hits = set(), {}
        for base in sorted(bases):
            _, _, h, tr = dcs_lookup(dcs, base)
            tried |= set(tr)
            hits.update(h)
        best_key = max(hits, key=lambda k: hits[k]) if hits else ""
        c = hits.get(best_key, 0)
        rank = sorted_counts.index(c) + 1 if c else len(sorted_counts) + 1
        diff = next((diff_rows[k] for k in sorted(tried) if k in diff_rows), None)

        rows.append({
            "batch": t["batch"], "deva": t["deva"], "iast": t["iast"],
            "gloss": t["gloss"],
            "structural_total": t["total"], "explicit": t["explicit"],
            "inherited": t["inherited"], "governed": t["governed"],
            "grammar_df": gdf["all"], "grammar_tf": gtf,
            "mahabhasya_df": per_group["Mahābhāṣya"],
            "kaumudi_df": per_group["Kaumudī / Bālamanoramā"],
            "vakyapadiya_df": per_group["Vākyapadīya + vṛtti"],
            "other_grammar_df": per_group["Bhūṣaṇasāra / Phitsūtras"],
            "dsg_mentions": dsg_m, "dsg_ru_mentions": dsg_ru_m,
            "dsg_headword_df": dsg_head, "stem_short": stem_short,
            "dsg_cites": t["dsg_cites"],
            "dsg_panini_cites": int(ent.get("panini_cites", 0) or 0),
            "dsg_chars": t["dsg_chars"],
            "dcs_key": key, "dcs_best_key": best_key,
            "dcs_count": c, "dcs_key_variants": "|".join(sorted(tried - {key})),
            "dcs_variant_hits": "|".join("%s=%d" % (k, v)
                                         for k, v in sorted(hits.items())),
            "dcs_present": int(c > 0), "dcs_rank": rank,
            "dcs_difficulty_rank": diff,
        })

    # --- correlations ---------------------------------------------------------
    def col(name, subset=None, skip_none=False):
        xs = rows if subset is None else [r for r in rows if subset(r)]
        if skip_none:
            xs = [r for r in xs if r[name] is not None]
        return [float(r[name]) for r in xs]

    content = lambda r: r["batch"] != 0
    correlations = {
        "all_119_terms": {
            "structural ~ grammar_df": corr(col("structural_total"), col("grammar_df")),
            "structural ~ grammar_tf": corr(col("structural_total"), col("grammar_tf")),
            "structural ~ dcs_count": corr(col("structural_total"), col("dcs_count")),
            "grammar_df ~ dcs_count": corr(col("grammar_df"), col("dcs_count")),
        },
        "content_only_107_terms_excluding_B0_operators": {
            "structural ~ grammar_df": corr(col("structural_total", content),
                                            col("grammar_df", content)),
            "structural ~ grammar_tf": corr(col("structural_total", content),
                                            col("grammar_tf", content)),
            "structural ~ dcs_count": corr(col("structural_total", content),
                                           col("dcs_count", content)),
            "grammar_df ~ dcs_count": corr(col("grammar_df", content),
                                           col("dcs_count", content)),
            "structural ~ dsg_mentions": corr(
                col("structural_total", content), col("dsg_mentions", content)),
            "structural ~ dsg_ru_mentions (collision-controlled)": corr(
                col("structural_total", content), col("dsg_ru_mentions", content)),
            "structural ~ dsg_headword_df": corr(
                col("structural_total", content), col("dsg_headword_df", content)),
        },
    }

    # --- headline evidence ----------------------------------------------------
    top_struct = sorted(rows, key=lambda r: -r["structural_total"])[:15]
    top_dcs = sorted(rows, key=lambda r: -r["dcs_count"])[:12]
    batch_means = {}
    for b in sorted({r["batch"] for r in rows}):
        xs = [r for r in rows if r["batch"] == b]
        batch_means[str(b)] = {
            "terms": len(xs),
            "mean_structural": round(sum(r["structural_total"] for r in xs) / len(xs), 1),
            "mean_grammar_df": round(sum(r["grammar_df"] for r in xs) / len(xs), 1),
            "mean_dcs_count": round(sum(r["dcs_count"] for r in xs) / len(xs), 1),
            "dcs_absent": sum(1 for r in xs if not r["dcs_present"]),
        }

    out = {
        "question": "Does the 3 include frequency in grammars? DCS as well 4th?",
        "answer": {
            "three_are": "Aṣṭādhyāyī-internal structural positions (pc / an / ad), "
                         "not three corpora",
            "grammar_frequency_in_original": False,
            "dcs_in_original": "indirect only (function-word exclusion principle from "
                               "DIFFICULTY_ORDERING_RESULT.md); never a measured column",
            "dcs_as_fourth_of_same_kind": False,
            "recommended_taxonomy": [
                "Axis A - structural demand: pc, an, ad (3 channels, one text)",
                "Axis B - grammatical discourse: vyākaraṇa corpus df/tf (channel G) "
                "+ DSG lexicographic salience (channel L)",
                "Axis C - general literary register: DCS (channel D), a control, "
                "not a ranking signal",
            ],
        },
        "generated": datetime.date.today().isoformat(),
        "sources": {
            "panini": rep["sources"]["panini"],
            "dsg": rep["sources"]["dsg"],
            "grammar_corpus": {
                "url": "https://github.com/ashtadhyayi-com/data (raw/master)",
                "files": inventory,
                "total_passages": len(units),
                "excluded": ["grammar_corpus/courses__sk_with_bm.json "
                             "(structured duplicate of Kaumudī + Bālamanoramā)"],
            },
            "dcs": {
                "file": "sanskrit-util/tools/KeySwap/data/dcs_freq.txt",
                "sha256": sha(dcs_path),
                "distinct_keys": len(dcs), "sum_of_counts": sum(dcs.values()),
                "note": "DCS-2026 lemma RANKING table; the fuller DCS export is "
                        "5,688,416 tokens / 90,349 lemmas per "
                        "SanskritLexicography/RussianTranslation/release/fixture/"
                        "dcs_freq.ttl. Counts here are the locally pinned ranking list.",
            },
        },
        "channels": {
            "G_grammar_corpus": {
                "unit": "one Sanskrit passage / chunk / verse / sūtra-gloss",
                "total_passages": len(units),
                "total_matching_tokens": sum(r["grammar_tf"] for r in rows),
            },
            "L_dsg_salience": {
                "entries": len(dsg),
                "fields": ["English prose (folded)", "Russian prose (folded)",
                           "Devanāgarī headwords (class-nasal/anusvāra variants)"],
                "matching_rule": L_MATCH_RULE,
                "terms_without_measurement":
                    sum(1 for r in rows if r["dsg_mentions"] is None),
                "short_stems_collision_controlled": [
                    {k: r[k] for k in ("iast", "deva", "dsg_mentions",
                                       "dsg_ru_mentions", "dsg_headword_df")}
                    for r in rows if r["stem_short"]],
            },
            "D_dcs": {"keys": len(dcs),
                      "core_terms_present": sum(r["dcs_present"] for r in rows),
                      "core_terms_absent": sum(1 - r["dcs_present"] for r in rows),
                      "core_terms_count_le_5":
                          sum(1 for r in rows if 0 < r["dcs_count"] <= 5),
                      "variant_keys_enabled": True,
                      "core_terms_with_variant_keys":
                          sum(1 for r in rows if r["dcs_key_variants"]),
                      "core_terms_hit_only_through_a_variant":
                          sum(1 for r in rows if r["dcs_best_key"]
                              and r["dcs_best_key"] != r["dcs_key"]),
                      },
        },
        "data_quality": {
            "hk_vs_slp1": rep["slp1_keys"],
            "join_table": "dsg_dcs_join.tsv",
            "key_module": "slp1_keys.py",
            "rule": "DSG `HK` is never joined to DCS directly. A single-pass "
                    "longest-match HK->SLP1 conversion (or IAST->SLP1 when HK "
                    "is blank/dirty) produces the canonical key; "
                    "slp1_variants() adds class-nasal <-> anusvara spellings; "
                    "the best-attested spelling is used (variants are "
                    "alternative spellings, not independent lemmas, so counts "
                    "are not summed).",
        },
        "correlations": correlations,
        "batch_means": batch_means,
        "headline": {
            "top_by_structural_demand": [
                {k: r[k] for k in ("iast", "structural_total", "grammar_df",
                                   "grammar_tf", "dcs_count", "dsg_mentions")}
                for r in top_struct],
            "top_by_dcs": [
                {k: r[k] for k in ("iast", "dcs_count", "structural_total", "grammar_df")}
                for r in top_dcs],
        },
        "terms": rows,
    }

    # --- TSV ------------------------------------------------------------------
    cols = ["batch", "deva", "iast", "structural_total", "explicit", "inherited",
            "governed", "grammar_df", "grammar_tf", "mahabhasya_df", "kaumudi_df",
            "vakyapadiya_df", "other_grammar_df",
            "dsg_mentions", "dsg_ru_mentions", "dsg_headword_df", "stem_short",
            "dsg_cites", "dsg_panini_cites", "dsg_chars",
            "dcs_key", "dcs_best_key", "dcs_key_variants", "dcs_variant_hits",
            "dcs_count", "dcs_present", "dcs_rank", "dcs_difficulty_rank", "gloss"]
    with open(os.path.join(HERE, "external_channels.tsv"), "w", encoding="utf-8") as f:
        f.write("\t".join(cols) + "\n")
        for r in rows:
            f.write("\t".join("" if r[c] is None else str(r[c]) for c in cols) + "\n")

    with open(os.path.join(HERE, "external_channels.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)

    write_html(out, inventory, correlations, top_struct, top_dcs, batch_means, rows)

    # --- console summary ------------------------------------------------------
    print("Grammar corpus passages:", len(units))
    print("DCS keys:", len(dcs), "| core terms present:",
          sum(r["dcs_present"] for r in rows), "/", len(rows))
    print("L: terms without a measurement:",
          sum(1 for r in rows if r["dsg_mentions"] is None),
          "| short stems measured:", sum(r["stem_short"] for r in rows))
    print("D: terms with variant keys:",
          sum(1 for r in rows if r["dcs_key_variants"]),
          "| hits only via a variant:",
          sum(1 for r in rows if r["dcs_best_key"] and
              r["dcs_best_key"] != r["dcs_key"]))
    print("HK->SLP1 audit:",
          json.dumps(rep["slp1_keys"]["hk_vs_iast_conversion_audit"],
                     ensure_ascii=False))
    print("DSG->DCS join:",
          json.dumps(rep["slp1_keys"]["dcs_join"], ensure_ascii=False))
    print("\nCorrelations:")
    for scope, cs in correlations.items():
        print(" ", scope)
        for k, v in cs.items():
            print("   %-30s rho=%+.3f  tau=%+.3f  n=%d" %
                  (k, v["spearman"], v["kendall_tau_b"], v["n"]))
    print("\nTop by structural demand (term | structural | grammar_df | DCS):")
    for r in top_struct[:10]:
        print("  %-24s %5d %6d %6d" %
              (r["iast"], r["structural_total"], r["grammar_df"], r["dcs_count"]))
    print("\nTop by DCS (term | DCS | structural | grammar_df):")
    for r in top_dcs[:10]:
        print("  %-24s %6d %5d %6d" %
              (r["iast"], r["dcs_count"], r["structural_total"], r["grammar_df"]))


# --------------------------------------------------------------------------- HTML
def bars(items, cutoff=12):
    mx = max(v for _, v, _ in items[:cutoff]) or 1
    out = []
    for lab, val, sub in items[:cutoff]:
        out.append(
            '<div class="bar-row"><div class="bar-lab">%s</div>'
            '<div class="bar-track"><div class="bar-fill" style="width:%.1f%%"></div></div>'
            '<div class="bar-val">%s</div><div class="bar-sub">%s</div></div>'
            % (e(lab), 100.0 * val / mx, e(val), e(sub)))
    return "".join(out)


def write_html(out, inventory, correlations, top_struct, top_dcs, batch_means, rows):
    mk = open(os.path.join(HERE, "make_html.py"), encoding="utf-8").read()
    css = re.search(r"<style>(.*?)</style>", mk, re.S).group(1)

    inv_rows = "".join(
        "<tr><td>%s</td><td class='mono'>%s</td><td>%s</td><td class='num'>%s</td>"
        "<td class='num'>%s</td></tr>" %
        (e(x["source"]), e(x["group"]), e(x["file"].split("/")[-1]),
         f'{x["passages"]:,}', f'{x["devanagari_chars"]:,}')
        for x in inventory)

    corr_rows = []
    for scope, cs in correlations.items():
        corr_rows.append('<tr class="grp"><td colspan="4">%s</td></tr>' %
                         e(scope.replace("_", " ")))
        for k, v in cs.items():
            cls = "good" if v["spearman"] >= .5 else ("bad" if v["spearman"] < .25 else "")
            corr_rows.append(
                '<tr><td>%s</td><td class="num %s">%+.3f</td>'
                '<td class="num %s">%+.3f</td><td class="num">%d</td></tr>' %
                (e(k), cls, v["spearman"], cls, v["kendall_tau_b"], v["n"]))
    corr_rows = "".join(corr_rows)

    inv1 = "".join(
        "<tr><td class='deva'>%s</td><td class='iast'>%s</td>"
        "<td class='num'>%s</td><td class='num'>%s</td>"
        "<td class='num hot'>%s</td><td class='num'>%s</td></tr>" %
        (e(r["deva"]), e(r["iast"]), f'{r["structural_total"]:,}',
         f'{r["grammar_df"]:,}', r["dcs_count"],
         f'{r["dsg_mentions"]:,}')
        for r in top_struct)
    inv2 = "".join(
        "<tr><td class='deva'>%s</td><td class='iast'>%s</td>"
        "<td class='num hot'>%s</td><td class='num'>%s</td>"
        "<td class='num'>%s</td></tr>" %
        (e(next(x["deva"] for x in rows if x["iast"] == r["iast"])),
         e(r["iast"]), f'{r["dcs_count"]:,}', f'{r["structural_total"]:,}',
         f'{r["grammar_df"]:,}')
        for r in top_dcs)

    bm = "".join(
        "<tr><td>B%s</td><td class='num'>%d</td><td class='num'>%s</td>"
        "<td class='num'>%s</td><td class='num'>%s</td><td class='num'>%d</td></tr>" %
        (b, v["terms"], v["mean_structural"], v["mean_grammar_df"],
         v["mean_dcs_count"], v["dcs_absent"])
        for b, v in sorted(batch_means.items(), key=lambda x: int(x[0])))

    ch = out["channels"]["D_dcs"]
    big = [
        ("Aṣṭādhyāyī sūtras", 3983, "the one text the 3 channels live in"),
        ("Grammar passages (G)", out["channels"]["G_grammar_corpus"]["total_passages"],
         "Mahābhāṣya → Phitsūtras"),
        ("DSG entries (L)", 4383, "Abhyankar's grammatical lexicon"),
        ("DCS keys (D)", ch["keys"], "literary register control"),
        ("Core terms absent from DCS", ch["core_terms_absent"], "of 119 curriculum terms"),
    ]
    bigbars = bars([(a, b, c) for a, b, c in big], cutoff=5)

    # --- data-quality section -------------------------------------------------
    dq = out["data_quality"]["hk_vs_slp1"]
    jn = dq["dcs_join"]
    aud = dq["hk_vs_iast_conversion_audit"]
    short_rows = [r for r in rows if r["stem_short"]]
    short_tbl = "".join(
        "<tr><td class='deva'>%s</td><td class='iast'>%s</td>"
        "<td class='num'>%s</td><td class='num hot'>%s</td>"
        "<td class='num'>%s</td><td class='num'>%s</td></tr>" %
        (e(r["deva"]), e(r["iast"]), f'{r["dsg_mentions"]:,}',
         f'{r["dsg_ru_mentions"]:,}', f'{r["dsg_headword_df"]:,}',
         f'{r["dsg_cites"]:,}')
        for r in short_rows)
    dq_rows = [
        ("DSG headwords", f'{jn["dsg_entries"]:,}', "4,383 entries with a derived SLP1 key"),
        ("HK column is wrong as a DCS key", f'{jn["headword_keys_differ_from_hk"]:,}',
         "headwords whose SLP1 key differs from the raw HK value"),
        ("HK -> SLP1 conversion checks", f'{aud["agree"]:,} / {aud["hk_clean_rows_compared"]:,}',
         "agree with the independent IAST headword; %d disagree" % aud["disagree"]),
        ("DCS hits with the naive HK join", f'{jn["naive_hk_join_hits"]:,}',
         "the old, silently wrong join"),
        ("DCS hits with the corrected join", f'{jn["corrected_join_hits"]:,}',
         "%d hits the naive join missed" % jn["hits_the_naive_join_missed"]),
        ("Headwords with SLP1 spelling variants", f'{dq["entries_with_slp1_variants"]:,}',
         "class-nasal <-> anusvara alternates generated"),
        ("Hits found only through a variant", f'{jn["hits_found_only_through_a_spelling_variant"]:,}',
         "e.g. saMbanDa -> sambanDa, saMBava -> samBava"),
        ("Short terms now measured (were blank)", f'{len(short_rows)}',
         "all measured in three fields; none blank"),
    ]
    dq_tbl = "".join(
        "<tr><td>%s</td><td class='num hot'>%s</td><td class='small'>%s</td></tr>" %
        (e(a), e(b), e(c)) for a, b, c in dq_rows)

    TPL = r"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>The missing channels — grammars, DSG, and DCS</title>
<style>__CSS__</style>
<style>
.hot{color:#b0472b;font-weight:700}.good{color:#2f6b45;font-weight:700}.bad{color:#b0472b}
.mono{font-size:11px;color:var(--muted)}.num{text-align:right;font-variant-numeric:tabular-nums}
table.wide{width:100%;border-collapse:collapse;font-size:12.5px}
table.wide th{text-align:left;padding:7px 9px;border-bottom:2px solid var(--line);
 font-size:10.5px;letter-spacing:.08em;text-transform:uppercase;color:var(--muted)}
table.wide td{padding:6px 9px;border-bottom:1px solid var(--line)}
table.wide tr.grp td{background:var(--soft);font-weight:700;font-size:11px;
 letter-spacing:.05em;text-transform:uppercase;color:var(--accent)}
table.wide td.deva{font-size:15px;color:var(--accent);white-space:nowrap}
table.wide td.iast{font-style:italic;color:var(--muted)}
.answer{background:#fff;border:1px solid var(--line);border-left:5px solid var(--accent2);
 padding:18px 22px;margin:18px 0 26px}
.answer p{margin:0 0 9px}.answer p:last-child{margin:0}
.axis{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin:14px 0 26px}
.axis>div{background:var(--card);border:1px solid var(--line);padding:15px 17px}
.axis b{display:block;font-size:11px;letter-spacing:.1em;text-transform:uppercase;
 color:var(--accent2);margin-bottom:7px}
.axis p{font-size:12.5px;color:var(--muted);margin:0}
.kicker{font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:var(--accent2)}
.small{font-size:12px;color:var(--muted)}
.two{display:grid;grid-template-columns:1fr 1fr;gap:22px}
@media(max-width:820px){.axis,.two{grid-template-columns:1fr}}
@media print{.axis>div,.answer{break-inside:avoid}}
</style></head><body><div class="wrap">
<div class="kicker">Companion study · DSG_learning_batches</div>
<h1>The missing channels: grammars, DSG, and DCS</h1>
<p class="lede">A direct answer to <i>“Does the 3 include frequency in grammars?
DCS as well 4th?”</i> — with the two absent channels actually measured, not just
described.</p>

<div class="answer">
<p><b>No.</b> The three channels were <code>pc</code> (explicitly written),
<code>an</code> (inherited by anuvṛtti) and <code>ad</code> (supplied by a
governing adhikāra). All three are <b>structural positions inside the same
3,983 sūtras</b> — they describe <i>how a term is required in order to read one
rule</i>. They are not three corpora, so they cannot contain “frequency in
grammars”.</p>
<p><b>DCS was not a fourth measured channel either.</b> It entered the design
only indirectly: <code>DIFFICULTY_ORDERING_RESULT.md</code> supplied the
function-word-exclusion principle (τ = 0.887 inside content vocabulary). No DCS
count appeared in <code>core_terms.tsv</code>.</p>
<p><b>So the right fix is not “3 + DCS = 4”.</b> It is a two-axis design: keep the
three structural channels on Axis A, then add grammatical-discourse frequency on
Axis B and DCS as a <i>register control</i> on Axis C. DCS measures how often a
word turns up in epic / Purāṇa / kāvya text, which is the wrong target for a
technical term.</p>
</div>

<h2><span class="n">01</span>What the three channels actually are</h2>
<div class="axis">
<div><b>Axis A · structural demand</b><p>One text: the Aṣṭādhyāyī. Three ways a
term is loaded: <code>pc</code> 13,068 occurrences / 6,741 forms ·
<code>an</code> 9,808 / 1,571 · <code>ad</code> 14,323 / 69 headings.
37,199 required-term readings, ~1.8 implicit for every 1 explicit.</p></div>
<div><b>Axis B · grammatical discourse</b><p>New here. Channel <b>G</b>: 12,627
passages of Mahābhāṣya, Kaumudī, Bālamanoramā, Vākyapadīya, Bhūṣaṇasāra,
Phitsūtras. Channel <b>L</b>: mentions + citation density across 4,383 DSG
entries.</p></div>
<div><b>Axis C · literary register</b><p>New here. Channel <b>D</b>: the DCS
lemma ranking table (50,474 keys). Used to show what <i>not</i> to optimise for,
and to flag terms that a student will never meet outside a grammar.</p></div>
</div>

<h2><span class="n">02</span>Corpus inventory (newly pinned)</h2>
<p class="small">All files are local snapshots of
<a href="https://github.com/ashtadhyayi-com/data" target="_blank" rel="noopener">ashtadhyayi-com/data</a>.
The structured <code>courses/sk_with_bm.json</code> is deliberately excluded
because it duplicates Kaumudī + Bālamanoramā. SHA-256 for every file is in
<code>external_channels.json</code>.</p>
<table class="wide"><thead><tr><th>Text</th><th>Group</th><th>File</th>
<th style="text-align:right">Passages</th><th style="text-align:right">Dev. chars</th></tr></thead>
<tbody>__INV__</tbody></table>

<h2><span class="n">03</span>Scale of the four sources</h2>
__BIG__

<h2><span class="n">04</span>The measurement: rank correlations</h2>
<p class="small">Spearman ρ and Kendall τ-b between the original structural
<b>reading-pressure</b> score and each new channel. Computed twice: for all 119
curated terms, and for the 107 <i>content</i> terms after stripping the B0
operators (the same curation move the estate's difficulty study recommends).</p>
<table class="wide"><thead><tr><th>Comparison</th><th style="text-align:right">ρ</th>
<th style="text-align:right">τ-b</th><th style="text-align:right">n</th></tr></thead>
<tbody>__CORR__</tbody></table>
<p class="small"><b>Read this as the answer.</b> Grammar-corpus frequency tracks
structural demand; DCS does not. DCS is therefore a diagnostic, not a fourth
co-equal weight.</p>

<h2><span class="n">05</span>The inversion that decides it</h2>
<div class="two">
<div><h3>Top 15 by structural demand</h3>
<table class="wide"><thead><tr><th>Term</th><th></th>
<th style="text-align:right">Aṣṭ. demand</th><th style="text-align:right">Grammar df</th>
<th style="text-align:right">DCS</th><th style="text-align:right">DSG mentions</th>
</tr></thead><tbody>__INV1__</tbody></table></div>
<div><h3>Top 12 by DCS frequency</h3>
<table class="wide"><thead><tr><th>Term</th><th></th>
<th style="text-align:right">DCS</th><th style="text-align:right">Aṣṭ. demand</th>
<th style="text-align:right">Grammar df</th></tr></thead>
<tbody>__INV2__</tbody></table></div>
</div>
<p class="small"><code>pratyaya</code> governs 1,821 sūtras and is written in
only 22, yet DCS gives it <b>17</b>. <code>taddhita</code> governs 1,115 sūtras
and gets <b>3</b>; <code>saṃjñā</code>, <code>saṃdhi</code> are <b>absent</b>.
Meanwhile <code>ca</code> gets <b>3,385</b> and <code>iti</code> <b>1,512</b>
— operators and ordinary words, not concepts. Adding DCS as a co-equal fourth
weight would actively invert the syllabus.</p>

<h2><span class="n">06</span>Per-batch means</h2>
<table class="wide"><thead><tr><th>Batch</th><th style="text-align:right">Terms</th>
<th style="text-align:right">Mean structural</th><th style="text-align:right">Mean grammar df</th>
<th style="text-align:right">Mean DCS</th><th style="text-align:right">DCS-absent</th>
</tr></thead><tbody>__BM__</tbody></table>

<h2><span class="n">07</span>Data quality: the HK → SLP1 fix and the ten short stems</h2>
<p class="small">DSG's column labelled <code>slp1</code> is <b>Harvard-Kyoto</b>,
not SLP1. DCS is keyed in SLP1, so joining the column directly produces wrong
keys: <code>Adeza</code> → <code>AdeSa</code>, <code>saJjJA</code> →
<code>saYjYA</code>, <code>kRt</code> → <code>kft</code>. HK and SLP1 differ by a
<i>cyclic</i> substitution (<code>R</code> = ṛ ↔ <code>f</code>,
<code>G</code> = ṅ ↔ <code>N</code>, <code>N</code> = ṇ ↔ <code>R</code>,
<code>z</code> = ś ↔ <code>S</code>), so a single-pass longest-match converter
is required — sequential replacement corrupts the result. The conversion is
verified against DSG's independent IAST headword column, and every one of the
4,383 headwords is re-joined in <code>dsg_dcs_join.tsv</code>.</p>
<table class="wide"><thead><tr><th>Check</th><th style="text-align:right">Value</th>
<th>What it means</th></tr></thead><tbody>__DQ__</tbody></table>
<p class="small">The class-nasal ↔ anusvāra variants are now generated in
<b>SLP1</b> as well as in Devanāgarī: <code>aNga</code>/<code>aMga</code>,
<code>saYjYA</code>/<code>saMjYA</code>, <code>saNKyA</code>/<code>saMKyA</code>,
<code>saMbanDa</code>/<code>sambanDa</code>. Word-final nasals are deliberately
<i>not</i> varied — <code>aM</code> (the letter aṃ) and <code>an</code> are
different words. Variants are alternative spellings of one lemma, so the
best-attested spelling is used rather than summing counts (which would
double-count); every attested variant is recorded in
<code>external_channels.tsv</code>.</p>

<h3>The ten short stems are measured, not declared unmeasurable</h3>
<p class="small">The first release left these ten blank because
<code>it</code>, <code>ca</code> and <code>na</code> collide with English words
in Abhyankar's English definitions. They are now measured with one documented
rule in three independent fields. English prose is explicitly an
<b>upper bound</b>; the Russian definitions (where English function words are
absent) and the Devanāgarī headword index are collision controls. No value is
guessed and no value is blank.</p>
<table class="wide"><thead><tr><th>Term</th><th></th>
<th style="text-align:right">EN prose (upper bound)</th>
<th style="text-align:right">RU prose (collision-free)</th>
<th style="text-align:right">Dev. headwords</th>
<th style="text-align:right">DSG cites</th></tr></thead>
<tbody>__SHORT__</tbody></table>
<p class="small">The collision is visible and quantified rather than hidden:
English <code>it</code> scores 565 but Russian <code>it</code> scores 30, i.e.
most English hits are the pronoun, not the Pāṇinian marker. Correlations are
therefore reported for both <code>dsg_mentions</code> and the
collision-controlled <code>dsg_ru_mentions</code>.</p>

<h2><span class="n">08</span>Verdict — how to use each channel</h2>
<div class="method">
<div class="m"><h4>Keep A as the backbone</h4><p><code>pc / an / ad</code>
determine <i>when a term becomes unavoidable</i> while reading Pāṇini. This is
what fixes batch order. Do not dilute it with corpus counts.</p></div>
<div class="m"><h4>Use G to validate and to pace</h4><p>Grammar-corpus df is the
independent check that the tradition really talks about a term. It also tells
you how much prose exposure a student gets in Mahābhāṣya vs. Kaumudī vs.
Vākyapadīya.</p></div>
<div class="m"><h4>Use L for the reference shelf</h4><p>DSG entry length,
citation density and cross-mentions decide which terms deserve a full dictionary
entry in a student's notes — they are a salience signal, not a learn-first
signal.</p></div>
<div class="m"><h4>Use D as a negative control</h4><p>Low or zero DCS count is
<i>evidence for</i> teaching a term early: it will never be picked up by
reading literature. High DCS count mostly flags operators and everyday words
that must be excluded from the vocabulary list.</p></div>
</div>

<footer>
<b>Sources.</b> Aṣṭādhyāyī <code>sutraani/data.txt</code> (3,983 sūtras) ·
DSG <a href="https://samskrtam.ru/sanskrit-lexicon/dsg/" target="_blank"
rel="noopener">samskrtam.ru</a> (4,383 entries) · vyākaraṇa corpus
<a href="https://github.com/ashtadhyayi-com/data" target="_blank"
rel="noopener">ashtadhyayi-com/data</a> · DCS ranking table
<code>sanskrit-util/tools/KeySwap/data/dcs_freq.txt</code>.<br><br>
<b>Limitations.</b> G counts <i>document frequency over passages</i>, not raw
sūtra-style readings; passage granularity differs by source (an āhnika chunk is
longer than a kārikā). Matching reuses the curated prefix inventory from
<code>build_batches.py</code> with class-nasal ↔ anusvāra variants in both
Devanāgarī and SLP1. L measures all 119 terms in three fields (English prose,
Russian prose, Devanāgarī headwords); short stems use exact-token matching and
their known English collision is reported rather than suppressed. D is the
locally pinned 50,474-key DCS <i>ranking</i> table, not the full
5,688,416-token / 90,349-lemma export; multi-part rows use their first lemma.
DSG's mislabelled <code>HK</code> column is never joined to DCS directly:
see <code>slp1_keys.py</code>, <code>dsg_entries.tsv</code> and
<code>dsg_dcs_join.tsv</code>. Two DSG headwords (jihvāmūlīya / upadhmānīya)
have non-Latin placeholder characters and yield no SLP1 key; they are flagged
as <code>slp1_source=none</code>.<br><br>
<a href="index.html">← back to the seven-batch deck</a> ·
generated by <code>external_channels.py</code> on __DATE__.
</footer>
</div></body></html>
"""

    def bars2(items):
        mx = max(v for _, v, _ in items) or 1
        return "".join(
            '<div class="bar-row"><div class="bar-lab">%s</div>'
            '<div class="bar-track"><div class="bar-fill" style="width:%.1f%%"></div></div>'
            '<div class="bar-val">%s</div><div class="bar-sub">%s</div></div>' %
            (e(a), 100.0 * b / mx, e(f"{b:,}"), e(c)) for a, b, c in items)

    res = (TPL.replace("__CSS__", css)
           .replace("__INV__", inv_rows)
           .replace("__BIG__", bars2(big))
           .replace("__CORR__", corr_rows)
           .replace("__INV1__", inv1)
           .replace("__INV2__", inv2)
           .replace("__BM__", bm)
           .replace("__DQ__", dq_tbl)
           .replace("__SHORT__", short_tbl)
           .replace("__DATE__", out["generated"]))
    with open(os.path.join(HERE, "external_channels.html"), "w", encoding="utf-8") as f:
        f.write(res)


if __name__ == "__main__":
    main()
