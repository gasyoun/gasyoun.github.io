# infographics50 — remaining 40 of the catalog (H3705)

_Created: 29-08-2026 · Last updated: 30-08-2026_

Counting scripts + HTML emitter for the 40 catalog rows that were still «идея» after wave 1, plus the H3711 b5 unblocks and eight fresh estate ideas.

## Reproduce

```
python scripts/infographics50/probe.py
python scripts/infographics50/build.py
python scripts/infographics50/h3711_probe.py
python scripts/infographics50/h3711_build.py
node scripts/check.mjs
```

`probe.py` reads local GitHub/ clones (csl-orig, MWinflect, kosha, …) and writes `data/infographics50.json`. `build.py` emits `infographics/<slug>-2026-08-29/index.html` and flips the catalog chips. `h3711_probe.py` / `h3711_build.py` add rows #51–#58 and refresh #18/#27.

## Replacements (catalog notes the probe)

- **#18** Ashtadhyayi city → Somadeva 18+18 chapters (`somadeva/chapters_san|rus`)
- **#27** ORS funnel unblocked from `ORS-FAQ/Tukan_stats.md` public aggregates (no names)
- **#42** Wikipedia vs dictionaries → BookIndex markdown census (no Wikipedia dump on box)

## Gate

`node scripts/check.mjs` — lang=ru, 1080×1920, «Посчитано», script provenance, no TODO. Rows with `"external": true` in `built.json` (pages owned by another lane, e.g. `mw-letters` by the catalog session) skip only the canvas-shape assertion.

PNG: `node scripts/render.mjs` if Playwright is installed; skip is not a fake PNG. As of H3707 every b1 page carries `infographic.png` (+ `.mp4`/`.gif`), rendered with the epic-infographics pipeline (layout gate 0 errors).

## H3707 b1 completion (30-08-2026)

Batch b1 (#2,3,4,5,6,9,11,12,17,50) arrived already emitted by the parallel H3705 sweep; this pass completed the production contract without replacing any page wholesale:

- `probe.py` is box-portable now (estate root via `$GITHUB_ESTATE` / auto-detect; was a hard-coded Windows path), `COUNTED` derives from the run date, header titles unwrap nested `<foreign>` + transcode SLP1→IAST via sanskrit-util (fixes empty `vcp`/`skd`/`shs`/`pui`/`inm`/`pe`/`krm` titles and the `>Goldstücker` artifact), `dict_lang` detects Sanskrit-metalanguage titles (SA), and `mw.anatomy_kfzRa` carries the raw record.
- `patch_titles_h3707.py` re-derived ONLY time-invariant fields (titles/langs/raw record, verified against counted counts) into the committed counted-29.08 JSON; counts untouched.
- Repaired pages: anatomy-mw (raw-record card), morph-snowflake (radial rays + 3×3 slot labels + root center), case-grid (reading-strip), dict-genealogy (inheritance arrows), editions-timeline + dict-passport (real titles).
- Re-derive on any box: `GITHUB_ESTATE=… python scripts/infographics50/probe.py` → regenerating the verbs/nominals `calc_tables.txt` first via MWinflect `redo.sh` chains (see H3707 close note).

_Dr. Mārcis Gasūns_

## H3710 b4 completion (30-08-2026)

Batch b4 (#33,41,42,43,44,46,48,49 + spares prefaces/bookindex) arrived already emitted by the parallel H3705 sweep; this pass completed the production contract without touching any page's counted numbers:

- `infographic.png` rendered for all 9 b4 pages (Playwright, `.canvas` @1080×1920) + `infographic.mp4`/`.gif` for `growth-slider` (rAF counter is not WAAPI-scrubbable, so frames are fresh-load wall-clock captures at 0…2400 ms — real page states, ffmpeg assembly).
- `h3711_probe.py` portability fix (H3710): estate root via `$GITHUB_ESTATE`/auto-detect (was hard-coded `C:\Users\user\Documents\GitHub` from the Windows session); `probe_prefaces` now falls back to `prefaces_X-promote` clones and records which form was counted in `via`.
- Re-derivation spot-check on 30-08-2026: all probes run green on this Mac (`ok=True`); counts differ from the frozen 29.08 JSONs only by estate drift since the count (csl-orig 1 496 157→1 506 391 entries, IndologyScholars CI rebuild 6 841→3 407 md, prefaces 425→500 files across promote renames, BookIndex/SanskritSorting ±). Pages stay frozen at «Посчитано 29.08.2026» — the committed JSONs are the counted evidence.

_Dr. Mārcis Gasūns_
