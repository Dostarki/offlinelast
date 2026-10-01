# Equipment, Soldier, Energy Drink validation — 30 September 2026

## Canlı sunucu ve zoom düzeltmesi

- İsim etiketleri zoom/resize sırasında yaklaşık 42 CSS piksel sprite yüksekliğine göre ölçeklenir; mobil genişlik sınırı uygulanır.
- Yeni backend doğrulaması: 14 test geçti; gerçek WebSocket handler üzerinden beş ayrı asker alımı, altıncı ret, instance bazlı yükseltme/çıkarma ve gerçek motor atış/hasar testi kapsandı.
- İsim etiketi, MarketPanel ve CraftPanel: 7 arayüz testi geçti; frontend derlemesi başarılı (mevcut isteğe bağlı cüzdan bağımlılığı uyarıları sürüyor).
- 8001 portundaki eski `local_run.py` süreci otomatik reload kullanmıyordu. Yerel kayıt yedeği alınarak güncel `.venv` çalıştırıcısıyla yeniden başlatıldı.
- Yeniden başlatma sonrası `/api/status` ve `/api/market/catalog`: HTTP 200. Kaydedilmiş `player_progress` ve `player_accounts` içerikleri yedekle eşit; mevcut ilerleme yeniden yazılmadı.
- Canlı oyuncu cüzdanıyla oyun içi görsel savaş kontrolü yapılmadı; atış ve hasar gerçek motor ve izole WebSocket testleriyle doğrulandı.

- `backend/.venv/Scripts/python.exe -m compileall -q backend` completed successfully.
- `backend/.venv/Scripts/python.exe -m pytest backend/tests/test_soldier_energy_focus.py -q` completed: 5 passed. The focused cases cover real five-slot roster reconciliation/state retention, autonomous approach and ally filtering, soldier recovery, energy-drink refresh/replay behavior, final 2× engine regen, expiry, cap, and snapshot fields.
- `npm run build` completed successfully after the equipment and consumable UI changes.
- The build retained existing optional wagmi wallet connector resolution warnings.
- Live server/browser smoke validation was not run because local ports were not listening.
- Bundled-venv Uvicorn smoke subsequently started `local_run:app` on port 8002. `GET /api/world`, `/api/weapons`, `/api/auth/me`, and `/api/market/catalog` each returned 200; catalog exposed equipment, materials, sell prices, and soldiers. The temporary server was stopped after the smoke check.
- Cüzdansız yerel lobi render edildi. Cüzdan oturumu olmadığı için oyun içi görsel doğrulama yapılmadı.
- Final scoped run: soldier/energy, safe-zone inventory, and alliance-damage suites: 11 passed. Historical alliance fixtures were moved from the origin safe zone to open combat coordinates while retaining their offsets.
- Market UI now normalizes legacy numeric soldier tiers, displays active and owned counts separately, and sends per-tier deactivate requests. The final frontend build completed successfully with the existing optional wagmi connector warnings.
