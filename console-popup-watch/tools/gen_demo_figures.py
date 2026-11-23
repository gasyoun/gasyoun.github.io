#!/usr/bin/env python3
# MIT License — © 2026 Dr. Mārcis Gasūns — https://github.com/gasyoun/gasyoun.github.io
"""Generate the console-popup-watch guide figures from the committed demo feeds.

stdlib-only, deterministic (no timestamps, no randomness). Reads
console-popup-watch/demo/{before,after}.jsonl and emits seven
console-popup-watch/figures/*.svg — four feed-derived (fig-timeline, fig-jsonl-
anatomy, fig-canary, fig-ancestry; regen-diff gated) and three hand-authored
concept diagrams (fig-flash-cause, fig-protocol, fig-fix-picker; no data claims).

  python tools/gen_demo_figures.py            # (re)write figures/*.svg
  python tools/gen_demo_figures.py --check    # regen-diff; exit 1 on byte drift

Every data figure derives ONLY from the committed synthetic demo feeds
(obviously-fake paths, C:\\demo / C:\\tools probe class). No real capture
ever enters this folder (ADR-0001 · ADR-0002).
"""
import argparse
import json
import os
import sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # console-popup-watch/
DEMO = os.path.join(HERE, "demo")
FIGDIR = os.path.join(HERE, "figures")

BEFORE = os.path.join(DEMO, "before.jsonl")
AFTER = os.path.join(DEMO, "after.jsonl")

# ---------------------------------------------------------------- svg helpers

STYLE = """<style>
  :root{--fg:#1d232a;--muted:#5a6672;--line:#d8dee4;--code:#f2f5f8;--accent:#0b6bcb;--bad:#a33a1e;--good:#1e7a3f}
  @media (prefers-color-scheme:dark){:root{--fg:#e6eaee;--muted:#98a0a8;--line:#3a4046;--code:#1f2429;--accent:#5ea3e8;--bad:#e08663;--good:#5cc389}}
  text{fill:var(--fg);font-family:system-ui,'Segoe UI',Roboto,sans-serif}
  .mono{font-family:ui-monospace,Consolas,'Cascadia Mono',monospace}
  .mut{fill:var(--muted)} .acc{fill:var(--accent)} .bad{fill:var(--bad)} .good{fill:var(--good)}
  .ln{stroke:var(--line)} .accl{stroke:var(--accent)} .fgl{stroke:var(--fg)}
  .badl{stroke:var(--bad)} .goodl{stroke:var(--good)}
  .box{fill:var(--code);stroke:var(--line)}
</style>"""


def esc(s):
    return (str(s).replace("&", "&amp;").replace("<", "&lt;")
            .replace(">", "&gt;").replace('"', "&quot;"))


def svg(w, h, title, body):
    return ('<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" '
            'viewBox="0 0 %d %d" role="img" aria-label="%s">\n%s\n%s\n</svg>\n'
            % (w, h, w, h, esc(title), STYLE, body))


def text(x, y, s, cls="", size=13, anchor="start", weight=""):
    a = ' text-anchor="%s"' % anchor if anchor != "start" else ""
    wt = ' font-weight="%s"' % weight if weight else ""
    return ('<text x="%s" y="%s" class="%s" font-size="%s"%s%s>%s</text>'
            % (x, y, cls, size, a, wt, esc(s)))


def rect(x, y, w, h, cls="box", sw=1.5, extra=""):
    return ('<rect x="%s" y="%s" width="%s" height="%s" rx="7" class="%s"'
            ' stroke-width="%s"%s/>' % (x, y, w, h, cls, sw, extra))


def line(x1, y1, x2, y2, cls="accl", sw=1.6):
    return ('<line x1="%s" y1="%s" x2="%s" y2="%s" class="%s" stroke-width="%s"/>'
            % (x1, y1, x2, y2, cls, sw))


def arrow_at(x1, y1, x2, y2, cls="accl", sw=1.6):
    return ('<line x1="%s" y1="%s" x2="%s" y2="%s" class="%s" stroke-width="%s"'
            ' marker-end="url(#arr)"/>' % (x1, y1, x2, y2, cls, sw))


DEFS = ('<defs><marker id="arr" viewBox="0 0 10 10" refX="9" refY="5"'
        ' markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
        '<path d="M0,0 L10,5 L0,10 z" fill="context-stroke"/></marker></defs>')


# ------------------------------------------------------------------ feed io

