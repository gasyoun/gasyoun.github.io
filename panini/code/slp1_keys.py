#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Canonical transliteration keys for DSG headwords and DCS joins.

Why this module exists
----------------------
The column called ``slp1`` in the DSG page (and in the first version of
``dsg_entries.tsv``) is **Harvard-Kyoto (HK), not SLP1**.  Joining it directly
to the DCS ranking table silently produces wrong keys:

    naive IAST  "taddhita"  ->  tadDita   (d + D, not d + dh)
    naive IAST  "vibhakti"  ->  viBakti
    DSG HK      "Adeza"     ->  AdeSa     (HK z = ś; SLP1 S = ś)
    DSG HK      "saJjJA"    ->  saYjYA    (HK J = ñ; SLP1 Y = ñ)
    DSG HK      "saGkhyA"   ->  saNKyA    (HK G = ṅ; SLP1 N = ṅ, K = ख)
    DSG HK      "kRt"       ->  kft       (HK R = ṛ; SLP1 f = ṛ)

HK and SLP1 differ by a *cyclic* substitution, so sequential string.replace()
is wrong: the conversion must be a single left-to-right longest-match pass.

This module is the only place where the three encodings are converted.  Both
``measure.py`` and ``external_channels.py`` import from it, so a correction
cannot be applied in one script and forgotten in the other.

Also provides class-nasal <-> anusvāra variants:

    Devanāgarī  सञ्ज्ञा / संज्ञा, सङ्ख्या / संख्या, सम्प्रसारण / संप्रसारण
    SLP1        saYjYA / saMjYA, saNKyA / saMKyA, samprasAraRa / saMprasAraRa

