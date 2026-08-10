import os
import sys
import json
import random
from typing import Dict, Any

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

env_file = os.path.join(os.path.dirname(__file__), ".env")
if os.path.exists(env_file):
    with open(env_file, "r", encoding="utf-8") as f:
        for line in f:
            if "=" in line and not line.startswith("#"):
                key, val = line.strip().split("=", 1)
                os.environ[key] = val

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
from database import log_event

# 8 VIRAL STORY CATEGORIES (100% GLOBAL ENGLISH)
STORY_CATEGORIES = {
    "creepypasta": [
        "Did you know about the entity spotted at 3 AM in Minecraft? A player entered a deserted cave and heard footsteps following him. Suddenly, the screen glitched and Herobrine appeared right behind him!",
        "In 2014, a player found a seed with no animals or mobs. But as night fell, red redstone torches started forming an arrow pointing directly to a dark hole!"
    ],
    "myths_and_secrets": [
        "This hidden Minecraft secret was kept quiet for years! If you place a diamond block under lava in ancient cities, a secret sound triggers that was never meant to be heard!",
        "The rarest event in Roblox Brookhaven just got discovered! Entering the hospital room at midnight unlocks an unreleased secret room under the map!"
    ],
    "hacks_and_glitches": [
        "The fastest level-up glitch in Roblox was just leaked! Stepping into this hidden corner lets you farm 10,000 XP every single second without getting banned!",
        "Only 1% of Minecraft players know this bedrock trick! Using a trapdoor and ender pearl lets you break straight through bedrock in under 3 seconds!"
    ],
    "horror_encounters": [
        "A Roblox streamer was playing alone when a random player named 'Don't Look' joined her private server. Every time she turned around, he got closer without walking!",
        "Never craft a clock at 3 AM in Minecraft! Players who did reported their game audio turning into whisper sounds that followed them even after closing the game!"
    ],
    "pro_vs_noob": [
        "A beginner joined a hardcore Minecraft server pretending to be weak. But when a group of toxic pros tried to trap him, he pulled off a 1v4 crystal PvP clutch!",
        "Noob vs Hacker in Roblox parkour! The hacker used speed cheats, but the pro used physics bounces to win the race at the very last second!"
    ]
}

FALLBACK_METADATA = {
    "minecraft": [
        {
            "title": "THE 3 AM MINECRAFT SECRET 😱 #shorts",
            "description": "Never play Minecraft at 3 AM! Watch until the end to see what happened!",
            "hashtags": "#shorts #minecraft #gaming #viral #creepypasta",
            "hook": "NEVER DO THIS 😱"
        },
        {
            "title": "Bro thought he was completely safe 💀 #shorts",
            "description": "Never lower your guard in Minecraft. Double tap if you agree!",
            "hashtags": "#shorts #minecraft #memes #gamer #funny",
            "hook": "DON'T LOOK BACK 💀"
        }
    ],
    "roblox": [
        {
            "title": "Top 1 Secret in Roblox Nobody Knew! 🤫 #shorts",
            "description": "Did you know this crazy Roblox glitch? Try it out right now!",
            "hashtags": "#shorts #roblox #robloxfunny #gaming",
            "hook": "ROBLOX SECRET EXPOSED 🔥"
        }
    ],
    "default": [
        {
            "title": "UNBELIEVABLE GAMING MOMENT! 🎮 #shorts",
            "description": "Best gameplay highlight of the day. Like & Subscribe!",
            "hashtags": "#shorts #gaming #viral #gamer #trend",
            "hook": "WAIT FOR THE END 🔥"
        }
    ]
}

def generate_metadata(niche: str, language: str = "en", filename: str = "") -> Dict[str, str]:
    """Generates viral title, description, hashtags and hook text using Gemini 1.5 API or Fallback."""
    if GEMINI_API_KEY:
        try:
            import google.generativeai as genai
            genai.configure(api_key=GEMINI_API_KEY)
            model = genai.GenerativeModel("gemini-1.5-flash")

            prompt = f"""
            You are a master viral YouTube Shorts creator for {niche} gaming content.
            Language: 'en'.
            Create a viral YouTube Shorts metadata JSON with exact keys:
            - "title": (Under 60 chars, includes 1 emoji and #shorts)
            - "description": (Engaging 2-sentence description with Call to Action)
            - "hashtags": (5 trending hashtags space separated)
            - "hook": (3-5 words ALL CAPS viral overlay text for top of video, e.g. 'DON'T LOOK BACK 😱')
            Return ONLY raw valid JSON format without markdown code blocks.
            """
            response = model.generate_content(prompt)
            clean_text = response.text.replace("```json", "").replace("```", "").strip()
            return json.loads(clean_text)
        except Exception as e:
            log_event(None, "WARNING", f"Gemini API fallback metadata kullanılıyor: {str(e)}")

    niche_key = "minecraft" if "mc" in niche.lower() or "minecraft" in niche.lower() else ("roblox" if "roblox" in niche.lower() else "default")
    return random.choice(FALLBACK_METADATA.get(niche_key, FALLBACK_METADATA["default"]))

def generate_script(niche: str, language: str = "en") -> str:
    """Generates 25-second viral storytelling AI Voiceover script using Gemini 1.5 API or Story Categories."""
    if GEMINI_API_KEY:
        try:
            import google.generativeai as genai
            genai.configure(api_key=GEMINI_API_KEY)
            model = genai.GenerativeModel("gemini-1.5-flash")

            category = random.choice(["creepypasta", "myths_and_secrets", "horror_encounters", "hacks_and_glitches", "pro_vs_noob"])
            prompt = f"""
            You are a master viral TikTok/Shorts storyteller for {niche} gaming content.
            Write an ultra-engaging 25-second storytelling voiceover script in English ({category} style).
            Requirements:
            - Start with a dramatic 3-second opening hook (e.g., 'No one believed what happened in Minecraft at 3 AM...').
            - Tell a thrilling short story, mystery, creepypasta, or mind-blowing glitch.
            - Include a shocking plot twist in the middle.
            - End with a strong call to action ('Subscribe right now for more secrets!').
            Return ONLY plain text to be spoken by TTS engine. No stage instructions or brackets.
            """
            response = model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            log_event(None, "WARNING", f"Gemini API script fallback kullanılıyor: {str(e)}")

    # Pick a random viral story from our rich 5-category library
    cat = random.choice(list(STORY_CATEGORIES.keys()))
    return random.choice(STORY_CATEGORIES[cat])

if __name__ == "__main__":
    print("Sample Script:", generate_script("minecraft", "en"))
