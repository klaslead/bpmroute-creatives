// Renders reel.html frame by frame and muxes it with out/music.wav.
// Run: python3 music.py && node render.js            -> out/happy-diwali-2026-reel.mp4
//      node render.js --stills 60,180,240,330,390      -> out/still-<frame>.jpg (quick previews)
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path'), { spawn } = require('child_process');

(async () => {
  const out = path.join(__dirname, 'out'); fs.mkdirSync(out, { recursive: true });
  const html = fs.readFileSync(path.join(__dirname, 'reel.html'), 'utf8')
    .replace('MARK_SVG', fs.readFileSync(path.join(__dirname, 'mark.svg'), 'utf8'));
  const tmp = path.join(__dirname, '_reel.html'); fs.writeFileSync(tmp, html);
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
  p.on('pageerror', e => console.error('page error:', e.message));
  await p.goto('file://' + tmp);
  await p.evaluate(() => window.ready);
  await p.waitForTimeout(300);

  const si = process.argv.indexOf('--stills');
  if (si > 0) {
    const want = process.argv[si + 1].split(',').map(Number), last = Math.max(...want);
    for (let f = 0; f <= last; f++) {
      await p.evaluate(f => window.renderFrame(f), f);
      if (want.includes(f)) await p.screenshot({ path: path.join(out, `still-${f}.jpg`), type: 'jpeg', quality: 85 });
    }
  } else {
    const total = await p.evaluate(() => Math.round(DATA.dur * DATA.fps));
    const mp4 = path.join(out, 'happy-diwali-2026-reel.mp4');
    const ff = spawn('ffmpeg', ['-y', '-loglevel', 'error', '-f', 'image2pipe', '-c:v', 'mjpeg', '-framerate', '30', '-i', '-',
      '-i', path.join(out, 'music.wav'), '-c:v', 'libx264', '-preset', 'slow', '-crf', '17', '-pix_fmt', 'yuv420p',
      '-profile:v', 'high', '-level', '4.2', '-c:a', 'aac', '-b:a', '256k', '-shortest', '-movflags', '+faststart', mp4], { stdio: ['pipe', 'inherit', 'inherit'] });
    const t0 = Date.now();
    for (let f = 0; f < total; f++) {
      await p.evaluate(f => window.renderFrame(f), f);
      const buf = await p.screenshot({ type: 'jpeg', quality: 95 });
      if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
      if (f % 60 === 0) console.log(`frame ${f}/${total}  ${((Date.now() - t0) / 1000).toFixed(0)}s`);
    }
    ff.stdin.end();
    await new Promise(r => ff.on('close', r));
    console.log('wrote', mp4);
  }
  await b.close();
  fs.unlinkSync(tmp);
})();
