#!/usr/bin/env python3
"""Render campus/index.html from campus_data.json (derive-don't-store, idempotent). H4261."""
import json
from pathlib import Path

HERE = Path(__file__).parent
data = json.loads((HERE/"campus_data.json").read_text(encoding="utf-8"))
WING_INTRO = {
    "grammar": "Падежи, сандхи, самасы, морфология, письмо — как устроен язык.",
    "study": "Путь ученика: от алфавита до Рамаяны, слова и тексты в цифрах.",
    "estate": "Что построено, кем, чего стоит: карта, пульс и цена имения.",
    "products": "Словари, школы, воронки и всё, что работает на ученика и читателя.",
}
CSS = (HERE/"campus.css").read_text(encoding="utf-8")
def esc(s): return s.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")
total = sum(len(w["items"]) for w in data["wings"].values())
out = [f"""<!doctype html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Кампус наглядности — санскритское имение одним входом</title>
<style>{CSS}</style>
</head>
<body>
<main>
<h1>Кампус <span>наглядности</span></h1>
<p class="sub">Один вход ко всей визуальной наглядности имения: {total} артефактов в 4 крыльях. Сгенерировано скриптом — рукописных страниц нет.</p>"""]
for wid, w in data["wings"].items():
    out.append(f'<h2 id="{wid}"><span class="n">крыло</span>{esc(w["title"])}</h2>')
    out.append(f'<p class="intro">{esc(WING_INTRO[wid])}</p>')
    out.append("<ul>")
    for it in w["items"]:
        no = f'<span class="no">№{it["no"]}</span>' if it.get("no") else '<span class="no">·</span>'
        if it["url"]:
            out.append(f'<li>{no}<a href="{it["url"]}">{esc(it["title"])}</a></li>')
        else:
            out.append(f'<li>{no}<span class="plain">{esc(it["title"])}</span></li>')
    out.append("</ul>")
out.append(f"""
<footer>Собрано <a href="https://github.com/gasyoun/gasyoun.github.io/blob/master/scripts/campus/campus_build.py">scripts/campus/campus_build.py</a> из <a href="https://gasyoun.github.io/infographics/sanskrit-infographics-catalog/index.html">каталога инфографик</a> · H4261 · 06-09-2026 · Dr. Mārcis Gasūns</footer>
</main>
</body>
</html>
""")
dest = HERE.parent.parent/"campus"/"index.html"
dest.parent.mkdir(parents=True, exist_ok=True)
dest.write_text("\n".join(out), encoding="utf-8")
print("wrote", dest, dest.stat().st_size, "bytes")
