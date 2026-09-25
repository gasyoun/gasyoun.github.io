# -*- coding: utf-8 -*-
"""Генератор дополнительных страниц zalizniak-2026 (MG 25-09-2026, дедлайн 12:00).

1. dcs-top.html      — топ-50 частотных DCS-лемм, у которых есть русские параллели
                       в выборке Зализняка (kosha-lemma-frequency, LEFT-JOIN).
2. fasmer-extra.html — полная таблица 1238 статей Fasmer fasmer-dr-ind, которых
                       нет в выборке Зализняка, + школьная 50-ка сверху.

Источники (абсолютные пути на машинe сборки, MG 25-09-2026):
  * SamudraManthanam/web/corpus_builder/jsonl/fasmer-dr-ind.jsonl (разобранный Фасмер)
  * kosha/data/frequency/lemma_frequency.tsv (DCS lemma frequency, SLP1, 83 277 строк)

Метод: формальное сопоставление по «скелету» транслитерации (NFKD-нормализация,
diacritics off, ç→s; SLP1→скелет), корни — по префиксу. Это НЕ этимологическая
верификация; сомнительные пары отброшены вручную (EXCLUDE), у дублей выбрана
нужная статья (PREFER). Отобрано вручную: MG утвердил топ-50 и школьную 50-ку.
"""
import io, re, json, unicodedata, importlib.util, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.stdout.reconfigure(encoding="utf-8")

FASMER_JSONL = r"C:/Users/user/Documents/GitHub/SamudraManthanam/web/corpus_builder/jsonl/fasmer-dr-ind.jsonl"
DCS_TSV = r"C:/Users/user/Documents/GitHub/kosha/data/frequency/lemma_frequency.tsv"

# ---------- данные страницы ----------
spec = importlib.util.spec_from_file_location("bp", os.path.join(HERE, "build_page.py"))
bp = importlib.util.module_from_spec(spec); spec.loader.exec_module(bp)
M = bp.M

def skel(w):
    w = unicodedata.normalize("NFKD", w.lower())
    w = "".join(c for c in w if not unicodedata.combining(c))
    return re.sub(r"[^a-z]", "", w.replace("ç", "s"))

def slp1_skel(w):
    t = str.maketrans({"f": "ri", "F": "l", "x": "ri", "X": "l", "M": "m", "H": "h",
                       "z": "s", "S": "s", "c": "s", "w": "t", "q": "d"})
    return re.sub(r"[^a-z]", "", w.lower().translate(t))

def slp1_iast(w):
    t = str.maketrans({"A": "ā", "I": "ī", "U": "ū", "f": "ṛ", "F": "ḷ", "x": "ṝ", "X": "ḹ",
                       "E": "ai", "O": "au", "z": "ś", "S": "ṣ", "w": "ṭ", "W": "ṭh",
                       "q": "ḍ", "Q": "ḍh", "K": "kh", "G": "gh", "C": "ch", "J": "jh",
                       "T": "th", "D": "dh", "N": "ṇ", "P": "ph", "B": "bh",
                       "M": "ṃ", "H": "ḥ"})
    return w.translate(t)

# ручная чистка (MG-правило: формальный отбор, сомнительное — вон)
EXCLUDE = {"Darma", "dravya", "kriyA", "tAmra", "vicitra", "Siva", "ga", "mA",
           "kṛ", "kf", "varRa", "vidhi", "viDi", "darSana", "garbha", "pFthivI",
           "mArga", "drava", "sadA", "Sru", "zru"}
PREFER = {"vara": "VAR₂ 9", "gaRa": "GAR 9 •", "marday": "MAR₂ 9 •", "su": "SŪ 2",
          "sama": "sama‑"}
# статьи конспекта, все машинные матчи которых — ложные (ручная чистка 25-09)
BLOCK_SAN = {"KRĪ 9", "VAR 5", "PRĪ 9", "PIṢ 7", "MAR 1", "SAD —",
             "GAR₂ 6 •", "DAR 9 •"}

def fasmer_set():
    F = {}
    for l in io.open(FASMER_JSONL, encoding="utf-8"):
        r = json.loads(l)
        if r["passage"] in ("e1", "e2"):
            continue
        m = re.search(r"<td><p>(.*?)</p>", r["html"])
        if not m:
            continue
        hw = re.sub(r"<[^>]+>", "", m.group(1))
        gloss = re.sub(r"<[^>]+>", "", r["text"])
        gloss = re.sub(r"\s+", " ", gloss).strip()
        n = norm_ru(hw)
        if n and n not in F:
            F[n] = (hw, gloss)
    return F

