"""Chhath Puja 2026 (Usha Arghya, 16 Nov): one poster in feed (1080x1350) and story (1080x1920).
Run: python3 gen.py  -> writes html/<name>-<size>.html, then `node render.js` makes the JPEGs.
Same layout system as source/bhoot-chaturdashi/gen.py.
"""
import math, os, random

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'html')
os.makedirs(OUT, exist_ok=True)
MARK = open(os.path.join(HERE, 'mark.svg')).read().replace('<svg ', '<svg class="mk" ', 1)
FONTS = open(os.path.join(HERE, 'fonts', 'g.css')).read().replace('url(', 'url(../fonts/')
NAME = 'chhath-puja-2026'
SIZES = {'feed': 1350, 'story': 1920}

BASE = """
*{margin:0;padding:0;box-sizing:border-box}
html,body{background:#000}
body{width:1080px;height:%(h)dpx;font-family:-apple-system,"SF Pro Display","Helvetica Neue",Inter,Arial,sans-serif;color:#f5f5f7;overflow:hidden;position:relative;display:flex;flex-direction:column;padding:%(pt)dpx 80px %(pb)dpx}
.bg{position:absolute;inset:0;z-index:0;overflow:hidden}
.blob{position:absolute;border-radius:50%%;filter:blur(130px)}
header,main,section,footer{position:relative;z-index:2}
header{display:flex;align-items:center;gap:22px}
header .mk{width:76px;height:76px}
header span{font-size:40px;font-weight:700;letter-spacing:-1px}
.pill{margin-left:auto;font-size:21px;font-weight:600;letter-spacing:4px;padding:12px 24px;border-radius:999px;background:rgba(255,255,255,.07);border:1px solid rgba(255,211,110,.35);color:#ffd36e;backdrop-filter:blur(20px)}
main{flex:1;display:flex;align-items:center;justify-content:center;min-height:0}
main svg.art{width:100%%;height:100%%;overflow:visible}
.hi{display:inline-block;font-family:"Tiro Devanagari Hindi",serif;font-size:%(hi)dpx;line-height:1.25;padding:0 6px 4px 0;background:linear-gradient(100deg,#fff3c4 0%%,#ffd36e 30%%,#ffb547 60%%,#ff8a5e 85%%,#ff5ecf);-webkit-background-clip:text;background-clip:text;color:transparent;filter:drop-shadow(0 0 22px rgba(255,170,60,.45))}
h1{font-size:%(h1)dpx;line-height:1;font-weight:800;letter-spacing:-4px;margin-top:6px}
h1 em{font-style:normal;background:linear-gradient(90deg,#ffe9a8,#ffb547 40%%,#ff8a5e 70%%,#ff5ecf);-webkit-background-clip:text;background-clip:text;color:transparent}
.copy{margin-top:22px}
.sub{margin-top:24px;font-size:34px;line-height:1.3;color:rgba(245,245,247,.72);max-width:910px}
footer{margin-top:44px;display:flex;justify-content:space-between;font-size:26px;color:rgba(245,245,247,.6)}
footer b{color:#f5f5f7;font-weight:600}
.glass{background:linear-gradient(160deg,rgba(255,255,255,.15),rgba(255,255,255,.03));border:1.5px solid rgba(255,255,255,.22);backdrop-filter:blur(40px) saturate(170%%);box-shadow:inset 0 1.5px 0 rgba(255,255,255,.35),inset 0 -1px 0 rgba(255,255,255,.06),0 40px 90px rgba(0,0,0,.55)}
.chip{position:absolute;z-index:3;display:flex;align-items:center;gap:18px;padding:18px 28px 18px 18px;border-radius:999px;font-size:26px}
.chip .ic{width:58px;height:58px;border-radius:50%%;display:flex;align-items:flex-end;justify-content:center;gap:4px;padding-bottom:16px;background:linear-gradient(135deg,#ffe9a8,#ffb547 50%%,#ff5ecf)}
.chip .ic i{width:5px;border-radius:3px;background:#fff}
.chip b{display:block;font-size:20px;letter-spacing:3px;color:rgba(245,245,247,.55);font-weight:600}
"""

