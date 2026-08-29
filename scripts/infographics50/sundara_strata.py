#!/usr/bin/env python3
"""Commentary strata #15 — annotation layers of the Sundara-kanda apparatus (cutaway).

Derives infographics/commentary-strata-2026-08-29/{data.json,index.html}.
Sources (all committed, metadata counts only — no personal data):
  CommentaryStrategies/data/apparatus/sarga_*_kostina.json — notes[] per verse, layer field
  CommentaryStrategies/data/apparatus/sarga_*.json          — medieval commentator coverage
"""
import collections
import glob
import json
import os

BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
OUT = os.path.join(BASE, "infographics", "commentary-strata-2026-08-29")
APP = "/Users/mac/Documents/GitHub/CommentaryStrategies/data/apparatus"

LAYER_RU = {
    "tier1": ("ярус 1 — примечания Леонова и Костиной", "идут в печать как есть"),
    "lexical": ("лексические и этимологические глоссы", "черновой слой, требует проверки"),
    "phase2": ("диалог комментаторов", "Тилак · Бхушана · Широмани · Таттвадипика"),
    "crosstext": ("переклички с другими текстами", "Законы Ману · Махабхарата · Гита · кавья"),
    "edition": ("расхождения изданий", "южная вульгата против критического издания"),
}


def fmt(v):
    return "{:,}".format(v).replace(",", " ")


