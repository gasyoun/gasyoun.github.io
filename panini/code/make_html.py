#!/usr/bin/env python3
"""Render the self-contained, printable HTML study deck from core_terms.json + report.json."""
from __future__ import annotations

import html
import json
import os
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

HERE = os.path.dirname(os.path.abspath(__file__))
rep = json.load(open(os.path.join(HERE, "report.json"), encoding="utf-8"))
core = json.load(open(os.path.join(HERE, "core_terms.json"), encoding="utf-8"))
terms = core["terms"]
batches = core["batches"]
DSG = "https://samskrtam.ru/sanskrit-lexicon/dsg/"

e = lambda s: html.escape(str(s))


def bars(items, total, cutoff=12, cap=None):
    """items: list of (label, value, sublabel)"""
    mx = cap or max(v for _, v, _ in items[:cutoff]) or 1
    out = []
    for lab, val, sub in items[:cutoff]:
        pct = 100.0 * val / mx
        out.append(
            '<div class="bar-row"><div class="bar-lab">%s</div>'
            '<div class="bar-track"><div class="bar-fill" style="width:%.1f%%"></div></div>'
            '<div class="bar-val">%s</div><div class="bar-sub">%s</div></div>'
            % (e(lab), pct, e(val), e(sub)))
    return "".join(out)


pc = rep["top_pc"][:12]
an = rep["top_an"][:12]
ad = rep["top_ad"][:12]
written = bars([(w, c, "%.1f%% of sūtras" % (100.0 * c / 3983)) for w, c in pc], 3983)
inherited = bars([(w, c, "sūtras inherit it") for w, c in an], 3983)
scope = bars([(w, c, "%.1f%% of sūtras" % (100.0 * c / 3983)) for w, c in ad], 3983)

comp = rep["dsg_composition_first_definition_heuristic"]
comp_rows = []
palette = ["#4a447f", "#c2703a", "#7d8f69", "#9a7aa5", "#b8a05a", "#6f8b9b", "#a56b6b"]
for i, (k, v) in enumerate(sorted(comp.items(), key=lambda x: -x[1])):
    comp_rows.append(
        '<div class="bar-row"><div class="bar-lab">%s</div>'
        '<div class="bar-track"><div class="bar-fill" style="width:%.1f%%;background:%s"></div></div>'
        '<div class="bar-val">%d</div><div class="bar-sub">%.1f%%</div></div>'
        % (e(k), 100.0 * v / 2370, palette[i % len(palette)], v, 100.0 * v / 4383))

# coverage curve
import csv
rows = list(csv.DictReader(open(os.path.join(HERE, "panini_word_forms.tsv"), encoding="utf-8"), delimiter="\t"))
tot = sum(int(r["combined"]) for r in rows)
marks, cum, pts = [0, 10, 20, 30, 50, 75, 100, 150, 200, 300, 500, 1000], 0, []
for i, r in enumerate(rows, 1):
    cum += int(r["combined"])
    if i in marks:
        pts.append((i, 100.0 * cum / tot))
maxn = max(n for n, _ in pts)
xy = " ".join("%.1f,%.1f" % (20 + 520 * (n / maxn) ** 0.35, 130 - 110 * p / 100) for n, p in pts)
curve_labels = "".join(
    '<text x="%.1f" y="%.1f" class="pt">%s</text>' %
    (20 + 520 * (n / maxn) ** 0.35, 130 - 110 * p / 100 - 6, "%d" % n)
    for n, p in pts if n in (0, 20, 50, 100, 300, 1000))
cover = (
    '<svg viewBox="0 0 580 155" class="curve" role="img" aria-label="cumulative coverage curve">'
    '<line x1="20" y1="130" x2="545" y2="130" stroke="#d8d3c8"/>'
    '<line x1="20" y1="20" x2="20" y2="130" stroke="#d8d3c8"/>'
    '<polyline points="%s" fill="none" stroke="#4a447f" stroke-width="2.5"/>'
    '%s'
    '<text x="20" y="148" class="ax">1 form</text>'
    '<text x="470" y="148" class="ax">1,000 forms</text>'
    '<text x="24" y="18" class="ax">%% of all required-term readings</text>'
    '</svg>' % (xy, curve_labels))