def load_feed(path):
    recs = []
    with open(path, encoding="utf-8") as f:
        for i, raw in enumerate(f, 1):
            raw = raw.strip()
            if not raw:
                continue
            try:
                recs.append(json.loads(raw))
            except json.JSONDecodeError as e:
                raise SystemExit("FATAL: %s:%d is not valid JSONL: %s" % (path, i, e))
    if not recs:
        raise SystemExit("FATAL: %s is empty" % path)
    return recs


def first_of(recs, rtype):
    for r in recs:
        if r.get("type") == rtype:
            return r
    raise SystemExit('FATAL: feed has no "%s" record — regen refused' % rtype)


def all_of(recs, rtype):
    return [r for r in recs if r.get("type") == rtype]


# ---------------------------------------------------- hand-authored figures

def fig_flash_cause():
    b = DEFS
    # Lane A: parent already HAS a console
    b += text(24, 34, "A · parent already has a console", cls="acc", size=14, weight="600")
    b += rect(24, 52, 250, 64)
    b += text(40, 78, "demo-shell.exe", size=12, cls="mono")
    b += text(40, 98, "owns a console window", size=12, cls="mut")
    b += arrow_at(282, 84, 360, 84)
    b += rect(368, 52, 220, 64)
    b += text(384, 78, "console child (probe.exe)", size=12, cls="mono")
    b += text(384, 98, "inherits parent console", size=12, cls="mut")
    b += text(604, 90, "child reuses the parent's", size=12, cls="good", weight="600")
    b += text(604, 108, "console — nothing on screen", size=12, cls="good", weight="600")

    b += line(24, 150, 836, 150, cls="ln", sw=1.5)

    # Lane B: console-less parent
    b += text(24, 186, "B · parent has NO console", cls="acc", size=14, weight="600")
    b += rect(24, 204, 250, 64)
    b += text(40, 230, "GUI host / pythonw / service", size=12, cls="mono")
    b += text(40, 250, "has no console at all", size=12, cls="mut")
    b += arrow_at(282, 236, 360, 236)
    b += rect(368, 204, 220, 64)
    b += text(384, 230, "console child (probe.exe)", size=12, cls="mono")
    b += text(384, 250, "Windows allocates a console", size=12, cls="mut")
    b += arrow_at(596, 236, 674, 236, cls="badl")
    b += rect(682, 204, 150, 64, cls="", sw=1.8, extra=' stroke="var(--bad)"')
    b += text(697, 230, "visible 1-second", size=12, cls="bad", weight="600")
    b += text(697, 250, "flash on screen", size=12, cls="bad", weight="600")

    b += text(24, 302, "Every console-subsystem child gets a console — the only question is whose:",
              cls="mut", size=12)
    b += text(24, 320, "inherited (invisible) or freshly allocated (the flash the watcher records).",
              cls="mut", size=12)
    return svg(860, 336, "Why the 1-second console flash happens", b)


def fig_protocol():
    b = DEFS
    steps = [
        (24, "0 · baseline + heartbeat", "watch the live desktop;", "30-s heartbeats make a dead", "watcher visible in the log"),
        (236, "1 · A/B canary (--negctl)", "one control window visible,", "one with CREATE_NO_WINDOW: the", "verdict must read default>0, hidden==0"),
        (448, "2 · 15-min interception", "≥15 min while the estate", "works. 0 new windows = quiet;", "any window = a named lead"),
        (660, "3 · byte-match ×3", "live copy vs deploy copy vs", "repo HEAD (CRLF-normalized),", "run before and after the fix"),
    ]
    for x, t, l1, l2, l3 in steps:
        b += rect(x, 30, 176, 96)
        b += text(x + 14, 54, t, size=12.5, weight="600")
        b += text(x + 14, 76, l1, size=11, cls="mut")
        b += text(x + 14, 92, l2, size=11, cls="mut")
        b += text(x + 14, 108, l3, size=11, cls="mut")
    b += arrow_at(202, 78, 234, 78)
    b += arrow_at(414, 78, 446, 78)
    b += arrow_at(626, 78, 658, 78)

    # fork under step 1
    b += line(324, 126, 324, 148)
    b += rect(60, 148, 400, 46, cls="", sw=1.8, extra=' stroke="var(--good)"')
    b += text(76, 167, "canary 1/0 · watcher_not_blind: true", size=12, cls="good", weight="600")
    b += text(76, 184, "the watcher sees what appears — trust the quiet log", size=11, cls="mut")

    b += line(324, 194, 324, 216)
    b += rect(60, 216, 400, 46, cls="", sw=1.8, extra=' stroke="var(--bad)"')
    b += text(76, 235, "canary 0/0 → INCONCLUSIVE, never “clean”", size=12, cls="bad", weight="600")
    b += text(76, 252, "console-attached shell ate the probe: rerun under pythonw.exe,", size=11, cls="mut")

    b += text(500, 160, "…or force a brand-new console from the same shell:", size=11.5, cls="mut")
    b += text(500, 178, 'cmd /c start "" cmd /c "ping -n 4 127.0.0.1 >nul"', size=11.5, cls="mono")
    b += text(500, 196, "the new window must be caught, or the watcher is blind.", size=11.5, cls="mut")

    b += text(24, 290, "Verify after the fix with the same instruments you used before it —", cls="mut", size=12)
    return svg(860, 304, "The 15-minute verification protocol and the 0/0 fork", b)


