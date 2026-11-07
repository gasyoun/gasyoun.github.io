#!/usr/bin/env python3
"""Fetch sourced PIE cognate sets and the four inheritance-layer word lists.

For each PIE root/word we look up Wiktionary's per-language
"terms derived from the Proto-Indo-European root/word *X" categories and store
their real page members. Nothing here is invented: every displayed reflex comes
from a category member on the live source.

Outputs: archive/raw/cognates.json, archive/cognates-manifest.json,
data/cognates.js. Re-run fetch_snapshot.py afterwards to fold cognates.json
into the main SHA-256 manifest.
"""
import json
import time
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "archive" / "raw"
DATA = ROOT / "data"
ARCH = ROOT / "archive"
BASE = "https://en.wiktionary.org"
API = BASE + "/w/api.php"
UA = "SanskritEtymologyArchive/1.0 (https://gasyoun.github.io/wiki/)"
NOW = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

ITEMS = [
    ("root", "*bʰer-", "to bear, carry"),
    ("root", "*h₁es-", "to be"),
    ("root", "*ǵenh₁-", "to beget, give birth"),
    ("root", "*dʰeh₁-", "to put, place, do"),
    ("root", "*ped-", "foot, to tread"),
    ("root", "*ḱerd-", "heart"),
    ("root", "*meh₁-", "to measure"),
    ("root", "*h₂eǵ-", "to drive, lead"),
    ("root", "*bʰeh₂-", "to shine, to speak"),
    ("word", "*ph₂tḗr", "father"),
    ("word", "*méh₂tēr", "mother"),
    ("word", "*bʰréh₂tēr", "brother"),
    ("word", "*pṓds", "foot"),
    ("word", "*ḱm̥tóm", "hundred"),
    ("word", "*déḱm̥", "ten"),
    ("word", "*dwóh₁", "two"),
    ("word", "*dyḗws", "sky, daylight, sky-god"),
    ("word", "*wódr̥", "water"),
]

LANGS = [
    ("Sanskrit", "Indo-Iranian"),
    ("Avestan", "Indo-Iranian"),
    ("Proto-Indo-Iranian", "Indo-Iranian"),
    ("Vedic Sanskrit", "Indo-Iranian"),
    ("Ancient Greek", "Hellenic"),
    ("Latin", "Italic"),
    ("Old English", "Germanic"),
    ("English", "Germanic"),
]

LAYERS = [
    "Category:Sanskrit terms inherited from Proto-Indo-European",
    "Category:Sanskrit terms inherited from Proto-Indo-Iranian",
    "Category:Sanskrit terms inherited from Proto-Indo-Aryan",
    "Category:Sanskrit terms inherited from Vedic Sanskrit",
]


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept-Encoding": "identity"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read()


def query(params):
    params = dict(params, action="query", format="json", formatversion="2")
    return json.loads(get(API + "?" + urllib.parse.urlencode(params)))


def page_url(title):
    return BASE + "/wiki/" + urllib.parse.quote(title.replace(" ", "_"), safe="_-:()")


def cat_title(lang, kind, form):
    return "Category:%s terms derived from the Proto-Indo-European %s %s" % (lang, kind, form)


def existing(titles):
    out = set()
    for i in range(0, len(titles), 40):
        chunk = titles[i:i + 40]
        data = query({"titles": "|".join(chunk)})
        for p in data["query"]["pages"]:
            if not p.get("missing"):
                out.add(p["title"])
    return out


def members(title, cap=3000):
    params = {"list": "categorymembers", "cmtitle": title, "cmtype": "page", "cmlimit": "500"}
    out, cont = [], None
    while True:
        q = dict(params)
        if cont:
            q["cmcontinue"] = cont
        data = query(q)
        out.extend(m["title"] for m in data["query"]["categorymembers"])
        cont = data.get("continue", {}).get("cmcontinue")
        if not cont or len(out) >= cap:
            break
    return out[:cap]


def reconstruction_url(kind, form):
    stem = form.lstrip("*")
    return BASE + "/wiki/" + urllib.parse.quote("Reconstruction:Proto-Indo-European/" + stem, safe="_-:")


