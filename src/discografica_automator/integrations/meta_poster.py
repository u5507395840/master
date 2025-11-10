import os
import logging

# Configuración del logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

DUMMY_MODE = os.getenv('DUMMY_MODE', 'false').lower() in ('true', '1', 't')

def post_to_meta(platform: str, video_path: str, caption: str):
    """
    Publica un video en Instagram o Facebook.
    TODO: Implementar la lógica de subida real.
    """
    meta_access_token = os.getenv("META_ACCESS_TOKEN")
    meta_page_id = os.getenv("META_PAGE_ID") # Para Facebook
    meta_ig_user_id = os.getenv("META_IG_USER_ID") # Para Instagram

    if DUMMY_MODE:
        logging.info(f"[DUMMY] Publicando en {platform}: '{caption[:50]}...'")
        if not meta_access_token:
            logging.warning("[DUMMY] Advertencia: La variable META_ACCESS_TOKEN no está configurada.")
        return f"https://dummy.{platform}.com/post/12345"

    if not meta_access_token:
        logging.error("Error: Falta el token de acceso de Meta (META_ACCESS_TOKEN).")
        raise ValueError("Token de acceso de Meta no configurado en el entorno.")

    # Aquí iría la lógica real de publicación
    logging.info(f"Publicando en {platform}...")
    # from facebook_business.api import FacebookAdsApi
    # ... (lógica de autenticación y publicación)

    logging.warning(f"La lógica de publicación real en {platform} aún no está implementada.")
    return f"URL_DEL_POST_EN_{platform.upper()}"
