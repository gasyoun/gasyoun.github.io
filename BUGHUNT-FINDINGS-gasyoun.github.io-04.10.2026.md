_Created: 04-10-2026 · Last updated: 04-10-2026_

# BUGHUNT-FINDINGS — gasyoun.github.io — 04.10.2026

Nightly one-repo bug hunt (MG ruling 26-09-2026), repo `gasyoun.github.io`.
The 03:00 launchd run completed PHASE 1 (static hunt + live verification) and
died on a provider timeout mid-PHASE-2 (report never written — provider
response headers timed out after 60000 ms at 03:12). This report was recovered
from the stranded night log and re-verified live the same day; landing done as
a day-mode pass. Scope: repo CODE surface — `scripts/` (incl. `karta/`,
`campus/`, `infographics50/`), `javascripts/`, `.github/workflows/`, root
config — plus a secret sweep and the repo's own gates. Hunt tier: read-only
static + live probes; model GLM 5.3 Flash (zai-coding-plan/glm-5.3-flash).

Links below are frozen at the verification-time commit `7b5fc9dbaf50bdbae73b27f98490c29ce35977cc`
(origin/master tip; between the night tip `192bbe4` and it only hourly
handoff-status bot refreshes landed — zero code deltas, all findings re-verified
at the new tip).

## Elapsed

Night run 19 min (PHASE 1, killed by provider timeout) + same-day completion
pass (re-verification + report + GTD row), 04-10-2026.

## Ranked findings

