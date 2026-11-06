"""Dhanteras 2026 creative: "Buy gold. Go gold."
A golden record wrapped in a waveform rangoli, with a glass diya whose flame is a sound wave.
Run: python3 gen.py  -> writes feed.html (1080x1350) and story.html (1080x1920) next to this file.
"""
import math, os, random
HERE = os.path.dirname(os.path.abspath(__file__))
MARK = open(os.path.join(HERE, 'mark.svg')).read().replace('<svg ', '<svg class="mk" ', 1)

GOLD = ['#fff3c4', '#ffd36e', '#f5a623', '#c77b12']


def art(cx, cy, R=230):
    """Golden record + radial waveform rangoli + diya, centred on (cx, cy) in a 1080-wide svg."""
    random.seed(11)
    out = []
    # outer rangoli: radial waveform bars (two rings, alternating colours)
    n = 96
    for i in range(n):
        a = 2 * math.pi * i / n
        amp = 0.35 + 0.65 * abs(math.sin(i * 0.39)) * (0.55 + 0.45 * random.random())
        r1, r2 = R + 34, R + 34 + 26 + 78 * amp
        x1, y1 = cx + r1 * math.cos(a), cy + r1 * math.sin(a)
        x2, y2 = cx + r2 * math.cos(a), cy + r2 * math.sin(a)
        col = 'url(#gw)' if i % 2 == 0 else 'url(#pw)'
        out.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{col}" stroke-width="7" stroke-linecap="round" opacity="{0.55+0.45*amp:.2f}"/>')
    # rangoli petals (lotus) behind the bars
    petals = []
    for k in range(12):
        a = k * 30
        petals.append(f'<path d="M{cx} {cy-R-10} C{cx+58} {cy-R-70} {cx+40} {cy-R-135} {cx} {cy-R-168} C{cx-40} {cy-R-135} {cx-58} {cy-R-70} {cx} {cy-R-10}Z" transform="rotate({a} {cx} {cy})" fill="url(#petal)" stroke="rgba(255,211,110,.35)" stroke-width="1.5"/>')
    # rangoli dots ring
    dots = []
    for k in range(48):
        a = 2 * math.pi * k / 48 + 0.065
        rr = R + 185
        c = ['#ffd36e', '#ff5ecf', '#5ee7ff', '#9b7bff'][k % 4]
        dots.append(f'<circle cx="{cx+rr*math.cos(a):.1f}" cy="{cy+rr*math.sin(a):.1f}" r="{5 if k%2 else 7}" fill="{c}" opacity=".85"/>')
    # record grooves
    grooves = ''.join(
        f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="rgba(80,45,0,{0.18 if r%12 else 0.32})" stroke-width="1.6"/>'
        for r in range(96, R - 8, 6))
    # sparkles
    random.seed(4)
    spark = []
    for _ in range(38):
        x, y = random.uniform(40, 1040), random.uniform(190, cy + R + 220)
        if math.hypot(x - cx, y - cy) < R + 230: continue
        s = random.uniform(5, 15)
        spark.append(f'<path d="M{x:.0f} {y-s:.0f}Q{x:.0f} {y:.0f} {x+s:.0f} {y:.0f}Q{x:.0f} {y:.0f} {x:.0f} {y+s:.0f}Q{x:.0f} {y:.0f} {x-s:.0f} {y:.0f}Q{x:.0f} {y:.0f} {x:.0f} {y-s:.0f}Z" fill="#ffe7a3" opacity="{random.uniform(.35,.95):.2f}"/>')

    # diya: glass bowl sitting on the bottom edge of the record, flame = waveform
    dy = cy + R + 100
    diya = f'''
<g filter="url(#soft)"><ellipse cx="{cx}" cy="{dy-90}" rx="110" ry="120" fill="url(#halo)"/></g>
<path d="M{cx-170} {dy-38} Q{cx} {dy-60} {cx+170} {dy-38} Q{cx+150} {dy+60} {cx} {dy+70} Q{cx-150} {dy+60} {cx-170} {dy-38}Z" fill="rgba(14,8,2,.88)"/>
<path d="M{cx-170} {dy-38} Q{cx} {dy-60} {cx+170} {dy-38} Q{cx+150} {dy+60} {cx} {dy+70} Q{cx-150} {dy+60} {cx-170} {dy-38}Z" fill="url(#bowl)" stroke="rgba(255,236,180,.75)" stroke-width="2.5"/>
<path d="M{cx-150} {dy-30} Q{cx} {dy-48} {cx+150} {dy-30}" fill="none" stroke="rgba(255,255,255,.55)" stroke-width="3" stroke-linecap="round"/>
<path d="M{cx-120} {dy+12} Q{cx} {dy+40} {cx+120} {dy+12}" fill="none" stroke="rgba(255,211,110,.5)" stroke-width="2" stroke-dasharray="2 10" stroke-linecap="round"/>
<path d="M{cx} {dy-52} C{cx+44} {dy-90} {cx+36} {dy-130} {cx} {dy-185} C{cx-36} {dy-130} {cx-44} {dy-90} {cx} {dy-52}Z" fill="url(#flame)"/>
<path d="M{cx} {dy-62} C{cx+22} {dy-86} {cx+16} {dy-112} {cx} {dy-145} C{cx-16} {dy-112} {cx-22} {dy-86} {cx} {dy-62}Z" fill="#fff8e0"/>
<path d="M{cx-24} {dy-98} h7 l5 -18 l7 36 l7 -28 l5 14 h9" fill="none" stroke="#c77b12" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>
'''
    return f'''
<defs>
 <radialGradient id="disc" cx=".38" cy=".32" r=".8"><stop offset="0" stop-color="#fff3c4"/><stop offset=".35" stop-color="#ffd36e"/><stop offset=".75" stop-color="#e09a1f"/><stop offset="1" stop-color="#8a520a"/></radialGradient>
 <linearGradient id="sheen" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".45" stop-color="#fff" stop-opacity=".55"/><stop offset=".55" stop-color="#fff" stop-opacity="0"/></linearGradient>
 <linearGradient id="gw" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#fff3c4"/><stop offset="1" stop-color="#f5a623"/></linearGradient>
 <linearGradient id="pw" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#ff5ecf"/><stop offset="1" stop-color="#9b7bff"/></linearGradient>
 <linearGradient id="petal" x1="0" y1="1" x2="0" y2="0"><stop offset="0" stop-color="#ffd36e" stop-opacity=".22"/><stop offset="1" stop-color="#ff5ecf" stop-opacity=".04"/></linearGradient>
 <linearGradient id="bowl" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="rgba(255,236,180,.55)"/><stop offset=".5" stop-color="rgba(245,166,35,.35)"/><stop offset="1" stop-color="rgba(120,60,10,.55)"/></linearGradient>
 <linearGradient id="flame" x1="0" y1="1" x2="0" y2="0"><stop offset="0" stop-color="#ff5ecf"/><stop offset=".35" stop-color="#ff9f2e"/><stop offset="1" stop-color="#ffe27a"/></linearGradient>
 <radialGradient id="halo"><stop offset="0" stop-color="#ffb43c" stop-opacity=".85"/><stop offset="1" stop-color="#ffb43c" stop-opacity="0"/></radialGradient>
 <radialGradient id="glow"><stop offset="0" stop-color="#ffb43c" stop-opacity=".55"/><stop offset=".6" stop-color="#ff7a3c" stop-opacity=".12"/><stop offset="1" stop-color="#000" stop-opacity="0"/></radialGradient>
 <filter id="soft" x="-1" y="-1" width="3" height="3"><feGaussianBlur stdDeviation="22"/></filter>
</defs>
<circle cx="{cx}" cy="{cy}" r="{R+330}" fill="url(#glow)"/>
{''.join(spark)}
{''.join(petals)}
{''.join(dots)}
{''.join(out)}
<circle cx="{cx}" cy="{cy}" r="{R+8}" fill="#1a1205"/>
<circle cx="{cx}" cy="{cy}" r="{R}" fill="url(#disc)"/>
{grooves}
<circle cx="{cx}" cy="{cy}" r="{R}" fill="url(#sheen)" opacity=".7"/>
<circle cx="{cx}" cy="{cy}" r="{R}" fill="none" stroke="rgba(255,248,220,.8)" stroke-width="2"/>
<circle cx="{cx}" cy="{cy}" r="86" fill="#0b0b0f" stroke="rgba(255,211,110,.7)" stroke-width="2"/>
<text x="{cx}" y="{cy-14}" text-anchor="middle" fill="#ffd36e" font-size="17" font-weight="700" letter-spacing="3">BPMROUTE</text>
<text x="{cx}" y="{cy+16}" text-anchor="middle" fill="rgba(255,255,255,.7)" font-size="13" font-weight="600" letter-spacing="2.5">GOLD EDITION</text>
<text x="{cx}" y="{cy+40}" text-anchor="middle" fill="rgba(255,255,255,.45)" font-size="12" font-weight="600" letter-spacing="2">DHANTERAS · 2026</text>
{diya}
'''


