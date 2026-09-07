# gasyoun.github.io

_Created: 08-10-2014 · Last updated: 07-09-2026_

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

## No CHANGELOG here, deliberately

This repository is a publish surface, not a codebase with consumers: every artifact
carries its own date in the filename (`…-02.09.26.html`), each section index lists its
pages newest-first, and `git log` is the only history anyone needs. The org rule that
owes a `CHANGELOG.md` entry per durable artifact is satisfied in the repository that
*produced* the artifact; duplicating it here would be a second, drifting copy. Checked
and confirmed 07-09-2026 (H3970 residual 3) — do not re-open this as an omission.

_Dr. Mārcis Gasūns_
