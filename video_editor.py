import os
import subprocess
import random
from pathlib import Path
from typing import Optional
from config import OUTPUT_DIR
from database import log_event

def process_shorts_video(
    input_video_path: str,
    output_filename: str,
    hook_text: str = "WAIT FOR THE END 😱",
    voiceover_path: str = "",
    niche: str = "minecraft"
) -> str:
    """
    Transforms video or AI audio into a vibrant 9:16 vertical Shorts video (1080x1920).
    Merges background gameplay/AI video clip with AI voiceover audio track.
    """
    output_path = OUTPUT_DIR / output_filename
    clean_hook = hook_text.replace("'", "").replace(":", "-").replace('"', '')

    # Ensure background video exists
    if not input_video_path or not os.path.exists(input_video_path) or input_video_path.endswith(".mp3"):
        from video_fetcher import get_gameplay_clip
        bg_video = get_gameplay_clip(niche)
        audio_file = input_video_path if input_video_path.endswith(".mp3") else voiceover_path
    else:
        bg_video = input_video_path
        audio_file = voiceover_path

    ffmpeg_cmd = ["ffmpeg", "-y"]

    filter_complex = (
        "[0:v]scale=1080:1920:force_original_aspect_ratio=increase,"
        "crop=1080:1920,"
        f"drawtext=fontfile='C\\:/Windows/Fonts/arial.ttf':text='{clean_hook}':fontcolor=yellow:fontsize=56:x=(w-text_w)/2:y=180:"
        "box=1:boxcolor=black@0.8:boxborderw=20[v]"
    )

    # Pick random start offset (5s - 90s) so background clip is never identical
    start_sec = random.randint(5, 90)

    if audio_file and os.path.exists(audio_file):
        ffmpeg_cmd.extend([
            "-ss", str(start_sec),
            "-stream_loop", "-1", "-i", bg_video,
            "-i", audio_file,
            "-filter_complex", filter_complex,
            "-map", "[v]",
            "-map", "1:a",
            "-shortest"
        ])
    else:
        ffmpeg_cmd.extend([
            "-i", bg_video,
            "-vf", filter_complex
        ])

    ffmpeg_cmd.extend([
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "26",
        "-maxrate", "4M",
        "-bufsize", "8M",
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
