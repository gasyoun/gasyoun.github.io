#!/usr/bin/env python3
"""Sandhi records #20 — junction-rule frequencies of the Bhagavad-Gita (naturalist plate).

Derives infographics/sandhi-records-2026-08-29/{data.json,index.html}.
Source: kosha/data/gita/gita_sandhi.tsv (161 rules, count/pct/category/examples).
"""
import csv
import json
import os

SRC = "/Users/mac/Documents/GitHub/kosha/data/gita/gita_sandhi.tsv"
BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
OUT = os.path.join(BASE, "infographics", "sandhi-records-2026-08-29")

CAT_RU = {
    "vowel coalescence": ("гласные", "#4E7A34"),
    "visarga": ("висарга", "#3A6FB0"),
    "anusvāra / nasal": ("носовые", "#8F2F28"),
    "consonant / other": ("прочее", "#9A7104"),
}


def fmt(v):
    return "{:,}".format(v).replace(",", " ")


def main():
    rows = list(csv.DictReader(open(SRC, encoding="utf-8"), delimiter="\t"))
    for r in rows:
        r["count"] = int(r["count"])
    total = sum(r["count"] for r in rows)
    cats = {}
    for r in rows:
        n, _ = cats.get(r["category"], (0, 0))
        cats[r["category"]] = (n + r["count"], CAT_RU[r["category"]][1])
    top = sorted(rows, key=lambda r: -r["count"])[:8]
    assert total == 3412 and len(rows) == 161, (total, len(rows))
    os.makedirs(OUT, exist_ok=True)
    json.dump({"junctions": total, "rules": len(rows),
               "by_category": {k: v[0] for k, v in cats.items()},
               "top": [{k: r[k] for k in ("rule", "category", "count", "pct", "examples")} for r in top]},
              open(os.path.join(OUT, "data.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)

    # ranked bars (Fig. 1..8)
    mx = top[0]["count"]
    BW = 620
    figs = []
    y0, pitch = 268, 92
    for i, r in enumerate(top):
        y = y0 + i * pitch
        w = BW * r["count"] / mx
        col = CAT_RU[r["category"]][1]
        figs.append('<text class="figtag" x="%d" y="%d">Fig. %d.</text>' % (700, y + 18, i + 1))
        figs.append('<text class="rule" x="790" y="%d">%s</text>' % (y + 18, r["rule"]))
        figs.append('<rect x="790" y="%d" width="%.0f" height="16" fill="%s55" stroke="#3A3226" stroke-width="1"/>' % (y + 30, w, col))
        figs.append('<rect x="790" y="%d" width="%.0f" height="16" fill="%s" opacity="0.28"/>' % (y + 30, w, col))
        figs.append('<text class="figval" x="%.0f" y="%d">%s стыков · %s%%</text>' % (800 + w, y + 43, fmt(r["count"]), r["pct"]))
    # apothecary divided bar for categories
    seg = []
    bx, bw, by = 128, 460, 736
    x = bx
    for k, (n, col) in sorted(cats.items(), key=lambda kv: -kv[1][0]):
        w = bw * n / total
        seg.append('<rect x="%.0f" y="%d" width="%.1f" height="26" fill="%s" opacity=".45" stroke="#3A3226" stroke-width="1"/>' % (x, by, w, col))
        seg.append('<text class="segval" x="%.1f" y="%d">%s%%</text>' % (x + w / 2, by + 18, ("%.1f" % (100.0 * n / total)).replace(".", ",")))
        row = 44 if (len(seg) // 3) % 2 == 1 else 70
        seg.append('<text class="seglab" x="%.1f" y="%d">%s</text>' % (x + w / 2, by + row, CAT_RU[k][0]))
        x += w
    svg = "\n      ".join(figs + seg)

    html = TEMPLATE.format(svg=svg, total=fmt(total), rules=len(rows),
                           top_rule=top[0]["rule"], top_n=fmt(top[0]["count"]))
    open(os.path.join(OUT, "index.html"), "w", encoding="utf-8").write(html)
    print("junctions", total, "rules", len(rows), dict((k, v[0]) for k, v in cats.items()))


TEMPLATE = """<!doctype html>
<html lang="ru">
<head>
<meta charset="utf-8">
<title>Рекорды сандхи</title>
<!-- Composition: Specimen sheet — 8 ranked junction-rules pinned as Fig. 1–8, apothecary divided
     bar for the four families, hero numeral in the left column. Naturalist plate, wide 1920x1080. -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,500;0,600;0,700;1,500&family=EB+Garamond:ital,wght@0,400;0,500;0,600;1,400;1,500&display=swap" rel="stylesheet">
<style>
*, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
:root {{
  --bg:#F3ECDA; --surface:#EDE3CB; --surface-2:#E0D3B4;
  --ink:#3A3226; --ink-muted:#7C7060;
  --chart-1:#4E7A34; --chart-2:#3A6FB0; --chart-3:#8F2F28; --chart-4:#9A7104;
  --font-display:'Cormorant Garamond',serif; --font-body:'EB Garamond',serif;
}}
html, body {{ background: var(--bg); }}
body {{ width: 1920px; font-family: var(--font-body); color: var(--ink); }}
.canvas {{ position: relative; width: 1920px; height: 1080px; overflow: hidden; background: var(--bg); }}
.frame {{ position: absolute; inset: 28px; border: 2px solid var(--ink); pointer-events: none; }}
.frame::after {{ content: ''; position: absolute; inset: 6px; border: 1px solid var(--ink); }}
.platehead {{ position: absolute; left: 100px; right: 100px; top: 66px; text-align: center; }}
.plateno {{ font: 600 15px var(--font-body); font-variant: small-caps; letter-spacing: .3em; color: var(--ink-muted); }}
h1 {{ font-family: var(--font-display); font-weight: 600; font-size: 56px; letter-spacing: .12em;
  text-transform: uppercase; margin-top: 8px; }}
.latin {{ font-style: italic; font-size: 21px; color: var(--ink-muted); margin-top: 4px; }}
.lefcol {{ position: absolute; left: 128px; top: 280px; width: 470px; }}
.hero-num {{ font-family: var(--font-display); font-weight: 600; font-size: 182px; line-height: .95; }}
.hero-cap {{ font: 500 19px/1.5 var(--font-body); margin-top: 18px; }}
.scalebar {{ margin-top: 44px; }}
.scalebar .lab {{ font: 500 16px/1.4 var(--font-body); margin-top: 8px; }}
.divided {{ margin-top: 36px; }}
.divided h2 {{ font: 600 17px var(--font-body); font-variant: small-caps; letter-spacing: .08em; margin-bottom: 14px; }}
svg {{ display: block; }}
.figtag {{ font: 500 16px var(--font-body); font-variant: small-caps; letter-spacing: .06em; fill: var(--ink-muted); }}
.rule {{ font: 600 24px var(--font-body); fill: var(--ink); }}
.figval {{ font: 500 16px var(--font-body); fill: var(--ink-muted); }}
.segval {{ font: 600 16px var(--font-body); fill: var(--ink); text-anchor: middle; }}
.seglab {{ font: 500 14px var(--font-body); fill: var(--ink-muted); text-anchor: middle; }}
.caption-foot {{ position: absolute; left: 100px; right: 100px; bottom: 88px; border-top: 1px solid var(--ink-muted);
  padding-top: 10px; font: italic 400 14.5px/1.5 var(--font-body); color: var(--ink-muted); }}
footer {{ position: absolute; left: 100px; right: 100px; bottom: 46px;
  display: flex; justify-content: space-between; gap: 40px;
  font: 400 13.5px/1.4 var(--font-body); color: var(--ink-muted); }}
footer b {{ font-weight: 600; color: var(--ink); }}
</style>
</head>
<body>
<div class="canvas">
  <div class="frame"></div>
  <div class="platehead">
    <div class="plateno">Планша № 20 · Бхагавадгита · посчитано 29.08.2026</div>
    <h1>Рекорды сандхи</h1>
    <div class="latin">Coniunctionum in Gītā: {total} loci, {rules} regulae</div>
  </div>
  <div class="lefcol">
    <div class="hero-num" data-hero>{total}</div>
    <div class="hero-cap">стыков сандхи между словами Гиты; каждая описана одним из {rules} правил перехода</div>
    <div class="scalebar">
      <svg width="460" height="34">
        <line x1="2" y1="10" x2="458" y2="10" stroke="#3A3226" stroke-width="1.4"/>
        <line x1="2" y1="4" x2="2" y2="16" stroke="#3A3226" stroke-width="1.4"/>
        <line x1="458" y1="4" x2="458" y2="16" stroke="#3A3226" stroke-width="1.4"/>
      </svg>
      <div class="lab">Масштаб: самая частая стыковка «{top_rule}» встречается {top_n} раз — от неё отградуированы все линейки.</div>
    </div>
    <div class="divided">
      <h2>Четыре семейства правил</h2>
    </div>
  </div>
  <svg width="1920" height="1080" viewBox="0 0 1920 1080">
      {svg}
  </svg>
  <div class="caption-foot">Fig. 1–8 — восемь рекордных правил сандхи Гиты; толщина заливки — число стыков. Ниже — доля каждого семейства правил во всех {total} стыковках.</div>
  <footer>
    <div>Данные: <b>kosha · data/gita/gita_sandhi.tsv</b> — {rules} правил, {total} стыков</div>
    <div>скрипт: <b>scripts/infographics50/sandhi_records.py</b> · Посчитано 29.08.2026 · <b>Dr. Mārcis Gasūns</b></div>
  </footer>
</div>
</body>
</html>
"""

if __name__ == "__main__":
    main()
