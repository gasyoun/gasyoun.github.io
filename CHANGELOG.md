# CHANGELOG — gasyoun.github.io

Формат: дата · хендофф · что изменилось. Новые записи сверху.

## 07-11-2026 — /wiki/: Etymology explorer + Cognate map + Timeline of layers

- **Добавлено:** [wiki/explorer.html](https://gasyoun.github.io/wiki/explorer.html) — поиск по 3 164 реальным леммам (3 419 членств, 229 слов сразу в нескольких категориях, 22 `Reconstruction:`-вхождения), фильтры по линзе/категории/сортировке, режим «Source buckets» на 2 005 вложенных категорий (PIE-корни, языки-доноры, суффиксы, префиксы), панель cross-listed слов и отдельный список двух заголовков из namespace `Template:`, чтобы из архива ничего не пропадало. Каждое слово и каждый тег — ссылка на Wiktionary.
- **Добавлено:** [wiki/cognates.html](https://gasyoun.github.io/wiki/cognates.html) — матрица 18 PIE корней/слов × 8 языков (Sanskrit, Avestan, Proto-Indo-Iranian, Vedic Sanskrit, Ancient Greek, Latin, Old English, English), собранная из 114 per-language категорий Wiktionary; фильтр по ветви, панель sound correspondences на 4 языка, языковые якоря (`#Ancient_Greek`, `#Latin`, …), ссылка на каждый рефлекс и на всю категорию. Прямо проговорено, что членство в категории ≠ прямое родство.
- **Добавлено:** [wiki/timeline.html](https://gasyoun.github.io/wiki/timeline.html) — 10 слоёв: 4 реальных категории наследования (2 376 / 2 058 / 1 229 / 1 слов по общему юниту), затем dhātu+аффиксы, samāsa, vṛddhi, заимствования, Sanskritization, и слой неизвестного. Бары масштабируются только внутри своего трека: `c`, `e` и «члены категории» не складываются. Эпохи помечены как общепринятые учебные подсказки, а не данные источника.
- **Добавлено:** общий `nav.sitenav` на всех пяти страницах; `style.css` — компоненты statrow / tabs / matrix / timeline / wordlist / buckets. Проверено DOM-stub прогоном: 101 / 4 605 / 1 779 / 264 / 56 сгенерированных ссылок, ни одного `undefined`, `NaN` или неразрешённого `href="#"`, все локальные ссылки существуют; форматы URL (деванагари, `Reconstruction:`, `Category:*`, греческий/авестийский рефлекс, PIE-реконструкция) дают HTTP 200.
- **Данные:** [wiki/data/lemmata.js](https://github.com/gasyoun/gasyoun.github.io/blob/master/wiki/data/lemmata.js) (инвертированный индекс дерева), `data/cognates.js`, `archive/raw/cognates.json` (175 КБ), `archive/cognates-manifest.json` (118 точных URL). Новые генераторы `wiki/scripts/fetch_cognates.py`, `wiki/scripts/etymology_meta.py`; `fetch_snapshot.py` теперь умеет `--offline` — пересобирает все производные файлы из `raw/` без сети, сохраняя исходную метку времени и контрольные суммы (идемпотентно).
- **Изменено:** `archive/manifest.json` / `data/manifest.js` / `SNAPSHOT.md` — 7 файлов под SHA-256 вместо 5, новые totals и раздел «Derived teaching data»; `archive/index.html` — записи о новых файлах и `--offline`; `wiki/README.md` — полная карта сайта; `.token-gate-ignore` — `wiki/data/**` и `wiki/archive/cognates-manifest.json` (сгенерированные данные), а `fetch_snapshot.py` разгружен выносом метаданных в `etymology_meta.py`, чтобы остаться под лимитом 20 КБ staged-файла.
- **Бэкап:** независимое зеркало `sanskrit-etymology-source-archive` дополнено `raw/cognates.json`, `cognates-manifest.json`, обновлёнными manifest/SNAPSHOT/CHECKSUMS и README; все хэши сверены.
- Контекст: запрос MG 07-11-2026 «Timeline of layers, Etymology explorer, Cognate map - do all» — продолжение публикации визуализаций на github.io/wiki с полной кликабельностью и бэкапом источника.

## 07-11-2026 — /wiki/: визуализация Sanskrit terms by etymology + архив источника

- **Добавлено:** [wiki/index.html](https://gasyoun.github.io/wiki/) — учебная страница по [Category:Sanskrit terms by etymology](https://en.wiktionary.org/wiki/Category:Sanskrit_terms_by_etymology). 42 подкатегории перегруппированы в три линзы (происхождение / словообразование / достоверность), шкала по числу слов (e) отделена от ширины таксономии (c), добавлен интерактивный стенд guṇa/vṛddhi с worked examples в IAST и деванагари. Все 42 категории, 20 баров, 25 чипов и каждый пример слова кликабельны и ведут на точные страницы Wiktionary: 96 сгенерированных ссылок, все 42 URL проверены через MediaWiki API. Статика без CDN и без сборки, работает офлайн папкой.
- **Добавлено:** [wiki/archive/](https://gasyoun.github.io/wiki/archive/) — байт-в-байт бэкап источника на случай переименования или потери страницы: исходный HTML, wikitext (`{{auto cat}}`), отрендеренный intro, API-список 42 подкатегорий и 5 426 прямых членов дерева уровнем ниже (у родительской категории нет ни одной словарной страницы, поэтому копия только родителя бесполезна). Провенанс и SHA-256 — [manifest.json](https://gasyoun.github.io/wiki/archive/manifest.json), читаемая копия — SNAPSHOT.md, генератор — wiki/scripts/fetch_snapshot.py. Независимое зеркало — репозиторий `sanskrit-etymology-source-archive`.
- **Изменено:** [.token-gate-ignore](https://github.com/gasyoun/gasyoun.github.io/blob/master/.token-gate-ignore) — добавлен glob `wiki/archive/raw/**`: скачанные сторонние данные (303 КБ JSON, 84 КБ HTML) не проходят лимит 20 КБ на staged-файл. [README.md](https://github.com/gasyoun/gasyoun.github.io/blob/master/README.md) — новый пункт в каталоге публикаций.
- Контекст: запрос MG 07-11-2026 «выложить всё на github.io/wiki, сделать кликабельным с ссылками на оригинал и забакапить на GitHub на случай потери исходной страницы».

## 11-10-2026 — H6477–H6479 волна OG-превью (GLM) — root: og: meta + GitHub-lookalike карточка

- **Добавлено:** [og-card.png](https://github.com/gasyoun/gasyoun.github.io/blob/master/og-card.png) — карточка 1200×630 (avatar, ऋग्वेदः hero RV 1.1.1, ряд 1028 sūktas · 10 maṇḍalas · 4 languages) + генератор [scripts/make_og_card.py](https://github.com/gasyoun/gasyoun.github.io/blob/master/scripts/make_og_card.py) (headless Chrome, `OG_AVATAR`/`CHROME_BIN` override).
- **Изменено:** [index.html](https://github.com/gasyoun/gasyoun.github.io/blob/master/index.html) — добавлены `<title>` ( был пуст) и og:type/site_name/title/description/url/image; og:image = https://gasyoun.github.io/og-card.png. Telegram/Slack/X превью корня теперь показывают карточку вместо пустого сниппета.
- Контекст: гриль MG 11-10-2026 «динамические OG-карточки для наших сайтов»; pilot-волна H6477 (rvlinks) / H6478 (Cologne upstream PR) / H6479 (avlinks полный сет).

## 09-10-2026 — H6296 (GLM) — Дашборд «SMB pain-benchmark: похожа ли школа на типовой профиль малого бизнеса»

- **Добавлено:** [smb-pain-benchmark-2026/index.html](https://github.com/gasyoun/gasyoun.github.io/blob/master/smb-pain-benchmark-2026/index.html) + [data.json](https://github.com/gasyoun/gasyoun.github.io/blob/master/smb-pain-benchmark-2026/data.json) — сезонная матрица выручки 2024–2026 (календарные сезоны, декабрь из прошлого года; фильтры по годам/сезонам), помесячный ряд с маркерами наборов сен/янв, сверка контуров денег 2026 янв–июль (CRM ₽8,78M ≈ Tochka ₽7,02M + PayPal ₽1,37M, расхождение 4,5% ✓ ±10%), вердикты по 10 болям SMB (итог: 1 полное совпадение — «падают продажи» с 2026, −36% янв–сен к 2025; 2 частичных, 2 аналога, 5 не наши) + 5 наших болей вне топ-10; только агрегаты (PII-свип чист), meta noindex.
- Числа трассируемы в data.json; источники: БД Systema (повторная живая проба 09-10, псевдо-тарифы «Расход»/«salary_payout» отделены от выручки), Tochka-агрегаты, PayPal-реконсил 01-09, Metrika (оба счётчика), GSC (12 мес), аудит VK Ads, отчёты BUSINESS_HEALTH/PROCESS_MINING/BLEED_AUDIT; рулинги грилла MG — Uprava docs/DECISIONS_SMB_PAIN_BENCHMARK_GRILL_09-10-2026.md.

## 09-10-2026 — H6299 (OxAlpha) — Страница «Стоимость курсов по учителям» (₽+€, noindex)

- **Добавлено:** [courses/course-prices-teachers-2026-10-09.html](https://github.com/gasyoun/gasyoun.github.io/blob/master/courses/course-prices-teachers-2026-10-09.html) — все 140 курсов Systema, секции по учителям (20 + «Без учителя»); у каждого курса активные тарифы поблочно («весь курс» + блоки с периодами «мес год – мес год» из дат занятий), итог курса целиком, итог по учителю и общий итог — 5 911 801,00 ₽ / 68 366,65 €. meta `noindex, nofollow`; robots.txt уже закрывает весь сайт.
- **Добавлено:** [scripts/gen_course_prices.py](https://github.com/gasyoun/gasyoun.github.io/blob/master/scripts/gen_course_prices.py) — генератор: read-only срез прода .92 (courses, tariffs, tariff_foreign_prices, lessons; окно дат 2019–2027), хранимые евро-цены, 12 недостающих досчитаны по имплицитному медианному курсу 85,71 ₽/€ с пометкой `~`.
- Заказ MG 09-10 («учитель, курс, период, стоимость поблочно и целиком, ₽ и €, на гитхабио без индексации»); гриль — 4 ответа по умолчанию, ждут визы.

## 09-10-2026 — H6277 (GLM) — Публикация дашборда и инфографики переписи n8n

- **Добавлено:** `n8n-census-dashboard-08-10.html` — дашборд переписи 95
  воркфлоу n8n vps91 (дни, кластеры, топ-10, триггеры, креденшелы, скаттер,
  «тихие активные», поиск). Копия артефакта H6232 (Uprava); провенанс-ссылки
  на приватный Uprava нейтрализованы в текст (17 шт.) — публичная версия
  без битых/приватных ссылок.
- **Добавлено:** `n8n-census-infographic-08-10.html` — инфографика-чертёж
  «101 день» (полка 95 модулей, дыхание недели, контуры). Копия H6232
  дословно, 0 внешних ссылок.
- Вместе с `n8n-top5-dynamic-09-10.html` (H6276) — полный публичный набор
  n8n-визуализаций по правилу «ALL org HTML links point here, never blob».

## 09-10-2026 — H6276 (GLM) — Публикация динамики топ-5 воркфлоу n8n vps91

- **Добавлено:** `n8n-top5-dynamic-09-10.html` — интерактивная страница
  (обзор + 5 вкладок-воркфлоу): по-нодовые графы на реальных canvas-позициях
  живого экспорта n8n 2.38.6, анимация потока ∝ запусков/день, светлая/тёмная
  темы, trust block, таблицы-фолбэки. Копия артефакта H6272 (Uprava PR #4515,
  `--check` PASS, visual-judge 7/7); самодостаточная, 0 внешних ссылок,
  санитизирована (без параметров/креденшелов/webhookId). Оригинал-генератор и
  фид — в Uprava `docs/n8n/`.

## 04-10-2026 — H6079 + H6080 (OxAlpha) — Раздел 17 «Ежедневное использование» + WireGuard-шпаргалка (K061)

- **Добавлено:** `forgetme-wireguard-cheatsheet-2026-10-04.html` — полная
  спутница «VPS с нуля» (K061, секция F): WireGuard-сервер на Debian 12,
  ключи (пара на устройство), wg0.conf с MASQUERADE и IPv6-гвардом,
  ip_forward + автозапуск, клиентский конфиг и QR, подключение телефона,
  второй клиент через `wg syncconf`, AmneziaWG-набросок, траблшутинг,
  памятка, «Что проверено» с дисклеймером. На скелете базовой шпаргалки.
- **В базовой шпаргалке:** раздел 17 «Ежедневное использование: мак,
  Windows, планшет, айфон» (таблица путей + 17.1–17.4); в 16.3 — ссылка
  на WireGuard-шпаргалку; приписка в «Что проверено»; TOC в обоих
  оглавлениях. Запрос MG «а и б, дурабле док».
- **Карта:** +1 пункт K061; регенерация (60 пунктов), `--check` зелёный.
- Корневой `index.html` (Ригведа) не тронут.

## 04-10-2026 — H5993 (OxAlpha) — Раздел 16 «Путь с телефона» в ForgetMe-шпаргалке

- **Добавлено:** в `forgetme-vps-cheatsheet-2026-10-03.html` раздел 16
  «Путь с телефона: сервер как шлюз, без рабочего стола» — таблица трёх
  путей, Termius SOCKS-маршрут (16.2) с `ssh -D` для компьютера, набросок
  WireGuard/Amnezia (16.3). Запрос MG «yes» на оценку нику novo из Telegram.
- **Правда редакции:** подзаголовок и сайдбар на 04.10.2026; в «Что проверено»
  приписка — телефонный путь не прогонялся, WireGuard за рамками документа.
- Корневой `index.html` (Ригведа) не тронут; karta без изменений.

## 04-10-2026 — H5972 (OxAlpha) — ForgetMe VPS-шпаргалка (K060)

- **Добавлено:** `forgetme-vps-cheatsheet-2026-10-03.html` — самодостаточная
  инструкция «VPS с нуля» к видео ForgetMe (Debian 12 → SSH → XFCE +
  TigerVNC/noVNC + Firefox через SSH-туннель; редакция 03-10-2026, доведена
  ZCode после смерти MSI). В странице: canonical на живой URL и ссылка на
  [карту домена](https://gasyoun.github.io/karta/) в сайдбаре.
- **Карта:** +1 пункт — K060 (секция F, green); `karta/index.html`
  регенерирован (59 пунктов), `--check` зелёный.
- Корневой `index.html` (Ригведа) не тронут — решение MG 27-09-2026 в силе.

## 04-10-2026 — bughunt-fixes (GLM 5.3 Flash) — Фиксы MEDIUM по охоте 04-10

- **Karta coverage → GREEN:** +4 пункта в `karta_data.py` — K056
  `handoff-status/`, K057 `payroll/` (amber, @DO 0O3), K058 рунбук H3348,
  K059 сообщение Артёму H3348; `karta/index.html` перегенерирован (58 пунктов).
- **Индекс infographics → GREEN:** `--emit` вписал 2 директории
  (klammer-kutumbini, paradigm-a-stems); `check.mjs --index` 0 ошибок.
- **render_slugs.mjs:8:** корень берётся от `import.meta.url`, а не от cwd —
  запуск из любого каталога теперь работает (паттерн соседа render.mjs).
- **Vote-листы:** два недельных дрейн-листа (21_09, 28_09) довнесены в git —
  серия `uprava_drain_vote_weekly_*` отныне трекается целиком.
- HIGH (payroll-публичность) не тронут — money-class, решение по @DO 0O3 за MG.

## 04-10-2026 — bughunt (GLM 5.3 Flash) — Охота по коду: 1 HIGH, отчёт

- **HIGH (money-class, без авто-фикса):** payroll-ведомости (авг+сен 2026)
  публичны дважды — живой URL отвечает 200, и оба файла лежат в публичном
  репо, где robots.txt / noindex не действуют; с сайта туда же ведёт линк из
  vote-листа. GTD @DO 0O3 заминчена — решение за MG (приватность репо /
  перенос / осознанный приём).
- **Два живых гейта RED:** karta coverage (4 пункта мимо karta_data.py) и
  индекс infographics (DRIFTED, 2 директории не вписаны в index.html).
  Фиксы механические — по слову MG (дневной режим).
- **Код:** render_slugs.mjs:8 берёт корень от cwd вместо import.meta.url —
  работает только из корня репо (сосед render.mjs:8 делает правильно).
- **Отчёт:**
  [BUGHUNT-FINDINGS-gasyoun.github.io-04.10.2026.md](https://github.com/gasyoun/gasyoun.github.io/blob/master/BUGHUNT-FINDINGS-gasyoun.github.io-04.10.2026.md).
  Ночной прогон 03:00 погиб на provider-таймауте после PHASE 1 (отчёт не
  сел) — докончено дневным проходом 04-10 с живой перевёркой.

## 27-09-2026 — H5530 (OxAlpha) — Уборка по GTD 0JQ/0JR

- **Переименовано:** `reverse20-ouput/` → `reverse20-output/` (опечатка в имени;
  содержимое без изменений). Ссылки поправлены тем же коммитом: README.md, karta
  (K017). Старый URL больше не работает — осознанно, по GTD-остатку 0JQ.
- **Удалено:** `index2.html` — бойлерплейт GitHub Pages «Welcome to GitHub
  Pages» (GTD 0JR). `params.json` из того же шаблона оставлен. Корень
  (`index.html` = Ригведа) не тронут — решение MG 27-09-2026 в силе.
- **Карта:** 55 → 54 пункта; K041 (index2.html) выведен из данных — K-номера
  не переиспользуются, дырка в нумерации остаётся намеренно.

## 27-09-2026 — H5527 (OxAlpha) — Карта домена `/karta/`

- **Добавлено:** `karta/index.html` — аннотированный индекс всего домена:
  55 пунктов с уникальными номерами K001–K055 (стабильные, не переиспользуются),
  6 рубрик по назначению (тексты · хитмапы · ELI5 · исследовательские выкладки ·
  продукт/макеты · процесс/аудит) + секция «Острова домена» (13 project-pages
  других репо: kosha, SanskritLexicography, Systema-Sanscriticum, …).
  RU-аннотации 1–2 предложения, статусы 🟢 живой / 🟡 служебное / ⚰️ архив.
- **Генератор:** `scripts/karta/gen_karta_index.py` + данные
  `scripts/karta/karta_data.py`. Режимы: `--emit` (собрать), `--check`
  (диск/данные не дрейфанули), `--probe-islands` (живой HTTP-аудит всех 55 ссылок).
  Каверидж-гард: непокрытый контент на диске валит emit/check со списком.
- **Решения MG 27-09-2026 (гриль-раунд):** полный охват домена (не только диск
  этого репо); корень сайта не трогать (index.html = Ригведа 12.4 МБ остаётся);
  karta живёт на `/karta/`; глобальные K###; развёрнутые RU-аннотации; всё,
  включая мёртвое, со статусами.
- **Прецедент паттерна:** H3768 (infographics live-index, `--emit/--check`).
- **Доп. 27-09, тот же день:** K055 `mindmaps/` (волна H5525/H5526 легла в master через 40 минут после карты) — coverage-гард поймал новый каталог, карта дозрелла до 55 пунктов.

_Гасунс_
