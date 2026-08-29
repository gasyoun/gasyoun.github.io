#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Emit H3711's 10 infographics + catalog extension from data/h3711.json.

Python 3.9+. Reuses the H3705 1080x1920 shell.
"""
from __future__ import annotations

import html
import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
GH = Path(r"C:\Users\user\Documents\GitHub")
DATA = json.loads((HERE / "data" / "h3711.json").read_text(encoding="utf-8"))
COUNTED = DATA["counted"]
INF = ROOT / "infographics"
CATALOG = INF / "sanskrit-infographics-catalog" / "index.html"

FONTS = (
    "https://fonts.googleapis.com/css2?family=Comfortaa:wght@500;600;700"
    "&family=Nunito:wght@400;600;700;800&family=Noto+Mono&family="
    "Noto+Serif+Devanagari:wght@500;700&display=swap"
)


def e(s) -> str:
    return html.escape(str(s), quote=True)


def fmt(n) -> str:
    try:
        n = int(n)
    except (TypeError, ValueError):
        return str(n)
    s = str(abs(n))
    parts = []
    while s:
        parts.append(s[-3:])
        s = s[:-3]
    out = "\u202f".join(reversed(parts))
    return ("-" if n < 0 else "") + out


def shell(title, kicker, h1, inner, footer, script):
    return f"""<!doctype html>
<html lang="ru">
<head>
<meta charset="utf-8">
<title>{e(title)}</title>
<!-- {e(script)} -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="{FONTS}" rel="stylesheet">
<style>
*,*::before,*::after{{box-sizing:border-box;margin:0;padding:0}}
:root{{--bg:#F5EFE3;--ink:#29261F;--sub:rgba(41,38,31,.62);--accent:#C4552F;--card:#FFFFFF;
--neon:#6FE3C1;--bar:#009B7D;--blue:#4A55C8;--red:#D9503F;
--font-display:'Comfortaa',sans-serif;--font-body:'Nunito',sans-serif;
--dev:'Noto Serif Devanagari',serif;--mono:'Noto Mono',monospace}}
html,body{{background:var(--bg)}}
body{{width:1080px;font-family:var(--font-body);color:var(--ink)}}
.canvas{{position:relative;width:1080px;height:1920px;overflow:hidden;background:var(--bg)}}
.kicker{{position:absolute;left:64px;top:88px;font:700 13px/1.3 var(--font-body);
letter-spacing:.16em;text-transform:uppercase;color:var(--sub)}}
h1{{position:absolute;left:64px;top:118px;font-family:var(--font-display);
font-weight:700;font-size:46px;line-height:1.08;width:952px}}
.hero{{position:absolute;left:64px;top:230px;width:952px;font:600 16px/1.5 var(--font-body);color:var(--sub)}}
.hero b{{color:var(--accent);font-weight:800}}
.foot{{position:absolute;left:64px;top:1810px;width:952px;font:400 13px/1.5 var(--font-body);color:var(--sub)}}
.fade{{opacity:0;animation:fadein .45s ease-out forwards}}
@keyframes fadein{{to{{opacity:1}}}}
</style>
</head>
<body>
<div class="canvas">
  <div class="kicker">{e(kicker)}</div>
  <h1>{e(h1)}</h1>
  {inner}
  <div class="foot">{footer}</div>
