#!/usr/bin/env python3
"""Samasa wheel #19 — the compound mandala from SamasaChakram taxonomy.

Derives infographics/samasa-chakram-2026-08-29/{data.json,index.html}.
Source: SamasaChakram/samasacakra/samasacakra-taxonomy.json (committed).
Arc angles proportional to leaf-subtype counts per class (truthful geometry).
"""
import json
import math
import os

TAX = "/Users/mac/Documents/GitHub/SamasaChakram/samasacakra/samasacakra-taxonomy.json"
BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
OUT = os.path.join(BASE, "infographics", "samasa-chakram-2026-08-29")

INKS = {"tatpurusa": "#C8501E", "bahuvrihi": "#157F63", "dvandva": "#AD7A00", "avyayibhava": "#8E4468"}
RU = {"tatpurusa": "татпуруша", "bahuvrihi": "бахуврихи", "dvandva": "двандва", "avyayibhava": "авьяйибхава"}


def arc(cx, cy, r, a0, a1):
    large = 1 if (a1 - a0) > math.pi else 0
    x0, y0 = cx + r * math.cos(a0), cy + r * math.sin(a0)
    x1, y1 = cx + r * math.cos(a1), cy + r * math.sin(a1)
    return "M %.1f %.1f A %.1f %.1f 0 %d 1 %.1f %.1f" % (x0, y0, r, r, large, x1, y1)


