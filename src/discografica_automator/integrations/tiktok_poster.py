"""Placeholder para la integración con TikTok"""
import logging
logger = logging.getLogger(__name__)

def post_to_tiktok(video_path: str, caption: str):
    """Publica un video en TikTok."""
    logger.info(f"[DUMMY] Publicando video en TikTok: video='{video_path}', caption='{caption[:30]}...'")
    # Lógica real de la API de TikTok iría aquí
    # Por ejemplo, usando una librería como 'tiktok-api'
    # from TikTokApi import TikTokApi
    # api = TikTokApi()
    # api.upload_video(video_path, caption=caption)
    return {"status": "success", "video_id": "dummy_tiktok_67890"}