DEFS = """
<radialGradient id="fl" cx=".5" cy=".72" r=".7"><stop offset="0" stop-color="#fff"/><stop offset=".25" stop-color="#fff3c4"/><stop offset=".55" stop-color="#ffb547"/><stop offset=".85" stop-color="#ff5e7a"/><stop offset="1" stop-color="#ff5ecf" stop-opacity="0"/></radialGradient>
<linearGradient id="gold" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ffe9a8"/><stop offset=".5" stop-color="#e2a33a"/><stop offset="1" stop-color="#7a4a0c"/></linearGradient>
<radialGradient id="sun" cx=".42" cy=".38" r=".7"><stop offset="0" stop-color="#fffbe8"/><stop offset=".35" stop-color="#ffd36e"/><stop offset=".75" stop-color="#ff9a3c"/><stop offset="1" stop-color="#ff5e7a"/></radialGradient>
<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ff8a5e" stop-opacity="0"/><stop offset="1" stop-color="#ff8a5e" stop-opacity=".35"/></linearGradient>
<linearGradient id="water" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2a1a3a" stop-opacity=".9"/><stop offset="1" stop-color="#000" stop-opacity="0"/></linearGradient>
<linearGradient id="cane" x1="0" x2="1"><stop offset="0" stop-color="#1f5a2a"/><stop offset=".45" stop-color="#7fd36b"/><stop offset="1" stop-color="#2a6a30"/></linearGradient>
<linearGradient id="leaf" x1="0" x2="1"><stop offset="0" stop-color="#7fd36b" stop-opacity=".9"/><stop offset="1" stop-color="#2f7a3a" stop-opacity=".7"/></linearGradient>
<linearGradient id="soop" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#f3d18a"/><stop offset="1" stop-color="#9a6a24"/></linearGradient>
<linearGradient id="glassg" x1="0" y1="0" x2=".3" y2="1"><stop offset="0" stop-color="#fff" stop-opacity=".22"/><stop offset="1" stop-color="#fff" stop-opacity=".04"/></linearGradient>
<linearGradient id="rim" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#ffe9a8"/><stop offset=".5" stop-color="#ffffff" stop-opacity=".35"/><stop offset="1" stop-color="#ff5ecf"/></linearGradient>
<linearGradient id="hzl" x1="0" x2="1"><stop offset="0" stop-color="#ffd36e" stop-opacity="0"/><stop offset=".5" stop-color="#ffd36e" stop-opacity=".8"/><stop offset="1" stop-color="#ffd36e" stop-opacity="0"/></linearGradient>
<clipPath id="above"><rect x="0" y="0" width="920" height="%(hz)d"/></clipPath>
<filter id="glow" x="-100%%" y="-100%%" width="300%%" height="300%%"><feGaussianBlur stdDeviation="14"/></filter>
<filter id="big" x="-100%%" y="-100%%" width="300%%" height="300%%"><feGaussianBlur stdDeviation="40"/></filter>
<filter id="soft" x="-50%%" y="-50%%" width="200%%" height="200%%"><feGaussianBlur stdDeviation="4"/></filter>
"""


def flame(x, y, h, w=None):
    w = w or h * 0.42
    d = (f'M{x} {y-h} C{x+w*.55} {y-h*.55} {x+w*.62} {y-h*.12} {x} {y} '
         f'C{x-w*.62} {y-h*.12} {x-w*.55} {y-h*.55} {x} {y-h}Z')
    g = f'<ellipse cx="{x}" cy="{y-h*.35}" rx="{w*1.1}" ry="{h*.7}" fill="#ffb547" opacity=".45" filter="url(#glow)"/>'
    core = (f'<path d="M{x} {y-h*.55} C{x+w*.22} {y-h*.32} {x+w*.24} {y-h*.08} {x} {y-h*.02} '
            f'C{x-w*.24} {y-h*.08} {x-w*.22} {y-h*.32} {x} {y-h*.55}Z" fill="#fff" opacity=".9"/>')
    return g + f'<path d="{d}" fill="url(#fl)"/>' + core


