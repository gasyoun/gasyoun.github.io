#!/usr/bin/env python3
"""Case roads #21 — how five pedagogical grammars talk about the cases.

Derives infographics/case-roads-2026-08-29/{data.json,index.html}.
Sources: SanskritGrammar/{WhitneyGrammar_1889,ApteSyntax_1885,BuhlerLeitfaden_1923,
KocherginaUchebnik_1998,KnauerFrazy_1908} mdx corpora.
Counting: full case names + standard abbreviations (EN words; DE capitalized abbrs;
RU full words in the book's own text). Zeros are findings, not gaps — Knauer's
phrase book never names a case.
"""
import glob
import json
import os
import re

G = "/Users/mac/Documents/GitHub/SanskritGrammar"
BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
OUT = os.path.join(BASE, "infographics", "case-roads-2026-08-29")

SLOTS = ["имен.", "род.", "дат.", "вин.", "твор.", "отл.", "местн.", "зват."]

# slot -> per-language detectors
DETECTORS = {
    "en": {0: r"nominative", 1: r"genitive", 2: r"dative", 3: r"accusative",
           4: r"instrumental", 5: r"ablative", 6: r"locative", 7: r"vocative"},
    "de": {0: r"\bNom\.", 1: r"\bGen\.", 2: r"\bDat\.", 3: r"\bAkk\.",
           4: r"\bInstr\.", 5: r"\bAbl\.", 6: r"\bLok\.", 7: r"\bVok\."},
    "ru": {0: r"именительный", 1: r"родительный", 2: r"дательный", 3: r"винительный",
           4: r"творительный", 5: r"отложительный", 6: r"местный", 7: r"звательный"},
}
BOOKS = [
    ("Уитни · 1889 · EN", "en", "WhitneyGrammar_1889", "WhitneyGrammar_1889/*.mdx"),
    ("Апте · 1885 · EN", "en", "ApteSyntax_1885", "ApteSyntax_1885/src/01_Apte/*.mdx"),
    ("Бюлер · 1923 · DE", "de", "BuhlerLeitfaden_1923", "BuhlerLeitfaden_1923/Buhler_Unicode.mdx"),
    ("Кочергина · 1998 · RU", "ru", "KocherginaUchebnik_1998", "KocherginaUchebnik_1998/Kochergina_unicode.mdx"),
    ("Кнауэр · 1908 · RU", "ru", "KnauerFrazy_1908", "KnauerFrazy_1908/Frazy-Knauer-03.05.2023.mdx"),
]
COLORS = {"en": "#3E7CC1", "de": "#E4573D", "ru": "#57A15A"}


