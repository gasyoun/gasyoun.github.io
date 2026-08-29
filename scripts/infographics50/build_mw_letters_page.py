#!/usr/bin/env python3
"""Inject derived bars into template.html -> index.html (mw-letters infographic)."""
import json
import os

BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
DATA = os.path.join(BASE, "infographics", "mw-letters-2026-08-29", "data.json")
TEMPLATE = os.path.join(BASE, "infographics", "mw-letters-2026-08-29", "template.html")
OUT = os.path.join(BASE, "infographics", "mw-letters-2026-08-29", "index.html")

IAST = {"a": "a", "A": "ā", "i": "i", "I": "ī", "u": "u", "U": "ū",
        "f": "ṛ", "F": "ṝ", "x": "ḷ", "X": "ḹ", "e": "e", "E": "ai",
        "o": "o", "O": "au", "k": "ka", "K": "kha", "g": "ga", "G": "gha",
        "N": "ṅa", "c": "ca", "C": "cha", "j": "ja", "J": "jha", "Y": "ña",
        "w": "ṭa", "W": "ṭha", "q": "ḍa", "Q": "ḍha", "R": "ṇa", "t": "ta",
        "T": "tha", "d": "da", "D": "dha", "n": "na", "p": "pa", "P": "pha",
        "b": "ba", "B": "bha", "m": "ma", "y": "ya", "r": "ra", "l": "la",
        "v": "va", "S": "śa", "z": "ṣa", "s": "sa", "h": "ha"}
VOWELS = set("aAiIuUfFxeEoO")
TOP = {"s", "p", "v", "a", "k", "m"}
X0, PITCH, BW, YBASE, PLOTH = 90, 37.4, 29, 910, 600


def fmt(v):
    return "{:,}".format(v).replace(",", " ")


def main():
    d = json.load(open(DATA, encoding="utf-8"))
    rows = d["rows"]
    mx = max(r["entries"] for r in rows)
    parts = []
    for i, r in enumerate(rows):
        v = r["entries"]
        h = max(2, round(v / mx * PLOTH))
        x = X0 + i * PITCH + 4
        cls = "hero" if r["slp1"] == "s" else ("vowel" if r["slp1"] in VOWELS else "cons")
        parts.append('<rect class="bar %s" x="%.1f" y="%d" width="%s" height="%d"/>' % (cls, x, YBASE - h, BW, h))
        parts.append('<text class="glyph" x="%.1f" y="%d" text-anchor="middle">%s</text>' % (x + BW / 2, YBASE + 34, r["deva"]))
        if r["slp1"] in TOP:
            vcls = "val-hero" if r["slp1"] == "s" else "val"
            parts.append('<text class="%s" x="%.1f" y="%d" text-anchor="middle">%s</text>' % (vcls, x + BW / 2, YBASE - h - 10, fmt(v)))
        parts.append('<text class="iast" x="%.1f" y="%d" text-anchor="middle">%s</text>' % (x + BW / 2, YBASE + 52, IAST[r["slp1"]]))
    html = open(TEMPLATE, encoding="utf-8").read()
    assert "<!--BARS-->" in html
    html = html.replace("<!--BARS-->", "\n    ".join(parts))
    open(OUT, "w", encoding="utf-8").write(html)
    print("wrote", OUT, "| bars:", len(rows))


if __name__ == "__main__":
    main()
