import os
import sys
import time
import requests
from pathlib import Path

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

COLAB_API_URL = os.getenv("COLAB_API_URL", "")

def request_colab_ai_video(prompt: str, niche: str = "minecraft") -> str:
    """
    Sends an HTTP POST request to live Google Colab ngrok API to generate 9:16 AI Video.
    Returns path to downloaded MP4 clip.
    """
    colab_url = os.getenv("COLAB_API_URL", "").strip().rstrip("/")
    if not colab_url:
        log_event(None, "WARNING", "COLAB_API_URL .env içinde tanımlı değil. Fallback kullanılıyor.")
        return ""

    endpoint = f"{colab_url}/generate_video"
    payload = {
        "prompt": prompt,
        "niche": niche,
        "width": 576,
        "height": 1024,
        "num_frames": 121
    }

    try:
        log_event(None, "INFO", f"Google Colab Canlı API sunucusuna video isteği atılıyor: {endpoint}...")
        resp = requests.post(endpoint, json=payload, timeout=300)
        
        if resp.status_code == 200:
            dest_file = CLIP_POOL_DIR / f"colab_video_{int(time.time())}.mp4"
            with open(dest_file, "wb") as f:
                f.write(resp.content)
            log_event(None, "INFO", f"Google Colab'dan 9:16 AI Video başarıyla alındı: {dest_file.name}")
            return str(dest_file)
        else:
            log_event(None, "ERROR", f"Colab API Hata Yanıtı: {resp.status_code} - {resp.text}")
    except Exception as e:
        log_event(None, "ERROR", f"Colab API bağlantı hatası: {str(e)}")

    return ""

if __name__ == "__main__":
    test_res = request_colab_ai_video("Cinematic 4k vertical footage of Minecraft Steve exploring ancient city")
    print("Colab Video Output:", test_res)
