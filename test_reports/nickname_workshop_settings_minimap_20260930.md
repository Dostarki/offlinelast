# Asker adları, tercihler, workshop ve minimap — 30 Eylül 2026

Plan gpt-6.1-sol/low, uygulama gpt-5.6-terra/medium ile tamamlandı. Kota kesintisinden sonra kaydedilen checkpoint üzerinden devam edildi.

## Uygulama

- Asker başına NFC/trim doğrulanan 1–24 karakter nickname; instance ownership, HTTP ve WS işlemleri, Market düzenleme/kaydetme/iptal. Oyun etiketi, snapshot, ölüm/recovery isimleri aynı kalıcı kayıttan gelir. Mevcut can/cephane/recovery korunur.
- Sürümlü güvenli kullanıcı tercih kaydı: ses, volume, quality, skin, slotlar, zoom. Sıfır volume geçerli; engelli/bozuk storage güvenli. Yeni renderer/audio ve wheel zoom tercihi senkronize edilir.
- Workshop beş akışta seçili ürün/işlem alanı, küçük görsel katalog, ayrı SVG malzeme türleri, mevcut/gerekli miktar ve progress; yalnız seçili hero işlem düğmesi. Mobil 3+2 sekme, dar ekran tek sütun katalog. Eski nested işlem düğmeleri kaldırıldı. Dinamik SVG tier metni önizleme instrumentation hatası nedeniyle kaldırıldı; tier bilgisi normal metinde bulunur.
- Minimap oyuncunun yerel tahminli pozisyonunu ve hareket yönünü izler; kısa açı üzerinden yumuşak döner. Boss/NPC/bina/kuzey aynı dönüşümde. Nişan yönü hareketten bağımsız olduğu için haritayı döndürmez; durunca son yön korunur.

## Son doğrulama

Root tarafından birlikte çalıştırıldı:

```
npm.cmd test -- --watchAll=false --runInBand App.settings.test.jsx CraftPanel.test.jsx MarketPanel.test.jsx preferences.test.js minimap.test.js renderer.test.js HUD.stack.test.jsx
```

7 suite, 21 test geçti. Gerçek GameApp + GamePanels UI ayar/remount, renderer/audio uygulaması, gecikmiş world fetch, wheel callback; beş workshop callback'i, eksik parça ve klavye seçimi; Market instance adı ve minimap yön/edge/smoothing kapsamı içerir. Önceki renderer model-reuse ve HUD stack regresyonları da geçti.

```
backend/.venv/Scripts/python.exe -m pytest tests/test_soldier_energy_focus.py tests/test_soldier_ws_account_regression.py -q
```

16 test geçti. Gerçek WS rename/reconnect ve sahiplik/runtime; kalıcı 120sn recovery ve mevcut asker işlemleri kapsamı içerir. Starlette TestClient için iki mevcut deprecation uyarısı var.

Terra son production build'i başarıyla tamamladı; mevcut optional wagmi connector dependency uyarıları devam ediyor. Son küçük SVG tier kaldırma değişikliğinden sonra CraftPanel 3 testi tekrar geçti.

## Tarayıcı kontrolü

CUA ile gerçek `/settings` ekranında Smooth, volume 0, mute, zoom 18 seçildi; sayfa yenilendi. Smooth aktif sınıfı, volume 0, mute ve zoom 18 geri geldi. Kontrol sonunda başlangıç tercihleri Auto/.35/unmuted/24 geri yüklendi.

Geliştirmeye özel gerçek CraftPanel fixture masaüstü 1280px ve mobil 390px genişlikte incelendi. İlk kontrolde dar katalog kartlarında isim/rozet çakışması bulundu; 480px altında tek sütun yerleşim ile düzeltildi. Son görüntüde kartlar, hero ve materyal miktarları birbirini örtmüyor. Sekmeler arasında silah modları ve ekipman yükseltme görünümü ayrıca incelendi. Bu fixture gerçek hesapta craft veya cüzdan işlemi yapmaz; production'da açılmaz. Canlı hareket sırasında oynanış görsel testi yapılmadı; minimap matematiği testlerle doğrulandı.

## Yerel etkinleştirme

Gerçek storage dosyası gitignore kapsamındaki `.local-backups/pre-nickname-workshop-restart.json` konumuna yedeklendi. Port 8001 dinleyicisinin local_run.py süreci olduğu doğrulanıp yeniden başlatıldı. Yeni Python sunucu PID18828 (launcher13832); kayıtlar yüklenerek startup tamamlandı. `/api/status` ve `/api/market/catalog` HTTP200. Testler gerçek oyuncu hesabını değiştirmedi; kayıt/oturum içeriği bu rapora alınmadı.
