#!/usr/bin/env python3
"""Archive the Wiktionary Sanskrit-etymology category tree.

Writes byte-faithful source snapshots to wiki/archive/raw/, a checksum
manifest, a human-readable SNAPSHOT.md, and the two JS data files consumed by
the static pages. Re-run to refresh; every run records its own UTC timestamp.

Source: https://en.wiktionary.org/wiki/Category:Sanskrit_terms_by_etymology
Text is Wiktionary's (CC BY-SA); see Wiktionary:Copyrights.
"""
import hashlib
import html
import json
import re
import time
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "archive" / "raw"
DATA = ROOT / "data"
ARCH = ROOT / "archive"
RAW.mkdir(parents=True, exist_ok=True)
DATA.mkdir(parents=True, exist_ok=True)

BASE = "https://en.wiktionary.org"
CAT_TITLE = "Category:Sanskrit terms by etymology"
CAT_URL = BASE + "/wiki/Category:Sanskrit_terms_by_etymology"
API = BASE + "/w/api.php"
UA = "SanskritEtymologyArchive/1.0 (https://gasyoun.github.io/wiki/)"
NOW = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
STAMP = NOW[:10]


def get(url):
    req = urllib.request.Request(
        url, headers={"User-Agent": UA, "Accept-Encoding": "identity"}
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        return resp.read()


def api(params):
    params = dict(params, action="query", format="json", formatversion="2")
    return get(API + "?" + urllib.parse.urlencode(params))


def cat_url(title):
    if not title.startswith("Category:"):
        title = "Category:" + title
    return BASE + "/wiki/" + urllib.parse.quote(title.replace(" ", "_"), safe="_-:")


def word_url(deva):
    return BASE + "/wiki/" + urllib.parse.quote(deva, safe="") + "#Sanskrit"


def write_raw(name, payload, source):
    path = RAW / name
    path.write_bytes(payload)
    return {
        "file": "raw/" + name,
        "bytes": len(payload),
        "sha256": hashlib.sha256(payload).hexdigest(),
        "source": source,
        "fetched_at_utc": NOW,
    }


def parse_counts(page_html):
    """Read (N c, M e) from the CategoryTree markup in the raw page."""
    result = {}
    if isinstance(page_html, bytes):
        page_html = page_html.decode("utf-8", "replace")
    for li in re.findall(r"<li>.*?</li>", page_html, re.S):
        link = re.search(r'<a href="/wiki/(Category:[^"]+)" title="Category:([^"]+)"', li)
        count = re.search(r"\((\d+) c, (\d+) e\)", li)
        if not (link and count):
            continue
        title = html.unescape(link.group(2))
        result[title] = {"c": int(count.group(1)), "e": int(count.group(2))}
    return result


def members_of(title):
    params = {
        "list": "categorymembers",
        "cmtitle": title,
        "cmtype": "subcat|page",
        "cmlimit": "500",
    }
    out, cont = [], None
    while True:
        q = dict(params)
        if cont:
            q["cmcontinue"] = cont
        data = json.loads(api(q))
        out.extend({"ns": m["ns"], "title": m["title"]} for m in data["query"]["categorymembers"])
        cont = data.get("continue", {}).get("cmcontinue")
        if not cont or len(out) >= 20000:
            break
    return out


LENS = {
    "origin": {
        "borrowed terms", "borrowed back", "calques", "derived from other languages",
        "inherited terms", "semantic loans", "by Arabic root", "by Ashokan Prakrit root",
        "by Proto-Dravidian root", "by Proto-Dravidian word", "by Proto-Indo-Aryan root",
        "by Proto-Indo-European root", "by Proto-Indo-European word",
        "by Proto-Indo-Iranian root", "by Proto-South Dravidian root",
        "by Sanskrit root", "by Vedic Sanskrit root", "by Sanskritization",
    },
    "evidence": {
        "attributed to a specific source", "doublets", "neologisms", "nonce terms",
        "onomatopoeias", "reconstructed terms", "sound-symbolic", "defective word group",
        "unknown etymologies",
    },
}

DESC = {
    "Sanskrit back-formations": "Formed by reversing a supposed regular formation.",
    "Sanskrit borrowed terms": "Loanwords incorporated directly from another language.",
    "Sanskrit calques": "Piece-by-piece translations of terms from other languages.",
    "Sanskrit compound terms": "Terms composed of two or more stems (samāsa).",
    "Sanskrit words derived through corruption": "Result of a sporadic, non-systematic change.",
    "Sanskrit deverbals": "Terms derived from a verb.",
    "Sanskrit doublets": "Same ultimate source as another term, but a different route.",
    "Sanskrit inherited terms": "Inherited from an earlier stage of the language.",
    "Sanskrit words derived through metathesis": "Created by transposing sounds.",
    "Sanskrit neologisms": "Only recently acknowledged terms.",
    "Sanskrit nonce terms": "Invented for a single occasion.",
    "Sanskrit onomatopoeias": "Coined to sound like what they represent.",
    "Sanskrit reconstructed terms": "Not directly attested; reconstructed from evidence.",
    "Sanskrit reduplications": "Formed by repeating a root or stem.",
    "Sanskrit roots": "Basic morphemes (dhātu) from which words are formed.",
    "Sanskrit semantic loans": "A sense borrowed from a term in another language.",
    "Sanskrit sound-symbolic terms": "Sound symbolism, not strictly onomatopoeic.",
    "Sanskrit syncopic forms": "Loss of an interior sound or syllable.",
    "Sanskrit terms attributed to a specific source": "Coined by an identifiable person or work.",
    "Sanskrit terms by interfix": "Categorised by their interfixes.",
    "Sanskrit terms by prefix": "Categorised by their prefixes (upasarga).",
    "Sanskrit terms by root": "Categorised by the root they originate from.",
    "Sanskrit terms by suffix": "Categorised by their suffixes (pratyaya).",
    "Sanskrit terms derived from other languages": "Terms originating outside Sanskrit.",
    "Sanskrit terms with Indo-Aryan extensions": "Extended with pleonastic Indo-Aryan affixes.",
    "Sanskrit terms with unknown etymologies": "Etymology not yet established.",
    "Sanskrit univerbations": "Agglutination of two or more words into one.",
    "Sanskrit vrddhi derivatives": "Derived from a PIE root by vṛddhi derivation.",
}


def lens_for(name):
    for lens, needles in LENS.items():
        if any(n in name for n in needles):
            return lens
    return "formation"


GRADES = [
    {"vowels": "a / ā", "zero": "a / ā", "guna": "a", "vrddhi": "ā",
     "sandhi": "Before a following vowel: a and ā surface unchanged; only length changes.",
     "root": "पच्", "rootIast": "√pac",
     "gunaWord": "पचति", "gunaIast": "pacati",
     "vrddhiWord": "पाक", "vrddhiIast": "pāka",
     "gloss": "to cook → he cooks → cooking"},
    {"vowels": "i / ī", "zero": "i / ī", "guna": "e", "vrddhi": "ai",
     "sandhi": "Before a following vowel: e → ay, ai → āy (compare √ji + a → जय).",
     "root": "विद्", "rootIast": "√vid",
     "gunaWord": "वेद", "gunaIast": "veda",
     "vrddhiWord": "वैदिक", "vrddhiIast": "vaidika",
     "gloss": "to know → knowledge → Vedic"},
    {"vowels": "u / ū", "zero": "u / ū", "guna": "o", "vrddhi": "au",
     "sandhi": "Before a following vowel: o → av, au → āv (compare √bhū + a → भवति).",
     "root": "बुध्", "rootIast": "√budh",
     "gunaWord": "बोध", "gunaIast": "bodha",
     "vrddhiWord": "बौद्ध", "vrddhiIast": "bauddha",
     "gloss": "to wake → awakening → Buddhist"},
    {"vowels": "ṛ / ṝ", "zero": "ṛ / ṝ", "guna": "ar", "vrddhi": "ār",
     "sandhi": "Before a following vowel: ar and ār stay as they are (√kṛ → करोति, कार्य).",
     "root": "कृ", "rootIast": "√kṛ",
     "gunaWord": "करोति", "gunaIast": "karoti",
     "vrddhiWord": "कार्य", "vrddhiIast": "kārya",
     "gloss": "to do → he does → to be done"},
    {"vowels": "ḷ", "zero": "ḷ", "guna": "al", "vrddhi": "āl",
     "sandhi": "Before a following vowel: al and āl stay as they are; almost no roots are attested.",
     "root": "", "rootIast": "—",
     "gunaWord": "", "gunaIast": "—",
     "vrddhiWord": "", "vrddhiIast": "—",
     "gloss": "Rare in classical Sanskrit; listed for completeness"},
]


def main():
    manifest = []

    page = get(CAT_URL)
    manifest.append(write_raw("category.html", page, CAT_URL))
    counts = parse_counts(page)
    if len(counts) != 42:
        raise SystemExit("expected 42 subcategories, parsed %d" % len(counts))

    subs = api({"list": "categorymembers", "cmtitle": CAT_TITLE,
                "cmtype": "subcat", "cmlimit": "500"})
    sub_url = API + "?" + urllib.parse.urlencode(
        {"action": "query", "list": "categorymembers", "cmtitle": CAT_TITLE,
         "cmtype": "subcat", "cmlimit": "500", "format": "json"})
    manifest.append(write_raw("subcategories.json", subs, sub_url))

    wt_url = API + "?" + urllib.parse.urlencode(
        {"action": "parse", "page": CAT_TITLE, "prop": "wikitext", "format": "json"})
    wt = get(wt_url)
    manifest.append(write_raw("category-wikitext.json", wt, wt_url))

    rt_url = API + "?" + urllib.parse.urlencode(
        {"action": "parse", "page": CAT_TITLE, "prop": "text", "format": "json",
         "formatversion": "2"})
    manifest.append(write_raw("category-rendered.json", get(rt_url), rt_url))

    titles = sorted(counts)
    tree = {}
    for i, title in enumerate(titles, 1):
        tree[title] = members_of("Category:" + title)
        print("[%02d/42] %-70s %5d members" % (i, title[:70], len(tree[title])), flush=True)
        time.sleep(0.12)
    tree_payload = json.dumps(
        {"fetched_at_utc": NOW, "parent": CAT_URL, "categories": tree},
        ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    manifest.append(write_raw(
        "subcategory-members.json", tree_payload,
        [API + "?list=categorymembers&cmtitle=" + urllib.parse.quote(t) for t in titles]))

    categories = []
    for t in titles:
        categories.append({
            "name": t, "url": cat_url(t), "c": counts[t]["c"], "e": counts[t]["e"],
            "lens": lens_for(t), "desc": DESC.get(t, "Terms grouped by this etymological type."),
        })

    doc = {
        "snapshot_id": "sanskrit-etymology-" + STAMP,
        "created_at_utc": NOW,
        "source": {
            "category_page": CAT_URL,
            "api": API,
            "rights": "Wiktionary text is CC BY-SA; see "
                      "https://en.wiktionary.org/wiki/Wiktionary:Copyrights",
        },
        "purpose": "Restorable backup of the source taxonomy if the Wiktionary "
                   "category is moved, renamed or lost.",
        "totals": {"subcategories": len(categories),
                   "direct_members_captured": sum(len(v) for v in tree.values())},
        "files": manifest,
    }
    (ARCH / "manifest.json").write_text(
        json.dumps(doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (DATA / "manifest.js").write_text(
        "window.ETYMOLOGY_MANIFEST = " + json.dumps(doc, ensure_ascii=False) + ";\n",
        encoding="utf-8")

    for g in GRADES:
        g["rootUrl"] = word_url(g["root"]) if g["root"] else ""
        g["gunaUrl"] = word_url(g["gunaWord"]) if g["gunaWord"] else ""
        g["vrddhiUrl"] = word_url(g["vrddhiWord"]) if g["vrddhiWord"] else ""
    payload = {
        "snapshotId": doc["snapshot_id"], "fetchedAtUtc": NOW,
        "categoryUrl": CAT_URL, "categories": categories, "grades": GRADES,
        "sourceLinks": {
            "vrddhi": cat_url("Category:Sanskrit vrddhi derivatives"),
            "roots": cat_url("Category:Sanskrit roots"),
            "pieRoots": cat_url("Category:Sanskrit terms by Proto-Indo-European root"),
            "unknown": cat_url("Category:Sanskrit terms with unknown etymologies"),
            "copyrights": "https://en.wiktionary.org/wiki/Wiktionary:Copyrights",
        },
    }
    (DATA / "etymology.js").write_text(
        "window.ETYMOLOGY = " + json.dumps(payload, ensure_ascii=False, indent=1) + ";\n",
        encoding="utf-8")

    lines = [
        "# Source snapshot — Sanskrit terms by etymology", "",
        "Snapshot `%s`, taken %s." % (doc["snapshot_id"], NOW), "",
        "Byte-faithful backup of [%s](%s) and its 42 subcategories, including"
        % (CAT_TITLE, CAT_URL),
        "every direct member one level down (%d titles)."
        % doc["totals"]["direct_members_captured"], "",
        "The parent category contains **no word pages at all** — only subcategories —"
        " so a backup",
        "of the parent page alone would preserve the labels but none of the words.",
        "See [manifest.json](manifest.json) for SHA-256 checksums and source URLs.",
        "", "## Raw files", "",
        "| File | Bytes | SHA-256 |", "| --- | ---: | --- |",
    ]
    for f in manifest:
        lines.append("| [`%s`](%s) | %d | `%s` |"
                     % (f["file"].split("/")[-1], f["file"], f["bytes"], f["sha256"]))
    lines += ["", "## The 42 subcategories", "",
              "`c` = subcategories, `e` = word pages. Both are as displayed on the"
              " source page at snapshot time.", "",
              "| Subcategory | c | e |", "| --- | ---: | ---: |"]
    for cat in categories:
        lines.append("| [%s](%s) | %d | %d |" % (cat["name"], cat["url"], cat["c"], cat["e"]))
    lines += ["", "## Category descriptions (source page intro)", ""]
    for name in sorted(DESC):
        lines.append("- **%s** — %s" % (name, DESC[name]))
    lines += [
        "", "## Rights", "",
        "Wiktionary text is available under CC BY-SA; see"
        " [Wiktionary:Copyrights](%s)." % payload["sourceLinks"]["copyrights"],
        "This snapshot reproduces category names and counts for teaching and"
        " citation, with a link back to the original on every item.", "",
        "Regenerate with `python3 wiki/scripts/fetch_snapshot.py`.", "",
    ]
    (ARCH / "SNAPSHOT.md").write_text("\n".join(lines), encoding="utf-8")

    print("OK: %d categories, %d members, %d raw files" %
          (len(categories), doc["totals"]["direct_members_captured"], len(manifest)))


if __name__ == "__main__":
    main()
