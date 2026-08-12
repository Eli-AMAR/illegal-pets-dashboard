'use strict';
const { chromium } = require('playwright-core');
const fs = require('fs');
const path = require('path');

function findChromium() {
  const root = '/opt/pw-browsers';
  for (const d of fs.readdirSync(root)) {
    if (!d.startsWith('chromium')) continue;
    const c = path.join(root, d, 'chrome-linux', 'chrome');
    if (fs.existsSync(c)) return c;
  }
  return null;
}

(async () => {
  const browser = await chromium.launch({
    executablePath: findChromium(),
    args: ['--no-sandbox', '--force-color-profile=srgb', '--hide-scrollbars', '--force-device-scale-factor=1'],
  });
  const page = await browser.newPage({ viewport: { width: 1080, height: 1080 } });
  await page.goto('file://' + path.resolve(__dirname, 'profile.html'));
  await page.evaluate(() => Promise.all([
    document.fonts.load("400 100px 'Archivo Black'"),
    document.fonts.load('800 50px Inter'),
  ]).then(() => document.fonts.ready).then(() => undefined));
  for (const v of ['gold', 'blue', 'fx']) {
    await page.evaluate(name => window.RENDER(name), v);
    await page.screenshot({ type: 'png', path: path.join(__dirname, 'out', `avatar-${v}.png`) });
    console.log(`avatar-${v}.png`);
    await page.reload();
    await page.evaluate(() => document.fonts.ready.then(() => undefined));
  }
  await browser.close();
})().catch(e => { console.error(e); process.exit(1); });
