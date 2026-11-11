"""Shubho Bhai Phonta 2026 reel: original 28 s soundtrack at 96 BPM, plus per-frame audio levels.
Run: python3 music.py  -> out/music.wav and data.js. Everything is synthesised here, so it is licence free.
Timeline (s): 0 conch + intro | 1.2-9 chant | 9 phonta drop hits, groove | 16.5 DROP "Shubho Bhai Phonta" | 22 logo outro.
"""
import json, os
import numpy as np
from scipy.signal import butter, sosfilt, fftconvolve

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'out'); os.makedirs(OUT, exist_ok=True)
SR, DUR, FPS = 44100, 28.0, 30
N = int(SR * DUR)
rng = np.random.default_rng(1111)
L = np.zeros(N); R = np.zeros(N)
B = 60 / 96          # one beat
HIT, DROP, OUTRO = 9.0, 16.5, 22.0


def hz(note):
    names = {'C': 0, 'C#': 1, 'D': 2, 'D#': 3, 'E': 4, 'F': 5, 'F#': 6, 'G': 7, 'G#': 8, 'A': 9, 'A#': 10, 'B': 11}
    return 440.0 * 2 ** ((names[note[:-1]] + 12 * (int(note[-1]) + 1) - 69) / 12)
def lp(x, f, o=2): return sosfilt(butter(o, f, 'low', fs=SR, output='sos'), x)
def hp(x, f, o=2): return sosfilt(butter(o, f, 'high', fs=SR, output='sos'), x)
def bp(x, lo, hi, o=2): return sosfilt(butter(o, [lo, hi], 'band', fs=SR, output='sos'), x)
def tt(d): return np.arange(int(d * SR)) / SR
def add(sig, t, gain=1.0, pan=0.0):
    i = int(t * SR)
    if i >= N: return
    sig = sig[:N - i]
    L[i:i + len(sig)] += sig * gain * np.sqrt(0.5 * (1 - pan))
    R[i:i + len(sig)] += sig * gain * np.sqrt(0.5 * (1 + pan))
def saw(f, t, det=0.0):
    ph = (f * (1 + det)) * t
    return 2 * (ph - np.floor(ph + 0.5))


def pluck(f, d=1.6, decay=0.997, buzz=0.35):
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
    s = sum(a * np.sin(2 * np.pi * f * m * t) * np.exp(-t * k) for m, a, k in [(1, 1, 1.6), (2.76, .5, 3), (5.4, .25, 5), (8.9, .12, 8)])
    return s * np.minimum(1, t * 800)
def kick(d=0.55, punch=1.0):
    t = tt(d); f = 46 + 130 * np.exp(-t * 26)
    s = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 6)
    s += punch * 0.4 * rng.uniform(-1, 1, len(t)) * np.exp(-t * 300)
    return np.tanh(1.6 * s)
def snap(d=0.3):
    t = tt(d); n = bp(rng.uniform(-1, 1, len(t)), 1200, 6000)
    return n * (np.exp(-t * 22) + .6 * np.exp(-t * 160))
def hat(d=0.08, open_=False):
    t = tt(d if not open_ else 0.3)
    return hp(rng.uniform(-1, 1, len(t)), 7000) * np.exp(-t * (55 if not open_ else 12))
def dhol_lo():
    t = tt(0.7); f = 70 + 40 * np.exp(-t * 10)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 5) + .2 * lp(rng.uniform(-1, 1, len(t)), 400) * np.exp(-t * 30)
def dhol_hi(f=380):
    t = tt(0.3)
    s = (np.sin(2 * np.pi * f * t) + .4 * np.sin(2 * np.pi * f * 2.1 * t)) * np.exp(-t * 16)
    return s * .7 + .4 * bp(rng.uniform(-1, 1, len(t)), 1500, 5000) * np.exp(-t * 90)
def pad(notes, d, cutoff=1800, att=0.5, rel=0.9):
    t = tt(d)
    s = sum(saw(hz(n), t, dt) for n in notes for dt in (-0.006, 0, 0.0065))
    s = lp(s, cutoff, 2) / (len(notes) * 3)
    return s * np.minimum(1, t / att) * np.minimum(1, np.maximum(0, d - t) / rel)
def bass(f, d):
    t = tt(d)
    s = np.sin(2 * np.pi * f * t) + 0.3 * np.sin(2 * np.pi * 2 * f * t)
    return np.tanh(1.5 * s) * np.minimum(1, t * 200) * np.minimum(1, (d - t) * 30)
