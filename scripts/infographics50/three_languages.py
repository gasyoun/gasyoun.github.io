#!/usr/bin/env python3
"""Three languages #45 — which language do the 45 Cologne dictionaries speak?

Derives infographics/three-languages-2026-08-29/{data.json,index.html}.
Method: sample every 14th entry's gloss line in csl-orig/v02/<d>/<d>.txt;
classify by glyph/marker votes: Cyrillic -> RU, French accents -> FR,
German vs English function-word markers; dictionaries whose glosses carry no
European-language markers (Sanskrit-Sanskrit koshas, transliterated or
non-Latin glosses) -> bucket SA. RU=0 is a finding, not a gap.
"""
import json
import os
import re

V02 = "/Users/mac/Documents/GitHub/csl-orig/v02"
BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
OUT = os.path.join(BASE, "infographics", "three-languages-2026-08-29")

DE = re.compile(r"\b(der|die|das|und|oder|mit|sich|eines|unter|nach|vgl|etw)\b")
EN = re.compile(r"\b(the|and|of|with|who|which|having|cf|pron|esp|lit|viz)\b")
CYR = re.compile("[А-Яа-яЁё]")
FR = re.compile("[éèêàçùâîôû]")


def classify(path):
    n = cy = de = en = fr = 0
    take_next = False
    with open(path, encoding="utf-8", errors="ignore") as f:
        for i, line in enumerate(f):
            if i % 14 == 0:
                take_next = True
                continue
            if take_next:
                take_next = False
                if "<L>" in line or line.startswith("<"):
                    continue
                n += 1
                if CYR.search(line):
                    cy += 1
                if FR.search(line):
                    fr += 1
                if DE.search(line):
                    de += 1
                if EN.search(line):
                    en += 1
    if n < 30:
        return "SA", n
    if cy / n > 0.15:
        return "RU", n
    if fr / n > 0.10:
        return "FR", n
    if de / n > 0.15:
        return "DE", n
    if en / n > 0.15:
        return "EN", n
    return "SA", n


