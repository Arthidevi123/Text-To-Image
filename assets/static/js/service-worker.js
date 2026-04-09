const CACHE_NAME = 'ai-studio-cache-v2';
const ASSETS_TO_CACHE = [
    '/',
    '/static/css/style.css',
    '/static/css/bootstrap.min.css',
    '/static/js/jquery.min.js',
    '/static/js/bootstrap.bundle.min.js',
    '/static/manifest.json'
];

// Install Event
self.addEventListener('install', event => {
    event.waitUntil(
        caches.open(CACHE_NAME).then(cache => {
            console.log('Opened cache');
            return cache.addAll(ASSETS_TO_CACHE);
        })
    );
});

// Activate Event
self.addEventListener('activate', event => {
    event.waitUntil(
        caches.keys().then(cacheNames => {
            return Promise.all(
                cacheNames.map(cacheName => {
                    if (cacheName !== CACHE_NAME) {
                        return caches.delete(cacheName);
                    }
                })
            );
        })
    );
});

// Fetch Event (Offline support)
self.addEventListener('fetch', event => {
    // Let the browser do its default handling for non-GET requests
    // This is required to fix POST form submissions and 302 redirects in standalone PWA mode!
    if (event.request.method !== 'GET') {
        return;
    }

    event.respondWith(
        caches.match(event.request).then(response => {
            return response || fetch(event.request);
        })
    );
});
