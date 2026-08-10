import os
import random
import requests
from pathlib import Path
from config import CLIP_POOL_DIR
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
    Returns a real gameplay video clip from clip_pool/ or downloads open sample video.
    """
    niche_lower = niche.lower()
    tag = "minecraft" if any(k in niche_lower for k in ["mc", "minecraft", "craft"]) else "roblox"

    # 1. Check existing MP4 clips in clip_pool/
    local_clips = [f for f in CLIP_POOL_DIR.glob("*.mp4") if f.stat().st_size > 100000]
    if local_clips:
        selected = random.choice(local_clips)
        log_event(None, "INFO", f"Klip havuzundan oynanış klibi seçildi: {selected.name}")
        return str(selected)

    # 2. Download high quality gameplay clip
    urls = DEFAULT_GAMEPLAY_CLIPS.get(tag, DEFAULT_GAMEPLAY_CLIPS["minecraft"])
    target_url = random.choice(urls)
    dest_path = CLIP_POOL_DIR / f"gameplay_{tag}.mp4"

    try:
        log_event(None, "INFO", f"Arka plan klibi indiriliyor: {target_url}...")
        r = requests.get(target_url, stream=True, timeout=30)
        if r.status_code == 200:
            with open(dest_path, "wb") as f:
                for chunk in r.iter_content(chunk_size=1024*1024):
                    if chunk:
                        f.write(chunk)
            log_event(None, "INFO", f"Klip indirildi: {dest_path.name}")
            return str(dest_path)
    except Exception as e:
        log_event(None, "ERROR", f"Oynanış klibi indirme hatası: {str(e)}")

    return ""

if __name__ == "__main__":
    clip = get_gameplay_clip("minecraft")
    print("Selected Clip Path:", clip)