def main():
    dicts = sorted(d for d in os.listdir(V02)
                   if os.path.isfile(os.path.join(V02, d, d + ".txt")))
    rows = []
    for d in dicts:
        lang, n = classify(os.path.join(V02, d, d + ".txt"))
        rows.append({"dict": d, "lang": lang, "sampled": n})
    counts = {k: sum(1 for r in rows if r["lang"] == k) for k in ("EN", "DE", "FR", "RU", "SA")}
    assert len(rows) == 45 and counts["RU"] == 0, (len(rows), counts)
    os.makedirs(OUT, exist_ok=True)
    json.dump({"rows": rows, "counts": counts},
              open(os.path.join(OUT, "data.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)

    COL = {"EN": "#AD7A00", "DE": "#157F63", "FR": "#8E4468", "RU": "#C8501E", "SA": "#C9B593"}
    spines = []
    for i, r in enumerate(rows):
        shelf, pos = divmod(i, 15)
        x = 118 + pos * 46
        y = 560 - shelf * 128
        spines.append('<rect x="%d" y="%d" width="32" height="104" fill="%s" stroke="#33241A" stroke-width="1.6"/>' % (x, y, COL[r["lang"]]))
        spines.append('<text class="spine" x="%.1f" y="%d" transform="rotate(-90 %.1f %d)">%s</text>'
                      % (x + 22, y + 92, x + 22, y + 92, r["dict"]))
    for shelf in range(3):
        y = 666 - shelf * 128
        spines.append('<rect x="96" y="%d" width="700" height="8" fill="#33241A"/>' % y)
    svg = "\n      ".join(spines)

    legend = []
    for key, label, sub in [("EN", "английский", "%d словарь — от MW до Apte" % counts["EN"]),
                            ("DE", "немецкий", "%d словарей — PW, PWG, Грассман" % counts["DE"]),
                            ("FR", "французский", "%d словаря — Рену и Бурнуф" % counts["FR"]),
                            ("SA", "санскрит и прочее", "%d словарей без европейских глосс" % counts["SA"]),
                            ("RU", "русский", "0 — ниши нет и в каноне Кёльна")]:
        legend.append('<div class="lg"><span class="sw" style="background:%s"></span><span class="lgn">%s</span> — %s</div>'
                      % (COL[key], label, sub))
    html = TEMPLATE.format(svg=svg, legend="\n    ".join(legend),
                           en=counts["EN"], de=counts["DE"], fr=counts["FR"], sa=counts["SA"])
    open(os.path.join(OUT, "index.html"), "w", encoding="utf-8").write(html)
    print(counts)


TEMPLATE = """<!doctype html>
<html lang="ru">
<head>
<meta charset="utf-8">
<title>Три языка науки — и ноль по-русски</title>
<!-- Composition: Big Object — a shelf of 45 book spines, one per Cologne dictionary, colored by
     gloss language; hero «0 русских» at right. Retro-print, wide 1920x1080. -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Alfa+Slab+One&family=Karla:ital,wght@0,400;0,500;0,700;1,400&display=swap" rel="stylesheet">
<style>
*, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
:root {{
  --bg:#F5E9D4; --surface:#FBF3E2; --surface-2:#E7D6B6;
  --ink:#33241A; --ink-muted:#6E5B49;
  --chart-1:#C8501E; --chart-2:#157F63; --chart-3:#AD7A00; --chart-4:#8E4468;
  --de-emphasis:#C9B593;
  --font-display:'Alfa Slab One',serif; --font-body:'Karla',sans-serif;
}}
html, body {{ background: var(--bg); }}
body {{ width: 1920px; font-family: var(--font-body); color: var(--ink); }}
.canvas {{ position: relative; width: 1920px; height: 1080px; overflow: hidden;
  background: radial-gradient(ellipse 1400px 700px at 30% 25%, #FBF3E2 0%, var(--bg) 72%); }}
.grain {{ position: absolute; inset: 0; pointer-events: none; opacity: .36; }}
.title-block {{ position: absolute; left: 64px; top: 40px; width: 900px; z-index: 3; }}
.kicker {{ font: 700 15px/1.3 var(--font-body); text-transform: uppercase; letter-spacing: .06em; color: var(--ink-muted); }}
h1 {{ font-family: var(--font-display); font-weight: 400; font-size: 58px; line-height: 1.05; margin-top: 12px;
  text-shadow: 4px 3px 0 rgba(200,80,30,.35); }}
.standfirst {{ margin-top: 12px; font: 400 17px/1.5 var(--font-body); color: var(--ink-muted); width: 820px; }}
svg.shelf {{ position: absolute; left: 0; top: 0; }}
.spine {{ font: 700 12.5px var(--font-body); fill: var(--ink); text-anchor: middle; }}
.hero-block {{ position: absolute; right: 64px; top: 90px; width: 480px; text-align: left; z-index: 3;
  border-top: 2px solid var(--ink); padding-top: 20px; }}
.hero-num {{ font-family: var(--font-display); font-size: 150px; line-height: 1; color: var(--ink);
  text-shadow: 4px 3px 0 var(--chart-1); }}
.hero-label {{ font: 700 21px/1.35 var(--font-body); margin-top: 4px; }}
.hero-sub {{ margin-top: 10px; font: italic 400 14.5px/1.5 var(--font-body); color: var(--ink-muted); }}
.legend {{ position: absolute; right: 64px; top: 560px; width: 560px; z-index: 3; }}
.lg {{ border-top: 2px solid var(--ink); padding: 13px 0; font: 400 16px/1.45 var(--font-body); display: flex; align-items: center; gap: 12px; }}
.lg:last-child {{ border-bottom: 2px solid var(--ink); }}
.sw {{ width: 24px; height: 15px; border: 2px solid var(--ink); flex: none; }}
.lgn {{ font-weight: 700; }}
footer {{ position: absolute; left: 64px; right: 64px; bottom: 24px; z-index: 3;
  display: flex; justify-content: space-between; gap: 40px;
  border-top: 1.5px solid var(--ink); padding-top: 12px; font: 400 14px/1.5 var(--font-body); color: var(--ink-muted); }}
footer b {{ font-weight: 700; color: var(--ink); }}
</style>
</head>
<body>
<div class="canvas">
  <svg class="grain" width="1920" height="1080"><filter id="g"><feTurbulence type="fractalNoise" baseFrequency="0.8" numOctaves="2"/><feColorMatrix values="0 0 0 0 0.2 0 0 0 0 0.14 0 0 0 0 0.1 0 0 0 0.5 0"/></filter><rect width="1920" height="1080" filter="url(#g)"/></svg>
  <div class="title-block">
    <div class="kicker">САНСКРИТСКИЙ АРХИВ ГАСУНСА · CSL-ORIG · ПОСЧИТАНО 29.08.2026</div>
    <h1>Три языка науки: на чём говорят словари</h1>
    <p class="standfirst">45 словарей Кёльна — на одной полке, каждый корешок окрашен по языку глосс: выборка глосс каждого словаря проверена на кириллицу, французские акценты, немецкие и английские служебные слова.</p>
  </div>
  <svg class="shelf" width="1920" height="1080" viewBox="0 0 1920 1080">
      {svg}
  </svg>
  <div class="hero-block" data-hero>
    <div class="hero-num">0</div>
    <div class="hero-label">русских словарей в каноне Кёльна</div>
    <div class="hero-sub">Даже «Кочергина» из нашей коллекции хранится в csl-orig транслитом, без кириллицы. Русская ниша санскритской лексикографии свободна — её занимает наш проект.</div>
  </div>
  <div class="legend">
    {legend}
  </div>
  <footer>
    <div>Данные: <b>csl-orig/v02</b> — выборка глоссовых строк каждого словаря; Bucket SA — глоссы санскритом или транслитом без европейских маркеров</div>
    <div>скрипт: <b>scripts/infographics50/three_languages.py</b> · Посчитано 29.08.2026 · <b>Dr. Mārcis Gasūns</b></div>
  </footer>
</div>
</body>
</html>
"""

if __name__ == "__main__":
    main()