def fig_fix_picker():
    b = DEFS
    cx = 430
    b += rect(280, 20, 300, 44)
    b += text(cx, 47, "the watcher caught a new console", size=13, anchor="middle")

    b += arrow_at(cx, 64, cx, 98)
    b += rect(280, 98, 300, 44)
    b += text(cx, 125, "who is the PARENT?", size=13, anchor="middle", weight="600")

    # branch 1: console-attached parent
    b += arrow_at(280, 120, 190, 168, cls="fgl")
    b += text(214, 152, "console-attached", cls="mut", size=11, anchor="end")
    b += rect(60, 168, 280, 44)
    b += text(76, 186, "child inherits its console —", size=12, cls="mut")
    b += text(76, 204, "a flash from here is rare; audit anyway", size=12, cls="mut")

    # branch 2: console-less parent (the common case)
    b += arrow_at(580, 120, 670, 168, cls="fgl")
    b += text(664, 152, "console-less host", cls="mut", size=11)
    b += rect(470, 168, 350, 44)
    b += text(486, 186, "hide it at the call site, every call site:", size=12)
    b += text(486, 204, "CREATE_NO_WINDOW / windowsHide: true", size=12, cls="mono")

    # follow-up: patch available?
    b += arrow_at(cx, 142, cx, 244)
    b += rect(280, 244, 300, 44)
    b += text(cx, 271, "can you patch that code?", size=13, anchor="middle", weight="600")

    b += arrow_at(280, 266, 190, 314, cls="fgl")
    b += rect(40, 314, 300, 44)
    b += text(56, 332, "yes → apply the flag, audit with", size=12)
    b += text(56, 349, 'grep -rEn "spawn(Sync)?\\(|execFile\\(|exec\\(" .', size=10.5, cls="mono")

    b += arrow_at(580, 266, 670, 314, cls="fgl")
    b += rect(520, 314, 300, 44)
    b += text(536, 332, "no (third-party) → fix upstream,", size=12)
    b += text(536, 349, "or hide with a VBS shim / Start-Process -WindowStyle Hidden", size=10.5, cls="mut")

    # terminal node
    b += arrow_at(430, 358, 430, 384)
    b += rect(230, 384, 400, 44, cls="", sw=1.8, extra=' stroke="var(--good)"')
    b += text(cx, 402, "re-run the canary + 15-min watch", size=12.5, cls="good", weight="600", anchor="middle")
    b += text(cx, 419, "the same instruments prove the fix did not revert", size=11, cls="mut", anchor="middle")

    return svg(860, 448, "Pick the fix move by parent type", b)


# ----------------------------------------------------- data figures (feeds)