def diya(x, y, w):
    h = w * .34
    return (f'<path d="M{x-w/2} {y} Q{x} {y+h*1.9} {x+w/2} {y} Z" fill="url(#gold)"/>'
            f'<ellipse cx="{x}" cy="{y}" rx="{w/2}" ry="{h*.22}" fill="#3a2206" stroke="#ffe9a8" stroke-width="2" stroke-opacity=".6"/>')


def sugarcane(x0, y0, x1, y1, bend, flip):
    """A sugarcane stalk from the ground (x0,y0) arching to (x1,y1), knots + leaves at top."""
    cx, cy = (x0 + x1) / 2 + bend, (y0 + y1) / 2
    out = [f'<path d="M{x0} {y0} Q{cx} {cy} {x1} {y1}" fill="none" stroke="url(#cane)" stroke-width="12" stroke-linecap="round"/>']
    for i in range(1, 9):
        t = i / 9
        x = (1-t)**2*x0 + 2*(1-t)*t*cx + t**2*x1
        y = (1-t)**2*y0 + 2*(1-t)*t*cy + t**2*y1
        out.append(f'<ellipse cx="{x:.1f}" cy="{y:.1f}" rx="10" ry="3" fill="#123a18" opacity=".8"/>')
    # leaves fanning from the tip
    for k, (ang, ln) in enumerate([(-75, 150), (-35, 165), (5, 130), (45, 140), (85, 120), (-115, 125)]):
        a = math.radians(ang * flip)
        ex, ey = x1 + math.sin(a) * ln, y1 - math.cos(a) * ln * .55 + ln * .25
        mx, my = x1 + math.sin(a) * ln * .5, y1 - math.cos(a) * ln * .9
        out.append(f'<path d="M{x1} {y1} Q{mx:.1f} {my-18:.1f} {ex:.1f} {ey:.1f} Q{mx:.1f} {my+8:.1f} {x1} {y1}Z" fill="url(#leaf)"/>')
    return ''.join(out)


def soop(cx, cy, w):
    """Bamboo soop (winnow) with fruits, thekua and a diya: the Arghya offering."""
    h = w * .55
    l, r = cx - w / 2, cx + w / 2
    body = f'M{l} {cy} Q{cx} {cy + h*1.15} {r} {cy} Q{r - w*.06} {cy - h*.32} {cx} {cy - h*.36} Q{l + w*.06} {cy - h*.32} {l} {cy}Z'
    weave = ''.join(f'<path d="M{l + w*.08 + i*w*.084:.1f} {cy - h*.28} Q{cx + (i-5)*w*.02:.1f} {cy + h*.2} {l + w*.08 + i*w*.084:.1f} {cy + h*.5}" stroke="#7a4f14" stroke-width="2" fill="none" opacity=".45"/>' for i in range(11))
    items = [
        f'<circle cx="{cx - w*.26}" cy="{cy - h*.12}" r="{w*.075}" fill="#ffb547"/>',          # orange
        f'<circle cx="{cx - w*.14}" cy="{cy - h*.2}" r="{w*.06}" fill="#e2c14a"/>',            # sweet lime
        f'<ellipse cx="{cx + w*.22}" cy="{cy - h*.14}" rx="{w*.1}" ry="{w*.05}" fill="#f2d44a" transform="rotate(-25 {cx + w*.22} {cy - h*.14})"/>',  # banana
        f'<ellipse cx="{cx + w*.27}" cy="{cy - h*.06}" rx="{w*.1}" ry="{w*.05}" fill="#e8c43c" transform="rotate(-15 {cx + w*.27} {cy - h*.06})"/>',
        f'<circle cx="{cx + w*.06}" cy="{cy - h*.22}" r="{w*.05}" fill="#c1782f" stroke="#ffe9a8" stroke-opacity=".5" stroke-width="2" stroke-dasharray="3 4"/>',  # thekua
        f'<circle cx="{cx - w*.02}" cy="{cy - h*.06}" r="{w*.05}" fill="#b56a28" stroke="#ffe9a8" stroke-opacity=".5" stroke-width="2" stroke-dasharray="3 4"/>',
    ]
    return (f'<ellipse cx="{cx}" cy="{cy + h*.35}" rx="{w*.6}" ry="{h*.22}" fill="#ffb547" opacity=".25" filter="url(#glow)"/>'
            f'<path d="{body}" fill="url(#soop)" stroke="#ffe9a8" stroke-opacity=".6" stroke-width="2"/>{weave}{"".join(items)}'
            + diya(cx + w*.02, cy + h*.06, w*.17) + flame(cx + w*.02, cy + h*.04, w*.16))


