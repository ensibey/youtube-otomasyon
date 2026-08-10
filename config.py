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

# 10 VIRAL HIGH-RETENTION CHANNELS CONFIGURATION
DEFAULT_CHANNELS: List[ChannelConfig] = [
    ChannelConfig(id="ch_01", name="Craft Gizemleri TR", niche="minecraft_myths", language="tr", voice="tr-TR-AhmetNeural"),
    ChannelConfig(id="ch_02", name="CraftStories HQ (EN)", niche="minecraft_stories", language="en", voice="en-US-ChristopherNeural"),
    ChannelConfig(id="ch_03", name="BloxTR Shorts", niche="roblox_bugs", language="tr", voice="tr-TR-AhmetNeural"),
    ChannelConfig(id="ch_04", name="BloxConfessions (EN)", niche="roblox_drama", language="en", voice="en-US-JennyNeural"),
    ChannelConfig(id="ch_05", name="BrainrotCraft Shorts", niche="brainrot_memes", language="tr", voice="tr-TR-AhmetNeural"),
    ChannelConfig(id="ch_06", name="GTA Rampage Shorts", niche="gta_stunts", language="tr", voice="tr-TR-AhmetNeural"),
    ChannelConfig(id="ch_07", name="Satisfying Gaming ASMR", niche="satisfying_asmr", language="en", voice="en-US-AriaNeural"),
    ChannelConfig(id="ch_08", name="VsGaming Shorts", niche="gaming_versus", language="tr", voice="tr-TR-AhmetNeural"),
    ChannelConfig(id="ch_09", name="ProGamer Taktik", niche="pro_hacks", language="tr", voice="tr-TR-AhmetNeural"),
    ChannelConfig(id="ch_10", name="Komik Oyun Anları", niche="funny_fails", language="tr", voice="tr-TR-EmelNeural"),
]

VOICES = {
    "tr_male": "tr-TR-AhmetNeural",
    "tr_female": "tr-TR-EmelNeural",
    "en_male_kid": "en-US-ChristopherNeural",
    "en_male": "en-US-GuyNeural",
    "en_female": "en-US-JennyNeural",
}
