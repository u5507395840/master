"""
Meta Poster - Integración Real con la API Graph de Meta
Publica videos como Reels en una cuenta de negocio de Instagram.
"""
import os
import logging
import requests
import time
import json

logger = logging.getLogger(__name__)

API_VERSION = "v19.0"
BASE_URL = f"https://graph.facebook.com/{API_VERSION}"

def _check_publish_status(container_id: str, access_token: str, max_retries: int = 10, delay: int = 10) -> dict:
    """Verifica el estado de publicación del contenedor de forma periódica."""
    for i in range(max_retries):
        try:
            status_url = f"{BASE_URL}/{container_id}"
            params = {'fields': 'status_code', 'access_token': access_token}
            response = requests.get(status_url, params=params)
            response.raise_for_status()
            
            status_data = response.json()
            status_code = status_data.get('status_code')
            logger.info(f"Intento {i+1}/{max_retries}: Estado del contenedor '{container_id}' es '{status_code}'.")

            if status_code == 'FINISHED':
                return {"status": "success", "post_id": container_id}
            if status_code in ['ERROR', 'EXPIRED']:
                logger.error(f"La publicación del contenedor falló con estado: {status_code}")
                return {"status": "failed", "error": f"Container status: {status_code}"}
            
            time.sleep(delay)
        except requests.exceptions.RequestException as e:
            logger.error(f"Error al verificar el estado del contenedor: {e.response.text}")
            time.sleep(delay)
    
    return {"status": "failed", "error": "Timeout: El contenedor no finalizó a tiempo."}


def post_reel(video_path: str, caption: str):
    """
    Publica un video local como un Reel en Instagram.
    Este es un proceso asíncrono de 3 pasos.
    """
    # Obtener credenciales de las variables de entorno
    access_token = os.getenv("META_ACCESS_TOKEN")
    ig_user_id = os.getenv("INSTAGRAM_BUSINESS_ACCOUNT_ID")
    
    if not access_token or not ig_user_id:
        logger.warning("META_ACCESS_TOKEN o INSTAGRAM_BUSINESS_ACCOUNT_ID no están configurados. Usando DUMMY_MODE.")
        os.environ["DUMMY_MODE"] = "true"

    if os.getenv("DUMMY_MODE", "false").lower() == "true":
        logger.info(f"[DUMMY] Publicando Reel en Instagram: video='{video_path}', caption='{caption[:30]}...'")
        return {"status": "success", "post_id": "dummy_meta_12345"}

    logger.info(f"🚀 Iniciando publicación REAL de Reel en Instagram para el video: {video_path}")

    # --- Paso 1: Iniciar el contenedor de subida ---
    try:
        logger.info("Paso 1: Creando contenedor de media...")
        init_url = f"{BASE_URL}/{ig_user_id}/media"
        params = {
            'media_type': 'REELS',
            'video_url': video_path, # La API puede tomar una URL pública
            'caption': caption,
            'access_token': access_token,
        }
        response = requests.post(init_url, params=params)
        response.raise_for_status()
        creation_id = response.json()['id']
        logger.info(f"✅ Contenedor creado con ID: {creation_id}")
    except requests.exceptions.RequestException as e:
        error_text = e.response.text if e.response else str(e)
        logger.error(f"❌ Fallo en el Paso 1 (Crear Contenedor): {error_text}")
        return {"status": "failed", "step": 1, "error": json.loads(error_text)}

    # --- Paso 2: Publicar el contenedor ---
    # La API de Reels con `video_url` es asíncrona. Necesitamos sondear el estado.
    logger.info("Paso 2: Esperando a que el contenedor esté listo para publicar...")
    status_result = _check_publish_status(creation_id, access_token)
    
    if status_result['status'] != 'success':
        return status_result # Retorna el error encontrado durante el sondeo

    # --- Paso 3: Publicar el contenedor de media ---
    try:
        logger.info(f"Paso 3: Publicando el contenedor {creation_id}...")
        publish_url = f"{BASE_URL}/{ig_user_id}/media_publish"
        params = {
            'creation_id': creation_id,
            'access_token': access_token,
        }
        response = requests.post(publish_url, params=params)
        response.raise_for_status()
        final_post = response.json()
        logger.info(f"✅ ¡Reel publicado exitosamente! Post ID: {final_post.get('id')}")
        return {"status": "success", "post_id": final_post.get('id')}
    except requests.exceptions.RequestException as e:
        error_text = e.response.text if e.response else str(e)
        logger.error(f"❌ Fallo en el Paso 3 (Publicar Contenedor): {error_text}")
        return {"status": "failed", "step": 3, "error": json.loads(error_text)}

