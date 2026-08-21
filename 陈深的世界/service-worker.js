/**
 * service-worker.js — 陈深的世界 PWA 离线缓存
 * 1) 安装时预缓存应用外壳（游戏 HTML + manifest + 图标）
 * 2) 运行时缓存 CDN 图片（/photos/，不透明响应），实现离线玩
 */
const CACHE = 'chenshen-v1';
const APP_SHELL = [
  './陈深的世界-房间清单.html',
  './manifest.webmanifest',
  './icons/icon-192.png',
  './icons/icon-512.png',
];

self.addEventListener('install', (e) => {
  e.waitUntil(
    caches.open(CACHE)
      .then((c) => c.addAll(APP_SHELL))
      .then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', (e) => {
  e.waitUntil(
    caches.keys()
      .then((keys) => Promise.all(keys.filter((k) => k !== CACHE).map((k) => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', (e) => {
  const url = e.request.url;

  // 离线缓存 CDN 图片（跨域不透明响应）
  if (url.includes('/photos/')) {
    e.respondWith(
      caches.open(CACHE).then(async (c) => {
        const cached = await c.match(e.request);
        if (cached) return cached;
        const resp = await fetch(e.request);
        if (resp && (resp.ok || resp.type === 'opaque')) {
          c.put(e.request, resp.clone());
        }
        return resp;
      })
    );
    return;
  }

  // 页面导航：缓存优先，否则走网络
  if (e.request.mode === 'navigate') {
    e.respondWith(
      caches.match(e.request).then((r) => r || fetch(e.request))
    );
  }
});