def main():
    all_cats = [cat_title(l, k, f) for k, f, _ in ITEMS for l, _ in LANGS]
    print("checking %d language categories…" % len(all_cats), flush=True)
    found = existing(all_cats)
    recon_titles = [urllib.parse.unquote(
        reconstruction_url(k, f).split("/wiki/")[-1].replace("_", " "))
        for k, f, _ in ITEMS]
    recon_ok = existing(recon_titles)
    sources = []

    items = []
    for kind, form, gloss in ITEMS:
        cells = []
        for lang, branch in LANGS:
            title = cat_title(lang, kind, form)
            if title not in found:
                continue
            words = members(title)
            sources.append({"category": title, "url": page_url(title),
                            "member_count": len(words), "form": form, "language": lang})
            cells.append({"lang": lang, "branch": branch, "url": page_url(title),
                          "total": len(words), "words": words})
            time.sleep(0.08)
        if not cells:
            continue
        ru = reconstruction_url(kind, form)
        rt = urllib.parse.unquote(ru.split("/wiki/")[-1].replace("_", " "))
        if rt not in recon_ok:
            ru = page_url(cat_title("Sanskrit", kind, form))
        items.append({"kind": kind, "form": form, "gloss": gloss,
                      "reconstruction": ru,
                      "sanskritCategory": page_url(cat_title("Sanskrit", kind, form)),
                      "cells": cells})
        print("%-14s %-16s %d languages" % (form, gloss[:15], len(cells)), flush=True)

    layers = []
    for title in LAYERS:
        words = members(title)
        short = sorted([w for w in words if not w.startswith("Reconstruction:")
                        and not w.startswith("-")], key=lambda w: (len(w), w))[:8]
        layers.append({"title": title, "url": page_url(title),
                       "total": len(words), "words": words[:12], "short": short})
        sources.append({"category": title, "url": page_url(title),
                        "member_count": len(words), "form": "inheritance layer",
                        "language": "Sanskrit"})
        print("layer %-62s %d words" % (title[:62], len(words)), flush=True)
        time.sleep(0.08)

    doc = {
        "fetched_at_utc": NOW,
        "source": BASE + "/w/api.php",
        "method": "Members of Wiktionary's per-language 'terms derived from the "
                  "Proto-Indo-European root/word *X' categories. Glosses are short "
                  "teaching labels; the reconstruction link gives the full entry.",
        "items": items, "layers": layers,
    }
    (RAW / "cognates.json").write_text(
        json.dumps(doc, ensure_ascii=False, separators=(",", ":")) + "\n", encoding="utf-8")
    (ARCH / "cognates-manifest.json").write_text(
        json.dumps({"fetched_at_utc": NOW, "source_urls": sources,
                    "note": "One entry per queried Wiktionary category."},
                   ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    def core(words):
        cands = [w for w in words if not w.startswith("Reconstruction:")
                 and not w.startswith("-") and not w.isupper()]
        return sorted(cands, key=lambda w: (len(w), w.casefold()))[:5]

    def recon(words):
        return [w for w in words if w.startswith("Reconstruction:")][:4]

    slim = {
        "fetchedAtUtc": NOW,
        "languages": [l for l, _ in LANGS],
        "items": [{
            "kind": it["kind"], "form": it["form"], "gloss": it["gloss"],
            "reconstruction": it["reconstruction"],
            "sanskritCategory": it["sanskritCategory"],
            "cells": [{"lang": c["lang"], "branch": c["branch"], "url": c["url"],
                       "total": c["total"], "short": core(c["words"]),
                       "recon": recon(c["words"])} for c in it["cells"]]
        } for it in items],
        "layers": layers,
    }
    (DATA / "cognates.js").write_text(
        "window.ETYMOLOGY_COGNATES = " +
        json.dumps(slim, ensure_ascii=False, separators=(",", ":")) + ";\n", encoding="utf-8")
    print("OK: %d cognate sets, %d inheritance layers, %d source categories" %
          (len(items), len(layers), len(sources)))


if __name__ == "__main__":
    main()
