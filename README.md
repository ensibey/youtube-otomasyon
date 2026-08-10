# 🚀 YouTube Shorts 10-Kanal Otomasyon Sistemi

Bu proje, 10 farklı YouTube çocuk/oyun kanalı (Minecraft, Roblox, GTA, Brainrot vb.) için **Google Drive Entegrasyonlu**, **9:16 Shorts Video Editli**, **AI Başlık & Seslendirme Destekli** ve **Telegram Bildirimli** otomatik video yayınlama sistemidir.

---

## 🌟 Ana Özellikler

- 📁 **Google Drive Senkronizasyonu:** Her kanalın Drive klasöründen videoları otomatik çeker, yüklendikten sonra `Uploaded` klasörüne arşivler.
- 🎬 **Otomatik 9:16 Shorts Kırpma & Hook:** Videoları YouTube Shorts formatına çevirir, üst tarafına dikkat çekici başlık şeritleri basar.
- 🗣️ **%100 Ücretsiz AI Seslendirme (Edge-TTS):** Microsoft Edge Neural Voices ile doğal Türkçe/İngilizce seslendirme üretir.
- 🧠 **Gemini 1.5 AI SEO Engine:** Viral başlıklar, açıklamalar ve `#shorts` etiketleri oluşturur.
- 🤖 **Telegram Bot Bildirimleri:** Yüklenen videoların **YouTube Shorts linkini** anında Telegram cebine gönderir.
- ☁️ **GitHub Actions 7/24 Bulut Desteği:** Bilgisayarını açık tutmana gerek kalmadan günde 4 kez ücretsiz çalışır.

---

## 🛠️ Hızlı Kurulum & Kullanım

### 1. Bağımlılıkları Yükleyin

```bash
pip install -r requirements.txt
```

### 2. Veritabanını İlklendirin

```bash
python main.py --init-db
```

### 3. Çevre Değişkenleri (`.env` veya Ortam Değişkenleri)

Sistemin tam kapasite çalışması için aşağıdaki bilgileri ekleyebilirsiniz:

```env
GEMINI_API_KEY=AIzaSy...
TELEGRAM_BOT_TOKEN=123456789:ABC...
TELEGRAM_CHAT_ID=987654321
```

---

## 🚀 Çalıştırma Komutları

- **Tüm 10 Kanal İçin Otomasyonu Çalıştırın:**
  ```bash
  python main.py --run-all
  ```

- **Sadece Tek Bir Kanal İçin Çalıştırın:**
  ```bash
  python main.py --channel ch_01
  ```

- **Telegram Bot Dinleyicisini Başlatın:**
  ```bash
  python main.py --telegram-bot
  ```

---

## ☁️ GitHub Actions İle 7/24 Bulut Kurulumu

1. Kodlarınızı kendi GitHub reponuza yükleyin (`git push`).
2. GitHub Reponuzda **Settings ➔ Secrets and variables ➔ Actions** sekmesine gidin.
3. Şu **New repository secret** değişkenlerini ekleyin:
   - `GEMINI_API_KEY`
   - `TELEGRAM_BOT_TOKEN`
   - `TELEGRAM_CHAT_ID`
   - `CLIENT_SECRET_JSON` (Google Cloud'dan aldığınız `client_secret.json` içeriği)

Artık sistem her gün **09:00, 12:00, 15:00 ve 18:00** saatlerinde otomatik uyanıp videoları YouTube'a yükleyecek ve Telegram'a linkini atacaktır! 🚀
