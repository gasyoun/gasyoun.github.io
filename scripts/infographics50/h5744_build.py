#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Emit H5744 wave-b6: 8 infographics + catalog extension #59-#66.

Python 3.9+. Reuses the H3711 1080x1920 shell shape. Reads data/h5744.json
(written by h5744_probe.py — derive-don't-store).
"""
from __future__ import annotations

import html
import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
DATA = json.loads((HERE / "data" / "h5744.json").read_text(encoding="utf-8"))
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
    n = int(n)
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
--bar:#009B7D;--mono:'Noto Mono',monospace;
--font-display:'Comfortaa',sans-serif;--font-body:'Nunito',sans-serif}}
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


def write(slug: str, doc: str) -> Path:
    d = INF / slug
    d.mkdir(parents=True, exist_ok=True)
    p = d / "index.html"
    p.write_text(doc, encoding="utf-8")
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
            f'<div style="width:300px;font:700 15px var(--font-body)">{e(lab)}</div>'
            f'<div style="flex:1;height:14px;background:rgba(41,38,31,.08);border-radius:6px">'
            f'<div style="width:{w:.0f}px;height:100%;background:var(--bar);border-radius:6px"></div></div>'
            f'<div style="width:110px;text-align:right">{fmt(n)}</div></div>'
        )
    return "".join(out)


def page_kosha():
    k = DATA["kosha"]
    tiers = k["tiers"]
    items = [
        ("датасетов в манифесте", k["n_datasets"]),
        ("публичный тир", tiers.get("public", 0)),
        ("ограниченный тир", tiers.get("restricted", 0)),
        ("с DOI (Zenodo)", k["doi_count"]),
        ("суммарно строк данных", k["rows_sum"]),
    ]
    inner = (
        '<div class="hero">Реестр <b>kosha/data/manifest/datasets.json</b>: каждая запись — '
        "тир, лицензия, формат, строки. Публикуемое ядро имения одним кадром.</div>"
        + card_rows(items, y0=360, gap=170)
    )
    return shell(
        "kosha: 148 датасетов",
        "Санскритский архив Гасунса · свежая проба b6",
        "kosha: реестр датасетов",
        inner,
        foot("h5744_probe.py kosha"),
        "H5744 #59. kosha/data/manifest/datasets.json census. " + COUNTED,
    )


def page_vote():
    v = DATA["vote"]
    rows = [(p, n) for p, n in v["top_prefixes"] if n >= 3][:8]
    inner = (
        f'<div class="hero">Хаб голосований <b>vote/sheets</b>: <b>{fmt(v["n_sheets"])}</b> '
        "листов ревью/голосования. Топ префиксов имён — по темам решений.</div>"
        + bars(rows, y0=380, gap=150)
    )
    return shell(
        "Хаб голосований",
        "Санскритский архив Гасунса · свежая проба b6",
        f'{fmt(v["n_sheets"])} листов голосования',
        inner,
        foot("h5744_probe.py vote"),
        "H5744 #60. vote/sheets/**/*.html census. " + COUNTED,
    )


def page_handoffs():
    h = DATA["handoffs"]
    pools = h["pools"][:8]
    inner = (
        f'<div class="hero">Жизненный цикл хендоффов Uprava: <b>{fmt(h["total"])}</b> всего — '
        f"<b>{fmt(h['live'])}</b> в работе, <b>{fmt(h['archived'])}</b> в архиве. "
        "Столбики — пулы исполнителей по именам файлов.</div>"
        + bars(pools, y0=380, gap=150)
    )
    return shell(
        "Жизненный цикл хендоффов",
        "Санскритский архив Гасунса · свежая проба b6",
        f'{fmt(h["total"])} хендоффов за 4 месяца',
        inner,
        foot("h5744_probe.py handoffs"),
        "H5744 #61. Uprava/handoffs + archive file census. " + COUNTED,
    )


def page_rigveda():
    r = DATA["rigveda"]
    items = [
        ("строф Ригведы", r["verses"]),
        ("языков параллельно", r["langs"]),
        ("строк санскрита (sa)", r["classes"]["sa"]),
        ("строк русского (ru)", r["classes"]["ru"]),
        ("строк немецкого (de)", r["classes"]["de"]),
        ("строк английского (en)", r["classes"]["en"]),
    ]
    inner = (
        '<div class="hero">Четырёхъязычная Ригведа <b>RV/index.html</b>: каждая строфа — '
        "санскрит, русский, немецкий, английский. Полный параллельный корпус.</div>"
        + card_rows(items, y0=370, gap=180)
    )
    return shell(
        "Ригведа на четырёх языках",
        "Санскритский архив Гасунса · свежая проба b6",
        "10 552 строфы × 4 языка",
        inner,
        foot("h5744_probe.py rigveda"),
        "H5744 #62. RV/index.html verse-class census. " + COUNTED,
    )


def page_modules():
    m = DATA["modules"]
    items = [
        ("модулей заявлено", m["declared"]),
        ("в реестре", m["listed"]),
        ("пробовано на ящике", m["probed"]),
        ("без клона", m["no_clone"]),
        ("связей модуль→хендофф", m["module_to_handoff"]),
    ]
    inner = (
        '<div class="hero">Census разброса модулей <b>Uprava/data/module_spread_census_v2.json</b>: '
        "что заявлено, что реально пробовано, где растут сироты.</div>"
        + card_rows(items, y0=360, gap=170)
    )
    return shell(
        "Разброс модулей",
        "Санскритский архив Гасунса · свежая проба b6",
        "Реестр модулей имения",
        inner,
        foot("h5744_probe.py modules"),
        "H5744 #63. module_spread_census_v2.json universe census. " + COUNTED,
    )


def page_outages():
    o = DATA["outages"]
    rows = o["hosts"][:8]
    inner = (
        f'<div class="hero">Журнал простоев внешних источников <b>Uprava/SERVER_OUTAGES.md</b>: '
        f"<b>{o['rows']}</b> строк-инцидентов, <b>{len(o['hosts'])}</b> хостов. "
        "Сессии пропускают упавшие хосты по этому журналу.</div>"
        + bars(rows, y0=420, gap=150)
    )
    return shell(
        "Журнал простоев источников",
        "Санскритский архив Гасунса · свежая проба b6",
        f"{o['rows']} инцидентов внешних хостов",
        inner,
        foot("h5744_probe.py outages"),
        "H5744 #64. SERVER_OUTAGES.md row census. " + COUNTED,
    )


def page_reports():
    r = DATA["reports"]
    inner = (
        f'<div class="hero">Отчёты-доказательства <b>Uprava/reports/**</b>: <b>{fmt(r["total_files"])}</b> '
        "файлов — пробы, расследования, досье. Топ каталогов по числу файлов.</div>"
        + bars(r["top_dirs"][:8], y0=380, gap=150)
    )
    return shell(
        "Отчёты-доказательства",
        "Санскритский архив Гасунса · свежая проба b6",
        f'{fmt(r["total_files"])} файлов доказательств',
        inner,
        foot("h5744_probe.py reports"),
        "H5744 #65. Uprava/reports file census. " + COUNTED,
    )


def page_gtd():
    g = DATA["gtd"]
    mk = g["markers"]
    items = [
        ("строк-действий в очереди", g["table_rows"]),
        ("упоминаний @DO", mk["@DO"]),
        ("упоминаний @WAITING", mk["@WAITING"]),
        ("упоминаний @DECIDE (решает человек)", mk["@DECIDE"]),
    ]
    inner = (
        '<div class="hero">Текущая очередь <b>Uprava/GTD_NEXT_ACTIONS.md</b>: только счётчики. '
        "Решения @DECIDE остаются за человеком.</div>"
        + card_rows(items, y0=370, gap=190)
    )
    return shell(
        "Очередь GTD",
        "Санскритский архив Гасунса · свежая проба b6",
        "Что в очереди сейчас",
        inner,
        foot("h5744_probe.py gtd"),
        "H5744 #66. GTD_NEXT_ACTIONS.md aggregate counts only. " + COUNTED,
    )


PAGES = [
    ("kosha-manifest-2026-10-08", 59, page_kosha),
    ("vote-hub-sheets-2026-10-08", 60, page_vote),
    ("handoff-lifecycle-2026-10-08", 61, page_handoffs),
    ("rigveda-4langs-2026-10-08", 62, page_rigveda),
    ("module-spread-census-2026-10-08", 63, page_modules),
    ("outage-ledger-2026-10-08", 64, page_outages),
    ("evidence-reports-2026-10-08", 65, page_reports),
    ("gtd-queue-2026-10-08", 66, page_gtd),
]

ROW_SRC = {
    59: "kosha/data/manifest/datasets.json — тиры, DOI, строки. Проба: h5744_probe.py kosha.",
    60: "vote/sheets — листы ревью и голосований. Проба: h5744_probe.py vote.",
    61: "Uprava/handoffs + archive — жизненный цикл по пулам. Проба: h5744_probe.py handoffs.",
    62: "RV/index.html — строфы × 4 языка. Проба: h5744_probe.py rigveda.",
    63: "Uprava/data/module_spread_census_v2.json — universe реестра. Проба: h5744_probe.py modules.",
    64: "Uprava/SERVER_OUTAGES.md — инциденты внешних хостов. Проба: h5744_probe.py outages.",
    65: "Uprava/reports/** — файлы-доказательства. Проба: h5744_probe.py reports.",
    66: "Uprava/GTD_NEXT_ACTIONS.md — только агрегаты, без персоналий. Проба: h5744_probe.py gtd.",
}

ROW_TITLE = {
    59: "kosha: реестр датасетов",
    60: "Хаб голосований",
    61: "Жизненный цикл хендоффов",
    62: "Ригведа на четырёх языках",
    63: "Разброс модулей",
    64: "Журнал простоев источников",
    65: "Отчёты-доказательства",
    66: "Очередь GTD",
}


def extend_catalog() -> None:
    text = CATALOG.read_text(encoding="utf-8")
    if "№ 59" in text:
        print("catalog already has b6 extension")
        return
    if "нужны данные" in text:
        raise SystemExit("catalog still has blocked chips")
    lis = []
    for slug, num, _fn in PAGES:
        lis.append(
            f'      <li><span class="num">№ {num}</span><span class="t">{e(ROW_TITLE[num])}</span>'
            f'<span class="src">{e(ROW_SRC[num])}</span>'
            f'<div class="meta"><span class="chip done">готово</span> · '
            f'<a href="https://gasyoun.github.io/infographics/{slug}/index.html">смотреть</a></div></li>'
        )
    extension = (
        '\n  <div class="group"><h2>Свежие пробы имения · b6 (H5744)</h2>\n'
        '    <p class="note">Волна b6: census каталога после b5 — все 58 строк закрыты, '
        "остаток пуст, поэтому волна регистрирует восемь новых проб имения (№ 59–66) "
        "и сразу закрывает их. Только агрегаты из закоммиченных файлов, без персональных данных.</p>\n"
        "    <ol>\n" + "\n".join(lis) + "\n    </ol>\n  </div>\n"
    )
    marker = "  <footer>"
    if marker not in text:
        raise SystemExit("catalog footer not found")
    text = text.replace(marker, extension + marker, 1)
    b6_line = (
        "    Волна b6 (H5744): census каталога 08.10.2026 — 58/58 строк закрыто, остаток 0; "
        "добавлены № 59–66. Проба каталога: "
        "<span style='font-family:var(--mono)'>scripts/infographics50/catalog_probe.py --links</span>. · 08.10.2026 · Dr. Mārcis Gasūns\n"
    )
    text = text.replace("  </footer>", b6_line + "  </footer>", 1)
    CATALOG.write_text(text, encoding="utf-8")
    print("catalog extended with #59–#66 + b6 footer line")


def main() -> int:
    built = []
    for slug, num, fn in PAGES:
        write(slug, fn())
        built.append({"n": num, "slug": slug, "batch": "H5744-b6"})
    out = HERE / "data" / "h5744_built.json"
    out.write_text(
        json.dumps(built, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    extend_catalog()
    print("built", len(built), "pages")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
