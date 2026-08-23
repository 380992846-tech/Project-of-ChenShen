// 重试下载未成功的远程图片（限速，遵守 Wikimedia 机器人策略）
// 用法: node retry_missing.js
'use strict';
const fs = require('fs');
const path = require('path');

function readUtf8(p) {
  let b = fs.readFileSync(p);
  if (b[0] === 0xEF && b[1] === 0xBB && b[2] === 0xBF) b = b.slice(3);
  return b.toString('utf8');
}

const gameDir = __dirname;
const urlMap = JSON.parse(readUtf8(path.join(gameDir, 'url_map.json')));

const missing = [];
for (const url of Object.keys(urlMap)) {
  const rel = urlMap[url];
  if (!rel) continue;
  if (!fs.existsSync(path.join(gameDir, rel))) missing.push({ url, rel });
}
console.log('missing files to retry =', missing.length);

const sleep = (ms) => new Promise(r => setTimeout(r, ms));
const UA = 'ChenShenGameOfflineBuilder/1.0 (offline packaging tool; browser-extension-free)';

async function download(url, rel) {
  const out = path.join(gameDir, rel);
  for (let attempt = 1; attempt <= 4; attempt++) {
    try {
      const res = await fetch(url, { headers: { 'User-Agent': UA, 'Accept': 'image/*,*/*' }, redirect: 'follow' });
      if (res.status === 429) {
        const wait = 2000 + attempt * 6000;
        console.log('429 -> wait', wait, 'ms for', url.slice(0, 80));
        await sleep(wait);
        continue;
      }
      if (!res.ok) { console.log('HTTP', res.status, url.slice(0, 80)); await sleep(3000); continue; }
      const buf = Buffer.from(await res.arrayBuffer());
      fs.writeFileSync(out, buf);
      console.log('OK', rel);
      return true;
    } catch (e) {
      console.log('ERR', e.message, url.slice(0, 80));
      await sleep(3000);
    }
  }
  console.log('GIVEUP', url.slice(0, 90));
  return false;
}

(async () => {
  let ok = 0;
  for (let i = 0; i < missing.length; i++) {
    const m = missing[i];
    if (await download(m.url, m.rel)) ok++;
    await sleep(1800); // 节流
  }
  console.log('RETRY_DONE ok=', ok, 'failed=', missing.length - ok);
})();
