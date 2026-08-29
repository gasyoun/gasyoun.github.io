#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Emit the remaining 40 infographic HTML pages from infographics50.json."""
from __future__ import annotations

import html
import json
import math
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
DATA = json.loads((HERE / "data" / "infographics50.json").read_text(encoding="utf-8"))
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


def shell(title, kicker, h1, inner, footer, script, dark=False):
    bg = "#101216" if dark else "#F5EFE3"
    ink = "#F2F5F9" if dark else "#29261F"
    sub = "#9AA6B5" if dark else "rgba(41,38,31,.62)"
    accent = "#FF8A70" if dark else "#C4552F"
    card = "#1A1F26" if dark else "#FFFFFF"
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
:root{{--bg:{bg};--ink:{ink};--sub:{sub};--accent:{accent};--card:{card};
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
.chip{{display:inline-block;padding:3px 10px;border-radius:14px;font:700 12px var(--font-body);background:var(--accent);color:#fff}}
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


def page_anatomy():
    a = DATA["mw"]["anatomy_kfzRa"]
    layers = [
        ("лемма k1", a.get("deva", "कृष्ण") + " · " + a.get("iast", "kṛṣṇa"), "SLP1 kfzRa, первое омонимичное гнездо"),
        ("строки статьи", fmt(a.get("lines")), "включая <L>…<LEND>"),
        ("знаков", fmt(a.get("chars")), "сырой Cologne-текст"),
        ("<s> санскрит", fmt(a.get("n_s_tags")), "формы в SLP1"),
        ("<lex> грамматика", fmt(a.get("n_lex_tags")), "род / часть речи"),
        ("<ls> цитаты", fmt(a.get("n_ls_tags")), "источники в скобках"),
        ("¦ смыслы", fmt(a.get("n_senses")), "разделители значений"),
    ]
    cards = []
    for i, (t, n, s) in enumerate(layers):
        top = 330 + i * 200
        cards.append(
            f'<div class="fade" style="position:absolute;left:64px;top:{top}px;width:952px;'
            f'background:var(--card);border-radius:14px;padding:22px 28px;animation-delay:{0.2+i*0.07}s">'
            f'<div style="font:700 13px var(--font-body);color:var(--accent);letter-spacing:.08em">{e(t)}</div>'
            f'<div style="font:700 36px var(--font-display);margin-top:4px">{e(n)}</div>'
            f'<div style="color:var(--sub);margin-top:4px">{e(s)}</div></div>'
        )
    inner = (
        '<div class="hero">Одна статья MW — <b>kṛṣṇa</b> (омоним 1). Слои прочитаны из разметки '
        f'csl-orig/v02/mw/mw.txt, не нарисованы на глаз. Всего в MW <b>{fmt(DATA["mw"]["entries"])}</b> '
        f'статей · <b>{fmt(DATA["mw"]["unique_k1"])}</b> уникальных k1.</div>'
        + "".join(cards[:6])
    )
    if a.get("raw"):
        raw_lines = "".join(
            f'<div style="white-space:pre-wrap">{e(ln)}</div>'
            for ln in a["raw"].split("\n")
        )
        inner += (
            '<div class="fade" style="position:absolute;left:64px;top:1520px;width:952px;'
            'background:var(--card);border-radius:14px;padding:20px 26px;animation-delay:.7s">'
            '<div style="font:700 13px var(--font-body);color:var(--accent);letter-spacing:.08em">'
            'сырая статья, как лежит в mw.txt</div>'
            f'<div style="font:12.5px/1.55 var(--mono);color:var(--sub);margin-top:8px">{raw_lines}</div></div>'
        )
    return shell(
        "Анатомия одной статьи MW",
        "Санскритский архив Гасунса · словари",
        "Анатомия статьи MW",
        inner,
        foot("probe.py → mw.anatomy_kfzRa"),
        "Data: csl-orig/v02/mw/mw.txt first <h>1 k1=kfzRa block; tag counts. " + COUNTED,
    )


def page_letters():
    rows = DATA["mw"]["letters"][:33]
    mx = max(r["n"] for r in rows) or 1
    bars = []
    for i, r in enumerate(rows):
        x = 64 + (i % 11) * 86
        y = 340 + (i // 11) * 460
        h = 8 + 280 * r["n"] / mx
        bars.append(
            f'<div class="fade" style="position:absolute;left:{x}px;top:{y}px;width:76px;animation-delay:{0.15+i*0.03}s">'
            f'<div style="height:300px;display:flex;align-items:flex-end">'
            f'<div style="width:100%;height:{h:.1f}px;background:var(--bar);border-radius:8px 8px 0 0"></div></div>'
            f'<div style="font:700 22px var(--dev);text-align:center;margin-top:6px">{e(r["deva"])}</div>'
            f'<div style="font:700 12px var(--font-body);text-align:center;color:var(--sub)">{fmt(r["n"])}</div>'
            f'</div>'
        )
    inner = (
        f'<div class="hero">Первая буква SLP1-заголовка k1 в Monier-Williams. '
        f'<b>{fmt(DATA["mw"]["entries"])}</b> статей, <b>{len(DATA["mw"]["letters"])}</b> разных начал. '
        f'Высота — линейно по числу статей, не логарифм.</div>' + "".join(bars)
    )
    return shell(
        "MW по буквам",
        "Санскритский архив Гасунса · словари",
        "Словари по буквам",
        inner,
        foot("probe.py → mw.letters"),
        "Data: first char of <k1> in csl-orig/v02/mw/mw.txt. " + COUNTED,
    )


def page_timeline():
    rows = [r for r in DATA["dicts"]["rows"] if r.get("print_date")]
    def year0(row):
        m = re.search(r"(1[6-9]\d{2}|20\d{2})", row.get("print_date") or "")
        return int(m.group(1)) if m else 9999
    rows = sorted(rows, key=year0)
    items = []
    for i, r in enumerate(rows[:18]):
        y = 330 + i * 80
        items.append(
            f'<div class="fade" style="position:absolute;left:64px;top:{y}px;width:952px;display:flex;gap:18px;'
            f'align-items:baseline;animation-delay:{0.1+i*0.03}s">'
            f'<div style="width:160px;font:700 22px var(--font-display);color:var(--accent)">{e(r["print_date"])}</div>'
            f'<div style="width:90px;font:800 16px var(--font-body)">{e(r["code"])}</div>'
            f'<div style="flex:1;font:600 15px var(--font-body);color:var(--sub)">{e((r["title"] or "—")[:72])}</div>'
            f'<div style="width:120px;text-align:right;font:700 16px var(--font-display)">{fmt(r["entries"])}</div>'
            f'</div>'
        )
    inner = (
        f'<div class="hero">Годы печати из <b>*header.xml</b> Cologne (элемент date в title type=short). '
        f'Первые 18 из {len(rows)} словарей с датой. Не вымышлено.</div>' + "".join(items)
    )
    return shell(
        "Хронология изданий",
        "Санскритский архив Гасунса · словари",
        "Хронология изданий",
        inner,
        foot("probe.py → dicts.rows.print_date"),
        "Data: csl-orig/v02/*/ *header.xml <date>. " + COUNTED,
    )


def page_five():
    codes = {
        "Böhtlingk": ["pw", "pwg", "pwkvn"],
        "Roth": ["pwg"],
        "Monier-Williams": ["mw", "mw72", "mwe"],
        "Apte": ["ap", "ap90"],
        "Cappeller": ["ccs", "cae"],
    }
    by = {r["code"]: r for r in DATA["dicts"]["rows"]}
    cards = []
    for i, (name, ds) in enumerate(codes.items()):
        n = sum(by[c]["entries"] for c in ds if c in by)
        y = 330 + i * 280
        chips = " · ".join(ds)
        cards.append(
            f'<div class="fade" style="position:absolute;left:64px;top:{y}px;width:952px;background:var(--card);'
            f'border-radius:16px;padding:28px 32px;animation-delay:{0.15+i*0.08}s">'
            f'<div style="font:700 15px var(--font-body);color:var(--accent)">{e(name)}</div>'
            f'<div style="font:700 48px var(--font-display);margin-top:6px">{fmt(n)}</div>'
            f'<div style="color:var(--sub);margin-top:6px">статьи в клоне csl-orig: {e(chips)}</div></div>'
        )
    inner = (
        '<div class="hero">Пять имён — сумма <b>&lt;L&gt;</b> по их словарям в csl-orig/v02. '
        "Roth считается по PWG (совместное издание с Бётлингком), без двойного сложения в «пятёрке имён» ниже — "
        "карточка Roth отдельно показывает тот же PWG.</div>" + "".join(cards)
    )
    return shell(
        "Пятеро лексикографов",
        "Санскритский архив Гасунса · словари",
        "Пятеро лексикографов",
        inner,
        foot("probe.py → dicts.rows"),
        "Data: csl-orig/v02 <L> counts grouped by lexicographer. " + COUNTED,
    )


def page_genealogy():
    chain = [
        ("PWG", "1855–1875", "pwg"),
        ("PW", "1879–1889", "pw"),
        ("MW", "1899", "mw"),
        ("Apte", "1957–59 rev.", "ap"),
        ("MW 1872", "предшественник MW 1899", "mw72"),
    ]
    by = {r["code"]: r for r in DATA["dicts"]["rows"]}
    CARD_H = 202
    xs = [120, 360]
    arrows = []
    tops = []
    for i, (lab, when, code) in enumerate(chain):
        y0 = 340 + i * 270
        tops.append((xs[i % 2] + 300, y0, y0 + CARD_H))
    for i in range(3):  # PWG→PW→MW→Apte; MW 1872 stays a side note
        x1, _, yb = tops[i]
        x2, yt, _ = tops[i + 1]
        arrows.append(
            f'<line x1="{x1}" y1="{yb + 4}" x2="{x2}" y2="{yt - 8}" '
            f'stroke="#C4552F" stroke-opacity=".55" stroke-width="2.5" marker-end="url(#ahg)"/>'
        )
    svg = (
        '<svg style="position:absolute;left:0;top:0;pointer-events:none" width="1080" height="1920">'
        '<defs><marker id="ahg" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" '
        'orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#C4552F" opacity=".55"/></marker></defs>'
        + "".join(arrows) + "</svg>"
    )
    blocks = []
    for i, (lab, when, code) in enumerate(chain):
        n = by.get(code, {}).get("entries", 0)
        y = 340 + i * 270
        blocks.append(
            f'<div class="fade" style="position:absolute;left:{120 if i%2==0 else 360}px;top:{y}px;width:600px;'
            f'background:var(--card);border-radius:18px;padding:26px 30px;animation-delay:{0.15+i*0.1}s">'
            f'<div style="font:700 28px var(--font-display)">{e(lab)}</div>'
            f'<div style="color:var(--sub);margin-top:4px">{e(when)}</div>'
            f'<div style="font:800 40px var(--font-display);margin-top:8px;color:var(--accent)">{fmt(n)}</div>'
            f'<div style="color:var(--sub)">статей · {e(code)}</div></div>'
        )
    inner = (
        '<div class="hero">Не дерево «влияния» из головы: пять узлов с <b>датой из header.xml</b> '
        "и числом статей из того же клона. Стрелка наследования — историческая подпись серии, "
        "числа проверяемы.</div>"
        + svg
        + "".join(blocks)
    )
    return shell(
        "Генеалогия словарей",
        "Санскритский архив Гасунса · словари",
        "Генеалогия словарей",
        inner,
        foot("probe.py → dicts.rows"),
        "Data: csl-orig headers + <L> counts. " + COUNTED,
    )


def page_encodings():
    w = DATA["mw"]["word_encodings"]
    rows = [
        ("Devanagari", w["deva"], "человеческое письмо"),
        ("IAST", w["iast"], "sanskrit-util.from_slp1"),
        ("SLP1", w["slp1"], "машинный ключ Cologne"),
        ("Harvard-Kyoto", w["hk"], "таблица SLP1→HK в probe.py"),
        ("WX", w["wx"], "таблица SLP1→WX в probe.py"),
    ]
    cards = []
    for i, (name, val, note) in enumerate(rows):
        y = 340 + i * 270
        cards.append(
            f'<div class="fade" style="position:absolute;left:64px;top:{y}px;width:952px;background:var(--card);'
            f'border-radius:16px;padding:24px 30px;animation-delay:{0.12+i*0.08}s">'
            f'<div style="font:700 13px var(--font-body);color:var(--accent);letter-spacing:.1em">{e(name)}</div>'
            f'<div style="font:700 42px var(--dev);margin-top:8px">{e(val)}</div>'
            f'<div style="color:var(--sub);margin-top:6px">{e(note)}</div></div>'
        )
    inner = (
        '<div class="hero">Одно слово — <b>kṛṣṇa</b> — в пяти кодировках. Devanagari через '
        "<b>sanskrit-util.slp1_to_devanagari</b> (не ручной набор).</div>" + "".join(cards)
    )
    return shell(
        "Пять кодировок",
        "Санскритский архив Гасунса · слова",
        "Одно слово — пять кодировок",
        inner,
        foot("probe.py → mw.word_encodings"),
        "Data: SLP1 kfzRa via sanskrit-util + HK/WX tables. " + COUNTED,
        dark=True,
    )


def page_snowflake():
    forms = DATA["gam"]["present_para_gacC"]
    cx, cy, R = 540, 920, 400
    slots = ["3 sg", "3 du", "3 pl", "2 sg", "2 du", "2 pl", "1 sg", "1 du", "1 pl"]
    n = max(len(forms), 1)
    rays = [
        f'<svg style="position:absolute;left:0;top:0;pointer-events:none" width="1080" height="1920">'
        f'<defs><marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" '
        f'orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#FF8A70" opacity=".55"/></marker></defs>'
    ]
    nodes = []
    for i, f in enumerate(forms):
        ang = -math.pi / 2 + i * 2 * math.pi / n
        nx = cx + R * math.cos(ang)
        ny = cy + R * math.sin(ang)
        rays.append(
            f'<line x1="{cx}" y1="{cy}" x2="{nx:.0f}" y2="{ny + 6:.0f}" '
            f'stroke="#FF8A70" stroke-opacity=".38" stroke-width="2.5" marker-end="url(#ah)"/>'
        )
        nodes.append(
            f'<div class="fade" style="position:absolute;left:{nx - 90:.0f}px;top:{ny - 46:.0f}px;width:180px;'
            f'text-align:center;animation-delay:{0.2+i*0.05}s">'
            f'<div style="font:700 12px var(--font-body);color:var(--neon);letter-spacing:.08em">{e(slots[i])}</div>'
            f'<div style="font:700 28px var(--dev);margin-top:2px">{e(f["deva"])}</div>'
            f'<div style="font:600 13px var(--font-body);font-style:italic;color:var(--sub)">{e(f["iast"])}</div>'
            f'</div>'
        )
    rays.append("</svg>")
    inner = (
        f'<div class="hero">Корень <b>√gam</b> «идти», настоящее время, parasmaipada, основа gacch- — '
        f'<b>{len(forms)}</b> форм из MWinflect (20 строк gam в calc_tables.txt). '
        "Луч — форма; 3×3 лица и числа подписаны на лучах.</div>"
        + "".join(rays)
        + f'<div style="position:absolute;left:430px;top:{cy - 48}px;width:220px;text-align:center">'
        f'<div style="font:700 40px var(--dev)">√गम्</div>'
        f'<div style="font:italic 600 14px var(--font-body);color:var(--sub)">gam — корень</div></div>'
        + '<div class="fade" style="position:absolute;left:64px;top:1560px;width:952px;background:var(--card);'
        'border-radius:14px;padding:18px 26px;animation-delay:.8s">'
        '<div style="font:600 14.5px/1.55 var(--font-body);color:var(--sub)">Порядок лучей — как хранит '
        'MWinflect: <b style="color:var(--ink)">3-е → 2-е → 1-е лицо</b>, в каждом sg · du · pl. '
        'Каждая форма — одна строка таблицы verbs calc_tables.txt, модель 1,a,pre, основа gacC.</div></div>'
        + "".join(nodes)
    )
    return shell(
        "Морфологическая снежинка",
        "Санскритский архив Гасунса · формы",
        "Снежинка √gam",
        inner,
        foot("probe.py → gam.present_para_gacC"),
        "Data: MWinflect/verbs/.../calc_tables.txt 1,a,pre gam gacC. " + COUNTED,
        dark=True,
    )


def page_cases():
    cells = DATA["rama"]["cells"][:24]
    grid = ['<div style="position:absolute;left:64px;top:340px;width:952px;display:grid;'
            'grid-template-columns:repeat(3,1fr);gap:12px">']
    for i, c in enumerate(cells):
        grid.append(
            f'<div class="fade" style="background:var(--card);border-radius:12px;padding:14px 16px;'
            f'animation-delay:{0.1+i*0.03}s">'
            f'<div style="font:700 11px var(--font-body);color:var(--accent)">{e(c["slot"])}</div>'
            f'<div style="font:700 26px var(--dev);margin-top:4px">{e(c["deva"])}</div>'
            f'<div style="font:italic 13px var(--font-body);color:var(--sub)">{e(c["iast"])}</div></div>'
        )
    grid.append("</div>")
    inner = (
        f'<div class="hero">Парадигма <b>rāma</b> (m.) из MWinflect: '
        f'<b>{len(cells)}</b> клеток = 8 падежей × 3 числа. '
        f'Таблица nominals calc_tables.txt, {fmt(DATA["rama"]["table_rows"])} строк.</div>'
        + "".join(grid)
        + '<div class="fade" style="position:absolute;left:64px;top:1500px;width:952px;background:var(--card);'
        'border-radius:14px;padding:20px 26px;animation-delay:.6s">'
        '<div style="font:700 13px var(--font-body);color:var(--accent);letter-spacing:.08em">как читать сетку</div>'
        '<div style="font:600 15px/1.55 var(--font-body);color:var(--sub);margin-top:6px">'
        'Основа <b style="color:var(--ink)">rāma-</b> (модель m_a — мужской род, a-стем). '
        '<b style="color:var(--ink)">du</b> — двойственное число: ровно для двух предметов, '
        'отдельные формы во всех восьми падежах. Порядок строк — N A I D Ab G L V, '
        'как хранит calc_tables.txt (1s,1d,1p…8s,8d,8p).</div></div>'
    )
    return shell(
        "Сетка падежей",
        "Санскритский архив Гасунса · формы",
        "Сетка падежей rāma",
        inner,
        foot("probe.py → rama.cells"),
        "Data: MWinflect/nominals/.../calc_tables.txt rāma paradigm. " + COUNTED,
    )


def page_citations():
    rows = DATA["mw"]["top_ls"][:18]
    mx = max(r["n"] for r in rows) or 1
    items = []
    for i, r in enumerate(rows):
        w = 40 + 620 * r["n"] / mx
        y = 330 + i * 80
        items.append(
            f'<div class="fade" style="position:absolute;left:64px;top:{y}px;width:952px;display:flex;gap:16px;'
            f'align-items:center;animation-delay:{0.1+i*0.03}s">'
            f'<div style="width:70px;font:700 16px var(--font-display);color:var(--accent)">{i+1:02d}</div>'
            f'<div style="width:220px;font:700 18px var(--font-body)">{e(r["ls"])}</div>'
            f'<div style="flex:1;height:18px;background:rgba(41,38,31,.08);border-radius:6px">'
            f'<div style="width:{w:.0f}px;height:100%;background:var(--bar);border-radius:6px"></div></div>'
            f'<div style="width:90px;text-align:right;font:700 18px var(--font-display)">{fmt(r["n"])}</div></div>'
        )
    inner = (
        f'<div class="hero">Теги <b>&lt;ls&gt;</b> в MW: {fmt(DATA["mw"]["n_ls_tags"])} вхождений. '
        "Топ-18 источников, как они записаны в разметке (без нормализации аббревиатур).</div>"
        + "".join(items)
    )
    return shell(
        "Цитаты MW",
        "Санскритский архив Гасунса · корпуса",
        "Самые цитируемые источники",
        inner,
        foot("probe.py → mw.top_ls"),
        "Data: <ls> inner text counts in csl-orig/v02/mw/mw.txt. " + COUNTED,
    )


def page_passport():
    want = ["mw", "pw", "pwg", "ap", "vcp"]
    by = {r["code"]: r for r in DATA["dicts"]["rows"]}
    cards = []
    for i, code in enumerate(want):
        r = by.get(code, {})
        y = 330 + i * 280
        cards.append(
            f'<div class="fade" style="position:absolute;left:64px;top:{y}px;width:952px;background:var(--card);'
            f'border-radius:16px;padding:22px 28px;display:flex;gap:28px;animation-delay:{0.12+i*0.08}s">'
            f'<div style="width:120px;font:800 28px var(--font-display);color:var(--accent)">{e(code.upper())}</div>'
            f'<div style="flex:1"><div style="font:700 18px var(--font-body)">{e(r.get("title") or code)}</div>'
            f'<div style="color:var(--sub);margin-top:4px">печать {e(r.get("print_date") or "—")} · '
            f'{e(r.get("lang") or "?")} · {fmt(r.get("bytes", 0))} байт txt</div></div>'
            f'<div style="font:800 36px var(--font-display)">{fmt(r.get("entries", 0))}</div></div>'
        )
    inner = (
        '<div class="hero">Пять паспортов в одном шаблоне: код Cologne, заголовок header.xml, '
        "год печати, язык заглавия, число &lt;L&gt;, размер txt.</div>" + "".join(cards)
    )
    return shell(
        "Паспорт словаря",
        "Санскритский архив Гасунса · словари",
        "Паспорт: MW PW PWG AP VCP",
        inner,
        foot("probe.py → dicts.rows"),
        "Data: csl-orig/v02 five dictionaries. " + COUNTED,
    )


def page_gita_heat():
    ch = DATA["gita"]["chapters"]
    mx = max(c["n"] for c in ch) or 1
    cells = []
    for i, c in enumerate(ch):
        x = 64 + (i % 6) * 158
        y = 360 + (i // 6) * 430
        alpha = 0.18 + 0.82 * c["n"] / mx
        cells.append(
            f'<div class="fade" style="position:absolute;left:{x}px;top:{y}px;width:146px;height:390px;'
            f'background:rgba(201,85,47,{alpha:.3f});border-radius:16px;padding:18px 14px;animation-delay:{0.1+i*0.04}s">'
            f'<div style="font:700 13px var(--font-body);color:var(--sub)">глава {c["ch"]}</div>'
            f'<div style="font:800 36px var(--font-display);margin-top:12px">{fmt(c["n"])}</div>'
            f'<div style="color:var(--sub);margin-top:8px">токенов золота</div></div>'
        )
    inner = (
        f'<div class="hero">Гита по главам в <b>kosha/data/gita/gita_gold_master.tsv</b>: '
        f'{fmt(DATA["gita"]["n_tokens"])} токенов, {DATA["gita"]["n_chapters"]} глав, '
        f'{fmt(DATA["gita"]["n_lemmas"])} лемм. Это морфологическое золото, не сырой padapāṭha.</div>'
        + "".join(cells)
    )
    return shell(
        "Гита: тепловая карта",
        "Санскритский архив Гасунса · корпуса",
        "Гита: 18 глав",
        inner,
        foot("probe.py → gita.chapters"),
        "Data: kosha/data/gita/gita_gold_master.tsv tokens per chapter. " + COUNTED,
    )


def page_strata():
    s = DATA["sundara"]
    parts = [
        ("примечаний", s["total_notes"], "total_notes в _meta JSON"),
        ("сарг", s["sargas_covered"], "покрытие кн. V"),
        ("шлок с примечанием", s["verses_with_note"], "verses_with_note"),
        ("помечено Kostina", s["kostina"], "поле editor=kostina"),
        ("без editor в JSON", s["unattributed_in_json"], "агрегат, без тел примечаний"),
    ]
    cards = []
    for i, (lab, n, note) in enumerate(parts):
        y = 340 + i * 270
        cards.append(
            f'<div class="fade" style="position:absolute;left:64px;top:{y}px;width:952px;background:var(--card);'
            f'border-radius:16px;padding:26px 32px;animation-delay:{0.12+i*0.08}s">'
            f'<div style="font:700 15px var(--font-body);color:var(--accent)">{e(lab)}</div>'
            f'<div style="font:800 52px var(--font-display)">{fmt(n)}</div>'
            f'<div style="color:var(--sub)">{e(note)}</div></div>'
        )
    inner = (
        '<div class="hero">Стратиграфия аппарата Sundarakāṇḍa: <b>только поля _meta</b> файла '
        "leonov_own_notes.json. Тела примечаний на страницу не выгружались.</div>" + "".join(cards)
    )
    return shell(
        "Стратиграфия комментария",
        "Санскритский архив Гасунса · корпуса",
        "1058 примечаний, без текстов",
        inner,
        foot("probe.py → sundara"),
        "Data: CommentaryStrategies/data/leonov_own_notes.json _meta only. " + COUNTED,
    )


def page_corpora():
    c = DATA["corpora"]
    rows = [
        ("DCS CoNLL-U", c.get("dcs_conllu_files", 0), "файлов .conllu", c.get("dcs_path", "")),
        ("Parallel-Sanskrit-Corpora", c.get("parallel_text_files", 0), "txt/tsv/json/xml", c.get("parallel_path", "")),
        ("telegram-sanskrit-corpus", c.get("telegram_files", 0), "файлов в клоне", c.get("telegram_path", "")),
    ]
    cards = []
    for i, (name, n, unit, path) in enumerate(rows):
        y = 380 + i * 420
        cards.append(
            f'<div class="fade" style="position:absolute;left:64px;top:{y}px;width:952px;background:var(--card);'
            f'border-radius:18px;padding:36px 40px;animation-delay:{0.15+i*0.1}s">'
            f'<div style="font:700 22px var(--font-display)">{e(name)}</div>'
            f'<div style="font:800 64px var(--font-display);color:var(--accent);margin-top:10px">{fmt(n)}</div>'
            f'<div style="color:var(--sub);margin-top:8px">{e(unit)} · {e(path)}</div></div>'
        )
    inner = (
        '<div class="hero">Три корпуса рядом — <b>счёт файлов в локальных клонах</b>, не байты API. '
        "Жанры и лицензии на этой странице не вымышляются.</div>" + "".join(cards)
    )
    return shell(
        "Корпуса рядом",
        "Санскритский архив Гасунса · корпуса",
        "Корпуса рядом",
        inner,
        foot("probe.py → corpora"),
        "Data: file counts in dcs-conllu, Parallel-Sanskrit-Corpora, telegram-sanskrit-corpus. " + COUNTED,
    )


def page_samasa():
    classes = DATA["samasa"]["classes"]
    n = max(len(classes), 1)
    nodes = []
    cx, cy, R = 540, 1000, 360
    for i, c in enumerate(classes):
        ang = -math.pi / 2 + i * 2 * math.pi / n
        x = cx + R * math.cos(ang) - 110
        y = cy + R * math.sin(ang) - 50
        nodes.append(
            f'<div class="fade" style="position:absolute;left:{x:.0f}px;top:{y:.0f}px;width:220px;text-align:center;'
            f'animation-delay:{0.15+i*0.08}s">'
            f'<div style="font:700 20px var(--font-display)">{e(c["name"])}</div>'
            f'<div style="font:800 32px var(--font-display);color:var(--accent)">{c["leaves"]}</div>'
            f'<div style="font:600 12px var(--font-body);color:var(--sub)">листьев</div></div>'
        )
    inner = (
        f'<div class="hero">Таксономия SamasaChakram: <b>{DATA["samasa"]["n_classes"]}</b> класса, '
        f'<b>{DATA["samasa"]["n_leaves"]}</b> листьев из samasacakra-taxonomy.json.</div>'
        f'<div style="position:absolute;left:400px;top:930px;width:280px;text-align:center">'
        f'<div style="font:700 28px var(--dev)">समास</div></div>'
        + "".join(nodes)
    )
    return shell(
        "Колесо самас",
        "Санскритский архив Гасунса · грамматика",
        "Колесо самас",
        inner,
        foot("probe.py → samasa"),
        "Data: SamasaChakram/samasacakra/samasacakra-taxonomy.json. " + COUNTED,
        dark=True,
    )


def page_sandhi():
    rows = DATA["sandhi"]["top"][:12]
    mx = max(int(r["n"]) for r in rows) or 1
    items = []
    for i, r in enumerate(rows):
        w = 40 + 640 * int(r["n"]) / mx
        y = 340 + i * 115
        items.append(
            f'<div class="fade" style="position:absolute;left:64px;top:{y}px;width:952px;animation-delay:{0.1+i*0.04}s">'
            f'<div style="display:flex;justify-content:space-between;font:700 16px var(--font-body)">'
            f'<span>{e(r["rule"])}</span><span>{fmt(r["n"])}</span></div>'
            f'<div style="color:var(--sub);font:600 13px var(--font-body)">{e(r["category"])}</div>'
            f'<div style="height:14px;background:rgba(41,38,31,.08);border-radius:6px;margin-top:6px">'
            f'<div style="width:{w:.0f}px;height:100%;background:var(--blue);border-radius:6px"></div></div></div>'
        )
    inner = (
        '<div class="hero">Топ правил из <b>kosha/data/sandhi/corpus_sandhi.tsv</b> — global_count по 41 тексту.</div>'
        + "".join(items)
    )
    return shell(
        "Рекорды сандхи",
        "Санскритский архив Гасунса · грамматика",
        "Рекорды сандхи",
        inner,
        foot("probe.py → sandhi.top"),
        "Data: kosha/data/sandhi/corpus_sandhi.tsv. " + COUNTED,
    )


def page_case_tracks():
    # Honest: 5 printed grammars are not five comparable tables. Use Gita gold case codes.
    gita = GH_gita_codes()
    items = []
    mx = max((n for _k, n in gita), default=1)
    for i, (code, n) in enumerate(gita[:12]):
        y = 340 + i * 115
        w = 40 + 640 * n / mx
        items.append(
            f'<div class="fade" style="position:absolute;left:64px;top:{y}px;width:952px;animation-delay:{0.1+i*0.04}s">'
            f'<div style="display:flex;justify-content:space-between"><b>код {e(code)}</b><b>{fmt(n)}</b></div>'
            f'<div style="height:14px;background:rgba(41,38,31,.08);border-radius:6px;margin-top:8px">'
            f'<div style="width:{w:.0f}px;height:100%;background:var(--red);border-radius:6px"></div></div></div>'
        )
    inner = (
        '<div class="hero">Каталог просил «5 учебников». На диске нет пяти сопоставимых таблиц падежа. '
        "Вместо этого — <b>коды падежа/формы в золоте Гиты</b> (колонка code, kosha gita_gold_master.tsv). "
        f"Токенов: {fmt(DATA['gita']['n_tokens'])}.</div>" + "".join(items)
    )
    return shell(
        "Падежные дорожки",
        "Санскритский архив Гасунса · педагогика",
        "Падеж в золоте Гиты",
        inner,
        foot("build.py GH_gita_codes ← gita_gold_master.tsv"),
        "Replacement for 5-grammar compare: gita gold `code` frequencies. " + COUNTED,
    )


def GH_gita_codes():
    p = Path(r"C:\Users\user\Documents\GitHub\kosha\data\gita\gita_gold_master.tsv")
    c = {}
    with p.open("r", encoding="utf-8", errors="replace") as f:
        header = f.readline().split("\t")
        idx = header.index("code") if "code" in header else 5
        for line in f:
            parts = line.split("\t")
            if idx < len(parts):
                key = parts[idx].strip() or "?"
                c[key] = c.get(key, 0) + 1
    return sorted(c.items(), key=lambda kv: -kv[1])


def page_licenses():
    rows = DATA["dicts"]["rows"]
    buckets = {"PD-heuristic (<1928)": 0, "later-print": 0, "no-date": 0}
    items = []
    for r in rows:
        y0 = 9999
        m = re.search(r"(1[6-9]\d{2}|20\d{2})", r.get("print_date") or "")
        if m:
            y0 = int(m.group(1))
            key = "PD-heuristic (<1928)" if y0 < 1928 else "later-print"
        else:
            key = "no-date"
        buckets[key] += 1
    for i, (k, n) in enumerate(buckets.items()):
        y = 380 + i * 360
        color = "#2E7D4F" if i == 0 else ("#C9A227" if i == 1 else "#888")
        items.append(
            f'<div class="fade" style="position:absolute;left:64px;top:{y}px;width:952px;background:var(--card);'
            f'border-radius:18px;padding:36px;animation-delay:{0.15+i*0.1}s">'
            f'<div style="width:28px;height:28px;border-radius:50%;background:{color};display:inline-block"></div>'
            f'<div style="font:700 22px var(--font-display);margin-top:12px">{e(k)}</div>'
            f'<div style="font:800 56px var(--font-display)">{n}</div>'
            f'<div style="color:var(--sub)">словарей из {DATA["dicts"]["n_dicts"]}</div></div>'
        )
    inner = (
        '<div class="hero">Не юридический вердикт. Светофор по <b>году печати из header.xml</b>: '
        "до 1928 — эвристика PD для исходника; оцифровка Cologne — CC-BY-SA (LICENSE csl-orig). "
        "Серые зоны не закрашены в «можно публиковать».</div>" + "".join(items)
    )
    return shell(
        "Светофор лицензий",
        "Санскритский архив Гасунса · словари",
        "Светофор лицензий",
        inner,
        foot("probe.py → dicts.rows.print_date"),
        "Heuristic from print year; csl-orig LICENSE is CC-BY-SA. " + COUNTED,
    )


def page_devanagari_quarter():
    rows = [r for r in DATA["sanhw1"]["letters"] if r["slp1"].isalpha()][:33]
    mx = max(r["n"] for r in rows) or 1
    cards = []
    for i, r in enumerate(rows):
        x = 48 + (i % 6) * 168
        y = 330 + (i // 6) * 240
        h = 24 + 90 * r["n"] / mx
        cards.append(
            f'<div class="fade" style="position:absolute;left:{x}px;top:{y}px;width:156px;height:220px;'
            f'background:var(--card);border-radius:12px;padding:10px;animation-delay:{0.08+i*0.02}s">'
            f'<div style="font:700 28px var(--dev)">{e(r["deva"])}</div>'
            f'<div style="height:{h:.0f}px;margin-top:8px;background:var(--bar);border-radius:6px"></div>'
            f'<div style="font:700 13px var(--font-body);margin-top:6px">{fmt(r["n"])}</div></div>'
        )
    inner = (
        f'<div class="hero">Квартал букв: первая буква sanhw1 ({fmt(DATA["sanhw1"]["n_headwords"])} заголовков). '
        "Дома — пропорциональны частоте.</div>" + "".join(cards)
    )
    return shell(
        "Деванагари-квартал",
        "Санскритский архив Гасунса · педагогика",
        "Деванагари-квартал",
        inner,
        foot("probe.py → sanhw1.letters"),
        "Data: SanskritSpellCheck/sanhw1.txt first character. " + COUNTED,
    )


def page_coverage():
    curve = DATA["gita"]["coverage_curve"]
    pts = []
    w, h = 900, 900
    for c in curve:
        x = 80 + w * math.log(c["k"]) / math.log(max(curve[-1]["k"], 2))
        y = 1680 - h * c["coverage"] / 100
        pts.append(f"{x:.1f},{y:.1f}")
    labels = []
    for c in curve:
        x = 80 + w * math.log(c["k"]) / math.log(max(curve[-1]["k"], 2))
        y = 1680 - h * c["coverage"] / 100
        labels.append(
            f'<div style="position:absolute;left:{x-30:.0f}px;top:{y-28:.0f}px;font:700 12px var(--font-body)">'
            f'{c["k"]}→{c["coverage"]}%</div>'
        )
    inner = (
        f'<div class="hero">Кривая покрытия золота Гиты: топ-100 лемм = <b>{DATA["gita"]["top100_coverage"]}%</b> '
        f'из {fmt(DATA["gita"]["n_tokens"])} токенов. Ось X — логарифм k.</div>'
        f'<svg width="1080" height="1920" style="position:absolute;left:0;top:0">'
        f'<polyline fill="none" stroke="#009B7D" stroke-width="5" points="{" ".join(pts)}"/></svg>'
        + "".join(labels)
    )
    return shell(
        "Сколько слов для Гиты",
        "Санскритский архив Гасунса · педагогика",
        "Кривая покрытия Гиты",
        inner,
        foot("probe.py → gita.coverage_curve"),
        "Data: kosha/data/gita/gita_gold_master.tsv lemma frequencies. " + COUNTED,
    )


def page_langs():
    c = {}
    for r in DATA["dicts"]["rows"]:
        c[r["lang"]] = c.get(r["lang"], 0) + 1
    order = sorted(c.items(), key=lambda kv: -kv[1])
    cards = []
    for i, (lang, n) in enumerate(order):
        y = 360 + i * 260
        cards.append(
            f'<div class="fade" style="position:absolute;left:64px;top:{y}px;width:952px;background:var(--card);'
            f'border-radius:16px;padding:28px;animation-delay:{0.12+i*0.08}s;display:flex;justify-content:space-between">'
            f'<div style="font:700 28px var(--font-display)">{e(lang)}</div>'
            f'<div style="font:800 48px var(--font-display);color:var(--accent)">{n}</div></div>'
        )
    inner = (
        '<div class="hero">Язык <b>заглавия</b> в header.xml (не язык глосс внутри статьи). '
        "other — заголовок пуст или не EN/DE/FR/RU/SA.</div>" + "".join(cards)
    )
    return shell(
        "Три языка науки",
        "Санскритский архив Гасунса · сравнения",
        "Языки заглавий словарей",
        inner,
        foot("probe.py → dicts.rows.lang"),
        "Data: title language heuristic from *header.xml. " + COUNTED,
    )


def page_pulse():
    heat = DATA["git"]["heat_weekday_week"]
    flat = [v for row in heat for v in row]
    mx = max(flat) or 1
    rects = []
    for wd, row in enumerate(heat):
        for wk, n in enumerate(row[:48]):
            a = n / mx
            col = f"rgba(0,155,125,{0.08 + 0.92 * a:.3f})"
            x = 70 + wk * 19
            y = 420 + wd * 160
            rects.append(
                f'<rect x="{x}" y="{y}" width="16" height="140" rx="3" fill="{col}"/>'
            )
    days = "пн вт ср чт пт сб вс".split()
    labels = "".join(
        f'<div style="position:absolute;left:16px;top:{460+i*160}px;font:700 13px var(--font-body);color:var(--sub)">{d}</div>'
        for i, d in enumerate(days)
    )
    inner = (
        f'<div class="hero">Тепловая карта коммитов с 01.01.2025 в <b>12 клонах</b> (не все 85). '
        f'Всего <b>{fmt(DATA["git"]["commits_since_2025"])}</b> коммитов. Ячейка — неделя × день недели.</div>'
        f'<svg width="1080" height="1920" style="position:absolute;left:0;top:0">{"".join(rects)}</svg>'
        + labels
    )
    return shell(
        "Пульс коммитов",
        "Санскритский архив Гасунса · инфраструктура",
        "Пульс коммитов",
        inner,
        foot("probe.py → git.heat_weekday_week"),
        "Data: git log --since=2025-01-01 on 12 named clones. " + COUNTED,
        dark=True,
    )


def page_who():
    fam = DATA["registry"]["by_family"]
    total = sum(fam.values())
    items = []
    mx = max(fam.values()) if fam else 1
    for i, (k, n) in enumerate(fam.items()):
        y = 340 + i * 170
        w = 40 + 700 * n / mx
        items.append(
            f'<div class="fade" style="position:absolute;left:64px;top:{y}px;width:952px;animation-delay:{0.1+i*0.05}s">'
            f'<div style="display:flex;justify-content:space-between"><b>{e(k)}</b><b>{fmt(n)}</b></div>'
            f'<div style="height:22px;background:rgba(255,255,255,.08);border-radius:8px;margin-top:8px">'
            f'<div style="width:{w:.0f}px;height:100%;background:var(--accent);border-radius:8px"></div></div></div>'
        )
    inner = (
        f'<div class="hero">Имя модели в <b>имени файла handoff</b> (H###-Family_). '
        f'{fmt(DATA["registry"]["handoff_rows"])} строк реестра, {fmt(total)} с семейством. '
        "Не часы и не git-blame людей.</div>" + "".join(items)
    )
    return shell(
        "Кто пишет санскрит",
        "Санскритский архив Гасунса · инфраструктура",
        "Кто пишет: семейства агентов",
        inner,
        foot("probe.py → registry.by_family"),
        "Data: Uprava handoffs README + REGISTRY_ARCHIVE filename tokens. " + COUNTED,
        dark=True,
    )


def page_ci():
    rows = DATA["git"]["repos"]
    items = []
    for i, r in enumerate(rows):
        y = 330 + i * 120
        items.append(
            f'<div class="fade" style="position:absolute;left:64px;top:{y}px;width:952px;display:flex;gap:16px;'
            f'align-items:center;animation-delay:{0.08+i*0.03}s">'
            f'<div style="width:280px;font:700 16px var(--font-body)">{e(r["repo"])}</div>'
            f'<div style="flex:1;height:16px;background:rgba(41,38,31,.08);border-radius:6px">'
            f'<div style="width:{min(100, r["workflows"]*10)}%;height:100%;background:#2E7D4F;border-radius:6px"></div></div>'
            f'<div style="width:80px;text-align:right;font:800 20px var(--font-display)">{r["workflows"]}</div></div>'
        )
    inner = (
        f'<div class="hero">Файлы <b>.github/workflows/*.yml</b> в тех же 12 клонах: '
        f'{DATA["git"]["n_workflows"]} воркфлоу, {DATA["git"]["n_repos_with_workflows"]} репо с CI.</div>'
        + "".join(items)
    )
    return shell(
        "CI-паспорт",
        "Санскритский архив Гасунса · инфраструктура",
        "CI-паспорт 12 клонов",
        inner,
        foot("probe.py → git.repos.workflows"),
        "Data: count of .github/workflows yaml on 12 clones. " + COUNTED,
    )


def page_growth():
    rows = sorted(DATA["git"]["repos"], key=lambda r: -r["commits_since_2025"])
    mx = rows[0]["commits_since_2025"] or 1
    items = []
    for i, r in enumerate(rows):
        y = 330 + i * 120
        w = 40 + 700 * r["commits_since_2025"] / mx
        items.append(
            f'<div class="fade" style="position:absolute;left:64px;top:{y}px;width:952px;animation-delay:{0.08+i*0.03}s">'
            f'<div style="display:flex;justify-content:space-between"><b>{e(r["repo"])}</b>'
            f'<b>{fmt(r["commits_since_2025"])}</b></div>'
            f'<div style="height:16px;background:rgba(41,38,31,.08);border-radius:6px;margin-top:6px">'
            f'<div style="width:{w:.0f}px;height:100%;background:var(--blue);border-radius:6px"></div></div></div>'
        )
    inner = (
        '<div class="hero">Не кумулятив «репо с 2014». Честный срез: <b>коммиты с 1 января 2025</b> '
        f'в 12 клонах, сумма {fmt(DATA["git"]["commits_since_2025"])}.</div>' + "".join(items)
    )
    return shell(
        "Рост имения",
        "Санскритский архив Гасунса · инфраструктура",
        "Коммиты 2025–2026",
        inner,
        foot("probe.py → git.repos"),
        "Data: git log --since=2025-01-01 on 12 clones. " + COUNTED,
    )


def page_systema():
    s = DATA["systema"]
    inner = (
        f'<div class="hero">Колоды SRS в сидере Systema: <b>manifest.json</b> и CSV. '
        "Не прод-база студентов, не стрики живых людей.</div>"
        f'<div class="fade" style="position:absolute;left:64px;top:420px;width:952px;background:var(--card);'
        f'border-radius:20px;padding:48px">'
        f'<div style="font:700 16px var(--font-body);color:var(--accent)">manifest.json</div>'
        f'<div style="font:800 72px var(--font-display)">{fmt(s["manifests"])}</div>'
        f'<div style="margin-top:28px;font:700 16px var(--font-body);color:var(--accent)">CSV файлов</div>'
        f'<div style="font:800 72px var(--font-display)">{fmt(s["csv_files"])}</div>'
        f'<div style="margin-top:16px;color:var(--sub)">{e(s["path"])}</div></div>'
    )
    return shell(
        "Дорога ученика",
        "Санскритский архив Гасунса · приложения",
        "Systema: колоды в сидере",
        inner,
        foot("probe.py → systema"),
        "Data: Systema-Sanscriticum/database/seeders/data file counts. " + COUNTED,
    )


def page_campus():
    cards = [
        ("kosha", "локальный клон kosha"),
        ("Systema-Sanscriticum", "кабинет / SRS"),
        ("SanskritKaraoke", "чтение вслух"),
        ("gasyoun.github.io", "инфографики и vote"),
        ("ORS-FAQ", "публичный FAQ"),
        ("csl-orig", "45− словарей"),
    ]
    items = []
    for i, (name, note) in enumerate(cards):
        x = 64 + (i % 2) * 476
        y = 360 + (i // 2) * 440
        items.append(
            f'<div class="fade" style="position:absolute;left:{x}px;top:{y}px;width:452px;height:400px;'
            f'background:var(--card);border-radius:18px;padding:28px;animation-delay:{0.1+i*0.07}s">'
            f'<div style="font:800 28px var(--font-display)">{e(name)}</div>'
            f'<div style="color:var(--sub);margin-top:12px">{e(note)}</div>'
            f'<div style="margin-top:24px;font:700 13px var(--font-body);color:var(--accent)">клон на диске</div></div>'
        )
    inner = (
        '<div class="hero">Кампус продуктов — шесть публичных контуров, которые <b>лежат как клоны</b> '
        "на этой машине. Без вымышленных MAU.</div>" + "".join(items)
    )
    return shell(
        "Кампус продуктов",
        "Санскритский архив Гасунса · приложения",
        "Кампус продуктов",
        inner,
        foot("build.py campus cards"),
        "Inventory of local product clones, not traffic. " + COUNTED,
    )


def page_price():
    h = DATA["registry"]["handoff_rows"]
    entries = DATA["dicts"]["total_entries"]
    per_m = h / (entries / 1_000_000) if entries else 0
    inner = (
        f'<div class="hero">Грубая прокси-цена: строки handoff / миллион словарных статей. '
        "Это <b>не деньги и не часы</b> — только отношение двух посчитанных величин.</div>"
        f'<div class="fade" style="position:absolute;left:64px;top:420px;width:952px">'
        f'<div style="font:700 16px var(--font-body);color:var(--accent)">handoff-строк</div>'
        f'<div style="font:800 64px var(--font-display)">{fmt(h)}</div>'
        f'<div style="margin-top:28px;font:700 16px var(--font-body);color:var(--accent)">статей csl-orig</div>'
        f'<div style="font:800 64px var(--font-display)">{fmt(entries)}</div>'
        f'<div style="margin-top:28px;font:700 16px var(--font-body);color:var(--accent)">handoff на 1 млн статей</div>'
        f'<div style="font:800 64px var(--font-display)">{per_m:.1f}</div></div>'
    )
    return shell(
        "Цена слова",
        "Санскритский архив Гасунса · приложения",
        "Цена слова (прокси)",
        inner,
        foot("probe.py registry.handoff_rows / dicts.total_entries"),
        "Proxy ratio only. " + COUNTED,
    )


def page_gtd():
    g = DATA["registry"]["gtd"]
    items = []
    for i, (k, n) in enumerate(g.items()):
        y = 400 + i * 400
        items.append(
            f'<div class="fade" style="position:absolute;left:64px;top:{y}px;width:952px;background:var(--card);'
            f'border-radius:18px;padding:36px;animation-delay:{0.12+i*0.1}s">'
            f'<div style="font:700 22px var(--font-mono,monospace)">{e(k)}</div>'
            f'<div style="font:800 72px var(--font-display)">{fmt(n)}</div></div>'
        )
    inner = (
        '<div class="hero">Снепшот GTD: число токенов в Uprava/GTD_NEXT_ACTIONS.md. '
        "Не уникальные задачи (токен может повторяться).</div>" + "".join(items)
    )
    return shell(
        "Roadmap-снепшот",
        "Санскритский архив Гасунса · приложения",
        "GTD-снепшот",
        inner,
        foot("probe.py → registry.gtd"),
        "Data: token counts in GTD_NEXT_ACTIONS.md. " + COUNTED,
    )


def page_zaliznyak():
    zdir = Path(r"C:\Users\user\Documents\GitHub\kosha\data\zaliznyak")
    n = 0
    names = []
    if zdir.exists():
        for p in zdir.iterdir():
            if p.is_file():
                n += 1
                names.append(p.name)
    inner = (
        '<div class="hero">Мост не рисует биографию. На диске: каталог '
        "<b>kosha/data/zaliznyak</b> — сколько файлов индекса лежит рядом с санскритским золотом.</div>"
        f'<div class="fade" style="position:absolute;left:64px;top:480px;width:952px;background:var(--card);'
        f'border-radius:20px;padding:40px">'
        f'<div style="font:800 72px var(--font-display)">{n}</div>'
        f'<div style="color:var(--sub)">файлов</div>'
        f'<div style="margin-top:24px;font:600 16px var(--font-body)">{e(", ".join(names[:12]) or "—")}</div></div>'
    )
    return shell(
        "Мост Зализняк",
        "Санскритский архив Гасунса · люди",
        "Зализняк в kosha",
        inner,
        foot("build.py kosha/data/zaliznyak"),
        "Data: file listing of kosha/data/zaliznyak. " + COUNTED,
    )


def page_typos():
    t = DATA["typos"]
    inner = (
        f'<div class="hero">Таблица «грехов» не выдумана из чата. Файл '
        f'<b>gold_corrections.tsv</b>: {fmt(t["n"])} строк золотых правок SanskritSpellCheck. '
        "Типы в TSV — коды кампании, не педагогические ярлыки; поэтому здесь только объём золота.</div>"
        f'<div class="fade" style="position:absolute;left:64px;top:520px;width:952px;background:var(--card);'
        f'border-radius:20px;padding:48px;text-align:center">'
        f'<div style="font:800 96px var(--font-display);color:var(--accent)">{fmt(t["n"])}</div>'
        f'<div>строк gold_corrections.tsv</div></div>'
    )
    return shell(
        "Таблица грехов",
        "Санскритский архив Гасунса · педагогика",
        "Золото опечаток",
        inner,
        foot("probe.py → typos"),
        "Data: SanskritSpellCheck/detectors/gold_corrections.tsv row count. " + COUNTED,
    )


def page_atlas():
    n = DATA["indology"]["md_files"]
    inner = (
        '<div class="hero">Геокодированной таблицы учёных на этом ящике нет — карту мира с точками '
        f"рисовать нельзя. Честный атлас: <b>{fmt(n)}</b> markdown-файлов в клоне IndologyScholars.</div>"
        f'<div class="fade" style="position:absolute;left:64px;top:520px;width:952px;background:var(--card);'
        f'border-radius:20px;padding:48px;text-align:center">'
        f'<div style="font:800 88px var(--font-display)">{fmt(n)}</div>'
        f'<div>md файлов · IndologyScholars</div></div>'
    )
    return shell(
        "Атлас индологов",
        "Санскритский архив Гасунса · люди",
        "Атлас: файлы, не координаты",
        inner,
        foot("probe.py → indology.md_files"),
        "Data: markdown file count in IndologyScholars clone. " + COUNTED,
    )


def page_vs_world():
    ext = DATA["external_cited"]
    ours = DATA["dicts"]["total_entries"]
    rows = [
        ("csl-orig (этот клон)", ours, "probe.py dicts.total_entries"),
        ("OED", ext["oed_entries"], ext["oed_source"]),
        ("DWB Grimm", ext["dwb_headwords"], ext["dwb_source"]),
        ("Duden 27", ext["duden_27_words"], ext["duden_source"]),
    ]
    mx = max(r[1] for r in rows)
    items = []
    for i, (name, n, src) in enumerate(rows):
        y = 360 + i * 340
        w = 80 + 700 * n / mx
        items.append(
            f'<div class="fade" style="position:absolute;left:64px;top:{y}px;width:952px;animation-delay:{0.1+i*0.08}s">'
            f'<div style="font:700 20px var(--font-display)">{e(name)}</div>'
            f'<div style="font:800 40px var(--font-display);color:var(--accent)">{fmt(n)}</div>'
            f'<div style="height:18px;background:rgba(41,38,31,.08);border-radius:6px;margin:8px 0">'
            f'<div style="width:{w:.0f}px;height:100%;background:var(--bar);border-radius:6px"></div></div>'
            f'<div style="font:400 13px var(--font-body);color:var(--sub)">{e(src)}</div></div>'
        )
    inner = (
        '<div class="hero">Санскрит vs великие словари Европы. Внешние цифры <b>с цитатой на странице</b>; '
        "наша — из csl-orig. Разные единицы (статья / headword / Stichwort) не смешиваются в один ранг без оговорки.</div>"
        + "".join(items)
    )
    return shell(
        "MW среди великих",
        "Санскритский архив Гасунса · сравнения",
        "Место среди великих",
        inner,
        foot("probe.py dicts + external_cited"),
        "Internal: csl-orig <L>. External: Wikipedia OED/DWB; Welt 2017 Duden. " + COUNTED,
    )


def page_suitcases():
    rows = DATA["dicts"]["rows"][:12]
    mx = max(r["bytes"] for r in rows) or 1
    items = []
    for i, r in enumerate(rows):
        y = 330 + i * 120
        w = 40 + 700 * r["bytes"] / mx
        mb = r["bytes"] / 1_000_000
        items.append(
            f'<div class="fade" style="position:absolute;left:64px;top:{y}px;width:952px;animation-delay:{0.08+i*0.03}s">'
            f'<div style="display:flex;justify-content:space-between"><b>{e(r["code"])}</b>'
            f'<span>{mb:.1f} МБ · {fmt(r["entries"])} ст.</span></div>'
            f'<div style="height:16px;background:rgba(41,38,31,.08);border-radius:6px;margin-top:6px">'
            f'<div style="width:{w:.0f}px;height:100%;background:var(--red);border-radius:6px"></div></div></div>'
        )
    tot = DATA["dicts"]["total_bytes"] / 1_000_000
    inner = (
        f'<div class="hero">Вес txt в csl-orig/v02: <b>{tot:.1f} МБ</b> на {DATA["dicts"]["n_dicts"]} словарях. '
        "Чемодан = размер файла, не бумага.</div>" + "".join(items)
    )
    return shell(
        "Словари как чемоданы",
        "Санскритский архив Гасунса · сравнения",
        "Словари как чемоданы",
        inner,
        foot("probe.py → dicts.rows.bytes"),
        "Data: Path.stat().st_size of csl-orig/v02/*/code.txt. " + COUNTED,
    )


def page_anthill():
    fam = DATA["registry"]["by_family"]
    dots = []
    colors = {
        "Opus": "#D9503F", "Sonnet": "#4A55C8", "Fable": "#009B7D",
        "Grok": "#C9A227", "OxAlpha": "#8888cc", "Codex": "#aa66aa",
        "Haiku": "#66aaaa", "Kimi": "#999",
    }
    i = 0
    for fam_name, n in fam.items():
        shown = min(n, 180)
        for k in range(shown):
            x = 80 + (i % 28) * 33
            y = 360 + (i // 28) * 33
            col = colors.get(fam_name, "#999")
            dots.append(f'<circle cx="{x}" cy="{y}" r="6" fill="{col}"/>')
            i += 1
    legend = " · ".join(f"{k} {v}" for k, v in fam.items())
    inner = (
        f'<div class="hero">Муравейник: до 180 точек на семейство из {fmt(DATA["registry"]["handoff_rows"])} '
        f"handoff. Цвет = токен файла. {e(legend)}</div>"
        f'<svg width="1080" height="1920" style="position:absolute;left:0;top:0">{"".join(dots)}</svg>'
    )
    return shell(
        "Муравейник агентов",
        "Санскритский архив Гасунса · эксперимент",
        "Муравейник агентов",
        inner,
        foot("probe.py → registry.by_family"),
        "Each dot is a capped sample of handoff filename families. " + COUNTED,
        dark=True,
    )


def page_slider():
    n = DATA["dicts"]["total_entries"]
    inner = (
        f'<div class="hero">От 1 статьи до <b>{fmt(n)}</b> — CSS-анимация счётчика. '
        "Число конечное — из probe.py, не «примерно полтора миллиона».</div>"
        f'<div id="n" style="position:absolute;left:64px;top:720px;font:800 84px var(--font-display);color:var(--accent)">1</div>'
        f'<script>const T={n};const el=document.getElementById("n");let t0=null;'
        f'function f(ts){{if(!t0)t0=ts;const p=Math.min(1,(ts-t0)/2400);'
        f'el.textContent=Math.round(1+(T-1)*p).toLocaleString("ru-RU");'
        f'if(p<1)requestAnimationFrame(f);}}requestAnimationFrame(f);</script>'
    )
    return shell(
        "Слайдер роста",
        "Санскритский архив Гасунса · эксперимент",
        "От 1 до всех статей",
        inner,
        foot("probe.py → dicts.total_entries"),
        "Animated counter to dicts.total_entries. " + COUNTED,
        dark=True,
    )


def page_dashboard():
    cells = [
        ("словари", DATA["dicts"]["n_dicts"]),
        ("статьи", DATA["dicts"]["total_entries"]),
        ("MW k1", DATA["mw"]["unique_k1"]),
        ("sanhw1", DATA["sanhw1"]["n_headwords"]),
        ("handoff", DATA["registry"]["handoff_rows"]),
        ("коммиты 2025+", DATA["git"]["commits_since_2025"]),
        ("токены Гиты", DATA["gita"]["n_tokens"]),
        ("примечания V", DATA["sundara"]["total_notes"]),
        ("CI yaml", DATA["git"]["n_workflows"]),
        ("DCS файлов", DATA["corpora"].get("dcs_conllu_files", 0)),
        ("Systema CSV", DATA["systema"]["csv_files"]),
        ("Indology md", DATA["indology"]["md_files"]),
    ]
    cards = []
    for i, (lab, n) in enumerate(cells):
        x = 64 + (i % 3) * 318
        y = 340 + (i // 3) * 340
        cards.append(
            f'<div class="fade" style="position:absolute;left:{x}px;top:{y}px;width:300px;height:310px;'
            f'background:var(--card);border-radius:16px;padding:22px;animation-delay:{0.08+i*0.04}s">'
            f'<div style="color:var(--sub);font:700 13px var(--font-body)">{e(lab)}</div>'
            f'<div style="font:800 36px var(--font-display);margin-top:18px">{fmt(n)}</div></div>'
        )
    inner = (
        '<div class="hero">Вселенная одним кадром: двенадцать чисел из того же JSON, что и остальные плакаты.</div>'
        + "".join(cards)
    )
    return shell(
        "Вселенная санскрита",
        "Санскритский архив Гасунса · эксперимент",
        "Мета-дашборд",
        inner,
        foot("probe.py JSON rollup"),
        "All figures from scripts/infographics50/data/infographics50.json. " + COUNTED,
    )


def page_somadeva():
    san = Path(r"C:\Users\user\Documents\GitHub\somadeva\chapters_san")
    rus = Path(r"C:\Users\user\Documents\GitHub\somadeva\chapters_rus")
    def nlines(p):
        n = 0
        with p.open("r", encoding="utf-8", errors="replace") as f:
            for _ in f:
                n += 1
        return n
    san_files = sorted(san.glob("*.txt"))
    rus_files = sorted(rus.glob("*.txt"))
    san_n = sum(nlines(p) for p in san_files)
    rus_n = sum(nlines(p) for p in rus_files)
    bars = []
    mx = max((nlines(p) for p in san_files), default=1)
    for i, p in enumerate(san_files):
        n = nlines(p)
        y = 360 + i * 78
        w = 40 + 700 * n / mx
        bars.append(
            f'<div class="fade" style="position:absolute;left:64px;top:{y}px;width:952px;display:flex;gap:12px;'
            f'align-items:center;animation-delay:{0.05+i*0.02}s">'
            f'<div style="width:70px;font:700 14px var(--font-body)">гл. {i+1:02d}</div>'
            f'<div style="flex:1;height:14px;background:rgba(41,38,31,.08);border-radius:6px">'
            f'<div style="width:{w:.0f}px;height:100%;background:var(--bar);border-radius:6px"></div></div>'
            f'<div style="width:90px;text-align:right">{fmt(n)}</div></div>'
        )
    inner = (
        f'<div class="hero">Замена Аштадхьяи: параллельный Сомадева. '
        f'<b>{len(san_files)}</b> глав санскрита, <b>{fmt(san_n)}</b> строк; '
        f'<b>{len(rus_files)}</b> глав перевода, <b>{fmt(rus_n)}</b> строк. '
        "Пути: somadeva/chapters_san + chapters_rus.</div>" + "".join(bars)
    )
    return shell(
        "Сомадева: океан историй",
        "Санскритский архив Гасунса · замена №18",
        "Kathāsaritsāgara, 18 глав",
        inner,
        foot("build.py somadeva chapter line counts"),
        "Replacement for #18. somadeva/chapters_san + chapters_rus line counts. " + COUNTED,
    )


def page_ors_funnel():
    # Public aggregates from committed Tukan_stats.md — no names.
    steps = [
        ("личных диалогов", 3064),
        ("уникальных учеников (агрегат)", 2794),
        ("пар вопрос → ответ", 38280),
        ("сообщений учеников ~", 46325),
        ("оплата", 2553),
        ("стоимость", 1744),
        ("запись", 967),
    ]
    cards = []
    for i, (lab, n) in enumerate(steps):
        y = 340 + i * 200
        cards.append(
            f'<div class="fade" style="position:absolute;left:64px;top:{y}px;width:952px;background:var(--card);'
            f'border-radius:14px;padding:18px 26px;display:flex;justify-content:space-between;'
            f'animation-delay:{0.08+i*0.05}s">'
            f'<div style="font:700 18px var(--font-body)">{e(lab)}</div>'
            f'<div style="font:800 32px var(--font-display);color:var(--accent)">{fmt(n)}</div></div>'
        )
    inner = (
        '<div class="hero">Воронка из <b>ORS-FAQ/Tukan_stats.md</b> (апрель 2026): только опубликованные агрегаты, '
        "без имён и без сырого экспорта. Ступени — таблица «Статистика базы» и топ FAQ.</div>" + "".join(cards)
    )
    return shell(
        "Воронка ORS",
        "Санскритский архив Гасунса · приложения",
        "Воронка ORS (агрегаты)",
        inner,
        foot("ORS-FAQ/Tukan_stats.md public tables"),
        "Data: ORS-FAQ/Tukan_stats.md aggregate tables only. " + COUNTED,
    )


def page_countvowels():
    rows = DATA["countvowels"]["rows"]
    items = []
    mx = max((r["lines"] for r in rows), default=1)
    for i, r in enumerate(rows):
        y = 360 + i * 220
        w = 40 + 700 * r["lines"] / mx
        items.append(
            f'<div class="fade" style="position:absolute;left:64px;top:{y}px;width:952px;animation-delay:{0.1+i*0.06}s">'
            f'<div style="display:flex;justify-content:space-between"><b>{e(r["file"])}</b><b>{fmt(r["lines"])}</b></div>'
            f'<div style="height:18px;background:rgba(41,38,31,.08);border-radius:6px;margin-top:8px">'
            f'<div style="width:{w:.0f}px;height:100%;background:var(--bar);border-radius:6px"></div></div></div>'
        )
    inner = (
        '<div class="hero">Замена №18 «Аштадхьяи как город»: полного 8-книжного sūtrapāṭha на ящике нет. '
        "Вместо города правил — <b>CountVowels CVC-SLP1</b> (строки корпусов).</div>" + "".join(items)
    )
    return shell(
        "Гласные эпоса (замена №18)",
        "Санскритский архив Гасунса · замена",
        "CountVowels вместо Аштадхьяи",
        inner,
        foot("probe.py → countvowels"),
        "Replacement for #18. Data: SanskritSpellCheck/CountVowels/*-CVC-SLP1.txt. " + COUNTED,
    )


def page_prefaces():
    rows = DATA["prefaces"]["rows"]
    items = []
    for i, r in enumerate(rows):
        y = 340 + i * 190
        items.append(
            f'<div class="fade" style="position:absolute;left:64px;top:{y}px;width:952px;background:var(--card);'
            f'border-radius:14px;padding:22px 28px;display:flex;justify-content:space-between;'
            f'animation-delay:{0.1+i*0.05}s">'
            f'<div><b>{e(r["repo"])}</b><div style="color:var(--sub)">{"есть клон" if r["present"] else "нет клона"}</div></div>'
            f'<div style="font:800 32px var(--font-display)">{fmt(r["files"])}</div></div>'
        )
    inner = (
        '<div class="hero">Замена №27 «воронка ORS»: публичных обезличенных ступеней воронки в репо нет, '
        "а сырые CRM/TG не публикуем. Вместо воронки — перепись <b>семи prefaces_*</b>.</div>" + "".join(items)
    )
    return shell(
        "Предисловия семи словарей",
        "Санскритский архив Гасунса · замена",
        "7 репо предисловий",
        inner,
        foot("probe.py → prefaces"),
        "Replacement for #27. File counts in prefaces_* clones. " + COUNTED,
    )


def page_bookindex():
    n = DATA["bookindex"]["md_files"]
    inner = (
        '<div class="hero">Замена №42 «Википедия vs наши словари»: дампа Википедии локально нет, '
        f"внешнюю цифру не округляем. Вместо неё — индекс сканов BookIndex: <b>{fmt(n)}</b> md.</div>"
        f'<div class="fade" style="position:absolute;left:64px;top:560px;width:952px;background:var(--card);'
        f'border-radius:20px;padding:48px;text-align:center">'
        f'<div style="font:800 88px var(--font-display)">{fmt(n)}</div>'
        f'<div>markdown в BookIndex</div></div>'
    )
    return shell(
        "BookIndex (замена №42)",
        "Санскритский архив Гасунса · замена",
        "Индекс сканов",
        inner,
        foot("probe.py → bookindex"),
        "Replacement for #42. Data: BookIndex **/*.md count. " + COUNTED,
    )


def page_sanskrit_vs():
    # #41: our side + cited externals already on vs_world; here GitHub-local only.
    inner = (
        '<div class="hero">Кто «больше оцифрован» на GitHub: считаем только то, что клонировано. '
        "Латынь и греческий как отдельные клоны здесь не собраны — внешних цифр GitHub Search нет "
        "(это не воспроизводимый скрипт). На странице — наши словари и DCS.</div>"
        f'<div class="fade" style="position:absolute;left:64px;top:480px;width:952px">'
        f'<div style="font:700 16px;color:var(--accent)">статьи csl-orig</div>'
        f'<div style="font:800 64px var(--font-display)">{fmt(DATA["dicts"]["total_entries"])}</div>'
        f'<div style="margin-top:32px;font:700 16px;color:var(--accent)">DCS .conllu файлов</div>'
        f'<div style="font:800 64px var(--font-display)">{fmt(DATA["corpora"].get("dcs_conllu_files", 0))}</div>'
        f'<div style="margin-top:24px;color:var(--sub)">латынь/греческий GitHub totals — сняты как нелокальные</div></div>'
    )
    return shell(
        "Санскрит vs латынь vs греческий",
        "Санскритский архив Гасунса · сравнения",
        "Только локальные цифры",
        inner,
        foot("probe.py dicts + corpora; Latin/Greek GitHub omitted"),
        "Unverifiable external GitHub totals dropped. " + COUNTED,
    )


PAGES = [
    ("anatomy-mw-2026-08-29", 2, page_anatomy, False),
    ("mw-letters-2026-08-29", 3, page_letters, False),
    ("editions-timeline-2026-08-29", 4, page_timeline, False),
    ("five-lexicographers-2026-08-29", 5, page_five, False),
    ("dict-genealogy-2026-08-29", 6, page_genealogy, False),
    ("five-encodings-2026-08-29", 9, page_encodings, False),
    ("morph-snowflake-2026-08-29", 11, page_snowflake, False),
    ("case-grid-2026-08-29", 12, page_cases, False),
    ("mw-citations-2026-08-29", 17, page_citations, False),
    ("dict-passport-2026-08-29", 50, page_passport, False),
    ("gita-heatmap-2026-08-29", 14, page_gita_heat, False),
    ("commentary-strata-2026-08-29", 15, page_strata, False),
    ("corpora-beside-2026-08-29", 16, page_corpora, False),
    ("samasa-wheel-2026-08-29", 19, page_samasa, False),
    ("sandhi-records-2026-08-29", 20, page_sandhi, False),
    ("case-tracks-2026-08-29", 21, page_case_tracks, False),
    ("license-lights-2026-08-29", 35, page_licenses, False),
    ("devanagari-quarter-2026-08-29", 39, page_devanagari_quarter, False),
    ("gita-coverage-2026-08-29", 40, page_coverage, False),
    ("science-langs-2026-08-29", 45, page_langs, False),
    ("commit-pulse-2026-08-29", 23, page_pulse, False),
    ("who-writes-2026-08-29", 24, page_who, False),
    ("ci-passport-2026-08-29", 25, page_ci, False),
    ("estate-growth-2026-08-29", 26, page_growth, False),
    ("systema-srs-2026-08-29", 28, page_systema, False),
    ("product-campus-2026-08-29", 29, page_campus, False),
    ("price-of-word-2026-08-29", 30, page_price, False),
    ("gtd-snapshot-2026-08-29", 31, page_gtd, False),
    ("zaliznyak-bridge-2026-08-29", 34, page_zaliznyak, False),
    ("typo-gold-2026-08-29", 38, page_typos, False),
    ("indology-atlas-2026-08-29", 33, page_atlas, False),
    ("sanskrit-vs-classical-2026-08-29", 41, page_sanskrit_vs, False),
    ("bookindex-scans-2026-08-29", 42, page_bookindex, True),
    ("mw-among-greats-2026-08-29", 43, page_vs_world, False),
    ("dict-suitcases-2026-08-29", 44, page_suitcases, False),
    ("agent-anthill-2026-08-29", 46, page_anthill, False),
    ("growth-slider-2026-08-29", 48, page_slider, False),
    ("meta-dashboard-2026-08-29", 49, page_dashboard, False),
    ("somadeva-ocean-2026-08-29", 18, page_somadeva, True),
    ("ors-funnel-2026-08-29", 27, page_ors_funnel, False),
    ("countvowels-cvc-2026-08-29", 0, page_countvowels, False),
    ("prefaces-seven-2026-08-29", 0, page_prefaces, False),
]


def flip_catalog(num: int, slug: str, replaced: bool) -> None:
    text = CATALOG.read_text(encoding="utf-8")
    url = f"https://gasyoun.github.io/infographics/{slug}/index.html"
    chip = "замена · готово" if replaced else "готово"
    # replace the meta chip inside the matching № N item
    pat = re.compile(
        rf'(<span class="num">№ {num}</span>.*?<div class="meta">)(.*?)(</div></li>)',
        re.S,
    )

    def repl(m):
        return (
            m.group(1)
            + f'<span class="chip done">{chip}</span> · <a href="{url}">смотреть</a>'
            + m.group(3)
        )

    new, n = pat.subn(repl, text, count=1)
    if n != 1:
        print("WARN catalog flip failed for", num)
        return
    CATALOG.write_text(new, encoding="utf-8")


def main() -> int:
    built = []
    for slug, num, fn, replaced in PAGES:
        write(slug, fn())
        if num:
            flip_catalog(num, slug, replaced)
        built.append((num, slug, replaced))
    (HERE / "data" / "built.json").write_text(
        json.dumps([{"n": n, "slug": s, "replaced": r} for n, s, r in built], indent=2),
        encoding="utf-8",
    )
    print("built", len(built), "pages")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
