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
    niche: str  # e.g., "minecraft", "roblox", "gta", "brainrot"
    drive_folder_id: Optional[str] = ""
    language: str = "tr"  # "tr" or "en"
    daily_target: int = 4
    made_for_kids: bool = False
    voice: str = "tr-TR-AhmetNeural"  # Default Edge TTS voice

# Default 10 Channels Configuration
DEFAULT_CHANNELS: List[ChannelConfig] = [
    ChannelConfig(id="ch_01", name="Minecraft Shorts TR #1", niche="minecraft", language="tr", voice="tr-TR-AhmetNeural"),
    ChannelConfig(id="ch_02", name="Minecraft Shorts TR #2", niche="minecraft", language="tr", voice="tr-TR-EmelNeural"),
    ChannelConfig(id="ch_03", name="Roblox Stories TR #1", niche="roblox", language="tr", voice="tr-TR-AhmetNeural"),
    ChannelConfig(id="ch_04", name="Roblox Stories TR #2", niche="roblox", language="tr", voice="tr-TR-EmelNeural"),
    ChannelConfig(id="ch_05", name="Gaming Myths & Secrets", niche="gaming_myths", language="en", voice="en-US-ChristopherNeural"),
    ChannelConfig(id="ch_06", name="Minecraft Hacks EN", niche="minecraft", language="en", voice="en-US-GuyNeural"),
    ChannelConfig(id="ch_07", name="Roblox Funny Moments EN", niche="roblox", language="en", voice="en-US-JennyNeural"),
    ChannelConfig(id="ch_08", name="Brainrot & Memes TR", niche="brainrot", language="tr", voice="tr-TR-AhmetNeural"),
    ChannelConfig(id="ch_09", name="Satisfying Gaming Shorts", niche="satisfying", language="en", voice="en-US-AriaNeural"),
    ChannelConfig(id="ch_10", name="GTA 5 Stunts & Shorts", niche="gta", language="tr", voice="tr-TR-AhmetNeural"),
]

# Preferred Edge-TTS Voices
VOICES = {
    "tr_male": "tr-TR-AhmetNeural",
    "tr_female": "tr-TR-EmelNeural",
    "en_male_kid": "en-US-ChristopherNeural",
    "en_male": "en-US-GuyNeural",
    "en_female": "en-US-JennyNeural",
}
