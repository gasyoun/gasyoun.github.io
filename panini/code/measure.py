#!/usr/bin/env python3
"""Measure the frequency of Sanskrit grammatical terms in the Pāṇinian tradition.

Two locally snapshotted sources (both public):

  dsg_page.html   https://samskrtam.ru/sanskrit-lexicon/dsg/
                  K. V. Abhyankar, A Dictionary of Sanskrit Grammar (Baroda 1961)
  panini_data.txt https://github.com/ashtadhyayi-com/data  sutraani/data.txt
                  3,983 Aṣṭādhyāyī sūtras with padaccheda (pc), anuvṛtti (an)
                  and adhikāra (ad) fields.

Outputs:
  dsg_entries.tsv          4,383 DSG headwords + entry metrics
  dsg_dcs_join.tsv         the corrected DSG -> DCS join (HK -> SLP1 + variants)
  panini_word_forms.tsv    every word form in the sūtra reading, 3 frequency channels
  report.json              headline numbers + key-conversion audit

IMPORTANT (data-quality fix): the DSG page's column labelled ``slp1`` is
Harvard-Kyoto, NOT SLP1.  It used to be copied verbatim into
``dsg_entries.tsv`` under the key ``slp1``, which made every downstream join
to DCS silently wrong.  We now keep the raw value in ``hk`` and derive a real
SLP1 key (from HK when clean, otherwise from IAST), with class-nasal <->
anusvāra variants in a separate column.  See ``slp1_keys.py``.

No network calls at run time; the snapshots are pinned by SHA-256 in report.json.
"""
from __future__ import annotations

import collections
import hashlib
import html
import json
import os
import re
import sys


if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import slp1_keys as sk  # noqa: E402  (single source of truth for HK / IAST / SLP1)


