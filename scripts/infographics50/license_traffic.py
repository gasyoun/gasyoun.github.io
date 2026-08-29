#!/usr/bin/env python3
"""License traffic light #35 — license status of all 45 Cologne dictionaries.

Derives infographics/license-traffic-light-2026-08-29/{data.json,index.html}.
Evidence, in priority order:
  1. `;licence{...}` header in the canonical csl-orig/v02/<dict>/<dict>.txt
  2. LICENSE file of the matching estate repo clone (case-insensitive code match,
     mw -> MWS, yat -> Wil-YAT, pwkvn -> PWK)
Verdicts: green = CC BY-SA 4.0, yellow = GNU GPL v3, grey = not stated in-repo.
"""
import json
import os
import re

V02 = "/Users/mac/Documents/GitHub/csl-orig/v02"
ESTATE = "/Users/mac/Documents/GitHub"
BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
OUT = os.path.join(BASE, "infographics", "license-traffic-light-2026-08-29")

REPO_OVERRIDE = {"mw": "MWS", "yat": "Wil-YAT", "pwkvn": "PWK"}
HEADER_LIC = re.compile(r";licence\{([^}]*)\}")


def classify(text):
    t = text.lower()
    if "gnu general public" in t or "gpl" in t:
        return "yellow"
    if "attribution-sharealike" in t or "cc by-sa" in t or "creative commons" in t:
        return "green"
    return "grey"


