// Service Worker for 我们的时光 PWA
var CACHE = 'our-love-v2';
var ASSETS = ['./', 'index.html', 'manifest.json', 'icon.svg'];

self.addEventListener('install', function(e) {
  e.waitUntil(
    caches.open(CACHE).then(function(c) { return c.addAll(ASSETS) })
    .then(function() { return self.skipWaiting() })
  );
});

self.addEventListener('activate', function(e) {
  e.waitUntil(
    caches.keys().then(function(keys) {
      return Promise.all(keys.filter(function(k) { return k !== CACHE }).map(function(k) { return caches.delete(k) }));
    }).then(function() { return self.clients.claim() })
  );
});

self.addEventListener('fetch', function(e) {
  if (e.request.method !== 'GET') return;
  e.respondWith(
    caches.match(e.request).then(function(cached) {
      return cached || fetch(e.request).then(function(resp) {
        if (resp.ok && (e.request.url.startsWith('http://') || e.request.url.startsWith('https://'))) {
          var clone = resp.clone();
          caches.open(CACHE).then(function(c) { c.put(e.request, clone) });
        }
        return resp;
      }).catch(function() {
        return cached || new Response('离线中...', { headers: { 'Content-Type': 'text/plain; charset=utf-8' } });
      });
    })
  );
});