def norm_ru(w):
    w = unicodedata.normalize("NFKD", w)
    w = "".join(c for c in w if not unicodedata.combining(c)).lower().replace("ё", "е")
    w = re.sub(r"\(.*?\)", "", w)
    w = w.split("‘")[0]
    w = re.sub(r"[^а-яъыэь \-]", "", w)
    return w.strip(" -–—")

F = fasmer_set()
Zw = {}
for m in M:
    for w in m["ru"]:
        n = norm_ru(w)
        if n:
            Zw.setdefault(n, (w, m))
fony = sorted(set(F) - set(Zw))

# ---------- 1. fasmer-extra.html ----------
SCHOOL_50 = ["балагур", "баловать", "берлога", "беседа", "болото", "борщ", "бревно",
             "бубен", "буря", "быть", "ведро", "верблюд", "веретено", "верх", "веселый",
             "вещь", "веять", "вид", "внук", "воин", "возить", "волос", "ворожить",
             "ворота", "восемь", "вошь", "время", "встретить", "второй", "гавкать",
             "гнуть", "год", "голос", "горе", "горох", "готовый", "губа", "давать",
             "два", "двор", "девять", "диво", "дождь", "дорогой", "дуб", "дума",
             "дуть", "заяц", "земля", "злой"]
school_rows, seen = [], set()
F_BY_HW = {v[0]: v[1] for k, v in F.items()}
for hw in F_BY_HW:
    pass
for w in SCHOOL_50:
    for n, (hw, gloss) in F.items():
        base = re.sub(r"[^а-я]", "", hw.lower().replace("ё", "е"))
        if w == base and w not in seen:
            seen.add(w)
            school_rows.append((hw, gloss[:110]))
school_rows = [r for r in school_rows][:50]

def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

full_rows = "\n".join(
    "<tr><td>%d</td><td class='w'>%s</td><td class='g'>%s…</td></tr>"
    % (i, esc(F[n][0]), esc(F[n][1]))
    for i, n in enumerate(fony, 1))

school_html = "\n".join("<li><b>%s</b> — %s…</li>" % (esc(hw), esc(gl[:80]))
                        for hw, gl in school_rows)

fasmer_extra = """<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Фасмер: 1238 статей с др.-инд. вне выборки Зализняка — zalizniak-2026</title>
<style>
  body{margin:0;background:#faf6ee;color:#26221c;font:17px/1.6 Georgia,serif}
  main{max-width:1000px;margin:0 auto;padding:30px 18px 70px}
  h1{color:#8a3324;font-size:1.7rem}
  h2{color:#2f5d50;border-bottom:2px solid #e4dcc9;padding-bottom:5px}
  .note{color:#6b6353;font-size:.88rem;font-style:italic}
  table{width:100%%;border-collapse:collapse;background:#fffdf8;font-size:.88rem;
        font-family:"Segoe UI",system-ui,sans-serif;margin:12px 0}
  th{background:#efe7d3;text-align:left;padding:6px 8px;border:1px solid #e4dcc9}
  td{border:1px solid #e4dcc9;padding:5px 8px;vertical-align:top}
  td.w{font-weight:600;color:#8a3324;white-space:nowrap}
  td.g{color:#55503f}
  .school{background:#fffdf8;border:1px solid #e4dcc9;border-radius:12px;padding:10px 24px}
  .school li{margin:3px 0}
  .cols2{columns:2;column-gap:36px;font-size:.92rem}
  a{color:#2f5d50}
</style>
</head>
<body>
<main>
<p><a href="index.html">← Когнаты Зализняка: сводная страница</a></p>
<h1>Фасмер: 1238 статей с др.-инд. параллелями, которых нет в выборке Зализняка</h1>
<p class="note">Полный список «F-only»: статьи «Этимологического словаря русского языка» М. Фасмера, где есть древнеиндийская параллель, но соответствующего слова нет в русской колонке конспекта Зализняка (1408/1410 статей fasmer-dr-ind минус 167 пересечений; нормализация: строчные, без ударений, ё→е). Многое здесь — областная, диалектная и говорная лексика, а также производные; зато среди них — хорошо известные школьные слова.</p>

<h2>Школьная пятидесятка (самые узнаваемые)</h2>
<ol class="school cols2">
%s
</ol>

<h2>Все 1238 заголовков (с началом фасмеровской статьи)</h2>
<table>
<tr><th>№</th><th>Слово</th><th>Статья Фасмера (начало)</th></tr>
%s
</table>
<p class="note">Источник: fasmer-dr-ind (SamudraManthanam), разбор и выкладка 25-09-2026. Метод и пересечение со Зализняком — на <a href="index.html#fasmer">сводной странице, раздел VII</a>.</p>
</main>
</body>
</html>
""" % (school_html, full_rows)
io.open(os.path.join(HERE, "fasmer-extra.html"), "w", encoding="utf-8").write(fasmer_extra)
print("fasmer-extra.html:", len(school_rows), "school rows,", len(fony), "full rows")

