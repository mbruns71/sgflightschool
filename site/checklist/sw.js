/* ============================================================
   N61574 Checklist — service worker
   Cache-first so the checklist opens instantly with no signal.
   The cache name carries the build version, so publishing a new
   VERSION installs a fresh cache and drops the old one.
   Bump VERSION and version.json together on every deploy.
   ============================================================ */
var VERSION = "2026.08.26-8";
var CACHE   = "n61574-" + VERSION;

var ASSETS = [
  "./",
  "./index.html",
  "./manifest.webmanifest",
  "./icon-180.png",
  "./icon-192.png",
  "./icon-512.png"
];

self.addEventListener("install", function(e){
  e.waitUntil(
    caches.open(CACHE).then(function(c){ return c.addAll(ASSETS); })
  );
});

self.addEventListener("activate", function(e){
  e.waitUntil(
    caches.keys().then(function(keys){
      return Promise.all(keys.map(function(k){
        if(k !== CACHE) return caches.delete(k);
      }));
    }).then(function(){ return self.clients.claim(); })
  );
});

self.addEventListener("fetch", function(e){
  if(e.request.method !== "GET") return;
  var url = new URL(e.request.url);

  /* The version file must always come from the network, otherwise the app
     would be comparing itself against its own cached copy and never update. */
  if(url.pathname.indexOf("version.json") !== -1){
    e.respondWith(
      fetch(e.request, {cache:"no-store"}).catch(function(){
        return caches.match(e.request);
      })
    );
    return;
  }

  /* Cross-origin (Google Fonts) — never block on it; the CSS carries
     local fallbacks so the app is fully legible without it. */
  if(url.origin !== location.origin){
    e.respondWith(fetch(e.request).catch(function(){ return new Response("", {status:504}); }));
    return;
  }

  e.respondWith(
    caches.match(e.request).then(function(hit){
      return hit || fetch(e.request).then(function(res){
        if(res && res.ok){
          var copy = res.clone();
          caches.open(CACHE).then(function(c){ c.put(e.request, copy); });
        }
        return res;
      }).catch(function(){
        /* Navigation offline with nothing cached yet -> serve the shell. */
        if(e.request.mode === "navigate") return caches.match("./index.html");
        return new Response("", {status:504});
      });
    })
  );
});

/* The page asks us to take over only after the pilot taps "Update now". */
self.addEventListener("message", function(e){
  if(e.data === "skipWaiting") self.skipWaiting();
});
