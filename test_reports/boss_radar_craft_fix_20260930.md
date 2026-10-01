# Boss bölgeleri, minimap ve CraftPanel düzeltmesi

30 Eylül 2026. Plan gpt-6.1-sol/low; uygulama gpt-5.6-terra/medium.

## Sonuç

- Dört boss kendi home konumunun 38 m bölgesinde hedef edinir ve kalır; bölgeler ayrıdır. Hedef ölür, güvenli alana girer veya bölgeden çıkarsa hedef/pending saldırı bırakılır ve boss can yenilemeden yürüyerek eve döner. Leap/blink landing ve hareket sınır içindedir. Eski sınır dışı aktörler yalnız içeri yaklaşan adımlarla döner; ışınlanma veya iyileşme yapılmaz. Hasar/projectile/hazard menzilleri bu kapsamda yeniden dengelenmedi.
- CraftPanel yükseltme listesi yalnız katalogdaki sahip olunan ekipmanları kullanır. Bilinmeyen ID, boşa düşen seçim ve son sahip olunan eşyanın kaldırılması güvenli boş/fallback durumu üretir; artık undefined.id okunmaz. Görsel ile işlemdeki silah seçimi de aynı çözümlenmiş kimliği kullanır.
- Minimap tek kalıcı RAF döngüsüne geçti; snapshot değişince çizim yeniden başlatılmaz. Yerel pozisyon geçerli olmadan sunucu pozisyonu kullanılır. Heading en kısa yayda zaman bazlı yumuşatılır. Yol grid'i dünya koordinatlarına sabit; bina köşeleri/kapıları aynı dönüşümde. Kuzey dünya −Z vektöründen çizilir.

## Testler

Root doğrulaması:

```
npm.cmd test -- --watchAll=false --runInBand CraftPanel.test.jsx HUD.stack.test.jsx minimap.test.js App.settings.test.jsx renderer.test.js
```

5 suite, 18 test geçti. Craft unknown-only, unknown-first/valid-later, snapshot'ta seçimin/son eşyanın kaybolması; normal craft işlemleri; gerçek mounted HUD RAF sürekliliği ve yol hareketi; yön matematiği ve mevcut ayar/model regresyonlarını kapsar.

```
backend/.venv/Scripts/python.exe -m pytest tests/test_boss_territory_focus.py -q
```

5 test geçti. İlk dört test gerçek AI döngüsünde collision/LOS mock'larıyla bölge invariantı, 240 tick kiting, ölüm/güvenli bölge/asker hedefi, leap iptali, eski sınır dışı aktör dönüşü ve respawn ayrımını sınar. Beşinci test gerçek world collision/LOS kullanır: Hansel (80,0), hedef (80,20), hedef sonra (80,100); boss kendi bölgesinde kalıp eve döner, canı değişmez.

Eski `test_boss_features_focus.py` import sırasında eksik `requests` nedeniyle toplanamadı; bu dosyanın tamamı geçti diye raporlanmaz. Aynı çağrıdaki alliance/safezone beş testi geçti. Ortamda xdist mevcut; ayrı territory suite bununla başarıyla çalıştı. Terra production build'i başarıyla tamamladı; önceden var olan optional wagmi modül uyarıları sürüyor.

## Görsel ve yerel kontrol

CUA ile geliştimeye özel `/__dev/minimap-fixture` açıldı: dört boss, bina/kapılar ve yollar, 20 Hz hareket/dönüş, durdurma, sağ yön ve ±π sınır geçişi incelendi. Yol ve bina geometrisi tutarlı kaldı; player merkezde, boss işaretleri doğru çevrede kaldı. Fixture gerçek hesap veya oyun oturumu değiştirmez. Bu kontrollü görsel doğrulamadır; gerçek kullanıcı cüzdanıyla oynanış testi değildir.

Yerel storage gitignored `.local-backups/pre-boss-territory-restart.json` dosyasına yedeklendi. Port 8001 süreci local_run.py olarak doğrulanıp güncel kodla yeniden başlatıldı. Status/market HTTP200 kontrol edildi. Testler gerçek kayıt içeriğini değiştirmedi veya rapora kopyalamadı.
