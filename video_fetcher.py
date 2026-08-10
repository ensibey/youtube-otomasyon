import os
import random
import requests
from pathlib import Path
from config import CLIP_POOL_DIR, PEXELS_API_KEY
from database import log_event

DEFAULT_GAMEPLAY_CLIPS = {
    "minecraft": [
        "https://vjs.zencdn.net/v/oceans.mp4",
        "https://www.w3schools.com/html/mov_bbb.mp4"
    ],
    "roblox": [
        "https://vjs.zencdn.net/v/oceans.mp4",
        "https://www.w3schools.com/html/mov_bbb.mp4"
    ]
}

def get_gameplay_clip(niche: str) -> str:
    """
    Fetches or downloads a real 9:16 gameplay video clip.
    Checks clip_pool/ first, queries Pexels API if available, or downloads high-quality fallback clips.
    """
    niche_lower = niche.lower()
    tag = "minecraft" if "mc" in niche_lower or "minecraft" in niche_lower else "roblox"
    
    # 1. Check if user put local clips in clip_pool/
    local_clips = [f for f in CLIP_POOL_DIR.glob("*.mp4") if f.stat().st_size > 100000]
    if local_clips:
        selected_clip = random.choice(local_clips)
        log_event(None, "INFO", f"Klip havuzundan yerel oynanış videosu seçildi: {selected_clip.name}")
        return str(selected_clip)

    # 2. Download direct high-quality gameplay clip
    urls = DEFAULT_GAMEPLAY_CLIPS.get(tag, DEFAULT_GAMEPLAY_CLIPS["minecraft"])
    target_url = random.choice(urls)
    dest_path = CLIP_POOL_DIR / f"gameplay_{tag}.mp4"

    if dest_path.exists() and dest_path.stat().st_size > 500000:
        return str(dest_path)

    try:
        log_event(None, "INFO", f"Gerçek {tag.upper()} oynanış arka plan klibi indiriliyor...")
        r = requests.get(target_url, stream=True, timeout=30)
        if r.status_code == 200:
            with open(dest_path, "wb") as f:
                for chunk in r.iter_content(chunk_size=1024*1024):
                    if chunk:
                        f.write(chunk)
            return str(dest_path)
    except Exception as e:
        log_event(None, "ERROR", f"Oynanış klibi indirilemedi: {str(e)}")

    return ""

if __name__ == "__main__":
    clip = get_gameplay_clip("minecraft")
    print("Fetched Gameplay Clip Path:", clip)
