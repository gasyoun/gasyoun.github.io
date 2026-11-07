"""Teaching metadata for the Sanskrit-etymology snapshot generator.

Kept in its own module so the generator stays small, reviewable and under the
repository's staged-file token gate. `DESC` paraphrases the source category
introductions; `GRADES` drives the guṇa/vṛddhi lab on wiki/index.html.

Source: https://en.wiktionary.org/wiki/Category:Sanskrit_terms_by_etymology
"""

LENS = {
    "origin": {
        "borrowed terms", "borrowed back", "calques", "derived from other languages",
        "inherited terms", "semantic loans", "by Arabic root", "by Ashokan Prakrit root",
        "by Proto-Dravidian root", "by Proto-Dravidian word", "by Proto-Indo-Aryan root",
        "by Proto-Indo-European root", "by Proto-Indo-European word",
        "by Proto-Indo-Iranian root", "by Proto-South Dravidian root",
        "by Sanskrit root", "by Vedic Sanskrit root", "by Sanskritization",
    },
    "evidence": {
        "attributed to a specific source", "doublets", "neologisms", "nonce terms",
        "onomatopoeias", "reconstructed terms", "sound-symbolic", "defective word group",
        "unknown etymologies",
    },
}

DESC = {
    "Sanskrit back-formations": "Formed by reversing a supposed regular formation.",
    "Sanskrit borrowed terms": "Loanwords incorporated directly from another language.",
    "Sanskrit calques": "Piece-by-piece translations of terms from other languages.",
    "Sanskrit compound terms": "Terms composed of two or more stems (samāsa).",
    "Sanskrit words derived through corruption": "Result of a sporadic, non-systematic change.",
    "Sanskrit deverbals": "Terms derived from a verb.",
    "Sanskrit doublets": "Same ultimate source as another term, but a different route.",
    "Sanskrit inherited terms": "Inherited from an earlier stage of the language.",
    "Sanskrit words derived through metathesis": "Created by transposing sounds.",
    "Sanskrit neologisms": "Only recently acknowledged terms.",
    "Sanskrit nonce terms": "Invented for a single occasion.",
    "Sanskrit onomatopoeias": "Coined to sound like what they represent.",
    "Sanskrit reconstructed terms": "Not directly attested; reconstructed from evidence.",
    "Sanskrit reduplications": "Formed by repeating a root or stem.",
    "Sanskrit roots": "Basic morphemes (dhātu) from which words are formed.",
    "Sanskrit semantic loans": "A sense borrowed from a term in another language.",
    "Sanskrit sound-symbolic terms": "Sound symbolism, not strictly onomatopoeic.",
    "Sanskrit syncopic forms": "Loss of an interior sound or syllable.",
    "Sanskrit terms attributed to a specific source": "Coined by an identifiable person or work.",
    "Sanskrit terms by interfix": "Categorised by their interfixes.",
    "Sanskrit terms by prefix": "Categorised by their prefixes (upasarga).",
    "Sanskrit terms by root": "Categorised by the root they originate from.",
    "Sanskrit terms by suffix": "Categorised by their suffixes (pratyaya).",
    "Sanskrit terms derived from other languages": "Terms originating outside Sanskrit.",
    "Sanskrit terms with Indo-Aryan extensions": "Extended with pleonastic Indo-Aryan affixes.",
    "Sanskrit terms with unknown etymologies": "Etymology not yet established.",
    "Sanskrit univerbations": "Agglutination of two or more words into one.",
    "Sanskrit vrddhi derivatives": "Derived from a PIE root by vṛddhi derivation.",
}


def lens_for(name):
    for lens, needles in LENS.items():
        if any(n in name for n in needles):
            return lens
    return "formation"


GRADES = [
    {"vowels": "a / ā", "zero": "a / ā", "guna": "a", "vrddhi": "ā",
     "sandhi": "Before a following vowel: a and ā surface unchanged; only length changes.",
     "root": "पच्", "rootIast": "√pac",
     "gunaWord": "पचति", "gunaIast": "pacati",
     "vrddhiWord": "पाक", "vrddhiIast": "pāka",
     "gloss": "to cook → he cooks → cooking"},
    {"vowels": "i / ī", "zero": "i / ī", "guna": "e", "vrddhi": "ai",
     "sandhi": "Before a following vowel: e → ay, ai → āy (compare √ji + a → जय).",
     "root": "विद्", "rootIast": "√vid",
     "gunaWord": "वेद", "gunaIast": "veda",
     "vrddhiWord": "वैदिक", "vrddhiIast": "vaidika",
     "gloss": "to know → knowledge → Vedic"},
    {"vowels": "u / ū", "zero": "u / ū", "guna": "o", "vrddhi": "au",
     "sandhi": "Before a following vowel: o → av, au → āv (compare √bhū + a → भवति).",
     "root": "बुध्", "rootIast": "√budh",
     "gunaWord": "बोध", "gunaIast": "bodha",
     "vrddhiWord": "बौद्ध", "vrddhiIast": "bauddha",
     "gloss": "to wake → awakening → Buddhist"},
    {"vowels": "ṛ / ṝ", "zero": "ṛ / ṝ", "guna": "ar", "vrddhi": "ār",
     "sandhi": "Before a following vowel: ar and ār stay as they are (√kṛ → करोति, कार्य).",
     "root": "कृ", "rootIast": "√kṛ",
     "gunaWord": "करोति", "gunaIast": "karoti",
     "vrddhiWord": "कार्य", "vrddhiIast": "kārya",
     "gloss": "to do → he does → to be done"},
    {"vowels": "ḷ", "zero": "ḷ", "guna": "al", "vrddhi": "āl",
     "sandhi": "Before a following vowel: al and āl stay as they are; almost no roots are attested.",
     "root": "", "rootIast": "—",
     "gunaWord": "", "gunaIast": "—",
     "vrddhiWord": "", "vrddhiIast": "—",
     "gloss": "Rare in classical Sanskrit; listed for completeness"},
]
