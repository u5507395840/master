import os
import logging

# Configuración del logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

DUMMY_MODE = os.getenv('DUMMY_MODE', 'false').lower() in ('true', '1', 't')

def upload_video(video_path: str, title: str, description: str):
    """
    Sube un video a YouTube.
    TODO: Implementar la lógica de autenticación con OAuth2 usando las credenciales de entorno.
    """
    youtube_api_key = os.getenv("YOUTUBE_API_KEY")
    youtube_client_secret_json = os.getenv("YOUTUBE_CLIENT_SECRET_JSON")

    if DUMMY_MODE:
        logging.info(f"[DUMMY] Subiendo video a YouTube: '{title}' desde '{video_path}'")
        logging.info(f"[DUMMY] Descripción: {description[:50]}...")
        if not youtube_api_key:
            logging.warning("[DUMMY] Advertencia: La variable YOUTUBE_API_KEY no está configurada.")
        return f"https://dummy.youtube.com/watch?v={os.path.basename(video_path)}"
    
    if not youtube_api_key or not youtube_client_secret_json:
        logging.error("Error: Faltan las credenciales de YouTube (YOUTUBE_API_KEY, YOUTUBE_CLIENT_SECRET_JSON).")
        raise ValueError("Credenciales de YouTube no configuradas en el entorno.")

    # Aquí iría la lógica real de subida con la librería de Google
    logging.info(f"Subiendo video a YouTube: {title}")
    # from googleapiclient.discovery import build
    # ... (lógica de autenticación y subida)
    
    logging.warning("La lógica de subida real a YouTube aún no está implementada.")
    return "URL_DEL_VIDEO_EN_YOUTUBE"
