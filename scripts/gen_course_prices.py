#!/usr/bin/env python3
"""Generate the course-prices listing page (students' prices, RUB + EUR)
for gasyoun.github.io from Systema prod (.92), read-only.

Usage: python3 scripts/gen_course_prices.py
Output: courses/course-prices-teachers-<date>.html in the repo root.

Rules (MG defaults 09-10-2026, awaiting veto):
- all courses (visible + archive), archive flagged
- period from lesson dates (sane window 2019-2027), else "—"
- stored EUR prices; missing ones converted at the median implied rate
- totals: course = full tariff if present else sum of block tariffs
"""
import subprocess
import statistics
import sys
from datetime import date
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

REPO = Path(__file__).resolve().parent.parent
TODAY = date.today().strftime("%d-%m-%Y")
OUT_NAME = f"course-prices-teachers-{date.today().isoformat()}.html"

SSH = ["ssh", "-o", "ConnectTimeout=15", "-o", "BatchMode=yes",
       "root@100.85.73.83"]

REMOTE_ENV = r"""cd /var/www/html
U=$(grep '^DB_USERNAME=' .env | cut -d= -f2)
P=$(grep '^DB_PASSWORD=' .env | cut -d= -f2-)
D=$(grep '^DB_DATABASE=' .env | cut -d= -f2-)
"""

REMOTE_MAIN = REMOTE_ENV + r"""
M="mysql --default-character-set=utf8mb4 -N -B -u$U -p$P $D"
echo "===TEACHERS==="
$M -e "SELECT id, REPLACE(name,'\t',' ') FROM teachers ORDER BY id"
echo "===COURSES==="
$M -e "SELECT id, REPLACE(title,'\t',' '), IFNULL(teacher_id,''), is_visible FROM courses ORDER BY id"
echo "===TARIFFS==="
$M -e "SELECT course_id, type, IFNULL(block_number,''), price, REPLACE(LEFT(title,60),'\t',' ') FROM tariffs WHERE is_active=1 ORDER BY course_id, type, block_number, id"
echo "===COURSE_RANGE==="
$M -e "SELECT course_id, MIN(lesson_date), MAX(lesson_date), COUNT(*) FROM lessons WHERE lesson_date BETWEEN '2019-01-01' AND '2027-12-31' GROUP BY course_id"
echo "===BLOCK_RANGE==="
$M -e "SELECT course_id, block_number, MIN(lesson_date), MAX(lesson_date) FROM lessons WHERE lesson_date BETWEEN '2019-01-01' AND '2027-12-31' GROUP BY course_id, block_number"
"""

REMOTE_EUR = REMOTE_ENV + r"""
mysql --default-character-set=utf8mb4 -N -B -u$U -p$P $D -e "SELECT t.course_id, t.type, IFNULL(t.block_number,''), t.price, tfp.price FROM tariffs t JOIN tariff_foreign_prices tfp ON tfp.tariff_id=t.id AND tfp.currency='EUR' WHERE t.is_active=1"
"""

MONTHS = ["янв", "фев", "мар", "апр", "мая", "июн",
          "июл", "авг", "сен", "окт", "ноя", "дек"]


def ssh_query(script):
    res = subprocess.run(SSH + ["bash -s"], input=script,
                         capture_output=True, text=True,
                         encoding="utf-8", check=True)
    return res.stdout


def parse(raw):
    sec, data = None, {}
    for line in raw.splitlines():
        if line.startswith("==="):
            sec = line.strip("=^$")
            data[sec] = []
            continue
        if sec and line.strip():
            data[sec].append(line.split("\t"))
    return data


def money(v, sign):
    s = f"{v:,.2f}".replace(",", " ").replace(".", ",")
    return f"{s} {sign}"


def month_fmt(iso):
    y, m, _ = iso.split("-")[:3]
    return f"{MONTHS[int(m) - 1]} {y}"


def period(a, b):
    if not a or not b:
        return "—"
    return f"{month_fmt(a)} – {month_fmt(b)}"


