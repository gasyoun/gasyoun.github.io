#!/usr/bin/env python3
"""Gita coverage curve #40 — how many words unlock the Bhagavad-Gita (blueprint).

Derives infographics/gita-coverage-2026-08-29/{data.json,index.html}.
Source: kosha/data/gita/gita_gold_master.tsv — lemma column (9 092 word rows).
Curve: rank lemmas by frequency, cumulative share of tokens.
"""
import csv
import json
import os
from collections import Counter

SRC = "/Users/mac/Documents/GitHub/kosha/data/gita/gita_gold_master.tsv"
BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
OUT = os.path.join(BASE, "infographics", "gita-coverage-2026-08-29")

X0, X1, Y0, Y1 = 190, 1490, 170, 800


def px(rank, total_lemmas):
    return X0 + (X1 - X0) * rank / total_lemmas


def py(cov):
    return Y1 - (Y1 - Y0) * cov / 100.0


def main():
    freq = Counter()
    for r in csv.DictReader(open(SRC, encoding="utf-8"), delimiter="\t"):
        freq[r["lemma"]] += 1
    total = sum(freq.values())
    n_lemmas = len(freq)
    ranked = sorted(freq.items(), key=lambda kv: -kv[1])
    c = 0
    n50 = n80 = None
    cov100 = None
    pts = []
    for i, (_, n) in enumerate(ranked, 1):
        c += n
        cov = 100.0 * c / total
        if n50 is None and cov >= 50:
            n50 = i
        if n80 is None and cov >= 80:
            n80 = i
        if i == 100:
            cov100 = cov
        if i % 10 == 0 or i in (1, 100, n50, n80, n_lemmas):
            pts.append((i, cov))
    assert n_lemmas == 2748 and total == 9092, (n_lemmas, total)

    os.makedirs(OUT, exist_ok=True)
    json.dump({"tokens": total, "lemmas": n_lemmas, "cov_at_100": cov100,
               "n_at_50pct": n50, "n_at_80pct": n80},
              open(os.path.join(OUT, "data.json"), "w", encoding="utf-8"), indent=1)

    curve = " ".join("%.1f,%.1f" % (px(r, n_lemmas), py(cv)) for r, cv in pts)
    curve += " %.1f,%.1f %.1f,%.1f" % (px(n_lemmas, n_lemmas), Y1, X0, Y1)

    def dim(x_rank, cov, label):
        x = px(x_rank, n_lemmas)
        y = py(cov)
        return ('<line x1="%.0f" y1="%.0f" x2="%.0f" y2="%d" stroke="var(--line)" stroke-width="1" marker-start="url(#ar)" marker-end="url(#ar)"/>'
                '<rect x="%.0f" y="%.0f" width="150" height="22" fill="var(--bg)"/>'
                '<text class="dimlab" x="%.0f" y="%.0f">%s</text>'
                % (x, Y1 + 16, x, y - 8, x - 75, y - 32, x - 75, y - 16, label))

    svg = "\n      ".join([
        # axes
        '<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="var(--line)" stroke-width="2"/>' % (X0, Y1, X1, Y1),
        '<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="var(--line)" stroke-width="2"/>' % (X0, Y1, X0, Y0 - 30),
        '<text class="axlab" x="%d" y="%d">0 %%</text>' % (X0 - 66, Y1 + 4),
        '<text class="axlab" x="%d" y="%d">50 %%</text>' % (X0 - 66, (Y0 + Y1) // 2 + 4),
        '<text class="axlab" x="%d" y="%d">100 %%</text>' % (X0 - 74, Y0 + 4),
        '<text class="axlab" x="%d" y="%d">%s</text>' % (X1 - 120, Y1 + 30, "2 748 лемм"),
        '<text class="axlab" x="%d" y="%d">0</text>' % (X0 - 8, Y1 + 30),
        # hatched area under curve
        '<polygon points="%s" fill="var(--hatch-1)" opacity=".5" stroke="none"/>' % curve,
        # the curve
        '<polyline points="%s" fill="none" stroke="var(--chart-1)" stroke-width="3"/>' % " ".join(p for p in curve.split(" ")[:len(pts)]),
        # milestone dimension lines
        dim(n50, 50.0, "50 %% · %d слов" % n50),
        dim(n80, 80.0, "80 %% · %d слов" % n80),
        # dot markers on curve at milestones
        '<circle cx="%.0f" cy="%.0f" r="6" fill="var(--chart-1)"/>' % (px(100, n_lemmas), py(cov100)),
        '<circle cx="%.0f" cy="%.0f" r="6" fill="var(--chart-1)"/>' % (px(n50, n_lemmas), py(50)),
        '<circle cx="%.0f" cy="%.0f" r="6" fill="var(--chart-1)"/>' % (px(n80, n_lemmas), py(80)),
        # registration crosses
        '<path class="reg" d="M 40 40 h 20 M 50 30 v 20"/>',
        '<path class="reg" d="M 1860 40 h 20 M 1870 30 v 20"/>',
        '<path class="reg" d="M 40 1020 h 20 M 50 1010 v 20"/>',
    ])

    html = TEMPLATE.format(svg=svg, n50=n50, n80=n80, cov100=("%.1f" % cov100).replace(".", ","),
                           lemmas="{:,}".format(n_lemmas).replace(",", " "),
                           tokens="{:,}".format(total).replace(",", " "))
    open(os.path.join(OUT, "index.html"), "w", encoding="utf-8").write(html)
    print("lemmas", n_lemmas, "tokens", total, "cov@100", cov100, "n50", n50, "n80", n80)


TEMPLATE = """<!doctype html>
<html lang="ru">
<head>
<meta charset="utf-8">
<title>Сколько слов нужно для Гиты</title>
<!-- Composition: Big Object — the coverage curve as an engineering plot with dimension lines,
     title block bottom-right. Blueprint, wide 1920x1080. Curve from lemmas of gita_gold_master.tsv. -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Saira+Condensed:wght@600;700&family=IBM+Plex+Mono:ital,wght@0,400;0,500;0,600;1,400&display=swap" rel="stylesheet">
<style>
*, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
:root {{
  --bg:#123A66; --bg-2:#0D3054;
  --line:#D8E8F8; --line-soft:rgb(216 232 248 / 0.45);
  --ink:#EAF2FB; --ink-muted:#9FB8D4;
  --chart-1:#3E9BD6; --chart-2:#B8860B;
  --hatch-1:repeating-linear-gradient(45deg, #3E9BD6 0 1.5px, transparent 1.5px 7px);
  --font-display:'Saira Condensed',sans-serif; --font-body:'IBM Plex Mono',monospace;
}}
html, body {{ background: var(--bg); }}
body {{ width: 1920px; font-family: var(--font-body); color: var(--ink); }}
.canvas {{ position: relative; width: 1920px; height: 1080px; overflow: hidden;
  background-image:
    linear-gradient(var(--line-soft) 1px, transparent 1px),
    linear-gradient(90deg, var(--line-soft) 1px, transparent 1px);
  background-size: 40px 40px; }}
.frame {{ position: absolute; inset: 12px; border: 2px solid var(--line); pointer-events: none; }}
.frame::after {{ content: ''; position: absolute; inset: 4px; border: 1px solid var(--line-soft); }}
.title-block {{ position: absolute; left: 56px; top: 44px; }}
.kicker {{ font: 500 14px/1.4 var(--font-body); letter-spacing: .08em; text-transform: uppercase; color: var(--ink-muted); }}
h1 {{ font-family: var(--font-display); font-weight: 700; font-size: 64px; text-transform: uppercase;
  letter-spacing: .04em; line-height: .95; margin-top: 10px; }}
.standfirst {{ margin-top: 12px; font: italic 400 15px/1.5 var(--font-body); color: var(--ink-muted); width: 620px; }}
.hero {{ position: absolute; left: 1556px; top: 60px; width: 330px; border-left: 2px solid var(--line); padding-left: 24px; }}
.hero-num {{ font-family: var(--font-display); font-weight: 700; font-size: 120px; line-height: 1; }}
.hero-cap {{ font: 500 15px/1.45 var(--font-body); margin-top: 6px; }}
.hero-sub {{ margin-top: 16px; font: 400 13.5px/1.55 var(--font-body); color: var(--ink-muted); }}
svg.plot {{ position: absolute; left: 0; top: 0; }}
.dimlab {{ font: 500 13px var(--font-body); fill: var(--ink); text-anchor: middle; }}
.axlab {{ font: 400 13px var(--font-body); fill: var(--ink-muted); }}
.reg {{ stroke: var(--line-soft); stroke-width: 1; fill: none; }}
.tblock {{ position: absolute; right: 56px; bottom: 44px; width: 430px; border: 2px solid var(--line);
  outline: 1px solid var(--line-soft); outline-offset: 3px; background: var(--bg-2); }}
.tblock .tr {{ display: flex; border-top: 1px solid var(--line-soft); }}
.tblock .tr:first-child {{ border-top: none; }}
.tblock .th {{ width: 130px; padding: 7px 10px; font: 600 12px/1.3 var(--font-body); letter-spacing: .08em;
  color: var(--ink-muted); border-right: 1px solid var(--line-soft); }}
.tblock .td {{ padding: 7px 12px; font: 400 12.5px/1.3 var(--font-body); }}
footer {{ position: absolute; left: 56px; bottom: 44px; font: 400 12.5px/1.6 var(--font-body); color: var(--ink-muted); }}
footer b {{ color: var(--ink); font-weight: 600; }}
</style>
</head>
<body>
<div class="canvas">
  <div class="frame"></div>
  <div class="title-block">
    <div class="kicker">САНСКРИТСКИЙ АРХИВ ГАСУНСА · KOSHA · ЛИСТ № 40 · ПОСЧИТАНО 29.08.2026</div>
    <h1>Сколько слов нужно для Гиты</h1>
    <p class="standfirst">Кривая покрытия: слова Гиты, упорядоченные по частоте, против доли текста. Первая сотня закрывает половину — дальше кривая выходит на плато: хвост из двух тысяч редких лемм.</p>
  </div>
  <div class="hero" data-hero>
    <div class="hero-num">{n50}</div>
    <div class="hero-cap">слова покрывают половину Гиты</div>
    <div class="hero-sub">{tokens} словоупотреблений · {lemmas} лемм · сотая лемма закрывает {cov100} %</div>
  </div>
  <svg class="plot" width="1920" height="1080" viewBox="0 0 1920 1080">
    <defs>
      <marker id="ar" markerWidth="8" markerHeight="8" refX="4" refY="4" orient="auto">
        <path d="M1,1 L7,4 L1,7 z" fill="var(--line)"/>
      </marker>
    </defs>
      {svg}
  </svg>
  <div class="tblock">
    <div class="tr"><div class="th">TITLE</div><div class="td">Кривая покрытия Бхагавадгиты</div></div>
    <div class="tr"><div class="th">DWG No.</div><div class="td">40 / 50 · санскритские инфографики</div></div>
    <div class="tr"><div class="th">SCALE</div><div class="td">x: 0–2 748 лемм · y: 0–100 %</div></div>
    <div class="tr"><div class="th">DATE</div><div class="td">29.08.2026 · Dr. Mārcis Gasūns</div></div>
    <div class="tr"><div class="th">SOURCE</div><div class="td">kosha · gita_gold_master.tsv (леммы)</div></div>
  </div>
  <footer>
    Данные: <b>kosha · data/gita/gita_gold_master.tsv</b> — словарной разбор Гиты, счёт по столбцу lemma (форма учитывается через лемму).
  </footer>
</div>
</body>
</html>
"""

if __name__ == "__main__":
    main()
