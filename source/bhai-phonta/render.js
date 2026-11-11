// Renders reel.html frame by frame (Three.js via headless Chromium) and muxes it with out/final.wav.
// Run: python3 music.py && python3 mix.py && node render.js        -> out/shubho-bhai-phonta-2026-reel.mp4
//      node render.js --stills 30,150,280,330,420,560,640,720       -> out/still-<frame>.jpg
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path'), http = require('http'), { spawn } = require('child_process');
const TYPES = { '.html': 'text/html', '.js': 'text/javascript', '.css': 'text/css', '.woff2': 'font/woff2', '.svg': 'image/svg+xml' };

(async () => {
  const out = path.join(__dirname, 'out'); fs.mkdirSync(out, { recursive: true });
  const html = fs.readFileSync(path.join(__dirname, 'reel.html'), 'utf8').replace('MARK_SVG', fs.readFileSync(path.join(__dirname, 'mark.svg'), 'utf8'));
  const srv = http.createServer((q, r) => {
    const u = decodeURIComponent(q.url.split('?')[0]);
    if (u === '/' || u === '/reel.html') { r.writeHead(200, { 'content-type': 'text/html' }); return r.end(html); }
    const f = path.join(__dirname, u);
    if (!f.startsWith(__dirname) || !fs.existsSync(f)) { r.writeHead(404); return r.end(); }
    r.writeHead(200, { 'content-type': TYPES[path.extname(f)] || 'application/octet-stream' }); fs.createReadStream(f).pipe(r);
  }).listen(0);
  const port = srv.address().port;
  const b = await chromium.launch({ args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'] });
  const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
  p.on('pageerror', e => console.error('page error:', e.message));
  p.on('console', m => { if (m.type() === 'error' || m.type() === 'warning') console.log('console:', m.text()); });
  await p.goto(`http://127.0.0.1:${port}/reel.html`);
  await p.waitForFunction(() => window.ready); await p.evaluate(() => window.ready);
  await p.waitForTimeout(300);
  const shot = () => p.screenshot({ type: 'jpeg', quality: 94 });

  const si = process.argv.indexOf('--stills');
  if (si > 0) {
    for (const f of process.argv[si + 1].split(',').map(Number)) {
      await p.evaluate(f => window.renderFrame(f), f);
      fs.writeFileSync(path.join(out, `still-${f}.jpg`), await shot());
    }
  } else {
    const total = await p.evaluate(() => Math.round(DATA.dur * DATA.fps));
    const mp4 = path.join(out, 'shubho-bhai-phonta-2026-reel.mp4');
    const ff = spawn('ffmpeg', ['-y', '-loglevel', 'error', '-f', 'image2pipe', '-c:v', 'mjpeg', '-framerate', '30', '-i', '-',
      '-i', path.join(out, 'final.wav'), '-c:v', 'libx264', '-preset', 'slow', '-crf', '18', '-pix_fmt', 'yuv420p',
      '-profile:v', 'high', '-level', '4.2', '-c:a', 'aac', '-b:a', '256k', '-shortest', '-movflags', '+faststart', mp4], { stdio: ['pipe', 'inherit', 'inherit'] });
    const t0 = Date.now();
    for (let f = 0; f < total; f++) {
      await p.evaluate(f => window.renderFrame(f), f);
      const buf = await shot();
      if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
      if (f % 60 === 0) console.log(`frame ${f}/${total}  ${((Date.now() - t0) / 1000).toFixed(0)}s`);
    }
    ff.stdin.end(); await new Promise(r => ff.on('close', r));
    console.log('wrote', mp4);
  }
  await b.close(); srv.close();
})();
