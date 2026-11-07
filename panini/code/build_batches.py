#!/usr/bin/env python3
"""Turn the measured channels into a ranked core-term table and a batch curriculum.

Reads:  panini_data.txt, dsg_entries.tsv,
        ../../SanskritGrammar/data/panini_sutra_graph/study_order.tsv (topological layers)
Writes: core_terms.tsv, core_terms.json

The term inventory is curated (the ~100 real technical terms of the Pāṇinian
tradition: the 88 saṃjñās tagged in the Aṣṭādhyāyī plus the metarules), not
derived from the DSG headword list — because DSG is ~42% inventory
(affix names, author/work names, gaṇas, roots) and its digitisation has gaps
(standalone वृद्धि and अङ्ग are missing). Counts, however, are fully automatic.
"""
from __future__ import annotations

import collections
import csv
import json
import os
import re
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

HERE = os.path.dirname(os.path.abspath(__file__))
ESTATE = os.path.dirname(HERE)
DSG_URL = "https://samskrtam.ru/sanskrit-lexicon/dsg/#"

# (deva, iast, short gloss, batch, defining sūtra, [devanāgarī match prefixes])
# Prefixes are matched against the padaccheda / anuvṛtti / adhikāra word forms
# of every sūtra; a term "occurs" in a sūtra if any prefix matches any word form.
T = [
    # ---- B0: sūtra operators (structural, not vocabulary) -------------------
    ("च", "ca", "and; carries a preceding rule forward", 0, "passim", ["=च"]),
    ("न", "na", "negation / prohibition (pratiṣedha)", 0, "passim", ["=न"]),
    ("वा", "vā", "optionally", 0, "passim", ["=वा"]),
    ("विभाषा", "vibhāṣā", "optional rule (two alternatives)", 0, "1.1.44", ["विभाषा"]),
    ("अन्यतरस्याम्", "anyatarasyām", "in either of the two alternatives", 0, "passim", ["अन्यतरस्याम्"]),
    ("नित्यम्", "nityam", "obligatorily / invariably", 0, "passim", ["नित्य"]),
    ("बहुलम्", "bahulam", "variously (licensed latitude)", 0, "passim", ["बहुल"]),
    ("छन्दसि", "chandasi", "in the Veda (register tag)", 0, "passim", ["छन्दसि"]),
    ("सञ्ज्ञायाम्", "sañjñāyām", "when a technical name is meant", 0, "passim", ["संज्ञायाम्", "सञ्ज्ञायाम्"]),
    ("इति", "iti", "quotation / end-of-term marker", 0, "passim", ["=इति"]),
    ("अपि", "api", "also, even", 0, "passim", ["=अपि"]),
    ("वार्त्तिक", "vārttika", "Kātyāyana's supplementary rule", 0, "—", ["वार्त्तिक", "वार्तिक"]),

    # ---- B1: alphabet, sound classes, substitution -------------------------
    ("अक्षरसमाम्नाय", "akṣarasamāmnāya", "the 14 Śiva-sūtras; the sound inventory", 1, "Śiva-sūtras", ["अक्षरसमाम्नाय"]),
    ("प्रत्याहार", "pratyāhāra", "abbreviated sound class (aC, iK, haL …)", 1, "1.1.71", ["प्रत्याहार"]),
    ("इत्", "it", "anubandha: mute marker letter", 1, "1.3.2–1.3.9", ["इत्"]),
    ("सवर्ण", "savarṇa", "homorganic / same place+manner", 1, "1.1.9–10", ["सवर्ण"]),
    ("अनुनासिक", "anunāsika", "nasal", 1, "1.1.8", ["अनुनासिक"]),
    ("संयोग", "saṃyoga", "consonant cluster", 1, "1.1.7", ["संयोग", "सङ्योग"]),
    ("ह्रस्व / दीर्घ / प्लुत", "hrasva / dīrgha / pluta", "short / long / protracted vowel", 1, "1.2.27", ["ह्रस्व", "दीर्घ", "प्लुत"]),
    ("उदात्त / अनुदात्त / स्वरित", "udātta / anudātta / svarita", "the three accents", 1, "1.2.29–31", ["उदात्त", "अनुदात्त", "स्वरित"]),
    ("गुण", "guṇa", "the a/e/o grade", 1, "1.1.2", ["गुण"]),
    ("वृद्धि", "vṛddhi", "the ā/ai/au grade", 1, "1.1.1", ["वृद्धि"]),
    ("संप्रसारण", "saṃprasāraṇa", "semivowel → vowel replacement", 1, "1.1.45", ["संप्रसारण", "सम्प्रसारण", "संप्रसार"]),
    ("संहिता / संधि", "saṃhitā / sandhi", "contiguity; euphonic combination", 1, "1.4.109", ["संहिता", "संहितायाम्"]),
    ("लोप / लुक् / श्लु / लुप्", "lopa / luk / ślu / lup", "the four kinds of elision (zero)", 1, "1.1.60–61", ["लोप", "लुक्", "श्लु", "लुप्"]),
    ("आदेश", "ādeśa", "substitute", 1, "1.1.56", ["आदेश"]),
    ("स्थानिन्", "sthānin", "the item replaced", 1, "1.1.56", ["स्थानिन्", "स्थानि"]),
    ("आगम", "āgama", "augment (iṭ, aṭ, num …)", 1, "passim", ["आगम"]),
    ("प्रगृह्य", "pragṛhya", "vowel not subject to sandhi", 1, "1.1.11–19", ["प्रगृह्य"]),
    ("उपधा / टि / अन्त / आदि", "upadhā / ṭi / anta / ādi", "penultimate / final-part / end / beginning", 1, "1.1.64–65", ["उपधा", "टि", "अन्त", "आदि"]),

    # ---- B2: the derivation engine (highest measured scope) ----------------
    ("प्रत्यय", "pratyaya", "affix (the single highest-scope term)", 2, "3.1.1", ["प्रत्यय"]),
    ("धातु", "dhātu", "verbal root", 2, "1.3.1", ["धातु", "धातो", "धात्"]),
    ("प्रातिपदिक", "prātipadika", "nominal base (before a sup)", 2, "1.2.45–46", ["प्रातिपदिक"]),
    ("अङ्ग", "aṅga", "base immediately before an affix", 2, "1.4.13", ["अङ्ग"]),
    ("पद", "pada", "finished word (sup/tiṅ-ending)", 2, "1.4.14–17", ["पद"]),
    ("भ", "bha", "base before certain vowel/svarādi affixes", 2, "1.4.18–20", ["भस्य", "भात्", "भे"]),
    ("प्रकृति", "prakṛti", "underlying base; unchanged form", 2, "passim", ["प्रकृति", "प्रकृत्या"]),
    ("विकरण", "vikaraṇa", "conjugational stem-forming affix (śap etc.)", 2, "3.1.68", ["विकरण"]),
    ("सुप्", "sup", "the 21 nominal endings", 2, "1.1.4 / 4.1.2", ["सुप्", "सुपि", "सुपा"]),
    ("तिङ्", "tiṅ", "the 18 verbal endings", 2, "1.1.4 / 3.4.78", ["तिङ्", "तिङि", "तिङन्त"]),
    ("विभक्ति", "vibhakti", "case / personal ending", 2, "1.4.104", ["विभक्ति", "विभक्तौ"]),
    ("लकार", "lakāra", "tense-mood marker (laṭ, liṭ …)", 2, "3.2.110ff", ["लकार", "लः", "लस्य"]),
    ("कृत्", "kṛt", "primary (root → noun) affix", 2, "3.1.93", ["कृत्", "कृत"]),
    ("कृत्य", "kṛtya", "gerundive / participial kṛt subset", 2, "3.1.95–97", ["कृत्य"]),
    ("तद्धित", "taddhita", "secondary (noun → noun) affix", 2, "4.1.76", ["तद्धित"]),
    ("समासान्त", "samāsānta", "compound-final affix", 2, "5.4.68ff", ["समासान्त"]),
    ("स्त्रीप्रत्यय", "strīpratyaya", "feminine-forming affix (ṭāp, ṅīp …)", 2, "4.1.3ff", ["स्त्रियाम्", "स्त्रीप्रत्यय"]),

    # ---- B3: nominal system & kāraka ---------------------------------------
    ("लिङ्ग", "liṅga", "gender", 3, "passim", ["लिङ्ग"]),
    ("वचन", "vacana", "number (sg / du / pl)", 3, "1.4.102–103", ["वचन"]),
    ("पुरुष", "puruṣa", "person (prathama/madhyama/uttama)", 3, "1.4.101", ["पुरुष"]),
    ("संख्या", "saṅkhyā", "numeral", 3, "1.1.23–25", ["संख्या", "सङ्ख्या"]),
    ("सर्वनामन्", "sarvanāman", "pronominal", 3, "1.1.27–31", ["सर्वनाम"]),
    ("सर्वनामस्थान", "sarvanāmasthāna", "strong case stem", 3, "1.1.42–43", ["सर्वनामस्थान"]),
    ("अव्यय", "avyaya", "indeclinable", 3, "1.1.37–41", ["अव्यय"]),
    ("निपात", "nipāta", "particle", 3, "1.4.56–58", ["निपात"]),
    ("उपसर्ग", "upasarga", "verbal preverb (pra, vi, sam …)", 3, "1.4.59", ["उपसर्ग"]),
    ("गति", "gati", "preverb-like item before a verb", 3, "1.4.60–79", ["गति"]),
    ("कर्मप्रवचनीय", "karmapravacanīya", "quasi-preposition governing a case", 3, "1.4.83–98", ["कर्मप्रवचनीय"]),
    ("कारक", "kāraka", "syntactico-semantic role", 3, "1.4.23–55", ["कारक"]),
    ("कर्तृ", "kartṛ", "agent (svatantraḥ kartā)", 3, "1.4.54", ["कर्तृ", "कर्तर", "कर्ता", "कर्त्त"]),
    ("कर्मन्", "karman", "object / patient", 3, "1.4.49", ["कर्म"]),
    ("करण", "karaṇa", "instrument (sādhakatamam)", 3, "1.4.42", ["करण"]),
    ("सम्प्रदान", "sampradāna", "recipient / indirect object", 3, "1.4.32", ["सम्प्रदान", "संप्रदान"]),
    ("अपादान", "apādāna", "source / ablative role", 3, "1.4.24", ["अपादान"]),
    ("अधिकरण", "adhikaraṇa", "locus", 3, "1.4.45", ["अधिकरण"]),
    ("संबुद्धि / आमन्त्रित", "sambuddhi / āmantrita", "vocative", 3, "2.3.48–49", ["संबुद्धि", "सम्बुद्धि", "आमन्त्रित"]),
    ("समानाधिकरण", "samānādhikaraṇa", "co-referential / same case basis", 3, "2.1.49", ["समानाधिकरण", "समानाधिकरणे"]),

    # ---- B4: verbal system --------------------------------------------------
    ("दश लकाराः", "daśa lakārāḥ", "laṭ liṭ luṭ lṛṭ loṭ laṅ liṅ luṅ lṛṅ leṭ", 4, "3.2–3.4", ["लट्", "लिट्", "लुट्", "लृट्", "लोट्", "लङ्", "लिङ्", "लुङ्", "लृङ्", "लेट्"]),
    ("परस्मैपद", "parasmaipada", "active endings", 4, "1.4.99", ["परस्मैपद"]),
    ("आत्मनेपद", "ātmanepada", "middle endings", 4, "1.4.100", ["आत्मनेपद"]),
    ("प्रथम / मध्यम / उत्तम", "prathama / madhyama / uttama", "3rd / 2nd / 1st person", 4, "1.4.101", ["प्रथम", "मध्यम", "उत्तम"]),
    ("सार्वधातुक", "sārvadhātuka", "affix before which guṇa applies", 4, "3.4.113", ["सार्वधातुक"]),
    ("आर्धधातुक", "ārdhadhātuka", "affix with iṭ / no guṇa", 4, "3.4.114–117", ["आर्धधातुक"]),
    ("इट् / सेट् / अनिट्", "iṭ / seṭ / aniṭ", "intervening i augment", 4, "7.2.35ff", ["इट्", "सेट्", "अनिट्"]),
    ("क्ङिति / कित् / ङित्", "kṅiti / kit / ṅit", "k/ṅ-marked affix (no guṇa)", 4, "1.1.5", ["क्ङिति", "कित्", "ङित्"]),
    ("अभ्यास / अभ्यस्त", "abhyāsa / abhyasta", "reduplication syllable / reduplicated", 4, "6.1.4–5", ["अभ्यास", "अभ्यस्त"]),
    ("द्वित्व", "dvitva", "doubling / reduplication", 4, "6.1.1ff", ["द्वित्व"]),
    ("कर्तरि / कर्मणि / भावे", "kartari / karmaṇi / bhāve", "active / passive / impersonal voice", 4, "3.4.67–69", ["कर्तरि", "कर्मणि", "भावे", "भाव"]),
    ("सन् / सन्नन्त", "san / sannanta", "desiderative", 4, "3.1.7", ["सन्", "सन्नन्त"]),
    ("णिच् / णिजन्त", "ṇic / ṇijanta", "causative", 4, "3.1.26", ["णिच्", "णिजन्त", "णौ"]),
    ("निष्ठा / सत्", "niṣṭhā / sat", "kta/ktavatu; present participle", 4, "1.1.26 / 3.2.127", ["निष्ठा", "निष्ठायाम्", "सत्"]),
    ("सकर्मक / अकर्मक", "sakarmaka / akarmaka", "transitive / intransitive", 4, "1.4.52ff", ["सकर्मक", "अकर्मक"]),
    ("हेतु", "hetu", "causer / instigator", 4, "1.4.55", ["हेतु", "हेतौ"]),
    ("आम्रेडित", "āmreḍita", "repeated word in iteration", 4, "8.1.2", ["आम्रेडित"]),

    # ---- B5: compounds & secondary derivation ------------------------------
    ("समास", "samāsa", "compound", 5, "2.1.3", ["समास"]),
    ("तत्पुरुष", "tatpuruṣa", "determinative compound", 5, "2.1.22", ["तत्पुरुष"]),
    ("कर्मधारय", "karmadhāraya", "appositional tatpuruṣa", 5, "1.2.42", ["कर्मधारय"]),
    ("द्विगु", "dvigu", "numeral-initial tatpuruṣa", 5, "2.1.23", ["द्विगु"]),
    ("बहुव्रीहि", "bahuvrīhi", "exocentric (possessive) compound", 5, "2.2.23", ["बहुव्रीहि"]),
    ("द्वन्द्व", "dvandva", "copulative compound", 5, "2.2.29", ["द्वन्द्व"]),
    ("अव्ययीभाव", "avyayībhāva", "indeclinable compound", 5, "2.1.5", ["अव्ययीभाव"]),
    ("पूर्वपद / उत्तरपद", "pūrvapada / uttarapada", "prior / latter compound member", 5, "passim", ["पूर्वपद", "उत्तरपद"]),
    ("उपसर्जन", "upasarjana", "subordinate compound member", 5, "1.2.43–44", ["उपसर्जन"]),
    ("उपपद", "upapada", "governing co-occurring word", 5, "3.1.92", ["उपपद"]),
    ("सामर्थ्य", "sāmarthya", "semantic fitness required for derivation", 5, "2.1.1", ["समर्थ", "सामर्थ्य"]),
    ("अपत्य", "apatya", "descendant (taddhita sense)", 5, "4.1.92ff", ["अपत्य"]),
    ("गोत्र / युवन् / तद्राज", "gotra / yuvan / tadrāja", "lineage grades in taddhita", 5, "4.1.162–174", ["गोत्र", "युवन्", "तद्राज"]),
    ("वृद्ध", "vṛddha", "name-eligible elder / vṛddha-class", 5, "1.1.73–75", ["वृद्ध", "!वृद्धि"]),
    ("नदी / घि / घु", "nadī / ghi / ghu", "special stem classes", 5, "1.4.3–9, 1.1.20", ["नदी", "नद्या", "घि", "घु"]),
    ("अवसान", "avasāna", "pause / word-final position", 5, "1.4.110", ["अवसान"]),
    ("अपृक्त", "apṛkta", "affix consisting of a single phoneme", 5, "1.2.41", ["अपृक्त"]),
    ("विग्रह", "vigraha", "analytic paraphrase of a compound", 5, "—", ["विग्रह"]),

    # ---- B6: metarules / reference layer ------------------------------------
    ("सञ्ज्ञा", "sañjñā", "technical term (saṃjñā)", 6, "1.1.1ff", ["संज्ञा", "सञ्ज्ञा"]),
    ("परिभाषा", "paribhāṣā", "metarule interpreting other rules", 6, "passim", ["परिभाषा"]),
    ("अनुवृत्ति", "anuvṛtti", "recurrence of words from a prior rule", 6, "passim", ["अनुवृत्ति"]),
    ("अधिकार", "adhikāra", "governing heading rule", 6, "passim", ["अधिकार"]),
    ("अपवाद / उत्सर्ग", "apavāda / utsarga", "exception / general rule", 6, "passim", ["अपवाद", "उत्सर्ग"]),
    ("अतिदेश", "atideśa", "transfer of properties by extension", 6, "passim", ["अतिदेश"]),
    ("असिद्ध", "asiddha", "not yet in effect (rule ordering)", 6, "8.2.1 / 6.4.22", ["असिद्ध"]),
    ("अन्तरङ्ग / बहिरङ्ग", "antaraṅga / bahiraṅga", "internally / externally conditioned", 6, "paribhāṣā", ["अन्तरङ्ग", "बहिरङ्ग"]),
    ("नित्य / अनित्य", "nitya / anitya", "invariably / variably applicable", 6, "paribhāṣā", ["नित्य", "अनित्य"]),
    ("स्थाने / अन्तरतम", "sthāne / antaratama", "in place of / nearest substitute", 6, "1.1.50 / 1.1.56", ["स्थाने", "अन्तरतम"]),
    ("योगविभाग", "yogavibhāga", "splitting one sūtra into two", 6, "paribhāṣā", ["योगविभाग"]),
    ("उपसंख्यान / इष्टि", "upasaṅkhyāna / iṣṭi", "supplement / desideratum to a rule", 6, "vārttika", ["उपसङ्ख्यान", "उपसंख्यान", "इष्टि"]),
    ("व्याकरण", "vyākaraṇa", "grammar (the discipline)", 6, "—", ["व्याकरण"]),
    ("शब्द / अर्थ / स्फोट", "śabda / artha / sphoṭa", "word / meaning / semantic whole", 6, "Vākyapadīya", ["शब्द", "अर्थ", "स्फोट"]),
    ("वाच्य / वाचक", "vācya / vācaka", "expressed sense / expression", 6, "later Vyākaraṇa", ["वाच्य", "वाचक"]),
    ("प्रातिशाख्य / शिक्षा", "prātiśākhya / śikṣā", "Vedic phonetics treatises", 6, "—", ["प्रातिशाख्य", "शिक्षा"]),
    ("महाभाष्य / काशिका / सिद्धान्तकौमुदी", "Mahābhāṣya / Kāśikā / SK", "the three reference works", 6, "—", ["महाभाष्य", "काशिका", "सिद्धान्तकौमुदी"]),
]

