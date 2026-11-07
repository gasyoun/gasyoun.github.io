# Source archive — Sanskrit terms by etymology

_The backup half of <https://gasyoun.github.io/wiki/>._

Byte-faithful, checksummed snapshot of
[Category:Sanskrit terms by etymology](https://en.wiktionary.org/wiki/Category:Sanskrit_terms_by_etymology)
on English Wiktionary, plus its 42 subcategories and every direct member one
level down. See [index.html](index.html) for the browsable version,
[manifest.json](manifest.json) for provenance and SHA-256 digests, and
[SNAPSHOT.md](SNAPSHOT.md) for the complete readable record.

## Why the parent page alone is not a backup

The parent category has **zero word pages** — only subcategories. Copying that
one HTML page preserves 42 labels and none of the vocabulary. This snapshot
therefore also walks each subcategory and stores its direct children, 5,426
titles in total, so the taxonomy can be reconstructed offline.

## Files

- `raw/category.html` — original page as served, unmodified bytes.
- `raw/category-rendered.json` — `action=parse&prop=text`; preserves the
  template-generated introductory definitions, which are absent from wikitext.
- `raw/category-wikitext.json` — the page's entire wikitext, `{{auto cat}}`.
- `raw/subcategories.json` — API listing of the 42 subcategory titles.
- `raw/subcategory-members.json` — each of the 42 mapped to its direct
  subcategories and word pages.

Verify with `shasum -a 256 <file>` against `manifest.json`.

## Redundancy

The snapshot is committed here in the Pages repo **and** mirrored in the
independent repository
[gasyoun/sanskrit-etymology-source-archive](https://github.com/gasyoun/sanskrit-etymology-source-archive).
Loss of either repo leaves the other intact.

## Rights

Wiktionary text is available under CC BY-SA; see
[Wiktionary:Copyrights](https://en.wiktionary.org/wiki/Wiktionary:Copyrights).
This archive reproduces category names, counts and structure for teaching,
citation and preservation, with the original URL recorded for every item.
