# /wiki/ — Sanskrit terms by etymology

_Created: 07-11-2026 · extended: 07-11-2026_

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
| `explorer.html` | Etymology explorer: search 3,164 real lemmata, filter by lens/category, browse 2,005 second-level source buckets, inspect cross-listed words. |
| `cognates.html` | Cognate map: 18 PIE roots/words × 8 languages, branch filter, sound-correspondence panel. Every reflex links to its Wiktionary entry. |
| `timeline.html` | Timeline of layers: four inheritance strata with real word counts, then internal derivation, contact and uncertainty. |
| `archive/index.html` | Browsable source archive with SHA-256 checksums and restore instructions. |
| `style.css` | Shared stylesheet for all five pages, including the persistent section nav. |

## Data and generators

| Path | Role |
| --- | --- |
| `data/etymology.js` | 42 categories, `c`/`e` counts, exact URLs, lens, descriptions, vowel grades. |
| `data/lemmata.js` | Inverted index: 3,164 unique lemmata with 3,419 category memberships, 2,005 nested source buckets and 2 non-lemma titles. |
| `data/cognates.js` | 18 PIE sets across 8 languages plus 4 inheritance layers, read from 118 Wiktionary categories. |
| `data/manifest.js` | Same as `archive/manifest.json`, as a script so pages work without `fetch`. |
| `scripts/fetch_snapshot.py` | Fetches the category tree and regenerates every derived file. |
| `scripts/fetch_cognates.py` | Fetches the per-language PIE and inheritance-layer member lists. |
| `scripts/etymology_meta.py` | Lens rules, category descriptions and the guṇa/vṛddhi grade table, kept in a separate module so the generator stays under the repo's staged-file token gate. |
| `archive/raw/` | Byte-faithful source responses: HTML, wikitext, rendered intro, API lists, member tree, cognate sets. |
| `archive/manifest.json` | Provenance, timestamps and SHA-256 for all 7 archived files. |
| `archive/cognates-manifest.json` | Exact source URL of each of the 118 queried Wiktionary categories. |
| `archive/SNAPSHOT.md` | Human-readable full record of the snapshot. |

```sh
python3 wiki/scripts/fetch_cognates.py              # network: PIE + layer categories
python3 wiki/scripts/fetch_snapshot.py             # network: full refresh, new timestamp + checksums
python3 wiki/scripts/fetch_snapshot.py --offline   # no network: rebuild derived files from raw/, idempotent
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

## Rights

Wiktionary text is available under CC BY-SA; see
[Wiktionary:Copyrights](https://en.wiktionary.org/wiki/Wiktionary:Copyrights).
Category names, counts and word titles are reproduced here for teaching and
citation, with a link back to the original on every item. The same snapshot is
mirrored in
[gasyoun/sanskrit-etymology-source-archive](https://github.com/gasyoun/sanskrit-etymology-source-archive).
