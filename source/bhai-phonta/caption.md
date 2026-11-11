# Shubho Bhai Phonta 2026 reel – BPMroute

Vertical reel, 1080x1920, 28 s, 30 fps, H.264 + AAC. Real-time 3D (Three.js, rendered frame by frame) with an original soundtrack synthesised in `music.py` (96 BPM, conch call, flute, sitar plucks, dhol, a soft ulu at the drop), so it is safe to post with audio. Voice over in Bengali (ElevenLabs, voice "Swati S – Pleasant Engaging Creator").

Story: a conch sounds and a 3D brass thala rises out of the dark: diya, chandan, kumkum, sandesh, durva grass, dhaan and marigolds on an alpana-engraved plate → the sister's voice recites the phonta chant, captioned in Bengali and English → a drop of chandan rises from the bowl and flies into the camera, the beat lands, ripples and a 3D EQ ring burst out → "ঝগড়া, খুনসুটি, ভালোবাসা" fly through the frame in 3D → the thala tilts up and turns into a golden vinyl record with a tonearm and a glass "repeat" ring: "siblings are like your favourite song, on repeat for life" → drop: giant 3D "শুভ ভাইফোঁটা" with a spinning EQ halo, orbiting diyas and a marigold petal burst → 3D BPMroute logo tile, bpmroute.com, by EKSTAC33 Production.

Voice over script (Bengali):
> ভাইয়ের কপালে দিলাম ফোঁটা, যমের দুয়ারে পড়ল কাঁটা। যমুনা দেয় যমকে ফোঁটা, আমি দিই আমার ভাইকে ফোঁটা। ঝগড়া, খুনসুটি, আর অনেকটা ভালোবাসা… ভাই-বোনের এই সম্পর্কটা ঠিক প্রিয় গানের মতো, সারাজীবন রিপিটে বাজে। শুভ ভাইফোঁটা! BPMroute-এর পক্ষ থেকে, সব ভাই-বোনকে অনেক ভালোবাসা।

## Facebook caption

🪔✨ শুভ ভাইফোঁটা from BPMroute ✨🪔

ভাইয়ের কপালে দিলাম ফোঁটা, যমের দুয়ারে পড়ল কাঁটা। 🙏

Fights, teasing, and a whole lot of love. Siblings are like your favourite song: always on repeat. 🔁🎶

To every brother and sister celebrating today, from our studio to your home, Happy Bhai Phonta! ❤️

BPMroute is launching soon: AI mastering, worldwide distribution and production tools, starting with a free tier 👉 bpmroute.com

— BPMroute by EKSTAC33 Production

#BhaiPhonta #ShubhoBhaiphonta #BhaiDooj #Bhaiphota #BhaiPhonta2026 #Bengali #Kolkata #BPMroute #IndependentArtist #MusicDistribution #AIMastering #IndianMusic

## Instagram caption

শুভ ভাইফোঁটা 🪔✨

ভাইয়ের কপালে দিলাম ফোঁটা,
যমের দুয়ারে পড়ল কাঁটা 🙏

ঝগড়া, খুনসুটি, আর অনেকটা ভালোবাসা ❤️
Siblings = your favourite song, on repeat for life 🔁🎶

Tag the sibling who's always in your playlist 👇

Free to start, launching soon → link in bio · bpmroute.com

BPMroute by EKSTAC33 Production

.
.
#BhaiPhonta #ShubhoBhaiphonta #BhaiDooj #Bhaiphota #BhaiPhonta2026 #BhaiDooj2026 #Bangali #KolkataDiaries #BengaliReels #FestiveReels #BPMroute #IndependentArtist #IndieArtist #MusicDistribution #AIMastering #MusicProducer #IndianMusic #IndieMusicIndia #ReelsIndia

## Posting notes

- Instagram Reel: upload `shubho-bhai-phonta-2026-reel.mp4`, pick `shubho-bhai-phonta-2026-cover.jpg` as the cover (or the frame at 0:18). Keep the original audio.
- Facebook: post as a Reel/video on the BPMroute page via Make, only after approval.

## Rebuild

```
npm i three@0.170.0   # then copy node_modules/three/build/three.module.js and examples/jsm into vendor/ (see setup.sh)
python3 music.py && python3 mix.py && node render.js
```