cover_pts = " · ".join("top %d → %.0f%%" % (n, p) for n, p in pts if n in (10, 50, 100, 300, 1000))

# batches
bhtml = []
for b in sorted(batches, key=int):
    xs = sorted([t for t in terms if t["batch"] == int(b)], key=lambda t: -t["total"])
    mx = max(t["total"] for t in xs) or 1
    trs = []
    for t in xs:
        dl = ('<a class="dsg" href="%s" target="_blank" rel="noopener" title="Open the DSG entry">DSG ↗</a>'
              % e(t["dsg_url"])) if t["dsg_url"] else '<span class="nodsg">—</span>'
        cnt = ('<div class="minibar"><i style="width:%.1f%%"></i></div>'
               '<span class="ct">%d</span>' % (100.0 * t["total"] / mx, t["total"]))
        trs.append(
            '<tr><td class="deva">%s</td><td class="iast">%s</td><td class="gloss">%s</td>'
            '<td class="sutra">%s</td><td class="count">%s</td><td class="link">%s</td></tr>'
            % (e(t["deva"]), e(t["iast"]), e(t["gloss"]), e(t["sutra"]), cnt, dl))
    bhtml.append(
        '<section class="batch" id="b%s"><div class="bhead"><div class="bnum">B%s</div>'
        '<div><h3>%s</h3><p class="bnote">%s</p></div>'
        '<div class="bcount">%d terms</div></div>'
        '<table class="terms"><thead><tr><th>Devanāgarī</th><th>IAST</th><th>Meaning</th>'
        '<th>Defined at</th><th>Reading pressure</th><th>Entry</th></tr></thead>'
        '<tbody>%s</tbody></table></section>' %
        (b, b, e(batches[b]["title"]), e(batches[b]["note"]), len(xs), "".join(trs)))

TPL = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
title
<style>
:root{
 --bg:#faf8f4; --card:#fff; --ink:#24222a; --muted:#6c6872; --line:#e5e0d6;
 --accent:#4a447f; --accent2:#c2703a; --soft:#f3f0ea;
}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);
 font:15px/1.55 system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;}
