# -*- coding: utf-8 -*-
"""Karta data — аннотации всех страниц домена gasyoun.github.io.

Правила:
- Каждый пункт имеет уникальный стабильный номер K### (никогда не переиспользуется,
  переживает переносы между секциями; рубрика — группировка, не часть идентичности).
- Собственные страницы домена (репо gasyoun.github.io) несут key = путь на диске
  (для каталога — с завершающим «/»); генератор сверяет диск с этим списком:
  unmapped-запись на диске = --emit падает со списком, --check дрейфует.
- Острова (project-pages других репо того же домена) несут url и не участвуют
  в дисковой сверке; живость проверяется режимом --probe-islands.
- Статусы: green = живой; amber = служебное/черновик; tomb = архив/мусор.
"""

SITE = "https://gasyoun.github.io"
H_REF = "H5527"  # обновляется после минта хендоффа

# key → section rubric ordering
SECTIONS = [
    ("A", "Тексты"),
    ("B", "Хитмапы и дашборды"),
    ("C", "ELI5 и объяснители"),
    ("D", "Исследовательские выкладки"),
    ("E", "Продукт и макеты"),
    ("F", "Процесс, аудит, служебное"),
    ("G", "Острова домена — project-pages других репо"),
]

# Разрешённые верхнеуровневые каталоги-ассеты: не контент, в карту не входят.
ASSET_DIRS = {"fonts", "images", "javascripts", "stylesheets", "scripts",
              ".github", ".claude", ".repowise", "karta"}