DCS attests both spellings unevenly (``saYjYA`` = 28, ``saMjYA`` absent;
``aNga`` = 127, ``aMga`` absent), so a single canonical key loses real hits.
"""
from __future__ import annotations

import re
import unicodedata

# ---------------------------------------------------------------------------
# Devanāgarī orthographic variants
# ---------------------------------------------------------------------------
DEV_PAIRS = [
    ("\u091e\u094d\u091c", "\u0902\u091c"),  # ञ्ज <-> ंज
    ("\u0919\u094d\u0917", "\u0902\u0917"),  # ङ्ग <-> ंग
    ("\u0919\u094d\u0915", "\u0902\u0915"),  # ङ्क <-> ंक
    ("\u0923\u094d\u0921", "\u0902\u0921"),  # ण्ड <-> ंड
    ("\u092e\u094d\u092a", "\u0902\u092a"),  # म्प <-> ंप
    ("\u0928\u094d\u0927", "\u0902\u0927"),  # न्ध <-> ंध
    ("\u0928\u094d\u0928", "\u0902\u0928"),  # न्न <-> ंन
    ("\u092e\u094d\u092c", "\u0902\u092c"),  # म्ब <-> ंब
    ("\u091e\u094d\u091a", "\u0902\u091a"),  # ञ्च <-> ंच
    ("\u0923\u094d\u0923", "\u0902\u0923"),  # ण्ण <-> ंण
]


def dev_variants(w):
    """Return both class-nasal and anusvāra spellings of a Devanāgarī stem."""
    s = {w}
    for a, b in DEV_PAIRS:
        s |= {x.replace(a, b) for x in list(s)}
        s |= {x.replace(b, a) for x in list(s)}
    return {x for x in s if x}


def fold(s):
    """Fold IAST to a diacritic-free, anusvāra-homogeneous ASCII-ish key.

    NFD + Mn stripping turns ā->a, ṛ->r, ñ->n, ṃ->m, ṣ->s, ś->s ...
    The final regex collapses ``sañjñā`` / ``saṃjñā`` and ``aṅga`` / ``aṃga``
    onto one key (``saMjna`` / ``aMga``), which is exactly the DSG-vs-corpus
    spelling variation.
    """
    s = unicodedata.normalize("NFD", s)
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    s = s.lower()
    return re.sub(r"[nm](?=[bcdfghjklmnpqrstvwxyz])", "M", s)


# ---------------------------------------------------------------------------
# IAST -> SLP1
# ---------------------------------------------------------------------------
# Longest match first.  Two-letter digraphs must precede their single-letter
# parts, otherwise "dh" becomes "d"+"h" and "ai" becomes "a"+"i".
IAST_MAP = [
    ("ai", "E"), ("au", "O"),
    ("l\u1e5b", "x"), ("l\u1e5d", "X"),     # lṛ / lṝ (vocalic ḷ as DSG writes it)
    ("\u0101", "A"), ("\u012b", "I"), ("\u016b", "U"),     # ā ī ū
    ("\u1e5b", "f"), ("\u1e5d", "F"),        # ṛ ṝ
    ("\u1e37", "x"), ("\u1e39", "X"),        # ḷ ḹ
    ("\u1e43", "M"), ("\u1e41", "M"),        # ṃ ṁ
    ("\u1e25", "H"),                         # ḥ
    ("\u1e45", "N"), ("\u00f1", "Y"), ("\u1e47", "R"),   # ṅ ñ ṇ
    ("\u1e6dh", "W"), ("\u1e0dh", "Q"),      # ṭh ḍh
    ("kh", "K"), ("gh", "G"), ("ch", "C"), ("jh", "J"),
    ("th", "T"), ("dh", "D"), ("ph", "P"), ("bh", "B"),
    ("\u015b", "S"), ("\u1e63", "z"),        # ś ṣ
    ("\u1e6d", "w"), ("\u1e0d", "q"),        # ṭ ḍ
    ("k", "k"), ("g", "g"), ("c", "c"), ("j", "j"),
    ("t", "t"), ("d", "d"), ("p", "p"), ("b", "b"),
    ("m", "m"), ("n", "n"), ("y", "y"), ("r", "r"),
    ("l", "l"), ("v", "v"), ("s", "s"), ("h", "h"),
    ("a", "a"), ("i", "i"), ("u", "u"), ("e", "e"), ("o", "o"),
]
# Compatibility alias for the earlier version of external_channels.py.
SLP_MAP = IAST_MAP
_IAST_RE = re.compile("|".join(re.escape(a) for a, _ in IAST_MAP))
_IAST_D = dict(IAST_MAP)


def primary_iast(s):
    """First transliterated headword from a DSG ``iast`` cell such as
    ``/a ೱ k/, /jihvāmūlīya/`` -> ``a ೱ k``."""
    return re.split(r"\s*/\s*", (s or "").strip().strip("/ "))[0].strip()


def iast_to_slp1(s):
    s = primary_iast(s).lower().replace(" ", "")
    return "".join(_IAST_D.get(m.group(0), "") for m in _IAST_RE.finditer(s))


# ---------------------------------------------------------------------------
# Harvard-Kyoto -> SLP1
# ---------------------------------------------------------------------------
# DSG's HK is the Cologne-style variant: A/I/U long vowels, R = ṛ,
# G = ṅ, J = ñ, N = ṇ, T/D = ṭ/ḍ, z = ś, S = ṣ, M/H = ṃ/ḥ.
# Aspirates are written as digraphs (kh, Th, dh ...), NOT as capitals.
HK_MAP = [
    ("lRR", "X"), ("lR", "x"), ("RR", "F"),
    ("ai", "E"), ("au", "O"),
    ("kh", "K"), ("gh", "G"), ("ch", "C"), ("jh", "J"),
    ("Th", "W"), ("Dh", "Q"), ("th", "T"), ("dh", "D"),
    ("ph", "P"), ("bh", "B"),
    ("A", "A"), ("I", "I"), ("U", "U"), ("R", "f"),
    ("M", "M"), ("H", "H"),
    ("G", "N"), ("J", "Y"), ("N", "R"),      # ṅ ñ ṇ
    ("T", "w"), ("D", "q"),                  # ṭ ḍ
    ("z", "S"), ("S", "z"),                  # ś / ṣ are SWAPPED in SLP1
    ("X", "X"),
    ("k", "k"), ("g", "g"), ("c", "c"), ("j", "j"),
    ("t", "t"), ("d", "d"), ("p", "p"), ("b", "b"),
    ("m", "m"), ("n", "n"), ("y", "y"), ("r", "r"),
    ("l", "l"), ("v", "v"), ("s", "s"), ("h", "h"),
    ("a", "a"), ("i", "i"), ("u", "u"), ("e", "e"), ("o", "o"),
]
_HK_RE = re.compile("|".join(re.escape(a) for a, _ in HK_MAP))
_HK_D = dict(HK_MAP)


def hk_is_clean(hk):
    """True when the HK cell is a single plain Latin headword we can convert."""
    return bool(re.fullmatch(r"[a-zA-Z]+", hk or ""))


def hk_to_slp1(hk):
    """Single-pass longest-match HK -> SLP1 (never sequential replace)."""
    return "".join(_HK_D.get(m.group(0), "") for m in _HK_RE.finditer((hk or "").strip()))


# ---------------------------------------------------------------------------
# SLP1 class-nasal <-> anusvāra variants
# ---------------------------------------------------------------------------
# SLP1 nasals: N = ṅ, Y = ñ, R = ṇ, n = न्, m = म्, M = anusvāra.
# f/F/x/X are vocalics, NOT nasals -- do not confuse them with R.
CLASS_NASALS = frozenset("NYRnm")
HOMORGANIC = {}
for _c, _n in (("kKgG", "N"), ("cCjJ", "Y"), ("wWqQ", "R"),
               ("tTdD", "n"), ("pPbB", "m")):
    for _ch in _c:
        HOMORGANIC[_ch] = _n
# Only stops and nasals participate in the class-nasal/anusvAra alternation.
# Fricatives/approximants (y r l v z S s h) are excluded: a spelling like
# ``aMyatarasyAm`` for अन्यतरस्याम् does not exist and would be a false key.
SLP_STOPS = frozenset("kKgGcCjJwWqQtTdDpPbB")
SLP_NASALS = frozenset("nNYRm")
SLP_CONSONANTS = SLP_STOPS | SLP_NASALS


def slp1_variants(key, max_edits=3, cap=64):
    """All class-nasal <-> anusvāra spellings of one SLP1 key.

    A class nasal immediately before a consonant may be written as anusvāra
    (``aNga`` -> ``aMga``, ``saYjYA`` -> ``saMjYA``); conversely an anusvāra
    before a stop may be written as its homorganic class nasal
    (``aMga`` -> ``aNga``, ``saMjYA`` -> ``saYjYA``).  Word-final nasals are
    NOT varied: ``aM`` (the letter aṃ) and ``an`` are different words.

    Bounded BFS: at most ``max_edits`` substitutions and ``cap`` results, so
    the join stays deterministic and cannot explode on long compounds.
    """
    if not key:
        return {""}
    out = {key}
    frontier = [key]
    for _ in range(max_edits):
        nxt_frontier = []
        for k in frontier:
            for i, ch in enumerate(k):
                if i + 1 >= len(k) or k[i + 1] not in SLP_CONSONANTS:
                    continue
                alts = []
                if ch in CLASS_NASALS:
                    alts.append("M")
                elif ch == "M":
                    h = HOMORGANIC.get(k[i + 1])
                    if h:
                        alts.append(h)
                for a in alts:
                    alt = k[:i] + a + k[i + 1:]
                    if alt not in out:
                        out.add(alt)
                        nxt_frontier.append(alt)
                        if len(out) >= cap:
                            return out
        if not nxt_frontier:
            break
        frontier = nxt_frontier
    return out


def dcs_lookup(dcs, base_key):
    """Look up one term in the DCS ranking table using every spelling variant.

    Returns ``(best_key, count, hits, tried)``.  Orthographic variants are
    alternative spellings of *one* lemma, so we take the best-attested key
    (max) rather than summing, which would double-count.  ``hits`` records
    every attested variant so nothing is hidden.
    """
    tried = sorted(slp1_variants(base_key))
    hits = {k: dcs[k] for k in tried if dcs.get(k, 0) > 0}
    if not hits:
        return "", 0, {}, tried
    best = max(hits, key=lambda k: hits[k])
    return best, hits[best], hits, tried


if __name__ == "__main__":
    for a, b in [("taddhita", "tadDita"), ("vibhakti", "viBakti"),
                 ("ādeśa", "AdeSa"), ("dhātu", "DAtu"), ("kṛt", "kft"),
                 ("lṛ", "x"), ("āṁ", "AM")]:
        print("IAST %-14s -> %-14s (expected %s)" % (a, iast_to_slp1(a), b))
    for a, b in [("Adeza", "AdeSa"), ("saJjJA", "saYjYA"),
                 ("saGkhyA", "saNKyA"), ("kRt", "kft"), ("aN", "aR")]:
        print("HK   %-14s -> %-14s (expected %s)" % (a, hk_to_slp1(a), b))
    for k in ("aNga", "saYjYA", "saMjYA", "tadDita", "saMDi", "aM"):
        print("VAR  %-12s -> %s" % (k, sorted(slp1_variants(k))))
