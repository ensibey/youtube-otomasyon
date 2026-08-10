import os
import shutil
from pathlib import Path
from typing import List, Dict, Any, Optional
from config import DOWNLOADS_DIR, CREDENTIALS_DIR
from database import log_event

class DriveService:
    def __init__(self):
        self.gauth = None
        self.drive = None
        self._init_drive()

    def _init_drive(self):
        """Initializes PyDrive2 if client_secrets.json exists."""
        secrets_file = CREDENTIALS_DIR / "client_secrets.json"
        if not secrets_file.exists():
            log_event(None, "WARNING", f"Google Drive client_secrets.json bulunamadı. Yerel klasör modu kullanılacak ({CREDENTIALS_DIR}).")
            return

        try:
            from pydrive2.auth import GoogleAuth
            from pydrive2.drive import GoogleDrive
            
            GoogleAuth.DEFAULT_SETTINGS['client_config_file'] = str(secrets_file)
            self.gauth = GoogleAuth()
            # Try loading saved credentials
            cred_file = CREDENTIALS_DIR / "drive_credentials.json"
            if cred_file.exists():
                self.gauth.LoadCredentialsFile(str(cred_file))
            
            if self.gauth.credentials is None:
                log_event(None, "INFO", "Google Drive kimlik doğrulaması gerekiyor.")
            elif self.gauth.access_token_expired:
                self.gauth.Refresh()
            else:
                self.gauth.Authorize()
                
            self.gauth.SaveCredentialsFile(str(cred_file))
            self.drive = GoogleDrive(self.gauth)
            log_event(None, "INFO", "Google Drive servisi başarıyla bağlandı.")
        except Exception as e:
            log_event(None, "ERROR", f"Google Drive bağlantı hatası: {str(e)}")

    def fetch_pending_videos(self, channel_id: str, drive_folder_id: Optional[str] = None) -> List[Dict[str, str]]:
        """
        Fetches pending video files for a specific channel.
        If Google Drive is enabled and folder ID is provided, checks Drive.
        Otherwise falls back to local `downloads/<channel_id>/pending/` directory.
        """
        downloaded_files = []
        
        # 1. Local Fallback Directory Check
        channel_pending_dir = DOWNLOADS_DIR / channel_id / "pending"
        channel_uploaded_dir = DOWNLOADS_DIR / channel_id / "uploaded"
        channel_pending_dir.mkdir(parents=True, exist_ok=True)
        channel_uploaded_dir.mkdir(parents=True, exist_ok=True)

        # Check local files first
        video_extensions = ('.mp4', '.mov', '.mkv', '.avi')
        local_files = [f for f in channel_pending_dir.iterdir() if f.suffix.lower() in video_extensions]
        
        for file_path in local_files:
            downloaded_files.append({
                "filename": file_path.name,
                "local_path": str(file_path),
                "source": "local_pending",
                "drive_file_id": ""
            })

        # 2. Google Drive API Check (if configured and active)
        if self.drive and drive_folder_id:
            try:
                query = f"'{drive_folder_id}' in parents and trashed=false and title contains '.mp4'"
                file_list = self.drive.ListFile({'q': query}).GetList()
                
                for f in file_list:
                    dest_path = channel_pending_dir / f['title']
                    if not dest_path.exists():
                        log_event(channel_id, "INFO", f"Drive'dan video indiriliyor: {f['title']}")
                        f.GetContentFile(str(dest_path))
                    
                    downloaded_files.append({
                        "filename": f['title'],
                        "local_path": str(dest_path),
                        "source": "google_drive",
                        "drive_file_id": f['id']
                    })
            except Exception as e:
                log_event(channel_id, "ERROR", f"Drive klasörü taranırken hata: {str(e)}")

        return downloaded_files

    def mark_as_uploaded(self, channel_id: str, filename: str, drive_file_id: str = ""):
        """Moves processed video from pending/ to uploaded/ locally and in Drive."""
        pending_path = DOWNLOADS_DIR / channel_id / "pending" / filename
        uploaded_path = DOWNLOADS_DIR / channel_id / "uploaded" / filename
        
        if pending_path.exists():
            shutil.move(str(pending_path), str(uploaded_path))
            log_event(channel_id, "INFO", f"Video yerel arşiv klasörüne taşındı: {filename}")

        if self.drive and drive_file_id:
            try:
                drive_file = self.drive.CreateFile({'id': drive_file_id})
                drive_file['title'] = f"[UPLOADED]_{filename}"
                drive_file.Upload()
                log_event(channel_id, "INFO", f"Drive dosya adı güncellendi: [UPLOADED]_{filename}")
            except Exception as e:
                log_event(channel_id, "ERROR", f"Drive dosya adı değiştirilemedi: {str(e)}")

if __name__ == "__main__":
    ds = DriveService()
    files = ds.fetch_pending_videos("ch_01")
    print(f"Ch 01 Pending Files: {len(files)}")
