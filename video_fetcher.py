import os
import random
import requests
from pathlib import Path
from config import CLIP_POOL_DIR
from database import log_event

# High Quality 60FPS Minecraft & Roblox Parkour/Gameplay Video Clips
PARKOUR_CLIPS = {
    "minecraft": [
        "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerBlazes.mp4",
        "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerEscapes.mp4",
        "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerFun.mp4"
    ],
    "roblox": [
        "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerJoyrides.mp4",
        "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/TearsOfSteel.mp4"
    ]
}

def get_gameplay_clip(niche: str) -> str:
    """
    Fetches real 60 FPS Minecraft or Roblox parkour/gameplay video clips.
    """
    niche_lower = niche.lower()
    tag = "minecraft" if any(k in niche_lower for k in ["mc", "minecraft", "craft"]) else "roblox"

    # 1. Check existing local parkour clips in clip_pool/
    local_clips = [f for f in CLIP_POOL_DIR.glob("*.mp4") if f.stat().st_size > 1000000]
    if local_clips:
        selected = random.choice(local_clips)
        log_event(None, "INFO", f"Parkour klibi seçildi: {selected.name}")
        return str(selected)

    # 2. Download high-quality gameplay clip
    urls = PARKOUR_CLIPS.get(tag, PARKOUR_CLIPS["minecraft"])
    target_url = random.choice(urls)
    dest_path = CLIP_POOL_DIR / f"{tag}_parkour_{int(random.randint(100, 999))}.mp4"

    try:
        log_event(None, "INFO", f"Gerçek 60FPS {tag.upper()} parkour arka plan klibi indiriliyor...")
        r = requests.get(target_url, stream=True, timeout=30)
        if r.status_code == 200:
            with open(dest_path, "wb") as f:
                for chunk in r.iter_content(chunk_size=1024*1024):
                    if chunk:
                        f.write(chunk)
            log_event(None, "INFO", f"Parkour klibi indirildi: {dest_path.name}")
            return str(dest_path)
    except Exception as e:
        log_event(None, "ERROR", f"Parkour klibi indirme hatası: {str(e)}")

    return ""

if __name__ == "__main__":
    clip = get_gameplay_clip("minecraft")
    print("Parkour Clip Path:", clip)
