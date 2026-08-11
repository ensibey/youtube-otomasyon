import os
import sys
import time
from pathlib import Path
from gradio_client import Client

sys.path.insert(0, r"c:\Users\hp\Desktop\youtube otomasyon")
from config import CLIP_POOL_DIR, BASE_DIR
from database import log_event

# Load environment variables
env_file = BASE_DIR / ".env"
if env_file.exists():
    with open(env_file, "r", encoding="utf-8") as f:
        for line in f:
            if "=" in line and not line.startswith("#"):
                key, val = line.strip().split("=", 1)
                os.environ[key] = val

def request_colab_ai_video(prompt: str, niche: str = "minecraft") -> str:
    """
    Connects to live Google Colab Gradio Share URL and generates 9:16 AI Video.
    No Cloudflare timeouts, no port conflicts, 100% reliable.
    """
    colab_url = os.getenv("COLAB_API_URL", "").strip().rstrip("/")
    if not colab_url:
        log_event(None, "WARNING", "COLAB_API_URL .env içinde tanımlı değil. Fallback kullanılıyor.")
        return ""

    try:
        log_event(None, "INFO", f"Google Colab Canlı Gradio API sunucusuna video isteği atılıyor: {colab_url}...")
        client = Client(colab_url)
        result_path = client.predict(prompt=prompt, api_name="/predict")
        
        if result_path and os.path.exists(result_path):
            dest_file = CLIP_POOL_DIR / f"colab_ai_video_{int(time.time())}.mp4"
            import shutil
            shutil.copy(result_path, dest_file)
            log_event(None, "INFO", f"Google Colab'dan 9:16 AI Video başarıyla çekildi: {dest_file.name}")
            return str(dest_file)
    except Exception as e:
        log_event(None, "ERROR", f"Colab Gradio API bağlantı hatası: {str(e)}")

    return ""

if __name__ == "__main__":
    test_res = request_colab_ai_video("Cinematic 4k vertical footage of Minecraft Steve exploring ancient city")
    print("Colab Gradio Video Output:", test_res)