def main():
    data = parse(ssh_query(REMOTE_MAIN))
    for k in ("TEACHERS", "COURSES", "TARIFFS"):
        if k not in data:
            sys.exit(f"missing section {k}")

    teachers = {r[0]: r[1] for r in data["TEACHERS"]}
    courses = {}
    course_rng = {r[0]: (r[1], r[2], r[3]) for r in data.get("COURSE_RANGE", [])}
    block_rng = {(r[0], r[1]): (r[2], r[3]) for r in data.get("BLOCK_RANGE", [])}

    for r in data["COURSES"]:
        cid, title, tid, vis = r[0], r[1], r[2] or None, r[3] == "1"
        courses[cid] = {"_cid": cid, "title": title, "teacher": tid,
                        "visible": vis, "tariffs": []}
    for r in data["TARIFFS"]:
        cid, ttype, bnum, price, title = r[0], r[1], r[2] or None, float(r[3]), r[4]
        if cid not in courses:
            courses[cid] = {"_cid": cid, "title": f"(курс {cid} вне таблицы)",
                            "teacher": None, "visible": False, "tariffs": []}
        courses[cid]["tariffs"].append(
            {"type": ttype, "block": bnum, "rub": price, "title": title,
             "eur": None, "eur_conv": False})

    eur_join = {}
    for line in ssh_query(REMOTE_EUR).splitlines():
        p = line.split("\t")
        if len(p) == 5:
            eur_join.setdefault((p[0], p[1], p[2] or None), []).append(
                (float(p[3]), float(p[4])))

    implied = []
    for cid, c in courses.items():
        for t in c["tariffs"]:
            for rub_stored, eur_stored in eur_join.get(
                    (cid, t["type"], t["block"]), []):
                if abs(rub_stored - t["rub"]) < 0.01 and eur_stored > 0:
                    t["eur"] = eur_stored
                    implied.append(t["rub"] / eur_stored)
                    break

    rate = statistics.median([x for x in implied if 60 < x < 150]) if implied else 100.0
    n_missing = 0
    for c in courses.values():
        for t in c["tariffs"]:
            if t["eur"] is None:
                t["eur"] = round(t["rub"] / rate, 2)
                t["eur_conv"] = True
                n_missing += 1

    def eur_cell(t):
        return ("~" if t["eur_conv"] else "") + money(t["eur"], "€")

    sections = {}
    for cid, c in courses.items():
        sections.setdefault(c["teacher"] or "__none__", []).append(c)

    html = [f"""<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<title>Стоимость курсов по учителям — {TODAY}</title>
<style>
  :root {{ color-scheme: light dark; }}
  body {{ font: 15px/1.5 -apple-system, "Segoe UI", Roboto, sans-serif; margin: 0; padding: 0 16px 80px; background: #faf9f7; color: #1c1a17; }}
  main {{ max-width: 860px; margin: 0 auto; }}
  h1 {{ font-size: 23px; margin: 32px 0 8px; }}
  h2 {{ font-size: 18px; margin: 34px 0 4px; border-bottom: 1px solid #d8d2c8; padding-bottom: 6px; }}
  h3 {{ font-size: 15px; margin: 22px 0 6px; }}
  .sub {{ color: #6b665e; margin: 0 0 18px; font-size: 14px; }}
  .legend {{ background: #eef1f4; border: 1px solid #c9d4de; border-radius: 10px; padding: 12px 16px; font-size: 13px; margin-bottom: 26px; }}
  table.pay {{ width: 100%; border-collapse: collapse; font-size: 13.5px; margin: 0 0 6px; }}
  table.pay th, table.pay td {{ text-align: left; padding: 5px 8px; border-bottom: 1px solid #e5e0d8; vertical-align: top; }}
  table.pay th {{ color: #6b665e; font-weight: 600; font-size: 11.5px; text-transform: uppercase; letter-spacing: .04em; }}
  td.num, th.num {{ text-align: right; white-space: nowrap; font-variant-numeric: tabular-nums; }}
  tr.total td {{ font-weight: 700; border-top: 1px solid #9a938a; background: rgba(0,0,0,.03); }}
  tr.grand td {{ font-weight: 700; border-top: 2px solid #1c1a17; font-size: 14.5px; }}
  .arch {{ color: #8a8378; font-size: 12px; }}
  footer {{ color: #6b665e; font-size: 12px; margin-top: 44px; }}
  @media print {{ body {{ background: #fff; }} }}
  @media (prefers-color-scheme: dark) {{
    body {{ background: #17150f; color: #e8e2d5; }}
    table.pay th, table.pay td {{ border-color: #3a362c; }}
    tr.total td {{ border-color: #6b665e; background: rgba(255,255,255,.04); }}
    h2 {{ border-color: #3a362c; }}
    .legend {{ background: #232018; border-color: #4a4438; }}
  }}
</style>
</head>
<body>
<main>
<h1>Стоимость курсов по учителям — {TODAY}</h1>
<p class="sub">Systema прод .92, срез только для чтения · цены учеников, ₽ и € · поблочно и целиком</p>
<div class="legend">
<b>Как читать:</b> у каждого курса — все активные тарифы («весь курс» и блоки), цена в ₽ и €.
Период курса = первая–последняя дата занятий в базе (окно 2019–2027); «—» значит дат нет.
€ берётся из сохранённой в системе цены; где её нет ({n_missing} тарифов) — пересчёт по среднему имплицитному курсу {rate:.2f} ₽/€, такие суммы помечены ~.
<b>Итог курса</b> = цена тарифа «весь курс», если он есть, иначе сумма блоков. Итоги учителей и общий итог считаются по этим ценам курса.
</div>"""]

    grand_rub = grand_eur = 0.0
    tids = sorted(sections, key=lambda k: (k == "__none__",
                                           teachers.get(k, "").lower()))
    for tid in tids:
        tname = teachers.get(tid, "") if tid != "__none__" else "Без учителя"
        if not tname:
            tname = f"Учитель id={tid}"
        cl = sections[tid]
        tr = te = 0.0
        rows = []
        for c in sorted(cl, key=lambda x: x["title"].lower()):
            full = [t for t in c["tariffs"] if t["type"] == "full"]
            blocks = sorted([t for t in c["tariffs"] if t["block"]],
                            key=lambda t: (int(t["block"]) if t["block"] and t["block"].isdigit() else 999, t["title"]))
            others = [t for t in c["tariffs"] if t["type"] != "full" and not t["block"]]
            a, b, _n = course_rng.get(c["_cid"], (None, None, 0))
            rows.append(f'<h3>{c["title"]}'
                        + ('' if c["visible"] else ' <span class="arch">архив</span>')
                        + f' <span class="arch">· {period(a, b)}</span></h3>')
            rows.append('<table class="pay"><tr><th>Тариф</th><th>Блок</th>'
                        '<th>Период блока</th><th class="num">₽</th><th class="num">€</th></tr>')
            for t in full:
                rows.append(f'<tr><td>{t["title"] or "Весь курс"}</td><td>—</td><td>—</td>'
                            f'<td class="num">{money(t["rub"], "₽")}</td>'
                            f'<td class="num">{eur_cell(t)}</td></tr>')
            for t in blocks:
                ba, bb = block_rng.get((c["_cid"], t["block"]), (None, None))
                rows.append(f'<tr><td>{t["title"] or "Блок"}</td><td>{t["block"]}</td>'
                            f'<td>{period(ba, bb)}</td>'
                            f'<td class="num">{money(t["rub"], "₽")}</td>'
                            f'<td class="num">{eur_cell(t)}</td></tr>')
            for t in others:
                rows.append(f'<tr><td>{t["title"] or t["type"]}</td><td>{t["type"]}</td><td>—</td>'
                            f'<td class="num">{money(t["rub"], "₽")}</td>'
                            f'<td class="num">{eur_cell(t)}</td></tr>')
            if full:
                cr = (full[0]["rub"], full[0]["eur"])
            elif blocks:
                cr = (sum(t["rub"] for t in blocks), sum(t["eur"] for t in blocks))
            else:
                cr = None
            if cr:
                rows.append(f'<tr class="total"><td colspan="3">Итог курса</td>'
                            f'<td class="num">{money(cr[0], "₽")}</td>'
                            f'<td class="num">{money(cr[1], "€")}</td></tr>')
                tr += cr[0]
                te += cr[1]
            if not c["tariffs"]:
                rows.append('<tr><td colspan="5" class="arch">активных тарифов нет</td></tr>')
            rows.append("</table>")
        html.append(f"<h2>{tname} <span class='arch'>· курсов: {len(cl)}</span></h2>")
        html.extend(rows)
        html.append(f'<p class="sub">Итог по учителю: <b>{money(tr, "₽")}</b> · <b>{money(te, "€")}</b></p>')
        grand_rub += tr
        grand_eur += te

    html.append(f'<table class="pay"><tr class="grand"><td>ОБЩИЙ ИТОГ · {len(courses)} курсов</td>'
                f'<td class="num">{money(grand_rub, "₽")}</td>'
                f'<td class="num">{money(grand_eur, "€")}</td></tr></table>')
    html.append(f"""<footer>Сгенерировано {TODAY} скриптом <code>scripts/gen_course_prices.py</code>
(gasyoun.github.io), источник: Systema прод .92 (MySQL, только чтение: courses, course_blocks,
tariffs, tariff_foreign_prices, lessons). Страница без индексации: meta noindex + robots.txt.
Правила среза согласованы с MG 09-10 (гриль, ответы по умолчанию — ждут визы).</footer>
</main>
</body>
</html>""")

    out = REPO / "courses" / OUT_NAME
    out.parent.mkdir(exist_ok=True)
    out.write_text("\n".join(html), encoding="utf-8")
    print(f"OK {out} ({out.stat().st_size} bytes); courses={len(courses)}, "
          f"teachers={len(tids)}, eur_missing_converted={n_missing}, rate={rate:.2f}")


if __name__ == "__main__":
    main()
