# -*- coding: utf-8 -*-
"""Karta — аннотированный индекс домена gasyoun.github.io.

Скан верхнего уровня репо + рукописные аннотации из karta_data.py ->
одна страница karta/index.html. Паттерн и паритет по H3768
(scripts/infographics50/gen_infographics_index.py).

    python3 scripts/karta/gen_karta_index.py --emit     # собрать страницу
    python3 scripts/karta/gen_karta_index.py --check    # диск не дрейфанул?
    python3 scripts/karta/gen_karta_index.py --probe-islands   # живой HTTP-аудит всех ссылок

Правила:
- Каждый пункт karta_data.py несёт уникальный K### (не переиспользуется).
- Собственные ключи: "index.html" (файл) или "имя_каталога/" (каталог верхнего
  уровня) или вложенный путь внутри каталога. Каждая контентная сущность диска
  обязана быть покрыта хотя бы одним пунктом данных, иначе --emit/--check
  падают со списком непокрытого — карта не молча устаревает.
- Острова (project-pages других репо) живут только в данных и проверяются
  режимом --probe-islands по HTTP.
"""
import argparse
import subprocess
import sys
import urllib.request
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(Path(__file__).parent))
import karta_data as D  # noqa: E402

OUT = ROOT / "karta" / "index.html"

STYLE = """
body{font-family:-apple-system,'Segoe UI',Roboto,sans-serif;max-width:900px;margin:0 auto;
padding:24px 16px;color:#222;background:#faf9f6;line-height:1.55}
h1{font-size:1.6em;margin-bottom:2px} .sub{color:#666;margin:0 0 14px}
h2{font-size:1.15em;margin:28px 0 8px;padding-bottom:4px;border-bottom:2px solid #ddd}
.item{margin:10px 0;padding:8px 12px;background:#fff;border:1px solid #e4e1da;border-radius:8px}
.item b a{color:#1a4d8f;text-decoration:none}.item b a:hover{text-decoration:underline}
.kid{font-family:ui-monospace,monospace;color:#8a6d3b;font-size:.85em;margin-right:6px}
.note{color:#444;font-size:.93em;margin-top:2px}
.meta{color:#888;font-size:.8em;margin-top:2px}
.badge{font-size:.85em}
.legend{background:#f0ede6;border-radius:8px;padding:8px 12px;font-size:.88em;margin:12px 0}
.footer{margin-top:32px;color:#888;font-size:.82em;border-top:1px solid #ddd;padding-top:10px}
code{background:#eee;padding:1px 4px;border-radius:3px;font-size:.9em}
"""


def git_date(rel: str) -> str:
    """Дата последнего коммита, коснувшегося пути (для своих пунктов)."""
    try:
        out = subprocess.run(
            ["git", "log", "-1", "--format=%as", "--", rel],
            cwd=ROOT, capture_output=True, text=True, timeout=30,
        ).stdout.strip()
        return out or "—"
    except Exception:
        return "—"


def disk_scan():
    """Контентные ключи верхнего уровня: *.html файлы и каталоги (не ассеты)."""
    keys = set()
    for p in ROOT.iterdir():
        if p.name.startswith(".") or p.name in D.ASSET_DIRS:
            continue
        if p.is_file() and p.suffix == ".html":
            keys.add(p.name)
        elif p.is_dir():
            keys.add(p.name + "/")
    return keys


def covered_prefixes():
    pref = set()
    for it in D.ITEMS:
        if "key" not in it:
            continue
        head = it["key"].split("/", 1)[0]
        pref.add(head + ("/" if "/" in it["key"] or (ROOT / head).is_dir() else ""))
    return pref


def coverage_errors():
    errs = []
    disk = disk_scan()
    covered = covered_prefixes()
    unmapped = sorted(disk - covered)
    if unmapped:
        errs.append("на диске есть контент, не внесённый в karta_data.py: "
                    + ", ".join(unmapped))
    for it in D.ITEMS:
        if "key" in it and not (ROOT / it["key"].rstrip("/") ).exists() \
                and not (ROOT / it["key"]).exists():
            errs.append(f"{it['id']}: путь {it['key']} не существует на диске")
    ids = [it["id"] for it in D.ITEMS]
    if len(ids) != len(set(ids)):
        errs.append("дубликаты K### в данных")
    return errs


