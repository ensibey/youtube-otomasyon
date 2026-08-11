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

def request_colab_ai_video(prompt: str, niche: str = "minecraft") -> str:
    """
    Sends an HTTP POST request to live Google Colab API using Async Job Polling.
    Prevents Cloudflare 524 Timeout errors completely.
    """
    colab_url = os.getenv("COLAB_API_URL", "").strip().rstrip("/")
    if not colab_url:
        log_event(None, "WARNING", "COLAB_API_URL .env içinde tanımlı değil. Fallback kullanılıyor.")
        return ""

    start_ep = f"{colab_url}/start_generation"
    payload = {
        "prompt": prompt,
        "niche": niche,
        "width": 256,
        "height": 448
    }

    try:
        log_event(None, "INFO", f"Google Colab Canlı API sunucusuna video görevi gönderiliyor: {start_ep}...")
        resp = requests.post(start_ep, json=payload, timeout=15)
        
        if resp.status_code == 200:
            data = resp.json()
            job_id = data.get("job_id")
            log_event(None, "INFO", f"Google Colab Görevi Başlatıldı (Job ID: {job_id}). Durum kontrol ediliyor...")

            status_ep = f"{colab_url}/job_status/{job_id}"
            for attempt in range(60):  # max 5 minutes wait
                time.sleep(5)
                st_resp = requests.get(status_ep, timeout=10)
                if st_resp.status_code == 200:
                    st_data = st_resp.json()
                    status = st_data.get("status")
                    print(f"Polling Colab Job [{job_id}] -> Status: {status} ({attempt * 5}s)")
                    
                    if status == "completed":
                        dl_ep = f"{colab_url}/download_video/{job_id}"
                        dl_resp = requests.get(dl_ep, timeout=30)
                        if dl_resp.status_code == 200:
                            dest_file = CLIP_POOL_DIR / f"colab_video_{int(time.time())}.mp4"
                            with open(dest_file, "wb") as f:
                                f.write(dl_resp.content)
                            log_event(None, "INFO", f"Google Colab'dan 9:16 AI Video başarıyla indirildi: {dest_file.name}")
                            return str(dest_file)
                    elif status == "failed":
                        log_event(None, "ERROR", f"Colab Video Üretim Hatası: {st_data.get('error')}")
                        break
        else:
            log_event(None, "ERROR", f"Colab API Başlatma Hatası: {resp.status_code} - {resp.text}")
    except Exception as e:
        log_event(None, "ERROR", f"Colab API bağlantı hatası: {str(e)}")

    return ""

if __name__ == "__main__":
    test_res = request_colab_ai_video("Cinematic 4k vertical footage of Minecraft Steve exploring ancient city")
    print("Colab Video Output:", test_res)
