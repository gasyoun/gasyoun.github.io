#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Assemble the static site published at https://gasyoun.github.io/panini/

Run order:
    python build_experiment.py     # quiz.html + data/item_bank*.{tsv,json}
    python make_site.py            # Russian pages, EN reports, data, code, indexes

The Russian pages are authored in templates/*.ru.html; this script supplies the
measured tables and numbers so prose and data cannot drift apart.
"""
from __future__ import annotations

import csv
import html
import json
import os
import shutil
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import ru_glossary as ru  # noqa: E402

SITE = os.path.join(HERE, "site")
DATA = os.path.join(SITE, "data")
CODE = os.path.join(SITE, "code")
TPL = os.path.join(HERE, "templates")
for d in (SITE, DATA, CODE):
    os.makedirs(d, exist_ok=True)

E = lambda s: html.escape(str(s if s is not None else ""), quote=True)


def num(n):
    return format(int(n), ",").replace(",", " ")


def load():
    terms = list(csv.DictReader(open(os.path.join(HERE, "core_terms.tsv"), encoding="utf-8"), delimiter="\t"))
    for t in terms:
        t["batch"] = int(t["batch"])
        for k in ("total", "explicit", "inherited", "governed"):
            t[k] = int(t[k])
    stats = json.load(open(os.path.join(DATA, "item_bank_stats.json"), encoding="utf-8"))
    report = json.load(open(os.path.join(HERE, "report.json"), encoding="utf-8"))
    ext = json.load(open(os.path.join(HERE, "external_channels.json"), encoding="utf-8"))
    return terms, stats, report, ext


# ---------------------------------------------------------------- Russian tables
def batch_cards(terms):
    out = []
    for b in sorted(ru.BATCH_TITLES):
        xs = sorted([t for t in terms if t["batch"] == b], key=lambda t: -t["total"])
        top = ", ".join('<span class="deva">%s</span> <i>%s</i>' % (E(t["deva"]), E(t["iast"]))
                        for t in xs[:6])
        out.append(
            '<div class="card"><h3 style="margin:0 0 4px"><span class="b">B%d</span> %s '
            '<span class="note">· %d терминов</span></h3>'
            '<p class="note" style="margin:4px 0 10px">%s</p>'
            '<div>%s</div></div>' %
            (b, E(ru.BATCH_TITLES[b]), len(xs), E(ru.BATCH_NOTES[b]), top))
    return "\n".join(out)


def term_table(terms):
    out = []
    for b in sorted(ru.BATCH_TITLES):
        xs = sorted([t for t in terms if t["batch"] == b], key=lambda t: -t["total"])
        out.append('<h3><span class="b">B%d</span> %s <span class="note">· %d</span></h3>' %
                   (b, E(ru.BATCH_TITLES[b]), len(xs)))
        out.append('<table><tr><th>Термин</th><th>IAST</th><th>Толкование</th>'
                   '<th>Спрос</th><th>явно / an / ad</th><th>Сутра</th></tr>')
        for t in xs:
            link = ('<a href="%s" title="DSG">↗</a>' % E(t["dsg_url"])) if t["dsg_url"] else ""
            out.append(
                '<tr><td class="deva">%s %s</td><td><i>%s</i></td><td>%s</td>'
                '<td>%s</td><td class="note">%s / %s / %s</td><td class="note">%s</td></tr>' %
                (E(t["deva"]), link, E(t["iast"]), E(ru.RU.get(t["iast"], t["gloss"])),
                 num(t["total"]), num(t["explicit"]), num(t["inherited"]),
                 num(t["governed"]), E(t["sutra"])))
        out.append('</table>')
    return "\n".join(out)


def bank_stats_html(stats):
    f = stats["forms"]
    ch = stats["implicit_by_channel"]
    lines = [
        '<div class="card"><b>Банк заданий собран из тех же закреплённых данных</b> '
        '(не придуман вручную).</div>',
        '<table><tr><th>Показатель</th><th>Значение</th></tr>',
        '<tr><td>Сутры / ядерные термины</td><td>%s / %s</td></tr>' %
        (num(stats["sutras"]), num(stats["core_terms"])),
        '<tr><td>Потенциальных «неявных слотов» (термин требуется, но не написан)</td><td>%s</td></tr>' %
        num(stats["implicit_candidates"]),
        '<tr><td>из них <code>adhikāra</code> / <code>anuvṛtti</code></td><td>%s / %s</td></tr>' %
        (num(ch["adhikāra"]), num(ch["anuvṛtti"])),
        '<tr><td>Русских толкований</td><td>%s из %s</td></tr>' %
        (num(stats["terms_with_russian_gloss"]), num(stats["core_terms"])),
    ]
    for form in ("A", "B"):
        v = f[form]
        lines.append(
            '<tr><td>Форма %s</td><td>%s заданий = %s <code>gloss</code> + %s '
            '<code>implicit_trained</code> + %s <code>implicit_transfer</code>; '
            '%s различных терминов, %s различных сутр</td></tr>' %
            (form, num(v["total"]), num(v["by_type"]["gloss"]),
             num(v["by_type"]["implicit_trained"]), num(v["by_type"]["implicit_transfer"]),
             num(v["distinct_terms"]), num(v["distinct_sutras"])))
        lines.append('<tr><td>Форма %s, неявные задания по блокам B0…B6</td><td>%s</td></tr>' %
                     (form, " / ".join("%s" % v["implicit_by_batch"][str(b)] for b in range(7))))
    lines += [
        '<tr><td>Резерв для будущих параллельных форм</td><td>%s заданий</td></tr>' %
        num(stats["reserve_items"]),
        '<tr><td><b>Всего в банке</b></td><td><b>%s заданий</b></td></tr>' %
        num(stats["total_items_in_bank"]),
        '</table>',
        '<p class="big">Формы A и B не пересекаются по парам «термин + сутра»; задания на '
        'перенос берутся из адхьяй 4–8, которые не входят в учебный материал. '
        'B0-операторы в неявные задания не включены (потолочный эффект).</p>',
    ]
    return "\n".join(lines)


# ------------------------------------------------------------- English artifacts
RU_NAV = (
    '<div style="background:#efe9dc;border-bottom:1px solid #d8d0c0;padding:9px 28px;'
    'font:14px/1.5 system-ui,sans-serif;color:#3a3550">'
    'Русская версия: <a href="index.html" style="color:#4a447f">главная</a> · '
    '<a href="experiment.html" style="color:#4a447f">протокол эксперимента</a> · '
    '<a href="quiz.html" style="color:#4a447f">пилотный тест</a>'
    '&nbsp;&nbsp;<span style="color:#777">|</span>&nbsp;&nbsp;'
    '<b>This page is the English research original</b></div>'
)


def copy_english():
    p = open(os.path.join(HERE, "index.html"), encoding="utf-8").read()
    p = p.replace('href="external_channels.html"', 'href="channels.html"')
    p = p.replace("<body>", "<body>" + RU_NAV, 1)
    open(os.path.join(SITE, "study.html"), "w", encoding="utf-8").write(p)

    q = open(os.path.join(HERE, "external_channels.html"), encoding="utf-8").read()
    q = q.replace('href="index.html"', 'href="study.html"')
    q = q.replace("<body>", "<body>" + RU_NAV, 1)
    open(os.path.join(SITE, "channels.html"), "w", encoding="utf-8").write(q)


# ------------------------------------------------------------------- data / code
DATA_FILES = ["core_terms.tsv", "core_terms.json", "panini_word_forms.tsv",
              "dsg_entries.tsv", "dsg_dcs_join.tsv", "report.json",
              "external_channels.tsv", "external_channels.json"]
CODE_FILES = ["measure.py", "build_batches.py", "external_channels.py", "make_html.py",
              "build_experiment.py", "make_site.py", "ru_glossary.py",
              "slp1_keys.py"]


def copy_assets():
    for f in DATA_FILES:
        shutil.copyfile(os.path.join(HERE, f), os.path.join(DATA, f))
    for f in CODE_FILES:
        shutil.copyfile(os.path.join(HERE, f), os.path.join(CODE, f))
    os.makedirs(os.path.join(CODE, "templates"), exist_ok=True)
    for f in os.listdir(TPL):
        if f.endswith(".ru.html"):
            # keep as .txt: raw templates still contain placeholders and must
            # not be served as (broken) HTML pages by Jekyll
            shutil.copyfile(os.path.join(TPL, f),
                            os.path.join(CODE, "templates", f + ".txt"))


def dir_index(path, title, back, extra=""):
    entries = []
    for name in sorted(os.listdir(path)):
        if name.startswith("."):
            continue
        full = os.path.join(path, name)
        size = os.path.getsize(full) if os.path.isfile(full) else 0
        entries.append('<tr><td><a href="%s">%s</a>%s</td><td class="note">%s</td></tr>' %
                       (E(name), E(name), "/" if os.path.isdir(full) else "",
                        ("%s байт" % num(size)) if size else "каталог"))
    doc = ('<!DOCTYPE html><html lang="ru"><head><meta charset="utf-8">'
           '<meta name="viewport" content="width=device-width,initial-scale=1">'
           '<title>%s</title><style>body{font:16px/1.6 system-ui,sans-serif;color:#24222a;'
           'background:#faf8f4;margin:0}.wrap{max-width:820px;margin:0 auto;padding:40px 24px 70px}'
           'a{color:#4a447f}table{border-collapse:collapse;width:100%%;background:#fff}'
           'th,td{border:1px solid #e5e0d6;padding:7px 10px;text-align:left}'
           'th{background:#f3f0ea}.note{color:#6c6872;font-size:13px}</style></head>'
           '<body><div class="wrap"><p><a href="%s">← %s</a></p><h1>%s</h1>%s'
           '<table><tr><th>Файл</th><th>Размер</th></tr>%s</table></div></body></html>' %
           (E(title), E(back), E("Назад"), E(title), extra, "\n".join(entries)))
    open(os.path.join(path, "index.html"), "w", encoding="utf-8").write(doc)


README = """# panini — что учить первым в санскритской грамматике

Русская версия исследования о порядке изучения терминов Aṣṭādhyāyī.
Опубликовано на https://gasyoun.github.io/panini/

## Страницы

| Файл | Что это |
|---|---|
| `index.html` | русская главная: метод, три оси, семь блоков, 119 терминов |
| `experiment.html` | **протокол ненапроведённого эксперимента** по приросту обучения: гипотезы, РКИ, мощность, анализ, критерии опровержения |
| `quiz.html` | офлайн-инструмент: две параллельные формы A/B, экспорт CSV |
| `study.html` | первичный англоязычный отчёт: измеренный порядок и seven-batch curriculum |
| `channels.html` | англоязычное дополнение: каналы G / L / D, корреляции |
| `data/` | таблицы и JSON со всеми числами |
| `code/` | снимки скриптов измерения и генерации |

## Главный результат

DSG (Abhyankar, 1961) содержит 4 383 статьи и не годится как учебная программа.
Три структурных канала в 3 983 сутрах (`pc` / `an` / `ad`) дают 37 199 требуемых
чтений, из которых ≈65 % — неявные (`anuvṛtti`, `adhikāra`). 119 ядерных терминов
разбиты на семь блоков. Частота в грамматиках подтверждает порядок (ρ = 0,557),
частота в DCS — почти нет (ρ = 0,139), поэтому DCS используется как отрицательный
контроль, а не как четвёртый равноправный канал.

## Качество ключей (исправлено)

Колонка DSG, названная `slp1`, на самом деле **Harvard-Kyoto**, а не SLP1.
Прямое соединение с DCS даёт неверные ключи. В `code/slp1_keys.py` — единый
конвертер HK → SLP1 (проверен по независимой колонке IAST: 3 272 / 3 272
совпадений) и генератор вариантов «классовый назальный ↔ анусвара» как для
деванагари, так и для SLP1. Исправленное соединение всех 4 383 статей —
`data/dsg_dcs_join.tsv`: было 266 совпадений с DCS, стало 1 178 (921 потерянное
совпадение восстановлено). Десять коротких терминов больше не помечаются как
«неизмеримые»: они измерены в трёх полях DSG (английский текст, русский текст,
деванагари-заголовки), пустых значений нет.

## Что НЕ сделано

Никакого эксперимента с учащимися не проводилось. Прирост обучения не измерялся.
`experiment.html` описывает, какой эксперимент можно поставить и какие результаты
опровергли бы предложенный порядок; `quiz.html` и `data/item_bank.tsv` — готовый
пилотный инструмент, а **не валидированный психометрический тест**.

## Воспроизводимость

Снимки источников: `dsg_page.html` (samskrtam.ru) и `panini_data.txt`
(ashtadhyayi-com/data) закреплены по SHA-256 в `data/report.json`.
Внешний vyākaraṇa-корпус — 10 файлов из того же репозитория, 12 627 пассажей.
Порядок пересборки: `measure.py` → `build_batches.py` → `make_html.py` →
`external_channels.py` → `build_experiment.py` → `make_site.py`.
"""


def main():
    terms, stats, report, ext = load()
    assert report["sources"]["dsg"]["entries"] == 4383
    assert report["sources"]["panini"]["sutras"] == 3983
    assert stats["terms_with_russian_gloss"] == len(terms) == 119

    copy_english()
    copy_assets()

    # ---- Russian landing
    tpl = open(os.path.join(TPL, "index.ru.html"), encoding="utf-8").read()
    replacements = {
        "__BATCH_CARDS__": batch_cards(terms),
        "__TERM_TABLE__": term_table(terms),
        "__BANK_TOTAL__": num(stats["total_items_in_bank"]),
        "__BANK_IMPLICIT__": num(stats["implicit_candidates"]),
        "__BANK_FORMS__": num(stats["forms"]["A"]["total"]),
        "__BANK_GLOSS__": num(stats["terms_with_russian_gloss"]),
        "__DQ_NAIVE__": num(ext["data_quality"]["hk_vs_slp1"]["dcs_join"]
                            ["naive_hk_join_hits"]),
        "__DQ_FIXED__": num(ext["data_quality"]["hk_vs_slp1"]["dcs_join"]
                            ["corrected_join_hits"]),
        "__DQ_MISSED__": num(ext["data_quality"]["hk_vs_slp1"]["dcs_join"]
                             ["hits_the_naive_join_missed"]),
        "__DQ_AGREE__": num(ext["data_quality"]["hk_vs_slp1"]
                            ["hk_vs_iast_conversion_audit"]["agree"]),
        "__DCS_ABSENT__": num(ext["channels"]["D_dcs"]["core_terms_absent"]),
        "__DCS_LE5__": num(ext["channels"]["D_dcs"]["core_terms_count_le_5"]),
        "__SHORT_N__": num(len(ext["channels"]["L_dsg_salience"]
                               ["short_stems_collision_controlled"])),
    }
    for k, v in replacements.items():
        tpl = tpl.replace(k, v)
    open(os.path.join(SITE, "index.html"), "w", encoding="utf-8").write(tpl)

    # ---- Russian protocol
    proto = open(os.path.join(TPL, "experiment.ru.html"), encoding="utf-8").read()
    proto = proto.replace("__BANK_STATS__", bank_stats_html(stats))
    open(os.path.join(SITE, "experiment.html"), "w", encoding="utf-8").write(proto)

    # ---- README + directory indexes
    open(os.path.join(SITE, "README.md"), "w", encoding="utf-8").write(README)
    dir_index(DATA, "Данные исследования", "../index.html",
              '<p class="note">TSV в UTF-8, разделитель — табуляция; JSON с отступами. '
              'Хэши исходных снимков — в <code>report.json</code>.</p>')
    dir_index(CODE, "Скрипты", "../index.html",
              '<p class="note">Снимки скриптов для воспроизводимости. Для запуска '
              'нужны исходные снимки <code>dsg_page.html</code> и '
              '<code>panini_data.txt</code> в родительском каталоге проекта.</p>')

    sizes = {f: os.path.getsize(os.path.join(SITE, f))
             for f in ("index.html", "experiment.html", "quiz.html", "study.html", "channels.html")}
    print("site assembled:", json.dumps(sizes, ensure_ascii=False))
    print("data files:", len(os.listdir(DATA)), "code files:", len(os.listdir(CODE)))


if __name__ == "__main__":
    main()
