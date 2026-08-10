import asyncio
import edge_tts
from pathlib import Path
from config import OUTPUT_DIR, VOICES
from database import log_event

async def _generate_audio_async(text: str, voice: str, output_path: str):
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(output_path)

def generate_voiceover(text: str, voice: str = "tr-TR-AhmetNeural", output_filename: str = "voiceover.mp3") -> str:
    """
    Generates high-quality neural AI voiceover using free edge-tts.
    Returns absolute path to generated MP3 audio file.
    """
    output_path = OUTPUT_DIR / output_filename
    try:
        asyncio.run(_generate_audio_async(text, voice, str(output_path)))
        log_event(None, "INFO", f"AI Seslendirme başarıyla oluşturuldu: {output_filename}")
        return str(output_path)
    except Exception as e:
        log_event(None, "ERROR", f"Edge-TTS seslendirme hatası: {str(e)}")
        return ""

if __name__ == "__main__":
    sample_text = "Minecraft dünyasındaki bu gizli hileyi biliyor muydunuz? Abone olmayı unutmayın!"
    audio_file = generate_voiceover(sample_text, "tr-TR-AhmetNeural", "test_voice.mp3")
    print("Generated Audio File:", audio_file)
