# llms.txt census of public GitHub Pages repos — 17-11-2026

_Census taken 17-11-2026 for handoff H8386 (llms.txt on remaining public Pages repos). Method: `gh api repos/gasyoun/<repo>/pages` per public repo (REST, 200 = Pages enabled), then live probe of `https://gasyoun.github.io/<repo>/llms.txt`._

## Summary

- Public repos scanned: 85+ (full `gh repo list`); **public repos with GitHub Pages enabled: 22**
- Already had llms.txt before H8386: **1** (gasyoun.github.io apex, the kosha public dataset catalog)
- llms.txt added by H8386: **20**
- Pages enabled but excluded: **1** (IndologyArchiveAtlas — Pages source = main/, but zero builds and no index.html: nothing is served, so there is no live content to index; revisit when the site actually publishes)
- Note: hub-h7887-8300 also serves an llms.txt but is outside this public-repo census.

## The 22 public Pages repos

| Repo | llms.txt status | Notes |
|---|---|---|
| gasyoun.github.io | pre-existing (apex) | kosha public dataset catalog, generated |
| Systema-Sanscriticum | added | promo + uptime status pages |
| SanskritGrammar | added | digitized grammar sources (Docusaurus) |
| CommentaryStrategies | added | 5-translator commentary analyses |
| SanskritKaraoke | added | karaoke app + catalogue |
| IndologyScholars | added | Zografskie/Rerikhovskie readings dashboard |
| SanskritLexicography | added | PWG article translations (RU/EN) |
| SamudraManthanam | added | nkrya-parallel thesis corpus docs |
| kosha | added | redirects to docs-site |
| BookIndex | added | Зализнякиада companion site |
| WhitneyRoots | added | Whitney dhātu reader |
| VisualDCS | added | DCS visualisations |
| SamasaChakram | added | compound wheel (single-page app) |
| IndologyArchiveAtlas | excluded | Pages on, site never built — nothing served |
| zalizniak-diff | added | two-preprint collation + annotated PDFs |
| RussianRamayana | added | Russian Rāmāyaṇa archive |
| visual-explainer | added | token-tax/BPE/context-window explainers |
| pwg-ru-lod | added | w3id sanskrit-lexicon namespace index |
| ZalizniakVideo | added | 176-video archive + JSON catalogs |
| SanskritRussian | added | glossary TSV/JSONL downloads |
| SanskritMacros | added | EmEditor/Excel/Word macro index |
| AfanasiyNikitin | added | Никитин atlas (ru/en) |

## Convention (v2)

Each `llms.txt` follows the apex reference: `# H1 title`, `> one-line description`, optional prose, `## Sections`, `- [Title](URL): description` bullets. Every URL listed was verified live (HTTP 200) against the repo's Pages site before being indexed; only content actually served is indexed.

Live check: `curl -s https://gasyoun.github.io/<repo>/llms.txt`
