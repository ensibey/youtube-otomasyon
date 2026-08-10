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
    Transforms any video or AI audio into a vibrant 9:16 vertical Shorts video (1080x1920).
    Uses background gameplay clips from clip_pool/ or generates dynamic animated color background if input is audio.
    """
    output_path = OUTPUT_DIR / output_filename
    clean_hook = hook_text.replace("'", "").replace(":", "-").replace('"', '')

    # Check if clip_pool directory has background gameplay clips
    clip_pool_dir = Path(__file__).parent / "clip_pool"
    bg_clips = list(clip_pool_dir.glob("*.mp4")) if clip_pool_dir.exists() else []

    is_audio_only = input_video_path.endswith(".mp3") or input_video_path.endswith(".wav")

    ffmpeg_cmd = ["ffmpeg", "-y"]

    if is_audio_only:
        audio_file = input_video_path
        if bg_clips:
            # Use gameplay clip from clip_pool
            bg_file = str(bg_clips[0])
            filter_complex = (
                "[0:v]scale=1080:1920:force_original_aspect_ratio=increase,"
                "crop=1080:1920,"
                f"drawtext=text='{clean_hook}':fontcolor=yellow:fontsize=56:x=(w-text_w)/2:y=180:"
                "box=1:boxcolor=black@0.8:boxborderw=20[v]"
            )
            ffmpeg_cmd.extend([
                "-i", bg_file,
                "-i", audio_file,
                "-filter_complex", filter_complex,
                "-map", "[v]",
                "-map", "1:a",
                "-shortest"
            ])
        else:
            # Generate vibrant animated testsrc2 dynamic color pattern background
            filter_complex = (
                "[0:v]scale=1080:1920,"
                f"drawtext=text='{clean_hook}':fontcolor=yellow:fontsize=52:x=(w-text_w)/2:y=200:"
                "box=1:boxcolor=black@0.85:boxborderw=25[v]"
            )
            ffmpeg_cmd.extend([
                "-f", "lavfi", "-i", "testsrc2=s=1080x1920:r=30",
                "-i", audio_file,
                "-filter_complex", filter_complex,
                "-map", "[v]",
                "-map", "1:a",
                "-shortest"
            ])
    else:
        # Standard video input (from Drive or local pending)
        filter_complex = (
            "scale=1080:1920:force_original_aspect_ratio=increase,"
            "crop=1080:1920,"
            f"drawtext=text='{clean_hook}':fontcolor=white:fontsize=48:x=(w-text_w)/2:y=120:"
            "box=1:boxcolor=black@0.7:boxborderw=15"
        )
        ffmpeg_cmd.extend([
            "-i", input_video_path,
            "-vf", filter_complex,
            "-c:a", "copy"
        ])

    ffmpeg_cmd.extend([
        "-c:v", "libx264",
        "-preset", "fast",
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
