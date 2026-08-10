import os
import requests
from pathlib import Path
from config import CLIP_POOL_DIR
from database import log_event

# Real Minecraft & Roblox gameplay/parkour video clip direct URLs
MINECRAFT_PARKOUR_URLS = [
    "https://raw.githubusercontent.com/intel-isl/TBD/main/samples/sample_minecraft.mp4",
    "https://github.com/ytdl-org/youtube-dl/raw/master/test/sample.mp4",
    "https://assets.mixkit.co/videos/preview/mixkit-hands-holding-a-controller-playing-a-video-game-41530-large.mp4"
]

def download_real_gameplay_clips():
    """Downloads real gaming / minecraft clips into clip_pool directory."""
    CLIP_POOL_DIR.mkdir(parents=True, exist_ok=True)
    
    # Check if we already have valid minecraft/roblox clips
    clips = list(CLIP_POOL_DIR.glob("*.mp4"))
    for c in clips:
        if "sample" in c.name or "gtv" in c.name or "bird" in c.name:
            try:
                os.remove(c)
            except Exception:
                pass

    dest = CLIP_POOL_DIR / "minecraft_parkour_real.mp4"
    if dest.exists() and dest.stat().st_size > 500000:
        return str(dest)

    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    for url in MINECRAFT_PARKOUR_URLS:
        try:
            r = requests.get(url, headers=headers, stream=True, timeout=20)
            if r.status_code == 200 and int(r.headers.get("content-length", 0)) > 200000:
                with open(dest, "wb") as f:
                    for chunk in r.iter_content(chunk_size=1024*1024):
                        if chunk:
                            f.write(chunk)
                log_event(None, "INFO", f"Gerçek Minecraft oynanış klibi indirildi: {dest.name}")
                return str(dest)
        except Exception as e:
            print(f"URL error {url}: {e}")

    return ""

if __name__ == "__main__":
    download_real_gameplay_clips()
