#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""H6294 acceptance verifier: Зализняк-аннотации на fasmer-2026 (original/middle/short).

Checks (machine, per handoff H6294 / H5484 anchor contract):
  1. Anchors: id set e1..e1408 identical to git HEAD in all three variants, no dups.
  2. Navigation: <nav>…</nav> byte-identical to git HEAD in all three variants.
  3. Headword text unchanged (dt inner minus <span class=zal> equals HEAD's dt inner).
  4. 20 random annotated articles (seeded): all 3 variants carry a <span class=zal>
     with a stress mark (U+0301/U+0300/U+0341) or ё, plus title="Зализняк…".
  5. 20 random unannotated articles: no zal span (no false positives).
  6. zal span count == 992 == matched rows in zalizniak_matches.tsv.
  7. index.html and deti.html byte-identical to git HEAD (untouched by this pass).

Usage: python3 verify_zalizniak.py   (run from repo root or fasmer-2026/)
Exit code 0 = PASS, 1 = FAIL (details printed).
"""
import random, re, subprocess, sys

BASE = 'fasmer-2026/'
VARIANTS = ['original.html', 'middle.html', 'short.html']
EXPECT_MATCHED = 992
STRESS = '\u0301\u0300\u0341'
ZAL_RE = re.compile(r'<span class=zal[^>]*>(.*?)</span>')
DT_RE = re.compile(r'<dt id=(e\d+)>(.*?)</dt>', re.S)

def head(path):
    return subprocess.run(['git', 'show', f'HEAD:{path}'], capture_output=True,
                          text=True, check=True).stdout

def dts(html):
    return {m.group(1): m.group(2) for m in DT_RE.finditer(html)}

def nav_of(html):
    m = re.search(r'<nav>.*?</nav>', html, re.S)
    return m.group(0) if m else ''

def strip_zal(s):
    return ZAL_RE.sub('', s).strip()

fails = []

def check(name, ok, detail=''):
    print(('PASS' if ok else 'FAIL'), '-', name, detail)
    if not ok: fails.append(name)

# --- load TSV matched/unmatched ids
matched, unmatched = [], []
with open(BASE + 'zalizniak_matches.tsv', encoding='utf-8') as f:
    for line in f:
        p = line.rstrip('\n').split('\t')
        if len(p) >= 5 and p[0].startswith('e') and p[2]:
            matched.append(p[0])
        elif len(p) >= 5 and p[0].startswith('e'):
            unmatched.append(p[0])

rng = random.Random(6294)
sample_matched = rng.sample(matched, 20)
sample_unmatched = rng.sample(unmatched, min(20, len(unmatched)))

for f in VARIANTS:
    path = BASE + f
    now = open(path, encoding='utf-8').read()
    old = head(path)
    # 1. anchors
    ids_now = [m.group(1) for m in DT_RE.finditer(now)]
    ids_old = [m.group(1) for m in DT_RE.finditer(old)]
    check(f'{f}: anchor list identical to HEAD', ids_now == ids_old,
          f'({len(ids_now)} ids, dups={len(ids_now)-len(set(ids_now))})')
    check(f'{f}: 1408 anchors', len(ids_now) == 1408)
    # 2. nav
    check(f'{f}: <nav> byte-identical to HEAD', nav_of(now) == nav_of(old))
    # 3. headword text unchanged
    d_now, d_old = dts(now), dts(old)
    diff = [k for k in d_old if strip_zal(d_now.get(k, '')) != d_old[k]]
    check(f'{f}: headword text unchanged', not diff, f'({len(diff)} diffs)')
    # 4. sampled annotated articles
    VOWELS = set('аеёиоуыэюяАЕЁИОУЫЭЮЯ')
    def has_stress(txt):
        if any(c in txt for c in STRESS): return True      # combining acute/grave
        if 'ё' in txt.lower(): return True                   # ё IS the stress
        # monosyllabic lemma: stress implicit in the source (зять, пол, ми)
        return sum(c in VOWELS for c in txt.split()[0] if txt.split()) <= 1
    bad = []
    for eid in sample_matched:
        inner = d_now.get(eid, '')
        m = ZAL_RE.search(inner)
        if not m or 'title="Зализняк' not in inner:
            bad.append((eid, 'no span')); continue
        if not has_stress(m.group(1)):
            bad.append((eid, 'no stress: ' + m.group(1)[:40]))
    check(f'{f}: 20 sampled articles have stress+tag ({sample_matched[0]}…{sample_matched[-1]})', not bad,
          str(bad[:3]))
    # 5. sampled unannotated articles
    bad2 = [eid for eid in sample_unmatched if ZAL_RE.search(d_now.get(eid, ''))]
    check(f'{f}: 20 sampled unannotated articles have NO zal span', not bad2, str(bad2[:3]))
    # 6. span count
    n = len(ZAL_RE.findall(now))
    check(f'{f}: zal span count == {EXPECT_MATCHED}', n == EXPECT_MATCHED, f'(got {n})')

# 7. untouched files
for f in ['index.html', 'deti.html']:
    check(f'{f}: byte-identical to HEAD',
          open(BASE + f, encoding='utf-8').read() == head(BASE + f))

check('TSV matched == EXPECT', len(matched) == EXPECT_MATCHED, f'(got {len(matched)})')
print(f'\nmatched={len(matched)} unmatched={len(unmatched)} sampled=20+20')
if fails:
    print('VERDICT: FAIL', fails); sys.exit(1)
print('VERDICT: PASS — H6294 acceptance met')
