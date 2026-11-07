# Sources and licences for the word-formation join

The `/wiki/` snapshot itself comes from English Wiktionary and is covered by
[Wiktionary:Copyrights](https://en.wiktionary.org/wiki/Wiktionary:Copyrights)
(CC BY-SA). The word-formation views additionally join that snapshot to nine
local datasets. Exactly which file, revision-independent URL and licence apply
to each one is recorded machine-readably in
[`formation-manifest.json`](formation-manifest.json); the SHA-256 of every
input is in [`manifest.json`](manifest.json).

| Key | Source file | Upstream | Licence / status |
| --- | --- | --- | --- |
| `mw_etymology` | `csl-orig/v02/mw/mw_etymology.tsv` | [sanskrit-lexicon/csl-orig](https://github.com/sanskrit-lexicon/csl-orig/blob/main/v02/mw/mw_etymology.tsv) | CC BY-SA 4.0 |
| `mw_devanagari` | `csl-devanagari/v02/mw/mw.txt` | [sanskrit-lexicon/csl-devanagari](https://github.com/sanskrit-lexicon/csl-devanagari/blob/main/v02/mw/mw.txt) | CC BY-SA 4.0; header also asserts Universität Köln / The Sanskrit Library, 2012 |
| `mw_slp1` | `csl-orig/v02/mw/mw.txt` | [sanskrit-lexicon/csl-orig](https://github.com/sanskrit-lexicon/csl-orig/blob/main/v02/mw/mw.txt) | CC BY-SA 4.0 |
| `whitney_roots` | `WhitneyRoots/crosswalk/roots.csv` | [gasyoun/WhitneyRoots](https://github.com/gasyoun/WhitneyRoots/blob/main/crosswalk/roots.csv) | Apache-2.0 |
| `dcs_lemma2root` | `SanskritRussian/dcs_lemma2root.tsv` | [gasyoun/SanskritRussian](https://github.com/gasyoun/SanskritRussian/blob/main/dcs_lemma2root.tsv) | No LICENSE file in the source repository; machine-derived minimal table, used with attribution |
| `affix_data` | `WhitneyRoots/src/affix_data.json` | [gasyoun/WhitneyRoots](https://github.com/gasyoun/WhitneyRoots/blob/main/src/affix_data.json) | Apache-2.0 |
| `samasa_taxonomy` | `SamasaChakram/samasacakra/samasacakra-taxonomy.json` | [gasyoun/SamasaChakram](https://github.com/gasyoun/SamasaChakram/blob/main/samasacakra/samasacakra-taxonomy.json) | Apache-2.0 |
| `compound_members` | `MWderivations/issue15/compounds_both_sides.tsv` | [gasyoun/MWderivations](https://github.com/gasyoun/MWderivations/blob/master/issue15/compounds_both_sides.tsv) | No LICENSE file in the source repository; aggregate counts only |
| `compound_list` | `MWderivations/compounds/compounds.txt` | [gasyoun/MWderivations](https://github.com/gasyoun/MWderivations/blob/master/compounds/compounds.txt) | No LICENSE file in the source repository; short curated examples only |

## What is actually published

Only **minimal derived joins** are shipped in `wiki/data/`: identifiers,
structured parse fields, class/gloss/period strings, aggregate counts, and
short example lists. The 63 MB / 48 MB dictionary files, the 12.6 MB
`MWderivations/step4/analysis2.txt` (220,248 records) and all full dictionary
entry text stay out of the public site. Every published claim links back to
its own source file or Wiktionary page.

Because the Monier-Williams inputs are CC BY-SA 4.0, the derived fields that
come from them (the `mw*` columns of `formation.js`) are likewise shared under
CC BY-SA 4.0 with attribution to the Cologne Sanskrit Lexicon / The Sanskrit
Library. Where a source repository has no licence file, only aggregate counts
or a handful of short examples are used, with a direct link to the source.

## Deliberately excluded

`/fasmer-2026/zalizniak_matches.tsv` derives from A. A. Zalizniak's
*Grammatical Dictionary of the Russian Language* (6th ed., 2010), whose
rightsholder distributes it under **CC BY-NC**. It is not Sanskrit cognate
evidence and is not used anywhere in `/wiki/`. The Cognate map keeps its
eight Wiktionary-sourced language columns unchanged; no Slavic column was
added without cleared, sourced data.

## Provenance and honesty

`build_formation.py` validates its Devanagari → SLP1 bridge against 8,000
`<L>`-aligned metaline pairs from the two CSL editions on every run and
refuses any unrecognised character instead of emitting a wrong key. Joins are
labelled **candidate cross-references**, not etymologies: homonym roots can
collide (for example MW √hṛ "take" versus Whitney #924 hṛ "be angry"), so the
site never synthesises a new derivation from a join.
