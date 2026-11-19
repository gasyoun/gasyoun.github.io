# AGENTS.md — gasyoun.github.io

_Created: 13-09-2026 · Last updated: 19-11-2026_

## Tool manifest

- Purpose: public GitHub Pages repo, root-served from `master`
  (https://gasyoun.github.io) — vote hub, HTML dashboards, published course
  and research deliverables; ALL org HTML links point here, never blob URLs.
- Harnesses: Claude Code / Codex / OpenCode / Grok (this AGENTS.md) — org
  default all four.
- CI: [dependabot-auto-merge.yml](https://github.com/gasyoun/gasyoun.github.io/blob/master/.github/workflows/dependabot-auto-merge.yml) +
  [sheet-staleness.yml](https://github.com/gasyoun/gasyoun.github.io/blob/master/.github/workflows/sheet-staleness.yml);
  no build system — static files only.
- Repo-level MCP: none carried (no `.mcp.json`).
- Landing route: PR + auto-merge (gasyoun-owned, H4086 allowlist v2).
- Generated pages: `campus/` + `mastery/` render from
  [scripts/campus/](https://github.com/gasyoun/gasyoun.github.io/tree/master/scripts/campus)
  generators — edit generator/data, never the HTML; canonical mastery page =
  `mastery_map_build.py`, stats variant = `mastery_build.py`
  ([dual-run ledger](https://github.com/gasyoun/gasyoun.github.io/blob/master/scripts/campus/MASTERY_DUALRUN_2026-09-14.md)).
- Census: tracked by [module-spread census v2](https://github.com/gasyoun/Uprava/blob/main/data/module_spread_census_v2.json)
  (`mcp_config` marker, H4525).

## Branches (truth since 19-11-2026 — GTD YKR ruling A)

- `master` is the ONLY truth: default branch AND the GitHub Pages source. The
  hourly refresh lanes (cpu-page H7869, public handoff-status, estate-site)
  commit and push it directly; the site deploys from it.
- `main` was a decoy PR-intake branch (squash-diverged since 16-08, never
  published); retired 19-11-2026 — real content converged onto `master`, ref
  preserved as `archive/main-diverged-19-11`. Do NOT recreate it; do NOT
  hand-pick a non-default base when opening PRs — land on `master`.
- A push-loop/rebase for this repo targets `origin/master` (the repo's actual
  default), never a hardcoded `main`; the retired main history is a
  1450-pick rebase wall by construction.

## Memory store

This repo keeps a committed memory store at [`.claude/projects/gasyoun.github.io/memory/`](https://github.com/gasyoun/gasyoun.github.io/tree/master/.claude/projects/gasyoun.github.io/memory) per the org Memory-routing rule ([`/danger-memory`](https://github.com/gasyoun/claude-config/blob/main/commands/danger-memory.md)) — write dangerous/durable facts there and index each in its `MEMORY.md` (H4547).

_Dr. Mārcis Gasūns_
