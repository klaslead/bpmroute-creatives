// Renders html/*.html to out/*.jpg. Run: node render.js
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path');
(async () => {
  const dir = path.join(__dirname, 'html'), out = path.join(__dirname, 'out');
  fs.mkdirSync(out, { recursive: true });
  const b = await chromium.launch();
  for (const f of fs.readdirSync(dir).filter(f => f.endsWith('.html'))) {
    const h = f.includes('-story') ? 1920 : 1350;
    const p = await b.newPage({ viewport: { width: 1080, height: h } });
    await p.goto('file://' + path.join(dir, f));
    await p.evaluate(() => document.fonts.ready);
    await p.waitForTimeout(300);
    await p.screenshot({ path: path.join(out, f.replace('.html', '.jpg')), type: 'jpeg', quality: 92 });
    await p.close();
  }
  await b.close();
})();
