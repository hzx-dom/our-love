// Service Worker for 我们的时光 PWA v3 — network-first
var CACHE = 'our-love-v3';

self.addEventListener('install', function(e) {
  self.skipWaiting();
});

self.addEventListener('activate', function(e) {
  e.waitUntil(
    caches.keys().then(function(keys) {
      return Promise.all(keys.map(function(k) { return caches.delete(k); }));
    }).then(function() { return self.clients.claim(); })
  );
});

self.addEventListener('fetch', function(e) {
  if (e.request.method !== 'GET') return;
  // HTML: network-first (no stale cache)
  if (e.request.destination === 'document' || e.request.url.endsWith('/')) {
    e.respondWith(
      fetch(e.request).catch(function() {
        return caches.match(e.request) || new Response('离线中...请联网后刷新', { headers: { 'Content-Type': 'text/plain; charset=utf-8' } });
      })
    );
    return;
  }
  // Other assets: cache-first
  e.respondWith(
    caches.match(e.request).then(function(cached) {
      return cached || fetch(e.request).then(function(resp) {
        if (resp.ok) {
          var clone = resp.clone();
          caches.open(CACHE).then(function(c) { c.put(e.request, clone); });
        }
        return resp;
      });
    })
  );
});
