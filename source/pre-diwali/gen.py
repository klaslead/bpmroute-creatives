"""Pre-Diwali 2026: five posters, each in feed (1080x1350) and story (1080x1920).
Run: python3 gen.py  -> writes html/<name>-<size>.html, then `node render.js` makes the JPEGs.
"""
import math, os, random

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'html')
os.makedirs(OUT, exist_ok=True)
MARK = open(os.path.join(HERE, 'mark.svg')).read().replace('<svg ', '<svg class="mk" ', 1)
FONTS = open(os.path.join(HERE, 'fonts', 'g.css')).read().replace('url(', 'url(../fonts/')

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
.hindi{font-family:"Tiro Devanagari Hindi",serif;font-size:46px;color:#ffd36e;margin-bottom:4px;text-shadow:0 0 30px rgba(255,180,60,.45)}
h1{font-size:%(h1)dpx;line-height:1;font-weight:800;letter-spacing:-4px}
h1 em{font-style:normal;background:linear-gradient(90deg,#ffe9a8,#ffb547 45%%,#ff5ecf);-webkit-background-clip:text;background-clip:text;color:transparent}
.copy{margin-top:30px}
.sub{margin-top:24px;font-size:34px;line-height:1.3;color:rgba(245,245,247,.72);max-width:900px}
footer{margin-top:44px;display:flex;justify-content:space-between;font-size:26px;color:rgba(245,245,247,.6)}
footer b{color:#f5f5f7;font-weight:600}
.glass{background:linear-gradient(160deg,rgba(255,255,255,.15),rgba(255,255,255,.03));border:1.5px solid rgba(255,255,255,.22);backdrop-filter:blur(40px) saturate(170%%);box-shadow:inset 0 1.5px 0 rgba(255,255,255,.35),inset 0 -1px 0 rgba(255,255,255,.06),0 40px 90px rgba(0,0,0,.55)}
"""

DEFS = """
<radialGradient id="fl" cx=".5" cy=".72" r=".7"><stop offset="0" stop-color="#fff"/><stop offset=".25" stop-color="#fff3c4"/><stop offset=".55" stop-color="#ffb547"/><stop offset=".85" stop-color="#ff5e7a"/><stop offset="1" stop-color="#ff5ecf" stop-opacity=".0"/></radialGradient>
<linearGradient id="gold" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ffe9a8"/><stop offset=".5" stop-color="#e2a33a"/><stop offset="1" stop-color="#7a4a0c"/></linearGradient>
<linearGradient id="brand" x1="0" x2="1"><stop offset="0" stop-color="#5ee7ff"/><stop offset=".5" stop-color="#9b7bff"/><stop offset="1" stop-color="#ff5ecf"/></linearGradient>
<filter id="glow" x="-100%" y="-100%" width="300%" height="300%"><feGaussianBlur stdDeviation="14"/></filter>
<filter id="soft" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="4"/></filter>
"""


def flame(x, y, h, w=None, glow=True):
    """Teardrop flame with its base at (x, y)."""
    w = w or h * 0.42
    d = (f'M{x} {y-h} C{x+w*.55} {y-h*.55} {x+w*.62} {y-h*.12} {x} {y} '
         f'C{x-w*.62} {y-h*.12} {x-w*.55} {y-h*.55} {x} {y-h}Z')
    g = f'<ellipse cx="{x}" cy="{y-h*.35}" rx="{w*1.1}" ry="{h*.7}" fill="#ffb547" opacity=".45" filter="url(#glow)"/>' if glow else ''
    core = (f'<path d="M{x} {y-h*.55} C{x+w*.22} {y-h*.32} {x+w*.24} {y-h*.08} {x} {y-h*.02} '
            f'C{x-w*.24} {y-h*.08} {x-w*.22} {y-h*.32} {x} {y-h*.55}Z" fill="#fff" opacity=".9"/>')
    return g + f'<path d="{d}" fill="url(#fl)"/>' + core


def diya(x, y, w):
    """Glass-and-gold diya bowl, top edge centred at (x, y)."""
    h = w * .34
    return (f'<path d="M{x-w/2} {y} Q{x} {y+h*1.9} {x+w/2} {y} Z" fill="url(#gold)"/>'
            f'<ellipse cx="{x}" cy="{y}" rx="{w/2}" ry="{h*.22}" fill="#3a2206" stroke="#ffe9a8" stroke-width="2" stroke-opacity=".6"/>'
            f'<path d="M{x-w*.36} {y+h*.35} Q{x} {y+h*1.15} {x+w*.36} {y+h*.35}" fill="none" stroke="#fff" stroke-opacity=".35" stroke-width="2" stroke-dasharray="2 9" stroke-linecap="round"/>')


def page(name, size, *, pill, hindi, h1, sub, art, blobs, h1px=104):
    h = SIZES[size]
    pt, pb = (80, 64) if size == 'feed' else (190, 230)
    css = BASE % dict(h=h, pt=pt, pb=pb, h1=h1px)
    blob_html = ''.join(
        f'<div class="blob" style="left:{x}px;top:{y if size=="feed" else int(y*1.42)}px;width:{s}px;height:{s}px;background:{c};opacity:{o}"></div>'
        for x, y, s, c, o in blobs)
    html = f"""<!doctype html><html><head><meta charset="utf-8"><style>{FONTS}{css}{art.get('css','')}</style></head><body class="{size}">
<div class="bg">{blob_html}{sparkles(24, 1080, (130, 720 if size=="feed" else 1150), len(name)+h)}</div>
<header>{MARK}<span>BPMroute</span><div class="pill">{pill}</div></header>
<main>{art['main'](size)}</main>
<section class="copy"><div class="hindi">{hindi}</div><h1>{h1}</h1><p class="sub">{sub}</p></section>
<footer><b>bpmroute.com</b><span>by EKSTAC33 Production</span></footer>
</body></html>"""
    with open(os.path.join(OUT, f'{name}-{size}.html'), 'w') as f:
        f.write(html)


def sparkles(n, w, yr, seed):
    random.seed(seed)
    out = []
    for _ in range(n):
        x, y, s = random.uniform(20, w-20), random.uniform(*yr), random.uniform(5, 16)
        c = random.choice(['#ffd36e', '#fff3c4', '#ff5ecf', '#5ee7ff', '#9b7bff'])
        out.append(f'<path d="M{x} {y-s}Q{x} {y} {x+s} {y}Q{x} {y} {x} {y+s}Q{x} {y} {x-s} {y}Q{x} {y} {x} {y-s}Z" fill="{c}" opacity="{random.uniform(.35,.9):.2f}"/>')
    return f'<svg width="1080" height="1920" style="position:absolute;left:0;top:0">{"".join(out)}</svg>'


# ---------------------------------------------------------------- 1. Diwali is loading
def p1_main(size):
    big = size == 'story'
    notes = [
        ('linear-gradient(135deg,#ffd36e,#f5a623)', '🪔', 'Diya & Co.', 'now', '12 diyas are out for delivery. ETA: before sunset.'),
        ('linear-gradient(135deg,#ff8fb1,#ff5ecf)', '🍬', 'Family group', '2m ago', 'Mom: "Who finished the kaju katli??" (3 new)'),
        ('linear-gradient(135deg,#5ee7ff,#9b7bff)', None, 'BPMroute', '5m ago', 'Your Diwali track is mastered ✨ Ready to light up every speaker.'),
    ]
    if big:
        notes.insert(2, ('linear-gradient(135deg,#9b7bff,#5ee7ff)', '🧹', 'Reminders', '1h ago', 'Clean the house. Then clean the mix. Then the hard drive.'))
    pct = 92
    r = 108
    circ = 2 * math.pi * r
    ring = f"""<svg width="280" height="280" viewBox="0 0 280 280"><defs>{DEFS}</defs>
<circle cx="140" cy="140" r="{r}" fill="none" stroke="rgba(255,255,255,.1)" stroke-width="22"/>
<circle cx="140" cy="140" r="{r}" fill="none" stroke="url(#brand)" stroke-width="22" stroke-linecap="round" stroke-dasharray="{circ*pct/100:.1f} {circ:.1f}" transform="rotate(-90 140 140)"/>
{flame(140, 168, 92)}
</svg>"""
    items = ''
    for bg, emo, app, t, msg in notes:
        icon = f'<div class="ic" style="background:{bg}">{emo}</div>' if emo else f'<div class="ic bp">{MARK}</div>'
        items += f'<div class="note glass">{icon}<div class="nt"><div class="nh"><b>{app}</b><span>{t}</span></div><div class="nm">{msg}</div></div></div>'
    return f"""<div class="lock"><div class="widget glass">{ring}<div class="wt"><div class="wl">DIWALI</div><div class="wn">{pct}%</div><div class="wd">1 day to go · Sun, 8 Nov</div></div></div>
<div class="stack">{items}</div></div>"""


P1_CSS = """
.lock{width:100%;display:flex;flex-direction:column;gap:22px}
.widget{display:flex;align-items:center;gap:34px;padding:26px 40px 26px 26px;border-radius:54px}
.wl{font-size:24px;letter-spacing:6px;font-weight:700;color:#ffd36e}
.wn{font-size:120px;font-weight:800;letter-spacing:-5px;line-height:1}
.wd{font-size:28px;color:rgba(245,245,247,.65);margin-top:6px}
.stack{display:flex;flex-direction:column;gap:14px}
.note{display:flex;gap:22px;align-items:center;padding:22px 26px;border-radius:38px}
.ic{flex:none;width:72px;height:72px;border-radius:20px;display:flex;align-items:center;justify-content:center;font-size:40px;font-family:"Noto Color Emoji"}
.ic.bp{background:none}.ic.bp .mk{width:72px;height:72px}
.nt{flex:1}
.feed .note{padding:15px 24px}.feed .widget{padding:14px 36px 14px 14px}.feed .lock{gap:14px}.feed .stack{gap:12px}.feed .wn{font-size:104px}
.nh{display:flex;justify-content:space-between;font-size:25px}
.nh span{color:rgba(245,245,247,.5)}
.nm{font-size:27px;line-height:1.3;color:rgba(245,245,247,.82);margin-top:4px}
"""

# ---------------------------------------------------------------- 2. The Pre-Diwali EP
TRACKS = [
    ('Safai', 'Clean Mix', '2:26'),
    ('Rangoli', 'Arrangement', '3:08'),
    ('Mithai', 'Sweetened Master', '2:54'),
    ('Diya', 'Lit Version', '3:33'),
    ('Patakha', 'Green Edit, no smoke', '0:08'),
]


def p2_main(size):
    random.seed(4)
    cover_art = []
    # cover: concentric rangoli of waveform dots around a flame
    for ring, n, col in [(60, 12, '#ffd36e'), (92, 18, '#ff5ecf'), (124, 24, '#9b7bff'), (150, 30, '#5ee7ff')]:
        for k in range(n):
            a = 2 * math.pi * k / n
            L = 6 + 10 * abs(math.sin(k * 1.3 + ring))
            x1, y1 = 170 + (ring - L) * math.cos(a), 170 + (ring - L) * math.sin(a)
            x2, y2 = 170 + (ring + L) * math.cos(a), 170 + (ring + L) * math.sin(a)
            cover_art.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{col}" stroke-width="6" stroke-linecap="round"/>')
    cover = f"""<svg viewBox="0 0 340 340" class="cov"><defs>{DEFS}<radialGradient id="cbg"><stop offset="0" stop-color="#3a1d05"/><stop offset="1" stop-color="#0a0508"/></radialGradient></defs>
<rect width="340" height="340" rx="34" fill="url(#cbg)"/>{''.join(cover_art)}{flame(170, 198, 74)}
<text x="22" y="318" font-size="17" font-weight="700" letter-spacing="3" fill="#ffd36e">PRE-DIWALI EP</text></svg>"""
    rows = ''
    for i, (t, v, d) in enumerate(TRACKS, 1):
        playing = i == 4
        eq = '<span class="eq"><i></i><i></i><i></i><i></i></span>' if playing else f'<span class="n">{i}</span>'
        rows += f'<div class="row{" on" if playing else ""}">{eq}<div class="tt"><b>{t}</b><span>{v}</span></div><span class="d">{d}</span></div>'
    extra = '<div class="np glass"><div class="bar"><div></div></div><div class="tm"><span>1:47</span><span>−1:46</span></div><div class="ctl">⏮&nbsp;&nbsp;&nbsp;❚❚&nbsp;&nbsp;&nbsp;⏭</div></div>' if size == 'story' else ''
    return f"""<div class="ep glass"><div class="top">{cover}<div class="meta"><div class="lab">ALBUM · 2026</div><div class="ttl">Pre-Diwali</div><div class="art">BPMroute &amp; Your Family</div><div class="gen">Festive · 5 songs · 14 min</div><div class="btns"><span class="play">▶&nbsp; Play</span><span class="sh">⤨ Shuffle</span></div></div></div>
<div class="list">{rows}</div></div>{extra}"""


P2_CSS = """
main{flex-direction:column;gap:22px}
.ep{width:100%;border-radius:56px;padding:34px}
.top{display:flex;gap:34px;align-items:center}
.cov{width:300px;height:300px;flex:none;border-radius:30px;box-shadow:0 30px 60px rgba(255,150,40,.25)}
.lab{font-size:21px;letter-spacing:4px;color:rgba(245,245,247,.5);font-weight:600}
.ttl{font-size:68px;font-weight:800;letter-spacing:-2.5px;margin-top:6px;line-height:1}
.art{font-size:28px;color:#ffd36e;margin-top:10px;font-weight:600}
.gen{font-size:23px;color:rgba(245,245,247,.5);margin-top:8px}
.btns{display:flex;gap:14px;margin-top:22px}
.btns span{font-size:24px;font-weight:700;padding:14px 26px;border-radius:999px}
.play{background:#f5f5f7;color:#000}
.sh{background:rgba(255,255,255,.1);border:1px solid rgba(255,255,255,.2)}
.list{margin-top:22px}
.row{display:flex;align-items:center;gap:24px;padding:15px 14px;border-top:1px solid rgba(255,255,255,.09);border-radius:18px}
.row .n{width:40px;text-align:center;font-size:26px;color:rgba(245,245,247,.45)}
.tt{flex:1;display:flex;flex-direction:column}
.tt b{font-size:30px;font-weight:600}
.tt span{font-size:22px;color:rgba(245,245,247,.5)}
.row .d{font-size:24px;color:rgba(245,245,247,.45)}
.row.on{background:rgba(255,211,110,.1);border-top-color:transparent}
.row.on b{color:#ffd36e}
.eq{width:40px;height:32px;display:flex;align-items:flex-end;gap:4px;justify-content:center}
.eq i{width:6px;border-radius:3px;background:#ffd36e}
.eq i:nth-child(1){height:40%}.eq i:nth-child(2){height:100%}.eq i:nth-child(3){height:65%}.eq i:nth-child(4){height:85%}
.feed .ep{padding:26px 30px}.feed .cov{width:220px;height:220px}.feed .ttl{font-size:60px}.feed .btns{margin-top:16px}
.feed .list{margin-top:12px}.feed .row{padding:8px 14px}.feed .tt b{font-size:28px}.feed .tt span{font-size:20px}
.np{width:100%;border-radius:44px;padding:30px 40px}
.bar{height:8px;border-radius:4px;background:rgba(255,255,255,.15)}
.bar div{width:50%;height:100%;border-radius:4px;background:linear-gradient(90deg,#ffe9a8,#ffb547,#ff5ecf)}
.tm{display:flex;justify-content:space-between;font-size:20px;color:rgba(245,245,247,.5);margin-top:10px}
.ctl{text-align:center;font-size:44px;margin-top:6px;letter-spacing:4px}
"""

# ---------------------------------------------------------------- 3. Every fader up
CHANNELS = [('DIYAS', 0.96), ('MITHAI', 0.92), ('FAMILY', 1.0), ('RANGOLI', 0.9), ('BASS', 0.98)]


def p3_main(size):
    H = 640 if size == 'feed' else 980
    W = 920
    cw = W / len(CHANNELS)
    top, bot = 120, H - 90
    parts = []
    for i, (lab, lvl) in enumerate(CHANNELS):
        cx = cw * i + cw / 2
        # knob
        parts.append(f'<circle cx="{cx}" cy="56" r="30" fill="#141418" stroke="rgba(255,255,255,.25)" stroke-width="2"/>'
                     f'<line x1="{cx}" y1="56" x2="{cx+18*math.cos(-0.6)}" y2="{56+18*math.sin(-0.6)}" stroke="#ffd36e" stroke-width="5" stroke-linecap="round"/>')
        # meter: stacked led segments, drawn like flames getting hotter
        segs = 22
        mx = cx + 46
        for s in range(segs):
            y = bot - (s + 1) * (bot - top) / segs
            on = s / segs < lvl
            c = '#5ee7ff' if s < 9 else ('#9b7bff' if s < 15 else ('#ffb547' if s < 19 else '#ff5ecf'))
            parts.append(f'<rect x="{mx-6}" y="{y+3:.1f}" width="12" height="{(bot-top)/segs-6:.1f}" rx="4" fill="{c}" opacity="{1 if on else .12}"/>')
        # track
        parts.append(f'<rect x="{cx-7}" y="{top}" width="14" height="{bot-top}" rx="7" fill="#050507" stroke="rgba(255,255,255,.18)"/>')
        for t in range(11):
            ty = top + t * (bot - top) / 10
            parts.append(f'<line x1="{cx-34}" y1="{ty}" x2="{cx-20}" y2="{ty}" stroke="rgba(255,255,255,.25)" stroke-width="2"/>')
        # fader cap = a diya, flame lit at max
        fy = bot - lvl * (bot - top)
        parts.append(f'<rect x="{cx-7}" y="{fy}" width="14" height="{bot-fy}" rx="7" fill="url(#brand)" opacity=".85"/>')
        parts.append(diya(cx, fy + 8, 92))
        parts.append(flame(cx, fy + 4, 70 if lvl > .95 else 56))
        parts.append(f'<text x="{cx}" y="{H-36}" text-anchor="middle" font-size="24" font-weight="700" letter-spacing="3" fill="rgba(245,245,247,.8)">{lab}</text>')
    return f"""<div class="desk glass"><svg width="{W}" height="{H}" viewBox="0 0 {W} {H}"><defs>{DEFS}</defs>{''.join(parts)}</svg></div>"""


P3_CSS = """.desk{border-radius:56px;padding:20px 0;width:100%;display:flex;justify-content:center}"""

# ---------------------------------------------------------------- 4. Louder than crackers
def burst(cx, cy, R, n, cols, seed):
    random.seed(seed)
    out = [f'<circle cx="{cx}" cy="{cy}" r="{R*.5}" fill="{cols[0]}" opacity=".18" filter="url(#glow)"/>']
    for k in range(n):
        a = 2 * math.pi * k / n
        amp = .45 + .55 * abs(math.sin(k * .7 + seed)) * random.uniform(.7, 1)
        r1, r2 = R * .18, R * amp
        c = cols[k % len(cols)]
        x1, y1, x2, y2 = cx + r1 * math.cos(a), cy + r1 * math.sin(a), cx + r2 * math.cos(a), cy + r2 * math.sin(a)
        out.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{c}" stroke-width="{5 if k%2 else 7}" stroke-linecap="round"/>')
        out.append(f'<circle cx="{cx+(r2+16)*math.cos(a):.1f}" cy="{cy+(r2+16)*math.sin(a):.1f}" r="4" fill="{c}"/>')
    return ''.join(out)


def p4_main(size):
    H = 660 if size == 'feed' else 950
    sky = ''
    if size == 'feed':
        sky += burst(300, 260, 220, 56, ['#ffd36e', '#ffb547', '#fff3c4'], 1)
        sky += burst(720, 200, 170, 44, ['#ff5ecf', '#9b7bff'], 2)
        sky += burst(780, 470, 120, 36, ['#5ee7ff', '#9b7bff'], 3)
    else:
        sky += burst(330, 300, 250, 60, ['#ffd36e', '#ffb547', '#fff3c4'], 1)
        sky += burst(760, 230, 180, 48, ['#ff5ecf', '#9b7bff'], 2)
        sky += burst(720, 620, 200, 52, ['#5ee7ff', '#9b7bff'], 3)
        sky += burst(260, 720, 120, 36, ['#ff5ecf', '#ffd36e'], 4)
    # skyline: rooftops lit with diyas + a speaker stack instead of a cracker
    random.seed(9)
    ground = H - 120
    x, roofs = -120, []
    while x < 1080:
        w = random.randint(70, 150)
        h = random.randint(50, 170)
        roofs.append(f'<rect x="{x}" y="{ground-h}" width="{w-6}" height="{h+130}" rx="10" fill="#0c0b10" stroke="rgba(255,255,255,.08)"/>')
        for wx in range(x + 14, x + w - 20, 30):
            for wy in range(ground - h + 18, ground, 34):
                if random.random() < .45:
                    roofs.append(f'<rect x="{wx}" y="{wy}" width="12" height="16" rx="3" fill="#ffd36e" opacity="{random.uniform(.4,.95):.2f}"/>')
        for dx in range(x + 18, x + w - 18, 34):
            roofs.append(flame(dx, ground - h - 2, 16, glow=False))
        x += w
    # speaker on the tallest roof, sending the waves up
    sp = (f'<g transform="translate(470 {ground-250})"><rect x="0" y="0" width="120" height="170" rx="18" fill="#141418" stroke="url(#brand)" stroke-width="3"/>'
          f'<circle cx="60" cy="58" r="30" fill="#050507" stroke="rgba(255,255,255,.3)" stroke-width="3"/><circle cx="60" cy="58" r="11" fill="url(#brand)"/>'
          f'<circle cx="60" cy="128" r="18" fill="#050507" stroke="rgba(255,255,255,.3)" stroke-width="3"/>'
          + ''.join(f'<path d="M{60-r} {-14-r*.2} Q60 {-14-r*.9} {60+r} {-14-r*.2}" fill="none" stroke="url(#brand)" stroke-width="5" stroke-linecap="round" opacity="{1-r/170:.2f}"/>' for r in (40, 75, 110, 145))
          + '</g>')
    return f"""<svg width="1080" height="{H}" viewBox="-40 0 1000 {H}" style="margin:0 -80px;flex:none;overflow:visible"><defs>{DEFS}</defs>{sky}{''.join(roofs)}{sp}<defs><linearGradient id="fade" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000"/></linearGradient></defs><rect x="-200" y="{H-230}" width="1400" height="232" fill="url(#fade)"/></svg>"""


# ---------------------------------------------------------------- 5. Turn up the lights
def p5_main(size):
    H = 590 if size == 'feed' else 1020
    n = 9
    W = 920
    base = H - 170
    labels = ['32', '64', '125', '250', '500', '1k', '2k', '4k', '16k']
    curve = [.55, .8, 1.0, .82, .6, .72, .9, .66, .45]
    parts = []
    # glass shelf
    parts.append(f'<rect x="0" y="{base+30}" width="{W}" height="34" rx="17" fill="rgba(255,255,255,.08)" stroke="rgba(255,255,255,.25)"/>')
    pts = []
    for i in range(n):
        x = 50 + i * (W - 100) / (n - 1)
        fh = 90 + curve[i] * (H * .52)
        parts.append(flame(x, base - 6, fh, w=62))
        parts.append(diya(x, base, 96))
        # reflection
        parts.append(f'<ellipse cx="{x}" cy="{base+90}" rx="40" ry="10" fill="#ffb547" opacity=".35" filter="url(#soft)"/>')
        parts.append(f'<text x="{x}" y="{base+128}" text-anchor="middle" font-size="22" font-weight="600" fill="rgba(245,245,247,.45)">{labels[i]}</text>')
        pts.append((x, base - 6 - fh - 26))
    # EQ curve over the flame tips
    d = f'M{pts[0][0]} {pts[0][1]}' + ''.join(
        f' C{(pts[i-1][0]+pts[i][0])/2} {pts[i-1][1]} {(pts[i-1][0]+pts[i][0])/2} {pts[i][1]} {pts[i][0]} {pts[i][1]}' for i in range(1, n))
    parts.append(f'<path d="{d}" fill="none" stroke="url(#brand)" stroke-width="5" stroke-linecap="round" stroke-dasharray="1 14" opacity=".9"/>')
    for x, y in pts:
        parts.append(f'<circle cx="{x}" cy="{y}" r="8" fill="#000" stroke="url(#brand)" stroke-width="4"/>')
    parts.append(f'<text x="{W}" y="{base+168}" text-anchor="end" font-size="20" letter-spacing="3" font-weight="600" fill="rgba(255,211,110,.6)">Hz · DIYA EQ · PRESET: DEEPAVALI</text>')
    return f"""<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" style="overflow:visible"><defs>{DEFS}</defs>{''.join(parts)}</svg>"""


POSTERS = [
    dict(name='pre-diwali-01-loading', pill='PRE-DIWALI', hindi='दिवाली आ रही है',
         h1='Diwali is <em>loading.</em>', sub='1 day to go. Get the house, the heart and your next release ready.',
         art={'main': p1_main, 'css': P1_CSS},
         blobs=[(-200, 160, 640, '#9b7bff', .4), (620, 60, 560, '#ffb547', .3), (300, 820, 600, '#ff5ecf', .28)]),
    dict(name='pre-diwali-02-ep', pill='NOW PLAYING', hindi='त्योहार का प्लेलिस्ट',
         h1='Now playing: <em>Diwali.</em>', sub='Five tracks, one festival, streaming in every home this week.',
         art={'main': p2_main, 'css': P2_CSS},
         blobs=[(-160, 80, 620, '#ffb547', .34), (640, 380, 600, '#ff5ecf', .3), (100, 900, 560, '#5ee7ff', .2)], h1px=96),
    dict(name='pre-diwali-03-faders', pill='SOUNDCHECK', hindi='रोशनी फुल वॉल्यूम पर',
         h1='Every fader <em>up.</em>', sub='Pre-Diwali soundcheck: lights, sweets, family and bass. All at max.',
         art={'main': p3_main, 'css': P3_CSS},
         blobs=[(-200, 260, 620, '#5ee7ff', .22), (560, 140, 640, '#ffb547', .32), (200, 760, 600, '#9b7bff', .32)]),
    dict(name='pre-diwali-04-louder', pill='GREEN DIWALI', hindi='पटाखे नहीं, संगीत',
         h1='Louder than <em>crackers.</em>', sub='Celebrate with sound, not smoke. Turn the music up and keep the sky clear.',
         art={'main': p4_main, 'bg': ''},
         blobs=[(-120, 0, 640, '#9b7bff', .3), (560, -60, 620, '#ff5ecf', .24), (240, 700, 600, '#ffb547', .2)], h1px=100),
    dict(name='pre-diwali-05-lights', pill='1 DAY TO GO', hindi='शुभ दीपावली',
         h1='Turn up <em>the lights.</em>', sub='May your home glow and your tracks hit every frequency.',
         art={'main': p5_main},
         blobs=[(-160, 300, 640, '#ffb547', .3), (600, 200, 560, '#ff5ecf', .24), (240, 880, 620, '#9b7bff', .26)]),
]

for i, p in enumerate(POSTERS):
    for size in SIZES:
        page(p['name'], size, **{k: v for k, v in p.items() if k != 'name'})
print('ok')
