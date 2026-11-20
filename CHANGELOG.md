# CHANGELOG — gasyoun.github.io

Формат: дата · хендофф · что изменилось. Новые записи сверху.

## 20-11-2026 — YLQ wave 1: три live-parked листа разблокированы → live (compound_rules_30, pwg_c2p2, systema_nkrya)

- **[compound_rules_30](https://gasyoun.github.io/vote/sheets/compound_rules_30.html) → live:** генератор мигрировал под H1649 screening-гейт — `screening_block_for()` выводит счётчики из того же adjudication TSV, что и карточки ([SanskritLexicography #2523](https://github.com/gasyoun/SanskritLexicography/pull/2523)): candidates 3 780 pwg-right → agent 3 750 · human 30 · deterministic 0 · lookup 0 (H1664 §11 HYBRID-B2; 268 index-right + 305 unresolved вне scope — задокументированы); новый закоммиченный `review/…ratify30_screening_evidence.md` — цель banner'а. Гейт: было `ValueError: screening= is required when extras=True (H1649)` → стало `--selftest`/`--write` PASS, preflight PASS. Identity (H2852): sheet_id/localStorage неизменны, 30 карточек, seed 1887, evidence manifest байт-идентичен; живой TSV несёт 8 правил (floor 3 + 6 пропорциональных), а не исторические 7 — инварианты целы.
- **[pwg_c2p2_work_dating_11](https://gasyoun.github.io/vote/sheets/pwg_c2p2_work_dating_11.html) → live:** база пере-рендерена на csl-pyutil 0.25.0 ([SanskritLexicography #2522](https://github.com/gasyoun/SanskritLexicography/pull/2522); lock перезаписан `REVIEW_LOCK_FORCE=1`, 11/11 непроголосованы), поверх — H4116 ремейк-слой из закоммиченного спека (Uprava `review/specs/c2p2_work_dating.spec.json` + `tools/sheet_evidence_stamper.py`): ssb-evidence штамп и все 11 agent-evidence панелей (вкл. **C2P2-D1** — панель, которую базовый рендер терял) байт-идентичны опубликованной копии; остальные дельты — механика 0.25.0-эмиттера (autosave-JS, meta, content_hash). `sheet_evidence_gate.py` PASS 11/11 (`--sample 3`).
- **[systema_nkrya_gloss_lint_rare_swaps_23-09-2026](https://gasyoun.github.io/vote/sheets/systema_nkrya_gloss_lint_rare_swaps_23-09-2026.html) → live:** генератор испускает IAST в прозе — класс-фикс `iast()` через `sanskrit_util.from_slp1` под детектором `csl_pyutil.evidence.find_slp1` ([Systema-Sanscriticum #4339](https://github.com/gasyoun/Systema-Sanscriticum/pull/4339)); preflight был красный на `anarTa`, теперь чистый (`slp1_leak []` / `mixed_script []`); диф против пре-фикс сбора — только `anarTa→anartha`. Данные дрейфнули с 23-09: голосуемых карточек теперь **4** — новая SWAP-карточка `lemmas-subhashita-beginner-anartha` («вред», 30.12 ipm) и была источником префлайт-оффендера (паркованная копия несла 3); известная косметика: policy-карточка называет 8 negation-строк при 9 в данных — не голосуемая, очередь на мелкий фикс.
- **Реестр:** `live` 10→13, `live_parked` 5→2 (остались h3361_window25_review · h180_reglue_v7 — лейны D/E в работе). Контракт соблюдён тем же проходом: хостинг + регистрация в live одним PR (рулинг A — strict-on-live). (GLM 5.3 (opencode-go/glm-5.3))

## 19-11-2026 — YLO: два live-parked листа закрыты чат-голосом MG (записи сняты из реестра)

- **Сняты из `live_parked` (запись уходит в момент применения голоса — контракт реестра):** [uprava_docs-fixwaves_judgment-links_05-09-26](https://gasyoun.github.io/vote/sheets/uprava_docs-fixwaves_judgment-links_05-09-26.html) — **7/7 «Применить»** (F1–F5 масс-волны + F6 класс закрыт без прогона + F7 BookIndex признан генерённым контентом) и [uprava_skill_scan_adopt_h5129_18-09-26](https://gasyoun.github.io/vote/sheets/uprava_skill_scan_adopt_h5129_18-09-26.html) — **6/6 approve** (S1–S6 adopt-parts). Генераторы обоих листов ретированы рулингом 0K8 (MG 28-09) — реген невозможен, поэтому закрытие шло чат-голосом MG 19-11 (GTD row YLO, интерактив ≤4 карты/вызов), а хаб-копии остаются архивным record; карточки продублированы в Uprava-аудите `reports/DECISIONS_APPLIED_YL0_CHAT_19-11-2026.md`.
- **После снятия:** `live_parked` — ровно пять листов, все ждут unblock-юнитов (GTD row YLQ: compound_rules_30, systema_nkrya, pwg_c2p2 + h3361, h180_reglue_v7); применение вердиктов — хендоффы [H8479](https://github.com/gasyoun/Uprava/blob/main/handoffs/H8479-GLM_Uprava_docs-fixwaves-apply-chat-vote_19.11.26.md) (масс-волны) + [H8480](https://github.com/gasyoun/Uprava/blob/main/handoffs/H8480-GLM_claude-config_skill-scan-adopt-h5129-apply_19.11.26.md) (adopt-parts); decisions.json — в `Uprava/review/` (локально, gitignored).

## 19-11-2026 — YL3: реген-волна листов на csl-pyutil 0.25.0 + строгий чек, скованный с LIVE-реестром (рулинг A)

- **Реген (9 хаб-файлов):** [h215_gold_full_320](https://gasyoun.github.io/vote/sheets/h215_gold_full_320.html) (+32 пака H3098 в `vote/sheets/h215_gold_full_320/`), h2805_q3_deploy, rv_divergence_gate_v5, renou_hypotheses_v2 + байт-идентичный дубль renou_pilot_v2_h062, nilakantha_licence_46, uprava_h2868_stubs, h3863_giveback_slot_conflicts + дубль kosha-giveback-slot-conflicts_h3863_review — пересобраны их закоммиченными генераторами на 0.25.0; SHEET_ID/STORE_KEY/карточки не изменились (голоса в localStorage выживают); evidence h215 байт-идентичен опубликованному (263/138/252/320 из 320). Компаньон: [SanskritLexicography #2521](https://github.com/gasyoun/SanskritLexicography/pull/2521) (4 лока + 2 committed HTML).
- **Рулинг A (MG 19-11, форк YL3 «H3848-смягчение vs H2854-строгость»):** exit-1 теперь только для stale LIVE-листов — [scripts/live_vote_sheets.json](https://github.com/gasyoun/gasyoun.github.io/blob/master/scripts/live_vote_sheets.json) (10 live · 7 live_parked · 4 frozen/archived); закрытые decision-records — regen-queue в логе (91), никогда фейл; live_parked — громкий WARN с причиной и путём разблокировки. Позитив/негатив-проба: pinned 0.25.0 → rc 0; pinned 0.26.0 → rc 1 (STALE LIVE секция фейлит).
- **Не перевыпущены (доктрина H2852 — не собирать руками):** uprava_gtd_harvest_triage_22 (строитель читает живой GTD-харвест — исторические входы не закоммичены, реген дал бы другой лист) и uprava_gtd_harvest_66 (ручная вырезка H2888, генератора нет) — закрытые голосованные записи, остаются в очереди.

## 19-11-2026 — ветки: `main` ретирована, её контент сведён на master (GTD YKR, рулинг A)

- **Изменено:** `main` был decoy-веткой PR-intake (squash-diverged с 16-08, никогда не публиковалась). Реальный контент сведён на `master` одним PR: строгий staleness-чекер H2854 step-5 (d56a147), `vote/index.html` (H2898 harvest triage) и 3 листа (h215_gold_full_320, h2805_q3_deploy — H2854 step-6 regen; nilakantha_licence_46 — H2883). Остальное на main: stray `index2.html` (не взято), typo-переименование `reverse20-ouput/` (не взято — на master правильное `reverse20-output/`), копия MSI-страницы (уже публикуется с master, `e71dce5` удалил её как ошибку). Реф сохранён как `archive/main-diverged-19-11`, ветка `main` удалена; AGENTS.md получил секцию Branches («truth = master»).
- **Ожидаемо красный CI:** staleness-чек на master теперь строгий (H3848-смягчение снято H2854) и честно светит на листы, сгенерированные csl-pyutil 0.13.0 при актуальной 0.25.0 (uprava_gtd_harvest_triage_22, uprava_h2868_stubs) и на листы без meta-тега (renou_hypotheses_v2, rv_divergence_gate_v5, uprava_gtd_harvest_66). Реген-волна на 0.25.0 — GTD-строка (YKR residuals).

## 08-11-2026 — /cpu/: auto-refresh lane (H7869)

- **Изменено:** [cpu/](https://gasyoun.github.io/cpu/) больше не статичный снимок — почасовая launchd-лейна `ml.gasyoun.cpu-page` (Air, H7869; net-speed-log v1.1.0, PR gasyoun/net-speed-log#23) рендерит `--fleet` из свежего `origin/main` net-speed-log и публикует `cpu/index.html` push-if-changed: `generated <TS>` штамп выведен из diff-гейта (без timestamp-спама), неудавшийся пуш ретраится следующим интервалом. Первый автопуш: `cpu page auto-refresh 2026-11-08T12:51:45Z (H7869 hourly lane)`.

## 08-11-2026 — /cpu/: fleet GB page (Air + MSI)

- **Изменено:** [cpu/](https://gasyoun.github.io/cpu/) стал флот-страницей GB-цензуса: по секции на хост (MacBook-Air + MSI/DESKTOP-8N57E9U) — RAM free / swap used / disk C free (now + 24h avg), 7-дневные графики swap GB и RAM free GB, механические вердикт-карточки и предупреждение о протухшем зонде (probe stale). Хост, молчащий 45+ дней, рендерится как retired-install skip, а не секция. Рендер: `python3 tools/build_agent_dashboard.py --fleet` (net-speed-log v1.0.3, PR #22); статический снимок деплоится сюда.
- **Починено на MSI (DESKTOP-8N57E9U):** после переустановки Windows зондило почасово, но пуш-нога умерла (3 дня строк лежали незакоммиченными в клоне, на origin не ехали); skill-копия measure.ps1 была битой (40 строк вместо 227) — развёрнута заново из репо-копии, hourly-таск AgentResourcesProbe перепрошит на windows/probe_push.ps1 (зонд + commit/push, absolute pwsh-путь), первый свежий 28-колоночный ряд (swap 1.03 GB, zcode 23 procs / 2692 MB) уехал на origin 08-11 11:22Z.
- Полный MB-цензус по Air остался: [agent_dashboard.html](https://github.com/gasyoun/net-speed-log/blob/main/agent_dashboard.html) (рендерится по требованию).

## 08-11-2026 — /cpu/: agent resources memory census

- **Добавлено:** [cpu/](https://gasyoun.github.io/cpu/) — дашборд «куда уходит память» по эстейт-группам (browsers / OpenCode / ZCode / Claude / Codex / Grok / Actions runners / git / Spotlight), 7-дневные графики свапа/сессий/браузеров/раннеров и механические вердикт-карточки. Источник данных: net-speed-log hourly probe (28-колоночный CSV, H7846); рендер `python3 tools/build_agent_dashboard.py` в клоне net-speed-log, статический снимок деплоится сюда.

## 07-11-2026 — /wiki/: Transliteration reference page (EN/RU)

- **Добавлено:** [wiki/translit.html](https://gasyoun.github.io/wiki/translit.html) и [wiki/ru/translit.html](https://gasyoun.github.io/wiki/ru/translit.html) — статический справочник всей этимологии санскрита в транслитерации IAST. Все 42 категории Викисловаря перегруппированы в три линзы (происхождение 18 / словообразование 15 / достоверность 9), полная таблица ступеней гласных guṇa/vṛddhi для всех пяти типов корневой гласной (a, i, u, ṛ, ḷ) с примерами (√pac, √vid, √budh, √kṛ), правило сандхи (o→av, au→āv), цепочка √budh → bodha → bauddha, словарь терминов словообразования (samāsa, dhātu, upasarga, pratyaya, guṇa, vṛddhi, sandhi) и пять методических выводов.
- **Принцип:** страница не требует чтения деванагари. Все санскритские термины даны в IAST; деванагари — в отдельных столбцах для справки. Каждая категория — ссылка на первоисточник в Викисловаре. Страница полностью статическая: никакого JavaScript, загрузки данных через `fetch` или `<script src>`. Самодостаточный HTML, работает офлайн.
- **Изменено:** nav всех 16 страниц (EN + RU) — добавлена ссылка «Transliteration» / «Транслитерация» между «Word formation» / «Словообразование» и «Archive» / «Архив».
- Контекст: запрос MG 07-11-2026 — данные с gasyoun.github.io/wiki/ нужно предоставить в виде HTML-страниц (не .md), чтобы посетителям не приходилось разбирать деванагари на внешнем сайте.

## 07-11-2026 — /wiki/: Dhātu desk + Word formation + Explorer enrichment (EN/RU)

- **Добавлено:** [wiki/dhatu.html](https://gasyoun.github.io/wiki/dhatu.html) — стол дхату: 930 корней Уитни (№, IAST, SLP1, класс, глосса, период, частота DCS, формы), таблица с поиском/сортировкой/фильтром по классу и периоду, панель покрытия сайта (86,6% корней встречаются среди 3 111 лемм деванагари), bars по категориям. Каждый корень — ссылка на Wiktionary и на Whitney. **Это кандидаты на перекрёстную ссылку, не новые этимологии.**
- **Добавлено:** [wiki/wordformation.html](https://gasyoun.github.io/wiki/wordformation.html) — словообразование: 27 аффиксов (kṛt / taddhita / stri) с поверхностной формой, пратьяя, анубандха, функцией, примерами; таксономия самаса (4 класса, 9 семейств, 58 листьев с vigraha); 12 курируемых примеров сложных слов с разбором компонентов. Каждый пример — ссылка на Wiktionary.
- **Добавлено:** [wiki/ru/dhatu.html](https://gasyoun.github.io/wiki/ru/dhatu.html) и [wiki/ru/wordformation.html](https://gasyoun.github.io/wiki/ru/wordformation.html) — русские издания тех же страниц; перевод через `data/i18n-formation.js` (`window.WIKI_FORMATION_I18N`, EN+RU в одном модуле). Исходные данные (корни, аффиксы, пратьяя, самаса-термины, примеры) — в точном виде источника.
- **Изменено:** [wiki/explorer.html](https://gasyoun.github.io/wiki/explorer.html) и [wiki/ru/explorer.html](https://gasyoun.github.io/wiki/ru/explorer.html) — панель «перекрёстные ссылки прежних работ»: toggle вкл/выкл, фильтр «только слова со ссылкой», 797 из 3 111 лемм деванагари получили кандидаты на MW-деривацию / DCS lemma→root / Whitney root. Каждая ссылка ведёт на свой источник. Поддержка deep links `?cat=&q=&fmt=1` от словообразовательных страниц.
- **Данные:** `data/formation.js` (797 аннотированных лемм, 25,6% покрытия), `data/roots.js` (930 корней Уитни), `data/wordformation.js` (27 аффиксов, таксономия самаса, 60 членов сложных слов, 12 курируемых примеров), `data/i18n-formation.js` (билингвальный EN+RU модуль). Генератор `scripts/build_formation.py` — офлайн, без сети, без внешних пакетов; деванагари→SLP1 конвертер валидируется на 8 000 выровненных MW-металин при каждом запуске (99,83% точность). Replayable provenance record в `archive/raw/formation-sources.json`, контрольный манифест в `archive/formation-manifest.json`, лицензии в `archive/SOURCES-LICENSES.md`.
- **Изменено:** `archive/manifest.json` / `data/manifest.js` / `SNAPSHOT.md` — 9 файлов под SHA-256 (добавлены `raw/formation-sources.json` и `formation-manifest.json`); totals — `formation_annotated: 797`, `whitney_roots: 930`. Nav всех 14 страниц — добавлены ссылки «Dhātu desk» / «Дхату» и «Word formation» / «Словообразование».
- **Бэкап:** зеркало `sanskrit-etymology-source-archive` дополнено `raw/formation-sources.json`, `formation-manifest.json`, `SOURCES-LICENSES.md`, обновлёнными manifest/SNAPSHOT/CHECKSUMS; все 9 хэшей сверены.
- **Лицензии:** CSL Monier-Williams (Devanagari + SLP1) — CC BY-SA 4.0; WhitneyRoots, SamasaChakram — Apache-2.0; MWderivations, SanskritRussian — без LICENSE (используются только минимальные агрегаты); Zalizniak/Fasmer (CC BY-NC) — **намеренно исключены** из `/wiki/`.
- Контекст: запрос MG 07-11-2026 «do all» — реализация трёх фаз интеграции прежних работ по корням/деривации/аффиксам/самаса в учебный сайт.

## 07-11-2026 — /wiki/ru/: полное русское издание учебного сайта

- **Добавлено:** [wiki/ru/](https://gasyoun.github.io/wiki/ru/) — параллельное русское издание из пяти страниц: [обзор](https://gasyoun.github.io/wiki/ru/) (три линзы, честная шкала `e`/`c`, лаборатория гуна/вриддхи), [поиск по этимологии](https://gasyoun.github.io/wiki/ru/explorer.html) (3 164 леммы, 2 005 категорий-источников), [карта когнатов](https://gasyoun.github.io/wiki/ru/cognates.html) (18 ПИЕ-форм × 8 языков), [исторические слои](https://gasyoun.github.io/wiki/ru/timeline.html) (10 пластов) и [архив источника](https://gasyoun.github.io/wiki/ru/archive/). Интерфейс, подписи, методические заметки, названия пластов, языков и ветвей, сандхи и глоссы переведены; `<html lang="ru">`, русские `title` и `aria-label`.
- **Принцип:** исходные данные не переводятся. Названия 42 категорий Wiktionary, леммы в деванагари и IAST, ПИЕ-реконструкции, рефлексы восьми языков и все URL остаются байт-в-байт теми же, что в английском издании. Проверено попарным сравнением множеств ссылок на начальном рендере: 45 / 84 / 507 / 72 / 42 URL, расхождений **ноль** для всех пяти пар. Оригинальные английские названия доступны в `title`, в архиве — под русским ярлыком всегда, в обзоре — по переключателю «Показать оригинальные названия».
- **Данные:** `wiki/data/i18n-ru.js` (`window.WIKI_RU`, 11,5 КБ) — 42 названия категорий, 28 описаний, 18 ПИЕ-глосс, 4 пласта (кратко и полно), 8 языков, 4 ветви, 5 sandhi-заметок, 5 глосс примеров, 3 подписи ступеней. Покрытие сверено с `etymology.js` и `cognates.js`: пропусков нет. Модуль уже покрыт существующим glob `wiki/data/**` в `.token-gate-ignore`.
- **Изменено:** общий `nav.sitenav` всех пяти английских страниц получил переключатель EN → RU и взаимные `<link rel="alternate" hreflang>`; `wiki/style.css` — компоненты `.langsw` и `.orig` / `.showorig`. Страницы русского издания грузят те же данные через `../data/*.js` (архив — `../../data/*.js`) и ту же таблицу стилей, поэтому при обновлении снимка оба издания меняются синхронно; новых сетевых зависимостей, CDN и сборки нет.
- **Проверено:** DOM-stub прогон всех десяти страниц (английские + русские) с реальными данными и сценариями взаимодействия — ни одного `undefined` / `NaN` / неразрешённого `href="#"`, все контейнеры заполнены, все ID-заглушки получили ссылки; 0 битых локальных ссылок, 0 дублей ID; 7 ссылок на файлы снимка из русского архива разрешаются; форматы URL (деванагари, `Reconstruction:`, `Category:*`, ПИЕ-категория, категория наследования) дают HTTP 200. Сканирование видимого текста русских страниц: единственная латиница без кириллицы — сам переключатель `EN`/`RU`.
- **Бэкап:** исходные данные не менялись, поэтому независимое зеркало `sanskrit-etymology-source-archive` и его CHECKSUMS остаются актуальными; в его README добавлена ссылка на русское издание.
- Контекст: запрос MG 07-11-2026 «Make a russian edition as well» — продолжение публикации визуализаций на github.io/wiki.

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
