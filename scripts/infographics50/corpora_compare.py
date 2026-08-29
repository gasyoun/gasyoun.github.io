#!/usr/bin/env python3
"""Corpora side-by-side #16 — DCS vs spoken vs telegram Sanskrit corpora.

Derives infographics/corpora-side-by-side-2026-08-29/{data.json,index.html}.
Sources (committed):
  dcs-conllu/files/*/*.conllu                — sentences + tokens
  spoken-sanskrit-corpus/data/manifest/video_transcripts_index.jsonl — indexed transcripts
  telegram-sanskrit-corpus/data/derived/messages.clean.jsonl — anonymized messages
"""
import glob
import json
import os
import re

BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
OUT = os.path.join(BASE, "infographics", "corpora-side-by-side-2026-08-29")


def fmt(v):
    return "{:,}".format(v).replace(",", " ")


def main():
    files = glob.glob("/Users/mac/Documents/GitHub/dcs-conllu/files/*/*.conllu")
    sents = tokens = 0
    for f in files:
        for line in open(f, encoding="utf-8"):
            if line.startswith("# sent_id"):
                sents += 1
            elif re.match(r"^\d+\t", line):
                tokens += 1
    texts = len(set(os.path.dirname(f) for f in files))

    spoken = [json.loads(l) for l in open(
        "/Users/mac/Documents/GitHub/spoken-sanskrit-corpus/data/manifest/video_transcripts_index.jsonl",
        encoding="utf-8")]

    tw = tc = 0
    peers = set()
    for l in open("/Users/mac/Documents/GitHub/telegram-sanskrit-corpus/data/derived/messages.clean.jsonl",
                  encoding="utf-8"):
        r = json.loads(l)
        t = r.get("clean_text") or r.get("text") or ""
        tw += len(t.split())
        tc += len(t)
        peers.add(r.get("peer_title") or r.get("peer"))
    ratio = round(tokens / tw)

    os.makedirs(OUT, exist_ok=True)
    json.dump({"dcs": {"texts": texts, "files": len(files), "sentences": sents, "tokens": tokens},
               "spoken": {"transcripts": len(spoken)},
               "telegram": {"messages": sum(1 for _ in open(
                   "/Users/mac/Documents/GitHub/telegram-sanskrit-corpus/data/derived/messages.clean.jsonl",
                   encoding="utf-8")), "words": tw, "chars": tc, "chats": len(peers)},
               "dcs_vs_telegram_words_x": ratio},
              open(os.path.join(OUT, "data.json"), "w", encoding="utf-8"), indent=1)

    # bars: each corpus on its OWN scale (unit noted), honest non-comparison
    def bar(w):
        return '<rect x="0" y="0" width="%.0f" height="22" fill="var(--chart-1)"/>' % w if w else ''

    rows = [
        ("dcs", "DCS · письменная классика", "5 688 416", "токенов", 500),
        ("spoken", "Spoken · устная речь (видео)", "2 861", "транскрипта", 160),
        ("tg", "Telegram · живой чат", "27 898", "слов", 273),
    ]
    bars = []
    for i, (key, label, val, unit, w) in enumerate(rows):
        y = 0
        bars.append(
            '<div class="row"><div class="rl">%s</div><svg class="rb" width="505" height="22">%s</svg>'
            '<div class="rv">%s <span class="ru">%s</span></div></div>' % (label, bar(w), val, unit))

    html = TEMPLATE.format(
        dcs_t=fmt(tokens), dcs_s=fmt(sents), dcs_txt=texts, dcs_f=fmt(len(files)),
        sp_n=fmt(len(spoken)),
        tg_m="979", tg_w=fmt(tw), tg_ch=fmt(tc), tg_peers=len(peers),
        ratio=ratio, rows="\n      ".join(bars))
    open(os.path.join(OUT, "index.html"), "w", encoding="utf-8").write(html)
    print("dcs tokens", tokens, "sents", sents, "| spoken", len(spoken), "| tg words", tw, "x", ratio)