def art(size):
    W, H = (920, 760) if size == 'feed' else (920, 1080)
    hz = int(H * (.58 if size == 'feed' else .56))     # horizon (water line)
    g = []
    sx, sy, sr = 460, hz + 10, 150 if size == 'feed' else 180
    # sky glow
    g.append(f'<ellipse cx="{sx}" cy="{hz}" rx="{W*.55}" ry="{hz*.75}" fill="#ff8a5e" opacity=".22" filter="url(#big)"/>')
    g.append(f'<circle cx="{sx}" cy="{sy}" r="{sr*1.9}" fill="#ff9a3c" opacity=".35" filter="url(#big)"/>')
    g.append(f'<ellipse cx="{sx}" cy="{hz + 120}" rx="{W*.52}" ry="120" fill="#3a2350" opacity=".55" filter="url(#big)"/>')
    # equaliser rays around the sun (only above the horizon)
    rays = []
    random.seed(16)
    n = 64
    for i in range(n):
        a = math.pi + math.pi * i / (n - 1)
        L = 30 + 70 * abs(math.sin(i * .55)) * random.uniform(.6, 1)
        r0 = sr + 22
        x0, y0 = sx + math.cos(a) * r0, sy + math.sin(a) * r0
        x1, y1 = sx + math.cos(a) * (r0 + L), sy + math.sin(a) * (r0 + L)
        c = ['#ffe9a8', '#ffb547', '#ff8a5e', '#ff5ecf'][i % 4]
        rays.append(f'<line x1="{x0:.1f}" y1="{y0:.1f}" x2="{x1:.1f}" y2="{y1:.1f}" stroke="{c}" stroke-width="7" stroke-linecap="round" opacity=".85"/>')
    g.append(f'<g clip-path="url(#above)">{"".join(rays)}'
             f'<circle cx="{sx}" cy="{sy}" r="{sr}" fill="url(#sun)"/>'
             + ''.join(f'<circle cx="{sx}" cy="{sy}" r="{sr*k:.1f}" fill="none" stroke="#fff" stroke-opacity=".16" stroke-width="2"/>' for k in (.4, .52, .64, .76, .88))
             + '</g>')
    # water
    g.append(f'<line x1="60" y1="{hz}" x2="{W-60}" y2="{hz}" stroke="url(#hzl)" stroke-width="2.5"/>')
    # sun reflection as an audio waveform on the water
    for j in range(6):
        y = hz + 22 + j * 26
        amp = (1 - j / 7)
        wdt = (sr * 1.5) * amp + 40
        pts = []
        for k in range(61):
            t = k / 60
            x = sx - wdt + 2 * wdt * t
            yy = y + math.sin(t * 22 + j) * 5 * amp * math.sin(math.pi * t)
            pts.append(f'{x:.1f},{yy:.1f}')
        col = ['#ffe9a8', '#ffb547', '#ff8a5e', '#ff5ecf'][j % 4]
        g.append(f'<polyline points="{" ".join(pts)}" fill="none" stroke="{col}" stroke-width="{6 - j*.45:.1f}" stroke-linecap="round" opacity="{.85 - j*.07:.2f}"/>')
    # floating diyas on the water
    for x, yo, w in [(130, 70, 40), (250, 130, 34), (690, 120, 36), (800, 60, 40), (90, 190, 30), (840, 200, 30)]:
        y = hz + yo
        g.append(f'<ellipse cx="{x}" cy="{y + 12}" rx="{w*.7}" ry="5" fill="#ffb547" opacity=".35" filter="url(#soft)"/>')
        g.append(diya(x, y, w) + flame(x, y - 2, w * 1.05))
    # sugarcane arches either side
    ground = hz + (150 if size == 'feed' else 210)
    top = hz - (300 if size == 'feed' else 380)
    g.append(sugarcane(30, ground, 120, top + 30, -30, -1))
    g.append(sugarcane(60, ground, 170, top, -45, -1))
    g.append(sugarcane(890, ground, 800, top + 30, 30, 1))
    g.append(sugarcane(860, ground, 750, top, 45, 1))
    # soop with offerings, front centre (glass plate behind)
    sw = 300 if size == 'feed' else 340
    scy = H - (95 if size == 'feed' else 150)
    g.append(f'<rect x="{460 - sw*.72}" y="{scy - sw*.32}" width="{sw*1.44}" height="{sw*.62}" rx="{sw*.31}" fill="url(#glassg)" stroke="url(#rim)" stroke-width="1.5"/>')
    g.append(soop(460, scy, sw))
    return (f'<svg class="art" viewBox="0 0 {W} {H}" preserveAspectRatio="xMidYMid meet"><defs>{DEFS % dict(hz=hz)}</defs>{"".join(g)}</svg>')


