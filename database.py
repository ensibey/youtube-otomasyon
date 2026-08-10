import sqlite3
from datetime import datetime
from typing import List, Dict, Any, Optional
from config import DB_PATH, DEFAULT_CHANNELS

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_db() as conn:
        cursor = conn.cursor()
        
        # Channels Table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS channels (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            niche TEXT NOT NULL,
            drive_folder_id TEXT DEFAULT '',
            language TEXT DEFAULT 'tr',
            daily_target INTEGER DEFAULT 4,
            voice TEXT DEFAULT 'tr-TR-AhmetNeural',
            made_for_kids INTEGER DEFAULT 0,
            token_path TEXT DEFAULT '',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

        # Videos Table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS videos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            channel_id TEXT NOT NULL,
            filename TEXT NOT NULL,
            source TEXT DEFAULT 'drive', -- 'drive' or 'ai_generated'
            title TEXT,
            description TEXT,
            hashtags TEXT,
            local_path TEXT,
            youtube_video_id TEXT,
            status TEXT DEFAULT 'pending', -- 'pending', 'processed', 'uploaded', 'failed'
            error_message TEXT,
            scheduled_at TIMESTAMP,
            uploaded_at TIMESTAMP,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (channel_id) REFERENCES channels (id)
        )
        """)

        # Logs Table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            channel_id TEXT,
            level TEXT DEFAULT 'INFO',
            message TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

        # Seed default 10 channels if table is empty
        cursor.execute("SELECT COUNT(*) as count FROM channels")
        if cursor.fetchone()["count"] == 0:
            for ch in DEFAULT_CHANNELS:
                cursor.execute("""
                INSERT INTO channels (id, name, niche, drive_folder_id, language, daily_target, voice, made_for_kids, token_path)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (ch.id, ch.name, ch.niche, ch.drive_folder_id, ch.language, ch.daily_target, ch.voice, 1 if ch.made_for_kids else 0, f"tokens/{ch.id}.json"))
        
        conn.commit()

def log_event(channel_id: Optional[str], level: str, message: str):
    try:
        with get_db() as conn:
            conn.cursor().execute(
                "INSERT INTO logs (channel_id, level, message) VALUES (?, ?, ?)",
                (channel_id, level, message)
            )
            conn.commit()
    except sqlite3.OperationalError:
        # Table might not exist yet, initialize and retry
        init_db()
        try:
            with get_db() as conn:
                conn.cursor().execute(
                    "INSERT INTO logs (channel_id, level, message) VALUES (?, ?, ?)",
                    (channel_id, level, message)
                )
                conn.commit()
        except Exception:
            pass

# Auto-initialize DB on import
init_db()

def record_video(channel_id: str, filename: str, source: str = "drive", local_path: str = "") -> int:
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO videos (channel_id, filename, source, local_path, status) VALUES (?, ?, ?, ?, 'pending')",
            (channel_id, filename, source, local_path)
        )
        conn.commit()
        return cursor.lastrowid

def update_video_status(video_id: int, status: str, title: str = "", description: str = "", hashtags: str = "", youtube_id: str = "", error: str = ""):
    with get_db() as conn:
        cursor = conn.cursor()
        now = datetime.now() if status == "uploaded" else None
        cursor.execute("""
        UPDATE videos 
        SET status = ?, title = COALESCE(NULLIF(?, ''), title), description = COALESCE(NULLIF(?, ''), description),
            hashtags = COALESCE(NULLIF(?, ''), hashtags), youtube_video_id = COALESCE(NULLIF(?, ''), youtube_video_id),
            error_message = ?, uploaded_at = COALESCE(?, uploaded_at)
        WHERE id = ?
        """, (status, title, description, hashtags, youtube_id, error, now, video_id))
        conn.commit()

def get_channels() -> List[Dict[str, Any]]:
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM channels")
        return [dict(row) for row in cursor.fetchall()]

def get_channel_by_id(channel_id: str) -> Optional[Dict[str, Any]]:
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM channels WHERE id = ?", (channel_id,))
        row = cursor.fetchone()
        return dict(row) if row else None

if __name__ == "__main__":
    init_db()
    print("Database initialized successfully.")
