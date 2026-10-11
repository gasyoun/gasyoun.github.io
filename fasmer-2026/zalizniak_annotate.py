#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""fasmer-2026 × «Грамматический словарь» А. А. Зализняка — ударение + грам-пометa
на головных словах (original/middle/short), H6294 (09-10-2026).

Источник словаря: gramdict/zalizniak-2010 (гранки 6-го изд. 2010, ~110 тыс. слов;
правообладатель Анна Андреевна Зализняк, лицензия CC BY-NC; сайт gramdict.ru).
Файлы не коммитятся (no redistribution beyond the derived per-headword tags);
fetch: см. DECISIONS-2026-09-25.md, секция «Зализняк (H6294)».

Usage:
  python3 zalizniak_annotate.py --zaldir /path/to/zal [--root DIR]
    zaldir layout: n/*.txt (Нарицательные), v/*.txt (Глаголы), sobstv.txt (Собственные)

Idempotent: existing <span class=zal ...> in <dt> is stripped before re-injection.
Outputs: writes the three variant HTML files + zalizniak_matches.tsv.
"""
import argparse, glob, os, re, sys, unicodedata

ACCENTS = '\u0301\u0300\u0341\u030d'  # combining acute/grave/perispomeni
POS = {'м','ж','с','мо','жо','н','п','св','нсв','св-нсв','мо-жо','мн.','мн',
       'союз','част.','част','межд.','межд','предик.','предик','предл.','предл',
       'мс','мс-п','числ.','числ','вводн.','сравн.','нп'}
STOP = ('(', '[', '_', '//', '◑', '§', '<', '▷')

def norm(w):
    w = unicodedata.normalize('NFC', w)
    for a in ACCENTS: w = w.replace(a, '')
    return w

def norm_e(w):
    return norm(w).replace('ё', 'е')

def parse_line(line):
    line = line.strip()
    if not line: return None
    line = re.sub(r'^\d+/', '', line)
    line = re.sub(r'^§\d+\s*', '', line)
    # tags can sit after parenthesized notes: а (_без удар._) союз
    tail = re.sub(r'\([^)]*\)', ' ', line)
    tail = re.sub(r'\[[^\]]*\]', ' ', tail)
    parts = tail.split()
    if not parts: return None
    lemma = parts[0]
    tags = []
    for tok in parts[1:]:
        t = tok.strip(',;:')
        if not t or any(t.startswith(p) for p in STOP): break
        ok = t in POS or re.fullmatch(r'[△◑]?\d[\d/a-zа-яё*′①②③—–-]*', t) or t in ('ё','безл.','нп?')
        if ok: tags.append(t)
        else: break
    return lemma, ' '.join(tags)

def load_zal(zaldir):
    ex, ex_e = {}, {}
    def add(path):
        for line in open(path, encoding='utf-8'):
            p = parse_line(line)
            if not p: continue
            lemma, tag = p
            k = norm(lemma)                      # case-sensitive key
            if k and tag and k not in ex: ex[k] = (lemma, tag)  # skip multi-word-name fragments
            ke = norm_e(lemma).lower()
            if ke and tag and ke not in ex_e: ex_e[ke] = (lemma, tag)
    for path in sorted(glob.glob(os.path.join(zaldir, 'n', '*.txt'))): add(path)
    for path in sorted(glob.glob(os.path.join(zaldir, 'v', '*.txt'))): add(path)
    sp = os.path.join(zaldir, 'sobstv.txt')
    if os.path.exists(sp): add(sp)
    return ex, ex_e

DT_RE = re.compile(r'(<dt id=e\d+>)(.*?)(</dt>)', re.S)
ZALSPAN_RE = re.compile(r'\s*<span class=zal[^>]*>.*?</span>')

def clean_word(dt_inner):
    txt = re.sub(r'<[^>]+>', '', dt_inner)      # strip inner markup e.g. <span class=q>
    txt = txt.replace('(?)', '')                 # год (?) → год
    txt = re.sub(r'[()]', '', txt)               # Даж(д)ьбог → Даждьбог, втюрить(ся) → втюриться
    txt = txt.split()[0] if txt.split() else ''  # only the headword token
    return txt

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--zaldir', required=True)
    ap.add_argument('--root', default=os.path.dirname(os.path.abspath(__file__)))
    a = ap.parse_args()
    ex, ex_e = load_zal(a.zaldir)
    rows, methods = [], {}
    files = ['original.html', 'middle.html', 'short.html']
    for fname in files:
        path = os.path.join(a.root, fname)
        html = open(path, encoding='utf-8').read()
        out, hits = [], 0
        def repl(m):
            nonlocal hits
            open_tag, inner, close_tag = m.groups()
            inner = ZALSPAN_RE.sub('', inner)  # idempotency
            w = clean_word(inner)
            hit = ex.get(norm(w)) or ex_e.get(norm_e(w).lower())
            if hit:
                lemma, tag = hit
                method = 'exact' if norm(w) in ex else 'yo'
                note = f'{lemma}' + (f' {tag}' if tag else '')
                ann = f' <span class=zal title="Зализняк, Грамматический словарь (2010)">{note}</span>'
                inner2 = inner + ann
                hits += 1
                rows.append((fname, m.group(0), lemma, tag, method))
            else:
                inner2 = inner
            return open_tag + inner2 + close_tag
        html2 = DT_RE.sub(repl, html)
        open(path, 'w', encoding='utf-8').write(html2)
        print(f'{fname}: annotated {hits}/1408')
    # mapping table (per eN, from original pass only to avoid dup rows)
    tsv = os.path.join(a.root, 'zalizniak_matches.tsv')
    seen = set()
    with open(tsv, 'w', encoding='utf-8') as f:
        f.write('# fasmer-2026 × Зализняк: eN\tfasmer_word\tzal_lemma\tgram_tag\tmatch\n')
        html = open(os.path.join(a.root, 'original.html'), encoding='utf-8').read()
        for m in re.finditer(r'<dt id=(e\d+)>(.*?)</dt>', html):
            eid, inner = m.group(1), ZALSPAN_RE.sub('', m.group(2))
            w = clean_word(inner)
            hit = ex.get(norm(w)) or ex_e.get(norm_e(w).lower())
            lemma, tag, meth = ('', '', '')
            if hit:
                lemma, tag = hit
                meth = 'exact' if norm(w) in ex else 'yo'
            f.write(f'{eid}\t{w}\t{lemma}\t{tag}\t{meth}\n')
    n_exact = sum(1 for r in open(tsv, encoding='utf-8') if r.rstrip().endswith('\texact'))
    n_yo = sum(1 for r in open(tsv, encoding='utf-8') if r.rstrip().endswith('\tyo'))
    print(f'TSV: {tsv} — exact {n_exact}, ё-folded {n_yo}, total {n_exact+n_yo}/1408')

if __name__ == '__main__':
    main()