# ---------- 2. dcs-top.html ----------
exact, root_pref = {}, {}
for m in M:
    if not m["ru"]:
        continue  # только статьи с русскими параллелями
    ms = skel(m["san"])
    if not ms:
        continue
    if m["sec"] == "К" and len(ms) >= 3:
        root_pref.setdefault(ms, []).append(m)
    else:
        exact.setdefault(ms, []).append(m)

best = {}
with io.open(DCS_TSV, encoding="utf-8") as fh:
    fh.readline()
    for l in fh:
        p = l.split("\t")
        try:
            cnt = int(p[1])
        except Exception:
            continue
        s = slp1_skel(p[0])
        if len(s) < 2 or p[0] in EXCLUDE:
            continue
        cands = exact.get(s) or (len(s) >= 3 and next(
            (root_pref[s[:k]] for k in range(3, len(s) + 1) if s[:k] in root_pref), None)) or []
        for m in cands:
            if m["san"] in BLOCK_SAN:
                continue
            if PREFER.get(p[0]) and m["san"] != PREFER[p[0]]:
                continue
            if m["n"] not in best or best[m["n"]][0] < cnt:
                best[m["n"]] = (cnt, p[0], m)

pairs = sorted(best.values(), key=lambda t: -t[0])[:50]
rows = "\n".join(
    "<tr><td>%d</td><td class='w'>%s</td><td>%s</td><td class='san'>%s</td>"
    "<td>%s</td><td class='ru'>%s</td></tr>"
    % (i, esc(slp1_iast(slp)), "{:,}".format(cnt).replace(",", " "),
       esc(m["san"]), esc(m["gloss"]), esc(" · ".join(m["ru"])))
    for i, (cnt, slp, m) in enumerate(pairs, 1))

dcs_top = """<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Топ-50 частотных санскритских слов с русскими параллелями (DCS) — zalizniak-2026</title>
<style>
  body{margin:0;background:#faf6ee;color:#26221c;font:17px/1.6 Georgia,serif}
  main{max-width:1000px;margin:0 auto;padding:30px 18px 70px}
  h1{color:#8a3324;font-size:1.7rem}
  .note{color:#6b6353;font-size:.88rem;font-style:italic}
  table{width:100%%;border-collapse:collapse;background:#fffdf8;font-size:.92rem;
        font-family:"Segoe UI",system-ui,sans-serif;margin:12px 0}
  th{background:#efe7d3;text-align:left;padding:7px 9px;border:1px solid #e4dcc9}
  td{border:1px solid #e4dcc9;padding:6px 9px;vertical-align:top}
  td.w{font-weight:600;color:#8a3324;white-space:nowrap}
  td.san{font-weight:600;color:#8a3324;white-space:nowrap}
  td.ru{font-weight:600;color:#2f5d50}
  a{color:#2f5d50}
</style>
</head>
<body>
<main>
<p><a href="index.html">← Когнаты Зализняка: сводная страница</a></p>
<h1>Топ-50 частотных санскритских слов, у которых есть русские параллели</h1>
<p class="note">Частота — число словоупотреблений леммы в корпусе DCS (Digital Corpus of Sanskrit, ~5,4 млн токенов; sidecar kosha-lemma-frequency, whole-corpus). Параллели — из русской колонки конспекта Зализняка на сводной странице. Сопоставление формальное, по скелету транслитерации (корни — по префиксу); сомнительные пары отброшены вручную. Это <b>не</b> этимологическая верификация: перед цитированием сверяйтесь со статьёй Зализняка (№ — сквозной номер на сводной странице).</p>
<table>
<tr><th>№</th><th>Санскрит (DCS-лемма)</th><th>Частота в DCS</th><th>Статья Зализняка</th><th>Что значит</th><th>Русские параллели</th></tr>
%s
</table>
<p class="note">Частотные служебные слова (ca «и», tad «тот», na «не»…) не включались: у них нет русских параллелей в конспекте. Полный список сопоставлений (105 пар) можно восстановить скриптом build_extras.py. Данные: kosha-lemma-frequency (CC BY-SA 4.0), DCS (Oliver Hellwig, CC BY 4.0).</p>
</main>
</body>
</html>
""" % rows
io.open(os.path.join(HERE, "dcs-top.html"), "w", encoding="utf-8").write(dcs_top)
print("dcs-top.html rows:", len(pairs))
