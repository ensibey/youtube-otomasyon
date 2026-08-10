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
    niche: str = "minecraft"
) -> str:
    """
    Transforms video or AI audio into a vibrant 9:16 vertical Shorts video (1080x1920).
    When input is AI voiceover audio, fetches real Minecraft/Roblox gameplay videos automatically!
    """
    output_path = OUTPUT_DIR / output_filename
    clean_hook = hook_text.replace("'", "").replace(":", "-").replace('"', '')

    is_audio_only = input_video_path.endswith(".mp3") or input_video_path.endswith(".wav")

    ffmpeg_cmd = ["ffmpeg", "-y"]

    if is_audio_only:
        audio_file = input_video_path
        # Fetch real Minecraft/Roblox gameplay clip
        from video_fetcher import get_gameplay_clip
        bg_file = get_gameplay_clip(niche)

        if bg_file and os.path.exists(bg_file):
            filter_complex = (
                "[0:v]scale=1080:1920:force_original_aspect_ratio=increase,"
                "crop=1080:1920,"
                f"drawtext=fontfile='C\\:/Windows/Fonts/arial.ttf':text='{clean_hook}':fontcolor=yellow:fontsize=56:x=(w-text_w)/2:y=180:"
                "box=1:boxcolor=black@0.8:boxborderw=20[v]"
            )
            ffmpeg_cmd.extend([
                "-stream_loop", "-1", "-i", bg_file,
                "-i", audio_file,
                "-filter_complex", filter_complex,
                "-map", "[v]",
                "-map", "1:a",
                "-shortest"
            ])
        else:
            # Fallback color canvas if clip fetch fails
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
    else:
        filter_complex = (
            "scale=1080:1920:force_original_aspect_ratio=increase,"
            "crop=1080:1920,"
            f"drawtext=fontfile='C\\:/Windows/Fonts/arial.ttf':text='{clean_hook}':fontcolor=white:fontsize=48:x=(w-text_w)/2:y=120:"
            "box=1:boxcolor=black@0.7:boxborderw=15"
        )
        ffmpeg_cmd.extend([
            "-i", input_video_path,
            "-vf", filter_complex,
            "-c:a", "copy"
        ])

    ffmpeg_cmd.extend([
        "-c:v", "libx264",
        "-preset", "ultrafast",
        "-t", "58",
        str(output_path)
    ])

    try:
        log_event(None, "INFO", f"Video Shorts formatına dönüştürülüyor: {output_filename}")
        subprocess.run(ffmpeg_cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        log_event(None, "INFO", f"Video editleme tamamlandı: {output_path}")
        return str(output_path)
    except subprocess.CalledProcessError as e:
        log_event(None, "ERROR", f"FFmpeg video editleme hatası: {e.stderr.decode('utf-8', errors='ignore')}")
        return ""
    except Exception as e:
        log_event(None, "ERROR", f"Video işleme genel hatası: {str(e)}")
        return ""

if __name__ == "__main__":
    print("Video editor module loaded successfully.")
