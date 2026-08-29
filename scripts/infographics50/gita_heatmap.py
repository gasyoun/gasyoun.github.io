#!/usr/bin/env python3
"""Gita heatmap #14 — 700 verses x 18 chapters, colored by commentary depth.

Derives infographics/gita-heatmap-2026-08-29/{data.json,index.html}.
Source: CommentaryStrategies/data/gita/chapter_*/verse_*.json (layer fields per verse).
Every number on the page is re-derived here: verse counts, layer groups,
scvv exception, heat thresholds (quartiles of scsri length).
"""
import json
import os

SRC = "/Users/mac/Documents/GitHub/CommentaryStrategies/data/gita"
BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
OUT = os.path.join(BASE, "infographics", "gita-heatmap-2026-08-29")

COLS = {  # field-prefix group -> (label, ink)
    "sc": ("санскритские слои", 13), "et": ("английские переводы", 7),
    "ht": ("хинди", 5), "gl": ("пословные глоссы", 2),
}


def group_of(f):
    if f.startswith("sc"):
        return "sc"
    if f.startswith("et"):
        return "et"
    if f.startswith("ht") or f.startswith("hc"):
        return "ht"
    return "gl"


def fmt(v):
    return "{:,}".format(v).replace(",", " ")


def main():
    chapters = []
    layer_cov = {}
    scsri_lens = []
    verses = 0
    for ci in range(1, 19):
        d = os.path.join(SRC, "chapter_%02d" % ci)
        rows = []
        for fn in sorted(os.listdir(d)):
            if not fn.startswith("verse_"):
                continue
            v = json.load(open(os.path.join(d, fn), encoding="utf-8"))
            n = 0
            for k, val in v.items():
                if isinstance(val, str) and val.strip():
                    layer_cov[k] = layer_cov.get(k, 0) + 1
                    n += 1
            L = len(v.get("scsri", ""))
            scsri_lens.append(L)
            rows.append(L)
            verses += 1
        chapters.append(rows)
    sc_full = sum(1 for l in scsri_lens if l > 0)
    scvv = layer_cov.get("scvv", 0)
    groups = {}
    for f in layer_cov:
        g = group_of(f)
        groups[g] = groups.get(g, 0) + 1
    assert verses == 700 and sum(groups.values()) == 27, (verses, groups)

    import statistics
    qs = statistics.quantiles([l for l in scsri_lens], n=4)
    avg = sum(scsri_lens) // len(scsri_lens)
    mx_i = max(range(700), key=lambda i: scsri_lens[i])
    mx_ch = 0
    acc = 0
    for ci, rows in enumerate(chapters):
        if acc + len(rows) > mx_i:
            mx_ch = ci
            break
        acc += len(rows)
    mx_v = mx_i - acc + 1

    # ---- data.json ----
    os.makedirs(OUT, exist_ok=True)
    json.dump({"verses": verses, "chapters": [len(c) for c in chapters],
               "layers": {f: layer_cov[f] for f in sorted(layer_cov)},
               "scvv_covered": scvv, "scsri_quartiles": qs, "scsri_avg": avg,
               "scsri_max": {"ch": mx_ch + 1, "verse": mx_v, "len": scsri_lens[mx_i]}},
              open(os.path.join(OUT, "data.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)

    # ---- heatmap svg rows ----
    BH, BW, PITCH, X0, Y0 = 26, 13, 14, 118, 372
    parts = []
    maxrow = max(len(c) for c in chapters)
    for ci, rows in enumerate(chapters):
        y = Y0 + ci * (BH + 6)
        parts.append('<text class="chlab" x="%d" y="%.1f">%d</text>' % (X0 - 24, y + BH / 2 + 5, ci + 1))
        parts.append('<text class="chcnt" x="%.1f" y="%.1f">%d</text>' % (X0 + len(rows) * PITCH + 14, y + BH / 2 + 5, len(rows)))
        for vi, L in enumerate(rows):
            if L <= qs[0]:
                cls = "q0"
            elif L <= qs[1]:
                cls = "q1"
            elif L <= qs[2]:
                cls = "q2"
            else:
                cls = "q3"
            x = X0 + vi * PITCH
            parts.append('<rect class="brick %s" x="%d" y="%d" width="%d" height="%d"/>' % (cls, x, y, BW, BH))
    parts.append('<text class="chlab" x="%d" y="%.1f">гл.</text>' % (X0 - 96, Y0 - 12))
    parts.append('<text class="chcnt" x="%d" y="%.1f">шлок</text>' % (X0 + maxrow * PITCH - 24, Y0 - 12))
    bars = "\n      ".join(parts)

    html = TEMPLATE.format(
        bars=bars,
        q1=fmt(int(qs[0])), q2=fmt(int(qs[1])), q3=fmt(int(qs[2])),
        avg=fmt(avg), mx_len=fmt(scsri_lens[mx_i]),
        mx_ch=mx_ch + 1, mx_v=mx_v,
        ch18=max(len(c) for c in chapters), chmin=min(len(c) for c in chapters),
    )
    open(os.path.join(OUT, "index.html"), "w", encoding="utf-8").write(html)
    print("verses", verses, "| quartiles", [int(q) for q in qs], "| avg", avg,
          "| max gl.%d.%d %d" % (mx_ch + 1, mx_v, scsri_lens[mx_i]), "| scvv", scvv)


TEMPLATE = """<!doctype html>
<html lang="ru">
<head>
<meta charset="utf-8">
<title>Гита: тепловая карта 700 шлок</title>
<!-- Composition: Big Object — the brick wall of 700 verses (18 chapter courses) fills the left
     two-thirds; title + hero layers block on the right. Retro-print, wide 1920x1080.
     Brick color = quartile of the Sanskrit commentary field scsri length (data.json).
     Layer groups re-derived from field-name prefixes of CommentaryStrategies/data/gita verse JSON. -->
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
  --space-1:8px; --space-2:16px; --space-3:24px; --space-4:40px; --space-5:64px;
}}
html, body {{ background: var(--bg); }}
body {{ width: 1920px; font-family: var(--font-body); color: var(--ink); }}
.canvas {{ position: relative; width: 1920px; height: 1080px; overflow: hidden;
  background: radial-gradient(ellipse 1500px 700px at 30% 20%, #FBF3E2 0%, var(--bg) 70%); }}
.grain {{ position: absolute; inset: 0; pointer-events: none; opacity: .38; }}
.title-block {{ position: absolute; left: var(--space-5); top: var(--space-4); width: 700px; }}
.kicker {{ font: 700 15px/1.3 var(--font-body); text-transform: uppercase; letter-spacing: .06em; color: var(--ink-muted); }}
h1 {{ font-family: var(--font-display); font-weight: 400; font-size: 64px; line-height: 1.04;
  margin-top: var(--space-2); text-shadow: 4px 3px 0 rgba(200,80,30,.35); }}
.standfirst {{ margin-top: var(--space-2); font: 400 17px/1.5 var(--font-body); color: var(--ink-muted); width: 660px; }}
.hero-block {{ position: absolute; right: var(--space-5); top: var(--space-4); width: 560px; text-align: left;
  border-top: 2px solid var(--ink); padding-top: var(--space-3); }}
.hero-num {{ font-family: var(--font-display); font-size: 132px; line-height: 1; color: var(--ink);
  text-shadow: 4px 3px 0 var(--chart-1); }}
.hero-label {{ margin-top: var(--space-1); font: 700 22px/1.3 var(--font-body); }}
.hero-sub {{ margin-top: var(--space-2); font: 400 16.5px/1.55 var(--font-body); color: var(--ink-muted); }}
.legend {{ margin-top: var(--space-3); }}
.legend .row {{ display: flex; align-items: center; gap: 10px; font: 700 15.5px var(--font-body); margin-bottom: 10px; }}
.sw {{ width: 30px; height: 18px; border: 2px solid var(--ink); flex: none; }}
.note {{ margin-top: var(--space-3); font: italic 400 14px/1.5 var(--font-body); color: var(--ink-muted); width: 520px; }}
svg.wall {{ position: absolute; left: 0; top: 0; }}
.brick {{ stroke: rgba(51,36,26,.45); stroke-width: .5; }}
.brick.q0 {{ fill: var(--de-emphasis); }}
.brick.q1 {{ fill: var(--chart-3); }}
.brick.q2 {{ fill: var(--chart-2); }}
.brick.q3 {{ fill: var(--chart-1); }}
.chlab {{ font: 700 15px var(--font-body); fill: var(--ink); }}
.chcnt {{ font: 400 13.5px var(--font-body); fill: var(--ink-muted); }}
.heatline {{ position: absolute; left: var(--space-5); bottom: 132px; }}
footer {{ position: absolute; left: var(--space-5); right: var(--space-5); bottom: var(--space-3);
  display: flex; justify-content: space-between; gap: 40px;
  border-top: 1.5px solid var(--ink); padding-top: 12px; font: 400 14px/1.5 var(--font-body); color: var(--ink-muted); }}
footer b {{ font-weight: 700; color: var(--ink); }}
</style>
</head>
<body>
<div class="canvas">
  <svg class="grain" width="1920" height="1080"><filter id="g"><feTurbulence type="fractalNoise" baseFrequency="0.8" numOctaves="2"/><feColorMatrix values="0 0 0 0 0.2 0 0 0 0 0.14 0 0 0 0 0.1 0 0 0 0.5 0"/></filter><rect width="1920" height="1080" filter="url(#g)"/></svg>
  <div class="title-block">
    <div class="kicker">САНСКРИТСКИЙ АРХИВ ГАСУНСА · БХАГАВАДГИТА · ПОСЧИТАНО 29.08.2026</div>
    <h1>Гита: тепловая карта 700 шлок</h1>
    <p class="standfirst">Каждый кирпич — одна шлока Бхагавадгиты; 18 рядов — 18 глав. Цвет показывает, насколько пространный санскритский комментарий (поле scsri) сопровождает шлоку: от краткого до развёрнутого толкования. Стена читается слева направо, глава за главой.</p>
  </div>
  <div class="hero-block" data-hero>
    <div class="hero-num">27</div>
    <div class="hero-label">слоя текста на каждую из 700 шлок</div>
    <div class="hero-sub">13 санскритских · 7 английских переводов · 5 хинди · 2 пословные глоссы. У 670 шлок есть и 27-й слой (scvv) — тридцати шлокам его не достаётся.</div>
    <div class="legend">
      <div class="row"><span class="sw" style="background:var(--de-emphasis)"></span> комментарий до {q1} знаков</div>
      <div class="row"><span class="sw" style="background:var(--chart-3)"></span> {q1}–{q2} знаков</div>
      <div class="row"><span class="sw" style="background:var(--chart-2)"></span> {q2}–{q3} знаков</div>
      <div class="row"><span class="sw" style="background:var(--chart-1)"></span> свыше {q3} знаков</div>
    </div>
    <div class="note">Самый длинный комментарий — шлока {mx_ch}.{mx_v}, {mx_len} знаков. Средняя глубина по всей Гите — {avg} знаков на шлоку. Самая просторная глава — 18-я: {ch18} шлок; самые сжатые — {chmin} шлок.</div>
  </div>
  <svg class="wall" width="1920" height="1080" viewBox="0 0 1920 1080">
      {bars}
  </svg>
  <div class="heatline" style="display:none"></div>
  <footer>
    <div>Данные: <b>CommentaryStrategies · data/gita</b> — 700 шлок × 27 слоёв (гл. 1–18), счёт по полям verse JSON</div>
    <div>скрипт: <b>scripts/infographics50/gita_heatmap.py</b> · Посчитано 29.08.2026 · <b>Dr. Mārcis Gasūns</b></div>
  </footer>
</div>
</body>
</html>
"""

if __name__ == "__main__":
    main()