BATCHES = {
    0: ("Operators — one sitting, teach structurally, never drill",
        "The most *written* words in the Aṣṭādhyāyī are not concepts: ca appears in 847 of 3,983 sūtras. "
        "Learn these as the punctuation of a sūtra. Your own difficulty-ordering study (τ=0.89 within "
        "content vocabulary) showed the decisive curation move is function-word exclusion — same here."),
    1: ("Alphabet, sound classes, substitution",
        "Everything needed to decode a sūtra's phonological metalanguage: the Śiva-sūtras, pratyāhāras, "
        "it-markers, the vowel grades and the zero/substitution vocabulary."),
    2: ("The derivation engine — highest measured scope",
        "These are the terms that govern the most sūtras *without being written*. pratyaya governs 1,821 "
        "sūtras (46%); prātipadika 1,190; taddhita 1,115; aṅga 613; dhātu 610."),
    3: ("Nominal system and kāraka",
        "The 1.4 kāraka section plus the categories needed to decline and parse a noun. "
        "Learn the six kārakas as one block, not six separate words."),
    4: ("Verbal system",
        "The ten lakāras, the two padas, the sārvadhātuka/ārdhadhātuka split, reduplication and the "
        "derived stems. iṭ is inherited into 70 sūtras; kṛt into 498."),
    5: ("Compounds and secondary derivation",
        "The samāsa taxonomy and the taddhita sense-categories. This is where DSG starts to earn its keep "
        "as a lookup tool rather than a reading list."),
    6: ("Metarules, hermeneutics and the reference shelf",
        "Rule-interpretation vocabulary and the names of the works. Read once, then use as an index — "
        "these are the terms that make the commentaries readable."),
}


