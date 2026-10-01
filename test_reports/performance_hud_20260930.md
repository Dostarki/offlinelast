# Renderer ve HUD doğrulaması — 30 Eylül 2026

## Değişiklik

- `GameRenderer.syncState`, backend asker skinlerini `getSkin(...).id` ile kanonikleştirir. Böylece `soldier_woodland`, `soldier_desert`, `soldier_urban` ve `soldier_winter` fallback görünümü her snapshot'ta yeniden kurdurmaz.
- Görünüm yalnız kanonik skin, silah veya ekipman değiştiğinde yeniden kurulur.
- Hasar sunumu `formatDamage` ile kırpılır; fizik ve sunucu hasarı değiştirilmez. Canvas sprite 96 × 48 ekran pikseli olarak zoom 4–40 arasında ölçeklenir.
- Aktif sprite sayısı 12, damage texture önbelleği 24 ile sınırlıdır. Eviction yalnız aktif bir floating sprite tarafından kullanılmayan texture üzerinde yapılır.
- StatusEffects, güvenli alan/koruma uyarıları ve BossHUD aynı üst orta flex akışındadır. BossHUD'un eski masaüstü/mobil mutlak `top` ofsetleri kaldırılmıştır.

## Çalıştırılan doğrulama

`CI=true npm test -- --runInBand --watchAll=false src/game/renderer.test.js src/game/damage.test.js src/components/HUD.stack.test.jsx`

Sonuç: 3 suite, 6 test geçti.

- 5 asker (S1–S5) × 100 değişmeyen snapshot: `createHuman` 5, dispose 0.
- Bir asker silah yükseltmesi: bir model yeniden oluşturma ve bir dispose.
- Bir askerin snapshot'tan kaldırılması: bir dispose.
- Zoom 4 ve 40'ta 96 px hasar yazısı kontratı.
- Aktif sprite texture'ının cache eviction tarafından dispose edilmemesi.
- Safe-zone, spawn protection ve BossHUD'un gerçek React render içinde aynı bildirim stack'inde olması.

Önceki ölçülen backend sabit dünyası: 0 asker 0.630 ms/tick; 5 asker 1.295 ms/tick; 400 `update_soldier` çağrısı 42 ms kümülatif, `wall_distance` 6.683 çağrı/23 ms. Bu yük testi veya FPS ölçümü değildir; bu nedenle backend hedef taramasına ölçülmemiş bir cache değişikliği eklenmedi.
