'use strict';
/* Renders one video config to a JPEG frame sequence using headless Chromium.
   Usage: node render.js <config.json> <framesDir> */
const { chromium } = require('playwright-core');
const fs = require('fs');
const path = require('path');

const cfgPath = process.argv[2];
const outDir = process.argv[3];
const cfg = JSON.parse(fs.readFileSync(cfgPath, 'utf8'));
fs.mkdirSync(outDir, { recursive: true });

function findChromium() {
  const roots = ['/opt/pw-browsers'];
  for (const root of roots) {
    for (const d of fs.readdirSync(root)) {
      if (!d.startsWith('chromium')) continue;
      for (const cand of [
        path.join(root, d, 'chrome-linux', 'chrome'),
        path.join(root, d, 'chrome-linux', 'headless_shell'),
      ]) if (fs.existsSync(cand)) return cand;
    }
  }
  return null;
}

(async () => {
  const browser = await chromium.launch({
    executablePath: findChromium(),
    args: ['--no-sandbox', '--force-color-profile=srgb', '--disable-lcd-text',
      '--hide-scrollbars', '--force-device-scale-factor=1', '--disable-gpu'],
  });
  const page = await browser.newPage({ viewport: { width: 1080, height: 1920 } });
  await page.goto('file://' + path.resolve(__dirname, 'template.html'));
  // Webfonts load lazily; force them before any text measurement.
  await page.evaluate(() => Promise.all([
    document.fonts.load("400 100px 'Archivo Black'"),
    document.fonts.load('600 30px Inter'),
    document.fonts.load('800 50px Inter'),
    document.fonts.load('900 50px Inter'),
  ]).then(() => document.fonts.ready).then(() => undefined));
  const total = await page.evaluate(c => window.INIT(c), cfg);
  const fps = cfg.fps || 30;
  const frames = Math.round(total / 1000 * fps);
  for (let f = 0; f < frames; f++) {
    await page.evaluate(t => window.seek(t), f * 1000 / fps);
    await page.screenshot({
      type: 'jpeg', quality: 92,
      path: path.join(outDir, String(f).padStart(5, '0') + '.jpg'),
    });
    if (f % 90 === 0) console.log(`  frame ${f}/${frames}`);
  }
  console.log(`TOTAL_MS=${Math.round(total)}`);
  console.log(`FRAMES=${frames}`);
  await browser.close();
})().catch(e => { console.error(e); process.exit(1); });
