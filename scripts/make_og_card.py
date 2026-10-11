# coding=utf-8
"""Render the GitHub-lookalike social preview card (og-card.png, 1200x630)
for the gasyoun.github.io root page. One-shot generator; rerun after
editing the copy below. Requires headless Chrome (CHROME_BIN overrides).
Usage: python3 scripts/make_og_card.py
"""
import os, sys, subprocess

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

CHROME = os.environ.get('CHROME_BIN',
    '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome')
AVATAR = os.environ.get('OG_AVATAR', '/tmp/gasyoun-avatar.png')

TEMPLATE = u"""<!DOCTYPE html>
<html><head><meta charset="UTF-8">
<style>
html,body {{ margin:0; padding:0; }}
#card {{ width:1200px; height:630px; background:#ffffff; box-sizing:border-box;
 padding:64px 72px; display:flex; border-bottom:14px solid #1a3e6e;
 font-family:-apple-system,'Segoe UI',Helvetica,Arial,sans-serif; color:#24292f; }}
.left {{ flex:1; padding-right:48px; display:flex; flex-direction:column; }}
.owner {{ font-size:40px; color:#59636e; }}
.name {{ font-size:64px; font-weight:800; letter-spacing:-1px; }}
.desc {{ font-size:30px; color:#3d444d; margin-top:26px; line-height:1.45; }}
.sa {{ font-size:40px; color:#8b0000; margin-top:30px; line-height:1.5;
 font-family:'Devanagari Sangam MN','Noto Serif Devanagari',serif; }}
.stats {{ margin-top:auto; display:flex; gap:56px; font-size:26px; color:#59636e; }}
.stats b {{ color:#24292f; font-weight:600; margin-right:8px; }}
.avatar {{ width:200px; height:200px; border-radius:24px; margin-top:6px; }}
</style></head>
<body><div id="card">
 <div class="left">
  <div class="owner">gasyoun.github.io/<b style="color:#24292f">Rigveda</b></div>
  <div class="name">ऋग्वेदः — Rigveda</div>
  <div class="desc">All 1028 sūktas in Devanagari with IAST transliteration and
  Russian, German and English translations.</div>
  <div class="sa">अ॒ग्निमी॑ळे पु॒रोहि॑तं य॒ज्ञस्य॑ दे॒वमृ॒त्विज॑म् ।</div>
  <div class="stats">
   <span><b>1028</b>sūktas</span><span><b>10</b>maṇḍalas</span>
   <span><b>4</b>languages</span><span><b>RV 1.1–10.191</b></span>
  </div>
 </div>
 <img class="avatar" src="{avatar}">
</div></body></html>
"""

def main():
    out = 'og-card.png'
    html_path = '_og_card_tmp.html'
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(TEMPLATE.format(avatar='file://' + os.path.abspath(AVATAR)))
    if os.path.exists(out):
        os.remove(out)
    cmd = [CHROME, '--headless', '--disable-gpu', '--hide-scrollbars',
           '--window-size=1200,630', '--virtual-time-budget=4000',
           '--screenshot=%s' % out, 'file://%s' % os.path.abspath(html_path)]
    subprocess.run(cmd, capture_output=True, timeout=60,
                   encoding='utf-8', errors='replace')
    os.remove(html_path)
    if not os.path.exists(out) or os.path.getsize(out) == 0:
        print('CARD FAIL')
        return 1
    print('card written:', out, os.path.getsize(out), 'bytes')
    return 0

if __name__ == '__main__':
    sys.exit(main())