def norm(w):
    w = w.strip().strip(".,;:!?()[]{}\"' \u0964\u0965")
    w = w.replace("\u2019", "").replace("\u2013", "-").replace("\u093d", "")
    return re.sub(r"[\u0902\u0903]+$", "", w)


def words(field):
    out = []
    for chunk in (field or "").split("##"):
        w = chunk.split("$")[0].strip()
        for part in w.split("-"):
            p = norm(part)
            if p:
                out.append(p)
    return out


def main():
    j = json.loads(open(os.path.join(HERE, "panini_data.txt"), encoding="utf-8-sig").read())
    sutras = []
    for r in j["data"]:
        sutras.append({
            "ref": "%s.%s.%s" % (r["a"], r["p"], r["n"]),
            "pc": words(r.get("pc")), "an": words(r.get("an")), "ad": words(r.get("ad")),
        })

    # topological layers from the estate's Pāṇini graph (different corpus snapshot,
    # refs are stable; treat as an ordering hint, not an exact count)
    layer = {}
    p = os.path.join(ESTATE, "SanskritGrammar", "data", "panini_sutra_graph", "study_order.tsv")
    if os.path.exists(p):
        for row in csv.DictReader(open(p, encoding="utf-8"), delimiter="\t"):
            layer[row["ref"]] = int(row["layer"])

    dsg = {}
    for e in csv.DictReader(open(os.path.join(HERE, "dsg_entries.tsv"), encoding="utf-8"), delimiter="\t"):
        dsg[e["deva"]] = e

    # DSG spelling variants: the dictionary writes sañjñā / saṅkhyā, not saṃjñā / saṃkhyā
    DSG_ALIAS = {
        "सञ्ज्ञा": "सञ्ज्ञा", "संज्ञा": "सञ्ज्ञा", "वृद्धि": "वृद्धि",
        "अङ्ग": "अङ्ग", "संख्या": "सङ्ख्या", "संप्रसारण": "सम्प्रसारण",
        "संयोग": "संयोग", "संहिता / संधि": "संहिता", "संबुद्धि / आमन्त्रित": "सम्बुद्धि",
        "सामर्थ्य": "सामर्थ्य", "कर्मप्रवचनीय": "कर्मप्रवचनीय",
    }

    out = []
    for deva, iast, gloss, batch, sutra, prefixes in T:
        # '=xyz' -> exact word-form match (for 1-syllable operators where a
        # prefix match would swallow every word beginning with that syllable);
        # '!xyz' -> exclusion, applied after the positive match.
        exact = {norm(x[1:]) for x in prefixes if x.startswith("=")}
        exclude = [norm(x[1:]) for x in prefixes if x.startswith("!")]
        pref = [norm(x) for x in prefixes if not x.startswith(("=", "!"))]
        def m(w):
            if any(w.startswith(p) for p in exclude):
                return False
            return w in exact or any(w.startswith(p) for p in pref if p)
        exp = {s["ref"] for s in sutras if any(m(w) for w in s["pc"])}
        inh = {s["ref"] for s in sutras if any(m(w) for w in s["an"])}
        gov = {s["ref"] for s in sutras if any(m(w) for w in s["ad"])}
        first = min((layer[r] for r in exp if r in layer), default=None)
        key = DSG_ALIAS.get(deva, deva.split(" / ")[0])
        e = dsg.get(key) or dsg.get(deva)
        out.append({
            "deva": deva, "iast": iast, "gloss": gloss, "batch": batch, "sutra": sutra,
            "explicit": len(exp), "inherited": len(inh), "governed": len(gov),
            "total": len(exp | inh | gov), "first_layer": first,
            "dsg_id": e["id"] if e else None,
            "dsg_chars": int(e["en_chars"]) if e else 0,
            "dsg_cites": int(e["cites"]) if e else 0,
            "dsg_url": (DSG_URL + e["id"]) if e else None,
        })

    with open(os.path.join(HERE, "core_terms.tsv"), "w", encoding="utf-8") as f:
        cols = ["batch", "deva", "iast", "total", "explicit", "inherited", "governed",
                "first_layer", "dsg_chars", "dsg_cites", "sutra", "gloss", "dsg_url"]
        f.write("\t".join(cols) + "\n")
        for x in out:
            f.write("\t".join("" if x[c] is None else str(x[c]) for c in cols) + "\n")

    meta = {
        "batches": {str(k): {"title": v[0], "note": v[1]} for k, v in BATCHES.items()},
        "terms": out,
        "counts": {str(b): sum(1 for x in out if x["batch"] == b) for b in BATCHES},
    }
    with open(os.path.join(HERE, "core_terms.json"), "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=1)

    for b in sorted(BATCHES):
        xs = [x for x in out if x["batch"] == b]
        print("B%d  %2d terms  %s" % (b, len(xs), BATCHES[b][0]))
        for x in sorted(xs, key=lambda y: -y["total"])[:6]:
            print("      %-22s total=%4d (exp %3d / inh %3d / gov %4d)" %
                  (x["iast"], x["total"], x["explicit"], x["inherited"], x["governed"]))
    print("\ntotal curated terms:", len(out),
          "| with a DSG entry:", sum(1 for x in out if x["dsg_id"]),
          "| with a study layer:", sum(1 for x in out if x["first_layer"]))


if __name__ == "__main__":
    main()