CSS = '''
*{margin:0;box-sizing:border-box}
body{width:1080px;height:%dpx;background:#000;font-family:-apple-system,"SF Pro Display","Helvetica Neue",Inter,Arial,sans-serif;color:#f5f5f7;overflow:hidden;position:relative}
.blob{position:absolute;border-radius:50%%;filter:blur(140px)}
svg.art{position:absolute;left:0;top:0}
.top{position:absolute;top:72px;left:80px;right:80px;display:flex;align-items:center;gap:20px;z-index:5}
.mk{width:76px;height:76px}.top span{font-size:40px;font-weight:700;letter-spacing:-1px}
.pill{margin-left:auto;font-size:20px;font-weight:700;letter-spacing:3px;padding:12px 22px;border-radius:999px;color:#ffd36e;background:rgba(255,211,110,.08);border:1px solid rgba(255,211,110,.35);backdrop-filter:blur(20px)}
.copy{position:absolute;left:80px;right:80px;z-index:5}
.hindi{font-family:"Tiro Devanagari Hindi",serif;font-size:46px;color:#ffd36e;margin-bottom:6px;text-shadow:0 0 30px rgba(255,180,60,.45)}
h1{font-size:104px;line-height:1;font-weight:800;letter-spacing:-3.5px}
h1 em{font-style:normal;background:linear-gradient(90deg,#fff3c4,#ffd36e 35%%,#f5a623 65%%,#ff5ecf);-webkit-background-clip:text;background-clip:text;color:transparent}
p{margin-top:24px;font-size:32px;line-height:1.38;color:rgba(245,245,247,.75)}
.foot{position:absolute;bottom:60px;left:80px;right:80px;display:flex;justify-content:space-between;font-size:24px;color:rgba(245,245,247,.55);z-index:5}
.foot b{color:#f5f5f7;font-weight:600}
'''

