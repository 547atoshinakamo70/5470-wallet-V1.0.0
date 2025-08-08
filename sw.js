cat > sw.js << 'EOF'
const CACHE_NAME = '5470-wallet-v1.0.0';
const urlsToCache = ['./wallet_pwa.html', './manifest.json'];

self.addEventListener('install', (event) => {
  event.waitUntil(caches.open(CACHE_NAME).then((cache) => { console.log('Cache opened'); return cache.addAll(urlsToCache); }));
});

self.addEventListener('fetch', (event) => {
  event.respondWith(caches.match(event.request).then((response) => { return response || fetch(event.request); }));
});

self.addEventListener('activate', (event) => {
  event.waitUntil(caches.keys().then((cacheNames) => { return Promise.all(cacheNames.map((cacheName) => { if (cacheName !== CACHE_NAME) { return caches.delete(cacheName); } })); }));
});
EOF