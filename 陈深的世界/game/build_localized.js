// 本地化构建脚本：把远程图片 URL 替换为本地相对路径
// 用法: node build_localized.js
'use strict';
const fs = require('fs');
const path = require('path');

function readUtf8(p) {
  let b = fs.readFileSync(p);
  if (b[0] === 0xEF && b[1] === 0xBB && b[2] === 0xBF) b = b.slice(3); // strip BOM
  return b.toString('utf8');
}

const gameDir = __dirname;                       // game/
const parent = path.dirname(gameDir);
const worldSrc = path.join(parent, '陈深的世界.html');
const storySrc = path.join(parent, '陈深的故事V5.html');

// 1) 读取 assets 的 url_map
const urlMap = JSON.parse(readUtf8(path.join(gameDir, 'url_map.json')));

// 2) 生成 jsdelivr 个人照片 -> photos/<原名> 映射（扫描两个源文件）
const jsdelivrRe = /https:\/\/cdn\.jsdelivr\.net\/gh\/380992846-tech\/Project1@[^"'\)\s]+\/photos\/([^"'\)\s]+)/g;
function buildPhotoMap(html) {
  const map = {};
  let m;
  while ((m = jsdelivrRe.exec(html)) !== null) {
    const enc = m[1].replace(/\.$/, '');
    const dec = decodeURIComponent(enc);
    const rel = 'photos/' + dec;
    if (fs.existsSync(path.join(gameDir, rel))) map[m[0]] = rel;
  }
  return map;
}

// 3) 只把「目标文件确实存在」的 assets URL 替换成本地路径
function assetsSubstitutions(html) {
  const subs = {};
  for (const url of Object.keys(urlMap)) {
    const rel = urlMap[url];
    if (!rel) continue;
    if (fs.existsSync(path.join(gameDir, rel))) subs[url] = rel;
  }
  return subs;
}

function applySubs(html, subs) {
  let out = html;
  for (const url of Object.keys(subs)) {
    // 只替换 URL 本串（后面可能跟 ' " ) , 等代码符号，保留）
    out = out.split(url).join(subs[url]);
  }
  return out;
}

function build(src, dest, extraName) {
  let html = readUtf8(src);
  const subs = Object.assign({}, assetsSubstitutions(html), buildPhotoMap(html));
  const localized = applySubs(html, subs);
  // 调整页面标题，表明是典藏版
  localized.replace('<title>陈深的故事 V5', '<title>陈深的故事 · 典藏版');
  fs.writeFileSync(path.join(gameDir, dest), localized, 'utf8');
  return { urlCount: Object.keys(subs).length, sizeKB: Math.round(localized.length / 1024) };
}

const w = build(worldSrc, 'world.html');
const s = build(storySrc, 'story.html');
console.log('world.html 替换图片URL数=', w.urlCount, ' 大小KB=', w.sizeKB);
console.log('story.html 替换图片URL数=', s.urlCount, ' 大小KB=', s.sizeKB);
console.log('assets 文件数=', fs.readdirSync(path.join(gameDir, 'assets')).length);
console.log('photos 文件数=', fs.readdirSync(path.join(gameDir, 'photos')).length);
