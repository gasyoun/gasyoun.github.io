# /wiki/ — Sanskrit terms by etymology

_Сreated: 07-11-2026 · extended: 07-11-2026 (formation join)_

A static, offline-capable teaching site built from English Wiktionary's
[Category:Sanskrit terms by etymology](https://en.wiktionary.org/wiki/Category:Sanskrit_terms_by_etymology),
published at <https://gasyoun.github.io/wiki/>.

The source category is a flat alphabetical list of 42 subcategories and **zero
word pages**. The site regroups those labels into three pedagogical lenses
(provenance, formation, evidence), charts the counts on an honest scale, and
adds three study tools over the actual archived vocabulary. **Every category
name, count, bar, lemma, reflex and example word links back to its exact
original Wiktionary page.** No CDN, no build step, no `fetch` — plain
HTML/CSS/JS that also works when the folder is opened from disk.

## Pages

| Path | Role |
| --- | --- |
| `index.html` | Overview: three-lens regrouping, count bars and chips, interactive guṇa/vṛddhi derivation lab. |
| `explorer.html` | Etymology explorer: search 3,164 real lemmata, filter by lens/category, browse 2,005 second-level source buckets, inspect cross-listed words. Prior-work formation panel: 797 lemmata have candidate MW/DCS/Whitney root cross-references. |
| `cognates.html` | Cognate map: 18 PIE roots/words × 8 languages, branch filter, sound-correspondence panel. Every reflex links to its Wiktionary entry. |
| `timeline.html` | Timeline of layers: four inheritance strata with real word counts, then internal derivation, contact and uncertainty. |
| `dhatu.html` | Dhātu desk: 930 Whitney roots with gloss, class, period, frequency and attested forms; site coverage indicator (86.6%); search, sort and filter by class/period. |
| `wordformation.html` | Word formation: 27 affixes (kṛt / taddhita / stri) with surface form, pratyaya, anubandha, function and examples; samāsa taxonomy (4 classes, 9 families, 58 leaves with vigraha); 12 curated compound samples. |
| `archive/index.html` | Browsable source archive with SHA-256 checksums and restore instructions. |
| `style.css` | Shared stylesheet for all fourteen pages, including the persistent section nav, the EN/RU switcher and the `.orig` original-title display. |
| `formation.css` | Formation-specific styles for the Dhātu desk, Word formation pages and Explorer formation panel (split from `style.css` to stay under the 20 KB staged-file token gate). |

## Russian edition (`ru/`)

A complete parallel edition at <https://gasyoun.github.io/wiki/ru/>, with the
same seven pages (`ru/index.html`, `ru/explorer.html`, `ru/cognates.html`,
`ru/timeline.html`, `ru/dhatu.html`, `ru/wordformation.html`,
`ru/archive/index.html`), `<html lang="ru">` and translated
UI, teaching notes, layer names, language/branch labels, sandhi notes,
glosses, and formation page labels. It loads the **same** `data/*.js` files via
`../data/` (the archive via `../../data/`) and the same `style.css` +
`formation.css`, so a snapshot refresh updates both editions together. No
duplicated data, no CDN, no build step.

Source data is deliberately **not** translated: Wiktionary category titles,
Devanagari/IAST lemmata, PIE reconstructions, reflexes in eight languages and
every source URL remain byte-for-byte the ones used by the English pages. A
pairwise comparison of the generated Wiktionary URL sets on initial render
returns zero differences for all five page pairs. The original English
category titles stay available in `title` attributes, are always visible under
the Russian label on the archive page, and can be toggled on the overview with
"Показать оригинальные названия". Every page of both editions carries an EN/RU
switcher plus reciprocal `hreflang` alternates.

## Data and generators

| Path | Role |
| --- | --- |
| `data/etymology.js` | 42 categories, `c`/`e` counts, exact URLs, lens, descriptions, vowel grades. |
| `data/lemmata.js` | Inverted index: 3,164 unique lemmata with 3,419 category memberships, 2,005 nested source buckets and 2 non-lemma titles. |
| `data/cognates.js` | 18 PIE sets across 8 languages plus 4 inheritance layers, read from 118 Wiktionary categories. |
| `data/manifest.js` | Same as `archive/manifest.json`, as a script so pages work without `fetch`. |
| `data/formation.js` | `window.WIKI_FORMATION` — 797 Devanagari lemmata with candidate MW / DCS / Whitney root cross-references (25.6% coverage). Compact row arrays with a warning. |
| `data/roots.js` | `window.WIKI_ROOTS` — 930 Whitney roots with IAST, SLP1, class, gloss, period, frequency, attested forms, MW/Apte IDs, Devanagari, and an `inSite` flag. |
| `data/wordformation.js` | `window.WIKI_WORDFORMATION` — 27 affixes with surface, pratyaya, anubandha, kind, function, examples; samāsa taxonomy (4 classes / 9 families / 58 leaves); 60 compound members; 12 curated compound samples. |
| `data/i18n-ru.js` | `window.WIKI_RU` — Russian translation layer for the `ru/` edition: 42 category labels, 28 descriptions, 18 PIE glosses, layer/language/branch names, 5 sandhi notes, 5 example glosses, 3 grade labels, formation panel strings. Source titles are never translated. |
| `data/i18n-formation.js` | `window.WIKI_FORMATION_I18N` — bilingual EN+RU strings for the Dhātu desk and Word formation pages (section titles, labels, warnings, source attributions). |
| `scripts/fetch_snapshot.py` | Fetches the category tree and regenerates every derived file. |
| `scripts/fetch_cognates.py` | Fetches the per-language PIE and inheritance-layer member lists. |
| `scripts/build_formation.py` | Offline pipeline joining site Devanagari lemmata to prior-work root, derivation, affix and compound datasets. No network, no external packages; Devanagari→SLP1 converter validated against 8,000 aligned MW metalines on every run. |
| `scripts/etymology_meta.py` | Lens rules, category descriptions and the guṇa/vṛddhi grade table, kept in a separate module so the generator stays under the repo's staged-file token gate. |
| `archive/raw/` | Byte-faithful source responses: HTML, wikitext, rendered intro, API lists, member tree, cognate sets, formation-sources provenance record. |
| `archive/manifest.json` | Provenance, timestamps and SHA-256 for all 9 archived files. |
| `archive/cognates-manifest.json` | Exact source URL of each of the 118 queried Wiktionary categories. |
| `archive/formation-manifest.json` | Provenance, licences, converter validation and checksums for the 9 prior-work inputs and 3 derived data modules. |
| `archive/SOURCES-LICENSES.md` | Mixed-licence attribution for all nine prior-work datasets; documents the deliberate exclusion of CC BY-NC Zalizniak/Fasmer data. |
| `archive/SNAPSHOT.md` | Human-readable full record of the snapshot. |

```sh
python3 wiki/scripts/fetch_cognates.py              # network: PIE + layer categories
python3 wiki/scripts/fetch_snapshot.py             # network: full refresh, new timestamp + checksums
python3 wiki/scripts/fetch_snapshot.py --offline   # no network: rebuild derived files from raw/, idempotent
python3 wiki/scripts/build_formation.py            # offline: join prior-work datasets, generate formation.js / roots.js / wordformation.js
python3 wiki/scripts/build_formation.py --offline  # no source repos: replay from raw/formation-sources.json
```

The HTML pages need no edit when the data changes. `--offline` preserves the
original snapshot timestamp, so checksums stay reproducible even if Wiktionary
is unreachable.

`archive/raw/**`, `archive/cognates-manifest.json` and the generated `data/*.js`
files are listed in `.token-gate-ignore`: they are third-party fetched or
generated data, not agent-authored prose, and exceed the 20 KB staged-file gate.

## Scope and honesty

The crawl is **one level deep**: it captures direct members of the 42
subcategories, not the full contents of the 2,005 nested buckets. The explorer
is a faithful, citable sample of how Wiktionary files Sanskrit words, not a
complete lexicon. `c` (subcategories) and `e` (word pages) are different units
and are never added together; bars are only comparable within a single unit.

The prior-work formation join produces **candidate cross-references, not new
etymologies**. The Devanagari→SLP1 converter is validated against 8,000 aligned
MW metalines (99.83% accuracy), but homonym roots can collide and editorial
spellings diverge. Every field in the formation panel links to its own source;
deriving the etymology remains the student's work. Only minimal derived joins
are published — never dictionary text. See
[`archive/SOURCES-LICENSES.md`](https://gasyoun.github.io/wiki/archive/SOURCES-LICENSES.md)
for the full attribution and licence statement.

## Rights

Wiktionary text is available under CC BY-SA; see
[Wiktionary:Copyrights](https://en.wiktionary.org/wiki/Wiktionary:Copyrights).
Category names, counts and word titles are reproduced here for teaching and
citation, with a link back to the original on every item. The same snapshot is
mirrored in
[gasyoun/sanskrit-etymology-source-archive](https://github.com/gasyoun/sanskrit-etymology-source-archive).
