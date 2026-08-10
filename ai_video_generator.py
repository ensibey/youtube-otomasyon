import os
import time
import random
import requests
import urllib.parse
from pathlib import Path
from config import OUTPUT_DIR, CLIP_POOL_DIR
from database import log_event

def generate_ai_visual(prompt: str, niche: str) -> str:
    """
    Generates a 9:16 vertical cinematic AI image/clip using Pollinations AI (100% Free, No Quota).
    Returns local path to downloaded AI image.
    """
    output_image = CLIP_POOL_DIR / f"ai_img_{int(time.time())}.jpg"
    encoded_prompt = urllib.parse.quote(f"cinematic vertical 9:16 {niche} gameplay, {prompt}, 4k resolution, photorealistic, trending on artstation")
    url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1080&height=1920&nologo=true&seed={random.randint(1, 999999)}"

    try:
        log_event(None, "INFO", f"Pollinations AI ile görsel üretiliyor: {prompt[:30]}...")
        r = requests.get(url, timeout=25)
        if r.status_code == 200 and len(r.content) > 10000:
            with open(output_image, "wb") as f:
                f.write(r.content)
            log_event(None, "INFO", f"AI Görseli üretildi: {output_image.name}")
            return str(output_image)
    except Exception as e:
        log_event(None, "WARNING", f"AI görsel üretme hatası: {str(e)}")

    return ""

def create_hybrid_ai_video(niche: str, prompt: str, audio_file: str, hook_text: str, output_filename: str) -> str:
    """
    Creates a Hybrid AI Video:
    1. Generates 9:16 Cinematic AI Image via Pollinations AI.
    2. Combines AI Image with slow motion pan/zoom effect + AI Voiceover + Background Gameplay.
    3. Outputs ready-to-publish 9:16 Shorts video.
    """
    output_path = OUTPUT_DIR / output_filename
    clean_hook = hook_text.replace("'", "").replace(":", "-").replace('"', '')

    ai_image_path = generate_ai_visual(prompt, niche)
    
    # Import video fetcher for fallback or background gameplay clip
    from video_fetcher import get_gameplay_clip
    gameplay_clip = get_gameplay_clip(niche)

    import subprocess
    ffmpeg_cmd = ["ffmpeg", "-y"]

    if ai_image_path and os.path.exists(ai_image_path):
        # AI Image + Audio with dynamic zoompan effect
        filter_complex = (
            "[0:v]zoompan=z='min(zoom+0.0015,1.15)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=125:s=1080x1920,"
            f"drawtext=fontfile='C\\:/Windows/Fonts/arial.ttf':text='{clean_hook}':fontcolor=yellow:fontsize=52:x=(w-text_w)/2:y=200:"
            "box=1:boxcolor=black@0.85:boxborderw=25[v]"
        )
        ffmpeg_cmd.extend([
            "-loop", "1", "-i", ai_image_path,
            "-i", audio_file,
            "-filter_complex", filter_complex,
            "-map", "[v]",
            "-map", "1:a",
            "-shortest"
        ])
    elif gameplay_clip and os.path.exists(gameplay_clip):
        # Gameplay video fallback
        filter_complex = (
            "[0:v]scale=1080:1920:force_original_aspect_ratio=increase,"
            "crop=1080:1920,"
            f"drawtext=fontfile='C\\:/Windows/Fonts/arial.ttf':text='{clean_hook}':fontcolor=yellow:fontsize=56:x=(w-text_w)/2:y=180:"
            "box=1:boxcolor=black@0.8:boxborderw=20[v]"
        )
        ffmpeg_cmd.extend([
            "-stream_loop", "-1", "-i", gameplay_clip,
            "-i", audio_file,
            "-filter_complex", filter_complex,
            "-map", "[v]",
            "-map", "1:a",
            "-shortest"
        ])
    else:
        # Simple color canvas
        filter_complex = (
            "[0:v]scale=1080:1920,"
            f"drawtext=fontfile='C\\:/Windows/Fonts/arial.ttf':text='{clean_hook}':fontcolor=yellow:fontsize=52:x=(w-text_w)/2:y=200:"
            "box=1:boxcolor=black@0.85:boxborderw=25[v]"
        )
        ffmpeg_cmd.extend([
            "-f", "lavfi", "-i", "color=c=0x1e1e2e:s=1080x1920:r=24",
            "-i", audio_file,
            "-filter_complex", filter_complex,
            "-map", "[v]",
            "-map", "1:a",
            "-shortest"
        ])

    ffmpeg_cmd.extend([
        "-c:v", "libx264",
        "-preset", "ultrafast",
        "-t", "58",
        str(output_path)
    ])

    try:
        log_event(None, "INFO", f"Hibrit AI Video üretiliyor: {output_filename}")
        subprocess.run(ffmpeg_cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        log_event(None, "INFO", f"Hibrit AI Video üretimi tamamlandı: {output_path}")
        return str(output_path)
    except subprocess.CalledProcessError as e:
        log_event(None, "ERROR", f"FFmpeg Hibrit Video hatası: {e.stderr.decode('utf-8', errors='ignore')}")
        return ""
    except Exception as e:
        log_event(None, "ERROR", f"Hibrit Video genel hata: {str(e)}")
        return ""

if __name__ == "__main__":
    img = generate_ai_visual("4k cinematic Minecraft Steve in dark forest", "minecraft")
    print("Generated AI Visual Path:", img)
