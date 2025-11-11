"""
YouTube Satellite Manager - Automatización de publicación y métricas en cuentas satélite
"""
import os
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from typing import List, Dict

class YouTubeSatelliteManager:
    def __init__(self, api_keys: List[str], main_channel_id: str):
        """
        api_keys: lista de API Keys de cuentas satélite
        main_channel_id: ID del canal principal
        """
        self.api_keys = api_keys
        self.main_channel_id = main_channel_id
        self.clients = [build('youtube', 'v3', developerKey=key) for key in api_keys]

    def publish_video(self, video_metadata: Dict, video_file_path: str) -> List[Dict]:
        """
        Publica el video en todas las cuentas satélite.
        video_metadata: dict con 'title', 'description', 'tags', etc.
        video_file_path: ruta al archivo de video
        Devuelve lista de resultados por cuenta
        """
        results = []
        for client in self.clients:
            try:
                request = client.videos().insert(
                    part="snippet,status",
                    body={
                        "snippet": video_metadata,
                        "status": {"privacyStatus": "public"}
                    },
                    media_body=video_file_path
                )
                response = request.execute()
                results.append({"status": "ok", "videoId": response["id"]})
            except HttpError as e:
                results.append({"status": "error", "error": str(e)})
        return results

    def get_metrics(self) -> List[Dict]:
        """
        Recoge métricas de los últimos videos publicados en cada cuenta satélite.
        Devuelve lista de dicts con views, likes, comments, etc.
        """
        metrics = []
        for client in self.clients:
            try:
                # Obtiene los últimos videos del canal
                channel_id = self.main_channel_id  # O el ID satélite si se gestiona por separado
                search_response = client.search().list(
                    channelId=channel_id,
                    part="id",
                    order="date",
                    maxResults=5
                ).execute()
                video_ids = [item["id"]["videoId"] for item in search_response["items"] if item["id"].get("videoId")]
                for vid in video_ids:
                    stats = client.videos().list(
                        part="statistics",
                        id=vid
                    ).execute()
                    metrics.append({"videoId": vid, "statistics": stats["items"][0]["statistics"]})
            except HttpError as e:
                metrics.append({"status": "error", "error": str(e)})
        return metrics

# Ejemplo de uso:
# manager = YouTubeSatelliteManager(["API_KEY_1", "API_KEY_2"], "MAIN_CHANNEL_ID")
# manager.publish_video({"title": "Longcat Viral", "description": "Video experimental", "tags": ["longcat", "viral"]}, "/path/video.mp4")
# print(manager.get_metrics())
