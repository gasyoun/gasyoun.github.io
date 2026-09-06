#!/usr/bin/env python3
"""Render mastery/index.html — Карта мастерства ученика (H4262, stream S2 of H4260).

Input : mastery/data/mastery_snapshot.tsv (vendored from kosha, hash in manifest)
Output: mastery/index.html (derive-don't-store, idempotent — 2nd run byte-identical).
Status defaults to «не начато» everywhere: no learner data on the public hub;
the personal layer is built later, locally.
"""
import json
from pathlib import Path

HERE = Path(__file__).parent
ROOT = HERE.parent.parent
DATA = ROOT / "mastery" / "data"
SNAP = DATA / "mastery_snapshot.tsv"
MANI = DATA / "mastery_manifest.json"

KOSHA_BLOB = "https://github.com/gasyoun/kosha/blob/main/data/mastery/combined_schedule.json"
SPEC_BLOB = "https://github.com/gasyoun/kosha/blob/main/data/MASTERY_WEIGHTS_SPEC.md"
GEN_BLOB = "https://github.com/gasyoun/gasyoun.github.io/blob/master/scripts/campus/mastery_map_build.py"
MANI_BLOB = "https://github.com/gasyoun/gasyoun.github.io/blob/master/mastery/data/mastery_manifest.json"
CAMPUS = "https://gasyoun.github.io/campus/"
KARAOKE = "https://github.com/gasyoun/SanskritKaraoke/blob/main/progress.html"
INFO28 = "https://gasyoun.github.io/infographics/systema-srs-2026-08-29/index.html"
INFO36 = "https://gasyoun.github.io/infographics/student-road-2026-08-29/index.html"

FAMILIES = [
    ("sandhi", "Сандхи", "Благозвучные слияния на стыке слов — старт чтения."),
    ("samasa", "Самасы", "Сложные слова: от опознания к самостоятельному разбору."),
    ("morphology", "Морфология", "Падежные формы существительных — сетка 7134 рангов учебной программы."),
    ("vocab", "Частотная лексика", "Слова по частотным рангам DCS: от топ-500 вглубь."),
    ("thematic_vocab", "Тематическая лексика", "20 варг словаря-тезауруса: лес, люди, воины, небо…"),
]


SANDHI_ORDER = ["Уроки 1–3 · старт чтения", "Уроки 4–6", "Уроки 7–9"]
MORPH_ORDER = ["Урок 1", "Урок 2", "Урок 3"]
VOCAB_ORDER = ["Ранги 1–500", "Ранги 501–2000", "Ранги 2001+"]


def sandhi_stages(ax):
    n = int(ax)
    return SANDHI_ORDER[0] if n <= 3 else SANDHI_ORDER[1] if n <= 6 else SANDHI_ORDER[2]


SAMASA_ORDER = [
    ("identify", "Опознание (identify)"),
    ("member_side", "Член по стороне (member_side)"),
    ("member_recall", "Член по памяти (member_recall)"),
    ("split", "Разбор (split)"),
]


def morph_stages(ax):
    return "Урок " + str(int(ax))


def vocab_stages(ax):
    n = int(ax)
    return VOCAB_ORDER[0] if n <= 500 else VOCAB_ORDER[1] if n <= 2000 else VOCAB_ORDER[2]


def build():
    manifest = json.loads(MANI.read_text(encoding="utf-8"))
    agg = {}
    fam_totals = {}
    with open(SNAP, encoding="utf-8") as f:
        header = f.readline().rstrip("\n").split("\t")
        assert header == ["family", "id", "ease", "axis"], header
        for line in f:
            fam, _iid, ease, axis = line.rstrip("\n").split("\t")
            if fam == "sandhi":
                st = sandhi_stages(axis)
            elif fam == "samasa":
                st = dict(SAMASA_ORDER)[axis]
            elif fam == "morphology":
                st = morph_stages(axis)
            elif fam == "vocab":
                st = vocab_stages(axis)
            else:
                st = axis
            cell = agg.setdefault(fam, {}).setdefault(st, [0, 0.0])
            cell[0] += 1
            cell[1] += float(ease)
            fam_totals[fam] = fam_totals.get(fam, 0) + 1

    board = []
    for fid, title, blurb in FAMILIES:
        cells = agg[fid]
        if fid == "thematic_vocab":
            stage_items = sorted(cells.items(), key=lambda kv: (-kv[1][1] / kv[1][0], kv[0]))
        elif fid == "samasa":
            stage_items = [(n, cells[n]) for _c, n in SAMASA_ORDER if n in cells]
        elif fid == "sandhi":
            stage_items = [(t, cells[t]) for t in SANDHI_ORDER if t in cells]
        elif fid == "morphology":
            stage_items = [(t, cells[t]) for t in MORPH_ORDER if t in cells]
        else:
            stage_items = [(t, cells[t]) for t in VOCAB_ORDER if t in cells]
        stages = [
            {
                "title": t,
                "count": c[0],
                "ease": round(c[1] / c[0], 2),
                "status": "не начато",
            }
            for t, c in stage_items
        ]
        board.append({"id": fid, "title": title, "blurb": blurb, "total": fam_totals[fid], "stages": stages})

    g0 = manifest["gate0"]
    src = manifest["source"]
    short = {p: h[:16] for p, h in src["files"].items()}
    page = render(board, manifest, g0, src, short)
    dest = ROOT / "mastery" / "index.html"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(page, encoding="utf-8")
    print("wrote", dest, dest.stat().st_size, "bytes")