def flute(f, d, vib=5.2):
    t = tt(d)
    fm = f * (1 + 0.006 * np.sin(2 * np.pi * vib * t) * np.minimum(1, t / .35))
    ph = 2 * np.pi * np.cumsum(fm) / SR
    s = np.sin(ph) + .22 * np.sin(2 * ph) + .08 * np.sin(3 * ph)
    s += .12 * bp(rng.uniform(-1, 1, len(t)), f * .8, min(f * 3, 15000))
    env = np.minimum(1, t / .08) * np.minimum(1, np.maximum(0, d - t) / .25)
    return s * env
def conch(d=2.4, f=hz('A#3')):
    """Shankha: brassy horn with a rising swell and breath."""
    t = tt(d)
    fm = f * (0.985 + 0.02 * np.minimum(1, t / .4)) * (1 + .004 * np.sin(2 * np.pi * 4.5 * t))
    ph = np.cumsum(fm) / SR
    s = 2 * (ph - np.floor(ph + .5))
    s = bp(s, 300, 2600) + .6 * bp(s, 900, 1300, 2)
    s += .25 * bp(rng.uniform(-1, 1, len(t)), 600, 3000)
    env = np.minimum(1, (t / .5) ** 1.5) * np.minimum(1, np.maximum(0, d - t) / .6)
    return np.tanh(2 * s) * env
def ulu(d=1.6, f=1050):
    """Soft ululation (ulu-dhvani): a fast tongue-trill warble."""
    t = tt(d)
    fm = f * (1 + .07 * np.sign(np.sin(2 * np.pi * 7.5 * t)) * .5 + .05 * np.sin(2 * np.pi * 7.5 * t))
    fm = lp(fm, 40)
    ph = 2 * np.pi * np.cumsum(fm) / SR
    s = np.sin(ph) + .3 * np.sin(2 * ph)
    am = .6 + .4 * np.abs(np.sin(2 * np.pi * 7.5 * t))
    return s * am * np.minimum(1, t / .15) * np.minimum(1, np.maximum(0, d - t) / .4)
def boom(d=2.2, big=1.0):
    t = tt(d)
    n = lp(rng.uniform(-1, 1, len(t)), 180 + 120 * big, 2)
    thud = np.sin(2 * np.pi * np.cumsum(38 + 50 * np.exp(-t * 20)) / SR) * np.exp(-t * 5)
    return (n * np.exp(-t * (2.6 - .8 * big)) * 3 + thud * .9) * big
def swell(d):
    t = tt(d); k = t / d
    n = rng.uniform(-1, 1, len(t))
    return ((1 - k) * lp(n, 700) + k * hp(n, 1500) + .25 * saw(1, np.cumsum(180 + 1100 * k ** 2) / SR)) * k ** 2.2
def chime_shimmer(d):
    out = np.zeros(int(d * SR))
    for k in range(int(d * 14)):
        x = rng.uniform(0, d - .6)
        b = bell(hz(rng.choice(['D6', 'E6', 'F#6', 'A6', 'B6', 'D7'])), .6)
        i = int(x * SR); out[i:i + len(b)] += b * rng.uniform(.2, .6)
    return out


# ---------- arrangement (D major pentatonic, Bhairavi-ish warmth) ----------
t = tt(DUR)
drone = sum(a * saw(hz(n), t, dd) for n, a, dd in [('D2', .5, 0), ('A2', .35, .002), ('D3', .3, -.002), ('A3', .12, .001)])
drone = lp(drone, 850) * (0.6 + 0.4 * np.sin(2 * np.pi * 0.21 * t) ** 2)
add(drone * np.clip(t / 2.0, 0, 1) * np.clip((DUR - t) / 2.5, 0, 1), 0, .15)

# Intro: conch call, bell, soft shimmer
add(conch(2.6), 0.0, .42, -.1)
add(bell(hz('D6'), 4), 0.9, .25, .2)
add(pad(['D3', 'A3', 'D4', 'F#4'], 8.2, 1300, att=2.0, rel=2.0), 0.8, .55)
# Chant bed: gentle flute phrases between the spoken lines
phr = [('A4', 0, 1.0), ('B4', 1.0, .5), ('D5', 1.5, 1.5), ('E5', 3.0, .75), ('D5', 3.75, .75), ('B4', 4.5, 1.6),
       ('A4', 6.2, .6), ('F#4', 6.8, .6), ('A4', 7.4, 1.2)]
for n, x, d in phr:
    add(flute(hz(n), d * B * 1.6), 1.3 + x * B * 1.6 * .62, .07, .25)
for k, x in enumerate([2.0, 4.6, 7.0]):
    add(pluck(hz(['D4', 'A4', 'F#4'][k]), 2.4, .999), x, .22, (k - 1) * .4)
add(swell(1.4), HIT - 1.4, .35)
add(chime_shimmer(1.2), HIT - 1.2, .06)

# HIT: the phonta lands
add(boom(2.4, 1.2), HIT, .7)
add(bell(hz('D5'), 4), HIT, .35); add(bell(hz('A5'), 4), HIT + .02, .2, .4)

