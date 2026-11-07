#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate the learning-gain experiment's item bank and an offline pilot quiz.

All items are derived from the SAME pinned snapshots used by measure.py:

  panini_data.txt   3,983 sutras with pc / an / ad
  core_terms.tsv    119 curated terms in 7 batches (via build_batches.T)
  ru_glossary.py    Russian glosses

Three item types
  gloss              term -> Russian meaning
  implicit_trained   recover an unwritten term in sutras of adhyayas 1-3
  implicit_transfer  recover an unwritten term in sutras of adhyayas 4-8
                     (held out from the teaching materials by design)

The "implicit" types are the specific skill the three structural channels
predict: the term is required to read the sutra but is supplied only by
anuvrtti or adhikara, never written in the padaccheda.

Outputs (into site/):
  data/item_bank.tsv        all items, including a reserve pool
  data/item_bank_stats.json reproducible counts for the Russian protocol
  quiz.html                 self-contained offline instrument, forms A / B
"""
from __future__ import annotations

import csv
import json
import os
import random
import re
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import measure                    # noqa: E402
import build_batches as bb        # noqa: E402
import ru_glossary as ru          # noqa: E402

SITE = os.path.join(HERE, "site")
DATA = os.path.join(SITE, "data")
os.makedirs(DATA, exist_ok=True)

SEED = 20261107
RNG = random.Random(SEED)


# ----------------------------------------------------------------- term matchers
def build_terms():
    """Reuse exactly the curated matchers from build_batches.py."""
    out = []
    for deva, iast, gloss, batch, sutra, prefixes in bb.T:
        exact = {bb.norm(x[1:]) for x in prefixes if x.startswith("=")}
        exclude = [bb.norm(x[1:]) for x in prefixes if x.startswith("!")]
        pref = [bb.norm(x) for x in prefixes if not x.startswith(("=", "!"))]

        def m(w, exact=exact, exclude=exclude, pref=pref):
            if any(w.startswith(p) for p in exclude):
                return False
            return w in exact or any(w.startswith(p) for p in pref if p)

        out.append({
            "deva": deva, "iast": iast, "gloss": gloss, "batch": batch,
            "sutra": sutra, "m": m,
            "ru": ru.RU.get(iast, gloss),
            "total": 0, "explicit": 0, "inherited": 0, "governed": 0,
        })
    # measured counts, for item metadata
    measured = {}
    for r in csv.DictReader(open(os.path.join(HERE, "core_terms.tsv"), encoding="utf-8"), delimiter="\t"):
        measured[r["iast"]] = r
    for t in out:
        r = measured.get(t["iast"])
        if r:
            for k in ("total", "explicit", "inherited", "governed"):
                t[k] = int(r[k])
    return out


# --------------------------------------------------------------- implicit slots
def collect_implicit(sutras, terms):
    cands = []
    for s in sutras:
        if not s["deva"] or not s["pc"]:
            continue
        pc_t, an_t, ad_t = set(), set(), set()
        for i, t in enumerate(terms):
            f = t["m"]
            if any(f(w) for w in s["pc"]):
                pc_t.add(i)
            if any(f(w) for w in s["an"]):
                an_t.add(i)
            if any(f(w) for w in s["ad"]):
                ad_t.add(i)
        for i in (an_t | ad_t) - pc_t:
            # Group labels ("prathama / madhyama / uttama", "lopa / luk / ...")
            # are curricular concepts, not single recoverable word forms. They
            # belong in gloss items, not in "recover the unwritten word" items.
            if " / " in terms[i]["iast"]:
                continue
            cands.append({
                "term": i, "sutra": s,
                "channel": "adhikāra" if i in ad_t else "anuvṛtti",
                "adhyaya": int(s["ref"].split(".")[0]),
                "padaccheda": " ".join(s["pc"]),
            })
    return cands


# ------------------------------------------------------------------ distractors
def distractors(terms, idx, n=3, gloss=False):
    t = terms[idx]
    pool = [j for j, u in enumerate(terms)
            if j != idx and u["batch"] == t["batch"]
            and (not gloss or u["ru"] != t["ru"])]
    pool.sort(key=lambda j: (abs(terms[j]["total"] - t["total"]), j))
    if len(pool) < n:
        pool += [j for j, u in enumerate(terms)
                 if j != idx and u["batch"] != t["batch"] and j not in pool][:n - len(pool)]
    return pool[:n]


def option_text(terms, idx):
    t = terms[idx]
    return "%s — %s" % (t["deva"], t["iast"])


def make_item(terms, item_id, form, kind, term_idx, cand=None):
    t = terms[term_idx]
    shuffle = random.Random(SEED * 31 + item_id * 977)
    if kind == "gloss":
        opts = [t["ru"]] + [terms[j]["ru"] for j in distractors(terms, term_idx, gloss=True)]
        correct_text = t["ru"]
        prompt = "Что означает термин <b>%s</b> (%s)?" % (t["deva"], t["iast"])
        ref, deva, pada, channel = "", "", "", ""
    else:
        opts = [option_text(terms, term_idx)] + \
               [option_text(terms, j) for j in distractors(terms, term_idx)]
        correct_text = option_text(terms, term_idx)
        prompt = ("Восстановите слово, которое <b>не написано</b> в этой сутре, "
                  "но переносится из предыдущей сутры (anuvṛtti) либо задаётся "
                  "управляющим заголовком (adhikāra).")
        ref, deva, pada, channel = (cand["sutra"]["ref"], cand["sutra"]["deva"],
                                    cand["padaccheda"], cand["channel"])
    order = list(range(len(opts)))
    shuffle.shuffle(order)
    options = [opts[k] for k in order]
    answer = options.index(correct_text)
    return {
        "id": item_id, "form": form, "type": kind,
        "batch": t["batch"], "term_deva": t["deva"], "term_iast": t["iast"],
        "sutra_ref": ref, "sutra_deva": deva, "padaccheda": pada, "channel": channel,
        "prompt": prompt, "options": options, "answer": answer,
        "ru_gloss": t["ru"],
        "total": t["total"], "explicit": t["explicit"],
        "inherited": t["inherited"], "governed": t["governed"],
    }


# ------------------------------------------------------------------- item forms
def pick(pool, n, used_keys, per_term_cap, terms, batch_cap=2, exclude=(0,)):
    """Round-robin across batches so the implicit subscale is not swamped by
    B2 governance terms. B0 operators are excluded: they show ceiling effects
    and are dropped from the primary endpoint anyway."""
    import collections
    by_batch = collections.defaultdict(list)
    for c in pool:
        b = terms[c["term"]]["batch"]
        if b not in exclude:
            by_batch[b].append(c)
    chosen, per_term, per_batch = [], {}, {}
    batches = sorted(by_batch)
    while len(chosen) < n:
        progressed = False
        for b in batches:
            if per_batch.get(b, 0) >= batch_cap:
                continue
            cand = None
            for c in by_batch[b]:
                key = (c["term"], c["sutra"]["ref"])
                if key in used_keys or per_term.get(c["term"], 0) >= per_term_cap:
                    continue
                cand = c
                break
            if cand is None:
                continue
            used_keys.add((cand["term"], cand["sutra"]["ref"]))
            chosen.append(cand)
            per_term[cand["term"]] = per_term.get(cand["term"], 0) + 1
            per_batch[b] = per_batch.get(b, 0) + 1
            progressed = True
            if len(chosen) >= n:
                break
        if not progressed:
            break
    if len(chosen) < n:  # relax the batch cap if a bucket is thin
        for c in pool:
            if terms[c["term"]]["batch"] in exclude:
                continue
            key = (c["term"], c["sutra"]["ref"])
            if key in used_keys:
                continue
            chosen.append(c)
            used_keys.add(key)
            if len(chosen) >= n:
                break
    return chosen


def main():
    sutras = measure.parse_panini()
    terms = build_terms()
    cands = collect_implicit(sutras, terms)
    RNG.shuffle(cands)

    trained = [c for c in cands if c["adhyaya"] <= 3]
    transfer = [c for c in cands if c["adhyaya"] >= 4]

    # Cap each term's dominance, then take disjoint A/B forms.
    used = set()
    forms = {}
    for form in ("A", "B"):
        tr = pick(trained, 10, used, 2, terms)
        tf = pick(transfer, 10, used, 2, terms)
        # top up from whichever bucket still has material
        if len(tr) < 10:
            tr += pick(transfer, 10 - len(tr), used, 2, terms)
        if len(tf) < 10:
            tf += pick(trained, 10 - len(tf), used, 2, terms)
        forms[form] = (tr, tf)

    items, next_id = [], 1
    gloss_pool = list(range(len(terms)))
    RNG.shuffle(gloss_pool)
    gi = 0
    for form in ("A", "B"):
        tr, tf = forms[form]
        for kind, bucket in (("implicit_trained", tr), ("implicit_transfer", tf)):
            for c in bucket:
                items.append(make_item(terms, next_id, form, kind, c["term"], c))
                next_id += 1
        for _ in range(10):
            if gi >= len(gloss_pool):
                gi = 0
            idx = gloss_pool[gi]
            gi += 1
            items.append(make_item(terms, next_id, form, "gloss", idx))
            next_id += 1

    # Reserve pool: further implicit items for future parallel forms
    used_keys = {(i["term_iast"], i["sutra_ref"]) for i in items if i["type"] != "gloss"}
    reserve = 0
    for c in cands:
        if reserve >= 180:
            break
        if terms[c["term"]]["batch"] == 0:
            continue
        key = (terms[c["term"]]["iast"], c["sutra"]["ref"])
        if key in used_keys:
            continue
        kind = "implicit_trained" if c["adhyaya"] <= 3 else "implicit_transfer"
        items.append(make_item(terms, next_id, "R", kind, c["term"], c))
        next_id += 1
        reserve += 1
        used_keys.add(key)

    # ------------------------------------------------------------- item_bank.tsv
    cols = ["item_id", "form", "type", "batch", "term_deva", "term_iast",
            "sutra_ref", "channel", "sutra_deva", "padaccheda",
            "correct", "options", "answer_index", "ru_gloss",
            "total", "explicit", "inherited", "governed"]
    with open(os.path.join(DATA, "item_bank.tsv"), "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, delimiter="\t", lineterminator="\n")
        w.writerow(cols)
        for i in items:
            w.writerow([i["id"], i["form"], i["type"], i["batch"], i["term_deva"],
                        i["term_iast"], i["sutra_ref"], i["channel"], i["sutra_deva"],
                        i["padaccheda"], i["options"][i["answer"]], "|".join(i["options"]),
                        i["answer"], i["ru_gloss"], i["total"], i["explicit"],
                        i["inherited"], i["governed"]])

    bank = [i for i in items if i["form"] in ("A", "B")]
    stats = {
        "sutras": len(sutras),
        "core_terms": len(terms),
        "terms_with_russian_gloss": sum(1 for t in terms if t["iast"] in ru.RU),
        "implicit_candidates": len(cands),
        "implicit_by_channel": {
            "adhikāra": sum(1 for c in cands if c["channel"] == "adhikāra"),
            "anuvṛtti": sum(1 for c in cands if c["channel"] == "anuvṛtti"),
        },
        "implicit_by_adhyaya": {str(a): sum(1 for c in cands if c["adhyaya"] == a)
                                for a in range(1, 9)},
        "forms": {form: {
            "total": sum(1 for i in bank if i["form"] == form),
            "by_type": {k: sum(1 for i in bank if i["form"] == form and i["type"] == k)
                        for k in ("gloss", "implicit_trained", "implicit_transfer")},
            "distinct_terms": len({i["term_iast"] for i in bank if i["form"] == form}),
            "distinct_sutras": len({i["sutra_ref"] for i in bank
                                    if i["form"] == form and i["sutra_ref"]}),
            "implicit_by_batch": {str(b): sum(1 for i in bank if i["form"] == form
                                              and i["type"] != "gloss" and i["batch"] == b)
                                  for b in range(7)},
        } for form in ("A", "B")},
        "reserve_items": reserve,
        "total_items_in_bank": len(items),
    }
    with open(os.path.join(DATA, "item_bank_stats.json"), "w", encoding="utf-8") as f:
        json.dump(stats, f, ensure_ascii=False, indent=1)

    # ------------------------------------------------------------------- quiz.html
    tpl = open(os.path.join(HERE, "templates", "quiz.ru.html"), encoding="utf-8").read()
    payload = json.dumps(bank, ensure_ascii=False).replace("</", "<\\/")
    meta = {
        "forms": stats["forms"],
        "core_terms": stats["core_terms"],
        "russian_glosses": stats["terms_with_russian_gloss"],
    }
    out = (tpl.replace("__ITEMS__", payload)
              .replace("__META__", json.dumps(meta, ensure_ascii=False))
              .replace("__TITLE__", "Пилотный тест: прирост понимания терминов"))
    with open(os.path.join(SITE, "quiz.html"), "w", encoding="utf-8") as f:
        f.write(out)

    print(json.dumps(stats, ensure_ascii=False, indent=1))
    print("\nwrote site/quiz.html (%d bytes), site/data/item_bank.tsv (%d rows)" %
          (len(out.encode("utf-8")), len(items)))


if __name__ == "__main__":
    main()
