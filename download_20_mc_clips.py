import os
import sys
import subprocess
from pathlib import Path

sys.path.insert(0, r"c:\Users\hp\Desktop\youtube otomasyon")
from config import CLIP_POOL_DIR

def download_clip_library():
    CLIP_POOL_DIR.mkdir(parents=True, exist_ok=True)
    print("Downloading 5 fresh Minecraft Parkour gameplay clips into clip_pool...")

    cmd = [
        "python", "-m", "yt_dlp",
        "ytsearch5:Minecraft parkour gameplay 60fps no copyright",
        "-f", "b[ext=mp4][height<=1080]/b[height<=720]/best",
        "-o", str(CLIP_POOL_DIR / "mc_parkour_%(id)s.mp4")
    ]
    try:
        subprocess.run(cmd, check=True)
        print("Successfully downloaded clip library!")
    except Exception as e:
        print(f"Error downloading clips: {e}")

if __name__ == "__main__":
    download_clip_library()
