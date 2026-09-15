# AGENTS.md — gasyoun.github.io

_Created: 13-09-2026 · Last updated: 15-09-2026_

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
- Census: tracked by [module-spread census v2](https://github.com/gasyoun/Uprava/blob/main/data/module_spread_census_v2.json)
  (`mcp_config` marker, H4525).

## Memory store

This repo keeps a committed memory store at [`.claude/projects/gasyoun.github.io/memory/`](https://github.com/gasyoun/gasyoun.github.io/tree/master/.claude/projects/gasyoun.github.io/memory) per the org Memory-routing rule ([`/danger-memory`](https://github.com/gasyoun/claude-config/blob/main/commands/danger-memory.md)) — write dangerous/durable facts there and index each in its `MEMORY.md` (H4547).

_Dr. Mārcis Gasūns_