def main():
    d = json.load(open(TAX, encoding="utf-8"))
    classes = []
    fam_total = 0
    leaf_total = 0
    for c in d["classes"]:
        fams = c.get("families", [])
        n = sum(len(f.get("leaves", [])) for f in fams)
        fam_total += len(fams)
        leaf_total += n
        ex = fams[0]["leaves"][0]
        classes.append({"id": c["id"], "name": RU.get(c["id"], c["id"]), "families": len(fams),
                        "leaves": n, "pradhana": c.get("pradhana", ""),
                        "ex_term": ex.get("term", ""), "ex": ex.get("ex", ""),
                        "vigraha": ex.get("vigraha", ""), "ru": ex.get("ru", "")})
    assert leaf_total == 58 and fam_total == 9, (leaf_total, fam_total)
    os.makedirs(OUT, exist_ok=True)
    json.dump({"classes": classes, "families": fam_total, "leaves": leaf_total},
              open(os.path.join(OUT, "data.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)

    CX, CY = 560, 600
    R1, W1 = 336, 74
    R2, W2 = 244, 10
    start = -math.pi / 2
    parts = []
    for c in classes:
        span = 2 * math.pi * c["leaves"] / leaf_total
        col = INKS[c["id"]]
        mid = start + span / 2
        # class ring segment
        parts.append('<path class="seg" d="%s" fill="none" stroke="%s" stroke-width="%d"/>'
                     % (arc(CX, CY, R1 - W1 / 2, start + 0.012, start + span - 0.012), col, W1))
        # family ticks on inner ring
        fa = start
        for f in [f for f in d["classes"] if f["id"] == c["id"]][0]["families"]:
            fspan = 2 * math.pi * len(f.get("leaves", [])) / leaf_total
            parts.append('<path d="%s" fill="none" stroke="%s" stroke-width="%d" opacity=".8"/>'
                         % (arc(CX, CY, R2, fa + 0.006, fa + fspan - 0.006), col, W2))
            fa += fspan
        # label on arc
        lx, ly = CX + (R1 + 64) * math.cos(mid), CY + (R1 + 64) * math.sin(mid)
        parts.append('<text class="seg-lab" x="%.1f" y="%.1f" fill="%s">%s · %d</text>'
                     % (lx, ly, col, c["name"], c["leaves"]))
        start += span
    # sunburst rays behind the wheel
    for i in range(20):
        a = 2 * math.pi * i / 20
        parts.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="#AD7A00" stroke-width="3" opacity=".14"/>'
                     % (CX + 380 * math.cos(a), CY + 380 * math.sin(a), CX + 470 * math.cos(a), CY + 470 * math.sin(a)))
    svg = "\n      ".join(parts)

    legend = []
    for c in classes:
        legend.append(
            '<div class="lg"><div class="lg-h"><span class="sw" style="background:%s"></span>%s — %d подтипов в %d семействах</div>'
            '<div class="lg-p">%s</div>'
            '<div class="lg-ex"><i>%s</i> «%s» — %s</div></div>'
            % (INKS[c["id"]], c["name"], c["leaves"], c["families"], c["pradhana"],
               c["ex"], c["vigraha"], c["ru"]))
    html = TEMPLATE.format(svg=svg, legend="\n    ".join(legend),
                           leaves=leaf_total, fams=fam_total)
    open(os.path.join(OUT, "index.html"), "w", encoding="utf-8").write(html)
    print("families", fam_total, "leaves", leaf_total, [c["leaves"] for c in classes])


TEMPLATE = """<!doctype html>
<html lang="ru">
<head>
<meta charset="utf-8">
<title>Колесо самас: 58 подтипов</title>
<!-- Composition: Big Object — the mandala wheel (4 ink classes, 9 family ticks, center seal)
     dominates the left two-thirds; legend column right. Retro-print, wide 1920x1080.
     Segment angles proportional to leaf-subtype counts from samasacakra-taxonomy.json. -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Alfa+Slab+One&family=Karla:ital,wght@0,400;0,500;0,700;1,400&display=swap" rel="stylesheet">
<style>
*, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
:root {{
  --bg:#F5E9D4; --surface:#FBF3E2; --surface-2:#E7D6B6;
  --ink:#33241A; --ink-muted:#6E5B49;
  --chart-1:#C8501E; --chart-2:#157F63; --chart-3:#AD7A00; --chart-4:#8E4468;
  --font-display:'Alfa Slab One',serif; --font-body:'Karla',sans-serif;
}}
html, body {{ background: var(--bg); }}
body {{ width: 1920px; font-family: var(--font-body); color: var(--ink); }}
.canvas {{ position: relative; width: 1920px; height: 1080px; overflow: hidden;
  background: radial-gradient(ellipse 1300px 700px at 26% 55%, #FBF3E2 0%, var(--bg) 72%); }}
.grain {{ position: absolute; inset: 0; pointer-events: none; opacity: .36; }}
.title-block {{ position: absolute; left: var(--space-5, 64px); top: var(--space-4, 40px); width: 900px; z-index: 3; }}
.kicker {{ font: 700 15px/1.3 var(--font-body); text-transform: uppercase; letter-spacing: .06em; color: var(--ink-muted); }}
h1 {{ font-family: var(--font-display); font-weight: 400; font-size: 62px; line-height: 1.05; margin-top: var(--space-2);
  text-shadow: 4px 3px 0 rgba(200,80,30,.35); }}
.standfirst {{ margin-top: var(--space-2); font: 400 17px/1.5 var(--font-body); color: var(--ink-muted); width: 760px; }}
svg.wheel {{ position: absolute; left: 0; top: 0; }}
.seg-lab {{ font: 700 24px var(--font-body); paint-order: stroke; stroke: #F5E9D4; stroke-width: 8; stroke-linejoin: round; }}
.seal-arc {{ font: 700 15px var(--font-body); letter-spacing: .32em; text-transform: uppercase; fill: var(--ink-muted); }}
.center {{ position: absolute; left: 428px; top: 512px; width: 264px; text-align: center; z-index: 2; }}
.hero-num {{ font-family: var(--font-display); font-size: 132px; line-height: 1; color: var(--ink);
  text-shadow: 4px 3px 0 var(--chart-1); }}
.hero-label {{ font: 700 17px/1.3 var(--font-body); margin-top: 2px; }}
.legend {{ position: absolute; right: var(--space-5, 64px); top: 220px; width: 620px; }}
.lg {{ border-top: 2px solid var(--ink); padding: 16px 0 20px; }}
.lg:last-child {{ border-bottom: 2px solid var(--ink); }}
.lg-h {{ display: flex; align-items: center; gap: 12px; font: 700 21px var(--font-body); }}
.sw {{ width: 26px; height: 16px; border: 2px solid var(--ink); flex: none; }}
.lg-p {{ margin-top: 6px; font: 500 14.5px/1.4 var(--font-body); color: var(--ink-muted); }}
.lg-ex {{ margin-top: 6px; font: 400 15.5px/1.45 var(--font-body); }}
.lg-ex i {{ color: var(--chart-2); }}
footer {{ position: absolute; left: var(--space-5, 64px); right: var(--space-5, 64px); bottom: var(--space-3, 24px);
  display: flex; justify-content: space-between; gap: 40px;
  border-top: 1.5px solid var(--ink); padding-top: 12px; font: 400 14px/1.5 var(--font-body); color: var(--ink-muted); }}
footer b {{ font-weight: 700; color: var(--ink); }}
</style>
</head>
<body>
<div class="canvas">
  <svg class="grain" width="1920" height="1080"><filter id="g"><feTurbulence type="fractalNoise" baseFrequency="0.8" numOctaves="2"/><feColorMatrix values="0 0 0 0 0.2 0 0 0 0 0.14 0 0 0 0 0.1 0 0 0 0.5 0"/></filter><rect width="1920" height="1080" filter="url(#g)"/></svg>
  <div class="title-block">
    <div class="kicker">САНСКРИТСКИЙ АРХИВ ГАСУНСА · SAMASACHAKRAM · ПОСЧИТАНО 29.08.2026</div>
    <h1>Колесо самас: {leaves} подтипов</h1>
    <p class="standfirst">Все типы санскритских компаундов из таксономии SamasaChakram — четыре класса по «главному слову» Патанджали, {fams} семейства, 58 листьев. Дуга каждого класса пропорциональна числу подтипов; тонкие дуги внутри — семейства.</p>
  </div>
  <svg class="wheel" width="1920" height="1080" viewBox="0 0 1920 1080">
      {svg}
  </svg>
  <div class="center" data-hero>
    <div class="hero-num">{leaves}</div>
    <div class="hero-label">подтипов самас</div>
  </div>
  <div class="legend">
    {legend}
  </div>
  <footer>
    <div>Данные: <b>SamasaChakram · samasacakra-taxonomy.json</b> — 4 класса, {fams} семейств, {leaves} подтипов; примеры из конспекта Лейтана</div>
    <div>скрипт: <b>scripts/infographics50/samasa_wheel.py</b> · Посчитано 29.08.2026 · <b>Dr. Mārcis Gasūns</b></div>
  </footer>
</div>
</body>
</html>
"""

if __name__ == "__main__":
    main()