def main():
    dicts = sorted(d for d in os.listdir(V02)
                   if os.path.isfile(os.path.join(V02, d, d + ".txt")))
    rows = []
    for d in dicts:
        verdict, evidence = "grey", "не заявлено в клоне"
        with open(os.path.join(V02, d, d + ".txt"), encoding="utf-8", errors="ignore") as f:
            head = []
            for i, line in enumerate(f):
                if line.startswith(";"):
                    head.append(line)
                if i > 4000:
                    break
            head = "".join(head)
        m = HEADER_LIC.search(head)
        if m:
            verdict, evidence = classify(m.group(1)), ";licence{%s} в шапке текста" % m.group(1).strip()
        else:
            repo = REPO_OVERRIDE.get(d, d.upper())
            lic = os.path.join(ESTATE, repo, "LICENSE")
            if os.path.isfile(lic):
                with open(lic, encoding="utf-8", errors="ignore") as f:
                    verdict, evidence = classify(f.read(2000)), "LICENSE репозитория %s" % repo
        rows.append({"dict": d, "verdict": verdict, "evidence": evidence})
    counts = {"green": 0, "yellow": 0, "grey": 0}
    for r in rows:
        counts[r["verdict"]] += 1
    assert len(rows) == 45, len(rows)
    os.makedirs(OUT, exist_ok=True)
    json.dump({"rows": rows, "counts": counts},
              open(os.path.join(OUT, "data.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)

    bands = [("green", "ЗЕЛЁНЫЙ — CC BY-SA 4.0", "свободное использование с атрибуцией и share-alike"),
             ("yellow", "ЖЁЛТЫЙ — GNU GPL v3", "копилефт-лицензия «для кода», для данных — серая зона"),
             ("grey", "СЕРЫЙ — не заявлено", "лицензии нет ни в шапке текста, ни в клоне репозитория")]
    band_html = []
    for key, title, sub in bands:
        codes = [r["dict"] for r in rows if r["verdict"] == key]
        chips = "".join('<span class="chip c-%s">%s</span>' % (key, c) for c in codes)
        band_html.append(
            '<div class="band"><div class="bhead"><span class="light l-%s"></span><span class="btitle">%s · %d</span>'
            '<span class="bsub">%s</span></div><div class="chips">%s</div></div>'
            % (key, title, len(codes), sub, chips))
    html = TEMPLATE.format(bands="\n  ".join(band_html),
                           green=counts["green"], yellow=counts["yellow"], grey=counts["grey"])
    open(os.path.join(OUT, "index.html"), "w", encoding="utf-8").write(html)
    print("45 dicts:", counts)


TEMPLATE = """<!doctype html>
<html lang="ru">
<head>
<meta charset="utf-8">
<title>Светофор лицензий 45 словарей</title>
<!-- Composition: Editorial spread — verdict numeral in the tall left column, three traffic-light
     bands with per-dictionary plates on the right. Editorial, wide 1920x1080. -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,400;0,9..144,600;0,9..144,900;1,9..144,400&family=Libre+Franklin:wght@400;500;600&display=swap" rel="stylesheet">
<style>
*, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
:root {{
  --bg:#FAF7F2; --surface:#F1ECE2; --surface-2:#E3DCCC;
  --ink:#20242C; --ink-muted:#6B6F76; --accent:#A32035;
  --green:#0D7F63; --yellow:#B07C1F; --grey:#9A958A;
  --font-display:'Fraunces',serif; --font-body:'Libre Franklin',sans-serif;
}}
html, body {{ background: var(--bg); }}
body {{ width: 1920px; font-family: var(--font-body); color: var(--ink); }}
.canvas {{ position: relative; width: 1920px; height: 1080px; overflow: hidden; background: var(--bg); }}
.folio {{ position: absolute; left: 72px; right: 72px; top: 40px; display: flex; justify-content: space-between;
  border-top: 1px solid var(--ink); border-bottom: 1px solid var(--ink); padding: 10px 0;
  font: 600 13.5px/1 var(--font-body); letter-spacing: .1em; text-transform: uppercase; color: var(--ink-muted); }}
.left {{ position: absolute; left: 72px; top: 150px; width: 430px; }}
.kicker {{ font: 600 15px/1 var(--font-body); text-transform: uppercase; letter-spacing: .1em; color: var(--ink-muted); }}
h1 {{ font-family: var(--font-display); font-weight: 900; font-size: 68px; line-height: .98; letter-spacing: -0.015em; margin-top: 16px; }}
.standfirst {{ margin-top: 18px; font: italic 400 19px/1.5 var(--font-display); }}
.verdict {{ margin-top: 34px; border-top: 3px solid var(--ink); padding-top: 18px; }}
.verdict .num {{ font-family: var(--font-display); font-weight: 900; font-size: 150px; line-height: 1; }}
.verdict .cap {{ font: 600 17px/1.45 var(--font-body); margin-top: 4px; }}
.meth {{ position: absolute; left: 72px; bottom: 110px; width: 430px; border-top: 1px solid var(--ink);
  padding-top: 12px; font: 400 13.5px/1.6 var(--font-body); color: var(--ink-muted); }}
.bands {{ position: absolute; left: 560px; right: 72px; top: 130px; }}
.band {{ border-top: 1px solid var(--ink); padding: 20px 0 22px; }}
.band:last-child {{ border-bottom: 1px solid var(--ink); }}
.bhead {{ display: flex; align-items: baseline; gap: 14px; flex-wrap: wrap; }}
.light {{ width: 20px; height: 20px; border-radius: 50%; border: 2px solid var(--ink); flex: none; align-self: center; }}
.l-green {{ background: var(--green); }} .l-yellow {{ background: var(--yellow); }} .l-grey {{ background: var(--grey); }}
.btitle {{ font: 600 21px var(--font-body); }}
.bsub {{ font: 400 14px/1.3 var(--font-body); color: var(--ink-muted); }}
.chips {{ margin-top: 12px; display: flex; flex-wrap: wrap; gap: 8px; }}
.chip {{ font: 600 13.5px/1 var(--font-body); padding: 6px 10px; border: 1.5px solid var(--ink); background: var(--surface); }}
.c-green {{ background: #CDE8DF; }} .c-yellow {{ background: #F0E2C0; }} .c-grey {{ background: var(--surface-2); }}
footer {{ position: absolute; left: 72px; right: 72px; bottom: 28px;
  display: flex; justify-content: space-between; gap: 40px;
  border-top: 1px solid var(--ink); padding-top: 12px; font: 400 13.5px/1.5 var(--font-body); color: var(--ink-muted); }}
footer b {{ font-weight: 600; color: var(--ink); }}
</style>
</head>
<body>
<div class="canvas">
  <div class="folio"><span>ЛИЦЕНЗИИ · CСL-ORIG · 45 СЛОВАРЕЙ</span><span>ПОСЧИТАНО 29.08.2026 · No. 35</span></div>
  <div class="left">
    <div class="kicker">САНСКРИТСКИЙ АРХИВ ГАСУНСА · СВЕТОФОР ЛИЦЕНЗИЙ</div>
    <h1>Светофор лицензий 45 словарей</h1>
    <p class="standfirst">Каждый словарь Кёльна получил вердикт по своим же документам: шапке канонического текста или LICENSE-файлу его репозитория.</p>
    <div class="verdict" data-hero>
      <div class="num">{green}<span style="font-size:64px;color:var(--ink-muted)">/45</span></div>
      <div class="cap">словарей открыты под CC BY-SA 4.0 — зелёный свет для производных работ с атрибуцией</div>
    </div>
  </div>
  <div class="meth">
    <b>Методика.</b> Вердикт ставится только по найденному документу: «;licence{{…}}» в первых строках v02/&lt;dict&gt;/&lt;dict&gt;.txt или LICENSE-файл клона репозитория (mw → MWS, yat → Wil-YAT, pwkvn → PWK). Ничего не угадывается: серые — это отсутствие документа, а не разрешение.
  </div>
  <div class="bands">
  {bands}
  </div>
  <footer>
    <div>Данные: <b>csl-orig/v02</b> (шапки текстов) + LICENSE-файлы клонов словарных репозиториев</div>
    <div>скрипт: <b>scripts/infographics50/license_traffic.py</b> · Посчитано 29.08.2026 · <b>Dr. Mārcis Gasūns</b></div>
  </footer>
</div>
</body>
</html>
"""

if __name__ == "__main__":
    main()