def fig_timeline(before, after):
    W, H = 860, 300
    left, right = 96, 808
    span = right - left
    b = DEFS

    wins_b = all_of(before, "new_visible_window")
    hbs_b = all_of(before, "heartbeat")
    dur_b = float(first_of(before, "stop")["elapsed_s"])
    wins_a = all_of(after, "new_visible_window")
    hbs_a = all_of(after, "heartbeat")
    dur_a = float(first_of(after, "stop")["elapsed_s"])

    for (y, label, feed_dur, wins, hbs) in [
        (96, "before — demo 23-min watch (synthetic feed)", dur_b, wins_b, hbs_b),
        (206, "after — demo 15-min watch (synthetic feed)", dur_a, wins_a, hbs_a),
    ]:
        b += text(24, y - 22, label, size=13, weight="600")
        b += line(left, y, right, y, cls="fgl", sw=2)
        b += ('<path d="M%d,%d L%d,%d L%d,%d z" fill="var(--fg)"/>'
              % (right - 11, y - 5, right, y, right - 11, y + 5))
        for r in hbs:
            x = left + span * float(r["elapsed_s"]) / feed_dur
            b += ('<circle cx="%.1f" cy="%d" r="1.8" fill="var(--accent)"'
                  ' fill-opacity="0.55"/>' % (x, y + 9))
        for r in wins:
            x = left + span * float(r["elapsed_s"]) / feed_dur
            b += line("%s" % ("%.1f" % x), y - 13, "%.1f" % float(x), y + 13, cls="badl", sw=2.4)
    # replace the two event-tick lines rendered via line() above: they already are

    # legend
    b += line(96, 140, 116, 140, cls="badl", sw=2.4)
    b += text(122, 144, "new visible window — the 1-second console flash", size=11.5, cls="mut")
    dots = "".join('<circle cx="%d" cy="140" r="1.8" fill="var(--accent)" fill-opacity="0.55"/>'
                   % (268 + i * 7) for i in range(3))
    b += dots
    b += text(296, 144, "30-s heartbeat — silence is auditable", size=11.5, cls="mut")

    # callouts
    b += rect(96, 232, 340, 48, cls="", sw=1.8, extra=' stroke="var(--bad)"')
    b += text(112, 252, "%d new-window events in 23 min" % len(wins_b),
              size=12.5, cls="bad", weight="600")
    b += text(112, 270, "a waterfall of tooling-spawned consoles", size=11, cls="mut")
    b += rect(470, 232, 338, 48, cls="", sw=1.8, extra=' stroke="var(--good)"')
    b += text(486, 252, "%d new-window events in 15 min" % len(wins_a),
              size=12.5, cls="good", weight="600")
    b += text(486, 270, "%d heartbeats prove the watcher was alive" % len(hbs_a),
              size=11, cls="mut")
    return svg(W, H, "Before/after the fix: window events vs heartbeats", b)


def fig_jsonl_anatomy(rec, feed_name):
    W = 860
    raw = json.dumps(rec, ensure_ascii=False)
    char_w = 7.2
    wrap = 104
    rows = [raw[i:i + wrap] for i in range(0, len(raw), wrap)]
    mono_y0 = 64
    H = mono_y0 + len(rows) * 15 - 3 + 96
    b = DEFS
    b += text(24, 26, "one receipts line, dissected", size=14, weight="600")
    b += text(W - 24, 26, "feed: %s" % feed_name, size=11, cls="mut", anchor="end")

    for i, rw in enumerate(rows):
        b += ('<text x="24" y="%d" class="mono" font-size="11.5"'
              ' fill="var(--fg)">%s</text>' % (mono_y0 + i * 15, esc(rw)))

    annos = [
        ("type", "badl", "bad", "type — what happened: a new visible top-level window"),
        ("elapsed_s", "accl", "acc", "elapsed_s — when, inside the watch window"),
        ("ancestry", "goodl", "good", "ancestry — parent chain to the launcher, with PEB cmdlines"),
    ]
    ann_y = mono_y0 + len(rows) * 15 + 18
    for dy_idx, (field, lcls, tcls, label) in enumerate(annos):
        idx = raw.find('"%s"' % field)
        row_i = idx // wrap
        x = 24 + (idx % wrap) * char_w
        y = mono_y0 + row_i * 15
        ly = ann_y + dy_idx * 20
        b += ('<line x1="%s" y1="%s" x2="%s" y2="%s" class="%s" stroke-width="1.3"'
              ' stroke-dasharray="3 3"/>' % (x, y + 4, x, ly - 7, lcls))
        b += text(x + 7, ly, label, size=11.5, cls=tcls)
    return svg(W, H, "The JSONL receipt, field by field", b)


def fig_canary(after):
    W, H = 860, 240
    b = DEFS
    v = first_of(after, "negative_control_verdict")
    d = int(v["default_spawn_windows"])
    g = int(v["create_no_window_windows"])
    verdict = bool(v.get("watcher_not_blind"))

    b += text(24, 30, "A/B canary verdict — is the watcher blind?", size=14, weight="600")

    b += text(24, 84, "default spawn (no flags)", size=12, cls="mut")
    bar = max(6, 120 * min(d, 3))
    b += rect(24, 98, bar, 30, cls="", sw=1.6,
              extra=' stroke="var(--bad)" fill="var(--bad)" fill-opacity="0.25"')
    b += text(48 + bar, 118, "%d window caught" % d, size=12, cls="bad", weight="600")

    b += text(24, 164, "CREATE_NO_WINDOW spawn", size=12, cls="mut")
    b += rect(24, 178, max(6, 120 * min(g, 3)), 30, cls="", sw=1.6,
              extra=' stroke="var(--line)"')
    b += text(48 + max(6, 120 * min(g, 3)) + 14, 198,
              "%d windows — the hidden spawn stayed hidden" % g, size=12, cls="mut")

    b += rect(500, 98, 336, 56, cls="", sw=1.8,
              extra=' stroke="var(--good)"' if verdict else ' stroke="var(--bad)"')
    vb = "watcher_not_blind: %s" % ("true" if verdict else "false")
    b += text(516, 122, vb, size=13, cls="good" if verdict else "bad", weight="600")
    b += text(516, 142, "a new console appears ⇒ the watcher sees it", size=11.5, cls="mut")

    b += text(24, 232, "Same session, same window station: the canary must reproduce BOTH outcomes "
                       "(visible and hidden) before a quiet log means anything.",
              size=11.5, cls="mut")
    return svg(W, H, "A/B canary verdict bars", b)


