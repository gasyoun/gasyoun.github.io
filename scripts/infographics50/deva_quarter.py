#!/usr/bin/env python3
"""Devanagari quarter #39 — 46 letters as an isometric city block.

Derives infographics/devanagari-quarter-2026-08-29/{data.json,index.html}.
Source: first character of <k1> across ALL 45 csl-orig v02 dictionary texts.
Heights are linear: px = count / max * 260, floor 2px (isometric-world, truthful).
"""
import collections
import json
import os

V02 = "/Users/mac/Documents/GitHub/csl-orig/v02"
BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
OUT = os.path.join(BASE, "infographics", "devanagari-quarter-2026-08-29")

DEVA = {"a": "अ", "A": "आ", "i": "इ", "I": "ई", "u": "उ", "U": "ऊ", "f": "ऋ", "F": "ॠ",
        "x": "ऌ", "e": "ए", "E": "ऐ", "o": "ओ", "O": "औ",
        "k": "क", "K": "ख", "g": "ग", "G": "घ", "N": "ङ", "c": "च", "C": "छ", "j": "ज",
        "J": "झ", "Y": "ञ", "w": "ट", "W": "ठ", "q": "ड", "Q": "ढ", "R": "ण",
        "t": "त", "T": "थ", "d": "द", "D": "ध", "n": "न", "p": "प", "P": "फ", "b": "ब",
        "B": "भ", "m": "म", "y": "य", "r": "र", "l": "ल", "v": "व", "S": "श", "z": "ष",
        "s": "स", "h": "ह"}
ORDER = list(DEVA)
VOWELS = set("aAiIuUfFxeEoO")
TRIADS = {"v": ("#4DB49D", "#009B7D", "#007259"), "c": ("#CC9440", "#B57300", "#8A5700"),
          "hero": ("#E58272", "#D9503F", "#A93A2D")}


def fmt(v):
    return "{:,}".format(v).replace(",", " ")


def P(x, y, z):
    return (330 + (x - y) * 0.866, 452 + (x + y) * 0.5 - z)


def poly(pts, fill, stroke="#22333B", w="1.2"):
    s = " ".join("%.1f,%.1f" % p for p in pts)
    return '<polygon points="%s" fill="%s" stroke="%s" stroke-width="%s"/>' % (s, fill, stroke, w)