ITEMS = [
    # ---------- A. Тексты ----------
    dict(id="K001", sec="A", key="index.html", status="green",
         title="Ригведа — гимны (корень сайта)",
         note="Корневая index.html — та самая страница гимнов Ригведы (~12 МБ): деванагари, IAST, падапата. "
              "Живёт в корне с первых лет сайта и по решению MG (27-09-2026) остаётся тем, что видит посетитель корня."),
    dict(id="K002", sec="A", key="RV/", status="amber",
         title="RV — та же Ригведа под путём /RV/",
         note="Копия корневой страницы гимнов в подкаталоге; содержательно дублирует K001. "
              "Служебный дубль — при уборке сайта один из двух экземпляров можно свести."),
    dict(id="K003", sec="A", key="bookindex/toponyms-review-latest.html", status="green",
         title="Топоним-карта — последняя версия",
         note="Ревью топонимов (связка географических имён), файл latest — закладывайте именно его. "
              "Рядом лежат датированные версии v4.17.32–34."),
    dict(id="K004", sec="A", key="bookindex/", href="bookindex/toponyms-review-v4.17.34.html", status="tomb",
         title="bookindex — архив версий топоним-карты",
         note="Каталог держит исторические версии toponyms-review (v4.17.32, v4.17.33, v4.17.34). "
              "Архив: актуальная ссылка — всегда latest (K003)."),

    # ---------- B. Хитмапы и дашборды ----------
    dict(id="K005", sec="B", key="decision-heatmaps/", status="green",
         title="Decision heatmaps — куда идёт работа",
         note="Тепловые карты распределения текущей работы по направлениям. "
              "Дашборд для быстрых решений «куда вкладывать следующую неделю»."),
    dict(id="K006", sec="B", key="learner-heatmaps/", status="green",
         title="Learner heatmaps — вовлечение, воронка, SRS",
         note="Вовлечение учеников: воронка, повторения SRS, мастерство по drill-семьям. "
              "Учебная аналитика платформы на статической странице."),
    dict(id="K007", sec="B", key="sanskrit-heatmaps/", status="green",
         title="Sanskrit research heatmaps",
         note="Исследовательские тепловые карты по корпусу: sandhi × текст, лемма × период. "
              "Инструмент видения плотности языковых явлений в материалах."),
    dict(id="K008", sec="B", key="traffic-heatmaps/", status="green",
         title="Traffic heatmaps — Яндекс.Метрика",
         note="Куда реально идут посетители домена: снимки Яндекс.Метрики. "
              "Пара к learner-heatmap: внешние посетители против учебной телеметрии."),

    # ---------- C. ELI5 и объяснители ----------
    dict(id="K009", sec="C", key="eli5/", status="green",
         title="ELI5 — хаб объяснений",
         note="Индекс серии «объясни как пятилетнему»: подача домашки, сжатие видео, "
              "конвейер PWG→RU (H3970), сколько слов в санскрите (H5509). Страницы самодостаточны для отправки ссылкой."),
    dict(id="K010", sec="C", key="shunt-explained-ru.html", status="green",
         title="Шунт — как это работает",
         note="Объяснение шунта для неспециалиста, RU. Плейсхолдер технической серии ELI5 вне санскрита."),
    dict(id="K011", sec="C", key="coincidence-paradox-sanskrit.html", status="green",
         title="Парадокс совпадений на санскритских данных",
         note="Разбор парадокса дней рождения (Diaconis–Mosteller) на наших корпусных данных: "
              "почему «невероятные» совпадения форм закономерны. Переименовано по решению MG 26-09-2026."),

    # ---------- D. Исследовательские выкладки ----------
    dict(id="K012", sec="D", key="zalizniak-2026/", status="green",
         title="Родня слов: когнаты из конспекта Зализняка",
         note="Санскрит и пять языков — когнатические пары из конспекта Зализняка; генерируется build_page.py. "
              "В каталоге ещё страницы лекций, НКРЯ-срезы и числительные (gen_lectures / gen_nkrya / gen_numbers)."),
    dict(id="K013", sec="D", key="fasmer-2026/", status="green",
         title="Фасмер: др.-инд. заимствования, 2026",
         note="Статистика древнеиндийских следов в словаре Фасмера с вариантами подачи (short/middle/original, «детям»). "
              "Рядом загадки (gen_riddles.py) и решенийый DECISIONS-файл от 25-09-2026."),
    dict(id="K014", sec="D", key="sanskrit-cognates-zalizniak-2026/", href="sanskrit-cognates-zalizniak-2026/index.html", status="tomb",
         title="Старый адрес когнат-страницы",
         note="Страница переехала: актуальное содержимое живёт в zalizniak-2026 (K012). "
              "Каталог оставлен как редирект для старых ссылок."),
    dict(id="K015", sec="D", key="reverse22-output/", href="reverse22-output/reversesorted3.html", status="green",
         title="Реверс деванагари — итерация 22",
         note="Обратная сортировка словоформ (reversesorted3.html) — последняя итерация реверс-конвейера. "
              "Рабочий материал для словообразовательного поиска «с конца»."),
    dict(id="K016", sec="D", key="reverse21-output/", href="reverse21-output/devanagarisorted3.html", status="tomb",
         title="Реверс деванагари — итерация 21",
         note="Промежуточная итерация реверс-выкладки; заменена K015. Держится для истории сравнения."),
    dict(id="K017", sec="D", key="reverse20-output/", href="reverse20-output/devanagarisorted3.html", status="tomb",
         title="Реверс деванагари — итерация 20",
         note="Первая итерация реверс-выкладки; заменена K015. Каталог переименован из «reverse20-ouput» "
              "(опечатка в имени) 27-09-2026 (H5530); ссылки на прежнее имя больше не работают."),
    dict(id="K018", sec="D", key="PWGagainstMW.html", status="amber",
         title="PWG против MW",
         note="Сверка статей PWG с Monier-Williams: параллельные выписки для проверки полноты перевода. "
              "Старый XHTML без <title>; служебная страница конвейера PWG→RU."),

    # ---------- E. Продукт и макеты ----------
    dict(id="K019", sec="E", key="diagrams/", href="diagrams/sanskrit-domain-landscape.html", status="green",
         title="Диаграммы поместья — 8 карт экосистемы",
         note="Визуальные карты проекта: ландшафт работ, поток данных, treemap данных, repo-экосистема, "
              "CDSL-спина «один источник — 44 словаря», конвейер статей, лента событий, мегакнига ELI5. "
              "Свежая волна от 24-09-2026."),
    dict(id="K020", sec="E", key="campus/", status="green",
         title="Кампус наглядности",
         note="«Санскритское имение одним входом» — кампус-лендинг наглядных материалов. "
              "Генерируется scripts/campus/campus_build.py: править генератор, не HTML."),
    dict(id="K021", sec="E", key="mastery/index.html", status="green",
         title="Карта мастерства — map-вариант",
         note="Пять drill-семей навыков ученика на одной карте. Каноничный билд — mastery_map_build.py "
              "(дуал-ран LEDGER в scripts/campus)."),
    dict(id="K022", sec="E", key="mastery/stats.html", status="green",
         title="Карта мастерства — stats-вариант",
         note="Та же система пяти семей в статистической подаче. Второй вариант из дуал-рана mastery-страниц."),
    dict(id="K023", sec="E", key="mockups/h3457-wpage-ux/", href="mockups/h3457-wpage-ux/favorites.html", status="amber",
         title="UX-макеты страниц слов kosha",
         note="Четыре направления дизайна (A–D на глаголе gam) плюс избранное — макеты страницы слова из H3457. "
              "Черновой материал для выбора направления UX."),
    dict(id="K024", sec="E", key="h3457-compare/", status="green",
         title="Страницы слов kosha: до / после",
         note="Наглядное сравнение текущих и переработанных страниц слов kosha из H3457. "
              "Аргументационная страница для апрува редизайна."),
    dict(id="K025", sec="E", key="h3744-sense-align/", status="green",
         title="Согласованные значения PWG · MW · Apte · ŚKDR · VCP",
         note="Сравнение словарных значений до/после согласования (H3744 + H3862). "
              "Показывает выравнивание пяти словарей на одних и тех же статьях."),
    dict(id="K026", sec="E", key="edtech-system-map.html", status="green",
         title="Edtech System Map — для внешнего ИИ",
         note="Карта edtech-системы института, написанная как контекст для внешних ИИ-агентов. "
              "Одностраничный вход в устройство продуктов."),
    dict(id="K027", sec="E", key="preview/", href="preview/kanva_weekly_preview_2026-09-10.html", status="amber",
         title="Недельные превью «Кто на чём закончил»",
         note="Превью-версии недельного отчёта кампуса от 09-09-2026. Служебные снимки перед публикацией в кампусе."),

    # ---------- F. Процесс, аудит, служебное ----------
    dict(id="K055", sec="E", key="mindmaps/", status="green",
         title="Марки-карты — 55 страниц по репо и темам",
         note="Волна markmap-карт (H5525/H5526, решения MG 27-09-2026): по одному на репо поместья и на сквозные темы. "
              "Приватные имена замаскированы по решению H5433-3; вход — index.html."),
    dict(id="K028", sec="F", key="vote/", status="green",
         title="Vote — хаб обзоров-голосований",
         note="Публичный хаб ревью-листов (H2755): бюллетени решений, голосуемые с гитхаб-страниц. "
              "Канонический домен голосований организации."),
    dict(id="K029", sec="F", key="infographics/", status="green",
         title="Инфографики — живой индекс",
         note="Индекс инфографик санскритского архива, генерируемый с диска (H3768, --emit/--check паритет). "
              "Прямой предшественник этой самой карты."),
    dict(id="K030", sec="F", key="audit-probes.html", status="green",
         title="Audit probes — библиотека проб",
         note="Библиотека аудит-проб: клик копирует однострочник, раскрытие даёт доказательство. "
              "Рабочий инструмент проверок серверов и пайплайнов."),
    dict(id="K031", sec="F", key="audit-probes-history.html", status="green",
         title="Audit probes — история запусков",
         note="История и свежесть запусков аудит-проб. Дополняет библиотеку K029."),
    dict(id="K032", sec="F", key="audit-probes-one-line-2026-08-29.html", status="amber",
         title="Однострочные аудит-пробы (снимок 29-08)",
         note="Датированный снимок набора однострочных проб. Служебная фиксация состояния на 29-08-2026."),
    dict(id="K033", sec="F", key="fruit-status.html", status="green",
         title="Fruit top picks",
         note="Статусная страница фруктовых пиков проекта. Живая, правится по ходу сезона."),
    dict(id="K034", sec="F", key="todo/index.html", status="amber",
         title="Todo — runbook миграции Mac → OpenCode",
         note="Чеклист переноса рабочего окружения на OpenCode. Служебная страница-задачник."),
    dict(id="K035", sec="F", key="todo/voice.html", status="amber",
         title="Voice-clone bake · чеклист M4",
         note="Чеклист запекания voice-клона (этап M4). Служебная страница-задачник."),
    dict(id="K036", sec="F", key="handy-dictation-playbook-2026-09-21.html", status="green",
         title="Диктовка на MSI (кнопка *)",
         note="Плейбук диктовки с самопроверкой и ремонтом на MSI-машине. Датированный практический мануал."),
    dict(id="K037", sec="F", key="kostya-covers-tz-2026-09-10.html", status="amber",
         title="ТЗ: автообложки уроков — Костя",
         note="Техническое задание на чистый шаблон автообложек уроков. Рабочий документ соавторства с Константином."),
    dict(id="K038", sec="F", key="subhashita-audio-compare-2026-09-14.html", status="green",
         title="Субхашиты: Бётлингк ↔ наши материалы",
         note="Аудио-сравнение субхашитов (H4474): записи Бётлингка против наших озвучек. "
              "Исследовательская страница серии аудио-сверок."),
    dict(id="K039", sec="F", key="teacher-anons-letters-29-08-2026.html", status="green",
         title="Письма преподавателям — осенняя программа",
         note="Заявки-анонсы для преподавателей на осеннюю программу от 29-08-2026. Датированная рассылочная страница."),
    dict(id="K040", sec="F", key="h2582/", href="h2582/index.md", status="green",
         title="H2582 — публичные копии артефактов исследования",
         note="Два из 13 артефактов исследования «samskrte.ru vs Sanskritorium»: скоркарты и 21 рекомендация. "
              "Выложены как фетчабельный вход для Deep Research; каноничное множество — в приватном репо."),
    # ---------- G. Острова домена ----------
    dict(id="K042", sec="G", url="kosha/", status="green",
         title="kosha — словарный поиск для переводчика",
         note="Translator-first lookup над экосистемой Cologne (CDSL): мульти-словарный вид, поиск по словоформе, "
              "скан-ссылки. Клей между словарями, переиспользующий готовое."),
    dict(id="K043", sec="G", url="SanskritLexicography/", status="green",
         title="SanskritLexicography — PWG: переводы статей (RU / EN)",
         note="Публичный сайт PWG-переводов статей с резолвером скан-ссылок. Витрина главного переводческого конвейера."),
    dict(id="K044", sec="G", url="pwg-ru-lod/", status="green",
         title="pwg-ru-lod — dereferenceable LOD для w3id.org",
         note="Цель dereference для пространства w3id.org/sanskrit-lexicon: SHACL-профиль, словарь и модельные доки "
              "графа PWG→RU. Данные ждут шлюза допуска значений G5."),
    dict(id="K045", sec="G", url="Systema-Sanscriticum/", status="green",
         title="Systema Sanscriticum — платформа онлайн-обучения",
         note="Прод-платформа обучения санскриту (личные кабинеты, курсы Парибока). Живой прод на 193.232.229.92."),
    dict(id="K046", sec="G", url="IndologyScholars/", status="green",
         title="IndologyScholars — индологическая наука РФ",
         note="Единый архив и статистический дашборд российской индологии: ETL-конвейер + статический сайт конференции."),
    dict(id="K047", sec="G", url="RussianRamayana/", status="green",
         title="RussianRamayana — Русская Рамаяна",
         note="Перевод и комментирование Рамаяны Вальмики. Публичное читалище перевода."),
    dict(id="K048", sec="G", url="SamasaChakram/", status="green",
         title="SamasaChakram — колесо самас",
         note="Samasa Chakram reinvented: интерактивный разбор типов санскритских сложений."),
    dict(id="K049", sec="G", url="SamudraManthanam/", status="green",
         title="SamudraManthanam — «Пахтанье океана»",
         note="Оффлайн-поисковик «Пахтанье океана». Десктоп-утилита с публичной страницей."),
    dict(id="K050", sec="G", url="SanskritKaraoke/", status="green",
         title="SanskritKaraoke — Shlokas in Waves",
         note="Шлоки в волнах: караоке-подача санскритских стихов с синхронизацией аудио и текста."),
    dict(id="K051", sec="G", url="SanskritMacros/", status="green",
         title="SanskritMacros — макросы EmEditor / Excel / Word",
         note="Набор макросов и скриптов для работы с санскритом в офисных программах. Инструментальная витрина."),
    dict(id="K052", sec="G", url="SanskritRussian/", status="green",
         title="SanskritRussian — глоссарий санскрит→русский",
         note="Глоссарий (поверхность · лемма · корень) из выровненного корпуса в 1.09 млн токенов, с поиском."),
    dict(id="K053", sec="G", url="WhitneyRoots/", status="green",
         title="WhitneyRoots — корни по Уитни",
         note="Переосмысление samskrtam.ru/whitney-roots: корневая система Уитни в интерактивной подаче."),
    dict(id="K054", sec="G", url="ZalizniakVideo/", status="green",
         title="ZalizniakVideo — архив видеозаписей Зализняка",
         note="192 видеотранскрипта А. А. Зализняка: архив с поиском по расшифровкам."),
    dict(id="K056", sec="F", key="handoff-status/", status="green",
         title="Handoff-status — публичное зеркало статуса хендоффов",
         note="Ежечасный bot-refresh статусов хендоффов поместья; вход — index.html."),
    dict(id="K057", sec="F", key="payroll/", status="amber",
         title="Payroll — ведомости зарплат",
         note="Ведомости авг+сен 2026 (noindex/nofollow, robots-block; на github.com репо публичны). "
              "Решение по доступу — GTD @DO 0O3, ожидает MG (bughunt 04-10-2026)."),
    dict(id="K058", sec="F", key="runbook-h3348-artem-root-session-2026-10-01.html", status="amber",
         title="Рунбук H3348 — root-сессия на .95",
         note="Служебный рунбук: искоренение импланта samskrtam.ru (Artem, root-сессия)."),
    dict(id="K059", sec="F", key="telegram-artem-h3348-2026-10-01.html", status="amber",
         title="Сообщение Артёму — root-сессия H3348",
         note="Служебная выгрузка сообщения Артёму по root-сессии samskrtam.ru."),
]

STATUS_BADGE = {
    "green": "🟢",
    "amber": "🟡",
    "tomb": "⚰️",
}

STATUS_LEGEND = {
    "green": "живой",
    "amber": "служебное / черновик",
    "tomb": "архив / мусор",
}
