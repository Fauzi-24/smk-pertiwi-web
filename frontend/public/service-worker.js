// Service Worker for PWA
const CACHE_NAME = 'smk-pertiwi-v2'; // Updated for PWA enhancements
const urlsToCache = [
    '/',
    '/src/styles/main.css',
    '/src/assets/SMK_PERTIWI_KUNINGAN-removebg-preview.png'
];

// Install event - cache resources
self.addEventListener('install', (event) => {
    event.waitUntil(
        caches.open(CACHE_NAME)
            .then((cache) => {
                console.log('Opened cache');
                return cache.addAll(urlsToCache);
            })
    );
    self.skipWaiting();
});

// Activate event - clean up old caches
self.addEventListener('activate', (event) => {
    event.waitUntil(
        caches.keys().then((cacheNames) => {
            return Promise.all(
                cacheNames.map((cacheName) => {
                    if (cacheName !== CACHE_NAME) {
                        console.log('Deleting old cache:', cacheName);
                        return caches.delete(cacheName);
                    }
                })
            );
        })
    );
    self.clients.claim();
});

// Fetch event - cache first, then network, and ignore non-GET requests
self.addEventListener('fetch', (event) => {
    // 1. Ignore non-GET requests (like POST)
    if (event.request.method !== 'GET') {
        return;
    }

    // 2. Ignore API requests (Backend Data) - Always fetch from network
    const url = new URL(event.request.url);
    if (url.pathname.startsWith('/api/')) {
        return; // Let browser handle it (Network only)
    }

    // 3. Cache First Strategy for Static Assets (Images, CSS, JS)
    event.respondWith(
        caches.match(event.request)
            .then((response) => {
                // Cache hit - return response
                if (response) {
                    return response;
                }
                return fetch(event.request).then(
                    (response) => {
                        // Check if we received a valid response
                        if (!response || response.status !== 200 || response.type !== 'basic') {
                            return response;
                        }

                        // Clone the response
                        const responseToCache = response.clone();

                        caches.open(CACHE_NAME)
                            .then((cache) => {
                                cache.put(event.request, responseToCache);
                            });

                        return response;
                    }
                );
            })
    );
});