def main():
    cnt = collections.Counter()
    total = 0
    unmapped = collections.Counter()
    for d in sorted(os.listdir(V02)):
        p = os.path.join(V02, d, d + ".txt")
        if not os.path.isfile(p):
            continue
        with open(p, encoding="utf-8", errors="ignore") as f:
            for line in f:
                i = line.find("<k1>")
                if i < 0:
                    continue
                ch = line[i + 4]
                if ch in DEVA:
                    cnt[ch] += 1
                else:
                    unmapped[ch] += 1
                total += 1
    assert total == 1503517 and len(cnt) == 46, (total, len(cnt), dict(unmapped))
    mx = max(cnt.values())
    os.makedirs(OUT, exist_ok=True)
    json.dump({"total": total, "letters": {c: cnt[c] for c in ORDER}, "max_letter": "a", "max": mx},
              open(os.path.join(OUT, "data.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)

    W = D = 42
    STEP = 44
    H = lambda c: max(2.0, 260.0 * cnt[c] / mx)
    parts = []
    placed = []
    # slab (drawn first, back row y=110 behind, front row y=0)
    rows = [(80 + i * STEP, 80) for i in range(23)] + [(i * STEP, 0) for i in range(23)]
    sx0, sx1 = -30, 22 * STEP + 50
    slab = [P(sx0, -30, 0), P(sx1, -30, 0), P(sx1, 124, 0), P(sx0, 124, 0)]
    parts.append('<polygon points="%s" fill="#CFD8DB"/>' % " ".join("%.1f,%.1f" % p for p in slab))
    parts.append('<polygon points="%s" fill="#B8C2C6"/>' % " ".join("%.1f,%.1f" % (px, py + 22) for px, py in slab))
    for x, y in sorted(rows, key=lambda t: -t[1]):
        ch = ORDER[len(placed)]
        placed.append(ch)
        h = H(ch)
        kind = "hero" if ch == "a" else ("v" if ch in VOWELS else "c")
        top, side, dark = TRIADS[kind]
        top4 = [P(x, y, h), P(x + W, y, h), P(x + W, y + D, h), P(x, y + D, h)]
        right = [P(x + W, y, h), P(x + W, y + D, h), P(x + W, y + D, 0), P(x + W, y, 0)]
        left = [P(x, y + D, h), P(x + W, y + D, h), P(x + W, y + D, 0), P(x, y + D, 0)]
        parts.append(poly(right, side))
        parts.append(poly(left, dark))
        parts.append(poly(top4, top))
        gx, gy = P(x + W / 2, y + D / 2, h)
        lx, ly = P(x + W / 2, y + D + 24, 0)
        parts.append('<text class="deva" x="%.1f" y="%.1f">%s</text>' % (lx, ly + 8, DEVA[ch]))
        if cnt[ch] >= 60000:
            parts.append('<text class="bigval" x="%.1f" y="%.1f">%s</text>' % (gx, gy - 14, fmt(cnt[ch])))
    svg = "\n      ".join(parts)
    top3 = sorted(cnt.items(), key=lambda kv: -kv[1])[:4]

    html = TEMPLATE.format(svg=svg, total=fmt(total), mx=fmt(mx),
                           t1=DEVA[top3[0][0]], t1n=fmt(top3[0][1]),
                           t2=DEVA[top3[1][0]], t2n=fmt(top3[1][1]),
                           t3=DEVA[top3[2][0]], t3n=fmt(top3[2][1]),
                           t4=DEVA[top3[3][0]], t4n=fmt(top3[3][1]))
    open(os.path.join(OUT, "index.html"), "w", encoding="utf-8").write(html)
    print("total", total, "| top", top3[:3])


TEMPLATE = """<!doctype html>
<html lang="ru">
<head>
<meta charset="utf-8">
<title>Квартал деванагари: 46 букв</title>
<!-- Composition: Big Object — one isometric slab of 46 letter-buildings (2 streets of 23),
     height linear 260px = max. Isometric world, wide 1920x1080. Two triads: vowels teal,
     consonants amber; hero letter a coral. True-iso: X = X0 + (x-y)*0.866, Y = Y0 + (x+y)*0.5 - z. -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fredoka:wght@500;600;700&family=Nunito+Sans:ital,opsz,wght@0,6..12,400;0,6..12,600;0,6..12,800;1,6..12,400&display=swap" rel="stylesheet">
<style>
*, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
:root {{
  --bg:#E8EDEF; --ground:#CFD8DB; --ground-2:#B8C2C6;
  --ink:#22333B; --ink-muted:#5D6E75; --de-emphasis:#AEB9BD;
  --chart-1:#D9503F; --chart-2:#009B7D; --chart-4:#B57300;
  --font-display:'Fredoka',sans-serif; --font-body:'Nunito Sans',sans-serif;
}}
html, body {{ background: var(--bg); }}
body {{ width: 1920px; font-family: var(--font-body); color: var(--ink); }}
.canvas {{ position: relative; width: 1920px; height: 1080px; overflow: hidden;
  background: radial-gradient(ellipse 1600px 800px at 40% 80%, #F2F6F7 0%, var(--bg) 70%); }}
.title-block {{ position: absolute; left: var(--space-5, 64px); top: var(--space-4, 40px); width: 760px; z-index: 3; }}
.kicker {{ font: 800 14px/1.3 var(--font-body); text-transform: uppercase; letter-spacing: .06em; color: var(--ink-muted); }}
h1 {{ font-family: var(--font-display); font-weight: 700; font-size: 58px; line-height: 1.02; margin-top: 12px; }}
.standfirst {{ margin-top: 12px; font: 400 17px/1.5 var(--font-body); color: var(--ink-muted); width: 720px; }}
svg.city {{ position: absolute; left: 0; top: 0; }}
.deva {{ font: 400 26px 'Devanagari Sangam MN','Noto Sans Devanagari',sans-serif; fill: var(--ink); text-anchor: middle; }}
.bigval {{ font: 800 15px var(--font-body); fill: var(--ink); text-anchor: middle; }}
.hero-block {{ position: absolute; right: var(--space-5, 64px); top: 60px; width: 420px; text-align: left; z-index: 3;
  border-top: 3px solid var(--ink); padding-top: 18px; }}
.hero-num {{ font-family: var(--font-display); font-weight: 700; font-size: 96px; line-height: 1; }}
.hero-label {{ font: 600 19px/1.4 var(--font-body); margin-top: 6px; }}
.tops {{ margin-top: 22px; }}
.tops .row {{ display: flex; align-items: baseline; gap: 12px; margin-bottom: 12px; font: 400 17px var(--font-body); }}
.tops .deva2 {{ font-family: 'Devanagari Sangam MN','Noto Sans Devanagari',sans-serif; font-size: 30px; width: 46px; }}
.tops .n {{ font-weight: 800; }}
.tops .bar {{ height: 10px; background: var(--chart-2); width: 170px; }}
.legend {{ position: absolute; left: var(--space-5, 64px); bottom: 120px; display: flex; gap: 24px; align-items: center;
  font: 600 15px var(--font-body); z-index: 3; }}
.dot {{ display: inline-block; width: 15px; height: 15px; margin-right: 7px; vertical-align: -2px; border: 1.5px solid var(--ink); }}
footer {{ position: absolute; left: var(--space-5, 64px); right: var(--space-5, 64px); bottom: var(--space-3, 24px);
  display: flex; justify-content: space-between; gap: 40px; z-index: 3;
  border-top: 1.5px solid var(--ink); padding-top: 12px; font: 400 14px/1.5 var(--font-body); color: var(--ink-muted); }}
footer b {{ font-weight: 700; color: var(--ink); }}
</style>
</head>
<body>
<div class="canvas">
  <div class="title-block">
    <div class="kicker">САНСКРИТСКИЙ АРХИВ ГАСУНСА · CSL-ORIG · ПОСЧИТАНО 29.08.2026</div>
    <h1>Квартал деванагари</h1>
    <p class="standfirst">46 букв словарного алфавита как здания квартала: высота каждого дома — сколько статей всех 45 словарей Кёльна начинаются на эту букву. Передний ряд — согласные варги, задний продолжает алфавитный порядок.</p>
  </div>
  <div class="hero-block" data-hero>
    <div class="hero-num">{total}</div>
    <div class="hero-label">статей в 45 словарях — 46 домов квартала</div>
    <div class="tops">
      <div class="row"><span class="deva2">{t1}</span><span class="bar" style="width:170px;background:var(--chart-1)"></span><span class="n">{t1n}</span></div>
      <div class="row"><span class="deva2">{t2}</span><span class="bar" style="width:149px"></span><span class="n">{t2n}</span></div>
      <div class="row"><span class="deva2">{t3}</span><span class="bar" style="width:146px"></span><span class="n">{t3n}</span></div>
      <div class="row"><span class="deva2">{t4}</span><span class="bar" style="width:113px"></span><span class="n">{t4n}</span></div>
    </div>
  </div>
  <svg class="city" width="1920" height="1080" viewBox="0 0 1920 1080">
      {svg}
  </svg>
  <div class="legend">
    <span><span class="dot" style="background:#4DB49D"></span>гласные</span>
    <span><span class="dot" style="background:#CC9440"></span>согласные</span>
    <span><span class="dot" style="background:#E58272"></span>рекордсмен a</span>
  </div>
  <footer>
    <div>Данные: <b>csl-orig/v02</b> — первые буквы ключей &lt;k1&gt; всех 45 словарей, {total} статей; высота 260px = {mx} статей</div>
    <div>скрипт: <b>scripts/infographics50/deva_quarter.py</b> · Посчитано 29.08.2026 · <b>Dr. Mārcis Gasūns</b></div>
  </footer>
</div>
</body>
</html>
"""

if __name__ == "__main__":
    main()