# Groove HIT -> DROP (3 bars of 4)
prog1 = [(['D3', 'F#3', 'A3', 'D4'], 'D2'), (['B2', 'D3', 'F#3', 'B3'], 'B1'), (['G2', 'B2', 'D3', 'G3'], 'G1')]
hook = [('F#5', 0), ('E5', .5), ('D5', 1), ('A4', 1.5), ('B4', 2.5), ('D5', 3)]
for bar, (ch, root) in enumerate(prog1):
    t0 = HIT + bar * 4 * B
    add(pad(ch, 4 * B + .1, 1700), t0, .42)
    for b in range(4):
        x = t0 + b * B
        add(kick(), x, .75 if b % 2 == 0 else .45)
        add(bass(hz(root), B * .8), x + .02, .26)
        add(hat(), x + B / 2, .1, .3)
        if b % 2: add(snap(), x, .32)
        add(dhol_hi(400 if b % 2 else 360), x + B * .75, .16, -.3)
    for n, bt in hook:
        add(pluck(hz(n), 1.4), t0 + bt * B, .3, .15)
add(swell(2 * B * 2), DROP - 4 * B, .42)
for k, x in enumerate(np.arange(DROP - 2 * B, DROP, B / 4)):
    add(snap(.12), x, .08 + .25 * k / 8)

# DROP: full groove, conch + ulu
add(boom(2.6, 1.4), DROP, .8)
add(conch(2.2, hz('D4')), DROP + .05, .3, .2)
add(ulu(1.8), DROP + .3, .05, -.3); add(ulu(1.5, 1180), DROP + 2.6, .035, .35)
prog2 = [(['D3', 'F#3', 'A3', 'D4'], 'D2'), (['G2', 'B2', 'D3', 'G3'], 'G1'),
         (['A2', 'C#3', 'E3', 'A3'], 'A1')]
hook2 = [('A4', 0), ('D5', .5), ('F#5', .75), ('E5', 1.5), ('D5', 2), ('B4', 2.5), ('A4', 3), ('D5', 3.5)]
for bar, (ch, root) in enumerate(prog2):
    t0 = DROP + bar * 4 * B
    if t0 >= OUTRO: break
    add(pad(ch, 4 * B + .1, 2300), t0, .5)
    for b in range(4):
        x = t0 + b * B
        if x >= OUTRO - .05: break
        add(kick(), x, .95)
        add(dhol_lo(), x + B / 2, .35)
        add(bass(hz(root), B * .7), x + .02, .32); add(bass(hz(root), B * .3), x + B * .5, .2)
        add(hat(), x + B / 2, .12, .3); add(hat(), x + B / 4, .05, -.3)
        if b % 2: add(snap(), x, .45)
        add(dhol_hi(), x + B * .75, .2, -.2)
    for n, bt in hook2:
        if t0 + bt * B < OUTRO:
            add(pluck(hz(n), 1.2), t0 + bt * B, .38, .15)
            add(flute(hz(n) * 2, .3), t0 + bt * B, .04, -.3)
add(chime_shimmer(2.5), DROP, .05)

# OUTRO: logo hit and long resolve
add(kick(0.9), OUTRO, .9); add(boom(2.5, .8), OUTRO, .45)
add(pad(['D3', 'F#3', 'A3', 'D4', 'F#4', 'A4'], DUR - OUTRO, 2000, att=.05, rel=3.5), OUTRO, .55)
add(bass(hz('D2'), 3), OUTRO, .25)
for k, n in enumerate(['D5', 'B4', 'A4', 'F#4', 'E4', 'D4']):
    add(pluck(hz(n), 2.0), OUTRO + .4 + k * B * .75, .3, (k % 2 - .5) * .6)
add(bell(hz('D6'), 5), OUTRO + .1, .25); add(bell(hz('A6'), 5), OUTRO + .6, .12, .4)
add(flute(hz('D5'), 3.2), OUTRO + 2.2, .06)

# ---------- mix ----------
mix = np.stack([L, R])
ir_t = np.arange(int(2.0 * SR)) / SR
ir = rng.uniform(-1, 1, (2, len(ir_t))) * np.exp(-ir_t * 3.0)
ir = np.stack([lp(i, 5000) for i in ir])
wet = np.stack([fftconvolve(mix[c], ir[c])[:N] for c in range(2)])
mix = mix / np.abs(mix).max() + 0.25 * wet / np.abs(wet).max()
mix *= np.clip((DUR - np.arange(N) / SR) / 2.0, 0, 1)
mix = np.tanh(1.6 * mix / np.abs(mix).max())
mix = mix / np.abs(mix).max() * 0.9
np.save(os.path.join(OUT, 'music.npy'), mix.astype(np.float32))
print('music ok', mix.shape)
