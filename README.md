# gasyoun.github.io

_Created: 08-10-2014 · Last updated: 10-10-2026_

Personal GitHub Pages site of Mārcis Gasūns ([@gasyoun](https://github.com/gasyoun)),
served at [gasyoun.github.io](https://gasyoun.github.io/). It hosts a handful of
static Sanskrit / Vedic lexicographic experiments — not a blog or CV — kept as
plain HTML and text data.

## What is published here
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
  (~12 MB) — a multilingual Ṛgveda reader. Each stanza is shown as Vedic
  Devanagari, IAST transliteration, and padapāṭha, alongside the Russian
  (Elizarenkova), German (Geldner), and English (Griffith) translations, using
  Indological web fonts served from
  [fonts/](https://github.com/gasyoun/gasyoun.github.io/tree/master/fonts). The
  same document also lives under
  [RV/](https://github.com/gasyoun/gasyoun.github.io/tree/master/RV) with its own
  [rigveda.css](https://github.com/gasyoun/gasyoun.github.io/blob/master/RV/rigveda.css).
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
plus the
[sheet-staleness workflow](https://github.com/gasyoun/gasyoun.github.io/blob/master/.github/workflows/sheet-staleness.yml)
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
entry per published change, newest first — дата · хендофф · что изменилось. The
earlier "no CHANGELOG here, deliberately" ruling (checked 07-09-2026, H3970 residual 3)
is superseded by that file. The artifact conventions still stand: every artifact
carries its own date in the filename (`…-02.09.26.html`) and each section index lists
its pages newest-first.

_Dr. Mārcis Gasūns_