def main():
    layers = collections.Counter()
    statuses = collections.Counter()
    total = 0
    for f in sorted(glob.glob(os.path.join(APP, "sarga_*_kostina.json"))):
        d = json.load(open(f, encoding="utf-8"))
        for v in d["verses"]:
            for n in (v.get("notes") or []):
                total += 1
                layers[n.get("layer")] += 1
                statuses[n.get("status")] += 1
    com = collections.Counter()
    verses = 0
    for f in sorted(f for f in glob.glob(os.path.join(APP, "sarga_*.json")) if "kostina" not in f):
        d = json.load(open(f, encoding="utf-8"))
        for v in d["verses"]:
            verses += 1
            for k, val in (v.get("commentary") or {}).items():
                if isinstance(val, str) and val.strip():
                    com[k] += 1
    assert layers["tier1"] == 1058 and total == 2527, (total, dict(layers))

    os.makedirs(OUT, exist_ok=True)
    json.dump({"total_notes": total, "by_layer": dict(layers), "by_status": dict(statuses),
               "verses": verses, "commentator_verses": dict(com)},
              open(os.path.join(OUT, "data.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)

    # ---- book cross-section: layer heights proportional to counts ----
    BOOK_X, BOOK_W = 480, 660
    BOOK_Y0, BOOK_H = 200, 640
    order = ["tier1", "lexical", "phase2", "crosstext", "edition"]
    colors = {"tier1": "#B5432F", "lexical": "#B57F1B", "phase2": "#7B5397",
              "crosstext": "#3E6DA6", "edition": "#0E8E76"}
    hscale = BOOK_H / total
    parts = []
    y = BOOK_Y0
    callouts = []
    num = 0
    for key in order:
        h = layers[key] * hscale
        c = colors[key]
        fill = c + "59"  # ~35% tint over paper
        # hatched cut bands between strata
        parts.append('<rect x="%d" y="%.1f" width="%d" height="%.1f" fill="%s" stroke="#2B2A26" stroke-width="1.2"/>' % (BOOK_X, y, BOOK_W, h, fill))
        parts.append('<rect x="%d" y="%.1f" width="%d" height="6" fill="url(#hatch)"/>' % (BOOK_X, y + h - 6, BOOK_W))
        num += 1
        callouts.append((num, key, y + h / 2))
        # in-layer count label (contrast: white circle + ink text beside)
        parts.append('<text class="strat-cnt" x="%.1f" y="%.1f">%s</text>' % (BOOK_X + 24, y + h / 2 + 7, fmt(layers[key])))
        parts.append('<text class="strat-pct" x="%.1f" y="%.1f">%.0f%%</text>' % (BOOK_X + BOOK_W - 20, y + h / 2 + 7, 100.0 * layers[key] / total))
        y += h
    # book cover sides (cut face stronger)
    parts.append('<rect x="%d" y="%d" width="%d" height="%d" fill="none" stroke="#2B2A26" stroke-width="3"/>' % (BOOK_X, BOOK_Y0, BOOK_W, BOOK_H))
    parts.append('<rect x="%d" y="%d" width="14" height="%d" fill="#E4DBC4" stroke="#2B2A26" stroke-width="1.2"/>' % (BOOK_X - 14, BOOK_Y0 - 10, BOOK_H + 20))
    parts.append('<rect x="%d" y="%d" width="%d" height="12" fill="#E4DBC4" stroke="#2B2A26" stroke-width="1.2"/>' % (BOOK_X - 14, BOOK_Y0 - 10, BOOK_W + 14))
    # callout circles pinned to strata + leader to captions on the right
    for n, key, cy in callouts:
        cx = BOOK_X + BOOK_W + 34
        parts.append('<circle cx="%.1f" cy="%.1f" r="13" fill="%s"/>' % (cx, cy, colors[key]))
        parts.append('<text class="callout-txt" x="%.1f" y="%.1f">%d</text>' % (cx, cy + 5, n))
        parts.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="#2B2A26" stroke-width="1"/>' % (BOOK_X + BOOK_W + 4, cy, cx - 13, cy))
    # commentator bars (detail column bottom-right) — local coords for the 430x170 lens svg
    bars = []
    mx = max(com.values())
    for i, (k, label) in enumerate([("bhusana", "Бхушана"), ("siromani", "Широмани"),
                                    ("tilaka", "Тилак"), ("tattvadipika", "Таттвадипика")]):
        v = com[k]
        w = 160.0 * v / mx
        yy = 30 + i * 38
        bars.append('<text class="comlab" x="0" y="%d">%s</text>' % (yy, label))
        bars.append('<rect x="110" y="%d" width="%.0f" height="13" fill="#3E6DA699" stroke="#2B2A26" stroke-width="1"/>' % (yy - 11, w))
        bars.append('<text class="comval" x="%.0f" y="%d">%s</text>' % (116 + w, yy, fmt(v)))
    # tiny person for scale
    person = ('<g transform="translate(430,868)" stroke="#2B2A26" stroke-width="2" fill="none">'
              '<circle cx="0" cy="-34" r="7" fill="#FAF6EC"/>'
              '<line x1="0" y1="-27" x2="0" y2="-6"/><line x1="0" y1="-6" x2="-9" y2="10"/>'
              '<line x1="0" y1="-6" x2="9" y2="10"/><line x1="0" y1="-20" x2="-11" y2="-10"/>'
              '<line x1="0" y1="-20" x2="11" y2="-12"/></g>')
    svg = "\n      ".join(parts) + person
    lens_svg = "\n      ".join(bars)

    st = statuses
    html = TEMPLATE.format(svg=svg, lens_svg=lens_svg,
                           total=fmt(total),
                           t1=fmt(layers["tier1"]), lx=fmt(layers["lexical"]),
                           p2=fmt(layers["phase2"]), ct=fmt(layers["crosstext"]),
                           ed=fmt(layers["edition"]),
                           verses=fmt(verses), bh=fmt(com["bhusana"]), sr=fmt(com["siromani"]),
                           tl=fmt(com["tilaka"]), td=fmt(com["tattvadipika"]),
                           st_print=fmt(st.get("в печатном аппарате перевода", 0)),
                           st_rev=fmt(st.get("review_required", 0)),
                           st_gate=fmt(st.get("ожидает гейта М.Г.", 0)),
                           st_ok=fmt(st.get("принято", 0) + st.get("принято гейтом М.Г. (2026-07-03)", 0)))
    open(os.path.join(OUT, "index.html"), "w", encoding="utf-8").write(html)
    print("notes", total, dict(layers), "| verses", verses, dict(com))


TEMPLATE = """<!doctype html>
<html lang="ru">
<head>
<meta charset="utf-8">
<title>Стратиграфия комментария: 2527 примечаний</title>
<!-- Composition: Big Object — the Sundara-kanda volume sliced open, five annotation strata inside;
     museum placard left, commentator detail column right. Cutaway, wide 1920x1080.
     Stratum heights proportional to note counts (data.json); hatched bands mark the cut. -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Bitter:wght@500;600;700;800&family=Source+Sans+3:ital,wght@0,400;0,600;0,700;1,400&display=swap" rel="stylesheet">
<style>
*, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
:root {{
  --bg:#FAF6EC; --surface:#F1EADA; --surface-2:#E4DBC4;
  --ink:#2B2A26; --ink-muted:#6E695D;
  --chart-1:#B5432F; --chart-2:#3E6DA6; --chart-3:#B57F1B;
  --chart-4:#0E8E76; --chart-5:#7B5397;
}}
html, body {{ background: var(--bg); }}
body {{ width: 1920px; font-family: 'Source Sans 3',sans-serif; color: var(--ink); }}
.canvas {{ position: relative; width: 1920px; height: 1080px; overflow: hidden; background: var(--bg); }}
.placard {{ position: absolute; left: var(--sp4, 40px); left: 64px; top: 56px; width: 380px;
  background: var(--surface); border: 2px solid var(--ink); padding: 24px; }}
.kicker {{ font: 700 13.5px/1.4 'Source Sans 3'; text-transform: uppercase; letter-spacing: .07em; color: var(--ink-muted); }}
h1 {{ font-family: 'Bitter',serif; font-weight: 800; font-size: 46px; line-height: 1.06; margin-top: 12px; }}
.standfirst {{ margin-top: 12px; font: 400 15.5px/1.5 'Source Sans 3'; color: var(--ink-muted); }}
.hero-num {{ font-family: 'Bitter',serif; font-weight: 800; font-size: 150px; line-height: 1; margin-top: 16px; letter-spacing: -0.01em; }}
.hero-label {{ font: 600 16px/1.35 'Source Sans 3'; margin-top: 6px; }}
.status {{ margin-top: 16px; border-top: 1px solid var(--ink); padding-top: 12px; font: 400 14px/1.7 'Source Sans 3'; }}
.status b {{ font-weight: 700; }}
svg.plate {{ position: absolute; left: 0; top: 0; }}
.strat-cnt {{ font: 700 26px 'Bitter',serif; fill: #FAF6EC; }}
.strat-pct {{ font: 600 15px 'Source Sans 3'; fill: #FAF6EC; text-anchor: end; }}
.callout-txt {{ font: 700 14px 'Source Sans 3'; fill: #FAF6EC; text-anchor: middle; }}
.comlab {{ font: 700 15px 'Source Sans 3'; fill: var(--ink); }}
.comval {{ font: 600 14px 'Source Sans 3'; fill: var(--ink-muted); }}
.captions {{ position: absolute; right: 64px; top: 150px; width: 300px; }}
.cap {{ margin-bottom: 26px; }}
.cap .n {{ display: inline-flex; width: 24px; height: 24px; border-radius: 50%; align-items: center;
  justify-content: center; font: 700 14px 'Source Sans 3'; color: #FAF6EC; margin-right: 8px; }}
.cap .t {{ font: 400 14.5px/1.45 'Source Sans 3'; color: var(--ink); }}
.cap .t b {{ font-weight: 700; }}
.lens {{ position: absolute; right: 64px; top: 646px; width: 430px; border-top: 2px solid var(--ink); padding-top: 10px; }}
.lens h2 {{ font: 700 17px 'Source Sans 3'; margin-bottom: 2px; }}
.lens .sub {{ font: 400 13px/1.4 'Source Sans 3'; color: var(--ink-muted); margin-bottom: 8px; }}
footer {{ position: absolute; left: 64px; right: 64px; bottom: 24px;
  display: flex; justify-content: space-between; gap: 40px;
  border-top: 1.5px solid var(--ink); padding-top: 12px; font: 400 14px/1.5 'Source Sans 3'; color: var(--ink-muted); }}
footer b {{ font-weight: 700; color: var(--ink); }}
</style>
</head>
<body>
<div class="canvas">
  <div class="placard">
    <div class="kicker">САНСКРИТСКИЙ АРХИВ ГАСУНСА · СУНДАРАКАНДА · ПОСЧИТАНО 29.08.2026</div>
    <h1>Стратиграфия комментария</h1>
    <p class="standfirst">Пятая книга Рамаяны в переводе Леонова готовится к печати с двухъярусным аппаратом. В разрезе тома — пять слоёв примечаний: от неприкосновенного яруса перевода до черновых глосс и диалога средневековых комментаторов.</p>
    <div class="hero-num" data-hero>{total}</div>
    <div class="hero-label">примечания в аппарате — 68 песней, {verses} шлок</div>
    <div class="status">
      <b>{st_print}</b> — в печатном аппарате перевода (ярус 1)<br>
      <b>{st_ok}</b> — принято гейтами · <b>{st_rev}</b> — на проверке<br>
      <b>{st_gate}</b> — ожидают гейта М.Г. · ни одно не печатается автоматически
    </div>
  </div>
  <svg class="plate" width="1920" height="1080" viewBox="0 0 1920 1080">
    <defs>
      <pattern id="hatch" patternUnits="userSpaceOnUse" width="6" height="6" patternTransform="rotate(45)">
        <rect width="6" height="6" fill="#FAF6EC"/><line x1="0" y1="0" x2="0" y2="6" stroke="#2B2A26" stroke-width="1" opacity=".55"/>
      </pattern>
    </defs>
      {svg}
  </svg>
  <div class="captions">
    <div class="cap"><span class="n" style="background:var(--chart-1)">1</span><span class="t"><b>Ярус 1 — примечания Леонова и Костиной · {t1}.</b> Единственный слой, который идёт в печать как есть.</span></div>
    <div class="cap"><span class="n" style="background:var(--chart-3)">2</span><span class="t"><b>Лексические и этимологические глоссы · {lx}.</b> Черновой слой, каждая строка требует проверки.</span></div>
    <div class="cap"><span class="n" style="background:var(--chart-5)">3</span><span class="t"><b>Диалог комментаторов · {p2}.</b> «Тилака понимает это слово так-то, а Широмани иначе».</span></div>
    <div class="cap"><span class="n" style="background:var(--chart-2)">4</span><span class="t"><b>Переклички с другими текстами · {ct}.</b> Законы Ману, Махабхарата, Гита, Калидаса.</span></div>
    <div class="cap"><span class="n" style="background:var(--chart-4)">5</span><span class="t"><b>Расхождения изданий · {ed}.</b> Места, где южная вульгата полнее критического издания.</span></div>
  </div>
  <div class="lens">
    <h2>Голоса комментаторов — число шлок с их толкованием</h2>
    <div class="sub">Из {verses} шлок Сундараканды (санскрит с Gita Supersite, CC BY 4.0)</div>
    <svg width="430" height="170">
      {lens_svg}
    </svg>
  </div>
  <footer>
    <div>Данные: <b>CommentaryStrategies · data/apparatus</b> — примечания 68 костинских сводок sarga_*_kostina.json + покрытие комментаторов в sarga_*.json</div>
    <div>скрипт: <b>scripts/infographics50/sundara_strata.py</b> · Посчитано 29.08.2026 · <b>Dr. Mārcis Gasūns</b></div>
  </footer>
</div>
</body>
</html>
"""

if __name__ == "__main__":
    main()
