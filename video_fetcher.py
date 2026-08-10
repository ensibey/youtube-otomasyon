import os
import random
import requests
from pathlib import Path
from config import CLIP_POOL_DIR
from database import log_event

def get_gameplay_clip(niche: str) -> str:
    """
    Returns a real Minecraft/Roblox gameplay video clip from clip_pool/ directory.
    User can drop any .mp4 gameplay/parkour files into clip_pool/ for custom videos.
    """
    niche_lower = niche.lower()
    tag = "minecraft" if any(k in niche_lower for k in ["mc", "minecraft", "craft"]) else "roblox"

    # Fetch all valid MP4 clips in clip_pool/
    clips = [f for f in CLIP_POOL_DIR.glob("*.mp4") if f.stat().st_size > 100000]
    
    # Filter tag specific clips if available
    tag_clips = [f for f in clips if tag in f.name.lower()]
    pool = tag_clips if tag_clips else clips

    if pool:
        selected = random.choice(pool)
        log_event(None, "INFO", f"Klip havuzundan oynanış klibi seçildi: {selected.name}")
        return str(selected)

    log_event(None, "WARNING", "clip_pool klasöründe henüz .mp4 oynanış videosu bulunamadı.")
    return ""

if __name__ == "__main__":
    clip = get_gameplay_clip("minecraft")
    print("Selected Clip Path:", clip)
