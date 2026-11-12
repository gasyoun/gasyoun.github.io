# DATA_LAYERS_CENSUS.md — the data we own but never counted

_Created: 06-07-2026 · Last updated: 29-10-2026_

**Purpose.** A QA/gap-finding census of the **data layers** across the ~85 canonical
repos, built by harvesting the filesystem (not the curated inventory). Where
[`FEATURES_INDEX.md`](https://github.com/gasyoun/SanskritLexicography/blob/master/FEATURES_INDEX.md)
answers *"what did we consciously register as an asset?"*, this file answers the
opposite: **what large data is sitting on disk that was never raised to asset level,
never counted, and never analysed?** It is a defect-finder, not a catalogue — every
row is meant to prompt "should this be backed up / registered / deduplicated / turned
into a statistic?".

**Scope vs. the kosha manifest (ruling F7, 26-08-2026).**
[`kosha/data/manifest/datasets.json`](https://github.com/gasyoun/kosha/blob/main/data/manifest/datasets.json)
is the registry for **published, fetchable** derived datasets — the ones another repo
or a human is meant to pull down and consume. This census stays the **human survey of
large on-disk data**, including data that is **not publishable** (rights-uncertain,
personal, or simply not worth shipping) — a giant belongs here whether or not it will
ever earn a manifest row.

> Harvest method: `os.walk` over the org clone root, data extensions only (`.jsonl .json
> .tsv .csv .txt .db .sqlite .conllu .xml .parquet …`), 1 MB threshold for "large".
> Tracked-vs-local classified by `git ls-files` membership. **Committed re-run:**
> [`tools/data_layers_harvest.py`](https://github.com/gasyoun/Uprava/blob/main/tools/data_layers_harvest.py)
> (H1989, 31-07-2026) — replaces the original throwaway `harvest.py` + `classify2.py`.
> Latest snapshot: [`reports/DATA_LAYERS_HARVEST_SNAPSHOT_2026-08-22.md`](https://github.com/gasyoun/Uprava/blob/main/reports/DATA_LAYERS_HARVEST_SNAPSHOT_2026-08-22.md)
> + [`data/data_layers_harvest_2026-08-22.json`](https://github.com/gasyoun/Uprava/blob/main/data/data_layers_harvest_2026-08-22.json)
> (H3316, OxAlpha `x-preview-f-free`; previous: [`reports/DATA_LAYERS_HARVEST_SNAPSHOT_2026-07-31.md`](https://github.com/gasyoun/Uprava/blob/main/reports/DATA_LAYERS_HARVEST_SNAPSHOT_2026-07-31.md)
> + [`data/data_layers_harvest.json`](https://github.com/gasyoun/Uprava/blob/main/data/data_layers_harvest.json)).
> Sizes below mix the **31-07-2026 re-harvest** (headline / §1) with older per-file notes
> that still carry their measurement dates; re-verify before acting on a single path.

---

## At a glance

- **22-08-2026 re-harvest (H3316, OxAlpha `x-preview-f-free`):** **31.58 GB** large files
  (≥1 MB) across **157** top-level dirs; **1,599** large files; tracked **11.08 GB (35%)**
  vs local-only **20.50 GB (65%)** — local-only *absolute* down ~1.2 GB and its share down
  2 pts since 31-07. FEATURES_INDEX basename hit **36** / miss **1,563**. Every anonymous
  no-consumer accumulation now named — see §6.
- **31-07-2026 re-harvest (H1989):** **32.3 GB** large files (≥1 MB) across **158** top-level
  dirs under `GitHub/` (scope wider than the original ~90 — see Method); **1,646** large files;
  FEATURES_INDEX basename hit **38** / miss **1,608**.
- **Tracked 10.6 GB (33%) · local-only 21.7 GB (67%)** — local-only *share* slightly down from
  the 06-07 **~70% / 19.2 GB** framing, but **absolute** local-only grew (~+2.5 GB) with new
  giants (SpellCheck DTA zip, spoken-sanskrit segments, nagari.db, nkrya-parallel).
- Historical 06-07 baseline (kept for delta): ~27.5 GB large / 1,343 unregistered / 8.3 GB tracked.
- One file — `archive_stopword.sqlite` — is still **~10.5 GB**, larger than every tracked repo combined.
- ✅ **H691 provenance sweep (11-07-2026, Fable 5 `claude-fable-5`):** every *then*-listed §2
  giant has SHA256 + live counts + schema + rebuild recipe in the
  [kosha manifest](https://github.com/gasyoun/kosha/blob/main/data/manifest/datasets.json)
  ([kosha PR #52](https://github.com/gasyoun/kosha/pull/52)). Of the old “19.2 GB single-copy”
  headline, only `corpus_lexicon.jsonl` (~277 MB on 31-07) is genuinely single-copy-and-not-
  rebuildable — **new** 31-07 giants (DTA zip, segments.jsonl, …) still need the same
  regenerate-vs-backup classification. **Update 25-10-2026:** the corpus_lexicon half of
  this sentence is superseded by the §2 row below (H3316/H3389): it is no longer
  single-copy, and the current state is recorded there with a dated verification.
- ✅ **GAPS §3 graduated 31-07-2026 → [FINDINGS §261](https://github.com/gasyoun/Uprava/blob/main/FINDINGS.md)** —
  the “never counted” claim is closed; residual unknowns are listed there, not a blank estate.

The headline QA finding is not "we lack statistics." It is that **the majority of our
derived data still sits local-only** — statistics (mostly done) and provenance (H691 for
the old giants) come first; **new** local-only arrivals need the same treatment.

---

## 1 · Data footprint per repo (tracked vs local-only)

**31-07-2026 re-harvest** (large files ≥1 MB only). Full table:
[`reports/DATA_LAYERS_HARVEST_SNAPSHOT_2026-07-31.md`](https://github.com/gasyoun/Uprava/blob/main/reports/DATA_LAYERS_HARVEST_SNAPSHOT_2026-07-31.md).

| Repo | Total | Tracked (shareable) | 🔴 Local-only | Files | Dominant |
|---|--:|--:|--:|--:|---|
| [VisualDCS](https://github.com/gasyoun/VisualDCS) | 14.7 GB | 2.6 GB | **12.2 GB** | 214 | `.sqlite .csv .txt` |
| [SanskritSpellCheck](https://github.com/gasyoun/SanskritSpellCheck) | 2.8 GB | 0.2 GB | **2.6 GB** | 48 | `.zip .txt .jsonl` |
| [SamudraManthanam](https://github.com/gasyoun/SamudraManthanam) | 2.5 GB | 0.7 GB | **1.8 GB** | 157 | `.db .txt .jsonl` |
| [kosha](https://github.com/gasyoun/kosha) | 2.1 GB | 0.4 GB | **1.8 GB** | 34 | `.db .tsv .sqlite` |
| [SanskritLexicography](https://github.com/gasyoun/SanskritLexicography) | 1.8 GB | 0.4 GB | **1.5 GB** | 110 | `.jsonl .tsv .json` |
| [VCP](https://github.com/sanskrit-lexicon/VCP) | 0.74 GB | 0.74 GB | 0.00 | 48 | `.txt .tsv` |
| [spoken-sanskrit-corpus](https://github.com/gasyoun/spoken-sanskrit-corpus) | 0.70 GB | 0.00 | **0.70 GB** | 2 | `.jsonl` |
| [MWS](https://github.com/sanskrit-lexicon/MWS) | 0.58 GB | 0.58 GB | 0.00 | 62 | `.txt .zip .xml` |
| [csl-json](https://github.com/sanskrit-lexicon/csl-json) | 0.49 GB | 0.49 GB | 0.00 | 34 | `.json` |
| [csl-devanagari](https://github.com/sanskrit-lexicon/csl-devanagari) | 0.48 GB | 0.48 GB | 0.00 | 35 | `.txt` |
| [mw-dev](https://github.com/sanskrit-lexicon/mw-dev) | 0.46 GB | 0.46 GB | 0.00 | 20 | `.txt .xml .zip` |
| [csl-orig](https://github.com/sanskrit-lexicon/csl-orig) | 0.42 GB | 0.38 GB | 0.04 GB | 53 | `.txt .jsonl .tsv` |
| [PWG](https://github.com/sanskrit-lexicon/PWG) | 0.39 GB | 0.39 GB | 0.00 | 106 | `.txt` |
| [IndologyScholars](https://github.com/gasyoun/IndologyScholars) | 0.38 GB | 0.06 GB | **0.32 GB** | 64 | `.db .zip .json` |
| [ORS-FAQ](https://github.com/gasyoun/ORS-FAQ) | 0.36 GB | 0.00 | **0.36 GB** | 4 | `.json .jsonl` |

_SpellCheck jumped from ~0.3 GB (06-07) to **2.8 GB** because `external_src/dta/dta_lingattr.zip`
(2.53 GB) is now on disk — the largest new local-only arrival. Full tail (AP, PWK, CORRECTIONS,
Systema, …) is in the snapshot report._

---

## 2 · 🔴 Local-only giants — single-copy, unbackuped, uncounted

Every file below is **not tracked by git** (gitignored or never added). If this disk dies,
they are gone. None is registered as an asset. Ranked by size.

**Exact counts (measured 06-07-2026; rows marked H691 re-measured 11-07-2026 with SHA256s
recorded in the [kosha manifest](https://github.com/gasyoun/kosha/blob/main/data/manifest/datasets.json)):**

| File | Rows / entries |
|---|--:|
| `kosha/data/db/kosha.db` | 444,773 entries · 323,425 lemmas · 692,403 senses · 1,378,401 forms · **6,916,522 inflections** (8 tables — H691: the live 05-07 build has NO `heritage_anchor`, the H345 ingest is absent) |
| `SamudraManthanam/web/corpus.db` | **580,552 corpus lines** · 152 sources (H691; was 574,939·148 on 06-07 — still growing) |
| `VisualDCS/src/DCS-data-2026/dcs_full.sqlite` | **5,688,416 tokens** · 754,726 sentences · 180,176 lemmas · 1,024,841 mwt · 270 texts (H691 confirmed) |
| `…/src/corpus_lexicon.jsonl` | **1,093,391 aligned rows** (H691; was 1,091,528 — append-only, growing) |
| `…/glossary/surface_glossary.jsonl` | 190,838 surface entries (H691 confirmed) |
| `…/src/assembled_cards*.jsonl` (all 4 variants) | **120,173 each — identical row count → intermediate stages redundant** |
| `VisualDCS/derived-data/Kompozity/names.csv` (tracked) | 168,880 compounds |
| `CORRECTIONS/ngram/allngramtxt.txt` (tracked) | **6,656,616 n-grams** |
| `csl-observatory/…/correction_events_all.csv` (tracked) | 52,499 events |
| `kosha/data/raw_sqlite/{mw,pwg,ap90}.sqlite` | mw 286,525 · pwg 123,366 · ap90 34,882 (H691; sums to kosha.db's 444,773 entries) |
| `archive_stopword.sqlite` (11 GB) | ✅ **40,573,260 stop-word parallels** + 3 aux tables (H691, 48 s scan — matches the [M9 validation report](https://github.com/gasyoun/VisualDCS/blob/main/src/DCS-data-2026/reports/m9_archive_ingest.md) exactly) |
| `SamudraManthanam/web/offline-packs/{base,dict}.db` | base 320,902 + dict 254,037 lines (H691; SHA256s match their `.sha256` sidecars) |
| `ORS-FAQ/result.json` (190 MB) | ~~not UTF-8 (cp1251)~~ — **flag was WRONG**: UTF-8 with ONE truncated Cyrillic byte @1,523,038 (Telegram name-cap artifact); sanitized `result.utf8.json` beside it, both gitignored. Counted + verdict 11-07-2026 (H693, [ORS-FAQ PR #82](https://github.com/gasyoun/ORS-FAQ/pull/82)) |


| Size | File | What it (probably) is | Action |
|--:|---|---|---|
| 11.0 GB | `VisualDCS/src/DCS-data-2026/archive_stopword.sqlite` | 40.57 M stop-word parallels (M9 D2) | ✅ counted + SHA256 (H691) — **fully regenerable** from tracked `Stopovye/` CSVs (`import_archive.py stopword`), no backup needed; manifest row `archive-stopword-sqlite` |
| 921 MB | `VisualDCS/src/DCS-data-2026/dcs_full.sqlite` | DCS 2026 full corpus DB | ✅ schema + SHA256 registered (H691); regenerable from DCS CoNLL-U (CC BY 4.0). **Doc-of-record (26-07-2026, H1407): [DCS_SQLITE_CONLLU_CONSUMER_DEEP_MANUAL.md](https://github.com/gasyoun/VisualDCS/blob/main/docs/DCS_SQLITE_CONLLU_CONSUMER_DEEP_MANUAL.md)** — read before querying (schema, vintages, fold rule, G1–G18 gotchas). **✅ BACKED UP 23-08-2026 (H3389)**: `samskrtam.ru/guhya/dcs_full.sqlite`, sha256 `8f3b06bd…bb23bc` (= registered) |
| 619 MB | `SamudraManthanam/web/corpus.db` | Sa↔Ru verse-parallel corpus (published translations) | ✅ counted + SHA256 (H691): 580,552·152; **NOT single-copy** — regenerates from git-tracked `corpus_builder/jsonl` |
| 361 MB | `SanskritGrammar/Concordance/UshaSanka_Ph.D_2014/` (dir) | Usha Sanka 2014–15 kāraka-PhD working corpus — Dhātupāṭha `dhatu_chart.csv` + `mAdhavIya-dhAtupATha.xlsx` + `dhatu-index.xlsx`, Aṣṭādhyāyī sūtrapāṭha XLSX (3,983 sūtras), 587 `DhatuVistara/*.html` per-verb concordance pages, PWG verb entries, and the kāraka-demand model as clean-Unicode `धातुकारकाकांक्षा.docx` | 🔴 **untracked, single-copy, unbackuped** — do NOT commit wholesale; extract structured derivations only (the [`Concordance/usha_karaka_gold/`](https://github.com/gasyoun/SanskritGrammar/tree/main/Concordance/usha_karaka_gold) kāraka gold already shipped, [SanskritGrammar #484](https://github.com/gasyoun/SanskritGrammar/pull/484)). Reuse survey: [`USHA_SANKA_KARAKA_TROVE_REUSE_SURVEY_2026.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/Concordance/USHA_SANKA_KARAKA_TROVE_REUSE_SURVEY_2026.md). **Rights (corrected 20-07-2026):** Usha's thesis was **published 2014** → her selection/analysis is reusable with attribution (NOT the earlier "unpublished/needs-permission"). Third-party works cleared too: Krishnacharya 1924 public-domain by age; Abhyankar 1961 + Palsule 1955/61 + *Bhāratīya Upasargārtha-Candrikā* 1976 all rights-held (MG) (H1395/H1399) |
| 290 MB | `SanskritLexicography/…/src/corpus_lexicon.jsonl` | 1.09 M aligned Sa→Ru rows (A1, registered but gitignored) | 🔴 H691-confirmed the **ONLY genuine single-copy giant** — NOT rebuildable (DeepSeek alignment); backup pending MG-gated H235. **Update 22-08-2026 (H3316 dual-run): no longer *single-copy*** — a byte-identical **git-tracked twin** now exists at `pwg-ru-data/corpus/corpus_lexicon.jsonl` (SHA-256 `9f3d852f…4072` verified identical to both the working copy and the H1998 `D:\Backups` mirror); master + one tracked GitHub copy + **off-machine leg CLOSED 23-08-2026 (H3389)**: digest-verified copy at samskrtam.ru/guhya/corpus_lexicon.jsonl (sha256 9f3d852f…4072 re-confirmed at upload). **Verified 25-10-2026:** the Mac master path is **absent**; `pwg-ru-data/corpus/corpus_lexicon.jsonl` is a **Git-LFS pointer** (134 B, oid `9f3d852f…4072`, size 290,543,363) — the bytes live in the LFS store, not in the worktree; a private restore from that LFS object hashed identical (`9f3d852f…4072`, dir 0700, file 0600). The guhya leg is **UNVERIFIED today**: FTPS to `t3cloud.ru` answers `530 Login incorrect` (stored password rotated), no `.env.deploy` on the Mac. Do not call this row three-copy until the guhya leg is re-proven. |
| 216 MB | `SamudraManthanam/web/offline-packs/base.db` | offline app pack (13-06 corpus snapshot) | ✅ rebuildable via `build_offline_pack.py` from corpus.db; SHA256s verified vs sidecars (H691); manifest row `samudra-offline-packs` |
| 210 MB×4 | `SanskritLexicography/…/src/assembled_cards*.jsonl` | 4 progressive variants (~810 MB total) | **✅ stages 1–3 DELETED 12-07 (~580 MB, content-contained per H692); keeper `.renou.bhs.wl` retained** |
| 190 MB | `ORS-FAQ/result.json` | Telegram Desktop full-account export (funnel DMs) | ✅ counted 11-07-2026 (H693): 3,180 chats / 170,017 msgs 2022-09→2026-07-05 / 8,729 contacts; **not stale** — caches newer, Track B drops DMs so nothing supersedes it. [Provenance](https://github.com/gasyoun/ORS-FAQ/blob/main/docs/telegram_export_result_json_provenance.md) |
| 147 MB | `SanskritLexicography/…/glossary/surface_glossary.jsonl` | surface-layer Sa→Ru glossary (A2 layer) | ✅ **backed up after all** (H691): tracked as `surface_glossary.jsonl.gz` in [gasyoun/SanskritRussian](https://github.com/gasyoun/SanskritRussian); also rebuildable from corpus_lexicon |
| 96 MB | `MWinflect/…/tables/calc_tables.txt` | generated inflection tables | ✅ generated — recipe documented (H695): [docs/INFLECTION_TABLES_PROVENANCE.md](https://github.com/sanskrit-lexicon/MWinflect/blob/main/docs/INFLECTION_TABLES_PROVENANCE.md); `decline_file.py` from `calc_stems.txt` (deterministic) — re-verified 12-07 by FULL-file regen: whole 96 MB byte-identical (md5 match), 44 s; `.gitignore`d, safe to exclude from backup/dedup |
| 164 MB | `kosha/data/raw_sqlite/{mw,pwg,ap90}.sqlite` | per-dict raw SQLite loaded into kosha.db | ✅ verified re-fetchable (H691): `build_entries.py` re-downloads the csl-sqlite release `2026-06-28-08-27-31`; manifest row `kosha-raw-sqlite` |

**Two recurring defects visible in this list:**
1. **Duplicate pipeline variants** — the `assembled_cards.jsonl` → `.renou.jsonl` →
   `.renou.bhs.jsonl` → `.renou.bhs.wl.jsonl` series (four ~200 MB stages, ~810 MB) is
   **content-contained: all four carry the identical 120,173 rows, earlier stages fully
   — only the final stage need survive (~607 MB). The per-dict `{code}.renou` (dot) vs
   `{code}_renou.bhs.wl` (underscore) families are **NOT** byte-redundant — they diverge
   (12-07-2026) ruled that divergence a **correction**: the dot-file is canonical and the
   `_renou*` chain over-attests (it predates the DCS min-support filter), so the ~379 MB
   underscore chain is **safe to delete as superseded** (not merged, not renamed).

---


MG's Yandex Disk (`rclone yadisk:`, WebDAV) scanned read-only: **13,963 files · 224.53 GB · 64 folders**. Research giants: ААЗализняк-архив 108.8 GB (txt 266 + **srt 200** + mp3 261), Dark_library 23.6 GB (368 pdf), Sanskrityatina workshop 26.7 GB (55 dirs), Panini 10.1 GB, kRtam own-corpus (Параллели 621 CSV 4.2 GB, Lazarus dictionary src, Композиты). Publishing: Frish multivolume chrestomathy 27 toms InDesign 8 GB. Full classification + Top-10 reusable candidates: [reports/YADISK_INVENTORY_07-09-2026.md](https://github.com/gasyoun/Uprava/blob/main/reports/YADISK_INVENTORY_07-09-2026.md). Landing = derived-only (H1333 precedent).

---

## 3 · Statistics to add, per layer (and where they live)

The question "what statistics, where" resolves to one table. Each row is a stat that is
currently **not** computed, the QA question it answers, and its home.

| Layer | Source | Statistic to compute | QA question it answers | Home |
|---|---|---|---|---|
| **Dictionary text** | `csl-orig` `<L>` records | **sense/polysemy distribution per dict — ◐ partial (11/44) 13-07-2026** (H817, FEATURES_INDEX **E45**, mirrors the A02 paper's `r2_h1.json`): [report](https://github.com/sanskrit-lexicon/csl-observatory/blob/main/reports/sense_polysemy_per_dict.md); family trait not diachronic trend (r=0.036); remaining 33 dicts genuinely blocked — no structural sense-marking, and `<L>` decimal-suffix numbering confirmed NOT a valid proxy (verified H817, dead end recorded) | is polysemy a school trait or a time trend? | csl-observatory + csl-atlas A02 |
| **Dictionary text** | restricted KoshaSHRI single-entry response + H7296 `pd_work_edition_map.tsv` | H7316 fixture counted 29-10-2026: [`pd_koshashri_entries.tsv`](https://github.com/sanskrit-lexicon/csl-atlas/blob/main/data/pd/pd_koshashri_entries.tsv) = one `agni` entry / 16 columns / 723,876 bytes; [`pd_koshashri_citations.tsv`](https://github.com/sanskrit-lexicon/csl-atlas/blob/main/data/pd/pd_koshashri_citations.tsv) = 1,400 reference rows / 15 columns / 708,516 bytes; all 29 senses, first-sense 242 texts→248 rows, only exact `ṚV.` resolved. Both are below the 1 MB large-data threshold but registered because the source is rights-restricted. Regenerate together with `python3 scripts/pd_koshashri_fixture_export.py`, prove `--check` + five offline tests; schemas and rights in sibling `.meta.md` files. Full JSON remains local-only and uncommitted | can the fixture be regenerated without a second parser, bulk publication or guessed work identities? | csl-atlas `data/pd` + kosha restricted manifest |
| **Commentaries/OCR** | Sundara, preface_* | ~~apparatus notes count~~ **посчитано 10-07-2026**: 1058 ярус-1 + 897 ярус-2 (pre-gate), зарегистрировано в kosha-манифесте как [`sundarakanda-two-tier-apparatus`](https://github.com/gasyoun/kosha/blob/main/data/manifest/datasets.json) (restricted, [kosha PR #43](https://github.com/gasyoun/kosha/pull/43)) · остаются: OCR pages per dict · % translated | front-matter/apparatus completeness | per-repo |
| **Telegram** | `telegram-sanskrit-corpus` | messages · tokens · date span · unique senders — ✅ recomputed 20-09-2026 post-drain: [`tools/corpus_stats.py`](https://github.com/gasyoun/telegram-sanskrit-corpus/blob/main/tools/corpus_stats.py) + [assessment](https://github.com/gasyoun/telegram-sanskrit-corpus/blob/main/docs/CORPUS_STATS.md). **2605 messages / 56 837 tokens / span 2025-11-03 → 2026-09-20 / 139 unique senders** (supersedes the stale 11-07 H690 all-zero row; H690 predates the first real harvest). author_hash is epoch 2 since 20-09 (H2669-era salt lost; not comparable to epoch-1 refs 1029/979/78). Privacy gate passed 20-09; **verdict: corpus-grade on volume + scrub mechanics, not yet citable** — publication still needs the versioned-snapshot + named-source Legal gate | that repo |

**Priority order for QA value:** (1) the local-only-backup gap in §2, (2) ~~the "keys with
no RU gloss" gap-list (directly feeds Tier-1 RussianTranslation)~~ ✅ done 11-07-2026 (H685), (3) the `<ls>` citation
graph (highest publishable novelty), (4) ~~the code-duplication census (measures the
`sanskrit-util` dedup payoff)~~ ✅ done 12-07-2026 (H688).

---

## 4 · Actionable gaps (mirror to GTD)

- ✅ **Back up `corpus_lexicon.jsonl` (277 MB / 290,543,363 B)** — **local dual-drive mirror
  done 31-07-2026 (H1998, Grok 4.5 `grok-4.5`)**: SHA-256
  `9f3d852f1f1424c275af2cc1823dab1b561e649320e597d3cab013068ccc4072` identical on
  `SanskritLexicography/…/src/corpus_lexicon.jsonl` and
  `D:\Backups\csl-data-layers\SanskritLexicography\RussianTranslation\src\`.
  Also mirrored the irreplaceable ReverseDictionary master (`266820-reverse-Gasuns.txt`).
  Script retiered: [`tools/backup_census_priority.py`](https://github.com/gasyoun/Uprava/blob/main/tools/backup_census_priority.py)
  defaults to **IRREPLACEABLE-only** + `--local-mirror` (regenerable giants no longer
  pollute the default run). 🔴 **Yandex / off-machine leg still open** — needs local
  `YANDEX_DISK_*` env (H235-era @DO). Do **not** priority-backup `archive_stopword.sqlite`
  or `dta_lingattr.zip` (rebuild / re-fetch). **Update 22-08-2026 (H3316):** a third copy of
  the master landed as a **tracked** file in [gasyoun/pwg-ru-data](https://github.com/gasyoun/pwg-ru-data)
  (`corpus/corpus_lexicon.jsonl`, SHA-256 identical) — the "irreplaceable single-copy"
  status is retired; remaining risk is only the off-machine leg.
- 🟢 **Prune superseded Renou variants** — **`{code}_renou*` underscore chain ✅ DELETED
  12-07-2026 (~362 MB freed, MG authorization; superseded per
  dot-file canonical, chain over-attests).** Also **✅ DELETED 12-07-2026 (~580 MB freed, MG
  authorization):** `assembled_cards` stages 1–3 (content-contained, verified 120,173-row parity
  + field-superset keeper; only the final `assembled_cards.renou.bhs.wl.jsonl` survives,
  Net ~942 MB freed across both. Small `.chunk`/`.perf`/`.smoke`/`.test`/`.quarantine` fixtures kept.
- ✅ **Register the tracked-but-uncounted assets** in `FEATURES_INDEX.md` — done 11-07-2026
  (H694, Fable 5 `claude-fable-5`): `CORRECTIONS/ngram/allngramtxt.txt` (6,656,616 n-grams, 82.3 MB → F43),
  `VisualDCS/derived-data/Kompozity/names.csv` (168,880 compounds, 90.7 MB → E42),
  the `csl-observatory` `correction_events_{all,typed,final}.csv` trio (52,498 events × 3, 178.0 MB → E41);
  [SL PR #350](https://github.com/gasyoun/SanskritLexicography/pull/350) + kosha manifest rows
  ([kosha PR #53](https://github.com/gasyoun/kosha/pull/53), ids `correction-events-log`,
  `kompozity-names-compound-splits`, `cdsl-headword-ngram-oracle`).
- ✅ `VisualDCS/derived-data/Paralleli-v-tekstah-korpusa-SRC/PARA/Stopovye/`
  (102 files, **1.17 GB**, the largest single derived-data bundle in the repo) —
  checked here 07-07-2026 (H291): it is git-**tracked** (113 objects incl. a
  split `.7z`), so it does not belong in § 2's unbackuped-giants table; instead
  registered as a bundle row (`stopovye-parallel-passages`) in
  [`kosha/data/manifest/datasets.json`](https://github.com/gasyoun/kosha/blob/main/data/manifest/datasets.json).

---

## 5 · The 27-07 no-consumer accumulation census (72 catalogued items) — reconciled 30-07-2026

Source: [ASK_BATCH_STAGING_FABLE_ROADMAP_HARVEST_2026-07.md](https://github.com/gasyoun/Uprava/blob/main/archive/ASK_BATCH_STAGING_FABLE_ROADMAP_HARVEST_2026-07.md)
§ "The data that is piling up — 72 catalogued accumulations" (27-07-2026, Opus 5 1M
`claude-opus-5[1m]`, `/ask-batch`): data on disk with **no downstream consumer found**,
harvested as a side-output of the Fable-tier roadmap sweep. Ten of the sweep's minted
handoffs (H1754–H1763) drain six of these rows in aggregate, but the source doc does not
map which six — the mint list and the accumulation list are reported as separate totals,
not a row-to-row crosswalk, so that mapping cannot be reconstructed after the fact.

**Honest enumeration limit.** The source doc lists 72 as a *count*, not 72 named rows —
its prose names roughly a dozen items with enough path specificity to re-stat individually
(the rest were only visible in the harvesting session's per-agent workflow journals, which
are ephemeral subagent transcripts, never committed, and not recoverable from this session).
Per this handoff's scope fence ("apply the most conservative reading that satisfies the
acceptance criteria, log it, press on"), the reconciliation below covers every item the
manifest names concretely, re-stated against the filesystem as of 30-07-2026 rather than
copied from the 27-07 figures. The remaining ~60 items named only in the manifest's
size/count roll-up prose cannot be individually rowed without re-running the harvest —
that gap is recorded here rather than silently closed.

| Path | Repo | Size / count (30-07-2026) | Consumer? | Notes |
|---|---|--:|---|---|
| `derived-data/` | [VisualDCS](https://github.com/gasyoun/VisualDCS) | 3.5 GB, 18 top-level entries (14 topic folders per the 27-07 count; `PARA/` subtree alone ~1.5 GB / 606 files) | ◐ one of 14 topics has ever been written up | Overlaps §1's VisualDCS row (16.0 GB total) — this is the derived-data slice specifically, not yet its own row there |
| `PDFtoTXT/` | [RuWritingStyles-corpus](https://github.com/gasyoun/RuWritingStyles-corpus) | 143 MB, 27 files (was "~15 PDF+TXT pairs, six with no consumer" 27-07) | 🔴 no | New row |
| `data/pwg_*` (10 dirs) | [SanskritGrammar](https://github.com/gasyoun/SanskritGrammar) | 28.5 MB total (compound_split 941K · derivation_graph 2.1M · gana_membership 413K · german_glosses 6.3M · ghostword_triage 276K · lex_pos 2.4M · lexicon_only_audit 2.7M · lid_hom_map 3.5M · panini_crosswalk 1.6M · register_genre 8.1M) | 🔴 only own README + generator reference each | New row |
| `nagari/data/processed/` | [IndologyScholars](https://github.com/gasyoun/IndologyScholars) | 897 KB, 12 CSVs (was "10,310 rows" 27-07) | 🔴 no `ARTICLES.md` row despite being the twin corpus of the ORS VK wall | New row |
| `runs/` | [RuWritingStyles](https://github.com/gasyoun/RuWritingStyles) | 1,462 run directories (was 1,356 on 27-07 — still growing, ~2/day) | 🔴 only aggregates ever surface | New row |
| `sheet-h1213dict.json` | RuWritingStyles | 286 KB (27-07 figure; exact path not relocated within this pass's search budget) | 🔴 waits on a single ~5-min human vote (precedent: vedic-r02 adjudication) | New row — re-stat deferred |
| `data/lexico/h4_semantic_field_review_packet.json` (+ `r2_checkpoint_review_packet.json` 36 KB, `r2_review_packets.json` 180 KB) | [csl-atlas](https://github.com/sanskrit-lexicon/csl-atlas) | 312 KB + 36 KB + 180 KB = 528 KB | 🔴 stalled on three outstanding human exports | New row |
| `docs/course_page_*.md` (21 files) | ORS-FAQ | 256 KB total (was 206,768 B 27-07) | 🔴 blocked on `WP_APP_PASSWORD` | New row |
| `reports/consumed_by_baseline_2026-07.md` | [csl-observatory](https://github.com/sanskrit-lexicon/csl-observatory) | 19,280 B | 🔴 self-reporting doc (flags 10/80 manifest assets with zero consumers) has no consumer of its own | New row |

**Dedup verdict:** 1 of 12 named items (ORS-FAQ's Telegram export) was already a §2 row —
no duplicate added. 1 of 12 (Uprava's `telegram-zabota-export/result.json`) has gained a
consumer since 27-07 and is marked consumed rather than dropped. The remaining 10 are new
rows above.

**What this does not close:** the ~60 accumulations visible only in the manifest's
size/count prose (e.g. the aggregate "six with no consumer" inside RuWritingStyles-corpus's
PDFtoTXT pairs, or SanskritGrammar's ten `pwg_*` directories counted as one bucket) are
captured at the bucket level above, not the individual-file level the acceptance criteria
originally envisioned — that finer grain no longer exists outside this reconciliation.
Re-running the harvest (`/ask-batch`'s underlying `os.walk` + no-consumer cross-ref, same
method as §"Method & reproduce" below) is the only way to recover it. **Closed 22-08-2026 —
see §6.**

---

## 6 · The 22-08 accumulation naming pass (H3316) — every anonymous accumulation named

The §5 honest-enumeration limit is closed. The fresh harvest (At a glance, 22-08) was
re-classified by
[`tools/data_layers_accumulations.py`](https://github.com/gasyoun/Uprava/blob/main/tools/data_layers_accumulations.py)
over the committed inventory
[`data/data_layers_harvest_2026-08-22.json`](https://github.com/gasyoun/Uprava/blob/main/data/data_layers_harvest_2026-08-22.json):
**217 of the 1,599 large files are both local-only and FEATURES_INDEX-unregistered**;
adaptive directory bucketing names them as **67 accumulation rows — each with a producing
repo, a consumer verdict, and a keep/prune-candidate flag; 0 unadjudicated**. Mechanical
facts: [`reports/DATA_LAYERS_ACCUMULATIONS_2026-08-22.tsv`](https://github.com/gasyoun/Uprava/blob/main/reports/DATA_LAYERS_ACCUMULATIONS_2026-08-22.tsv);
adjudication: [`reports/DATA_LAYERS_ACCUMULATIONS_2026-08-22.verdicts.json`](https://github.com/gasyoun/Uprava/blob/main/reports/DATA_LAYERS_ACCUMULATIONS_2026-08-22.verdicts.json)
— the table below is regenerable from those two (`--verdicts --md-out`), not hand-typed.
Scope fence held: **this pass classifies only; nothing was deleted or moved.**
Deletion candidates above are proposals for a later MG review sheet.

**Dual-run provenance (claim-holder adjudication, 22-08-2026).** Two independent OxAlpha
(`x-preview-f-free`) sessions executed H3316 concurrently — the claim holder (14:13Z) and
a second session that worked in the same worktree without checking the live claim. Both ran
full harvests 12 minutes apart with **byte-identical totals** (1,599 large files,
33,904,216,315 B; tracked 11,894,462,164 B vs local-only 22,009,754,151 B), diverging only
in dir count 156 vs 157 (one empty-of-large-files dir appeared between runs) — an inter-run
parity check, recorded here as validation. The landed pass is the second session's
(fbadc9ea); this paragraph and the two `corpus_lexicon.jsonl` updates above are the claim
holder's adjudication layer. One verdict refinement for MG's review sheet: `dta_lingattr.zip`
is **not agent-regenerable but IS human-refetchable** — the upstream public zip it came from
is named in [`detectors/extract_dta_pairs.py`](https://github.com/gasyoun/SanskritSpellCheck/blob/main/detectors/extract_dta_pairs.py)
(`dta-lingattr-tei_*.zip` from deutschestextarchiv.de/download); backup-vs-refetch stays MG's call.
The −1.2 GB local-only drop since 31-07 is explained by an external prune of
[SamudraManthanam](https://github.com/gasyoun/SamudraManthanam)'s local layer measured on disk
this pass: `nkrya-parallel` bulk removed (was ~0.9 GB local-only on 31-07; remainder tracked),
`web/corpus.db` zeroed to 0 B (gitignored generated search DB), `web/offline-packs/` emptied to
`.gitkeep` (rebuild recipe: `web/scripts/build_offline_pack.py`; prod status H2392). Zero-deletion
proof for both layers: `git diff --name-status origin/main..HEAD` shows A/M entries only.

### Post-H691 giants — regenerate-vs-backup verdicts

| Giant | Size (22-08) | Verdict | Evidence |
|---|--:|---|---|
| `segments.jsonl` ([spoken-sanskrit-corpus](https://github.com/gasyoun/spoken-sanskrit-corpus) `data/derived/`) | 752.7 MB | **REGENERABLE** — prune-candidate after one provenance re-run | derived stage output `raw_transcript.text → tools/clean_asr.py → segments.jsonl` (docstring line 10); transcripts fetched via `tools/fetch_transcripts.py`; pipeline in [PIPELINE_MANUAL.md](https://github.com/gasyoun/spoken-sanskrit-corpus/blob/main/docs/PIPELINE_MANUAL.md) |
| `nagari.db` ([IndologyScholars](https://github.com/gasyoun/IndologyScholars) `nagari/data/`) | 202.7 MB | **REGENERABLE — but backup target is its source, not the DB** | rebuilt by [nagari/scripts/run_pipeline.py](https://github.com/gasyoun/IndologyScholars/blob/main/nagari/scripts/run_pipeline.py) step `[1/4] ingest mbox → SQLite`; source dump `nagari-2005-2026/nagari@googlegroups.com` is **1.79 GB single-copy UNTRACKED** — new backup debt found by this pass |
| `nkrya-parallel` ([SamudraManthanam](https://github.com/gasyoun/SamudraManthanam)) | 7.7 MB | **DEMOTED — not a giant** | measured 81 files / 7.7 MB, **81/81 git-tracked** (`git ls-files nkrya-parallel`); corrects the 27-07 prose that listed it among giants; git itself is the backup, no action |

None of the three real giants carries an H691 kosha-manifest row (checked live:
107 manifest rows, zero basename hits) — they are post-H691 arrivals, exactly the gap the
31-07 At-a-glance flagged.

**H3180 backup disposition (23-08-2026).** All three post-H691 giants now have a
weekly restic estate copy (tags `local-data-layer,w4`, snapshot `e47ee898`):
`dta_lingattr.zip` and the `nagari-2005-2026/` mbox primary are **included**;
`segments.jsonl` is included as cheap insurance despite its REGENERABLE flag
(regeneration needs live fetches). One conflict recorded rather than silently
resolved: §2 says `archive_stopword.sqlite` is "fully regenerable … no backup
needed" (H691/H1989 manifest ruling) while this section's table flags it
"KEEP · backup-priority (top)" — Wave 4 followed the older regenerable ruling and
**excluded** the 11 GB file, so the estate does not carry it until MG rules which
row wins (@DECIDE, logged in
[docs/BACKUP_W4_LOCAL_DATA_LAYER_RUN_2026-08-23.md](https://github.com/gasyoun/Uprava/blob/main/docs/BACKUP_W4_LOCAL_DATA_LAYER_RUN_2026-08-23.md)).
Same run also excluded the `dcs_full.sqlite.gz` twin (PRUNE-candidate row above),

### Full classification table (67 rows)

> **⚠ Verdict update 05-09-2026 (H4177, MG chat vote on 8 prune items):** the table below
> predates the vote. Canonical verdicts now live in the regenerated
> [`reports/DATA_LAYERS_ACCUMULATIONS_2026-08-22.md`](https://github.com/gasyoun/Uprava/blob/main/reports/DATA_LAYERS_ACCUMULATIONS_2026-08-22.md)
> (+ `.verdicts.json` sidecar, same date): items 1–6 **APPROVED-DELETE** (Windows-side, SHA-proofed; item 1 conditional on the H3389 nonlocal backup — met), item 3 after one builder smoke,
> item 7 `segments.jsonl` **LEAVE AS IS**, item 8 `archive_stopword.sqlite` **BACKUP IT**
> (H691-vs-H3316 conflict resolved in favor of backup-priority; restic-include @DO open).
> Audit: [`review/weekly/archive/decisions_applied_2026-09-05_data-noise-prune-vote.md`](https://github.com/gasyoun/Uprava/blob/main/review/weekly/archive/decisions_applied_2026-09-05_data-noise-prune-vote.md).

[generated-table: DATA_LAYERS_ACCUMULATIONS_2026-08-22 · regen: tools/data_layers_accumulations.py --json data/data_layers_harvest_2026-08-22.json --tsv reports/DATA_LAYERS_ACCUMULATIONS_2026-08-22.tsv --max-files 28 --max-depth 4 --verdicts reports/DATA_LAYERS_ACCUMULATIONS_2026-08-22.verdicts.json --md-out reports/DATA_LAYERS_ACCUMULATIONS_2026-08-22.md]

| Accumulation | Repo | Files | MB | Consumer verdict | Keep / prune |
|---|---|--:|--:|---|---|
| `VisualDCS/src/DCS-data-2026/archive_stopword.sqlite` | VisualDCS | 1 | 11,039.1 | none found — raw DCS archive state, the 11 GB single-copy giant (At-a-glance since 06-07) | KEEP · backup-priority (top) |
| `kosha/` | kosha | 4 | 1,918.2 | service DB (H687 completeness audit: complete for scope) + raw_sqlite with H691 provenance rows (SHA256 + rebuild recipes) | rebuildable from csl-orig · backup pending H235 |
| `VisualDCS/src/DCS-data-2026/dcs_full.sqlite` | VisualDCS | 1 | 920.9 | counted + provenance row (H691 §1); VisualDCS src loaders | KEEP · backup pending H235 |
| `spoken-sanskrit-corpus/` | spoken-sanskrit-corpus | 1 | 752.7 | derived stage output: raw_transcript.text -> tools/clean_asr.py -> segments.jsonl (docstring line 10) | REGENERABLE · prune-candidate after one provenance re-run |
| `VisualDCS/src/DCS-data-2021` | VisualDCS | 2 | 483.2 | delta-stat baseline — §4 rules '2021 NOT superseded - keep' | KEEP |
| `ORS-FAQ/` | ORS-FAQ | 4 | 386.7 | result.json/result.utf8.json counted (H693); gap = duplicate untracked copy + missing manifest row (§5 dedup rows) | PRUNE duplicate · register manifest row |
| `IndologyScholars/nagari` | IndologyScholars | 28 | 308.2 | nagari.db REGENERABLE from mbox dump via nagari/scripts/run_pipeline.py step [1/4] ingest.build() (DB derived); attachments = Google-Group scans (incl. Wilson dictionaries) feeding extract_attachments.py -> processed CSVs | backup target = mbox primary (nagari-2005-2026/, 1.79 GB single-copy UNTRACKED), not the DB; KEEP sources |
| `SanskritLexicography/RussianTranslation/src/corpus_lexicon.jsonl` | SanskritLexicography | 1 | 290.5 | feeds H685 gap-stats builder; no longer single-copy per H3316 layer-2 dual-run: SHA256-identical git-tracked twin at pwg-ru-data/corpus/corpus_lexicon.jsonl (9f3d852f…4072, verified vs H1998 D:\Backups mirror). **25-10-2026:** the master file is absent on the Mac and the "twin" is an LFS pointer (oid match only); the only full local copy this pass was a private LFS restore | local copy absent on the Mac (25-10-2026) · off-machine guhya leg recorded CLOSED 23-08-2026 but re-verification blocked 25-10-2026 (FTPS 530) · do not prune on the "redundant" premise |
| `VisualDCS/src/DCS-data-2026/dcs_full.sqlite.gz` | VisualDCS | 1 | 287.7 | gzip twin of dcs_full.sqlite — redundant compressed copy | PRUNE-candidate after SHA256 match |
| `csl-pywork/v02/tempparent/mw` | csl-pywork | 10 | 248.4 | pywork build temp trees; pure build artifacts rebuildable from csl-orig via make_xml.py path | PRUNE-candidate (verify rebuild first) |
| `csl-pywork/v02/tempparent/pwg` | csl-pywork | 7 | 241.6 | pywork build temp trees; pure build artifacts rebuildable from csl-orig via make_xml.py path | PRUNE-candidate (verify rebuild first) |
| `SanskritLexicography/RussianTranslation/src/assembled_cards.renou.bhs.wl.jsonl` | SanskritLexicography | 1 | 209.7 | RU translation pipeline intermediates built over csl-orig/kosha upstreams by tracked in-repo builders | regenerable · prune-candidate individually after builder smoke |
| `SanskritLexicography/RussianTranslation/src/assembled_cards.jsonl` | SanskritLexicography | 1 | 191.6 | RU translation pipeline intermediates built over csl-orig/kosha upstreams by tracked in-repo builders | regenerable · prune-candidate individually after builder smoke |
| `VisualDCS/src/DCS-data-2026/archive.sqlite` | VisualDCS | 1 | 167.5 | raw DCS dump variant backing src loaders | KEEP · backup candidate |
| `SanskritGrammar/` | SanskritGrammar | 8 | 161.4 | ApteSyntax_1885 scan zip + misc source scans | KEEP (scans) · backup candidate |
| `SanskritLexicography/RussianTranslation/glossary` | SanskritLexicography | 2 | 152.7 | ru_gloss_gaps.tsv is the H685 deliverable (README-linked consumer) | KEEP · register |
| `MWinflect/` | MWinflect | 5 | 135.6 | pysanskritv2 stems intermediates under nominals/ | regenerable · prune-candidate after check |
| `SanskritLexicography/RussianTranslation/src/mw.renou.jsonl` | SanskritLexicography | 1 | 106.8 | RU translation pipeline intermediates built over csl-orig/kosha upstreams by tracked in-repo builders | regenerable · prune-candidate individually after builder smoke |
| `csl-pywork/v02/tempparent/mw72` | csl-pywork | 7 | 90.2 | pywork build temp trees; pure build artifacts rebuildable from csl-orig via make_xml.py path | PRUNE-candidate (verify rebuild first) |
| `SanskritLexicography/RussianTranslation/src/pwg.renou.jsonl` | SanskritLexicography | 1 | 83.6 | RU translation pipeline intermediates built over csl-orig/kosha upstreams by tracked in-repo builders | regenerable · prune-candidate individually after builder smoke |
| `VisualDCS/src/DCS-data-2026/conllu` | VisualDCS | 26 | 81.5 | conllu pipeline outputs (files/ + lookup/) feeding tracked conllu/observatory derived TSVs; rebuildable from dcs_full.sqlite | regenerable · prune-candidate after parity check |
| `SanskritLexicography/RussianTranslation/src/pw.renou.jsonl` | SanskritLexicography | 1 | 73.1 | RU translation pipeline intermediates built over csl-orig/kosha upstreams by tracked in-repo builders | regenerable · prune-candidate individually after builder smoke |
| `csl-pywork/v02/tempparent/ap90` | csl-pywork | 7 | 61.9 | pywork build temp trees; pure build artifacts rebuildable from csl-orig via make_xml.py path | PRUNE-candidate (verify rebuild first) |
| `Uprava/` | Uprava | 4 | 58.7 | Tochka_*.csv gitignored money data (+ .db) — bank exports | KEEP local-only · money/personal-data fence, never publish |
| `VisualDCS/src/DCS-data-2026/exports` | VisualDCS | 5 | 57.1 | clean CSV exports feeding derived-data builds; rebuildable from dcs_full.sqlite | regenerable · keep local |
| `SanskritLexicography/RussianTranslation/src/kosha_syn.jsonl` | SanskritLexicography | 1 | 48.4 | RU translation pipeline intermediates built over csl-orig/kosha upstreams by tracked in-repo builders | regenerable · prune-candidate individually after builder smoke |
| `SanskritLexicography/RussianTranslation/src/snap.jsonl` | SanskritLexicography | 1 | 40.9 | RU translation pipeline intermediates built over csl-orig/kosha upstreams by tracked in-repo builders | regenerable · prune-candidate individually after builder smoke |
| `csl-orig/` | csl-orig | 5 | 37.5 | etymology jsonl sidecars inside the fenced upstream repo | KEEP (fenced upstream) |
| `RuWritingStyles/` | RuWritingStyles | 1 | 34.8 | rws.db — council engine state store | KEEP |
| `VisualDCS/src/DCS-data-2026/dcs.sqlite` | VisualDCS | 1 | 31.9 | raw DCS dump variant backing src loaders | KEEP · backup candidate |
| `SanskritLexicography/RussianTranslation/src/apte_hi.jsonl` | SanskritLexicography | 1 | 31.8 | RU translation pipeline intermediates built over csl-orig/kosha upstreams by tracked in-repo builders | regenerable · prune-candidate individually after builder smoke |
| `SanskritLexicography/RussianTranslation/src/dcs_freq_dims.json` | SanskritLexicography | 1 | 30.8 | RU translation pipeline intermediates built over csl-orig/kosha upstreams by tracked in-repo builders | regenerable · prune-candidate individually after builder smoke |
| `SanskritLexicography/RussianTranslation/research` | SanskritLexicography | 5 | 30.2 | research sidecars (apte_sidecar.tsv etc.) feeding RU copy work | KEEP · register case-by-case |
| `SanskritLexicography/RussianTranslation/src/dcs_lemma_renou.json` | SanskritLexicography | 1 | 29.2 | RU translation pipeline intermediates built over csl-orig/kosha upstreams by tracked in-repo builders | regenerable · prune-candidate individually after builder smoke |
| `SanskritLexicography/RussianTranslation/src/ap.renou.jsonl` | SanskritLexicography | 1 | 28.4 | RU translation pipeline intermediates built over csl-orig/kosha upstreams by tracked in-repo builders | regenerable · prune-candidate individually after builder smoke |
| `IndologyScholars/vk-ors` | IndologyScholars | 2 | 26.9 | VK wall scrape outputs feeding ORS funnel analysis | KEEP · register |
| `SanskritLexicography/RussianTranslation/src/pwg_ru_translated.jsonl` | SanskritLexicography | 1 | 26.2 | RU translation pipeline intermediates built over csl-orig/kosha upstreams by tracked in-repo builders | regenerable · prune-candidate individually after builder smoke |
| `SanskritLexicography/RussianTranslation/src/pilot` | SanskritLexicography | 10 | 25.4 | RU translation pipeline intermediates built over csl-orig/kosha upstreams by tracked in-repo builders | regenerable · prune-candidate individually after builder smoke |
| `SanskritLexicography/HeadwordLists` | SanskritLexicography | 7 | 24.9 | headword-export-regen diff outputs (_diff added/removed lists); entry anatomy census via `/entry-anatomy`, regen+diff via `/headword-export-regen` (wired H5790, 03-10-2026) | regenerable · KEEP |
| `SanskritLexicography/RussianTranslation/src/ap90.renou.jsonl` | SanskritLexicography | 1 | 22.4 | RU translation pipeline intermediates built over csl-orig/kosha upstreams by tracked in-repo builders | regenerable · prune-candidate individually after builder smoke |
| `SanskritLexicography/review` | SanskritLexicography | 2 | 14.2 | Cologne-call timedtext + review notes | KEEP |
| `RussianRamayana/` | RussianRamayana | 1 | 14.0 | _meta/files mirror zip of RuWritingStyles-main — redundant copy of a tracked repo tarball | PRUNE-candidate (duplicate mirror) |
| `SanskritLexicography/RussianTranslation/src/ben.renou.jsonl` | SanskritLexicography | 1 | 12.8 | RU translation pipeline intermediates built over csl-orig/kosha upstreams by tracked in-repo builders | regenerable · prune-candidate individually after builder smoke |
| `SanskritLexicography/RussianTranslation/src/bhs.renou.jsonl` | SanskritLexicography | 1 | 12.8 | RU translation pipeline intermediates built over csl-orig/kosha upstreams by tracked in-repo builders | regenerable · prune-candidate individually after builder smoke |
| `SanskritLexicography/RussianTranslation/src/sch.renou.jsonl` | SanskritLexicography | 1 | 12.5 | RU translation pipeline intermediates built over csl-orig/kosha upstreams by tracked in-repo builders | regenerable · prune-candidate individually after builder smoke |
| `SanskritLexicography/RussianTranslation/src/pwg_sense_stratum.jsonl` | SanskritLexicography | 1 | 11.5 | RU translation pipeline intermediates built over csl-orig/kosha upstreams by tracked in-repo builders | regenerable · prune-candidate individually after builder smoke |
| `IndologyScholars/_site` | IndologyScholars | 6 | 11.0 | site analytics outputs incl. human_review_index.csv | KEEP · register |
| `SanskritLexicography/RussianTranslation/src/assembled_cards.perf.jsonl` | SanskritLexicography | 1 | 8.4 | RU translation pipeline intermediates built over csl-orig/kosha upstreams by tracked in-repo builders | regenerable · prune-candidate individually after builder smoke |
| `SanskritLexicography/RussianTranslation/src/dcs_freq.json` | SanskritLexicography | 1 | 6.5 | RU translation pipeline intermediates built over csl-orig/kosha upstreams by tracked in-repo builders | regenerable · prune-candidate individually after builder smoke |
| `SanskritLexicography/RussianTranslation/src/_review_queue.jsonl` | SanskritLexicography | 1 | 5.9 | RU translation pipeline intermediates built over csl-orig/kosha upstreams by tracked in-repo builders | regenerable · prune-candidate individually after builder smoke |
| `BookIndex/` | BookIndex | 3 | 5.5 | dist-vite build module JSONs | regenerable build output · keep local |
| `SanskritLexicography/RussianTranslation/src/koch.jsonl` | SanskritLexicography | 1 | 5.3 | RU translation pipeline intermediates built over csl-orig/kosha upstreams by tracked in-repo builders | regenerable · prune-candidate individually after builder smoke |
| `SanskritLexicography/RussianTranslation/src/vedic_rituals_hi.jsonl` | SanskritLexicography | 1 | 4.4 | RU translation pipeline intermediates built over csl-orig/kosha upstreams by tracked in-repo builders | regenerable · prune-candidate individually after builder smoke |
| `SanskritLexicography/RussianTranslation/src/_review_queue.csv` | SanskritLexicography | 1 | 4.2 | RU translation pipeline intermediates built over csl-orig/kosha upstreams by tracked in-repo builders | regenerable · prune-candidate individually after builder smoke |
| `csl-standards/` | csl-standards | 1 | 4.2 | p5subset.xml TEI standards subset used by validators | KEEP |
| `SanskritLexicography/RussianTranslation/pwg_ru` | SanskritLexicography | 1 | 3.9 | learner_scores.tsv for the pwg_ru lane | KEEP · register |
| `SanskritLexicography/RussianTranslation/src/kow.jsonl` | SanskritLexicography | 1 | 3.9 | RU translation pipeline intermediates built over csl-orig/kosha upstreams by tracked in-repo builders | regenerable · prune-candidate individually after builder smoke |
| `SanskritLexicography/literature` | SanskritLexicography | 1 | 3.1 | kos_01.txt corpus text | KEEP |
| `SanskritLexicography/RussianTranslation/src/pwg_ru_relationships.jsonl` | SanskritLexicography | 1 | 3.0 | RU translation pipeline intermediates built over csl-orig/kosha upstreams by tracked in-repo builders | regenerable · prune-candidate individually after builder smoke |
| `SanskritLexicography/RussianTranslation/review` | SanskritLexicography | 1 | 1.7 | H215-gold evidence-coverage review artifact | KEEP |
| `MWS/` | MWS | 1 | 1.6 | mw-microanalysis-supplementary.zip (paper supplementary) | KEEP |
| `SanskritLexicography/RussianTranslation/src/smirnov.jsonl` | SanskritLexicography | 1 | 1.5 | RU translation pipeline intermediates built over csl-orig/kosha upstreams by tracked in-repo builders | regenerable · prune-candidate individually after builder smoke |
| `SanskritLexicography/RussianTranslation/src/fri.jsonl` | SanskritLexicography | 1 | 1.2 | RU translation pipeline intermediates built over csl-orig/kosha upstreams by tracked in-repo builders | regenerable · prune-candidate individually after builder smoke |
| `IndologyScholars/profile_output.txt` | IndologyScholars | 1 | 1.1 | profiler stdout artifacts | transient · PRUNE-candidate |
| `IndologyScholars/profile_utf8_fast.txt` | IndologyScholars | 1 | 1.1 | profiler stdout artifacts | transient · PRUNE-candidate |
| `VisualDCS/src/DCS-data-2026/staging` | VisualDCS | 1 | 1.1 | in-progress ingest staging (Meghaduta.jsonl) | KEEP until pipeline done |


---

## Method & reproduce

**Committed (H1989, 31-07-2026):**
[`tools/data_layers_harvest.py`](https://github.com/gasyoun/Uprava/blob/main/tools/data_layers_harvest.py)
— single stdlib walker that sizes large data files, classifies tracked-vs-local via
`git ls-files`, and optionally marks FEATURES_INDEX basename registration.

```
python tools/data_layers_harvest.py --root C:\Users\user\Documents\GitHub ^
  --json-out data/data_layers_harvest.json ^
  --md-out reports/DATA_LAYERS_HARVEST_SNAPSHOT_YYYY-MM-DD.md
```

Exclusions (name heuristics, not a hard allow-list): `*-h###*` worktrees, `Uprava-*` /
`SanskritLexicography-*` / `IndologyScholars-*` / `SanskritGrammar-*` sidecars, `temp_*`,
`claude-config-*` / `codex-config-*`, utility clones
(`Retrieval-based-Voice-Conversion-WebUI`, `SOCKS5-VPS`), plus `node_modules` / `vendor` /
`.git` walk-prunes. The 06-07 throwaway pair (`harvest.py` + `classify2.py`) is retired —
do not re-derive it.

**Committed (H3316, 22-08-2026):**
[`tools/data_layers_accumulations.py`](https://github.com/gasyoun/Uprava/blob/main/tools/data_layers_accumulations.py)
— stdlib classifier over the harvest JSON: keeps local-only + unregistered files, buckets
them at adaptive directory granularity (`--max-files 28 --max-depth 4`), merges an
authored verdict sidecar (longest-prefix match), and emits the TSV + classification
markdown table of §6. The harvest's snapshot header now takes `--model-run` (was
hardcoded to one lane and mis-stamped provenance).

```sh
python tools/data_layers_accumulations.py \
  --json data/data_layers_harvest_2026-08-22.json \
  --tsv reports/DATA_LAYERS_ACCUMULATIONS_2026-08-22.tsv \
  --max-files 28 --max-depth 4 \
  --verdicts reports/DATA_LAYERS_ACCUMULATIONS_2026-08-22.verdicts.json \
  --md-out reports/DATA_LAYERS_ACCUMULATIONS_2026-08-22.md
```

Related hubs: [`FEATURES_INDEX.md`](https://github.com/gasyoun/SanskritLexicography/blob/master/FEATURES_INDEX.md)
(what's registered) · [`PROJECT_INTERLINKS.md`](https://github.com/gasyoun/Uprava/blob/main/PROJECT_INTERLINKS.md)
(who feeds whom) · [`SHARED_CODE.md`](https://github.com/gasyoun/github-spine/blob/main/SHARED_CODE.md)
(the actions from §4) · [GAPS §3 → FINDINGS §261](https://github.com/gasyoun/Uprava/blob/main/FINDINGS.md).

_Dr. Mārcis Gasūns_

## 7 · Process-mining event layer (H4394, 08-09-2026)

New owned layer: the hashed per-case business event log produced by
[`tools/pm_extract_events.py`](https://github.com/gasyoun/Uprava/blob/main/tools/pm_extract_events.py)
from the Systema prod DB (read-only, tunnel path of `pull_samskrte_db.py`).

| Artifact | Tracked? | Grain | Regenerable |
|---|---|---|---|
| `data/process_min/events_YYYYMMDD.tsv` | gitignored — private per-case (salted-hash ids, no names/emails) | one row per (case × activity) | one command, read-only pull |
| `data/process_min/pm_extract_summary_YYYYMMDD.json` | **tracked** | aggregates + frozen G1/G2/G3 gate verdict | derived — regen, never hand-edit |
| `data/process_min/.salt` | gitignored, 0600 | hash salt, stable per box | created once, never regenerated silently |

Contours and PII classes: [docs/PROCESS_MINING_SOURCES_2026-09.md](https://github.com/gasyoun/Uprava/blob/main/docs/PROCESS_MINING_SOURCES_2026-09.md);
frozen gate/thresholds: [docs/PROCESS_MINING_PREREGISTRATION_2026-09.md](https://github.com/gasyoun/Uprava/blob/main/docs/PROCESS_MINING_PREREGISTRATION_2026-09.md)
(pre-registered 2026-09-08T16:02:08Z, BEFORE first extractor run).


---

## 8 · Image layer registration (H5507, 26-09-2026)

| Layer | Count | Where | Licence | Status |
|---|--:|---|---|---|

---

## 9 · PD machine-readable text layer (H6718, 15-10-2026)

The Poona Dictionary's machine-readable text and its committed derivations, registered per
the 14-10-2026 PD grill (Q4). Headline numbers follow

> **Scope caveat, on every number:** the digital text exercises the letter-*a* canon only up
> to **~apaca-** — the fascicles **issued 1976–2009** (vols. 1.1–9.x). The printed record has
> since reached Vol. 35 / 6,056 pp by 2019, still inside letter *a*; that post-2009 print
> canon is *additional* material the text does not carry.

| Role | Artifact | Size / count | Where · status |
|---|---|---|---|
| **Source** (staged, gitignored) | `pd.txt` — Cologne **PDScan 2020** machine-readable text (`pdtxt.zip`, member `txt/pd.txt`); © 2014 The Sanskrit Library / Thomas Malten, CC BY-NC-SA 3.0 | **55 MB · 107,630 `<L>` entries · ~104,959 lemmas** (letter-*a* canon ≤ **~apaca-**) | re-stage locally via `get_external_source.py`; canonical URL <https://sanskrit-lexicon.uni-koeln.de/scans/PDScan/2020/downloads/pdtxt.zip> (HTTP 200, probed 11-10-2026) |
| ↳ derived · committed (1/12) | `pd_dcs_text_crosswalk.tsv` | 118 rows | [csl-atlas `data/pd/`](https://github.com/sanskrit-lexicon/csl-atlas/tree/main/data/pd) · H1336, 20-07-2026 |
| ↳ derived · committed (2/12) | `pd_siglum_families.tsv` | 5,106 sigla | H1336 |
| ↳ derived · committed (3/12) | `pd_siglum_raw.tsv` | 5,106 sigla | H1336 |
| ↳ derived · committed (4/12) | `dcs_text_inventory.tsv` | DCS bounded 276-text inventory | H1336 |
| ↳ derived · committed (5/12) | `pd_dcs_metrics.json` | headline metrics + mass breakdown | H1336 · rebased H6707, 14-10-2026 |
| ↳ derived · committed (6/12) | `letter_anatomy.tsv` | per-letter samasa/upasarga anatomy | H1416, 21-07-2026 |
| ↳ derived · committed (7/12) | `letter_anatomy_stats.json` | per-dict anatomy stats sidecar | H1416 |
| ↳ derived · committed (8/12) | `entry_size_by_position.tsv` | entry size by position (funding-decay test) | H1416 |
| ↳ derived · committed (9/12) | `upasarga_counts.tsv` | every preverb × every dict | H1416 follow-up |
| ↳ derived · committed (10/12) | `compound_share_by_letter.tsv` | compound share per letter (dash-truth wave) | H1423, 21-07-2026 |
| ↳ derived · committed (11/12) | `density_fingerprint.tsv` | density fingerprint (chars / spans / markup tags per entry) | H1423 |
| ↳ derived · committed (12/12) | `entry_size_by_year.tsv` | entry size by real year (decay test) | H1423 |

The `data/pd/` directory has since gained three AOB declared-canon TSVs (H6707, 14-10-2026) —
`pd_aob_declared_works.tsv`, `pd_aob_fuzzy_short_adjudication.tsv`, `pd_aob_siglum_title.tsv` —
plus the H6923 denominator audit (`pd_aob_declared_canon_audit.json`, 17-10-2026: what 1,419 /
1,118 / 1,464 each measure, band 7.78–8.32 %) and the H6720/H6941 reconciliation
(`pd_aob_entries.tsv`, 1,430 printed entries with their match route and exercise state;
`pd_aob_sigla_reconciliation.tsv`, 2,954 classed discrepancy rows; `pd_aob_sigla_reconciliation.json`,
three presence measures + the 269-of-681 printed-text confirmations), and its
[README](https://github.com/sanskrit-lexicon/csl-atlas/blob/main/data/pd/README.md)
carries the per-file descriptors; the per-file row counts above are from that README.

H6949 (18-10-2026) added the **quotation-level unit**, a different unit from the sigla every
other row here counts: `pd_quotations_by_entry.tsv` (107,630 rows — `{#...#}` blocks,
quotations, siglum loci, further references, attestations per entry),
`pd_quotations_vs_pwg.tsv` (4,093 rows — the same lemmas in PD and PWG, both measured with
the same rule) and `pd_quotations_summary.json` (totals, top-20, the PWG comparison block,
input hashes). The unit itself is defined in
[reports/PD_QUOTATION_UNIT_2026-10-18.md](https://github.com/sanskrit-lexicon/csl-atlas/blob/main/reports/PD_QUOTATION_UNIT_2026-10-18.md);
the scope caveat above binds these numbers too — they are a floor, not a description.

H7458/C2 (30-10-2026, [PR #666](https://github.com/sanskrit-lexicon/csl-atlas/pull/666))
added four committed derived layers: `pd_locus_fields.tsv` (**391,444** explicit pairs),
`pd_locus_coverage_by_entry.tsv` (**107,630** rows; **105,177 = 97.72 %** with a pair),
`pd_locus_rejections.tsv` (diagnostic classes and examples), and
`pd_locus_fields_summary.json` (protocol, metrics, input hashes and exact reconciliation of
all **28,446** non-pair markers). Regenerate all four together with
`python3.13 scripts/pd_locus_fields.py --pd <pd.txt>` and verify with `--check`; H6949/C1
artifacts stay unchanged. Report:
[PD_LOCUS_FIELDS_C2_2026-10-29.md](https://github.com/sanskrit-lexicon/csl-atlas/blob/main/reports/PD_LOCUS_FIELDS_C2_2026-10-29.md).

