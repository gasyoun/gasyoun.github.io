# /wiki/ — Sanskrit terms by etymology

_Created: 07-11-2026_

A static teaching view of English Wiktionary's
[Category:Sanskrit terms by etymology](https://en.wiktionary.org/wiki/Category:Sanskrit_terms_by_etymology),
published at <https://gasyoun.github.io/wiki/>.

The source category is a flat alphabetical list of 42 subcategories. This site
regroups them into three pedagogical lenses (provenance, formation, evidence),
charts the entry counts on a single honest scale, and adds an interactive
guṇa/vṛddhi derivation lab. **Every category name, count, bar and example word
links back to its exact original Wiktionary page.** All 42 links were checked
against the MediaWiki API at snapshot time.

## Layout

| Path | Role |
| --- | --- |
| `index.html` | The teaching view. No CDN, no build step — plain HTML/CSS/JS. |
| `style.css` | Shared stylesheet for both pages. |
| `data/etymology.js` | Generated dataset: 42 categories, counts, URLs, lens, descriptions, vowel grades. |
| `data/manifest.js` | Same as `archive/manifest.json`, as a script so pages work without `fetch`. |
| `archive/index.html` | Browsable source archive with checksums and restore notes. |
| `archive/raw/` | Byte-faithful source snapshot (HTML, wikitext, API responses, member tree). |
| `archive/manifest.json` | Provenance, timestamps and SHA-256 for every raw file. |
| `archive/SNAPSHOT.md` | Human-readable full record of the snapshot. |
| `scripts/fetch_snapshot.py` | Re-fetches everything and regenerates all generated files. |

Refresh with `python3 wiki/scripts/fetch_snapshot.py`. It rewrites the raw
files, both manifests, `SNAPSHOT.md` and `data/*.js` with a new UTC timestamp
and fresh checksums. The two HTML pages need no edit when the data changes.

`archive/raw/**` is listed in `.token-gate-ignore`: it is third-party fetched
data, not agent-authored prose, and exceeds the 20 KB staged-file gate.

## Rights

Wiktionary text is available under CC BY-SA; see
[Wiktionary:Copyrights](https://en.wiktionary.org/wiki/Wiktionary:Copyrights).
Category names and counts are reproduced here for teaching and citation, with a
link back to the original on every item.
