'use strict';
const CACHE='rifa-pro-shell-v1';
// Cache only the static app shell. Never cache sessions, campaign data or Supabase requests.
self.addEventListener('install',()=>self.skipWaiting());
self.addEventListener('activate',event=>event.waitUntil((async()=>{for(const name of await caches.keys())if(name.startsWith('rifa-pro-shell-')&&name!==CACHE)await caches.delete(name);await self.clients.claim()})()));
self.addEventListener('fetch',event=>{
 const url=new URL(event.request.url),scope=new URL(self.registration.scope);
 if(event.request.method!=='GET'||event.request.mode!=='navigate'||url.origin!==scope.origin||!(url.pathname===scope.pathname||url.pathname===scope.pathname+'index.html'))return;
 // Recovery URLs can carry an authorization code. Never put them in a cache key.
 event.respondWith((async()=>{const cache=await caches.open(CACHE),key=scope.href;try{const response=await fetch(event.request);if(response.ok&&response.type!=='opaque'&&!url.searchParams.has('code')&&!url.searchParams.has('access_token')){try{await cache.put(key,response.clone())}catch{}}return response}catch(error){const saved=await cache.match(key);if(saved)return saved;return new Response('<!doctype html><html lang="pt-BR"><meta name="viewport" content="width=device-width"><title>Rifa Pro</title><body style="font:16px system-ui;padding:30px;background:#f6f7f2;color:#20271f"><h1>Você está sem conexão.</h1><p>Conecte à internet e atualize para abrir sua campanha.</p><button onclick="location.reload()">Tentar novamente</button></body></html>',{status:503,headers:{'Content-Type':'text/html; charset=utf-8'}})}})());
});
