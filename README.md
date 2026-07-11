# gasyoun.github.io

_Created: 08-10-2014 · Last updated: 11-07-2026_

Personal GitHub Pages site of Mārcis Gasūns ([@gasyoun](https://github.com/gasyoun)),
served at [gasyoun.github.io](https://gasyoun.github.io/). It hosts a handful of
static Sanskrit / Vedic lexicographic experiments — not a blog or CV — kept as
plain HTML and text data.

## What is published here

- **[index.html](https://github.com/gasyoun/gasyoun.github.io/blob/master/index.html)**
  (~12 MB) — a multilingual Ṛgveda reader. Each stanza is shown as Vedic
  Devanagari, IAST transliteration, and padapāṭha, alongside the Russian
  (Elizarenkova), German (Geldner), and English (Griffith) translations, using
  Indological web fonts served from
  [fonts/](https://github.com/gasyoun/gasyoun.github.io/tree/master/fonts). The
  same document also lives under
  [RV/](https://github.com/gasyoun/gasyoun.github.io/tree/master/RV) with its own
  [rigveda.css](https://github.com/gasyoun/gasyoun.github.io/blob/master/RV/rigveda.css).
- **[PWGagainstMW.html](https://github.com/gasyoun/gasyoun.github.io/blob/master/PWGagainstMW.html)**
  — a comparison of PWG (Petersburger Wörterbuch) headwords against
  Monier-Williams, grouped by vowel/consonant patterns, each linking into the
  Cologne [sanskrit-lexicon](https://www.sanskrit-lexicon.uni-koeln.de/) scan
  viewer.
- **Reverse-index / reverse-sort outputs** — devanagari-sorted and
  reverse-sorted word lists derived from headword input:
  [reverse20-ouput/](https://github.com/gasyoun/gasyoun.github.io/tree/master/reverse20-ouput)
  (note the misspelled directory name, preserved as published),
  [reverse21-output/](https://github.com/gasyoun/gasyoun.github.io/tree/master/reverse21-output),
  and
  [reverse22-output/](https://github.com/gasyoun/gasyoun.github.io/tree/master/reverse22-output)
  (with its
  [input.txt](https://github.com/gasyoun/gasyoun.github.io/blob/master/reverse22-output/input.txt)).
- **[296.txt](https://github.com/gasyoun/gasyoun.github.io/blob/master/296.txt)**
  and
  **[296-SLP1.txt](https://github.com/gasyoun/gasyoun.github.io/blob/master/296-SLP1.txt)**
  — a 295-line reverse word-to-page index of a Sanskrit text, in raw and SLP1
  transliteration.

## Leftover scaffolding

[index2.html](https://github.com/gasyoun/gasyoun.github.io/blob/master/index2.html)
and
[params.json](https://github.com/gasyoun/gasyoun.github.io/blob/master/params.json)
are the original GitHub Pages "automatic generator" (Merlot theme) template
files, kept as-is; the served landing page is `index.html`, not `index2.html`.

## Maintenance

The only automation in the repo is Dependabot
([.github/dependabot.yml](https://github.com/gasyoun/gasyoun.github.io/blob/master/.github/dependabot.yml))
with a
[Dependabot auto-merge workflow](https://github.com/gasyoun/gasyoun.github.io/blob/master/.github/workflows/dependabot-auto-merge.yml).
There is no build step: GitHub Pages serves the static files directly from the
`master` branch.

_Dr. Mārcis Gasūns_
