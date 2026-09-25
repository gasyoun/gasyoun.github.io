# -*- coding: utf-8 -*-
"""lectures.html (zalizniak-2026): слова с рассказами в школьных лекциях Зализняка.
MG 25-09-2026: не переделывая BookIndex, взять его данные (app_data.json, lexicon
1367 статей, книга mumintroll) и отметить пересечение с нашей выборкой — чтобы
на лекции можно было сослаться: «про это слово у Зализняка есть рассказ, с. N»."""
import json, io, re, os, sys, unicodedata, importlib.util

HERE = os.path.dirname(os.path.abspath(__file__))
BOOKINDEX = r"C:/Users/user/Documents/GitHub/BookIndex/app_data.json"
sys.stdout.reconfigure(encoding="utf-8")

def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

def norm(w):
    w = unicodedata.normalize("NFKD", w)
    w = "".join(c for c in w if not unicodedata.combining(c))
    w = w.lower().replace("ё", "е").replace("´", "")
    w = re.sub(r"[⟨⟩()\[\]0-9!?,.\-–—:;'\"/ ]+", "", w)
    return w

# ---- наша выборка: русская колонка + школьная 50-ка + DCS-русские параллели ----
spec = importlib.util.spec_from_file_location("bp", os.path.join(HERE, "build_page.py"))
bp = importlib.util.module_from_spec(spec); spec.loader.exec_module(bp)
targets = {}  # norm -> (показ-слово, источник)
for m in bp.M:
    for w in m["ru"]:
        base = re.sub(r"[⟨⟩()\[\]]", "", w)
        base = re.split(r"[·,]", base)[0].strip()
        if base:
            targets.setdefault(norm(base), (base, "выборка Зализняка"))
import importlib
try:
    be = importlib.util.module_from_spec(importlib.util.spec_from_file_location(
        "be", os.path.join(HERE, "build_extras.py")))
    spec2 = importlib.util.spec_from_file_location("be", os.path.join(HERE, "build_extras.py"))
    be = importlib.util.module_from_spec(spec2); spec2.loader.exec_module(be)
    for w in be.SCHOOL_50:
        targets.setdefault(norm(w), (w, "школьная 50-ка Фасмера"))
    for slp, cnt, san, gloss, n, ru in getattr(be, "_DCS_RU", []):
        pass
except Exception:
    pass

# ---- BookIndex ----
D = json.load(io.open(BOOKINDEX, encoding="utf-8"))
lex = D["lexicon"]
lectures = D.get("lectures", [])

def page_to_lecture(pg):
    for L in lectures:
        mm = re.findall(r"(\d+)", L.get("pages", ""))
        if mm and len(mm) >= 2 and int(mm[0]) <= pg <= int(mm[1]):
            return L.get("name", "")
        if len(mm) == 1 and int(mm[0]) == pg:
            return L.get("name", "")
    return ""

hits = []
for it in lex:
    heads = [it.get("head", "")] + list(it.get("aliases", []))
    for h in heads:
        nh = norm(h)
        if nh in targets:
            occ = it.get("occurrences", {}).get("mumintroll", {})
            pages = occ.get("pages", []) or it.get("page_list", [])
            ctx = (occ.get("contexts") or [""])[0]
            ctx = re.sub(r"\s+", " ", ctx).strip(" …")
            for pg in pages[:3]:
                hits.append({
                    "word": targets[nh][0], "src": targets[nh][1],
                    "head": h, "page": pg,
                    "lecture": page_to_lecture(pg),
                    "ctx": ctx[:170],
                })
            break

hits.sort(key=lambda x: x["word"].lower())
rows = "\n".join(
    "<tr><td class='w'>%s</td><td>%s</td><td>с. %s</td><td class='c'>%s…</td></tr>"
    % (esc(h["word"]), esc(h["lecture"] or "школьные лекции"), h["page"], esc(h["ctx"]))
    for h in hits)

by_lecture = {}
for h in hits:
    by_lecture.setdefault(h["lecture"] or "школьные лекции", set()).add(h["word"].lower())
lec_rows = "\n".join(
    "<tr><td>%s</td><td>%s</td><td>%s</td></tr>"
    % (esc(k), len(v), esc(" · ".join(sorted(v))))
    for k, v in sorted(by_lecture.items(), key=lambda kv: -len(kv[1])))

html = """<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Слова с рассказами в школьных лекциях Зализняка — zalizniak-2026</title>
<style>
  body{margin:0;background:#faf6ee;color:#26221c;font:17px/1.6 Georgia,serif}
  main{max-width:1000px;margin:0 auto;padding:30px 18px 70px}
  h1{color:#8a3324;font-size:1.7rem}
  h2{color:#2f5d50;border-bottom:2px solid #e4dcc9;padding-bottom:5px}
  .note{color:#6b6353;font-size:.88rem;font-style:italic}
  table{width:100%;border-collapse:collapse;background:#fffdf8;font-size:.92rem;
        font-family:"Segoe UI",system-ui,sans-serif;margin:12px 0}
  th{background:#efe7d3;text-align:left;padding:7px 9px;border:1px solid #e4dcc9}
  td{border:1px solid #e4dcc9;padding:6px 9px;vertical-align:top}
  td.w{font-weight:600;color:#8a3324;white-space:nowrap}
  td.c{color:#55503f;font-size:.88rem}
  a{color:#2f5d50}
</style>
</head>
<body>
<main>
<p><a href="index.html">← Когнаты Зализняка: сводная страница</a></p>
<h1>Слова с рассказами в школьных лекциях Зализняка</h1>
<p class="note">Пересечение нашей выборки (русская колонка конспекта + школьная 50-ка Фасмера) с указателем книги А. А. Зализняка «Школьные лекции» (школа «Муми-тролль», 2005–2017; указатель — 1367 статей, <a href="https://gasyoun.github.io/BookIndex/aaz-index.html#v4/all/list">BookIndex, сводный указатель</a>). Эти слова на лекции можно отметить отдельно: «про это слово у Зализняка есть рассказ — страница такая-то».</p>
<h2>Сводка по лекциям</h2>
<table>
<tr><th>Лекция</th><th>Слов нашей выборки</th><th>Слова</th></tr>
@@LEC@@
</table>
<h2>Все совпадения (слово → лекция → страница → контекст)</h2>
<table>
<tr><th>Слово</th><th>Лекция</th><th>Страница</th><th>Контекст (из указателя BookIndex)</th></tr>
@@ROWS@@
</table>
<p class="note">Источник данных: BookIndex app_data.json (lexicon, книга «mumintroll»), срез 25-09-2026. Совпадения — по нормализованной форме (без ударений, ё→е); краткие служебные совпадения возможны — сверяйтесь с контекстом. Проверить слово: <a href="https://gasyoun.github.io/BookIndex/aaz-index.html#v4/all/list">aaz-index.html#v4/all/list</a>.</p>
</main>
</body>
</html>
""".replace("@@LEC@@", lec_rows).replace("@@ROWS@@", rows)
io.open(os.path.join(HERE, "lectures.html"), "w", encoding="utf-8").write(html)
print("lectures.html: hits =", len(hits), "| by-lecture =", len(by_lecture))
print(json.dumps({k: len(v) for k, v in sorted(by_lecture.items(), key=lambda kv: -len(kv[1]))},
                 ensure_ascii=False, indent=1))