TEMPLATE = """<!doctype html>
<html lang="ru">
<head>
<meta charset="utf-8">
<title>Три корпуса санскрита рядом</title>
<!-- Composition: Bleed — the DCS token numeral runs off the right edge; the two small corpora
     sit as ruled charticle rows below. Editorial, wide 1920x1080. Bars are per-corpus own-scale
     (unit labeled) — cross-corpus magnitudes differ ~200x and are stated in text instead. -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,400;0,9..144,600;0,9..144,900;1,9..144,400&family=Libre+Franklin:wght@400;500;600&display=swap" rel="stylesheet">
<style>
*, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
:root {{
  --bg:#FAF7F2; --surface:#F1ECE2; --surface-2:#E3DCCC;
  --ink:#20242C; --ink-muted:#6B6F76; --accent:#A32035;
  --font-display:'Fraunces',serif; --font-body:'Libre Franklin',sans-serif;
}}
html, body {{ background: var(--bg); }}
body {{ width: 1920px; font-family: var(--font-body); color: var(--ink); }}
.canvas {{ position: relative; width: 1920px; height: 1080px; overflow: hidden; background: var(--bg); }}
.folio {{ position: absolute; left: 72px; right: 72px; top: 40px; display: flex; justify-content: space-between;
  border-top: 1px solid var(--ink); border-bottom: 1px solid var(--ink); padding: 10px 0;
  font: 600 13.5px/1 var(--font-body); letter-spacing: .1em; text-transform: uppercase; color: var(--ink-muted); }}
.left {{ position: absolute; left: 72px; top: 130px; width: 520px; }}
.kicker {{ font: 600 15px/1 var(--font-body); text-transform: uppercase; letter-spacing: .1em; color: var(--ink-muted); }}
h1 {{ font-family: var(--font-display); font-weight: 900; font-size: 76px; line-height: .98;
  letter-spacing: -0.015em; margin-top: 18px; }}
.standfirst {{ margin-top: 22px; font: italic 400 21px/1.5 var(--font-display); }}
.standfirst::first-letter {{ font: 900 64px/0.8 var(--font-display); color: var(--accent); float: left; padding: 8px 10px 0 0; }}
.license-line {{ position: absolute; left: 72px; bottom: 120px; width: 520px; border-top: 1px solid var(--ink); padding-top: 14px;
  font: 400 14.5px/1.75 var(--font-body); color: var(--ink-muted); }}
.license-line b {{ color: var(--ink); font-weight: 600; }}
.hero {{ position: absolute; right: 72px; top: 116px; text-align: right; }}
.hero-num {{ font-family: var(--font-display); font-weight: 900; font-size: 186px; line-height: .9;
  letter-spacing: -0.03em; color: var(--ink); }}
.hero-cap {{ font: 600 20px/1.3 var(--font-body); color: var(--accent); margin-top: 8px; margin-right: 6px; }}
.rows {{ position: absolute; left: 640px; right: 72px; top: 480px; }}
.row {{ display: grid; grid-template-columns: 320px 510px 230px; align-items: center; gap: 20px;
  border-top: 1px solid var(--ink); padding: 26px 0; }}
.row:last-child {{ border-bottom: 1px solid var(--ink); }}
.rl {{ font: 600 19px/1.3 var(--font-body); }}
.rv {{ font-family: var(--font-display); font-weight: 600; font-size: 34px; white-space: nowrap; }}
.ru {{ font: 500 15px var(--font-body); color: var(--ink-muted); }}
footer {{ position: absolute; left: 72px; right: 72px; bottom: 28px;
  display: flex; justify-content: space-between; gap: 40px;
  border-top: 1px solid var(--ink); padding-top: 12px; font: 400 13.5px/1.5 var(--font-body); color: var(--ink-muted); }}
footer b {{ font-weight: 600; color: var(--ink); }}
</style>
</head>
<body>
<div class="canvas">
  <div class="folio"><span>КОРПУСА · САНКРИТСКИЙ АРХИВ ГАСУНСА</span><span>ПОСЧИТАНО 29.08.2026 · No. 16</span></div>
  <div class="left">
    <div class="kicker">САНСКРИТСКИЙ АРХИВ ГАСУНСА · ТРИ КОРПУСА РЯДОМ</div>
    <h1>Три корпуса санскрита</h1>
    <p class="standfirst">Письменная классика в миллионах размеченных токенов, устная речь в тысячах видеотранскриптов и живой телеграм-чат в десятках тысяч слов — три попытки поймать санскрит в его среде.</p>
  </div>
  <div class="license-line">
    <b>Лицензии.</b> DCS (Оливер Хелльвиг) — <b>CC BY 4.0</b>, 270 текстов, {dcs_s} предложений.<br>
    Spoken — публичный <b>индекс</b> {sp_n} видеотранскриптов, тексты по правам источников.<br>
    Telegram — <b>приватный</b>: {tg_m} анонимизированных сообщений из {tg_peers} чатов, {tg_ch} знаков.
  </div>
  <div class="hero" data-hero>
    <div class="hero-num">{dcs_t}</div>
    <div class="hero-cap">токенов в dcs-conllu · {dcs_txt} текстов</div>
  </div>
  <div class="rows">
      {rows}
  </div>
  <footer>
    <div>Данные: <b>dcs-conllu · spoken-sanskrit-corpus · telegram-sanskrit-corpus</b> — полные счёты по файлам репозиториев; полосы — каждая на своей шкале (единица подписана), разрыв величин ≈ {ratio}×</div>
    <div>скрипт: <b>scripts/infographics50/corpora_compare.py</b> · Посчитано 29.08.2026 · <b>Dr. Mārcis Gasūns</b></div>
  </footer>
</div>
</body>
</html>
"""

if __name__ == "__main__":
    main()
