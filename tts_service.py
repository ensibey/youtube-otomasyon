import os
import sys
import asyncio
import requests
import edge_tts
from pathlib import Path
from config import OUTPUT_DIR, VOICES
from database import log_event

ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY", "")

async def _generate_edge_tts_async(text: str, voice: str, output_path: str):
    """Generates audio using Microsoft Edge Multilingual Neural Voices with dynamic pitch/rate."""
    # Use Multilingual Andrew or Emel for ultra realistic human cadence
    selected_voice = voice
    if "Ahmet" in voice:
        selected_voice = "en-US-AndrewMultilingualNeural"  # Realistic deep male voice with Turkish support
    elif "Emel" in voice:
        selected_voice = "en-US-AvaMultilingualNeural"

    communicate = edge_tts.Communicate(text, selected_voice, rate="+3%", pitch="+0Hz")
    await communicate.save(output_path)

def generate_elevenlabs_voice(text: str, voice_id: str = "21m00Tcm4TlvDq8ikWAM", output_path: str = "") -> bool:
    """Generates 100% realistic human voiceover using ElevenLabs API."""
    if not ELEVENLABS_API_KEY:
        return False
    try:
        url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
        headers = {
            "Accept": "audio/mpeg",
            "Content-Type": "application/json",
            "xi-api-key": ELEVENLABS_API_KEY
        }
        data = {
            "text": text,
            "model_id": "eleven_multilingual_v2",
            "voice_settings": {"stability": 0.5, "similarity_boost": 0.75}
        }
        resp = requests.post(url, json=data, headers=headers, timeout=30)
        if resp.status_code == 200:
            with open(output_path, "wb") as f:
                f.write(resp.content)
            log_event(None, "INFO", "ElevenLabs ultra-gerçekçi insan seslendirmesi oluşturuldu.")
            return True
        else:
            log_event(None, "WARNING", f"ElevenLabs API yanıtı: {resp.status_code} - {resp.text}")
    except Exception as e:
        log_event(None, "ERROR", f"ElevenLabs seslendirme hatası: {str(e)}")
    return False

def generate_voiceover(text: str, voice: str = "tr-TR-AhmetNeural", output_filename: str = "voiceover.mp3") -> str:
    """
    Generates high-quality AI voiceover.
    Uses ElevenLabs if API key is provided, or Microsoft Multilingual Neural AI voices as fallback.
    """
    output_path = OUTPUT_DIR / output_filename

    # 1. Try ElevenLabs API if key is present
    if ELEVENLABS_API_KEY:
        success = generate_elevenlabs_voice(text, output_path=str(output_path))
        if success:
            return str(output_path)

    # 2. Fallback to Microsoft Multilingual Neural AI Voice Engine
    try:
        asyncio.run(_generate_edge_tts_async(text, voice, str(output_path)))
        log_event(None, "INFO", f"Multilingual Neural AI Seslendirme oluşturuldu: {output_filename}")
        return str(output_path)
    except Exception as e:
        log_event(None, "ERROR", f"Edge-TTS seslendirme hatası: {str(e)}")

    return ""

if __name__ == "__main__":
    sample = "Minecraft'ın bu gizli sırrını kimse bilmiyordu. Gece saat üçte madene inen oyuncuların başına gelen inanılmaz olay!"
    res = generate_voiceover(sample, "tr-TR-AhmetNeural", "test_human_voice.mp3")
    print("Voiceover Output:", res)