def sparkles(n, w, yr, seed):
    random.seed(seed)
    out = []
    for _ in range(n):
        x, y, s = random.uniform(20, w-20), random.uniform(*yr), random.uniform(4, 11)
        c = random.choice(['#fff3c4', '#ffd36e', '#ff8a5e', '#ff5ecf', '#ffffff'])
        out.append(f'<path d="M{x} {y-s}Q{x} {y} {x+s} {y}Q{x} {y} {x} {y+s}Q{x} {y} {x-s} {y}Q{x} {y} {x} {y-s}Z" fill="{c}" opacity="{random.uniform(.3,.8):.2f}"/>')
    return f'<svg width="1080" height="1920" style="position:absolute;left:0;top:0">{"".join(out)}</svg>'


def page(size):
    h = SIZES[size]
    pt, pb = (80, 64) if size == 'feed' else (190, 230)
    css = BASE % dict(h=h, pt=pt, pb=pb, h1=104, hi=60)
    blobs = [(-200, 120, 640, '#ff8a5e', .26), (600, 200, 600, '#ffb547', .2), (200, 820, 620, '#ff5ecf', .18), (560, 860, 420, '#9b7bff', .14)]
    blob_html = ''.join(
        f'<div class="blob" style="left:{x}px;top:{y if size=="feed" else int(y*1.42)}px;width:{s}px;height:{s}px;background:{c};opacity:{o}"></div>'
        for x, y, s, c, o in blobs)
    chip = ''
    if size == 'story':
        chip = ('<div class="chip glass" style="left:80px;top:300px"><div class="ic"><i style="height:12px"></i><i style="height:22px"></i><i style="height:16px"></i><i style="height:26px"></i></div>'
                '<div><b>NOW RISING</b>Your next release</div></div>')
    html = f"""<!doctype html><html><head><meta charset="utf-8"><style>{FONTS}{css}</style></head><body class="{size}">
<div class="bg">{blob_html}{sparkles(26, 1080, (130, 520 if size=="feed" else 760), 1611)}</div>
<header>{MARK}<span>BPMroute</span><div class="pill">CHHATH PUJA</div></header>
{chip}<main>{art(size)}</main>
<section class="copy"><div class="hi">छठ पूजा की हार्दिक शुभकामनाएँ</div><h1>Rise with the <em>sun.</em></h1>
<p class="sub">As the ghats glow for Usha Arghya, here's to every artist whose sound is ready to rise.</p></section>
<footer><b>bpmroute.com</b><span>by EKSTAC33 Production</span></footer>
</body></html>"""
    with open(os.path.join(OUT, f'{NAME}-{size}.html'), 'w') as f:
        f.write(html)


if __name__ == '__main__':
    for s in SIZES:
        page(s)
