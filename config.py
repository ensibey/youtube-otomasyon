import os
from pathlib import Path
from pydantic import BaseModel
from typing import Dict, List, Optional

BASE_DIR = Path(__file__).resolve().parent

# Directory Definitions
DOWNLOADS_DIR = BASE_DIR / "downloads"
OUTPUT_DIR = BASE_DIR / "output"
TOKENS_DIR = BASE_DIR / "tokens"
CREDENTIALS_DIR = BASE_DIR / "credentials"
CLIP_POOL_DIR = BASE_DIR / "clip_pool"
DB_PATH = BASE_DIR / "youtube_automation.db"

for folder in [DOWNLOADS_DIR, OUTPUT_DIR, TOKENS_DIR, CREDENTIALS_DIR, CLIP_POOL_DIR]:
    folder.mkdir(parents=True, exist_ok=True)

# Environment Variables
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")
PEXELS_API_KEY = os.getenv("PEXELS_API_KEY", "")

class ChannelConfig(BaseModel):
    id: str
    name: str
    niche: str
    drive_folder_id: Optional[str] = ""
    language: str = "tr"
    daily_target: int = 4
    made_for_kids: bool = False
    voice: str = "tr-TR-AhmetNeural"

# 10 PURE MINECRAFT & ROBLOX AI CHANNELS
DEFAULT_CHANNELS: List[ChannelConfig] = [
    # 5 MINECRAFT AI CHANNELS
    ChannelConfig(id="ch_01", name="Minecraft AI Hikayeleri TR", niche="mc_ai_stories_tr", language="tr", voice="tr-TR-AhmetNeural"),
    ChannelConfig(id="ch_02", name="Minecraft AI Gizemleri TR", niche="mc_ai_myths_tr", language="tr", voice="tr-TR-AhmetNeural"),
    ChannelConfig(id="ch_03", name="Minecraft AI Shorts Global (EN)", niche="mc_ai_global_en", language="en", voice="en-US-ChristopherNeural"),
    ChannelConfig(id="ch_04", name="Minecraft AI Brainrot & Memes", niche="mc_ai_memes", language="tr", voice="tr-TR-AhmetNeural"),
    ChannelConfig(id="ch_05", name="Minecraft AI Satisfying ASMR", niche="mc_ai_asmr", language="en", voice="en-US-AriaNeural"),

    # 5 ROBLOX AI CHANNELS
    ChannelConfig(id="ch_06", name="Roblox AI Hikayeleri TR", niche="roblox_ai_stories_tr", language="tr", voice="tr-TR-EmelNeural"),
    ChannelConfig(id="ch_07", name="Roblox AI Gizli Taktikler TR", niche="roblox_ai_hacks_tr", language="tr", voice="tr-TR-AhmetNeural"),
    ChannelConfig(id="ch_08", name="Roblox AI Confessions (EN)", niche="roblox_ai_global_en", language="en", voice="en-US-JennyNeural"),
    ChannelConfig(id="ch_09", name="Roblox AI Brookhaven Sırları", niche="roblox_ai_brookhaven", language="tr", voice="tr-TR-EmelNeural"),
    ChannelConfig(id="ch_10", name="Roblox vs Minecraft AI Battles", niche="roblox_ai_versus", language="tr", voice="tr-TR-AhmetNeural"),
]

VOICES = {
    "tr_male": "tr-TR-AhmetNeural",
    "tr_female": "tr-TR-EmelNeural",
    "en_male_kid": "en-US-ChristopherNeural",
    "en_male": "en-US-GuyNeural",
    "en_female": "en-US-JennyNeural",
}
