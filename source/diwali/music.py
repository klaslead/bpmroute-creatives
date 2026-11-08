"""Happy Diwali 2026 reel: original 20s soundtrack at 120 BPM, plus visual timing data.
Run: python3 music.py  -> out/music.wav and data.js (firework schedule + per-frame audio levels).
Everything is synthesised here, so there are no licensing issues.
"""
import json, os
import numpy as np
from scipy.signal import butter, sosfilt, fftconvolve

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'out')
os.makedirs(OUT, exist_ok=True)

SR, DUR, FPS = 44100, 20.0, 30
N = int(SR * DUR)
rng = np.random.default_rng(1108)
L = np.zeros(N); R = np.zeros(N)


def hz(note):
    names = {'C': 0, 'C#': 1, 'D': 2, 'D#': 3, 'E': 4, 'F': 5, 'F#': 6, 'G': 7, 'G#': 8, 'A': 9, 'A#': 10, 'B': 11}
    n, o = note[:-1], int(note[-1])
    return 440.0 * 2 ** ((names[n] + 12 * (o + 1) - 69) / 12)


def lp(x, f, o=2):
    return sosfilt(butter(o, f, 'low', fs=SR, output='sos'), x)


def hp(x, f, o=2):
    return sosfilt(butter(o, f, 'high', fs=SR, output='sos'), x)


def bp(x, lo, hi, o=2):
    return sosfilt(butter(o, [lo, hi], 'band', fs=SR, output='sos'), x)


def add(sig, t, gain=1.0, pan=0.0):
    i = int(t * SR)
    if i >= N:
        return
    sig = sig[:N - i]
    L[i:i + len(sig)] += sig * gain * np.sqrt(0.5 * (1 - pan))
    R[i:i + len(sig)] += sig * gain * np.sqrt(0.5 * (1 + pan))


def tt(d):
    return np.arange(int(d * SR)) / SR


# ---------- instruments ----------
def pluck(f, d=1.6, decay=0.997, buzz=0.35):
    """Karplus-Strong sitar-ish pluck with a little jawari buzz."""
    p = max(2, int(SR / f)); tot = int(d * SR)
    y = np.zeros(tot + p + 1)
    y[1:p + 1] = lp(rng.uniform(-1, 1, p), min(6000, f * 12))
    for s in range(p + 1, tot + p + 1, p):
        e = min(s + p, len(y))
        y[s:e] = decay * 0.5 * (y[s - p:e - p] + y[s - p - 1:e - p - 1])
    y = y[p + 1:]
    y = y + buzz * np.tanh(4 * y) * np.abs(y)
    y *= np.minimum(1, tt(d) * 400)
    return y / (np.abs(y).max() + 1e-9)


def bell(f, d=2.5):
    t = tt(d)
    s = sum(a * np.sin(2 * np.pi * f * m * t) * np.exp(-t * k) for m, a, k in
            [(1, 1, 1.6), (2.76, .5, 3), (5.4, .25, 5), (8.9, .12, 8)])
    return s * np.minimum(1, t * 800)


def kick(d=0.55, punch=1.0):
    t = tt(d)
    f = 48 + 140 * np.exp(-t * 28)
    s = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 6.5)
    s += punch * 0.4 * rng.uniform(-1, 1, len(t)) * np.exp(-t * 300)
    return np.tanh(1.6 * s)


def clap(d=0.35):
    t = tt(d)
    n = bp(rng.uniform(-1, 1, len(t)), 900, 4500)
    env = np.exp(-t * 18)
    for o in (0.0, 0.011, 0.022):
        env += 0.8 * np.exp(-np.maximum(0, t - o) * 140) * (t >= o)
    return n * env * 0.9


def hat(d=0.08, open_=False):
    t = tt(d if not open_ else 0.3)
    return hp(rng.uniform(-1, 1, len(t)), 7000) * np.exp(-t * (55 if not open_ else 12))


