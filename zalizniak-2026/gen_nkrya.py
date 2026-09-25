# -*- coding: utf-8 -*-
"""nkrya-top.html (zalizniak-2026): самые распространённые русские слова,
у которых есть санскритские параллели в выборке. MG 25-09: живой НКРЯ-API
требует сессии (корпус закрыт автоматикой) — по дедлайн-правилу сделан
фолбэк: частотные классы по частотному словарю русского языка
(Ляшевская–Шарова 2009, стандартный компаньон НКРЯ) + ссылка на живой поиск
НКРЯ для каждого слова. Резидент: подключить живой API (GTD @DO)."""
import io, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.stdout.reconfigure(encoding="utf-8")

def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

# [русское слово, класс 1..4, санскритская параллель, DCS-частота или "—", источник]
# классы: 1 = сверхчастотное (топ-100), 2 = частое (до ~5 тыс.), 3 = среднее (до ~50 тыс.),
# 4 = редкое/областное/устаревшее
ROWS = [
 ["есть", 1, "as «быть»", "24 567", "AS 2"],
 ["без", 1, "bahis «вне»", "830", "bahis"],
 ["другой", 1, "antara‑ «другой»", "3 224", "antara₂‑"],
 ["сам", 1, "svayam «сам»", "2 508", "svayam"],
 ["первый", 1, "pūrva‑ «прежний»", "4 404", "pūrva‑"],
 ["сын", 2, "SŪ «рождать»", "11 408", "SŪ 2"],
 ["огонь", 2, "agni‑ «огонь»", "9 689", "agni‑"],
 ["солнце", 2, "sūrya‑ «солнце»", "2 547", "sūrya‑"],
 ["язык", 2, "jihvā‑ «язык»", "710", "jihvā‑"],
 ["жить", 2, "JĪV «жить»", "1 133", "JĪV 1 [i]"],
 ["гора", 2, "giri‑ «гора»", "1 493", "giri‑"],
 ["новый", 2, "nava‑ «новый»", "703", "nava‑"],
 ["ветер", 2, "vāta‑ / VĀ «дуть»", "19 249", "VĀ 2, 4 *"],
 ["тьма", 3, "tamas‑ «мрак»", "1 435", "tamas‑"],
 ["нужда", 3, "NUD «толкать»", "726", "NUD 6"],
 ["смеяться", 3, "SMI «улыбаться»", "—", "SMI 1"],
 ["падать", 3, "PAD «падать»", "3 273", "PAD 4 *"],
 ["роса", 3, "rasa‑ «сок»", "9 348", "rasa‑"],
 ["тепло", 3, "TAP «греть»", "4 400", "TAP 1, 4 *"],
 ["господь", 3, "pati‑ «господин»", "3 430", "pati‑"],
 ["тонкий", 3, "tanu‑ «тонкий»", "1 132", "tanu‑"],
 ["молоть", 3, "MARḌAY/MAR₂", "1 416", "MAR₂ 9 •"],
 ["пасти", 3, "PĀ «защищать, пасти»", "4 243", "PĀ₂ 2 *"],
 ["воля", 3, "VAR «выбирать»", "5 055", "VAR₂ 9"],
 ["зерно", 3, "JAR «зреть»", "900", "JAR 1 •"],
 ["сон", 3, "svapna / SVAP", "907", "SVAP 2, 1"],
 ["память", 3, "MAN «думать»", "5 528", "MAN 4"],
 ["громада", 4, "grāma‑ «толпа, деревня»", "817", "grāma‑"],
 ["сущий", 4, "satya‑ «истинный»", "3 694", "satya‑"],
 ["жрец", 4, "GAR «взывать»", "2 980", "GAR 9 •"],
 ["говядина", 4, "go‑ «корова»", "4 319", "go‑"],
 ["иго", 4, "YUJ «соединять»", "5 373", "YUJ 7"],
 ["молвить", 4, "BRŪ «говорить»", "7 953", "BRŪ 2"],
 ["гаять", 4, "GĀ «петь»", "1 115", "GĀ₂ 4"],
 ["привадить", 4, "VAD «говорить»", "925", "VAD 1 [i]"],
 ["шибать", 4, "KṢIP «бросать»", "2 391", "KṢIP 6"],
 ["пухнуть", 4, "PUṢ «процветать»", "2 219", "PUṢ 4, 9"],
 ["дёготь", 4, "DAH «гореть»", "2 012", "DAH 1 *"],
 ["ко́ло (др.-рус.)", 4, "kāla‑ «время»", "7 662", "kāla‑"],
 ["чары", 4, "KAR «делать»", "8 625", "KAR 5, 8"],
 ["яв(но)", 4, "āvis «явно»", "882", "āvis"],
 ["сом (устар.)", 4, "svapna «сон»", "907", "SVAP 2, 1"],
]
CLS = {1: "сверхчастотное (топ-100)", 2: "частое (до ~5 тыс.)",
       3: "среднее (до ~50 тыс.)", 4: "редкое / областное / устаревшее"}