COPY = '''<div class="hindi">शुभ धनतेरस</div>
<h1>Buy gold.<br><em>Go gold.</em></h1>
<p>This Dhanteras, invest in the asset that keeps giving back: your music. Release it, master it, own it.</p>'''


def page(h, cy, copy_top, R):
    return f'''<!doctype html><html><head><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Tiro+Devanagari+Hindi&display=swap" rel="stylesheet">
<style>{CSS % h}</style></head><body>
<div class="blob" style="width:700px;height:700px;background:#f5a623;left:190px;top:{cy-420}px;opacity:.28"></div>
<div class="blob" style="width:520px;height:520px;background:#ff5ecf;left:-260px;top:{cy+120}px;opacity:.22"></div>
<div class="blob" style="width:520px;height:520px;background:#9b7bff;right:-260px;top:{cy-380}px;opacity:.22"></div>
<svg class="art" width="1080" height="{h}" viewBox="0 0 1080 {h}">{art(540, cy, R)}</svg>
<div class="top">{MARK}<span>BPMroute</span><div class="pill">HAPPY DHANTERAS</div></div>
<div class="copy" style="top:{copy_top}px">{COPY}</div>
<div class="foot"><b>bpmroute.com</b><span>by EKSTAC33 Production</span></div>
</body></html>'''


open(os.path.join(HERE, 'feed.html'), 'w').write(page(1350, 455, 835, 158))
open(os.path.join(HERE, 'story.html'), 'w').write(page(1920, 760, 1300, 200))
print('ok')