def tabla_na(f=540):
    t = tt(0.5)
    s = (np.sin(2 * np.pi * f * t) + .5 * np.sin(2 * np.pi * f * 2.02 * t) + .3 * np.sin(2 * np.pi * f * 3.01 * t)) * np.exp(-t * 9)
    s += 0.4 * bp(rng.uniform(-1, 1, len(t)), 2000, 6000) * np.exp(-t * 120)
    return s * .6


def tabla_ge():
    t = tt(0.7)
    f = 72 + 30 * (1 - np.exp(-t * 6))
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 4.5)


def saw(f, t, det=0.0):
    ph = (f * (1 + det)) * t
    return 2 * (ph - np.floor(ph + 0.5))


def pad(notes, d, cutoff=1800, att=0.4, rel=0.8):
    t = tt(d)
    s = sum(saw(hz(n), t, dt) for n in notes for dt in (-0.006, 0, 0.0065))
    s = lp(s, cutoff, 2) / (len(notes) * 3)
    env = np.minimum(1, t / att) * np.minimum(1, (d - t) / rel)
    return s * env


def bass(f, d):
    t = tt(d)
    s = np.sin(2 * np.pi * f * t) + 0.3 * np.sin(2 * np.pi * 2 * f * t)
    env = np.minimum(1, t * 200) * np.minimum(1, (d - t) * 30)
    return np.tanh(1.5 * s) * env


def boom(d=2.2, big=1.0):
    t = tt(d)
    n = lp(rng.uniform(-1, 1, len(t)), 180 + 120 * big, 2)
    body = n * np.exp(-t * (2.6 - .8 * big)) * 3
    thud = np.sin(2 * np.pi * np.cumsum(38 + 50 * np.exp(-t * 20)) / SR) * np.exp(-t * 5)
    crack = bp(rng.uniform(-1, 1, len(t)), 1500, 7000) * np.exp(-t * 60)
    return (body + thud * .9 + crack * .5) * big


def crackle(d=1.4, density=180):
    out = np.zeros(int(d * SR))
    for _ in range(int(density * d)):
        i = rng.integers(0, len(out) - 400)
        c = rng.uniform(-1, 1, 300) * np.exp(-np.arange(300) / 40)
        out[i:i + 300] += c * (1 - i / len(out)) * rng.uniform(.3, 1)
    return hp(out, 2500)


def whistle(d=0.85):
    t = tt(d)
    f = 1400 + 1900 * (t / d) ** 1.3
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.minimum(1, t * 8) * (1 - t / d) * .12


# ---------- arrangement ----------
B = 0.5  # one beat at 120 BPM
D_PENTA = ['D4', 'E4', 'F#4', 'A4', 'B4', 'D5', 'E5', 'F#5']

# Tanpura drone through the whole piece
t = tt(DUR)
drone = sum(a * saw(hz(n), t, d) for n, a, d in [('D2', .5, 0), ('A2', .35, .002), ('D3', .3, -.002), ('A3', .12, .001)])
drone = lp(drone, 900) * (0.6 + 0.4 * np.sin(2 * np.pi * 0.23 * t) ** 2)
drone_env = np.clip(t / 2.0, 0, 1) * np.where(t < 6, 1, 0.45) * np.clip((DUR - t) / 2.5, 0, 1)
add(drone * drone_env, 0, .16)

# Intro: shimmer + heartbeat
shim = hp(rng.uniform(-1, 1, int(2.2 * SR)), 6000) * np.linspace(0, 1, int(2.2 * SR)) ** 2
add(shim, 0, .05)
for x in (0.55, 0.8, 1.3, 1.55):
    add(kick(0.4, 0.2), x, .35 if x in (0.55, 1.3) else .22)
add(bell(hz('D6'), 3.5), 2.0, .35)
add(bell(hz('A6'), 3.0), 2.0, .18, .3)
add(boom(1.5, .45), 2.0, .5)

# Build: one pluck per diya, tabla groove
for k, n in enumerate(D_PENTA):
    add(pluck(hz(n), 1.6), 2.5 + 0.25 * k, .5, (k / 7 - .5) * .8)