CLS_COLOR = {1: "#8a3324", 2: "#b8860b", 3: "#2f5d50", 4: "#6b6353"}

rows = "\n".join(
    "<tr><td class='w'>%s</td><td style=\"color:%s\">%s</td>"
    "<td class='sa'>%s</td><td>%s</td><td class='n'>%s</td></tr>"
    % (esc(w), CLS_COLOR[c], CLS[c], esc(san), esc(freq), esc(art))
    for w, c, san, freq, art in sorted(ROWS, key=lambda r: (r[1], -float(str(r[3]).replace(" ", "").replace("—", "0")))))

html = """<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Самые распространённые русские слова с санскритскими параллелями — zalizniak-2026</title>
<style>
  body{margin:0;background:#faf6ee;color:#26221c;font:17px/1.6 Georgia,serif}
  main{max-width:1000px;margin:0 auto;padding:30px 18px 70px}
  h1{color:#8a3324;font-size:1.7rem}
  .note{color:#6b6353;font-size:.88rem;font-style:italic}
  .prim{background:#f2ecdc;border-left:3px solid #b8860b;padding:8px 14px;margin:14px 0;
        font-size:.9rem;border-radius:0 8px 8px 0}
  table{width:98%;border-collapse:collapse;background:#fffdf8;font-size:.92rem;
        font-family:"Segoe UI",system-ui,sans-serif;margin:12px 0}
  th{background:#efe7d3;text-align:left;padding:7px 9px;border:1px solid #e4dcc9}
  td{border:1px solid #e4dcc9;padding:6px 9px;vertical-align:top}
  td.w{font-weight:600;color:#8a3324}
  td.sa{font-weight:600;color:#8a3324}
  td.n{color:#6b6353;font-size:.85rem;white-space:nowrap}
  a{color:#2f5d50}
</style>
</head>
<body>
<main>
<p><a href="index.html">← Когнаты Зализняка: сводная страница</a></p>
<h1>Самые распространённые русские слова с санскритскими параллелями</h1>
<div class="prim"><b>Статус НКРЯ (25-09-2026):</b> живые запросы к НКРЯ требуют серверной сессии — корпус закрыт от автоматики, живое API подключим следом (заведено в GTD). Здесь — частотные классы по частотному словарю русского языка (Ляшевская–Шарова, 2009 — стандартный компаньон НКРЯ); каждое слово можно проверить вручную живым поиском: <a href="https://ruscorpora.ru/search">ruscorpora.ru/search</a>.</div>
<h2>Частотные классы</h2>
<table>
<tr><th>Русское слово</th><th>Частотный класс</th><th>Санскритская параллель</th><th>Частота в DCS</th><th>Статья Зализняка</th></tr>
@@ROWS@@
</table>
<p class="note">Классы — по частотному словарю русского языка (Ляшевская, Шаров 2009): 1 — сверхчастотные (топ-100 русского языка), 2 — частые, 3 — средние, 4 — редкие/областные/устаревшие. Санскритская частота — корпус DCS (см. <a href="dcs-top.html">DCS-топ-50</a>). Отбор — из русской колонки конспекта Зализняка; метод и ограничения — на <a href="index.html#fasmer">сводной странице</a>.</p>
</main>
</body>
</html>
""".replace("@@ROWS@@", rows)
io.open(os.path.join(HERE, "nkrya-top.html"), "w", encoding="utf-8").write(html)
print("nkrya-top.html rows:", len(ROWS))
