#!/usr/bin/env python3
"""Render mastery/stats.html (statistical variant) from mastery_summary.json. Canonical page: mastery/index.html by mastery_map_build.py (11a5c22) (derive-don't-store, idempotent). H4262.

Aggregate source: kosha/data/mastery/combined_schedule.json (H3742).
Re-derive the summary with: python3 mastery_build.py --from-kosha <path-to-combined_schedule.json>
"""
import json
from pathlib import Path

HERE = Path(__file__).parent
S = json.loads((HERE/"mastery_summary.json").read_text(encoding="utf-8"))

def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

CSS = (HERE/"campus.css").read_text(encoding="utf-8") + """
.family{border:1px solid var(--line);border-radius:10px;padding:1.25rem 1.5rem;margin:0 0 1.5rem}
.family h2{margin:.1rem 0 .2rem;font-size:1.2rem}
.family .desc{color:var(--mut);margin:0 0 1rem;font-size:.95rem}
.bar{display:flex;height:14px;border-radius:7px;overflow:hidden;margin:.4rem 0 .3rem}
.bar i{display:block;height:100%}
.legend{display:flex;gap:1rem;flex-wrap:wrap;color:var(--mut);font-size:.78rem;margin:0 0 .8rem}
.legend b{color:var(--fg);font-weight:normal}
.meta{color:var(--mut);font-size:.8rem;margin:.6rem 0 0}
.firsts{color:var(--mut);font-size:.8rem;font-family:Menlo,monospace}
.note{border-left:3px solid var(--acc);padding:.6rem 1rem;color:var(--mut);margin:2rem 0;font-size:.92rem}
"""
BC = ["#8c3b2e", "#a8562f", "#c08a3e", "#8fae5a", "#5f9e6e"]
BL = ["трудно 0–20%", "20–40%", "40–60%", "60–80%", "легко 80–100%"]

total = S["source"]["total_items"]
src = S["source"]
parts = [f"""<!doctype html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Карта мастерства — пять семей навыков</title>
<style>{CSS}</style>
</head>
<body>
<main>
<h1>Карта <span>мастерства</span></h1>
<p class="sub">{total} учебных позиций в 5 семьях, одна шкала освоимости (ease 0–1, H3742). Дефицита прогресса тут нет: это карта местности — что за чем учить.</p>
"""]
for fam, f in S["families"].items():
    n = f["count"]
    tot = sum(f["bands"])
    bars = "".join(
        f'<i style="width:{(b/tot*100):.1f}%;background:{BC[i]}" title="{BL[i]}: {b}"></i>'
        for i, b in enumerate(f["bands"]) if b)
    legend = " · ".join(f"<b>{BL[i]}</b> {f['bands'][i]}" for i in range(5))
    parts.append(f"""<section class="family">
<h2>{esc(f['title_ru'])} <span style="color:var(--mut);font-weight:normal;font-size:.85rem">— {n} позиций</span></h2>
<p class="desc">{esc(f['desc_ru'])}</p>
<div class="bar">{bars}</div>
<p class="legend">{legend}</p>
<p class="firsts">первые шаги: {' · '.join(f['first_ids'])}</p>
<p class="meta">ease: min {f['ease_min']} · средняя {f['ease_mean']} · медиана {f['ease_median']} · max {f['ease_max']}</p>
</section>""")
parts.append(f"""
<div class="note">Все позиции показаны как «не начато»: это общая карта курса без персональных данных.
Личный слой прогресса (streaks, «что повторить сегодня») живёт локально в ученической системе и на публичную страницу не попадает.</div>
<footer>Источник: <a href="{src['source_dir']}">kosha/data/mastery</a> (коммит {src['kosha_commit']}, эпоха {src['epoch']}, sha256 {src['sha256'][:12]}…, <a href="{src['weights_spec']}">семантика весов</a>) ·
Собрано <a href="https://github.com/gasyoun/gasyoun.github.io/blob/master/scripts/campus/mastery_build.py">scripts/campus/mastery_build.py</a> · H4262 · 06-09-2026 · Dr. Mārcis Gasūns</footer>
</main>
</body>
</html>
""")
dest = HERE.parent.parent/"mastery"/"stats.html"
dest.parent.mkdir(parents=True, exist_ok=True)
dest.write_text(chr(10).join(parts), encoding="utf-8")
print("wrote", dest, dest.stat().st_size, "bytes")
