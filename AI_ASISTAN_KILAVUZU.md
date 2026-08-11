# 🚀 YouTube Otomasyon Projesi — AI Asistan Başlangıç Kılavuzu

## 👤 Kullanıcı Hakkında
- **İsim:** Enis Doğan (`@Enis_Dogan`)
- **Telegram Chat ID:** `1215543640`
- **Dil:** Türkçe konuşur, kısa ve net cevap ister
- **Tarz:** Direkt, sabırsız — uzun açıklama istemez, sonuç ister
- **Önemli:** "sen yap, benden bir şey isteme" zihniyetiyle çalışıyor

---

## 🎯 Projenin Amacı

Tamamen otomatik bir YouTube Shorts üretim sistemi:

1. **Gemini AI** → Minecraft/gaming konularında viral script üretir
2. **Edge Neural TTS** → Sesi yapay zeka ile seslendirrir  
3. **Text-to-Video AI (ModelScope 1.7B / FLUX)** → %100 yapay zeka tarafından üretilen video görseli
4. **Video Editor** → Ses + görüntü + altyazı birleştirir, 9:16 Shorts formatına getirir
5. **Telegram Bot (`@YTUzmani_bot`)** → Bitmiş videoyu Enis'in telefonuna gönderir

---

## ⚠️ KRİTİK KULLANICI İSTEĞİ

> **"Görsel clip havuzundan (eski gameplay kayıtları) DEĞİL, %100 yapay zeka tarafından sıfırdan üretilmiş olmalı"**

Kullanıcı bunu defalarca vurguladı. Clip pool (`clip_pool/` klasörü) kesinlikle kullanılmamalı. Görsel ya:
- **ModelScope 1.7B** (Colab GPU üzerinde text-to-video)
- **FLUX AI** (Pollinations API üzerinden image→animated video)

...ile üretilmeli.

---

## 🏗️ Sistem Mimarisi

```
[Kullanıcı]
    |
    | (sadece Colab'da "Run" basar)
    v
[Google Colab - GPU]
    - ModelScope 1.7B Text-to-Video modeli yüklü
    - FastAPI sunucusu port 8000'de çalışır
    - ngrok/Cloudflare tunnel ile dışarıya açılır
    - Sunucu başladığında URL'yi otomatik Telegram'a gönderir
    |
    | (ngrok/trycloudflare public URL)
    v
[Local Windows PC - c:\Users\hp\Desktop\youtube otomasyon\]
    - auto_telegram_colab_pipeline.py URL'yi Telegram'dan okur
    - colab_client.py Colab API'ye istek gönderir
    - AI video klip indirilir
    - tts_service.py → Edge Neural TTS ses üretir
    - ai_generator.py → Gemini ile script + metadata üretir
    - video_editor.py → Hepsini birleştirip 9:16 Shorts yapar
    - Telegram'a sendVideo ile gönderir
    |
    v
[Enis'in Telefonu - Telegram]
    - Hazır video düşer
```

---

## 📁 Proje Dosyaları

| Dosya | Açıklama |
|-------|----------|
| `c:\Users\hp\Desktop\youtube otomasyon\.env` | API anahtarları (COLAB_API_URL, TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID) |
| `colab_client.py` | Colab API'ye bağlanır, async job polling yapar |
| `ai_generator.py` | Gemini AI ile script ve metadata üretir |
| `tts_service.py` | Edge Neural TTS ile seslendirme yapar |
| `video_editor.py` | Video montajı, altyazı, 9:16 crop |
| `generate_colab_notebook.py` | Colab notebook'unu (`.ipynb`) üretir ve GitHub'a push edilir |
| `Youtube_AI_Video_Generator.ipynb` | Google Colab'da çalışan notebook (GitHub'dan açılır) |

---

## 🔑 Kimlik Bilgileri (`.env`)

```env
COLAB_API_URL=https://[canlı-ngrok-url].ngrok-free.app   # Colab her başladığında değişir!
TELEGRAM_BOT_TOKEN=8709377467:AAFMfhaHuGND6rgM4Kxr5Brklvqwn56Ezko
TELEGRAM_CHAT_ID=1215543640
```

> **ÖNEMLİ:** `COLAB_API_URL` her Colab session'ında değişir. Notebook Cell 3 çalıştırıldığında yeni URL Telegram'a otomatik gönderilir, `auto_telegram_colab_pipeline.py` bunu okuyup `.env`'i günceller.

---

## 🤖 Telegram Botu

- **Bot:** `@YTUzmani_bot`
- **Token:** `8709377467:AAFMfhaHuGND6rgM4Kxr5Brklvqwn56Ezko`
- **Chat ID:** `1215543640` (Enis'in özel sohbeti)
- Videoları `sendVideo` API ile gönderir
- Başarılı gönderim → HTTP 200

---

## 🚫 Yapılmaması Gerekenler

1. ❌ `clip_pool/` klasöründen gameplay klip kullanma
2. ❌ Enis'ten URL veya başka bir şey isteme — sistem otomatik olmalı
3. ❌ Cloudflare trycloudflare.com kullan — 524 timeout hatası verir (100sn limit)
4. ❌ Senkron video üretimi isteği gönderme — async job polling kullan
5. ❌ Uzun açıklama yapma — Enis kısa ve net cevap ister

---

## ✅ Çalışan Akış (Son Başarılı Test)

1. FLUX AI (Pollinations) → `image.pollinations.ai/prompt/...` ile AI görsel çizildi
2. OpenCV ile 3D zoom animasyonu yapıldı → 12 saniyelik MP4
3. Gemini script + Edge TTS ses eklendi
4. Telegram'a gönderildi → **HTTP 200, Message ID: 93** ✅

---

## 🔄 Colab Notebook Akışı

Colab URL'i her session'da değişir. Çözüm:

1. Kullanıcı Colab'da **Cell 3'ü çalıştırır**
2. Notebook ngrok URL'ini alır
3. **Otomatik Telegram'a URL mesajı gönderir**
4. Local script (`auto_telegram_colab_pipeline.py`) Telegram'ı dinler
5. URL gelince `.env`'e yazar, video üretimine başlar

---

## 💡 Bir Sonraki AI Asistan İçin Öneriler

- Önce `.env` dosyasını oku, `COLAB_API_URL`'nin canlı olup olmadığını test et
- Canlı değilse: Enis'e Colab Cell 3'ü çalıştırmasını söyle (tek isteyebileceğin şey bu)
- URL geldikten sonra tamamen otomatik çalış
- Video üretiminde mutlaka AI görsel kullan (FLUX veya ModelScope)
- Her video Telegram'a gönderilmeli
- Hata olursa Enis'e sormadan alternatif yöntem dene