for b in range(4, 12):
    add(tabla_ge(), b * B, .55 if b % 2 == 0 else .3)
    add(tabla_na(560 if b % 2 else 520), b * B + .25, .35, .2)
for k, x in enumerate(np.arange(4.5, 6.0, 0.125)):   # accelerating clap roll
    add(clap(.15), x, .12 + .3 * k / 12)
rs = int(2 * SR); rt = np.arange(rs) / rs
riser = rng.uniform(-1, 1, rs)
riser = (1 - rt) * lp(riser, 600) + rt * hp(riser, 1500)
riser += 0.25 * saw(1, np.cumsum(200 + 1200 * rt ** 2) / SR)
add(riser * rt ** 2.2, 4.0, .4)

# Drop 6-14: four bars, I-vi-IV-V
prog = [(['D3', 'F#3', 'A3', 'D4'], 'D2'), (['B2', 'D3', 'F#3', 'B3'], 'B1'),
        (['G2', 'B2', 'D3', 'G3'], 'G1'), (['A2', 'C#3', 'E3', 'A3'], 'A1')]
hook = [('A4', 0), ('D5', .5), ('F#5', .75), ('E5', 1.5), ('D5', 2), ('B4', 2.5), ('A4', 3), ('D5', 3.5)]
hook2 = [('F#5', 0), ('E5', .5), ('D5', .75), ('B4', 1.5), ('A4', 2), ('B4', 2.5), ('D5', 3), ('E5', 3.25), ('F#5', 3.5)]
for bar, (ch, root) in enumerate(prog):
    t0 = 6 + bar * 2
    add(pad(ch, 2.1, 2200), t0, .5)
    for b in range(4):
        x = t0 + b * B
        add(kick(), x, .95)
        add(bass(hz(root), .42), x + .02, .32)
        add(bass(hz(root), .2), x + .25, .2)
        add(hat(), x + .25, .12, .3)
        add(hat(), x + .125, .05, -.3)
        if b % 2:
            add(clap(), x, .45)
    for n, bt in (hook if bar % 2 == 0 else hook2):
        add(pluck(hz(n), 1.2), t0 + bt * B, .42, .15)
        add(pluck(hz(n) * 2, 0.6, .995), t0 + bt * B + .12, .1, -.4)
    add(tabla_na(600), t0 + 1.75, .3)
    add(tabla_na(640), t0 + 1.875, .3)
add(hat(open_=True), 13.5, .15)

# Outro 14-20
add(kick(0.9), 14.0, 1.0)
add(pad(['G2', 'B2', 'D3', 'G3', 'B3'], 2.2, 2600), 14.0, .55)
add(pad(['A2', 'C#3', 'E3', 'A3', 'E4'], 2.2, 2400), 16.0, .5)
add(pad(['D3', 'F#3', 'A3', 'D4', 'F#4'], 4.0, 2000, rel=3.0), 18.0, .5)
add(bass(hz('G1'), 2), 14.0, .25); add(bass(hz('A1'), 2), 16.0, .22); add(bass(hz('D2'), 2), 18.0, .2)
for k, n in enumerate(['D5', 'B4', 'A4', 'F#4', 'E4', 'D4']):
    add(pluck(hz(n), 1.8), 14.5 + k * 0.5, .38, (k % 2 - .5) * .6)
add(bell(hz('D6'), 4), 15.0, .3)
add(bell(hz('F#6'), 4), 15.5, .14, -.4)
add(bell(hz('A6'), 4), 16.0, .12, .4)
add(pluck(hz('D4'), 3, .999), 18.0, .45)