</div>
</body>
</html>
"""


def write(slug: str, html_doc: str) -> Path:
    d = INF / slug
    d.mkdir(parents=True, exist_ok=True)
    p = d / "index.html"
    p.write_text(html_doc, encoding="utf-8")
    print("wrote", p.relative_to(ROOT))
    return p


def foot(script: str) -> str:
    return (
        f"Посчитано {COUNTED} · скрипт "
        f"<span style='font-family:var(--mono)'>scripts/infographics50/{e(script)}</span> "
        f"· Dr. Mārcis Gasūns"
    )


def card_rows(items, y0=360, gap=190):
    out = []
    for i, (lab, n) in enumerate(items):
        y = y0 + i * gap
        out.append(
            f'<div class="fade" style="position:absolute;left:64px;top:{y}px;width:952px;background:var(--card);'
            f'border-radius:14px;padding:18px 26px;display:flex;justify-content:space-between;'
            f'animation-delay:{0.08+i*0.05}s">'
            f'<div style="font:700 18px var(--font-body)">{e(lab)}</div>'
            f'<div style="font:800 32px var(--font-display);color:var(--accent)">{fmt(n)}</div></div>'
        )
    return "".join(out)


def bars(rows, y0=360, gap=78):
    mx = max((n for _, n in rows), default=1) or 1
    out = []
    for i, (lab, n) in enumerate(rows):
        y = y0 + i * gap
        w = 40 + 700 * n / mx
        out.append(
            f'<div class="fade" style="position:absolute;left:64px;top:{y}px;width:952px;display:flex;gap:12px;'
            f'align-items:center;animation-delay:{0.05+i*0.02}s">'
            f'<div style="width:280px;font:700 15px var(--font-body)">{e(lab)}</div>'
            f'<div style="flex:1;height:14px;background:rgba(41,38,31,.08);border-radius:6px">'
            f'<div style="width:{w:.0f}px;height:100%;background:var(--bar);border-radius:6px"></div></div>'
            f'<div style="width:90px;text-align:right">{fmt(n)}</div></div>'
        )
    return "".join(out)


def page_somadeva():
    s = DATA["somadeva"]
    mx = max(c["lines"] for c in s["chapters"]) or 1
    rows = []
    for i, c in enumerate(s["chapters"]):
        y = 360 + i * 78
        w = 40 + 700 * c["lines"] / mx
        rows.append(
            f'<div class="fade" style="position:absolute;left:64px;top:{y}px;width:952px;display:flex;gap:12px;'
            f'align-items:center;animation-delay:{0.05+i*0.02}s">'
            f'<div style="width:70px;font:700 14px var(--font-body)">гл. {i+1:02d}</div>'
            f'<div style="flex:1;height:14px;background:rgba(41,38,31,.08);border-radius:6px">'
            f'<div style="width:{w:.0f}px;height:100%;background:var(--bar);border-radius:6px"></div></div>'
            f'<div style="width:90px;text-align:right">{fmt(c["lines"])}</div></div>'
        )
    inner = (
        f'<div class="hero">Замена «Аштадхьяи как город»: полного 8-книжного текста сутр на ящике нет. '
        f"Параллельный Сомадева: <b>{s['san_files']}</b> глав санскрита, <b>{fmt(s['san_lines'])}</b> строк; "
        f"<b>{s['rus_files']}</b> глав перевода, <b>{fmt(s['rus_lines'])}</b> строк. "
        "Проба: somadeva/chapters_san + chapters_rus.</div>" + "".join(rows)
    )
    return shell(
        "Сомадева: океан историй",
        "Санскритский архив Гасунса · замена №18",
        "Kathāsaritsāgara, 18 глав",
        inner,
        foot("h3711_probe.py somadeva"),
        "H3711 #18 replacement. somadeva/chapters_san + chapters_rus. " + COUNTED,
    )


def page_ors():
    n = DATA["ors"]["numbers"]
    items = [
        ("личных диалогов", n["dialogs"]),
        ("уникальных учеников (агрегат)", n["students"]),
        ("пар вопрос → ответ", n["pairs"]),
        ("сообщений учеников", n["messages"]),
        ("оплата", n["pay"]),
        ("стоимость", n["price"]),
        ("запись", n["signup"]),
    ]
    inner = (
        '<div class="hero">Воронка из <b>ORS-FAQ/Tukan_stats.md</b>: только опубликованные агрегаты, '
        "без имён и без сырого экспорта. № 27 разблокирован этими цифрами.</div>"
        + card_rows(items, y0=340, gap=190)
    )
    return shell(
        "Воронка ORS",
        "Санскритский архив Гасунса · приложения",
        "Воронка ORS (агрегаты)",
        inner,
        foot("h3711_probe.py ors · ORS-FAQ/Tukan_stats.md"),
        "H3711 #27. ORS-FAQ/Tukan_stats.md public aggregates, no personal data. " + COUNTED,
    )


def page_prefaces():
    rows = DATA["prefaces"]["rows"]
    total = sum(r["files"] for r in rows)
    items = [(r["repo"], r["files"]) for r in rows]
    inner = (
        f'<div class="hero">Свежая идея H3711: семь репозиториев предисловий Cologne. '
        f"<b>{len(rows)}</b> клонов, <b>{fmt(total)}</b> файлов (рекурсивно). Не замена воронки ORS — "
        "ORS уже построен из Tukan_stats.md.</div>"
        + card_rows(items, y0=340, gap=180)
    )
    return shell(
        "Предисловия семи словарей",
        "Санскритский архив Гасунса · свежая проба",
        "7 репо предисловий",
        inner,
        foot("h3711_probe.py prefaces"),
        "H3711 fresh. File counts in prefaces_* clones. " + COUNTED,
    )


def page_countvowels():
    rows = [r for r in DATA["countvowels"]["rows"] if r["file"].endswith("-CVC-SLP1.txt")]
    total = sum(r["lines"] for r in rows)
    items = [(r["file"].replace("-CVC-SLP1.txt", ""), r["lines"]) for r in rows]
    inner = (
        f'<div class="hero">Свежая идея H3711: <b>CountVowels</b> CVC-SLP1, не замена Аштадхьяи. '
        f"<b>{len(rows)}</b> корпусов, <b>{fmt(total)}</b> строк. Путь: SanskritSpellCheck/CountVowels.</div>"
        + bars(items, y0=380, gap=200)
    )
    return shell(
        "Гласные эпоса (CVC)",
        "Санскритский архив Гасунса · свежая проба",
        "CountVowels: шесть корпусов",
        inner,
        foot("h3711_probe.py countvowels"),
        "H3711 fresh. SanskritSpellCheck/CountVowels/*-CVC-SLP1.txt. " + COUNTED,
    )


def page_bookindex():
    b = DATA["bookindex"]
    s = DATA["sorting"]
    items = [
        ("BookIndex markdown", b["md"]),
        ("BookIndex HTML", b["html"]),
        ("BookIndex JSON", b["json"]),
        ("SanskritSorting файлы", s["files"]),
    ]
    inner = (
        '<div class="hero">Индекс сканов: <b>BookIndex</b> + соседний <b>SanskritSorting</b>. '
        "Это же число стоит в каталоге как замена № 42 (дампа Википедии на ящике нет).</div>"
        + card_rows(items, y0=400, gap=280)
    )
    return shell(
        "BookIndex и SanskritSorting",
        "Санскритский архив Гасунса · свежая проба",
        "Индекс сканов",
        inner,
        foot("h3711_probe.py bookindex + sorting"),
        "H3711 fresh / catalog #42. BookIndex **/*.md + SanskritSorting files. " + COUNTED,
    )


def page_observatory():
    o = DATA["observatory"]
    reports = GH / "csl-observatory" / "reports"
    n_reports = sum(1 for p in reports.glob("*.md") if p.is_file()) if reports.exists() else 0
    items = [
        ("отчёты reports/*.md", n_reports),
        ("markdown во всём клоне", o["md"]),
        ("HTML", o["html"]),
        ("JSON", o["json"]),
        ("report-имена", o["reportish_md"]),
    ]
    inner = (
        '<div class="hero">Корпус отчётов <b>csl-observatory</b>: живой клон метрик Cologne. '
        "Считаем файлы, не содержимое личных issues.</div>"
        + card_rows(items, y0=380, gap=240)
    )
    return shell(
        "Обсерватория Cologne",
        "Санскритский архив Гасунса · свежая проба",
        "csl-observatory: корпус отчётов",
        inner,
        foot("h3711_probe.py observatory"),
        "H3711 fresh. csl-observatory md/html/json + reports/*.md. " + COUNTED,
    )


def page_visualdcs():
    v = DATA["visualdcs"]
    derived = GH / "VisualDCS" / "derived-data"
    dirs = sorted([p.name for p in derived.iterdir() if p.is_dir()]) if derived.exists() else []
    by = v["by_ext"]
    items = [
        ("папок derived-data", len(dirs)),
        ("CSV", by.get(".csv", 0)),
        ("TXT", by.get(".txt", 0)),
        ("JSON", by.get(".json", 0)),
        ("TSV", by.get(".tsv", 0)),
        ("всего data-файлов", v["data_files"]),
    ]
    inner = (
        '<div class="hero">Инвентарь <b>VisualDCS/derived-data</b>: производные таблицы корпуса DCS. '
        f"Верхние папки: {e(', '.join(dirs[:8]))}{'…' if len(dirs) > 8 else ''}.</div>"
        + card_rows(items, y0=380, gap=210)
    )
    return shell(
        "VisualDCS: derived-data",
        "Санскритский архив Гасунса · свежая проба",
        "Инвентарь производных DCS",
        inner,
        foot("h3711_probe.py visualdcs"),
        "H3711 fresh. VisualDCS derived-data inventory. " + COUNTED,
    )


def page_ovs():
    pairs = next(
        (h["lines"] for h in DATA["o_vs_O"]["hits"] if h["path"].endswith("o_vs_O2.txt") and "backup" not in h["path"] and "output" not in h["path"]),
        3884,
    )
    zenodo = next(
        (h["lines"] for h in DATA["o_vs_O"]["hits"] if "o_vs_O_evaluation_pairs.txt" in h["path"]),
        3884,
    )
    raw = next(
        (h["lines"] for h in DATA["o_vs_O"]["hits"] if h["path"].endswith("o_vs_O.txt") and "backup" not in h["path"] and "output" not in h["path"]),
        20185,
    )
    items = [
        ("пары o_vs_O2.txt (канон)", pairs),
        ("Zenodo evaluation pairs", zenodo),
        ("сырой o_vs_O.txt", raw),
    ]
    inner = (
        '<div class="hero">Орфографический дрейф: однобуквенные путаницы между словарями Cologne. '
        "Канон — <b>o_vs_O2.txt</b> (после фильтров), не HTML-дамп.</div>"
        + card_rows(items, y0=420, gap=320)
    )
    return shell(
        "o_vs_O: орфо-дрейф",
        "Санскритский архив Гасунса · свежая проба",
        "3 884 пары путаниц",
        inner,
        foot("h3711_probe.py o_vs_O"),
        "H3711 fresh. SanskritSpellCheck/o_vs_O/o_vs_O2.txt line count. " + COUNTED,
    )


def page_fuzzy():
    hits = [h for h in DATA["fuzzyalpha"]["hits"] if h["path"].endswith(".txt")]
    rows = []
    for h in hits:
        p = GH / h["path"].replace("\\", "/")
        n = 0
        if p.is_file():
            text = p.read_text(encoding="utf-8", errors="replace")
            n = text.count("------------------------------------------------------------------------")
        rows.append((Path(h["path"]).name, n or h["bytes"]))
    inner = (
        '<div class="hero">Близкие заголовки <b>fuzzyalpha</b>: INM / PUI / VEI. '
        "Столбик — число блоков (разделитель из дефисов) в txt, не HTML.</div>"
        + bars([(lab, int(n)) for lab, n in rows], y0=400, gap=180)
    )
    return shell(
        "fuzzyalpha: почти-дубли",
        "Санскритский архив Гасунса · свежая проба",
        "Близкие заголовки трёх словарей",
        inner,
        foot("h3711_probe.py fuzzyalpha"),
        "H3711 fresh. SanskritSpellCheck/fuzzyalpha/*.txt block counts. " + COUNTED,
    )


PAGES = [
    ("somadeva-ocean-2026-08-29", 18, page_somadeva, True),
    ("ors-funnel-2026-08-29", 27, page_ors, False),
    ("prefaces-seven-2026-08-29", 51, page_prefaces, False),
    ("observatory-reports-2026-08-29", 52, page_observatory, False),
    ("visualdcs-derived-2026-08-29", 53, page_visualdcs, False),
    ("countvowels-cvc-2026-08-29", 54, page_countvowels, False),
    ("o-vs-o-pairs-2026-08-29", 55, page_ovs, False),
    ("fuzzyalpha-dupes-2026-08-29", 56, page_fuzzy, False),
    ("bookindex-scans-2026-08-29", 42, page_bookindex, True),
    ("sanskrit-sorting-2026-08-29", 58, lambda: page_sorting(), False),
]


def page_sorting():
    s = DATA["sorting"]
    inner = (
        f'<div class="hero">Клон <b>SanskritSorting</b>: сортировки и конвертеры сканов. '
        f"<b>{fmt(s['files'])}</b> файлов в дереве. Сосед BookIndex — отдельный плакат.</div>"
        f'<div class="fade" style="position:absolute;left:64px;top:560px;width:952px;background:var(--card);'
        f'border-radius:20px;padding:48px;text-align:center">'
        f'<div style="font:800 88px var(--font-display)">{fmt(s["files"])}</div>'
        f"<div>файлов в SanskritSorting</div></div>"
    )
    return shell(
        "SanskritSorting",
        "Санскритский архив Гасунса · свежая проба",
        "Сортировки сканов",
        inner,
        foot("h3711_probe.py sorting"),
        "H3711 fresh. SanskritSorting file census. " + COUNTED,
    )


EXTENSION = """
  <div class="group"><h2>Свежие пробы имения (H3711)</h2>
    <p class="note">Восемь идей из опроса имения. № 18 заменён Сомадевой (полного текста сутр нет). № 27 разблокирован агрегатами Tukan_stats.md, без персональных данных.</p>
    <ol>
      <li><span class="num">№ 51</span><span class="t">Семь предисловий</span><span class="src">prefaces_ieg/lan/pe/pgn/ae/gst/snp — файлы в семи клонах. Проба: scripts/infographics50/h3711_probe.py prefaces.</span><div class="meta"><span class="chip done">готово</span> · <a href="https://gasyoun.github.io/infographics/prefaces-seven-2026-08-29/index.html">смотреть</a></div></li>
      <li><span class="num">№ 52</span><span class="t">Корпус отчётов обсерватории</span><span class="src">csl-observatory: markdown, HTML, JSON и reports/*.md. Проба: h3711_probe.py observatory.</span><div class="meta"><span class="chip done">готово</span> · <a href="https://gasyoun.github.io/infographics/observatory-reports-2026-08-29/index.html">смотреть</a></div></li>
      <li><span class="num">№ 53</span><span class="t">VisualDCS derived-data</span><span class="src">Инвентарь производных таблиц корпуса DCS. Проба: h3711_probe.py visualdcs.</span><div class="meta"><span class="chip done">готово</span> · <a href="https://gasyoun.github.io/infographics/visualdcs-derived-2026-08-29/index.html">смотреть</a></div></li>
      <li><span class="num">№ 54</span><span class="t">CountVowels CVC</span><span class="src">Шесть корпусов *-CVC-SLP1.txt в SanskritSpellCheck/CountVowels. Проба: h3711_probe.py countvowels.</span><div class="meta"><span class="chip done">готово</span> · <a href="https://gasyoun.github.io/infographics/countvowels-cvc-2026-08-29/index.html">смотреть</a></div></li>
      <li><span class="num">№ 55</span><span class="t">o_vs_O орфо-дрейф</span><span class="src">3 884 канонические пары SanskritSpellCheck/o_vs_O/o_vs_O2.txt. Проба: h3711_probe.py o_vs_O.</span><div class="meta"><span class="chip done">готово</span> · <a href="https://gasyoun.github.io/infographics/o-vs-o-pairs-2026-08-29/index.html">смотреть</a></div></li>
      <li><span class="num">№ 56</span><span class="t">fuzzyalpha почти-дубли</span><span class="src">Близкие заголовки INM/PUI/VEI. Проба: h3711_probe.py fuzzyalpha.</span><div class="meta"><span class="chip done">готово</span> · <a href="https://gasyoun.github.io/infographics/fuzzyalpha-dupes-2026-08-29/index.html">смотреть</a></div></li>
      <li><span class="num">№ 57</span><span class="t">BookIndex сканы</span><span class="src">Тот же индекс, что замена № 42. Проба: h3711_probe.py bookindex.</span><div class="meta"><span class="chip done">готово</span> · <a href="https://gasyoun.github.io/infographics/bookindex-scans-2026-08-29/index.html">смотреть</a></div></li>
      <li><span class="num">№ 58</span><span class="t">SanskritSorting</span><span class="src">Файлы клона сортировок сканов. Проба: h3711_probe.py sorting.</span><div class="meta"><span class="chip done">готово</span> · <a href="https://gasyoun.github.io/infographics/sanskrit-sorting-2026-08-29/index.html">смотреть</a></div></li>
    </ol>
  </div>
"""


def extend_catalog() -> None:
    text = CATALOG.read_text(encoding="utf-8")
    if "№ 51" in text:
        print("catalog already has H3711 extension")
        return
    if "нужны данные" in text:
        raise SystemExit("catalog still has blocked chips")
    marker = "  <footer>"
    if marker not in text:
        raise SystemExit("catalog footer not found")
    CATALOG.write_text(text.replace(marker, EXTENSION + "\n" + marker, 1), encoding="utf-8")
    print("catalog extended with #51–#58")


def main() -> int:
    built = []
    for slug, num, fn, replaced in PAGES:
        write(slug, fn())
        built.append({"n": num, "slug": slug, "replaced": replaced, "batch": "H3711"})
    out = HERE / "data" / "h3711_built.json"
    out.write_text(json.dumps(built, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    extend_catalog()
    print("built", len(built), "pages")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
