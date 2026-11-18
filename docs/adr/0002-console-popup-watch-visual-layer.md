# ADR 0002 — Visual layer for the console-popup-watch guide (7 figures, demo-feed generation, report.html)

_Created: 18-11-2026 · Status: accepted · Decided by: MG (grill-with-docs rounds 18-11-2026, two interactive frontiers), transcribed by GLM 5.3 (glm-5.3)_

## Context

The guide published today ([#113](https://github.com/gasyoun/gasyoun.github.io/pull/113), ADR 0001) is text-only: the core mental model (console-subsystem child spawned from a console-less parent ⇒ visible 1-second flash) is four dense paragraphs; the "silence must be auditable via 30-s heartbeats" promise is never shown; and the JSONL receipt the whole method hinges on is never displayed visually. A grill-with-docs interview (two rounds, whole frontier per round) settled what the visual layer adds and under what honesty constraints. ADR 0001 bars estate-private data from the public folder, so every data-shaped figure needs a legal, honest data source.

## Decision

1. **Seven static figures**, embedded in the guide's own palette via `<img>`: (a) flash-cause two-lane diagram — parent *with* console → child inherits (nothing visible) vs console-less parent → new console allocated (hand-authored, conceptual); (b) before/after timeline strip with 30-s heartbeat ticks and the already-public callout numbers 10-in-23-min → 0-in-15-min (generated from the demo feed); (c) JSONL line anatomy dissected from one demo event (generated); (d) verification-protocol timeline with the 0/0-canary-inconclusive fork (hand-authored); (e) canary A/B verdict bars (generated); (f) ancestry tree from a demo event's parent chain — attribute via ancestry when the PEB cmdline is empty (generated); (g) fix-picker static SVG flowchart — which fix move by parent type/language (hand-authored).
2. **Data honesty** — two synthetic demo feeds committed in the folder (`demo/before.jsonl`, `demo/after.jsonl`; the after-feed opens with the `--negctl` canary records, realistic usage order; obviously-fake paths only). Every data figure carries a trust block ("demo data, not a real capture") plus a feed link. The real outcome numbers may appear only as callouts — they are already public in the guide text; raw real feeds never cross into the folder.
3. **Mechanics (viz-page discipline)** — a committed stdlib generator (`tools/gen_demo_figures.py`) reads the feeds and emits `figures/*.svg`; a regen-diff `--check` keeps figures byte-identical to the feeds; `index.html` stays hand-authored. No hand-drawn figure pretends to be data.
4. **report.html (PR2)** — a separate, self-contained client-side page: drag/paste or Load-demo; timeline strip, flash table (utc, title, class, pid, ancestry), heartbeat coverage bar, canary verdict panel (`default_spawn_windows` / `create_no_window_windows` / `watcher_not_blind`), blind-watch warnings (0/0 canary = inconclusive, never clean; missing heartbeats); accepts both plain watch and `--negctl` JSONL in one parse; dark mode; linked from the guide's Download section. Extras examined and rejected this round: per-minute histogram, copy-verdict block, hover tooltips.
5. **Fix-picker shape** — static in-guide SVG flowchart. The house interactive decision-tree landing was rejected: a ~8–12-node tree gains little from interactivity and would split the method across two landings.
6. **Dark mode** — `prefers-color-scheme` adopted for `index.html` + `report.html`; figures drawn against `currentColor`/CSS vars so they theme for free.
7. **Delivery** — phased: PR1 = feeds + generator + 7 figures + index embeds + dark mode; PR2 = report.html + Download-section link. Execution handoffs: [H8457](https://github.com/gasyoun/Uprava/blob/main/handoffs/H8457-GLM_gasyoun.github.io_console-popup-viz-figures_18.11.26.md) (PR1), [H8458](https://github.com/gasyoun/Uprava/blob/main/handoffs/H8458-GLM_gasyoun.github.io_console-popup-viz-renderer_18.11.26.md) (PR2).

## Consequences

- The folder gains its first non-text assets; page weight grows slightly (inline-styled SVGs, still zero external dependencies, no chart library — the kit's dependency-free ethos holds).
- The generator + regen-diff check make the figures a maintained artifact: future feed edits re-render, and a drifted figure fails the check instead of silently lying.
- The demo feeds double as the renderer's Load-demo payload and as the shared fixture keeping figures and renderer in agreement.
- `report.html` becomes the kit's first client-side tool; it must stay MIT, dependency-free, and honest about verdicts (a 0/0 canary is inconclusive, never clean).

## Alternatives rejected

- **Interactive decision-tree landing** (house decision-tree skill, `decision-trees/*.html`) — splits the method across two landings, adds a generator dependency outside the folder, negligible gain at 8–12 nodes.
- **Inline-SVG semi-generated index.html** — turns the hand-authored guide into a semi-generated page; every regen needs a manual re-inline step, a drift risk the smoke check can only warn about.
- **Lookalike feed generated from a real capture** — realistic shape but adds a generation step and still needs a sanitize review; hand-crafted synthetic is deterministic and obviously-demo.
- **Redacted real capture** — redaction strips exactly the fields that teach (cmdline, ancestry); worst of both worlds.
- **Renderer embedded in index.html** — bloats the 12.7 KB guide with app code and mixes documentation with application.
- **One big PR** — the renderer would ship before anyone sanity-checked the figures it must agree with.

_Dr. Mārcis Gasūns_
