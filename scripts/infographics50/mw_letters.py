#!/usr/bin/env python3
"""MW letters census — entries of Monier-Williams (csl-orig v02/mw) per first letter.

Derives infographics/mw-letters-*/data.tsv + data.json.
An entry = one <L> record. First letter = first char of <k1> (SLP1), mapped to Devanagari.
Counted source: csl-orig/v02/mw/mw.txt
"""
import collections
import json
import os

SLP1_TO_DEVANAGARI = {
    "a": "अ", "A": "आ", "i": "इ", "I": "ई", "u": "उ", "U": "ऊ",
    "f": "ऋ", "F": "ॠ", "x": "ऌ", "X": "ॡ",
    "e": "ए", "E": "ऐ", "o": "ओ", "O": "औ",
    "k": "क", "K": "ख", "g": "ग", "G": "घ", "N": "ङ",
    "c": "च", "C": "छ", "j": "ज", "J": "झ", "Y": "ञ",
    "w": "ट", "W": "ठ", "q": "ड", "Q": "ढ", "R": "ण",
    "t": "त", "T": "थ", "d": "द", "D": "ध", "n": "न",
    "p": "प", "P": "फ", "b": "ब", "B": "भ", "m": "म",
    "y": "य", "r": "र", "l": "ल", "v": "व",
    "S": "श", "z": "ष", "s": "स", "h": "ह",
}

SOURCE = os.path.join(os.path.dirname(__file__),
                      "..", "..", "..", "csl-orig", "v02", "mw", "mw.txt")
OUT_DIR = os.path.join(os.path.dirname(__file__),
                       "..", "..", "infographics", "mw-letters-2026-08-29")


def main():
    counts = collections.Counter()
    total = 0
    unmapped = collections.Counter()
    with open(SOURCE, encoding="utf-8") as f:
        for line in f:
            i = line.find("<k1>")
            if i < 0:
                continue
            total += 1
            ch = line[i + 4]
            if ch in SLP1_TO_DEVANAGARI:
                counts[ch] += 1
            else:
                unmapped[ch] += 1
    # dictionary order: vowels, then varga consonants, then semivowels/sibilants
    rows = [(SLP1_TO_DEVANAGARI[ch], ch, counts[ch]) for ch in SLP1_TO_DEVANAGARI]
    assert sum(n for _, _, n in rows) == total, "unmapped first chars exist"
    if unmapped:
        print("UNMAPPED (excluded):", dict(unmapped))
    os.makedirs(OUT_DIR, exist_ok=True)
    tsv = os.path.join(OUT_DIR, "data.tsv")
    with open(tsv, "w", encoding="utf-8") as f:
        f.write("deva\tslp1\tentries\n")
        for deva, slp1, n in rows:
            f.write("%s\t%s\t%d\n" % (deva, slp1, n))
    js = os.path.join(OUT_DIR, "data.json")
    with open(js, "w", encoding="utf-8") as f:
        json.dump({"total": total, "source": "csl-orig/v02/mw/mw.txt",
                   "rows": [{"deva": d, "slp1": s, "entries": n} for d, s, n in rows]},
                  f, ensure_ascii=False, indent=1)
    top = max(rows, key=lambda r: r[2])
    print("total entries:", total, "| letters:", len(rows),
          "| top: %s (%s) %d" % (top[0], top[1], top[2]))
    print("wrote", tsv)


if __name__ == "__main__":
    main()
