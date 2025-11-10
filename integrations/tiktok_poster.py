"""Placeholder para la integración con TikTok"""
import logging
logger = logging.getLogger(__name__)

def post_video(video_path: str, caption: str, api_key: str):
    logger.info(f"[DUMMY] Publicando video en TikTok: video='{video_path}', caption='{caption[:30]}...'")
    # Lógica real de la API de TikTok iría aquí
    return {"status": "success", "video_id": "dummy_tiktok_67890"}
