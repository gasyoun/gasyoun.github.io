# infographics50 — remaining 40 of the catalog (H3705)

_Created: 29-08-2026 · Last updated: 30-08-2026_

Counting scripts + HTML emitter for the 40 catalog rows that were still «идея» after wave 1.

## Reproduce

```
python scripts/infographics50/probe.py
python scripts/infographics50/build.py
node scripts/check.mjs
```

`probe.py` reads local GitHub/ clones (csl-orig, MWinflect, kosha, …) and writes `data/infographics50.json`. `build.py` emits `infographics/<slug>-2026-08-29/index.html` and flips the catalog chips.

## Replacements (catalog notes the probe)

- **#18** Ashtadhyayi city → Somadeva 18+18 chapters (`somadeva/chapters_san|rus`)
- **#27** ORS funnel unblocked from `ORS-FAQ/Tukan_stats.md` public aggregates (no names)
- **#42** Wikipedia vs dictionaries → BookIndex markdown census (no Wikipedia dump on box)

## Gate

`node scripts/check.mjs` — lang=ru, 1080×1920, «Посчитано», script provenance, no TODO.

PNG: `node scripts/render.mjs` if Playwright is installed; skip is not a fake PNG.

_Dr. Mārcis Gasūns_
