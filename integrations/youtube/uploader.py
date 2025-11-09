"""
YouTube Uploader - Subida automática de videos
"""
import os
from typing import Dict

class YouTubeUploader:
    def __init__(self):
        self.client_id = os.getenv("YOUTUBE_CLIENT_ID")
        self.client_secret = os.getenv("YOUTUBE_CLIENT_SECRET")
        self.api_key = os.getenv("YOUTUBE_API_KEY")
        self.dummy_mode = os.getenv("DUMMY_MODE", "true").lower() == "true"
    
    def upload_video(self, video_path: str, title: str, description: str, tags: list) -> Dict:
        """Subir video a YouTube"""
        
        if self.dummy_mode:
            return {
                "id": f"YT_{title.replace(' ', '_')}",
                "title": title,
                "description": description,
                "tags": tags,
                "url": f"https://youtube.com/watch?v={title[:8]}",
                "status": "uploaded",
                "privacy": "public"
            }
        
        # Implementación real con Google API
        return {"dummy_data": True, "message": "Real implementation pending"}
    
    def get_video_analytics(self, video_id: str) -> Dict:
        """Obtener analytics de video"""
        
        if self.dummy_mode:
            return {
                "video_id": video_id,
                "views": 5230,
                "likes": 420,
                "comments": 89,
                "watch_time_minutes": 1245,
                "avg_view_duration": "00:02:15",
                "subscriber_growth": 34
            }
        
        return {"dummy_data": True}

# Instancia global
youtube_uploader = YouTubeUploader()