def fig_ancestry(rec):
    W, H = 860, 300
    b = DEFS
    chain = list(rec["ancestry"])
    b += text(24, 28, "empty PEB cmdline? attribute via ancestry — the chain still resolves",
              size=13, weight="600")
    b += text(24, 48, "window caught: %s  (pid %s)" % (rec["title"], rec["pid"]),
              size=11.5, cls="mut")

    y0, dy, box_w = 72, 56, 620
    for i, a in enumerate(chain):
        y = y0 + i * dy
        is_last = (i == len(chain) - 1)
        b += rect(40, y, box_w, 44)
        cmd = a.get("cmdline_peb") or "(empty PEB cmdline — broker/higher-integrity parent)"
        if len(cmd) > 66:
            cmd = cmd[:63] + "…"
        b += ('<text x="56" y="%s" class="mono" font-size="12.5" font-weight="600"'
              ' fill="var(--fg)">%s</text>' % (y + 19, esc("pid %s · %s" % (a["pid"], a["process"]))))
        b += text(56, y + 36, cmd, size=11, cls="mut")
        if not is_last:
            nxt = chain[i + 1]
            b += ('<line x1="120" y1="%s" x2="120" y2="%s" class="accl" stroke-width="1.6"'
                  ' marker-end="url(#arr)"/>' % (y + 44, y + dy))
            b += text(134, y + dy - 12, "parent pid %s" % nxt["pid"], size=10.5, cls="mut")

    b += text(700, y0 + 20, "walk up the", size=11.5, cls="mut")
    b += text(700, y0 + 36, "chain until the", size=11.5, cls="mut")
    b += text(700, y0 + 52, "launcher that", size=11.5, cls="mut")
    b += text(700, y0 + 68, "owns the spawn", size=11.5, cls="mut")
    return svg(W, H, "Ancestry: who really spawned the window", b)


# ---------------------------------------------------------------- regen core

def build_all():
    before = load_feed(BEFORE)
    after = load_feed(AFTER)
    ev = first_of(before, "new_visible_window")
    return {
        "fig-flash-cause.svg": fig_flash_cause(),
        "fig-protocol.svg": fig_protocol(),
        "fig-fix-picker.svg": fig_fix_picker(),
        "fig-timeline.svg": fig_timeline(before, after),
        "fig-jsonl-anatomy.svg": fig_jsonl_anatomy(ev, "demo/before.jsonl"),
        "fig-canary.svg": fig_canary(after),
        "fig-ancestry.svg": fig_ancestry(ev),
    }


def regen(outdir=FIGDIR):
    figs = build_all()
    os.makedirs(outdir, exist_ok=True)
    for name, data in sorted(figs.items()):
        with open(os.path.join(outdir, name), "w", encoding="utf-8", newline="\n") as f:
            f.write(data)
    return figs


def check():
    figs = build_all()
    bad = []
    for name, data in sorted(figs.items()):
        path = os.path.join(FIGDIR, name)
        if not os.path.exists(path):
            bad.append("  missing: figures/%s" % name)
            continue
        with open(path, "rb") as f:
            cur = f.read()
        want = data.encode("utf-8")
        if cur != want:
            bad.append("  drifted: figures/%s (%d bytes off)"
                       % (name, abs(len(cur) - len(want))))
    if bad:
        print("FAIL gen_demo_figures --check: figures drifted from the feeds:")
        print("\n".join(bad))
        print("regenerate: python tools/gen_demo_figures.py ; re-run --check")
        return 1
    print("OK --check: %d figures byte-identical to the demo feeds" % len(figs))
    return 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true",
                    help="regen-diff: exit 1 if any figure is not byte-identical")
    a = ap.parse_args()
    if a.check:
        sys.exit(check())
    figs = regen()
    print("wrote %d figures to %s:" % (len(figs), os.path.relpath(FIGDIR)))
    for name in sorted(figs):
        print("  figures/%s" % name)


if __name__ == "__main__":
    main()