def render():
    own = [it for it in D.ITEMS if "key" in it]
    islands = [it for it in D.ITEMS if "url" in it]
    parts = [
        "<!DOCTYPE html><html lang='ru'><head><meta charset='utf-8'>",
        "<meta name='viewport' content='width=device-width,initial-scale=1'>",
        f"<title>Карта домена gasyoun.github.io</title><style>{STYLE}</style></head><body>",
        "<h1>🗺️ Карта домена gasyoun.github.io</h1>",
        "<p class='sub'>Аннотированный индекс всего опубликованного: этот репо + "
        "острова-проекты других репо того же домена. Номера K### уникальны и стабильны.</p>",
        "<div class='legend'>Статусы: "
        + " · ".join(f"{D.STATUS_BADGE[s]} {D.STATUS_LEGEND[s]}"
                     for s in ("green", "amber", "tomb"))
        + ".&nbsp; Регенерация: <code>python3 scripts/karta/gen_karta_index.py --emit</code>"
        " · проверка дрейфа: <code>--check</code>.</div>",
    ]
    sec_names = dict(D.SECTIONS)
    order = [s for s, _ in D.SECTIONS]
    for sec in order:
        items = [it for it in D.ITEMS if it["sec"] == sec]
        label = sec_names[sec]
        n_own = sum(1 for it in items if "key" in it)
        extra = f" · {len(items) - n_own} островов" if sec == "G" else ""
        parts.append(f"<h2>{sec}. {label} <span class='meta'>({len(items)}{extra or f' · {len(items)}'})</span></h2>")
        for it in items:
            badge = f"<span class='badge'>{D.STATUS_BADGE[it['status']]}</span>"
            if "key" in it:
                link = it.get("href", it["key"])
                href = D.SITE + "/" + link
                date = git_date(it["key"])
                loc = f"<div class='meta'>диск: <code>{it['key']}</code> · посл. коммит {date}</div>"
            else:
                href = D.SITE + "/" + it["url"]
                loc = "<div class='meta'>project-pages другого репо (остров домена)</div>"
            parts.append(
                f"<div class='item'><span class='kid'>{it['id']}</span>{badge} "
                f"<b><a href='{href}'>{it['title']}</a></b>"
                f"<div class='note'>{it['note']}</div>{loc}</div>"
            )
    parts.append(
        f"<div class='footer'>Сгенерировано <code>scripts/karta/gen_karta_index.py --emit</code> ({D.H_REF}) "
        f"из данных <code>karta_data.py</code> · {len(D.ITEMS)} пунктов · "
        f"диск: {len(disk_scan())} ключей · 2026-09-27 · Dr. Mārcis Gasūns</div></body></html>"
    )
    return "\n".join(parts), own, islands


def probe(own, islands, timeout=10):
    fails = []

    def check(url):
        req = urllib.request.Request(url, method="HEAD",
                                     headers={"User-Agent": "karta-probe"})
        try:
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return r.status
        except Exception:
            try:
                with urllib.request.urlopen(url, timeout=timeout) as r:
                    return r.status
            except Exception as e:
                return str(e)

    for it in islands:
        url = f"{D.SITE}/{it['url']}"
        st = check(url)
        print(f"  {it['id']} {st} {url}")
        if st != 200:
            fails.append((it["id"], url, st))
    for it in own:
        url = f"{D.SITE}/{it.get('href', it['key'])}"
        st = check(url)
        print(f"  {it['id']} {st} {url}")
        if st != 200:
            fails.append((it["id"], url, st))
    return fails


def main():
    g = argparse.ArgumentParser(description=__doc__)
    gg = g.add_mutually_exclusive_group(required=True)
    gg.add_argument("--emit", action="store_true")
    gg.add_argument("--check", action="store_true")
    gg.add_argument("--probe-islands", action="store_true")
    args = g.parse_args()

    errs = coverage_errors()
    if errs:
        print("coverage FAIL:")
        for e in errs:
            print("  -", e)
        sys.exit(2)

    html, own, islands = render()

    if args.emit:
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_text(html, encoding="utf-8")
        print(f"emit: {OUT.relative_to(ROOT)} — {len(D.ITEMS)} пунктов, "
              f"{len(disk_scan())} ключей диска покрыто")
        sys.exit(0)

    if args.check:
        if not OUT.exists():
            print("check: karta/index.html отсутствует — запустите --emit")
            sys.exit(1)
        if OUT.read_text(encoding="utf-8") != html:
            print("check: karta/index.html ДРЕЙФАНУЛ от диска/данных — перегенерируйте --emit")
            sys.exit(1)
        print(f"check: karta/index.html соответствует диску и данным ({len(D.ITEMS)} пунктов)")
        sys.exit(0)

    if args.probe_islands:
        print("probe: живой аудит ссылок карты…")
        fails = probe(own, islands)
        if fails:
            print(f"probe FAIL: {len(fails)} ссылок не 200:")
            for i, u, st in fails:
                print(f"  - {i} {st} {u}")
            sys.exit(1)
        print(f"probe OK: все {len(own) + len(islands)} ссылок отдают 200")


if __name__ == "__main__":
    main()
