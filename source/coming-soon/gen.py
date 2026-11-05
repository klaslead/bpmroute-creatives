import re,sys
mark=open('/tmp/claude-0/sitezip/assets/logo/bpmroute-mark.svg').read()
mark=re.sub(r'<title.*?</title>','',mark,flags=re.S)
mark=mark.replace('<svg ','<svg class="mk" ',1)
BASE='''<!doctype html><html><head><meta charset="utf-8"><style>
*{margin:0;box-sizing:border-box}
body{width:1080px;height:1350px;background:#000;font-family:-apple-system,"SF Pro Display","Helvetica Neue",Inter,Arial,sans-serif;color:#f5f5f7;overflow:hidden;position:relative}
.blob{position:absolute;border-radius:50%;filter:blur(130px)}
.top{position:absolute;top:72px;left:80px;right:80px;display:flex;align-items:center;gap:20px;z-index:5}
.mk{width:76px;height:76px}.top span{font-size:40px;font-weight:700;letter-spacing:-1px}
.pill{margin-left:auto;font-size:20px;font-weight:600;letter-spacing:3px;padding:12px 22px;border-radius:999px;background:rgba(255,255,255,.08);border:1px solid rgba(255,255,255,.22)}
.num{position:absolute;top:190px;left:80px;font-size:22px;letter-spacing:4px;color:rgba(255,255,255,.5);font-weight:600;z-index:5}
.art{position:absolute;left:0;right:0;top:230px;height:560px;display:flex;align-items:center;justify-content:center;z-index:2}
.glass{background:linear-gradient(160deg,rgba(255,255,255,.16),rgba(255,255,255,.035));border:1.5px solid rgba(255,255,255,.24);backdrop-filter:blur(40px) saturate(160%);box-shadow:inset 0 1px 0 rgba(255,255,255,.4),0 40px 80px rgba(0,0,0,.45)}
.copy{position:absolute;left:80px;right:80px;bottom:150px;z-index:5}
.kick{font-size:26px;font-weight:700;letter-spacing:4px;text-transform:uppercase;margin-bottom:22px}
h1{font-size:92px;line-height:1.02;font-weight:800;letter-spacing:-3px}
h1 em{font-style:normal;-webkit-background-clip:text;background-clip:text;color:transparent}
p{margin-top:26px;font-size:34px;line-height:1.38;color:rgba(245,245,247,.75)}
.foot{position:absolute;bottom:60px;left:80px;right:80px;display:flex;justify-content:space-between;font-size:24px;color:rgba(245,245,247,.55);z-index:5}
.foot b{color:#f5f5f7;font-weight:600}
</style><style>{{css}}</style></head><body>{{blobs}}
<div class="top">{{mark}}<span>BPMroute</span><div class="pill">COMING SOON</div></div>
<div class="num">{{num}} / 05</div>
<div class="art">{{art}}</div>
<div class="copy"><div class="kick" style="color:{{c1}}">{{kick}}</div><h1>{{h1}}</h1><p>{{p}}</p></div>
<div class="foot"><b>bpmroute.com</b><span>by EKSTAC33 Production</span></div></body></html>'''
def blobs(*b): return ''.join(f'<div class="blob" style="width:{w}px;height:{w}px;background:{c};left:{x}px;top:{y}px;opacity:{o}"></div>' for w,c,x,y,o in b)
P=[]
# 1 Distribution: orbit rings around a glass disc
dots=''.join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{c}"/>' for x,y,r,c in [(540,95,12,"#5ee7ff"),(860,300,10,"#9b7bff"),(250,420,14,"#ff5ecf"),(780,500,9,"#5ee7ff"),(190,180,8,"#9b7bff"),(930,150,7,"#ff5ecf")])
P.append(dict(num='01',kick='Distribution',c1='#5ee7ff',
 h1='One upload.<br><em style="background-image:linear-gradient(90deg,#5ee7ff,#9b7bff)">Every stage.</em>',
 p='Send your release to streaming platforms and stores worldwide, from a single dashboard.',
 blobs=blobs((700,'#5ee7ff',-200,150,.45),(600,'#9b7bff',600,450,.4)),css='',
 art=f'''<svg width="1080" height="560" viewBox="0 0 1080 560"><g fill="none" stroke-width="2">
<ellipse cx="540" cy="290" rx="420" ry="150" stroke="rgba(94,231,255,.5)" transform="rotate(-12 540 290)"/>
<ellipse cx="540" cy="290" rx="330" ry="230" stroke="rgba(155,123,255,.45)" transform="rotate(25 540 290)"/>
<ellipse cx="540" cy="290" rx="250" ry="250" stroke="rgba(255,255,255,.18)" stroke-dasharray="4 10"/></g>{dots}
<foreignObject x="400" y="150" width="280" height="280"><div xmlns="http://www.w3.org/1999/xhtml" class="glass" style="width:280px;height:280px;border-radius:50%;display:flex;align-items:center;justify-content:center"><svg width="120" height="120" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M12 16V4M6 10l6-6 6 6"/><path d="M4 20h16"/></svg></div></foreignObject></svg>'''))
# 2 AI mastering: waveform before/after + loudness meter
import math,random
random.seed(3)
def bars(x0,amp,col,n=34):
  s=''
  for i in range(n):
    h=amp*(0.3+0.7*abs(math.sin(i*0.55)))*(0.6+0.4*random.random())
    s+=f'<rect x="{x0+i*12}" y="{280-h/2}" width="7" height="{h}" rx="3.5" fill="{col}"/>'
  return s
