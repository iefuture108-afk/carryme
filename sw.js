const CACHE_NAME = 'carryme-v1';
const ASSETS = [
  './',
  './index.html',
  './manifest.json',
  './Carryme logo.png',
  './Gym collection towels.png',
  './Golden earrings set.jpg',
  './home decor.png',
  './face towel.png'
];

// Install Lifecycle Event: Cache the App Shell
self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      return cache.addAll(ASSETS);
    }).then(() => self.skipWaiting())
  );
});

// Activate Lifecycle Event: Clean old caches
self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((keys) => {
      return Promise.all(
        keys.map((key) => {
          if (key !== CACHE_NAME) {
            return caches.delete(key);
          }
        })
      );
    }).then(() => self.clients.claim())
  );
});

// Cache-First with Network-Fallback Strategy
self.addEventListener('fetch', (event) => {
  // Only handle local relative asset requests
  if (!event.request.url.startsWith(self.location.origin)) return;

  event.respondWith(
    caches.match(event.request).then((cachedResponse) => {
      if (cachedResponse) {
        return cachedResponse;
      }
      return fetch(event.request).then((networkResponse) => {
        if (!networkResponse || networkResponse.status !== 200) {
          return networkResponse;
        }
        return caches.open(CACHE_NAME).then((cache) => {
          cache.put(event.request, networkResponse.clone());
          return networkResponse;
        });
      });
    }).catch(() => {
      // Fallback if network fails completely and resource is not cached
      return caches.match('./index.html');
    })
  );
});
