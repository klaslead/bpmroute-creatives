"""Bhoot Chaturdashi 2026 (7 Nov): one poster in feed (1080x1350) and story (1080x1920).
Run: python3 gen.py  -> writes html/<name>-<size>.html, then `node render.js` makes the JPEGs.
Same layout system as source/pre-diwali/gen.py.
"""
import math, os, random

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'html')
os.makedirs(OUT, exist_ok=True)
MARK = open(os.path.join(HERE, 'mark.svg')).read().replace('<svg ', '<svg class="mk" ', 1)
FONTS = open(os.path.join(HERE, 'fonts', 'g.css')).read().replace('url(', 'url(../fonts/')
NAME = 'bhoot-chaturdashi-2026'
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
main svg.art{width:100%%;height:100%%}
.bn{font-family:"Galada","Hind Siliguri",serif;font-size:58px;line-height:1.2;color:#ffd36e;margin-bottom:2px;text-shadow:0 0 30px rgba(255,180,60,.45)}
h1{font-size:%(h1)dpx;line-height:1;font-weight:800;letter-spacing:-4px}
h1 em{font-style:normal;background:linear-gradient(90deg,#5ee7ff,#9b7bff 45%%,#ff5ecf);-webkit-background-clip:text;background-clip:text;color:transparent}
.copy{margin-top:26px}
.sub{margin-top:24px;font-size:34px;line-height:1.3;color:rgba(245,245,247,.72);max-width:900px}
footer{margin-top:44px;display:flex;justify-content:space-between;font-size:26px;color:rgba(245,245,247,.6)}
footer b{color:#f5f5f7;font-weight:600}
.glass{background:linear-gradient(160deg,rgba(255,255,255,.15),rgba(255,255,255,.03));border:1.5px solid rgba(255,255,255,.22);backdrop-filter:blur(40px) saturate(170%%);box-shadow:inset 0 1.5px 0 rgba(255,255,255,.35),inset 0 -1px 0 rgba(255,255,255,.06),0 40px 90px rgba(0,0,0,.55)}
.chip{position:absolute;z-index:3;display:flex;align-items:center;gap:18px;padding:18px 28px 18px 18px;border-radius:999px;font-size:26px}
.chip .ic{width:58px;height:58px;border-radius:50%%;display:flex;align-items:flex-end;justify-content:center;gap:4px;padding-bottom:16px;background:linear-gradient(135deg,#5ee7ff,#9b7bff 55%%,#ff5ecf)}
.chip .ic i{width:5px;border-radius:3px;background:#fff}
.chip b{display:block;font-size:20px;letter-spacing:3px;color:rgba(245,245,247,.55);font-weight:600}
"""

DEFS = """
<radialGradient id="fl" cx=".5" cy=".72" r=".7"><stop offset="0" stop-color="#fff"/><stop offset=".25" stop-color="#fff3c4"/><stop offset=".55" stop-color="#ffb547"/><stop offset=".85" stop-color="#ff5e7a"/><stop offset="1" stop-color="#ff5ecf" stop-opacity=".0"/></radialGradient>
<linearGradient id="gold" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ffe9a8"/><stop offset=".5" stop-color="#e2a33a"/><stop offset="1" stop-color="#7a4a0c"/></linearGradient>
<linearGradient id="brand" x1="0" x2="1"><stop offset="0" stop-color="#5ee7ff"/><stop offset=".5" stop-color="#9b7bff"/><stop offset="1" stop-color="#ff5ecf"/></linearGradient>
<linearGradient id="ghost" x1="0" y1="0" x2=".35" y2="1"><stop offset="0" stop-color="#ffffff" stop-opacity=".97"/><stop offset=".55" stop-color="#e9e4ff" stop-opacity=".86"/><stop offset="1" stop-color="#b9a8ff" stop-opacity=".42"/></linearGradient>
<linearGradient id="rim" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#5ee7ff"/><stop offset=".5" stop-color="#ffffff" stop-opacity=".4"/><stop offset="1" stop-color="#ff5ecf"/></linearGradient>
<radialGradient id="moon" cx=".38" cy=".35" r=".75"><stop offset="0" stop-color="#fffbe8"/><stop offset=".6" stop-color="#ffe3a0"/><stop offset="1" stop-color="#d9a441"/></radialGradient>
<filter id="glow" x="-100%" y="-100%" width="300%" height="300%"><feGaussianBlur stdDeviation="14"/></filter>
<filter id="big" x="-100%" y="-100%" width="300%" height="300%"><feGaussianBlur stdDeviation="40"/></filter>
<filter id="soft" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="4"/></filter>
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


def ghost(cx, top, w):
    """Friendly liquid-glass ghost wearing BPMroute headphones."""
    h = w * 1.22
    l, r = cx - w / 2, cx + w / 2
    shoulder = top + w * .55
    bottom = top + h
    # wavy hem: 4 scallops
    n, seg = 4, w / 4
    hem = ''
    for i in range(n):
        x0 = r - i * seg
        hem += f' Q{x0 - seg*.25:.1f} {bottom + w*.09:.1f} {x0 - seg*.5:.1f} {bottom:.1f} Q{x0 - seg*.75:.1f} {bottom - w*.09:.1f} {x0 - seg:.1f} {bottom:.1f}'
    body = (f'M{l} {shoulder} C{l} {top - w*.02} {r} {top - w*.02} {r} {shoulder} '
            f'L{r + w*.04} {bottom}{hem} L{l} {shoulder}Z')
    # little arms
    ay = shoulder + w * .22
    arms = (f'<ellipse cx="{l - w*.02}" cy="{ay}" rx="{w*.13}" ry="{w*.065}" transform="rotate(-28 {l - w*.02} {ay})" fill="url(#ghost)" stroke="url(#rim)" stroke-width="2"/>'
            f'<ellipse cx="{r + w*.03}" cy="{ay - w*.06}" rx="{w*.13}" ry="{w*.065}" transform="rotate(-38 {r + w*.03} {ay - w*.06})" fill="url(#ghost)" stroke="url(#rim)" stroke-width="2"/>')
    ey = top + w * .5
    face = (f'<ellipse cx="{cx - w*.15}" cy="{ey}" rx="{w*.055}" ry="{w*.08}" fill="#14101f"/>'
            f'<ellipse cx="{cx + w*.15}" cy="{ey}" rx="{w*.055}" ry="{w*.08}" fill="#14101f"/>'
            f'<circle cx="{cx - w*.13}" cy="{ey - w*.03}" r="{w*.018}" fill="#fff"/>'
            f'<circle cx="{cx + w*.17}" cy="{ey - w*.03}" r="{w*.018}" fill="#fff"/>'
            f'<ellipse cx="{cx - w*.27}" cy="{ey + w*.1}" rx="{w*.06}" ry="{w*.03}" fill="#ff5ecf" opacity=".45"/>'
            f'<ellipse cx="{cx + w*.27}" cy="{ey + w*.1}" rx="{w*.06}" ry="{w*.03}" fill="#ff5ecf" opacity=".45"/>'
            f'<ellipse cx="{cx}" cy="{ey + w*.14}" rx="{w*.04}" ry="{w*.05}" fill="#14101f"/>')
    # headphones
    hy = top + w * .44
    band = (f'<path d="M{l - w*.04} {hy} C{l - w*.06} {top - w*.24} {r + w*.06} {top - w*.24} {r + w*.04} {hy}" '
            f'fill="none" stroke="url(#brand)" stroke-width="{w*.055}" stroke-linecap="round"/>')
    cups = ''
    for x in (l - w*.06, r + w*.06):
        cups += (f'<rect x="{x - w*.075}" y="{hy - w*.13}" width="{w*.15}" height="{w*.26}" rx="{w*.07}" fill="#1a1530" stroke="url(#rim)" stroke-width="3"/>'
                 f'<rect x="{x - w*.045}" y="{hy - w*.09}" width="{w*.09}" height="{w*.18}" rx="{w*.045}" fill="url(#brand)" opacity=".9"/>')
    shine = f'<path d="M{l + w*.14} {shoulder - w*.05} C{l + w*.16} {top + w*.16} {cx - w*.1} {top + w*.06} {cx} {top + w*.05}" fill="none" stroke="#fff" stroke-width="{w*.035}" stroke-linecap="round" opacity=".8"/>'
    halo = f'<ellipse cx="{cx}" cy="{top + h*.5}" rx="{w*.75}" ry="{h*.6}" fill="#9b7bff" opacity=".45" filter="url(#big)"/>'
    return (halo + arms + f'<path d="{body}" fill="url(#ghost)" stroke="url(#rim)" stroke-width="3"/>'
            + shine + face + band + cups)


def note(x, y, s, c, rot):
    return (f'<g transform="translate({x} {y}) rotate({rot}) scale({s})" fill="{c}" opacity=".9">'
            f'<ellipse cx="0" cy="22" rx="11" ry="8" transform="rotate(-20 0 22)"/><rect x="8" y="-14" width="4" height="36"/>'
            f'<path d="M8 -14 q18 6 16 24 q-4 -10 -16 -12z"/></g>')


def bat(x, y, s):
    return (f'<path transform="translate({x} {y}) scale({s})" fill="#0b0912" stroke="#9b7bff" stroke-opacity=".5" stroke-width="1.5" '
            f'd="M0 0 q-10 -12 -26 -10 q6 6 4 12 q-8 -2 -14 4 q14 0 20 6 q6 -4 10 -2 q4 -2 10 2 q6 -6 20 -6 q-6 -6 -14 -4 q-2 -6 4 -12 q-16 -2 -26 10 z"/>')


def art(size):
    W, H = (920, 760) if size == 'feed' else (920, 1060)
    g = []
    # moon
    mx, my = 760, 120
    g.append(f'<circle cx="{mx}" cy="{my}" r="120" fill="#ffd36e" opacity=".25" filter="url(#big)"/>')
    g.append(f'<circle cx="{mx}" cy="{my}" r="72" fill="url(#moon)"/>')
    for cx, cy, r in [(738, 98, 12), (782, 140, 8), (770, 92, 6)]:
        g.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#c99335" opacity=".35"/>')
    g.append(bat(150, 120, 1.2) + bat(240, 70, .8) + bat(640, 230, .7))
    # ghost
    gw = 270 if size == 'feed' else 330
    gtop = 150 if size == 'feed' else 230
    g.append(ghost(460, gtop, gw))
    # floating notes
    notes = [(250, gtop + 60, 1.3, '#5ee7ff', -12), (690, gtop + 120, 1.1, '#ff5ecf', 14), (215, gtop + 230, .9, '#9b7bff', 8), (720, gtop + 300, .8, '#ffd36e', -8)]
    g += [note(*n) for n in notes]
    # 14 prodip on a smile-shaped arc
    base = gtop + gw * 1.22 + (110 if size == 'feed' else 150)
    flames = []
    for i in range(14):
        t = i / 13
        x = 60 + t * 800
        y = base + 70 * (1 - (2 * t - 1) ** 2)
        fh = 58 + 14 * math.sin(i * 1.7) ** 2
        g.append(f'<ellipse cx="{x}" cy="{y + 26}" rx="30" ry="6" fill="#ffb547" opacity=".25" filter="url(#soft)"/>')
        flames.append(flame(x, y - 2, fh) + diya(x, y, 50))
    g += flames
    ly = base + 70 + 78
    g.append(f'<text x="460" y="{ly}" text-anchor="middle" font-size="22" font-weight="700" letter-spacing="5" fill="#ffd36e" opacity=".85">CHODDO PRODIP · 14 / 14 LIT · GHOST FILTER: ON</text>')
    return f'<svg class="art" viewBox="0 0 {W} {H}" preserveAspectRatio="xMidYMid meet"><defs>{DEFS}</defs>{"".join(g)}</svg>'


def sparkles(n, w, yr, seed):
    random.seed(seed)
    out = []
    for _ in range(n):
        x, y, s = random.uniform(20, w-20), random.uniform(*yr), random.uniform(4, 12)
        c = random.choice(['#fff3c4', '#5ee7ff', '#9b7bff', '#ff5ecf', '#ffffff'])
        out.append(f'<path d="M{x} {y-s}Q{x} {y} {x+s} {y}Q{x} {y} {x} {y+s}Q{x} {y} {x-s} {y}Q{x} {y} {x} {y-s}Z" fill="{c}" opacity="{random.uniform(.3,.85):.2f}"/>')
    return f'<svg width="1080" height="1920" style="position:absolute;left:0;top:0">{"".join(out)}</svg>'


def page(size):
    h = SIZES[size]
    pt, pb = (80, 64) if size == 'feed' else (190, 230)
    css = BASE % dict(h=h, pt=pt, pb=pb, h1=104)
    blobs = [(-200, 120, 640, '#9b7bff', .34), (600, 260, 600, '#5ee7ff', .16), (200, 820, 620, '#ff5ecf', .2), (620, -80, 420, '#ffb547', .16)]
    blob_html = ''.join(
        f'<div class="blob" style="left:{x}px;top:{y if size=="feed" else int(y*1.42)}px;width:{s}px;height:{s}px;background:{c};opacity:{o}"></div>'
        for x, y, s, c, o in blobs)
    chip = ''
    if size == 'story':
        chip = ('<div class="chip glass" style="left:80px;top:300px"><div class="ic"><i style="height:12px"></i><i style="height:22px"></i><i style="height:16px"></i><i style="height:26px"></i></div>'
                '<div><b>NOW HAUNTING</b>Your playlist</div></div>')
    html = f"""<!doctype html><html><head><meta charset="utf-8"><style>{FONTS}{css}</style></head><body class="{size}">
<div class="bg">{blob_html}{sparkles(30, 1080, (130, 760 if size=="feed" else 1200), 1314)}</div>
<header>{MARK}<span>BPMroute</span><div class="pill">BHOOT CHATURDASHI</div></header>
{chip}<main>{art(size)}</main>
<section class="copy"><div class="bn">শুভ ভূত চতুর্দশী</div><h1>Haunt every <em>playlist.</em></h1>
<p class="sub">Light all 14 prodip, keep the bhoots away, and let your music be the only thing that lingers.</p></section>
<footer><b>bpmroute.com</b><span>by EKSTAC33 Production</span></footer>
</body></html>"""
    with open(os.path.join(OUT, f'{NAME}-{size}.html'), 'w') as f:
        f.write(html)


if __name__ == '__main__':
    for s in SIZES:
        page(s)