def main():
    data = []
    total = 0
    for label, lang, repo, pattern in BOOKS:
        counts = [0] * 8
        for p in sorted(glob.glob(os.path.join(G, pattern))):
            t = open(p, encoding="utf-8", errors="ignore").read()
            for slot, pat in DETECTORS[lang].items():
                counts[slot] += len(re.findall(pat, t, re.IGNORECASE if lang in ("en", "ru") else 0))
        total += sum(counts)
        data.append({"book": label, "lang": lang, "counts": counts})
    os.makedirs(OUT, exist_ok=True)
    json.dump({"slots": SLOTS, "books": data, "total_mentions": total},
              open(os.path.join(OUT, "data.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)

    import math
    X0, PITCH = 470, 160
    Y0, ROW = 372, 128
    R = lambda c: max(3.5, math.sqrt(c) * 2.3)
    parts = []

    # case column headers
    for i, s in enumerate(SLOTS):
        parts.append('<text class="col" x="%d" y="%d" transform="rotate(-4 %d %d)">%s</text>'
                     % (X0 + i * PITCH, Y0 - 74, X0 + i * PITCH, Y0 - 74, s))
    # rows
    for k, d in enumerate(data):
        y = Y0 + k * ROW
        # wobble road
        pts = " ".join("%.1f,%.1f" % (X0 + i * PITCH, y + (6 if i % 2 else -5)) for i in range(8))
        parts.append('<polyline class="road" points="%s"/>' % pts)
        # washi-tape book label
        parts.append('<g transform="translate(74 %d) rotate(-1.5)">' % (y - 30))
        parts.append('<rect width="300" height="46" fill="#F4EFDF" opacity=".92" stroke="#2E2A25" stroke-width="2.5" filter="url(#wobble)"/>')
        parts.append('<text class="booklab" x="16" y="30">%s</text></g>' % d["book"])
        for i, c in enumerate(d["counts"]):
            cx, cy = X0 + i * PITCH, y + (6 if i % 2 else -5)
            col = COLORS[d["lang"]]
            if c:
                parts.append('<circle cx="%d" cy="%d" r="%.1f" fill="%s" opacity=".85" filter="url(#wobble)"/>' % (cx, cy, R(c), col))
                parts.append('<text class="val" x="%d" y="%.1f">%d</text>' % (cx, cy - R(c) - 8, c))
            else:
                parts.append('<circle cx="%d" cy="%d" r="3" fill="none" stroke="#7A7365" stroke-width="2"/>' % (cx, cy))
    # circled hero total
    parts.append('<ellipse cx="1652" cy="140" rx="150" ry="86" fill="none" stroke="#E4573D" stroke-width="5" filter="url(#wobble)" transform="rotate(-3 1652 140)"/>')
    svg = "\n      ".join(parts)

    html = TEMPLATE.format(svg=svg, total=total, apte=data[1]["counts"][1], wht=sum(data[0]["counts"]))
    open(os.path.join(OUT, "index.html"), "w", encoding="utf-8").write(html)
    print("total", total, [d["counts"] for d in data])


TEMPLATE = """<!doctype html>
<html lang="ru">
<head>
<meta charset="utf-8">
<title>Падежные дорожки: пять грамматик</title>
<!-- Composition: Specimen sheet of five hand-drawn roads (one per grammar), each with eight
     case stations; circle area ~ mentions (r = sqrt(c) * 2.3). Hand-drawn, wide 1920x1080. -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Shantell+Sans:ital,wght@0,500;0,700;0,800;1,500&family=Caveat:wght@600;700&display=swap" rel="stylesheet">
<style>
*, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
:root {{
  --bg:#FDFBF4; --surface:#F4EFDF; --surface-2:#E9E2CC;
  --ink:#2E2A25; --ink-muted:#7A7365;
  --chart-1:#E4573D; --chart-2:#3E7CC1; --chart-3:#57A15A; --chart-4:#9268B8;
  --font-body:'Shantell Sans',cursive; --font-aside:'Caveat',cursive;
}}
html, body {{ background: var(--bg); }}
body {{ width: 1920px; font-family: var(--font-body); font-weight: 500; color: var(--ink); }}
.canvas {{ position: relative; width: 1920px; height: 1080px; overflow: hidden; background: var(--bg); }}
.title-block {{ position: absolute; left: 64px; top: 40px; width: 900px; }}
.kicker {{ font: 700 15px/1.3 var(--font-body); text-transform: uppercase; letter-spacing: .05em; color: var(--ink-muted); }}
h1 {{ font-weight: 800; font-size: 62px; line-height: 1.02; margin-top: 12px; }}
h1 .u {{ text-decoration: underline; text-decoration-color: var(--chart-1); text-decoration-thickness: 6px; text-underline-offset: 8px; }}
.standfirst {{ margin-top: 14px; font: 500 16.5px/1.5 var(--font-body); color: var(--ink-muted); width: 820px; }}
.hero {{ position: absolute; left: 1492px; top: 78px; width: 320px; text-align: center; z-index: 2; }}
.hero-num {{ font-weight: 800; font-size: 116px; line-height: 1.35; }}
.hero-cap {{ font: 500 15px/1.35 var(--font-body); margin-top: -8px; }}
svg.roads {{ position: absolute; left: 0; top: 0; }}
.col {{ font: 700 20px var(--font-body); fill: var(--ink); text-anchor: middle; }}
.road {{ fill: none; stroke: var(--ink); stroke-width: 3; opacity: .55; }}
.booklab {{ font: 700 17px var(--font-body); fill: var(--ink); }}
.val {{ font: 700 13.5px var(--font-body); fill: var(--ink); text-anchor: middle; }}
.aside {{ position: absolute; left: 1210px; top: 795px; width: 380px; font: 600 27px/1.25 var(--font-aside); color: var(--ink); transform: rotate(-2deg); }}
.aside .arr {{ color: var(--chart-1); }}
.legend {{ position: absolute; left: 64px; bottom: 118px; display: flex; gap: 26px; font: 700 15px var(--font-body); align-items: center; }}
.dot {{ display: inline-block; width: 15px; height: 15px; border-radius: 50%; margin-right: 7px; vertical-align: -2px; }}
footer {{ position: absolute; left: 64px; right: 64px; bottom: 26px;
  display: flex; justify-content: space-between; gap: 40px;
  border-top: 2.5px solid var(--ink); padding-top: 12px; font: 500 13.5px/1.5 var(--font-body); color: var(--ink-muted); }}
footer b {{ font-weight: 700; color: var(--ink); }}
</style>
</head>
<body>
<div class="canvas">
  <svg width="0" height="0" style="position:absolute"><filter id="wobble"><feTurbulence type="fractalNoise" baseFrequency="0.035" numOctaves="3" result="n"/><feDisplacementMap in="SourceGraphic" in2="n" scale="4"/></filter></svg>
  <div class="title-block">
    <div class="kicker">САНСКРИТСКИЙ АРХИВ ГАСУНСА · SANSKRITGRAMMAR · ПОСЧИТАНО 29.08.2026</div>
    <h1>Падежные <span class="u">дорожки</span> пяти грамматик</h1>
    <p class="standfirst">Восемь падежей — восемь станций на каждой дорожке. Кружок — сколько раз грамматика называет падеж в своём тексте: Уитни и Апте проговаривают каждое падежное правило, Кнауэр учит фразами, не называя ни одного.</p>
  </div>
  <div class="hero" data-hero>
    <div class="hero-num">{total}</div>
    <div class="hero-cap">упоминаний падежей в пяти книгах</div>
  </div>
  <svg class="roads" width="1920" height="1080" viewBox="0 0 1920 1080">
      {svg}
  </svg>
  <div class="aside"><span class="arr">←</span> Кнауэр-фразы: ни одного названия падежа — дорожка без станций!</div>
  <div class="legend">
    <span><span class="dot" style="background:var(--chart-2)"></span>английские</span>
    <span><span class="dot" style="background:var(--chart-1)"></span>немецкая</span>
    <span><span class="dot" style="background:var(--chart-3)"></span>русские</span>
    <span style="font-weight:500;color:var(--ink-muted)">кружок = площадь ∝ числу упоминаний</span>
  </div>
  <footer>
    <div>Данные: <b>SanskritGrammar</b> — mdx-тексты Уитни 1889, Апте 1885 (синтаксис), Бюлера 1923, Кочергиной 1998, Кнауэра 1908; счёт по полным названиям и стандартным сокращениям падежей</div>
    <div>скрипт: <b>scripts/infographics50/case_roads.py</b> · Посчитано 29.08.2026 · <b>Dr. Mārcis Gasūns</b></div>
  </footer>
</div>
</body>
</html>
"""

if __name__ == "__main__":
    main()