def render(board, manifest, g0, src, short):
    data_json = json.dumps(board, ensure_ascii=False)
    next_hint_json = json.dumps(
        {
            f["id"]: "Следующий шаг: " + f["stages"][0]["title"] + " — "
            + str(f["stages"][0]["count"]) + " упражнений, средняя лёгкость "
            + str(f["stages"][0]["ease"]) + ". Статус меняется в локальном личном слое."
            for f in board
        },
        ensure_ascii=False,
    )
    rows_html = []
    for fam in board:
        cells = "".join(
            f'<button class="cell" data-fam="{fam["id"]}" data-i="{i}">'
            f'<span class="st">{esc(s["title"])}</span>'
            f'<span class="meta">{s["count"]} упр. · лёгкость {s["ease"]}</span>'
            f'<span class="chip">{s["status"]}</span></button>'
            for i, s in enumerate(fam["stages"])
        )
        nxt = fam["stages"][0]["title"]
        rows_html.append(
            f'<section class="fam" id="{fam["id"]}"><h2><span class="n">{fam["total"]} упр.</span>{esc(fam["title"])}</h2>'
            f'<p class="intro">{esc(fam["blurb"])}</p><div class="grid">{cells}</div>'
            f'<p class="next">Следующий шаг: <strong>{esc(nxt)}</strong></p></section>'
        )
    hashes = "".join(f"<tr><td>{esc(p)}</td><td><code>{h}</code></td></tr>" for p, h in sorted(short.items()))
    cov = " · ".join(f"{k} {v}" for k, v in manifest["join_coverage"].items())
    return f"""<!doctype html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Карта мастерства ученика — 5 drill-семей</title>
<style>
:root{{--bg:#101418;--fg:#e8e4da;--mut:#9aa3ad;--acc:#d9a441;--line:#2a3138}}
*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--fg);font:16px/1.55 Georgia,'Times New Roman',serif}}
main{{max-width:960px;margin:0 auto;padding:3rem 1.25rem 5rem}}
h1{{font-size:2rem;margin:0 0 .25rem}}h1 span{{color:var(--acc)}}
.sub{{color:var(--mut);margin:0 0 1.5rem}}
.legend{{display:flex;gap:1.2rem;flex-wrap:wrap;color:var(--mut);font-size:.9rem;margin:0 0 2rem}}
.legend .chip{{margin-right:.35rem}}
section.fam h2{{font-size:1.25rem;margin:2.2rem 0 .4rem;padding-bottom:.4rem;border-bottom:1px solid var(--line)}}
section.fam h2 .n{{color:var(--acc);font-size:.85rem;font-family:Menlo,monospace;margin-right:.6rem}}
p.intro{{color:var(--mut);margin:0 0 .8rem}}
.grid{{display:flex;flex-wrap:wrap;gap:.6rem}}
button.cell{{appearance:none;text-align:left;background:#161c22;border:1px solid var(--line);border-radius:8px;color:var(--fg);padding:.6rem .8rem;min-width:11rem;font:inherit;cursor:pointer}}
button.cell:hover{{border-color:var(--acc)}}
button.cell.open{{border-color:var(--acc);background:#1b232b}}
.cell .st{{display:block;font-weight:bold}}
.cell .meta{{display:block;color:var(--mut);font-size:.82rem;margin:.15rem 0 .4rem}}
.chip{{display:inline-block;font-size:.75rem;padding:.1rem .5rem;border-radius:99px;border:1px solid var(--line);color:var(--mut)}}
.chip.todo{{color:var(--mut)}}.chip.doing{{color:var(--acc);border-color:var(--acc)}}.chip.done{{color:#7db77d;border-color:#7db77d}}
p.next{{color:var(--mut);margin:.6rem 0 0;font-size:.92rem}}p.next strong{{color:var(--acc)}}
#detail{{margin-top:1rem;padding:1rem;border:1px dashed var(--line);border-radius:8px;color:var(--mut);display:none}}
#detail.show{{display:block}}
details.trust{{margin-top:3rem;border-top:1px solid var(--line);padding-top:1rem}}
details.trust summary{{cursor:pointer;color:var(--acc)}}
table{{border-collapse:collapse;margin:.8rem 0;font-size:.85rem}}
td{{padding:.25rem .8rem .25rem 0;border-bottom:1px dashed var(--line);color:var(--mut)}}
code{{font-family:Menlo,monospace;font-size:.8rem;color:var(--fg)}}
footer{{margin-top:3rem;color:var(--mut);font-size:.85rem}}
a{{color:var(--fg);text-decoration:none;border-bottom:1px solid var(--acc)}}a:hover{{color:var(--acc)}}
footer a{{color:var(--mut);border-bottom-color:var(--line)}}
</style>
</head>
<body>
<main>
<h1>Карта <span>мастерства</span></h1>
<p class="sub">Пять drill-семей · {sum(f["total"] for f in board)} упражнений · данные kosha (H3742) · уровень → следующий шаг</p>
<p class="legend"><span class="chip done">освоено</span><span class="chip doing">в процессе</span><span class="chip todo">не начато</span><span>· все ячейки сейчас «не начато»: публичная карта без персональных данных, личный слой строится локально.</span></p>
{"".join(rows_html)}
<div id="detail" role="status"></div>
<details class="trust"><summary>GATE 0: проба данных и происхождение</summary>
<p>Вердикт: <strong>{esc(g0["verdict"])}</strong> · живая проба 06-09-2026 нашла
<a href="{KOSHA_BLOB}">data/mastery/combined_schedule.json</a> в gasyoun/kosha @ <code>{src["commit"][:12]}</code>
(утренняя проба handoff’а «не найден» — устарела). Fallback на публичные drill-наборы не понадобился.
ease 0..1 — <a href="{SPEC_BLOB}">seed-веса учебной программы (H3742)</a>, не данные учеников.
Join-покрытие осей: {cov}. Snapshot: {manifest["snapshot"]["rows"]} строк, sha256 <code>{manifest["snapshot"]["sha256"][:16]}</code> · <a href="{MANI_BLOB}">манифест</a>.</p>
<table><tr><td>файл kosha @ {src["commit"][:12]}</td><td>sha256 (16)</td></tr>{hashes}</table>
<p>Родня: <a href="{KARAOKE}">SanskritKaraoke progress.html</a> (паттерн прогресса) · статичные
<a href="{INFO28}">№28 «Дорога ученика»</a> и <a href="{INFO36}">№36 «От алфавита до Рамаяны»</a> — эта карта их живая версия ·
хаб: <a href="{CAMPUS}">Кампус наглядности, крыло «Учёба»</a>.</p>
</details>
<footer>Собрано <a href="{GEN_BLOB}">scripts/campus/mastery_map_build.py</a> из снапшота kosha · H4262 · 06-09-2026 · Dr. Mārcis Gasūns</footer>
</main>
<script type="application/json" id="board">{data_json}</script>
<script>
var BOARD = JSON.parse(document.getElementById("board").textContent);
var NEXT_HINT = {next_hint_json};
var detail = document.getElementById("detail");
var opened = null;
Array.prototype.forEach.call(document.querySelectorAll("button.cell"), function (b) {{
  b.addEventListener("click", function () {{
    if (opened) opened.classList.remove("open");
    if (opened === b) {{ opened = null; detail.classList.remove("show"); return; }}
    opened = b; b.classList.add("open");
    var fam = BOARD.filter(function (f) {{ return f.id === b.getAttribute("data-fam"); }})[0];
    var s = fam.stages[Number(b.getAttribute("data-i"))];
    detail.textContent = fam.title + " · " + s.title + ": " + s.count + " упражнений, средняя лёгкость " + s.ease + ", статус «" + s.status + "». " + NEXT_HINT[fam.id];
    detail.classList.add("show");
  }});
}});
</script>
</body>
</html>
"""


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


if __name__ == "__main__":
    build()
