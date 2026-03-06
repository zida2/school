// Service Worker pour PWA
const CACHE_NAME = 'erp-etudiant-v1';
const urlsToCache = [
  '/mobile/',
  '/mobile/index.html',
  '/mobile/dashboard.html',
  '/mobile/inscription.html',
  '/mobile/styles.css',
  '/js/config.js',
  '/js/api.js'
];

// Installation du Service Worker
self.addEventListener('install', event => {
  console.log('📦 Service Worker: Installation...');
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => {
        console.log('✅ Cache ouvert');
        return cache.addAll(urlsToCache);
      })
      .catch(err => console.error('❌ Erreur cache:', err))
  );
  self.skipWaiting();
});

// Activation du Service Worker
self.addEventListener('activate', event => {
  console.log('🔄 Service Worker: Activation...');
  event.waitUntil(
    caches.keys().then(cacheNames => {
      return Promise.all(
        cacheNames.map(cacheName => {
          if (cacheName !== CACHE_NAME) {
            console.log('🗑️ Suppression ancien cache:', cacheName);
            return caches.delete(cacheName);
          }
        })
      );
    })
  );
  return self.clients.claim();
});

// Interception des requêtes (stratégie Network First)
self.addEventListener('fetch', event => {
  event.respondWith(
    fetch(event.request)
      .then(response => {
        // Clone la réponse
        const responseClone = response.clone();
        
        // Met en cache la nouvelle réponse
        caches.open(CACHE_NAME).then(cache => {
          cache.put(event.request, responseClone);
        });
        
        return response;
      })
      .catch(() => {
        // Si le réseau échoue, utilise le cache
        return caches.match(event.request);
      })
  );
});

// Gestion des notifications push
self.addEventListener('push', event => {
  console.log('📬 Notification push reçue');
  
  const data = event.data ? event.data.json() : {};
  const title = data.title || 'ERP Universitaire';
  const options = {
    body: data.body || 'Nouvelle notification',
    icon: '/mobile/icon-192.png',
    badge: '/mobile/icon-192.png',
    vibrate: [200, 100, 200],
    data: data.url || '/mobile/dashboard.html',
    actions: [
      { action: 'open', title: 'Ouvrir' },
      { action: 'close', title: 'Fermer' }
    ]
  };
  
  event.waitUntil(
    self.registration.showNotification(title, options)
  );
});

// Gestion des clics sur les notifications
self.addEventListener('notificationclick', event => {
  console.log('🔔 Clic sur notification');
  
  event.notification.close();
  
  if (event.action === 'open' || !event.action) {
    event.waitUntil(
      clients.openWindow(event.notification.data || '/mobile/dashboard.html')
    );
  }
});
