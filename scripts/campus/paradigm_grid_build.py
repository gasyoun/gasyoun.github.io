#!/usr/bin/env python3
"""Render infographics/paradigm-a-stems-2026-09-06/index.html (H4263, stream S3).

Input : vendored snapshot of DCS nominal paradigm class 'a' (Masc+Neut),
        hash recorded in paradigm_manifest.json.
Output: one static case x number grid page. Idempotent (2nd run byte-identical).
"""
import json
from pathlib import Path

HERE = Path(__file__).parent
PAGE_DIR = HERE.parent.parent / "infographics" / "paradigm-a-stems-2026-09-06"
SNAP = PAGE_DIR / "paradigm_a_snapshot.json"
MANI = PAGE_DIR / "paradigm_manifest.json"

SRC_BLOB = "https://github.com/gasyoun/VisualDCS/blob/main/visual/paradigm_nominal.json"
REG_BLOB = "https://github.com/gasyoun/kosha/blob/main/data/manifest/datasets.json"
GEN_BLOB = "https://github.com/gasyoun/gasyoun.github.io/blob/master/scripts/campus/paradigm_grid_build.py"

CASES_RU = {
    "Nom": "им.", "Acc": "вин.", "Ins": "тв.", "Dat": "дат.",
    "Abl": "отл.", "Gen": "род.", "Loc": "мес.", "Voc": "зват.",
}
NUMBERS_RU = {"Sing": "ед.", "Dual": "дв.", "Plur": "мн."}
GENDERS_RU = {"Masc": "мужской род", "Neut": "средний род"}


def esc(s):
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def build():
    snap = json.loads(SNAP.read_text(encoding="utf-8"))
    mani = json.loads(MANI.read_text(encoding="utf-8"))
    cases, numbers = snap["cases"], snap["numbers"]
    top = snap.get("topLemmas") or []

    grids_html = []
    for g in ("Masc", "Neut"):
        gd = snap["genders"][g]
        cells = gd["cells"]
        rows = []
        rows.append("<tr><th></th>" + "".join(
            f'<th>{NUMBERS_RU[n]}</th>' for n in numbers) + "</tr>")
        for c in cases:
            row = [f'<th scope="row">{CASES_RU[c]}</th>']
            for n in numbers:
                cell = cells.get(f"{c}.{n}")
                if not cell or not cell.get("n"):
                    row.append('<td class="empty">—</td>')
                    continue
                forms = "".join(
                    f'<span class="f">{esc(f[1])}<i>{f[0]}</i></span>'
                    for f in (cell.get("forms") or [])[:3]
                )
                end = "".join(esc(e) for e in (cell.get("endings") or [])[:2])
                row.append(
                    f'<td title="{cell.get("n")} токенов, {cell.get("lemmas")} лемм">{forms}'
                    f'<span class="meta">n={cell.get("n")}{(" · " + end) if end else ""}</span></td>'
                )
            rows.append("<tr>" + "".join(row) + "</tr>")
        att = gd.get("cellsAttested", "?")
        seg = gd.get("segmentablePct", "?")
        grids_html.append(
            f'<h2><span class="n">{g}</span>{GENDERS_RU[g]}</h2>'
            f'<p class="intro">аттестованных клеток: {att} из 24 · сегментируемость: {seg}</p>'
            f'<table class="grid">{"".join(rows)}</table>'
        )

    lem = ", ".join(f"{esc(l[1])} ({l[2]}) — {l[0]}" for l in top[:6])
    page = f"""<!doctype html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Парадигма a-основ: deva в корпусе DCS</title>
<style>
:root{{--bg:#101418;--fg:#e8e4da;--mut:#9aa3ad;--acc:#d9a441;--line:#2a3138}}
*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--fg);font:16px/1.55 Georgia,'Times New Roman',serif}}
main{{max-width:960px;margin:0 auto;padding:3rem 1.25rem 5rem}}
h1{{font-size:1.9rem;margin:0 0 .25rem}}h1 span{{color:var(--acc)}}
.sub{{color:var(--mut);margin:0 0 1.5rem}}
h2{{font-size:1.2rem;margin:2.2rem 0 .4rem;padding-bottom:.4rem;border-bottom:1px solid var(--line)}}
h2 .n{{color:var(--acc);font-size:.85rem;font-family:Menlo,monospace;margin-right:.6rem}}
p.intro{{color:var(--mut);margin:0 0 .8rem;font-size:.92rem}}
table.grid{{border-collapse:collapse;width:100%;font-size:.85rem}}
table.grid th{{color:var(--acc);font-weight:normal;font-family:Menlo,monospace;font-size:.78rem;padding:.4rem .5rem;border-bottom:1px solid var(--line);text-align:left}}
table.grid td{{vertical-align:top;padding:.45rem .5rem;border-bottom:1px dashed var(--line)}}
td .f{{display:inline-block;margin:0 .6rem .25rem 0}}td .f i{{color:var(--mut);font-style:normal;font-size:.72rem;margin-left:.25rem}}
td .meta{{display:block;color:var(--mut);font-size:.72rem}}
td.empty{{color:var(--line)}}
details{{margin-top:2.5rem;border-top:1px solid var(--line);padding-top:1rem}}summary{{cursor:pointer;color:var(--acc)}}
p.note{{color:var(--mut);font-size:.85rem}}
code{{font-family:Menlo,monospace;font-size:.78rem}}
a{{color:var(--fg);text-decoration:none;border-bottom:1px solid var(--acc)}}a:hover{{color:var(--acc)}}
footer{{margin-top:3rem;color:var(--mut);font-size:.85rem}}footer a{{color:var(--mut);border-bottom-color:var(--line)}}
</style>
</head>
<body>
<main>
<h1>Парадигма <span>a-основ</span>: deva в корпусе DCS</h1>
<p class="sub">Самый частотный класс имён (основа на -a, образец deva «бог»; топ-леммы: {lem}) · падеж × число · формы аттестованы корпусом DCS</p>
{"".join(grids_html)}
<details><summary>Источник данных и метод</summary>
<p class="note">Данные: <a href="{SRC_BLOB}">VisualDCS visual/paradigm_nominal.json</a>
(датасет <code>dcs-nominal-paradigm-grid</code>, реестр <a href="{REG_BLOB}">kosha datasets.json</a>;
билдер <code>gen_paradigm_nominal.py</code>, H1472) поверх корпуса DCS, релиз {esc(str(snap.get("corpusRelease")))}.
В снапшоте страницы: <code>{mani["snapshot"]["sha256"][:16]}</code> от исходника
<code>{mani["source"]["commit"][:12]}</code>. Лицензии: DCS CC BY 4.0, производное — CC BY-SA 4.0.</p>
<p class="note">⚠️ Класс основы — эвристика по цитатной форме леммы: DCS не размечает типы склонения.
В клетке: топ-аттестованные формы без сандхи с частотами, n — токенов, под курсором — лемм.
Полное описание эвристики: {esc(snap.get("note") or "")[:280]}…</p>
</details>
<footer>Собрано <a href="{GEN_BLOB}">scripts/campus/paradigm_grid_build.py</a> из снапшота dcs-nominal-paradigm-grid · H4263 · 06-09-2026 · Dr. Mārcis Gasūns</footer>
</main>
</body>
</html>
"""
    out = PAGE_DIR / "index.html"
    out.write_text(page, encoding="utf-8")
    print("wrote", out, out.stat().st_size, "bytes")


if __name__ == "__main__":
    build()
