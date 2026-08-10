import sys
import os
import argparse

# Enable UTF-8 encoding for Windows PowerShell / CMD console output
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from database import init_db, get_channels, log_event
from automation_engine import run_channel_pipeline, run_all_channels_pipeline
from telegram_bot import run_telegram_bot_poller

def main():
    parser = argparse.ArgumentParser(description="YouTube Shorts 10-Kanal Otomasyon Sistemi")
    parser.add_argument("--run-all", action="store_true", help="10 kanalın tamamı için otomatik video yükleme sürecini çalıştırır.")
    parser.add_argument("--channel", type=str, help="Tek bir kanal ID'si için otomasyonu çalıştırır (örn: ch_01).")
    parser.add_argument("--telegram-bot", action="store_true", help="Telegram komut dinleyici botunu çalıştırır.")
    parser.add_argument("--init-db", action="store_true", help="Veritabanını ve varsayılan 10 kanalı sıfırdan kurar.")

    args = parser.parse_args()

    # Always ensure DB is initialized
    init_db()

    if args.init_db:
        print("✅ Veritabanı ve 10 varsayılan kanal başarıyla oluşturuldu.")
        channels = get_channels()
        for ch in channels:
            print(f"  • [{ch['id']}] {ch['name']} ({ch['niche']})")
        return

    if args.telegram_bot:
        print("🤖 Telegram Bot Poller Başlatılıyor...")
        run_telegram_bot_poller()
        return

    if args.channel:
        print(f"🚀 Kanal için otomasyon başlatılıyor: {args.channel}")
        result = run_channel_pipeline(args.channel)
        print("Sonuç:", result)
        return

    # Default action if no flag or --run-all is passed
    print("🚀 10 Kanal YouTube Otomasyon Pipeline'ı Çalıştırılıyor...")
    results = run_all_channels_pipeline()
    print(f"\n✅ İşlem Tamamlandı. Toplam Çalıştırılan Kanal: {len(results)}")
    for res in results:
        status_icon = "✅" if res.get("success") else "❌"
        ch_name = res.get("channel", "Kanal")
        url_or_err = res.get("url") or res.get("error")
        print(f"  {status_icon} {ch_name}: {url_or_err}")

if __name__ == "__main__":
    main()
