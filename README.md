# gasyoun.github.io

_Created: 08-10-2014 · Last updated: 07-11-2026_

Personal GitHub Pages site of Mārcis Gasūns ([@gasyoun](https://github.com/gasyoun)),
served at [gasyoun.github.io](https://gasyoun.github.io/). It hosts a handful of
static Sanskrit / Vedic lexicographic experiments — not a blog or CV — kept as
plain HTML and text data. Since 09-10-2026 it also carries a few deliberately
`noindex` ops/business dashboards and cheat-sheets (SMB benchmark, course prices,
n8n census, VPS cheat-sheets) — [CHANGELOG.md](https://github.com/gasyoun/gasyoun.github.io/blob/master/CHANGELOG.md)
is the full catalog.

## What is published here
- **[wiki/](https://gasyoun.github.io/wiki/)** — «Sanskrit terms by etymology»:
  учебный вид [одноимённой категории Wiktionary](https://en.wiktionary.org/wiki/Category:Sanskrit_terms_by_etymology)
  (42 подкатегории в трёх линзах, шкала числа слов, интерактивный стенд
  guṇa/vṛddhi) плюс три инструмента поверх реального словаря:
  [Etymology explorer](https://gasyoun.github.io/wiki/explorer.html) (3 164 леммы,
  2 005 buckets источников, поиск и фильтры),
  [Cognate map](https://gasyoun.github.io/wiki/cognates.html) (18 PIE корней/слов ×
  8 языков, 118 категорий-источников) и
  [Timeline of layers](https://gasyoun.github.io/wiki/timeline.html) (4 слоя
  наследования с реальными числами, затем словообразование, контакты, лакуны).
  Каждая категория, число, лемма и рефлекс — ссылка на точную страницу оригинала;
  без CDN и сборки, работает офлайн папкой. Рядом
  **[wiki/archive/](https://gasyoun.github.io/wiki/archive/)** — байт-в-байт бэкап
  исходной страницы, 5 426 заголовков дерева категорий, 7 файлов с SHA-256,
  URL-манифест и инструкция восстановления (в т.ч. `--offline`-пересборка без сети).
- **[wiki/ru/](https://gasyoun.github.io/wiki/ru/)** — русское издание: те же пять
  страниц ([обзор](https://gasyoun.github.io/wiki/ru/), [поиск слов](https://gasyoun.github.io/wiki/ru/explorer.html),
  [карта когнатов](https://gasyoun.github.io/wiki/ru/cognates.html),
  [слои](https://gasyoun.github.io/wiki/ru/timeline.html),
  [архив](https://gasyoun.github.io/wiki/ru/archive/)) с полностью переведённым
  интерфейсом и учебным текстом. Названия категорий, леммы, праиндоевропейские
  реконструкции и рефлексы оставлены в точном виде источника и ведут на те же
  страницы Wiktionary; переводные строки вынесены в `wiki/data/i18n-ru.js`. Переключатель
  EN/RU и взаимные `hreflang` — на всех десяти страницах; обзор умеет показывать
  оригинальные англоязычные названия категорий поверх перевода.
- **[campus/](https://gasyoun.github.io/campus/)** — «Кампус наглядности»:
  один вход ко всей визуальной наглядности имения — 72 артефакта в 4 крыльях
  (грамматика / учёба / имение и финансы / продукты и привлечение); собирается
  генератором
  [scripts/campus/campus_build.py](https://github.com/gasyoun/gasyoun.github.io/blob/master/scripts/campus/campus_build.py)
  из каталога инфографик, рукописных страниц нет (H4261).
- **[mastery/](https://gasyoun.github.io/mastery/)** — «Карта мастерства»:
  35 517 учебных позиций в 5 drill-семях из kosha (H3742); статистический
  вариант — [stats.html](https://gasyoun.github.io/mastery/stats.html) (H4262,
  [dual-run запись](https://github.com/gasyoun/gasyoun.github.io/blob/master/scripts/campus/MASTERY_DUALRUN_2026-09-14.md)).

- **[index.html](https://github.com/gasyoun/gasyoun.github.io/blob/master/index.html)**
  — the workspace landing page: a static overview of the Sanskrit Lexicon / CDSL
  workspace (~196 repos), with quick links to the main published pages. Replaced the
  former Rigveda reader at the root on 07-11-2026 (the reader moved to `RV/`).
  Carries `og:` preview meta and
  [og-card.png](https://github.com/gasyoun/gasyoun.github.io/blob/master/og-card.png).
- **[RV/](https://github.com/gasyoun/gasyoun.github.io/tree/master/RV)** — the
  multilingual Ṛgveda reader (formerly the root `index.html`, ~12 MB). Each stanza is
  shown as Vedic Devanagari, IAST transliteration, and padapāṭha, alongside the Russian
  (Elizarenkova), German (Geldner), and English (Griffith) translations, using
  Indological web fonts served from
  [fonts/](https://github.com/gasyoun/gasyoun.github.io/tree/master/fonts). Now served
  at [gasyoun.github.io/RV/](https://gasyoun.github.io/RV/) with its own
  [rigveda.css](https://github.com/gasyoun/gasyoun.github.io/blob/master/RV/rigveda.css)
  and full `og:` meta tags.
- **[eli5/](https://github.com/gasyoun/gasyoun.github.io/tree/master/eli5)** — picture-led
  explainers, one question per page, English and Russian: how the Petersburg
  dictionary is translated into Russian, and short answers to recurring student
  questions. Pages authored as Claude Artifact fragments are wrapped for standalone
  serving by
  [build_standalone.py](https://github.com/gasyoun/gasyoun.github.io/blob/master/eli5/build_standalone.py)
  — an Artifact fragment copied here verbatim looks fine and renders broken, because
  the Artifact host supplies the `[hidden]{display:none!important}` reset that tabbed
  pages depend on.
- **[PWGagainstMW.html](https://github.com/gasyoun/gasyoun.github.io/blob/master/PWGagainstMW.html)**
  — a comparison of PWG (Petersburger Wörterbuch) headwords against
  Monier-Williams, grouped by vowel/consonant patterns, each linking into the
  Cologne [sanskrit-lexicon](https://www.sanskrit-lexicon.uni-koeln.de/) scan
  viewer.
- **Reverse-index / reverse-sort outputs** — devanagari-sorted and
  reverse-sorted word lists derived from headword input:
  [reverse20-output/](https://github.com/gasyoun/gasyoun.github.io/tree/master/reverse20-output)
  (renamed from the misspelled `reverse20-ouput` on 27-09-2026, H5528),
  [reverse21-output/](https://github.com/gasyoun/gasyoun.github.io/tree/master/reverse21-output),
  and
  [reverse22-output/](https://github.com/gasyoun/gasyoun.github.io/tree/master/reverse22-output)
  (with its
  [input.txt](https://github.com/gasyoun/gasyoun.github.io/blob/master/reverse22-output/input.txt)).
- **[zalizniak-2026/](https://github.com/gasyoun/gasyoun.github.io/tree/master/zalizniak-2026)**
  (short address since 25-09-2026; the old `sanskrit-cognates-zalizniak-2026/` path survives
  only as a meta-refresh redirect stub) — a five-language (RU·EN·DE·LA·GR) cognate reference
  built on A. A. Zalizniak's «Конспект грамматических сведений о санскрите» (2004), in four
  sections (roots, nouns, adjectives, indeclinables), plus a children's detective story
  companion page
  ([skazka.html](https://github.com/gasyoun/gasyoun.github.io/blob/master/zalizniak-2026/skazka.html)).
  Base text is the konspekt verbatim; editorial additions are marked with 〈angle brackets〉
  (H5481).
  - canonical page `index.html` = language-ordered tables (RU by Russian word; EN/DE/LA/GR
  by cognate) + embedded 6-chapter detective story; regenerable via `build_page.py` (H5481,
  MG rulings 24-09-2026: additions in ⟨…⟩, asterisk reserved for reconstructions, Zalizniak
  transliteration). `skazka.html` is the parallel-run alternate tale (kept).
- **[296.txt](https://github.com/gasyoun/gasyoun.github.io/blob/master/296.txt)**
  and
  **[296-SLP1.txt](https://github.com/gasyoun/gasyoun.github.io/blob/master/296-SLP1.txt)**
  — a 295-line reverse word-to-page index of a Sanskrit text, in raw and SLP1
  transliteration.

## Leftover scaffolding

[params.json](https://github.com/gasyoun/gasyoun.github.io/blob/master/params.json)
is a leftover of the original GitHub Pages "automatic generator" (Merlot theme)
template, kept as-is; the served landing page is `index.html`. The sibling
`index2.html` boilerplate page was deleted on 27-09-2026 (H5528).

## Maintenance

Repo-side automation is Dependabot
([.github/dependabot.yml](https://github.com/gasyoun/gasyoun.github.io/blob/master/.github/dependabot.yml))
with a
[Dependabot auto-merge workflow](https://github.com/gasyoun/gasyoun.github.io/blob/master/.github/workflows/dependabot-auto-merge.yml),
the
[sheet-staleness workflow](https://github.com/gasyoun/gasyoun.github.io/blob/master/.github/workflows/sheet-staleness.yml),
the [changelog duplicate-entry guard](https://github.com/gasyoun/gasyoun.github.io/blob/master/.github/workflows/changelog-lint.yml)
(since 24-10-2026), and the pinned-F821 gate
([f821-gate.yml](https://github.com/gasyoun/gasyoun.github.io/blob/master/.github/workflows/f821-gate.yml))
— a weekly cron (Monday 06:00 UTC, also on pushes to `vote/sheets/**`) that runs
[scripts/check_sheet_staleness.py](https://github.com/gasyoun/gasyoun.github.io/blob/master/scripts/check_sheet_staleness.py)
against the live vote sheets. [handoff-status/index.html](https://github.com/gasyoun/gasyoun.github.io/blob/master/handoff-status/index.html)
is refreshed hourly by an external automation that pushes `public handoff status
refresh <timestamp>` commits — no workflow in this repo generates it.
There is no build step: GitHub Pages serves the static files directly from the
`master` branch.

## CHANGELOG

[CHANGELOG.md](https://github.com/gasyoun/gasyoun.github.io/blob/master/CHANGELOG.md)
has been kept here since 27-09-2026 (started with the karta domain map, H5527): one
entry per published change, newest first — дата · хендофф · что изменилось (the
hourly `handoff-status` refreshes and vote-sheet churn are exempt). The
earlier "no CHANGELOG here, deliberately" ruling (checked 07-09-2026, H3970 residual 3)
is superseded by that file. The artifact conventions still stand: every artifact
carries its own date in the filename (`…-02.09.26.html`) and each section index lists
its pages newest-first.

_Dr. Mārcis Gasūns_
