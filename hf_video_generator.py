import os
import sys
import shutil
import time
from pathlib import Path
from config import OUTPUT_DIR, CLIP_POOL_DIR
from database import log_event

# Enable UTF-8 for console output
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

# List of free public Hugging Face AI Video Spaces
HF_VIDEO_SPACES = [
    "Lightricks/ltx-video-distilled",
    "OpenKing/wan2-video-generation",
    "mediasynthesismuseum/stable-video-diffusion"
]

def generate_hf_ai_video(prompt: str, niche: str) -> str:
    """
    Generates a 100% free AI video clip using Hugging Face Spaces & gradio_client (Wan / LTX-Video).
    Returns path to downloaded MP4 AI video clip.
    """
    try:
        from gradio_client import Client
        
        full_prompt = f"vertical 9:16 {niche} gameplay cinematic 4k, {prompt}"
        
        for space in HF_VIDEO_SPACES:
            try:
                log_event(None, "INFO", f"Hugging Face AI Video servisine bağlanılıyor: {space}...")
                client = Client(space)
                
                result = None
                try:
                    result = client.predict(full_prompt)
                except Exception:
                    try:
                        result = client.predict(full_prompt, api_name="/predict")
                    except Exception:
                        result = client.predict(full_prompt, "low quality", api_name="/generate")

                if result and isinstance(result, str) and os.path.exists(result):
                    dest_file = CLIP_POOL_DIR / f"hf_ai_video_{int(time.time())}.mp4"
                    shutil.copy(result, str(dest_file))
                    log_event(None, "INFO", f"Hugging Face AI Video başarıyla indirildi: {dest_file.name}")
                    return str(dest_file)
            except Exception as e:
                log_event(None, "WARNING", f"HF Space ({space}) denemesi başarısız oldu: {str(e)[:80]}")
                continue

    except Exception as e:
        log_event(None, "ERROR", f"Hugging Face gradio_client genel hata: {str(e)}")

    # Fallback to gameplay clip if HF spaces are queuing or failing
    from video_fetcher import get_gameplay_clip
    return get_gameplay_clip(niche)

if __name__ == "__main__":
    clip = generate_hf_ai_video("Minecraft Steve walking in 4k forest", "minecraft")
    print("Generated HF AI Video Path:", clip)
