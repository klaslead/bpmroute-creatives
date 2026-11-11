"""Mix the voice over onto the soundtrack, duck the music under it, and write data.js for the visuals.
Run after music.py:  python3 mix.py  -> out/final.wav, data.js
Voice over: vo/vo.wav (ElevenLabs, Bengali). It is cut on its pauses into segments and each phrase group is placed on the timeline.
"""
import json, os, wave
import numpy as np
from scipy.signal import butter, sosfilt

HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(HERE, 'out')
SR, FPS = 44100, 30
music = np.load(os.path.join(OUT, 'music.npy')).astype(np.float64)
N = music.shape[1]; DUR = N / SR
CUES = dict(dur=DUR, hit=9.0, morph=12.6, drop=16.5, outro=22.0, dropRise=6.9)

# phrase groups: (first segment, last segment, start time on the reel)
GROUPS = json.load(open(os.path.join(HERE, 'vo', 'groups.json'))) if os.path.exists(os.path.join(HERE, 'vo', 'groups.json')) else None
voice = np.zeros(N); segs_out = []
vo_path = os.path.join(HERE, 'vo', 'vo.wav')
if os.path.exists(vo_path):
    with wave.open(vo_path) as w:
        assert w.getframerate() == SR, w.getframerate()
        v = np.frombuffer(w.readframes(w.getnframes()), '<i2').astype(np.float64) / 32768
        if w.getnchannels() == 2: v = v.reshape(-1, 2).mean(1)
    # find speech segments (pauses >= 0.28 s)
    hop = int(.01 * SR); env = np.array([np.sqrt((v[i:i + hop] ** 2).mean()) for i in range(0, len(v) - hop, hop)])
    on = env > max(.01, env.max() * .04)
    segs, i = [], 0
    while i < len(on):
        if on[i]:
            j = i
            while j < len(on) and (on[j] or (on[j:j + 28].any() if j + 28 <= len(on) else False)): j += 1
            segs.append((max(0, i * hop - int(.04 * SR)), min(len(v), j * hop + int(.08 * SR)))); i = j
        else: i += 1
    print('vo segments:', [(round(a / SR, 2), round(b / SR, 2)) for a, b in segs])
    if GROUPS:
        for g in GROUPS:
            a, b = segs[g['from']][0], segs[g['to']][1]
            x = int(g['at'] * SR); piece = v[a:b] * g.get('gain', 1.0)
            fade = np.minimum(1, np.minimum(np.arange(len(piece)), np.arange(len(piece))[::-1]) / (.01 * SR))
            voice[x:x + len(piece)] += (piece * fade)[:N - x]
            for k in range(g['from'], g['to'] + 1):
                segs_out.append(dict(t0=round(g['at'] + (segs[k][0] - a) / SR, 3), t1=round(g['at'] + (segs[k][1] - a) / SR, 3)))
    voice = sosfilt(butter(2, 90, 'high', fs=SR, output='sos'), voice)
    voice /= (np.abs(voice).max() + 1e-9)

# duck music under the voice
venv = np.convolve(np.abs(voice), np.ones(int(.12 * SR)) / int(.12 * SR), 'same')
duck = 1 - .5 * np.clip(venv / (venv.max() + 1e-9) * 3, 0, 1)
duck = np.convolve(duck, np.ones(int(.2 * SR)) / int(.2 * SR), 'same')
mix = music * duck + np.stack([voice, voice]) * .95
mix = np.tanh(1.2 * mix) / np.tanh(1.2) ; mix = mix / np.abs(mix).max() * .94
pcm = (mix.T * 32767).astype('<i2')
with wave.open(os.path.join(OUT, 'final.wav'), 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())

# per-frame levels (music for visuals, voice for caption meters)
mono = music.mean(0); frames = int(DUR * FPS); hop = SR // FPS; win = 4096
edges = np.geomspace(40, 12000, 49); freqs = np.fft.rfftfreq(win, 1 / SR); wn = np.hanning(win)
bands, rms, lows, vol = [], [], [], []
for f in range(frames):
    c = f * hop; seg = mono[max(0, c - win // 2): c + win // 2]; seg = np.pad(seg, (0, win - len(seg)))
    mag = np.abs(np.fft.rfft(seg * wn))
    bands.append([float(mag[(freqs >= a) & (freqs < b)].mean()) if ((freqs >= a) & (freqs < b)).any() else 0. for a, b in zip(edges[:-1], edges[1:])])
    rms.append(float(np.sqrt((seg ** 2).mean()))); lows.append(float(mag[(freqs > 30) & (freqs < 140)].mean()))
    vs = voice[c:c + hop]; vol.append(float(np.sqrt((vs ** 2).mean())) if len(vs) else 0.)
bands = np.clip(np.log1p(np.array(bands) * 4) / (np.percentile(np.log1p(np.array(bands) * 4), 98, axis=0) + 1e-9), 0, 1.2)
rms = np.array(rms) / max(rms); lows = np.array(lows) / max(lows); vol = np.array(vol) / (max(vol) + 1e-9)

CAP_TEXT = json.load(open(os.path.join(HERE, 'captions.json')))
caps = []
for c in CAP_TEXT:
    if 'seg' in c and segs_out:
        s = segs_out[c['seg'][0]], segs_out[c['seg'][1]]
        caps.append(dict(bn=c['bn'], en=c['en'], t0=s[0]['t0'], t1=s[1]['t1'] + c.get('hold', .3)))
    else:
        caps.append(dict(bn=c['bn'], en=c['en'], t0=c['t0'], t1=c['t1']))
CUES['caps'] = caps
CUES['words'] = json.load(open(os.path.join(HERE, 'words.json')))
data = dict(fps=FPS, dur=DUR, cues=CUES, bands=[[round(v, 3) for v in r] for r in bands.tolist()],
            rms=[round(v, 3) for v in rms], low=[round(v, 3) for v in lows], vo=[round(v, 3) for v in vol])
open(os.path.join(HERE, 'data.js'), 'w').write('window.DATA=' + json.dumps(data, ensure_ascii=False, separators=(',', ':')) + ';')
print('mix ok', DUR, 'caps', [(c['t0'], c['t1']) for c in caps])
