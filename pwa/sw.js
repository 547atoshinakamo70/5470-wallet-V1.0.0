const CACHE_NAME='5470-wallet-v1.0.2';
const urlsToCache=['./wallet_pwa.html','./manifest.json','./icons/icon-192.png','./icons/icon-512.png'];
self.addEventListener('install',e=>{e.waitUntil(caches.open(CACHE_NAME).then(c=>c.addAll(urlsToCache)))});
self.addEventListener('fetch',e=>{e.respondWith(caches.match(e.request).then(r=>r||fetch(e.request)))});
self.addEventListener('activate',e=>{e.waitUntil(caches.keys().then(names=>Promise.all(names.map(n=>n!==CACHE_NAME&&caches.delete(n)))))});