# Fireworks: explosion time, x, y, type, size. Shared with the visuals through data.js.
FW = [
    (6.0, 540, 720, 'peony', 1.4), (6.5, 230, 520, 'ring', 1.0), (7.0, 860, 470, 'peony', 1.0),
    (7.5, 300, 1180, 'willow', 1.0), (8.0, 780, 1250, 'peony', 1.1), (8.75, 170, 330, 'ring', .8),
    (9.0, 900, 860, 'willow', 1.0), (9.5, 520, 360, 'peony', 1.0), (10.0, 220, 900, 'crossette', 1.0),
    (11.0, 880, 340, 'peony', .9), (12.0, 200, 300, 'willow', .9), (12.5, 900, 1500, 'ring', .9),
    (13.0, 150, 1450, 'peony', .9), (13.5, 870, 330, 'crossette', .9),
    (14.0, 540, 960, 'pulse', 1.6), (14.0, 200, 420, 'willow', 1.2), (14.0, 880, 420, 'willow', 1.2),
    (14.5, 250, 1350, 'peony', 1.0), (14.75, 830, 1380, 'peony', 1.0),
    (15.5, 180, 300, 'ring', .8), (16.25, 900, 260, 'peony', .8), (17.0, 160, 1430, 'willow', .9),
    (17.75, 920, 1480, 'peony', .8), (18.5, 540, 260, 'willow', .9),
]
for (x, px, py, kind, size) in FW:
    pan = (px / 1080 - .5) * 1.2
    add(boom(2.2, min(1.4, size)), x, .5 * size, pan)
    if kind in ('willow', 'crossette', 'pulse'):
        add(crackle(1.6), x + .35, .22, pan)
    if x - .85 > 6.0 and kind != 'pulse':
        add(whistle(), x - .85, .5, pan)

# ---------- mix ----------
mix = np.stack([L, R])
ir_t = np.arange(int(1.8 * SR)) / SR
ir = rng.uniform(-1, 1, (2, len(ir_t))) * np.exp(-ir_t * 3.2)
ir = np.stack([lp(i, 5000) for i in ir])
wet = np.stack([fftconvolve(mix[c], ir[c])[:N] for c in range(2)])
wet /= np.abs(wet).max()
mix = mix / np.abs(mix).max() + 0.22 * wet
fade = np.clip((DUR - np.arange(N) / SR) / 1.6, 0, 1)
mix *= fade
mix = np.tanh(1.8 * mix / np.abs(mix).max())
mix = mix / np.abs(mix).max() * 0.93

import wave
pcm = (mix.T * 32767).astype('<i2')
with wave.open(os.path.join(OUT, 'music.wav'), 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())

# ---------- per-frame levels for audio-reactive visuals ----------
mono = mix.mean(0)
frames = int(DUR * FPS); hop = SR // FPS; win = 4096
edges = np.geomspace(40, 12000, 49)
freqs = np.fft.rfftfreq(win, 1 / SR)
bands, rms, lows = [], [], []
w_ = np.hanning(win)
for f in range(frames):
    c = f * hop
    seg = mono[max(0, c - win // 2): c + win // 2]
    seg = np.pad(seg, (0, win - len(seg)))
    mag = np.abs(np.fft.rfft(seg * w_))
    bands.append([float(mag[(freqs >= a) & (freqs < b)].mean() if ((freqs >= a) & (freqs < b)).any() else 0) for a, b in zip(edges[:-1], edges[1:])])
    rms.append(float(np.sqrt((seg ** 2).mean())))
    lows.append(float(mag[(freqs > 30) & (freqs < 140)].mean()))
bands = np.log1p(np.array(bands) * 4)
bands = bands / (np.percentile(bands, 98, axis=0) + 1e-9)
bands = np.clip(bands, 0, 1.2)
rms = np.array(rms) / max(rms); lows = np.array(lows) / max(lows)
data = dict(
    fps=FPS, dur=DUR,
    fw=[dict(t=x, x=px, y=py, kind=k, size=s) for x, px, py, k, s in FW],
    bands=[[round(v, 3) for v in row] for row in bands.tolist()],
    rms=[round(v, 3) for v in rms.tolist()], low=[round(v, 3) for v in lows.tolist()],
)
with open(os.path.join(HERE, 'data.js'), 'w') as f:
    f.write('window.DATA=' + json.dumps(data, separators=(',', ':')) + ';')
print('ok', mix.shape, 'frames', frames)