def sha(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()


def strip_tags(s):
    s = re.sub(r"<br\s*/?>", " ", s, flags=re.I)
    s = re.sub(r"<[^>]+>", " ", s)
    return re.sub(r"\s+", " ", html.unescape(s)).strip()


# --------------------------------------------------------------------------- DSG
def parse_dsg():
    raw = open(os.path.join(HERE, "dsg_page.html"), encoding="utf-8", errors="replace").read()
    out = []
    for tr in re.findall(r"<tr[^>]*>(.*?)</tr>", raw, re.S):
        def cell(cls):
            m = re.search(r'class="' + cls + r'"[^>]*>(.*?)</[ap]>', tr, re.S)
            return strip_tags(m.group(1)) if m else ""
        deva = cell("sa")
        if not deva:
            continue
        m_id = re.search(r'<a id="(\d+)"', tr)
        m_en = re.search(r'<p class="transl">(.*?)</p>', tr, re.S)
        m_ru = re.search(r'<p class="transl2">(.*?)</p>', tr, re.S)
        en = strip_tags(m_en.group(1)) if m_en else ""
        ru = strip_tags(m_ru.group(1)) if m_ru else ""
        iast = cell("iast").strip("/ ")
        hk = cell("HK").strip("/ ")
        # Abhyankar's own cross-references are the best tradition-wide importance proxy:
        # how many times the entry cites Pāṇini / Mahābhāṣya / Kāśikā / a Vārttika.
        cites = {
            "panini": len(re.findall(r"\bP\.\s", en)),
            "mahabhasya": len(re.findall(r"\bM\.?\s?Bh\.", en)),
            "kasika": len(re.findall(r"\bKā[śs]\.", en)),
            "varttika": len(re.findall(r"\bVā?[āa]rt\.", en)),
            "pratisakhya": len(re.findall(r"\b[RTAXV]\.\s?Pr\.", en)),
        }
        # --- honest key derivation ------------------------------------------
        # The raw DSG value is HK. Keep it under `hk`; never expose it as SLP1.
        # Prefer the native HK headword when it is a clean Latin string and
        # agrees with the IAST headword; otherwise fall back to IAST.
        key_hk = sk.hk_to_slp1(hk) if sk.hk_is_clean(hk) else ""
        key_ia = sk.iast_to_slp1(iast)
        if key_hk and key_hk == key_ia:
            slp1, source = key_hk, "hk"
        elif key_hk and not key_ia:
            slp1, source = key_hk, "hk"
        elif key_hk and key_ia and key_hk != key_ia:
            slp1, source = key_ia, "iast:hk_mismatch"
        elif key_ia:
            slp1, source = key_ia, "iast"
        else:
            slp1, source = "", "none"
        variants = sorted(sk.slp1_variants(slp1) - {slp1}) if slp1 else []
        out.append({
            "id": int(m_id.group(1)) if m_id else len(out) + 1,
            "deva": deva, "iast": iast, "hk": hk,
            "slp1": slp1, "slp1_source": source,
            "slp1_variants": "|".join(variants),
            "en_chars": len(en), "ru_chars": len(ru),
            "cites": sum(cites.values()), "panini_cites": cites["panini"],
            "en": en, "ru": ru,
        })
    return out


def load_dcs():
    path = os.path.join(ROOT, "sanskrit-util/tools/KeySwap/data/dcs_freq.txt")
    dcs = {}
    for line in open(path, encoding="utf-8"):
        if line.startswith("#") or not line.strip():
            continue
        k, v = line.split()
        dcs[k] = int(v)
    return dcs, path


def key_audit(dsg):
    """Verify HK -> SLP1 against the independent IAST headword column."""
    agree = disagree = skipped = 0
    for x in dsg:
        if not sk.hk_is_clean(x["hk"]) or not sk.iast_to_slp1(x["iast"]):
            skipped += 1
            continue
        if sk.hk_to_slp1(x["hk"]) == sk.iast_to_slp1(x["iast"]):
            agree += 1
        else:
            disagree += 1
    return {"hk_clean_rows_compared": agree + disagree,
            "agree": agree, "disagree": disagree,
            "rows_not_comparable": skipped}


# ---------------------------------------------------------------- Aṣṭādhyāyī
def norm(w):
    """Light-touch normalisation: keep Devanāgarī virāma (it is structural, not a
    diacritic — dropping it turns प्रत्ययः into परतयय), drop only trailing
    visarga/anusvāra and surrounding punctuation."""
    w = w.strip().strip(".,;:!?()[]{}\"' \u0964\u0965")
    w = w.replace("\u2019", "").replace("\u2013", "-").replace("\u093d", "")
    w = re.sub(r"[\u0902\u0903]+$", "", w)  # trailing anusvāra / visarga
    return w


def words_in_field(field):
    """Yield the lexical word (before the $...$ annotation) of each ##-separated chunk."""
    if not field:
        return []
    res = []
    for chunk in field.split("##"):
        w = chunk.split("$")[0].strip()
        if not w:
            continue
        # Padaccheda annotates compounds with internal hyphens: keep both the
        # whole compound and its members (members are the terms students meet).
        for part in w.split("-"):
            p = norm(part)
            if p:
                res.append(p)
    return res


def parse_panini():
    j = json.loads(open(os.path.join(HERE, "panini_data.txt"), encoding="utf-8-sig").read())
    rows = j["data"]
    sutras = []
    for r in rows:
        ref = "%s.%s.%s" % (r["a"], r["p"], r["n"])
        sutras.append({
            "ref": ref,
            "deva": r.get("s", ""),
            "pc": words_in_field(r.get("pc", "")),
            "an": words_in_field(r.get("an", "")),
            "ad": words_in_field(r.get("ad", "")),
            "type": r.get("type", ""),
        })
    return sutras


def docfreq(sutras, field):
    """number of DISTINCT sūtras in which a word form occurs in this channel"""
    c = collections.Counter()
    for s in sutras:
        c.update(set(s[field]))
    return c


def main():
    dsg = parse_dsg()
    sutras = parse_panini()
    pc, an, ad = (docfreq(sutras, f) for f in ("pc", "an", "ad"))

    # explicit + inherited + governing scope = one combined "reading pressure" signal
    allforms = set(pc) | set(an) | set(ad)
    combined = {w: pc[w] + an[w] + ad[w] for w in allforms}

    dsg_cols = ("id", "deva", "iast", "hk", "slp1", "slp1_source",
                "slp1_variants", "en_chars", "ru_chars", "cites", "panini_cites")
    with open(os.path.join(HERE, "dsg_entries.tsv"), "w", encoding="utf-8") as f:
        f.write("\t".join(dsg_cols) + "\n")
        for e in dsg:
            f.write("\t".join(str(e[k]) for k in dsg_cols) + "\n")

    # --- corrected DSG -> DCS join -------------------------------------------
    # Every headword, with the honest HK value, the derived SLP1 key, ALL
    # SLP1 spelling variants tried, and the resulting DCS hit(s).  The
    # `naive_hk_*` columns show exactly what the old (wrong) join produced.
    dcs, dcs_path = load_dcs()
    join_cols = ("id", "deva", "iast", "hk", "slp1", "slp1_source",
                 "slp1_variants", "dcs_best_key", "dcs_count",
                 "dcs_variant_hits", "naive_hk_key", "naive_hk_count")
    naive_hits = corrected_hits = variant_only_hits = 0
    corrected_but_naive_missed = 0
    key_diffs = 0
    with open(os.path.join(HERE, "dsg_dcs_join.tsv"), "w", encoding="utf-8") as f:
        f.write("\t".join(join_cols) + "\n")
        for e in dsg:
            best, count, hits, tried = sk.dcs_lookup(dcs, e["slp1"])
            naive = dcs.get(e["hk"], 0)
            if naive:
                naive_hits += 1
            if count:
                corrected_hits += 1
                if not naive:
                    corrected_but_naive_missed += 1
                if best != e["slp1"]:
                    variant_only_hits += 1  # canonical key absent; a spelling variant hit
            if e["hk"] != e["slp1"]:
                key_diffs += 1
            f.write("\t".join((
                str(e["id"]), e["deva"], e["iast"], e["hk"], e["slp1"],
                e["slp1_source"], e["slp1_variants"], best, str(count),
                "|".join("%s=%d" % (k, v) for k, v in sorted(hits.items())),
                e["hk"], str(naive))) + "\n")

    with open(os.path.join(HERE, "panini_word_forms.tsv"), "w", encoding="utf-8") as f:
        f.write("word_deva\tsurface_pc\tanuvritti\tadhikara\tcombined\n")
        for w in sorted(allforms, key=lambda x: (-combined[x], x)):
            f.write("%s\t%d\t%d\t%d\t%d\n" % (w, pc[w], an[w], ad[w], combined[w]))

    # DSG composition: how much of the 4,383 is actually terminology vs. inventory?
    comp = collections.Counter()
    for e in dsg:
        t = e["en"].lower()
        if re.search(r"\b(kṛt|tad\.?|taddhita|kṛdanta|pratyaya|affix|suffix)\b", t[:220]) and \
           re.search(r"\baffix|suffix|pratyaya", t[:220]):
            comp["affix / pratyaya name"] += 1
        elif re.search(r"\baugment\b", t[:220]):
            comp["augment (āgama)"] += 1
        elif re.search(r"\bsubstitute\b|\bādeśa\b", t[:220]):
            comp["substitute (ādeśa)"] += 1
        elif re.search(r"\b(name of (a|an|the)|grammarian|author|work|treatise|commentary)\b", t[:260]):
            comp["author / work name"] += 1
        elif re.search(r"\broot\b", t[:220]):
            comp["root (dhātu) / root-list"] += 1
        elif re.search(r"\bclass\b|\bgaṇa\b", t[:220]):
            comp["gaṇa / word-class"] += 1
        else:
            comp["other (mostly saṃjñā, paribhāṣā, metalsense)"] += 1

    # saṃjñā definitions tagged in the dataset's `type` field
    samjna = collections.Counter()
    for s in sutras:
        for tag in re.findall(r"S\$([^$]*संज्ञा[^$]*)\$", s["type"]):
            samjna[norm(tag)] += 1

    rep = {
        "sources": {
            "dsg": {"file": "dsg_page.html", "sha256": sha(os.path.join(HERE, "dsg_page.html")),
                    "url": "https://samskrtam.ru/sanskrit-lexicon/dsg/", "entries": len(dsg)},
            "panini": {"file": "panini_data.txt", "sha256": sha(os.path.join(HERE, "panini_data.txt")),
                       "url": "https://github.com/ashtadhyayi-com/data sutraani/data.txt",
                       "sutras": len(sutras)},
        },
        "channels": {
            "pc": {"distinct_forms": len(pc), "occurrences": sum(pc.values()),
                   "sutras_with": sum(1 for s in sutras if s["pc"])},
            "an": {"distinct_forms": len(an), "occurrences": sum(an.values()),
                   "sutras_with": sum(1 for s in sutras if s["an"])},
            "ad": {"distinct_forms": len(ad), "occurrences": sum(ad.values()),
                   "sutras_with": sum(1 for s in sutras if s["ad"])},
        },
        "dsg_composition_first_definition_heuristic": dict(comp.most_common()),
        "dsg_samjna_like": len(samjna),
        "slp1_keys": {
            "issue": "DSG column labelled `slp1` is Harvard-Kyoto, not SLP1",
            "fix": "raw value kept in `hk`; SLP1 derived from HK or IAST; "
                   "class-nasal <-> anusvara variants generated for DCS joins",
            "module": "slp1_keys.py",
            "dcs_file": "sanskrit-util/tools/KeySwap/data/dcs_freq.txt",
            "dcs_sha256": sha(dcs_path),
            "hk_vs_iast_conversion_audit": key_audit(dsg),
            "slp1_source_counts": dict(collections.Counter(e["slp1_source"] for e in dsg)),
            "hk_present": sum(1 for e in dsg if e["hk"].strip()),
            "hk_clean": sum(1 for e in dsg if sk.hk_is_clean(e["hk"])),
            "entries_with_slp1_variants": sum(1 for e in dsg if e["slp1_variants"]),
            "dcs_join": {
                "dsg_entries": len(dsg),
                "headword_keys_differ_from_hk": key_diffs,
                "naive_hk_join_hits": naive_hits,
                "corrected_join_hits": corrected_hits,
                "hits_the_naive_join_missed": corrected_but_naive_missed,
                "hits_found_only_through_a_spelling_variant": variant_only_hits,
            },
        },
        "top_pc": pc.most_common(60),
        "top_an": an.most_common(60),
        "top_ad": ad.most_common(30),
        "top_combined": [(w, c) for w, c in sorted(combined.items(), key=lambda x: -x[1])[:80]],
        "top_dsg_by_cites": [(e["deva"], e["iast"], e["cites"], e["panini_cites"], e["en_chars"])
                             for e in sorted(dsg, key=lambda x: -x["cites"])[:40]],
        "top_dsg_by_length": [(e["deva"], e["iast"], e["en_chars"], e["cites"])
                              for e in sorted(dsg, key=lambda x: -x["en_chars"])[:30]],
    }
    with open(os.path.join(HERE, "report.json"), "w", encoding="utf-8") as f:
        json.dump(rep, f, ensure_ascii=False, indent=1)

    print("DSG entries:", len(dsg), " Aṣṭādhyāyī sūtras:", len(sutras))
    print("channels:", json.dumps(rep["channels"], ensure_ascii=False))
    print("\nDSG composition (first-definition heuristic):")
    for k, v in comp.most_common():
        print("  %-58s %5d  %5.1f%%" % (k, v, 100.0 * v / len(dsg)))
    print("\nTOP explicit padaccheda forms (distinct sūtras):")
    print("  " + "  ".join("%s:%d" % (w, c) for w, c in pc.most_common(40)))
    print("\nTOP anuvṛtti-inherited forms (# sūtras that inherit the word):")
    print("  " + "  ".join("%s:%d" % (w, c) for w, c in an.most_common(40)))
    print("\nTOP adhikāra governing words (# sūtras governed):")
    print("  " + "  ".join("%s:%d" % (w, c) for w, c in ad.most_common(25)))
    print("\nTOP DSG entries by citation count:")
    print("  " + "  ".join("%s(%d)" % (x[1], x[2]) for x in rep["top_dsg_by_cites"][:25]))
    print("\nTOP DSG entries by entry length:")
    print("  " + "  ".join("%s(%d)" % (x[1], x[2]) for x in rep["top_dsg_by_length"][:20]))
    k = rep["slp1_keys"]
    print("\nHK -> SLP1 key conversion:")
    print(" ", json.dumps(k["hk_vs_iast_conversion_audit"], ensure_ascii=False))
    print("  sources:", json.dumps(k["slp1_source_counts"], ensure_ascii=False))
    print("  DCS join:", json.dumps(k["dcs_join"], ensure_ascii=False))


if __name__ == "__main__":
    main()
