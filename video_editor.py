import os
import subprocess
from pathlib import Path
from typing import Optional
from config import OUTPUT_DIR
from database import log_event

def process_shorts_video(
    input_video_path: str,
    output_filename: str,
    hook_text: str = "WAIT FOR THE END 😱",
    audio_path: Optional[str] = None
) -> str:
    """
    Transforms any video into a 9:16 vertical YouTube Shorts format (1080x1920).
    Adds top hook banner text overlay and optional AI audio track using FFmpeg.
    """
    output_path = OUTPUT_DIR / output_filename
    
    if not os.path.exists(input_video_path):
        log_event(None, "ERROR", f"Girdi videosu bulunamadı: {input_video_path}")
        return ""

    # Safe text formatting for FFmpeg drawtext
    clean_hook = hook_text.replace("'", "").replace(":", "-").replace('"', '')

    # Construct FFmpeg command
    # 1. Scale and crop to 1080x1920 (9:16)
    # 2. Add Top Hook banner
    ffmpeg_cmd = [
        "ffmpeg", "-y",
        "-i", input_video_path,
    ]

    if audio_path and os.path.exists(audio_path):
        ffmpeg_cmd.extend(["-i", audio_path])
        # Mix original audio with voiceover or replace
        filter_complex = (
            "[0:v]scale=1080:1920:force_original_aspect_ratio=increase,"
            "crop=1080:1920,"
            f"drawtext=text='{clean_hook}':fontcolor=white:fontsize=48:x=(w-text_w)/2:y=120:"
            "box=1:boxcolor=black@0.7:boxborderw=15[v]"
        )
        ffmpeg_cmd.extend([
            "-filter_complex", filter_complex,
            "-map", "[v]",
            "-map", "1:a",
            "-shortest"
        ])
    else:
        filter_complex = (
            "scale=1080:1920:force_original_aspect_ratio=increase,"
            "crop=1080:1920,"
            f"drawtext=text='{clean_hook}':fontcolor=white:fontsize=48:x=(w-text_w)/2:y=120:"
            "box=1:boxcolor=black@0.7:boxborderw=15"
        )
        ffmpeg_cmd.extend([
            "-vf", filter_complex,
            "-c:a", "copy"
        ])

    ffmpeg_cmd.extend([
        "-c:v", "libx264",
        "-preset", "fast",
        "-t", "58",  # Guarantee < 59s for YouTube Shorts
        str(output_path)
    ])

    try:
        log_event(None, "INFO", f"Video Shorts formatına dönüştürülüyor: {output_filename}")
        subprocess.run(ffmpeg_cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        log_event(None, "INFO", f"Video editleme tamamlandı: {output_path}")
        return str(output_path)
    except subprocess.CalledProcessError as e:
        log_event(None, "ERROR", f"FFmpeg video editleme hatası: {e.stderr.decode('utf-8', errors='ignore')}")
        # Fallback: Copy file directly if FFmpeg filter fails
        try:
            import shutil
            shutil.copy(input_video_path, str(output_path))
            return str(output_path)
        except Exception:
            return ""
    except FileNotFoundError:
        log_event(None, "WARNING", "FFmpeg sistemde bulunamadı. Girdi videosu doğrudan kopyalanıyor.")
        import shutil
        shutil.copy(input_video_path, str(output_path))
        return str(output_path)

if __name__ == "__main__":
    print("Video editor module loaded successfully.")
