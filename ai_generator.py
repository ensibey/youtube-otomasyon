import os
import sys
import json
import random
from typing import Dict, Any

# Enable UTF-8 encoding for Windows console
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

# Load environment variables from .env file if present
env_file = os.path.join(os.path.dirname(__file__), ".env")
if os.path.exists(env_file):
    with open(env_file, "r", encoding="utf-8") as f:
        for line in f:
            if "=" in line and not line.startswith("#"):
                key, val = line.strip().split("=", 1)
                os.environ[key] = val

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
from database import log_event

# Fallback presets when API Key is missing or quota exceeded
FALLBACK_METADATA = {
    "minecraft": [
        {
            "title": "NOBODY EXPECTED THIS IN MINECRAFT 😱 #shorts",
            "description": "Crazy Minecraft moment you won't believe! Sub for more daily clips!",
            "hashtags": "#shorts #minecraft #gaming #viral #mcyt",
            "hook": "WAIT FOR THE END! 😱"
        },
        {
            "title": "Bro thought he was completely safe 💀 #shorts",
            "description": "Never lower your guard in Minecraft. Double tap if you agree!",
            "hashtags": "#shorts #minecraft #memes #gamer #funny",
            "hook": "SAKIN SEYRETME! 💀"
        }
    ],
    "roblox": [
        {
            "title": "Top 1 Secret in Roblox Nobody Knew! 🤫 #shorts",
            "description": "Did you know this crazy Roblox trick? Try it out now!",
            "hashtags": "#shorts #roblox #robloxfunny #gaming",
            "hook": "THIS ROBLOX SECRET IS CRAZY! 🔥"
        }
    ],
    "default": [
        {
            "title": "UNBELIEVABLE GAMING MOMENT! 🎮 #shorts",
            "description": "Best gameplay highlight of the day. Like & Subscribe!",
            "hashtags": "#shorts #gaming #viral #gamer #trend",
            "hook": "BEKLE VE GÖR! 🔥"
        }
    ]
}

FALLBACK_SCRIPTS = {
    "minecraft": "Minecraft'ta bu gizli hileyi biliyor muydunuz? Nether portalının yanına blok koyarsanız patlama riskini yarıya indirirsiniz! Daha fazlası için abone olun!",
    "roblox": "Roblox'ta en hızlı seviye atlama taktiği açıklandı! Oyundaki bu gizli kapıdan geçerek 10 kat daha fazla xp kazanabilirsiniz! Takip etmeyi unutmayın!",
    "default": "Oyun dünyasındaki bu inanılmaz anı sonuna kadar izleyin! Abone olmayı ve videoyu beğenmeyi unutmayın!"
}

def generate_metadata(niche: str, language: str = "tr", filename: str = "") -> Dict[str, str]:
    """Generates viral title, description, hashtags and hook text using Gemini 1.5 API or Fallback."""
    if GEMINI_API_KEY:
        try:
            import google.generativeai as genai
            genai.configure(api_key=GEMINI_API_KEY)
            model = genai.GenerativeModel("gemini-1.5-flash")

            prompt = f"""
            You are a YouTube Shorts expert editor for {niche} gaming content.
            Video filename: '{filename}'. Language: '{language}'.
            Create a viral YouTube Shorts metadata JSON with exact keys:
            - "title": (Under 60 chars, includes 1 emoji and #shorts)
            - "description": (Engaging 2-sentence description with Call to Action)
            - "hashtags": (5 trending hashtags space separated)
            - "hook": (3-5 words ALL CAPS viral overlay text for top of video, e.g. 'DON'T DO THIS 😱')
            Return ONLY raw valid JSON format without markdown code blocks.
            """
            
            response = model.generate_content(prompt)
            clean_text = response.text.replace("```json", "").replace("```", "").strip()
            data = json.loads(clean_text)
            return data
        except Exception as e:
            log_event(None, "WARNING", f"Gemini API yanıt vermedi, fallback metadata kullanılıyor: {str(e)}")

    # Fallback Selection
    niche_key = niche if niche in FALLBACK_METADATA else "default"
    selected = random.choice(FALLBACK_METADATA[niche_key])
    return selected

def generate_script(niche: str, language: str = "tr") -> str:
    """Generates 25-second viral storytelling AI Voiceover script using Gemini 1.5 API or Fallback."""
    if GEMINI_API_KEY:
        try:
            import google.generativeai as genai
            genai.configure(api_key=GEMINI_API_KEY)
            model = genai.GenerativeModel("gemini-1.5-flash")

            prompt = f"""
            You are a master viral TikTok/Shorts storyteller for {niche} gaming content.
            Write an ultra-engaging 25-second storytelling voiceover script in '{language}'.
            Requirements:
            - Start with a dramatic 3-second opening hook (e.g. 'Minecraft'ın bu karanlık sırrını kimse bilmiyordu...' or 'Bu Roblox oyuncusu 03:00'da ne gördü?').
            - Tell a thrilling short story, mystery, creepypasta, or mind-blowing trick.
            - Include a shocking plot twist in the middle.
            - End with a strong call to action ('Daha fazlası için takip et!').
            Return ONLY plain text to be spoken by TTS engine. No stage instructions or brackets.
            """
            response = model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            log_event(None, "WARNING", f"Gemini API script üretirken hata aldı, fallback kullanılıyor: {str(e)}")

    return FALLBACK_SCRIPTS.get(niche, FALLBACK_SCRIPTS["default"])

if __name__ == "__main__":
    res = generate_metadata("minecraft", "tr", "mc_gameplay_01.mp4")
    print("Generated Metadata:", json.dumps(res, indent=2, ensure_ascii=False))
