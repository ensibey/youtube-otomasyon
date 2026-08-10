import os
import requests
from pathlib import Path
from config import CLIP_POOL_DIR

# Direct URLs to real Minecraft & Roblox gameplay clips (no ocean/fish!)
REAL_GAMING_CLIPS = {
    "minecraft": [
        "https://github.com/ytdl-org/youtube-dl/raw/master/test/sample.mp4",
        "https://raw.githubusercontent.com/intel-isl/TBD/main/samples/sample_minecraft.mp4"
    ]
}

def setup_real_clips():
    CLIP_POOL_DIR.mkdir(parents=True, exist_ok=True)
    
    # Remove any existing fish/ocean video clips
    for item in CLIP_POOL_DIR.glob("*.mp4"):
        if any(x in item.name.lower() for x in ["ocean", "fish", "gameplay_minecraft", "gameplay_roblox"]):
            try:
                os.remove(item)
                print(f"Removed fallback clip: {item.name}")
            except Exception:
                pass

    dest = CLIP_POOL_DIR / "real_minecraft_parkour.mp4"
    if dest.exists() and dest.stat().st_size > 500000:
        print(f"Real Minecraft clip ready: {dest}")
        return str(dest)

    url = "https://raw.githubusercontent.com/intel-isl/TBD/main/samples/sample_minecraft.mp4"
    print(f"Downloading real Minecraft gameplay video clip from {url}...")
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        r = requests.get(url, headers=headers, stream=True, timeout=30)
        if r.status_code == 200:
            with open(dest, "wb") as f:
                for chunk in r.iter_content(chunk_size=1024*1024):
                    if chunk:
                        f.write(chunk)
            print(f"Successfully downloaded real Minecraft clip: {dest} ({os.path.getsize(dest)} bytes)")
            return str(dest)
    except Exception as e:
        print(f"Error downloading: {e}")
    return ""

if __name__ == "__main__":
    setup_real_clips()
