"""
YouTube Uploader - Integración Real con la API de YouTube Data v3
Sube videos como Shorts a un canal de YouTube.
"""
import os
import logging
import json
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.http import MediaFileUpload

logger = logging.getLogger(__name__)

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]
API_SERVICE_NAME = "youtube"
API_VERSION = "v3"

# --- Rutas a los archivos de credenciales ---
# Este archivo lo descargas desde Google Cloud Console
CLIENT_SECRETS_FILE = "client_secrets.json" 
# Este archivo se genera automáticamente después de la primera autorización
TOKEN_FILE = "token.json"

def get_authenticated_service():
    """
    Autentica con la API de YouTube y retorna un objeto de servicio.
    Maneja el flujo OAuth2, refrescando el token si es necesario.
    """
    creds = None
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
            except Exception as e:
                logger.error(f"No se pudo refrescar el token de YouTube: {e}. Se requiere re-autenticación manual.")
                # En un servidor, no podemos lanzar el flujo interactivo.
                # Se debería notificar al administrador para que re-autentice.
                return None
        else:
            # Este bloque es para la autenticación inicial y no debería ejecutarse en producción.
            if not os.path.exists(CLIENT_SECRETS_FILE):
                logger.critical(f"CRÍTICO: '{CLIENT_SECRETS_FILE}' no encontrado. Descárgalo desde Google Cloud Console.")
                return None
            
            logger.info("Iniciando flujo de autenticación de YouTube por primera vez...")
            flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
            # run_local_server abrirá un navegador para que el usuario autorice.
            creds = flow.run_local_server(port=0)
        
        # Guardar las credenciales para la próxima ejecución
        with open(TOKEN_FILE, 'w') as token:
            token.write(creds.to_json())
            logger.info(f"Token de YouTube guardado en '{TOKEN_FILE}'.")

    try:
        return googleapiclient.discovery.build(API_SERVICE_NAME, API_VERSION, credentials=creds)
    except Exception as e:
        logger.error(f"No se pudo construir el servicio de YouTube: {e}")
        return None

def upload_short(video_path: str, title: str, description: str):
    """
    Sube un video a YouTube. Para que sea un Short, el título o la descripción
    deben incluir #Shorts, el video debe ser vertical y durar menos de 60s.
    """
    if os.getenv("DUMMY_MODE", "false").lower() == "true":
        logger.info(f"[DUMMY] Subiendo Short a YouTube: video='{video_path}', title='{title[:30]}...'")
        return {"status": "success", "video_id": "dummy_yt_abcde"}

    logger.info(f"🚀 Iniciando subida REAL a YouTube para el video: {video_path}")
    
    youtube_service = get_authenticated_service()
    if not youtube_service:
        error_msg = "No se pudo autenticar con YouTube. Verifica las credenciales y los logs."
        logger.error(error_msg)
        return {"status": "failed", "error": error_msg}

    # Asegurarse de que el video sea tratado como un Short
    if "#shorts" not in title.lower() and "#shorts" not in description.lower():
        title += " #Shorts"

    body = {
        'snippet': {
            'title': title,
            'description': description,
            'tags': ["music", "trap", "newmusic", "shorts"],
            'categoryId': '10'  # 10 es la categoría de "Música"
        },
        'status': {
            'privacyStatus': 'public' # o 'private', 'unlisted'
        }
    }

    try:
        logger.info("Subiendo video a YouTube...")
        media = MediaFileUpload(video_path, chunksize=-1, resumable=True)
        
        request = youtube_service.videos().insert(
            part=",".join(body.keys()),
            body=body,
            media_body=media
        )
        
        response = request.execute()
        video_id = response.get('id')
        logger.info(f"✅ ¡Video subido exitosamente a YouTube! Video ID: {video_id}")
        return {"status": "success", "video_id": video_id, "url": f"https://youtu.be/{video_id}"}

    except googleapiclient.errors.HttpError as e:
        error_content = json.loads(e.content.decode('utf-8'))
        error_message = error_content.get('error', {}).get('message', 'Error desconocido de la API de YouTube')
        logger.error(f"❌ Fallo en la subida a YouTube: {error_message}")
        return {"status": "failed", "error": error_message}
    except Exception as e:
        logger.error(f"❌ Fallo inesperado durante la subida a YouTube: {e}")
        return {"status": "failed", "error": str(e)}

if __name__ == '__main__':
    # Este bloque permite ejecutar el script directamente para realizar la autenticación inicial.
    print("Ejecutando script de autenticación de YouTube...")
    print("Se abrirá una ventana en tu navegador para que autorices la aplicación.")
    get_authenticated_service()
    print("¡Autenticación completada! El archivo 'token.json' ha sido creado/actualizado.")