| # | Sev | Finding | Where |
|---|-----|---------|-------|
| H1 | HIGH | Payroll salary sheets (авг+сен 2026 ведомости) are public twice over: the live Pages URL answers 200 AND both files sit in the public repo, where robots.txt / noindex do not apply; a site-internal link leads to the dir from a published vote sheet | [payroll/vedomost-aug-sep-2026.html](https://github.com/gasyoun/gasyoun.github.io/blob/7b5fc9dbaf50bdbae73b27f98490c29ce35977cc/payroll/vedomost-aug-sep-2026.html), [-detail.html](https://github.com/gasyoun/gasyoun.github.io/blob/7b5fc9dbaf50bdbae73b27f98490c29ce35977cc/payroll/vedomost-aug-sep-2026-detail.html) |
| M1 | MEDIUM | karta coverage gate is RED: 4 on-disk content items are not mapped in `karta_data.py` — `handoff-status/`, `payroll/`, `runbook-h3348-artem-root-session-2026-10-01.html`, `telegram-artem-h3348-2026-10-01.html` | [scripts/karta/gen_karta_index.py](https://github.com/gasyoun/gasyoun.github.io/blob/7b5fc9dbaf50bdbae73b27f98490c29ce35977cc/scripts/karta/gen_karta_index.py) `--check` vs [scripts/karta/karta_data.py](https://github.com/gasyoun/gasyoun.github.io/blob/7b5fc9dbaf50bdbae73b27f98490c29ce35977cc/scripts/karta/karta_data.py) |
| M2 | MEDIUM | Infographics index drifted from disk: 2 published dirs unlisted in `index.html` (`klammer-kutumbini-2026-09-06`, `paradigm-a-stems-2026-09-06`); `gen_infographics_index.py --check` says DRIFTED | [scripts/infographics50/gen_infographics_index.py](https://github.com/gasyoun/gasyoun.github.io/blob/7b5fc9dbaf50bdbae73b27f98490c29ce35977cc/scripts/infographics50/gen_infographics_index.py), [scripts/check.mjs](https://github.com/gasyoun/gasyoun.github.io/blob/7b5fc9dbaf50bdbae73b27f98490c29ce35977cc/scripts/check.mjs) |
| M3 | MEDIUM (latent) | `render_slugs.mjs` resolves the repo root from `process.cwd()` instead of its own location (`path.dirname("")` is `"."`), so it only works when run from the repo root; sibling `render.mjs` resolves from `import.meta.url` and is cwd-proof | [scripts/render_slugs.mjs:8](https://github.com/gasyoun/gasyoun.github.io/blob/7b5fc9dbaf50bdbae73b27f98490c29ce35977cc/scripts/render_slugs.mjs#L8) vs [scripts/render.mjs:8](https://github.com/gasyoun/gasyoun.github.io/blob/7b5fc9dbaf50bdbae73b27f98490c29ce35977cc/scripts/render.mjs#L8) |
| L1 | LOW | Two generated vote sheets (~130 KB each) sit untracked in the shared main tree — regenerable residue, invisible to git | `vote/sheets/uprava_drain_vote_weekly_21_09_26.html`, `vote/sheets/uprava_drain_vote_weekly_28_09_26.html` |

## Evidence (live, re-verified this pass)

### H1 — payroll sheets are public on the site and in the repo

- `git ls-tree master --name-only -- payroll/` → both files tracked on the
  public default branch; `curl -s -o /dev/null -w "%{http_code}"
  https://gasyoun.github.io/payroll/vedomost-aug-sep-2026.html` → **200**.
- Exposure depth, anonymised (no names/sums quoted per the integrity rule):
  summary sheet = 15 person rows (`<tr>` count), detail sheet = 11 named
  `<h2>` sections with ruble-sum patterns present.
- Mitigations already in place and why they do not close it: `noindex, nofollow`
  meta added 29-09 (46ebb78); robots.txt blocks all crawling (intentional,
  MG 13-09 «working docs domain», efd72d0). Neither governs **github.com repo
  browsing** of the public repo. Additionally
  `vote/sheets/skill_mine_h5154_h5155.html` links into `payroll/` from the
  published site itself.
- Money/personal class → **no auto-fix** (standing fence). GTD `@DO` row
  **0O3** minted 04-10-2026 (Uprava, «Residuals registered 04-10-2026») with
  this report linked; decision (repo privacy / content move / accepted risk)
  is MG's.

### M1 — karta coverage gate RED

`python3 scripts/karta/gen_karta_index.py --check` → `coverage FAIL:` with the
4 unmapped items listed above (re-run live this pass, same output as the night
run). The gate itself works — it is the data map that is behind the disk.

### M2 — infographics index drift

- `python3 scripts/infographics50/gen_infographics_index.py --check` →
  `check: index.html DRIFTED from disk state — re-run with --emit`.
- `node scripts/check.mjs --index` → `FAIL index parity:` + the 2 unlisted
  dirs, `3 errors` (re-run live this pass).

### M3 — cwd-dependent root in render_slugs.mjs

- [render_slugs.mjs:8](https://github.com/gasyoun/gasyoun.github.io/blob/7b5fc9dbaf50bdbae73b27f98490c29ce35977cc/scripts/render_slugs.mjs#L8):
  `const root = path.resolve(path.dirname(""), process.cwd());` —
  `path.dirname("")` returns `"."`, so `root` collapses to the caller's cwd.
- [render.mjs:8](https://github.com/gasyoun/gasyoun.github.io/blob/7b5fc9dbaf50bdbae73b27f98490c29ce35977cc/scripts/render.mjs#L8):
  `const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");`
  — the correct pattern, one line away. Fix is mechanical: adopt the sibling's
  resolution (adjust the `".."` to `render_slugs.mjs`'s depth — it lives in
  `scripts/` too, so `..` is right as-is).
- Latent today (CI/docs invoke it from the root), hence MEDIUM not HIGH.

### L1 — untracked vote-sheet residue

`git status --short` → the two `uprava_drain_vote_weekly_*` sheets untracked
(~130 KB each). Generated artifacts; either commit them (if the vote hub links
them) or add to `.gitignore`.

### Clean surfaces (verified negative)

- Secret sweep negative: `git grep` for api-key/token/Bearer/AKIA/sk-/ghp-/xox
  patterns over the code surface → only benign hits (a `data-token` DOM key in
  frozen h3457 archive pages). Workflows carry `secrets.GITHUB_TOKEN` properly;
  the staleness workflow uses the public GitHub API only.
- No `os.system` / `shell=True` / `eval(` / `exec(` in the Python surface;
  `node --check` on all three .mjs and `py_compile` on the seven hunted
  generators pass.
- `main.js` is a stub; campus generators (`campus_build.py`, `mastery_build.py`,
  `mastery_map_build.py`, `paradigm_grid_build.py`) read clean.

## Verified-intentional (not findings)

- **robots.txt full-domain block** (`Allow: /$` + `Disallow: /`) — MG ruling
  13-09-2026, «working docs domain» (efd72d0). It sharpens H1 only because
  repo browsing bypasses it.
- **Sheet staleness 107/116 «stale»** — by design, non-blocking per H3848;
  the live run of `check_sheet_staleness.py` behaves as documented.
- **params.json** — GitHub Pages auto-generator boilerplate kept deliberately
  (karta K-note, 27-09 CHANGELOG entry).

## Disposition

Per MG ruling 26-09-2026: HIGH code bugs would be auto-fixed in-run — **none
found**; the single HIGH is money/personal-class (H1) → GTD `@DO` 0O3, no
self-fix. M1/M2 are two RED repo gates with mechanical fixes (`--emit` for the
infographics index; 4 karta rows — one of which is `payroll/`, so it should be
decided together with H1); M3 is a one-line cwd fix; L1 is a two-file
tidy-up. Day mode: say the word and the MEDIUMs land the same way.

_Гасунс_