P.append(dict(num='02',kick='AI Mastering',c1='#9b7bff',
 h1='Studio-grade sound.<br><em style="background-image:linear-gradient(90deg,#9b7bff,#ff5ecf)">In minutes.</em>',
 p='Upload a mix and get a loud, clear, release-ready master tuned for every platform.',
 blobs=blobs((650,'#9b7bff',-150,200,.5),(550,'#ff5ecf',650,300,.35)),css='',
 art=f'''<div class="glass" style="width:920px;height:440px;border-radius:48px;position:relative;overflow:hidden">
<svg width="920" height="440" viewBox="0 0 920 440"><text x="50" y="70" fill="rgba(255,255,255,.5)" font-size="22" font-weight="600" letter-spacing="3">YOUR MIX</text><text x="500" y="70" fill="#fff" font-size="22" font-weight="700" letter-spacing="3">MASTERED</text>
{bars(50,90,'rgba(255,255,255,.35)')}<path d="M460 120v320" stroke="rgba(255,255,255,.2)" stroke-width="2" stroke-dasharray="6 8"/>
<defs><linearGradient id="g2" x1="0" x2="1"><stop offset="0" stop-color="#9b7bff"/><stop offset="1" stop-color="#ff5ecf"/></linearGradient></defs>{bars(500,220,'url(#g2)')}
<text x="50" y="405" fill="rgba(255,255,255,.55)" font-size="22">-18 LUFS</text><text x="740" y="405" fill="#fff" font-size="22" font-weight="700">-9 LUFS</text></svg></div>'''))
# 3 Production: step sequencer grid
cols=['#ff5ecf','#ff9f5e','#9b7bff','#5ee7ff']
random.seed(7)
pads=''
for r in range(4):
  for c in range(8):
    on=random.random()<0.42 or (r==0 and c%4==0)
    st=f'background:{cols[r]};box-shadow:0 0 40px {cols[r]}99' if on else 'background:rgba(255,255,255,.06);border:1px solid rgba(255,255,255,.14)'
    pads+=f'<div style="width:92px;height:92px;border-radius:22px;{st}"></div>'
P.append(dict(num='03',kick='Production',c1='#ff5ecf',
 h1='Make the beat.<br><em style="background-image:linear-gradient(90deg,#ff5ecf,#ff9f5e)">Own the sound.</em>',
 p='Creator tools for producers: beats, stems, samples and sessions in one creative space.',
 blobs=blobs((650,'#ff5ecf',500,150,.4),(500,'#ff9f5e',-150,450,.3)),css='',
 art=f'''<div class="glass" style="padding:40px;border-radius:52px;display:grid;grid-template-columns:repeat(8,92px);gap:14px">{pads}</div>'''))
# 4 Analytics: rising bar chart in glass card
hs=[70,100,86,132,124,170,195,186,240,275]
bs=''.join(f'<rect x="{60+i*78}" y="{390-h}" width="48" height="{h}" rx="14" fill="url(#g4)" opacity="{0.45+i*0.055:.2f}"/>' for i,h in enumerate(hs))
P.append(dict(num='04',kick='Analytics &amp; royalties',c1='#5ee7ff',
 h1='Every stream.<br><em style="background-image:linear-gradient(90deg,#5ee7ff,#5effb1)">Every rupee.</em>',
 p='See where your fans listen and track your earnings clearly, all in real time.',
 blobs=blobs((650,'#5ee7ff',550,150,.38),(500,'#5effb1',-200,400,.25)),css='',
 art=f'''<div class="glass" style="width:920px;height:460px;border-radius:48px;position:relative">
<svg width="920" height="460" viewBox="0 0 920 460"><defs><linearGradient id="g4" x1="0" y1="1" x2="0" y2="0"><stop offset="0" stop-color="#5ee7ff"/><stop offset="1" stop-color="#5effb1"/></linearGradient></defs>
<text x="60" y="70" fill="rgba(255,255,255,.55)" font-size="22" font-weight="600" letter-spacing="3">MONTHLY LISTENERS</text>
<text x="860" y="74" text-anchor="end" fill="#5effb1" font-size="34" font-weight="800">▲ growing</text>{bs}

<line x1="60" y1="392" x2="860" y2="392" stroke="rgba(255,255,255,.18)" stroke-width="2"/></svg></div>'''))
# 5 Free tier: giant ₹0
P.append(dict(num='05',kick='Free plan',c1='#ff5ecf',
 h1='Start free.<br><em style="background-image:linear-gradient(90deg,#5ee7ff,#9b7bff,#ff5ecf)">Grow loud.</em>',
 p='No upfront cost to begin. Upgrade only when your music is ready to go further.',
 blobs=blobs((600,'#5ee7ff',-200,200,.38),(600,'#9b7bff',300,350,.35),(500,'#ff5ecf',650,100,.38)),css='',
 art='''<div class="glass" style="width:620px;height:460px;border-radius:64px;display:flex;flex-direction:column;align-items:center;justify-content:center;transform:rotate(-4deg)">
<div style="font-size:260px;font-weight:800;letter-spacing:-12px;line-height:1;background:linear-gradient(135deg,#fff,#c9c3ff 60%,#ff9ee3);-webkit-background-clip:text;color:transparent">₹0</div>
<div style="font-size:28px;font-weight:600;letter-spacing:6px;color:rgba(255,255,255,.7);margin-top:10px">TO GET STARTED</div></div>'''))
for d in P:
  d['mark']=mark
  h=BASE
  for k,v in d.items(): h=h.replace('{{'+k+'}}',v)
  open(f"poster-{d['num']}.html",'w').write(h)