.wrap{max-width:1080px;margin:0 auto;padding:0 28px 80px}
header{padding:52px 0 30px;border-bottom:2px solid var(--ink)}
h1{font-size:34px;line-height:1.18;margin:0 0 10px;letter-spacing:-.02em}
.sub{color:var(--muted);font-size:16px;max-width:780px;margin:0}
.kicker{text-transform:uppercase;letter-spacing:.16em;font-size:11px;color:var(--accent2);font-weight:700;margin-bottom:14px}
.stats{display:flex;flex-wrap:wrap;gap:0;margin:26px 0 0;border:1px solid var(--line);background:var(--card)}
.stat{flex:1 1 150px;padding:14px 18px;border-right:1px solid var(--line)}
.stat:last-child{border-right:0}
.stat b{display:block;font-size:25px;line-height:1.2;color:var(--accent)}
.stat span{font-size:11px;text-transform:uppercase;letter-spacing:.08em;color:var(--muted)}
h2{font-size:23px;margin:52px 0 6px;letter-spacing:-.01em}
h2 .n{color:var(--accent2);font-size:14px;margin-right:10px;font-variant-numeric:tabular-nums}
.lede{color:var(--muted);max-width:820px;margin:0 0 22px}
.card{background:var(--card);border:1px solid var(--line);padding:22px 24px;margin-bottom:16px}
.col3{display:grid;grid-template-columns:repeat(3,1fr);gap:14px}
.col3 .card{margin:0}
.card h4{margin:0 0 4px;font-size:15px}
.card .hint{font-size:12px;color:var(--muted);margin:0 0 16px;min-height:32px}
.bar-row{display:grid;grid-template-columns:minmax(76px,1fr) 1.15fr 38px 84px;gap:8px;align-items:center;margin:5px 0;font-size:12px}
.bar-lab{font-family:"Nirmala UI","Noto Sans Devanagari","Mangal",system-ui,sans-serif;font-size:13px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.bar-track{background:var(--soft);height:9px;border-radius:5px;overflow:hidden}
.bar-fill{height:100%;background:var(--accent);border-radius:5px}
.bar-val{text-align:right;font-variant-numeric:tabular-nums;font-weight:700}
.bar-sub{font-size:10px;color:var(--muted);white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.callout{background:#f2eee7;border-left:4px solid var(--accent2);padding:16px 20px;margin:20px 0;font-size:14px}
.callout b{color:var(--accent2)}
.method{display:grid;grid-template-columns:repeat(2,1fr);gap:12px;counter-reset:m}
.method .m{background:var(--card);border:1px solid var(--line);padding:16px 18px;position:relative;counter-increment:m}
.method .m:before{content:counter(m,decimal-leading-zero);position:absolute;top:14px;right:16px;font-size:22px;color:#ded8cb;font-weight:800}
.method h4{margin:0 0 6px;font-size:14px;padding-right:36px}
.method p{margin:0;font-size:13px;color:var(--muted)}
.method code{background:var(--soft);padding:1px 4px;font-size:11px;color:var(--accent)}
.curve{width:100%;height:auto;max-width:580px;display:block;margin:6px auto 0}
.curve .ax{fill:#8b867e;font-size:10px}
.curve .pt{fill:#4a447f;font-size:9px;font-weight:700;text-anchor:middle}
.curvepts{font-size:12px;color:var(--muted);text-align:center;margin-top:2px}
nav.mini{position:sticky;top:0;background:rgba(250,248,244,.96);backdrop-filter:blur(6px);z-index:5;padding:10px 0;border-bottom:1px solid var(--line);margin:0 0 20px;display:flex;gap:6px;flex-wrap:wrap}
nav.mini a{font-size:11px;font-weight:700;color:var(--accent);border:1px solid var(--line);background:#fff;padding:5px 10px;text-decoration:none;border-radius:20px}
nav.mini a:hover{background:var(--accent);color:#fff}
.batch{background:var(--card);border:1px solid var(--line);margin-bottom:18px;break-inside:avoid}
.bhead{display:flex;gap:16px;align-items:flex-start;padding:18px 22px;border-bottom:1px solid var(--line);background:linear-gradient(90deg,#f7f4ee,#fff)}
.bnum{font-size:22px;font-weight:800;color:var(--accent2);line-height:1;padding-top:3px;min-width:34px}
.bhead h3{margin:0 0 3px;font-size:17px}
.bnote{margin:0;font-size:12.5px;color:var(--muted);max-width:760px}
.bcount{margin-left:auto;font-size:11px;color:var(--muted);white-space:nowrap;border:1px solid var(--line);padding:3px 9px;border-radius:12px}
table.terms{width:100%;border-collapse:collapse;font-size:12.5px}
table.terms th{text-align:left;font-size:10px;text-transform:uppercase;letter-spacing:.08em;color:var(--muted);font-weight:700;padding:9px 10px;border-bottom:1px solid var(--line);background:#fcfbf8}
table.terms td{padding:7px 10px;border-bottom:1px solid #f0ede6;vertical-align:middle}
table.terms tr:last-child td{border-bottom:0}
table.terms tr:hover{background:#faf7f1}
.deva{font-family:"Nirmala UI","Noto Sans Devanagari","Mangal",system-ui,sans-serif;font-size:14px;font-weight:600;white-space:nowrap}
.iast{font-style:italic;color:var(--accent);white-space:nowrap}
.gloss{color:#403d45}
.sutra{color:var(--muted);font-size:11px;white-space:nowrap;font-variant-numeric:tabular-nums}
.count{width:120px;white-space:nowrap}
.minibar{display:inline-block;width:74px;height:6px;background:var(--soft);border-radius:3px;overflow:hidden;vertical-align:middle}
.minibar i{display:block;height:100%;background:var(--accent2)}
.ct{font-size:11px;color:var(--muted);margin-left:6px;font-variant-numeric:tabular-nums}
.dsg{font-size:10px;font-weight:700;color:var(--accent);text-decoration:none;border:1px solid var(--line);padding:3px 7px;border-radius:4px;white-space:nowrap}
.dsg:hover{background:var(--accent);color:#fff}
.nodsg{color:#c9c4ba}
footer{margin-top:56px;padding-top:22px;border-top:1px solid var(--line);font-size:11.5px;color:var(--muted)}
footer code{font-size:10px;background:var(--soft);padding:1px 4px;word-break:break-all}
.lim{background:#fff;border:1px solid var(--line);padding:16px 20px;font-size:12.5px;color:var(--muted)}
.lim b{color:var(--ink)}
.lim ul{margin:8px 0 0;padding-left:18px}
.lim li{margin:4px 0}
@media(max-width:820px){.col3,.method{grid-template-columns:1fr}.wrap{padding:0 16px 50px}h1{font-size:27px}
 table.terms .gloss{display:none}.bcount{display:none}}
@media print{body{background:#fff}.card,.batch{break-inside:avoid}nav.mini{display:none}.wrap{max-width:none}}
</style>
</head>
<body><div class="wrap">
<header>
 <div class="kicker">Vyākaraṇa · a measured core curriculum</div>
 <h1>Which Sanskrit grammar terms come first?</h1>
 <p class="sub">A frequency study of Pāṇini's Aṣṭādhyāyī read against Abhyankar's
 <i>A Dictionary of Sanskrit Grammar</i> (DSG), and a seven-batch learning order derived from it.
 Every count below is reproducible from the two pinned source snapshots.</p>
 <div class="stats">
  <div class="stat"><b>4,383</b><span>DSG headwords</span></div>
  <div class="stat"><b>3,983</b><span>Aṣṭādhyāyī sūtras</span></div>
  <div class="stat"><b>88</b><span>Pāṇinian saṃjñās</span></div>
  <div class="stat"><b>119</b><span>curated core terms</span></div>
  <div class="stat"><b>7</b><span>batches</span></div>
 </div>
</header>

<h2><span class="n">01</span>"Most frequent" has three different answers</h2>
<p class="lede">The tradition's own economy rule — <i>anuvṛtti</i> and <i>adhikāra</i> — means the
terms you need most are usually <b>not printed in the sūtra at all</b>. Counting only written tokens
gives the wrong answer. All three channels are counted as <b>document frequency</b>: the number of
distinct sūtras in which a term is required.</p>
<div class="col3">
 <div class="card"><h4>A · Most <u>written</u></h4><p class="hint">padaccheda field · 13,068 form-in-sūtra occurrences. Dominated by sūtra operators, not concepts.</p>__WRITTEN__</div>
 <div class="card"><h4>B · Most <u>inherited</u></h4><p class="hint">anuvṛtti field · 9,808 inheritances across 3,489 sūtras. Words carried forward from earlier rules.</p>__INHERITED__</div>
 <div class="card"><h4>C · Highest <u>scope</u></h4><p class="hint">adhikāra field · 14,323 governance links across 3,498 sūtras. Only 69 governing headings.</p>__SCOPE__</div>
</div>
<div class="callout"><b>The headline:</b> प्रत्यय <i>pratyaya</i> is the most frequent technical term in the
tradition — it governs <b>1,821 of 3,983 sūtras (46%)</b> while being written in only 22 of them.
Then प्रातिपदिक <i>prātipadika</i> 1,190, तद्धित <i>taddhita</i> 1,115, अङ्ग <i>aṅga</i> 613,
धातु <i>dhātu</i> 610. Conversely च <i>ca</i> is the most written word (847 sūtras = 21%) but it is
punctuation. <b>Raw string frequency and real reading pressure are almost opposites here.</b></div>

<h2><span class="n">02</span>How to count and measure</h2>
<p class="lede">A defensible pipeline. Steps 1, 2 and 4 are where naive counts go wrong — each of
these was an actual failure mode in building this study.</p>
<div class="method">
 <div class="m"><h4>Pin the corpus, record the hash</h4><p>DSG page = <code>dsg_page.html</code>, Aṣṭādhyāyī = <code>panini_data.txt</code>. Upstream drifts: the estate's graph was built against SHA <code>4d46f436…</code>; today's upstream is <code>6a22591f…</code>. Without pinning, none of the numbers reproduce.</p></div>
 <div class="m"><h4>Count terms, not word forms</h4><p>Use the tradition's own <i>padaccheda</i> (<code>pc</code>) rather than a generic tokenizer; Sanskrit sandhi merges words. <b>Never strip the Devanāgarī virāma</b> — it is structural: removing it turns प्रत्ययः into परतयय and silently corrupts every count.</p></div>
 <div class="m"><h4>Separate the three channels</h4><p><code>pc</code> explicit · <code>an</code> inherited by anuvṛtti · <code>ad</code> governing adhikāra. Report each, plus the union. Implicit readings (24,131) outnumber explicit ones (13,068) by <b>~1.8 : 1</b>.</p></div>
 <div class="m"><h4>Use document frequency, not tokens</h4><p># distinct sūtras requiring the term, not raw occurrences. One sūtra quoting a term three times is one learning event, not three. Compute a <b>coverage curve</b> over the ranked list.</p></div>
 <div class="m"><h4>Exclude function words</h4><p>Your <code>DIFFICULTY_ORDERING_RESULT.md</code> already measured this: within content vocabulary τ = 0.887, but the decisive curation move is deleting high-frequency function words. Here the top written words are exactly those operators — teach structurally, never SRS them.</p></div>
 <div class="m"><h4>Triangulate across corpora</h4><p>DSG citation density &amp; entry length (commentarial importance) · DCS lemma frequency (genre bias: epic/kāvya-heavy) · textbook first-lesson order (τ ≈ 0.05–0.10 vs frequency, ≈ 0.45–0.84 between textbooks). Agreement between channels is the confidence signal.</p></div>
 <div class="m"><h4>Validate the headword list</h4><p>DSG writes <b>सञ्ज्ञा</b> / <b>सङ्ख्या</b>, not संज्ञा / संख्या, and its digitisation has <b>no standalone वृद्धि or अङ्ग entry</b>. A naive headword-join drops two of the top ten terms. Always reconcile against the source text.</p></div>
 <div class="m"><h4>Report dispersion &amp; register</h4><p>Give per-1,000-sūtra rates, dispersion across adhyāyas, and the genre of the corpus. Zipf is steep here: the top 10 forms already cover 30% of required-term readings.</p></div>
</div>
<div class="card"><h4>Cumulative coverage — how many forms do you actually need?</h4>
__COVER__<div class="curvepts">__COVERPTS__</div>
<p class="hint" style="text-align:center;margin-top:10px">A steep head, a very long tail: 6,809 distinct forms, but ~1,000 cover four-fifths of the readings. The tail is almost entirely affix names — inventory, not vocabulary.</p></div>

<h2><span class="n">03</span>Why 4,383 entries are not a syllabus</h2>
<p class="lede">Abhyankar's own introduction says Pāṇini has <b>"about a hundred technical terms"</b>,
more than 200 suffixes, ~2,000 roots and 5,000+ special words. The Aṣṭādhyāyī dataset independently
tags <b>88 distinct saṃjñā definitions</b> — a striking match. So the fix is <b>filter by type, then
order by frequency</b>, not shrink the dictionary.</p>
<div class="card"><h4>DSG composition (first-definition heuristic, n = 4,383)</h4>
__COMP__
<p class="hint" style="margin-top:14px">≥ 42% is pure inventory: 858 affix/pratyaya names, 842 author &amp; work
names, 99 roots, 102 gaṇas, 61 substitutes, 51 augments. These belong in a <b>lookup layer</b>, not a
learning list. The longest DSG entries — <i>it</i> (4,900 chars), <i>pada</i> (3,709), <i>upasarga</i> (3,277),
<i>svara</i> (2,933), <i>dhātu</i> (2,591), <i>adhikāra</i> (2,560) — are the real conceptual core, and they
confirm this batching.</p></div>

<h2><span class="n">04</span>The batches</h2>
<p class="lede">119 terms in seven batches. <b>Batches B0–B5 (102 terms) are the learn-by-heart core</b>;
B6 is a read-once reference layer. "Reading pressure" = number of distinct sūtras in which the term is
explicit, inherited or governing, counted automatically from the Aṣṭādhyāyī. Rows are sorted by that
number within each batch; the pedagogical order is the batch order, not a raw frequency sort — because
your own sequencing study showed the grammar-topic spine, not frequency, is the scaffold.</p>
<nav class="mini">__NAV__</nav>
__BATCHES__

<h2><span class="n">05</span>What never goes into a batch</h2>
<div class="lim"><b>Lookup on demand.</b> DSG is the reference shelf, not a course. Keep it one click away
(<a href="__DSG__" target="_blank" rel="noopener">samskrtam.ru/sanskrit-lexicon/dsg/</a>) for:
<ul>
<li>the ~858 individual affix names — <i>ghañ, ṭhak, ṇvul, kta, lyuṭ, matup, ṭāp…</i> — learn the <i>system</i> (B2), look up the label when it appears;</li>
<li>augments, substitutes, roots and gaṇa lists (213 + ~2,000 + 250+ classes in the tradition);</li>
<li>the 842 author/work names, Prātiśākhya and non-Pāṇinian-school vocabulary (Kātantra, Cāndra, Jainendra, Haima);</li>
<li>Vedic accent and chanting specifics until the student actually reads Vedic text.</li>
</ul>
Suggested pacing: <b>B0 in one sitting</b> (it is a code, not a list) → one batch per 2–3 weeks, each
paired with reading ~30 real sūtras → begin B5–B6 only when the learner can parse a Siddhāntakaumudī
derivation. For SRS, drill B1–B5 only; exclude B0 and B6.</div>

<footer>
<b>Sources</b> (snapshots in this folder, SHA-256 recorded in <code>report.json</code>):<br>
DSG — K. V. Abhyankar, <i>A Dictionary of Sanskrit Grammar</i>, Gaekwad's Oriental Series 134, Baroda 1961;
web edition <a href="__DSG__" target="_blank" rel="noopener">__DSG__</a> — 4,383 entries.<br>
Aṣṭādhyāyī — <a href="https://github.com/ashtadhyayi-com/data" target="_blank" rel="noopener">ashtadhyayi-com/data</a>,
<code>sutraani/data.txt</code> — 3,983 sūtras with padaccheda / anuvṛtti / adhikāra fields.<br>
Study-order layers — <code>SanskritGrammar/data/panini_sutra_graph/study_order.tsv</code> (topological layers
over the reduced uttara-pūrva graph).<br><br>
<b>Limitations.</b> The DSG composition split is a first-definition keyword heuristic, not a manual
classification. Curated term counts for "family" rows (e.g. <i>upadhā / ṭi / anta / ādi</i>,
<i>karman</i>) aggregate several related word forms and are therefore upper bounds. Single-syllable
operators use exact word-form matching. The two corpus snapshots have different upstream revisions from
the estate's committed Pāṇini graph, so layer numbers are an ordering hint only. No learning-gain
experiment was run: this is an ordering study.<br><br>
<b>Addendum.</b> These three channels are Aṣṭādhyāyī-<i>internal</i> structural
positions, not corpora: they do not measure frequency in grammatical treatises,
and DCS was never a measured column. Both are measured separately in the
companion study <a href="external_channels.html">external_channels.html</a>
(grammar-corpus frequency, DSG salience, DCS as a register control).
</footer>
</div></body></html>
"""

nav = "".join('<a href="#b%s">B%s · %s</a>' %
              (b, b, e(batches[b]["title"].split("—")[0].split(",")[0].strip()[:26]))
              for b in sorted(batches, key=int))

out = (TPL.replace("title", "<title>Which Sanskrit grammar terms come first? — a measured core curriculum</title>")
       .replace("__WRITTEN__", written)
       .replace("__INHERITED__", inherited)
       .replace("__SCOPE__", scope)
       .replace("__COVER__", cover)
       .replace("__COVERPTS__", cover_pts)
       .replace("__COMP__", "".join(comp_rows))
       .replace("__NAV__", nav)
       .replace("__BATCHES__", "".join(bhtml))
       .replace("__DSG__", DSG))

p = os.path.join(HERE, "index.html")
open(p, "w", encoding="utf-8").write(out)
print("wrote", p, len(out), "bytes;", len(terms), "terms in", len(batches), "batches")
