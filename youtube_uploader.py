import os
import json
import time
from pathlib import Path
from typing import Dict, Any, Optional
from config import TOKENS_DIR, CREDENTIALS_DIR
from database import log_event

class YouTubeUploader:
    def __init__(self, channel_id: str):
        self.channel_id = channel_id
        self.token_file = TOKENS_DIR / f"{channel_id}.json"
        self.client_secrets = CREDENTIALS_DIR / "client_secret.json"
        self.youtube_service = None
        self._authenticate()

    def _authenticate(self):
        """Authenticates YouTube Data API v3 using stored token or OAuth flow."""
        if not self.client_secrets.exists():
            log_event(self.channel_id, "WARNING", f"client_secret.json bulunamadı ({self.client_secrets}). YouTube API yüklemeleri Test Modunda çalışacak.")
            return

        try:
            from google.oauth2.credentials import Credentials
            from google_auth_oauthlib.flow import InstalledAppFlow
            from googleapiclient.discovery import build

            SCOPES = ['https://www.googleapis.com/auth/youtube.upload']

            creds = None
            if self.token_file.exists():
                creds = Credentials.from_authorized_user_file(str(self.token_file), SCOPES)

            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    from google.auth.transport.requests import Request
                    creds.refresh(Request())
                else:
                    log_event(self.channel_id, "INFO", f"Kanal {self.channel_id} için OAuth doğrulaması başlatılıyor...")
                    flow = InstalledAppFlow.from_client_secrets_file(str(self.client_secrets), SCOPES)
                    creds = flow.run_local_server(port=0)

                with open(self.token_file, 'w') as token_out:
                    token_out.write(creds.to_json())

            self.youtube_service = build('youtube', 'v3', credentials=creds)
            log_event(self.channel_id, "INFO", f"YouTube API servisi başarıyla yetkilendirildi: {self.channel_id}")
        except Exception as e:
            log_event(self.channel_id, "ERROR", f"YouTube API Yetkilendirme hatası: {str(e)}")

    def upload_shorts(
        self,
        video_file_path: str,
        title: str,
        description: str,
        hashtags: str,
        category_id: str = "20",  # 20 = Gaming
        made_for_kids: bool = False
    ) -> Dict[str, Any]:
        """
        Uploads video to YouTube Shorts using Resumable MediaUpload.
        Returns dictionary with success status, video_id, and youtube_url.
        """
        if not os.path.exists(video_file_path):
            log_event(self.channel_id, "ERROR", f"Yüklenecek video dosyası yok: {video_file_path}")
            return {"success": False, "error": "File not found"}

        # Combine title and hashtags for Shorts ranking
        full_title = f"{title} {hashtags}".strip()
        if len(full_title) > 100:
            full_title = full_title[:97] + "..."

        full_description = f"{description}\n\n{hashtags}\n\n#shorts #gaming #youtube"

        # Mock Mode if API service is not authenticated
        if not self.youtube_service:
            mock_video_id = f"MOCK_YT_{int(time.time())}"
            log_event(self.channel_id, "INFO", f"[MOCK MODE] Video simüle edilerek yüklendi: {full_title}")
            return {
                "success": True,
                "video_id": mock_video_id,
                "url": f"https://youtube.com/shorts/{mock_video_id}",
                "mock": True
            }

        try:
            from googleapiclient.http import MediaFileUpload

            body = {
                'snippet': {
                    'title': full_title,
                    'description': full_description,
                    'tags': [t.strip('#') for t in hashtags.split()],
                    'categoryId': category_id
                },
                'status': {
                    'privacyStatus': 'public',
                    'selfDeclaredMadeForKids': made_for_kids
                }
            }

            media = MediaFileUpload(video_file_path, chunksize=-1, resumable=True, mimetype='video/mp4')
            request = self.youtube_service.videos().insert(
                part=','.join(body.keys()),
                body=body,
                media_body=media
            )

            response = None
            log_event(self.channel_id, "INFO", f"YouTube'a video yükleniyor: {full_title}")
            while response is None:
                status, response = request.next_chunk()
                if status:
                    progress = int(status.progress() * 100)
                    log_event(self.channel_id, "INFO", f"Yükleme İlerlemesi: %{progress}")

            video_id = response.get('id', '')
            shorts_url = f"https://youtube.com/shorts/{video_id}"
            log_event(self.channel_id, "INFO", f"Video başarıyla YouTube'a yüklendi! Link: {shorts_url}")

            return {
                "success": True,
                "video_id": video_id,
                "url": shorts_url,
                "mock": False
            }
        except Exception as e:
            error_msg = f"YouTube Yükleme Hatası: {str(e)}"
            log_event(self.channel_id, "ERROR", error_msg)
            return {"success": False, "error": error_msg}

if __name__ == "__main__":
    uploader = YouTubeUploader("ch_01")
    print("YouTube Uploader Initialized.")
