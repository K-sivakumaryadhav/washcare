const CACHE_NAME = "washcare-shell-v1";
const SHELL_FILES = [
  "/",
  "/static/css/style.css",
  "/static/js/main.js",
  "/static/js/api.js",
];

self.addEventListener("install", (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => cache.addAll(SHELL_FILES))
  );
});

self.addEventListener("fetch", (event) => {
  // Network-first for API calls, cache-first for the static app shell.
  if (event.request.url.includes("/api/")) return;
  event.respondWith(
    caches.match(event.request).then((cached) => cached || fetch(event.request))
  );
});
