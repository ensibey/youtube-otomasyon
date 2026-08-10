import requests
from typing import Optional
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID
from database import log_event, get_channels, get_db

def send_telegram_notification(
    channel_name: str,
    title: str,
    video_url: str,
    filename: str = "",
    status: str = "Success",
    error_msg: str = ""
) -> bool:
    """
    Sends real-time notification to user's Telegram chat or group.
    """
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        log_event(None, "WARNING", "Telegram BOT_TOKEN veya CHAT_ID tanımlı değil. Telegram bildirimi atlandı.")
        print(f"[TELEGRAM NOTIFICATION MOCK] {channel_name} | {title} | {video_url}")
        return False

    status_icon = "✅" if status.lower() == "success" else "❌"
    
    message = (
        f"🎬 **[{channel_name}] Shorts Yüklendi!**\n\n"
        f"📌 **Başlık:** {title}\n"
        f"🔗 **YouTube Shorts Linki:** {video_url}\n"
        f"📂 **Drive Dosyası:** `{filename}`\n"
        f"⚡ **Durum:** {status_icon} {status}\n"
    )
    if error_msg:
        message += f"⚠️ **Hata Detayı:** {error_msg}\n"

    telegram_api_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown",
        "disable_web_page_preview": False
    }

    try:
        response = requests.post(telegram_api_url, json=payload, timeout=10)
        if response.status_code == 200:
            log_event(None, "INFO", f"Telegram bildirimi gönderildi: {channel_name}")
            return True
        else:
            log_event(None, "ERROR", f"Telegram API hatası: {response.text}")
            return False
    except Exception as e:
        log_event(None, "ERROR", f"Telegram mesajı atılamadı: {str(e)}")
        return False

def run_telegram_bot_poller():
    """Starts Telegram Bot Command Poller for /status, /channels, /upload."""
    if not TELEGRAM_BOT_TOKEN:
        log_event(None, "WARNING", "Telegram BOT_TOKEN ayarlanmadığı için Komut Poller başlatılmadı.")
        return

    try:
        from telegram import Update
        from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

        async def start_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
            await update.message.reply_text(
                "🤖 **YouTube Otomasyon Telegram Botu Aktif!**\n\n"
                "Kullanılabilir komutlar:\n"
                "/status - Genel sistem durumu ve bekleyen videolar\n"
                "/channels - 10 Kanal listesi\n"
                "/upload - Manuel yükleme tetikle",
                parse_mode="Markdown"
            )

        async def status_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
            with get_db() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT count(*) as total FROM videos WHERE status = 'uploaded'")
                uploaded_count = cursor.fetchone()["total"]
                cursor.execute("SELECT count(*) as total FROM videos WHERE status = 'pending'")
                pending_count = cursor.fetchone()["total"]

            msg = f"📊 **Sistem Özeti**\n\n✅ Yüklenen Toplam Shorts: {uploaded_count}\n⏳ İşlenecek Bekleyen Video: {pending_count}"
            await update.message.reply_text(msg, parse_mode="Markdown")

        async def channels_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
            channels = get_channels()
            msg = "📺 **Kayıtlı 10 YouTube Kanalı:**\n\n"
            for ch in channels:
                msg += f"• **{ch['name']}** ({ch['niche']}) - Dil: {ch['language']}\n"
            await update.message.reply_text(msg, parse_mode="Markdown")

        app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
        app.add_handler(CommandHandler("start", start_cmd))
        app.add_handler(CommandHandler("status", status_cmd))
        app.add_handler(CommandHandler("channels", channels_cmd))

        log_event(None, "INFO", "Telegram Bot Komut Dinleyicisi başlatıldı...")
        app.run_polling()
    except Exception as e:
        log_event(None, "ERROR", f"Telegram Bot başlatma hatası: {str(e)}")

if __name__ == "__main__":
    send_telegram_notification(
        "Minecraft Shorts #01",
        "Bro thought he was safe in Minecraft 💀 #shorts",
        "https://youtube.com/shorts/test_id",
        "mc_video_01.mp4"
    )
