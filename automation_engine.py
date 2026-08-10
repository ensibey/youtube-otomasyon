import os
import time
from typing import Dict, Any
from database import get_channel_by_id, record_video, update_video_status, log_event
from drive_service import DriveService
from ai_generator import generate_metadata, generate_script
from tts_service import generate_voiceover
from video_editor import process_shorts_video
from youtube_uploader import YouTubeUploader
from telegram_bot import send_telegram_notification

def run_channel_pipeline(channel_id: str) -> Dict[str, Any]:
    """
    Runs full automation pipeline for a single YouTube channel:
    1. Fetch video from Drive / Local folder
    2. Generate AI Metadata & Voiceover if needed
    3. Edit to 9:16 Shorts format with Hook overlay
    4. Upload to YouTube Shorts
    5. Send Telegram notification with video URL
    """
    drive_service = DriveService()
    channel = get_channel_by_id(channel_id)
    if not channel:
        log_event(channel_id, "ERROR", f"Kanal ID bulunamadı: {channel_id}")
        return {"success": False, "error": "Channel not found"}

    channel_name = channel["name"]
    niche = channel["niche"]
    lang = channel["language"]
    drive_folder = channel.get("drive_folder_id", "")
    voice = channel.get("voice", "tr-TR-AhmetNeural")

    log_event(channel_id, "INFO", f"=== {channel_name} Otomasyonu Başlatıldı ===")

    # 1. Check for Pending Videos in Google Drive or Local folder
    pending_videos = drive_service.fetch_pending_videos(channel_id, drive_folder)
    
    input_video_path = ""
    filename = ""
    source = "drive"
    drive_file_id = ""

    if pending_videos:
        video_info = pending_videos[0]
        input_video_path = video_info["local_path"]
        filename = video_info["filename"]
        drive_file_id = video_info.get("drive_file_id", "")
        log_event(channel_id, "INFO", f"Drive'dan video bulundu: {filename}")
    else:
        # 2. AI AUTO-GENERATION FALLBACK MODE (If no video in Drive!)
        log_event(channel_id, "INFO", "Drive'da video bulunamadı. AI Tam Otomatik Modu başlatılıyor...")
        source = "ai_generated"
        filename = f"ai_gen_{int(time.time())}.mp4"
        
        # Generate AI Script & Voiceover
        script = generate_script(niche, lang)
        voiceover_file = generate_voiceover(script, voice, f"voice_{channel_id}.mp3")
        
        # Create temporary background video path (fallback generator)
        input_video_path = voiceover_file  # Video editor handles audio input

    # 3. Record video entry in Database
    db_video_id = record_video(channel_id, filename, source, input_video_path)

    # 4. Generate AI Title, Description, Hashtags & Hook Text
    metadata = generate_metadata(niche, lang, filename)
    title = metadata.get("title", "AWESOME GAMING MOMENT 😱 #shorts")
    description = metadata.get("description", "Watch until the end! Subscribe for daily gaming shorts.")
    hashtags = metadata.get("hashtags", "#shorts #gaming #viral")
    hook = metadata.get("hook", "BEKLE VE GÖR! 😱")

    # 5. Process & Edit 9:16 Shorts Video using Real 60FPS Gameplay Parkour Clips
    output_filename = f"shorts_{channel_id}_{int(time.time())}.mp4"
    final_shorts_path = process_shorts_video(input_video_path, output_filename, hook, niche=niche)

    if not final_shorts_path or not os.path.exists(final_shorts_path):
        error_msg = "Video editleme/dönüştürme başarısız oldu."
        update_video_status(db_video_id, "failed", error=error_msg)
        return {"success": False, "error": error_msg}

    # 6. Upload to YouTube Shorts
    uploader = YouTubeUploader(channel_id)
    upload_result = uploader.upload_shorts(
        video_file_path=final_shorts_path,
        title=title,
        description=description,
        hashtags=hashtags,
        made_for_kids=bool(channel.get("made_for_kids", 0))
    )

    if upload_result.get("success"):
        yt_url = upload_result.get("url", "")
        yt_id = upload_result.get("video_id", "")
        
        update_video_status(db_video_id, "uploaded", title, description, hashtags, yt_id)
        
        # Mark as uploaded in Drive & Local
        if source == "drive":
            drive_service.mark_as_uploaded(channel_id, filename, drive_file_id)

        # 7. Send Telegram Notification to phone with actual MP4 video file!
        send_telegram_notification(
            channel_name=channel_name,
            title=title,
            video_url=yt_url,
            filename=filename,
            status="Success",
            video_file_path=final_shorts_path
        )
        return {"success": True, "channel": channel_name, "url": yt_url}
    else:
        err = upload_result.get("error", "Unknown upload failure")
        update_video_status(db_video_id, "failed", error=err)
        send_telegram_notification(
            channel_name=channel_name,
            title=title,
            video_url="",
            filename=filename,
            status="Failed",
            error_msg=err
        )
        return {"success": False, "error": err}

def run_all_channels_pipeline():
    """Runs pipeline across all 10 configured YouTube channels."""
    from database import get_channels
    channels = get_channels()
    results = []
    print(f"Starting automation run for {len(channels)} channels...")
    for ch in channels:
        res = run_channel_pipeline(ch["id"])
        results.append(res)
    return results

if __name__ == "__main__":
    from database import init_db
    init_db()
    res = run_channel_pipeline("ch_01")
    print("Pipeline Result:", res)
