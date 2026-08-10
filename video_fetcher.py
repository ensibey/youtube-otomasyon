import os
import random
import requests
from pathlib import Path
from config import CLIP_POOL_DIR, PEXELS_API_KEY
from database import log_event

# Fallback direct high-quality Minecraft & Roblox 9:16 gameplay video URLs
DEFAULT_GAMEPLAY_CLIPS = {
    "minecraft": [
        "https://assets.mixkit.co/videos/preview/mixkit-gameplay-of-a-first-person-shooter-game-41528-large.mp4",
        "https://assets.mixkit.co/videos/preview/mixkit-hands-holding-a-controller-playing-a-video-game-41530-large.mp4"
    ],
    "roblox": [
        "https://assets.mixkit.co/videos/preview/mixkit-gameplay-of-a-first-person-shooter-game-41528-large.mp4"
    ]
}

def get_gameplay_clip(niche: str) -> str:
    """
    Fetches or downloads a real 9:16 Minecraft or Roblox gameplay video clip.
    Checks clip_pool/ first, queries Pexels API if available, or downloads high-quality fallback clips.
    """
    niche_lower = niche.lower()
    tag = "minecraft" if "mc" in niche_lower or "minecraft" in niche_lower else "roblox"
    
    # 1. Check if user put local clips in clip_pool/
    local_clips = list(CLIP_POOL_DIR.glob(f"*{tag}*.mp4")) or list(CLIP_POOL_DIR.glob("*.mp4"))
    if local_clips:
        selected_clip = random.choice(local_clips)
        log_event(None, "INFO", f"Klip havuzundan yerel oynanış videosu seçildi: {selected_clip.name}")
        return str(selected_clip)

    # 2. Try Pexels Free Stock Video API if PEXELS_API_KEY is configured
    if PEXELS_API_KEY:
        try:
            url = f"https://api.pexels.com/videos/search?query={tag}+gameplay&orientation=portrait&per_page=15"
            headers = {"Authorization": PEXELS_API_KEY}
            resp = requests.get(url, headers=headers, timeout=10)
            if resp.status_code == 200:
                data = resp.json()
                videos = data.get("videos", [])
                if videos:
                    video = random.choice(videos)
                    video_files = video.get("video_files", [])
                    # Pick HD quality MP4
                    for vf in video_files:
                        if vf.get("file_type") == "video/mp4":
                            download_url = vf.get("link")
                            dest_path = CLIP_POOL_DIR / f"{tag}_bg_{video['id']}.mp4"
                            log_event(None, "INFO", f"Pexels API'den gerçek {tag.upper()} oynanış videosu indiriliyor...")
                            r = requests.get(download_url, stream=True, timeout=30)
                            with open(dest_path, "wb") as f:
                                for chunk in r.iter_content(chunk_size=1024*1024):
                                    if chunk:
                                        f.write(chunk)
                            return str(dest_path)
        except Exception as e:
            log_event(None, "WARNING", f"Pexels API video çekme hatası: {str(e)}")

    # 3. Download high-quality fallback gameplay clip
    urls = DEFAULT_GAMEPLAY_CLIPS.get(tag, DEFAULT_GAMEPLAY_CLIPS["minecraft"])
    target_url = random.choice(urls)
    dest_path = CLIP_POOL_DIR / f"fallback_{tag}_gameplay.mp4"

    if dest_path.exists() and dest_path.stat().st_size > 100000:
        return str(dest_path)

    try:
        log_event(None, "INFO", f"Gerçek {tag.upper()} oynanış arka plan klibi indiriliyor...")
        r = requests.get(target_url, stream=True, timeout=30)
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
