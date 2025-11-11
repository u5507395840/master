

from fastapi import FastAPI, File, UploadFile, Body
from pydantic import BaseModel

# --- Definición de FastAPI al inicio ---
app = FastAPI()

# --- ENDPOINT: Healthcheck para Railway ---
@app.get("/health")
def health():
    return {"status": "ok", "message": "API is healthy"}

# --- Definición de FastAPI al inicio ---
app = FastAPI()



# --- ENDPOINT: Subida de creativos y metadatos ---
class CreativeUploadRequest(BaseModel):
    artist: str
    genre: str
    subgenres: list = []
    collaborators: list = []
    language: str = "es"
    notes: str = ""

@app.post("/upload_creative")
async def upload_creative(artist: str, genre: str, subgenres: str = "", collaborators: str = "", language: str = "es", notes: str = "", file: UploadFile = File(...)):
    # Dummy response
    return {"status": "ok", "metadata": {
        "artist": artist,
        "genre": genre,
        "subgenres": subgenres.split(",") if subgenres else [],
        "collaborators": collaborators.split(",") if collaborators else [],
        "language": language,
        "notes": notes,
        "file": f"dummy_path/{artist}_{genre}_file"
    }}
# --- Definición de FastAPI al inicio ---
app = FastAPI()
# --- ENDPOINT: Generación de estrategia y prompts creativos por IA ---
class IAPromptStrategyRequest(BaseModel):
    performance_data: dict
    total_budget: float
    youtube_channel_url: str
    creativity_level: str = "alto"
    model: str = "gpt-5"

    # ...existing code...
@app.post("/ia_generate_strategy")
def ia_generate_strategy(req: IAPromptStrategyRequest):
    # Dummy response
    return {"strategy": {
        "actions": ["Mejorar thumbnails", "Publicar en horario óptimo", "Colaborar con artistas emergentes"],
        "prompts": ["Crea un video viral sobre el proceso creativo", "Haz un reto musical colaborativo", "Cuenta la historia detrás del track"],
        "budget_distribution": {"YouTube": 40, "Meta Ads": 30, "TikTok": 30},
        "recommendations": ["Publicar martes y jueves", "Usar hashtags virales"],
        "creativity_level": req.creativity_level,
        "model": req.model
    }}
# --- ENDPOINT: Campaña 1 a 1 directa en cuentas satélite ---
class DirectSatelliteCampaignRequest(BaseModel):
    api_keys: list
    channel_id: str
    video_metadata: dict
    video_file_path: str

    # ...existing code...
@app.post("/direct_satellite_campaign")
def direct_satellite_campaign(req: DirectSatelliteCampaignRequest):
    # Dummy response
    results = []
    for idx, api_key in enumerate(req.api_keys):
        results.append({
            "status": "ok",
            "videoId": f"video_{idx+1}_dummy",
            "account": api_key,
            "analysis": "dummy_analysis",
            "analytics": "dummy_analytics",
            "metadatos": {},
            "prompt": "dummy_prompt"
        })
    return {"result": results}
# --- ENDPOINT: Automatización completa bajo trigger Meta Ads ---
class MetaTriggerSatelliteRequest(BaseModel):
    channel_id: str
    api_keys: list
    total_budget: float
    youtube_channel_url: str
    days: int = 30

    # ...existing code...
@app.post("/meta_trigger_youtube_satellite")
def meta_trigger_youtube_satellite(payload: dict):
    # Dummy response
    return {
        "status": "ok",
        "msg": f"Trigger recibido para campaña {payload.get('campaign_id', 'dummy')} con acción {payload.get('action', 'dummy')}"
    }



# --- ENDPOINT: Crear perfil GoLogin ---
class GoLoginProfileRequest(BaseModel):
    api_token: str
    name: str
    os_type: str = "android"

    # ...existing code...
@app.post("/gologin_create_profile")
def gologin_create_profile(req: GoLoginProfileRequest):
    # Dummy response
    return {"result": {"profile_id": "dummy_profile_id", "status": "created"}}

# --- ENDPOINT: Lanzar perfil GoLogin ---
class GoLoginStartProfileRequest(BaseModel):
    api_token: str
    profile_id: str

    # ...existing code...
@app.post("/gologin_start_profile")
def gologin_start_profile(req: GoLoginStartProfileRequest):
    # Dummy response
    return {"result": {"profile_id": req.profile_id, "status": "started"}}

# --- ENDPOINT: Parar perfil GoLogin ---
class GoLoginStopProfileRequest(BaseModel):
    api_token: str
    profile_id: str

    # ...existing code...
@app.post("/gologin_stop_profile")
def gologin_stop_profile(req: GoLoginStopProfileRequest):
    # Dummy response
    return {"result": {"profile_id": req.profile_id, "status": "stopped"}}

# --- ENDPOINT: Automatización Android (Appium/ADB) ---
class AndroidEmulatorRequest(BaseModel):
    avd_name: str

    # ...existing code...
@app.post("/android_start_emulator")
def android_start_emulator(req: AndroidEmulatorRequest):
    # Dummy response
    return {"status": "ok", "msg": f"Emulador {req.avd_name} lanzado (dummy)."}

class AndroidInstallApkRequest(BaseModel):
    apk_path: str
    device_id: str = "emulator-5554"

    # ...existing code...
@app.post("/android_install_apk")
def android_install_apk(req: AndroidInstallApkRequest):
    # Dummy response
    return {"status": "ok", "msg": f"APK {req.apk_path} instalado en {req.device_id} (dummy)."}

class AndroidAppiumRequest(BaseModel):
    device_id: str = "emulator-5554"
    port: int = 4723

    # ...existing code...
@app.post("/android_run_appium")
def android_run_appium(req: AndroidAppiumRequest):
    # Dummy response
    return {"status": "ok", "msg": f"Appium lanzado en {req.device_id}:{req.port} (dummy)."}

class AndroidAdbCommandRequest(BaseModel):
    command: list
    device_id: str = "emulator-5554"

    # ...existing code...
@app.post("/android_execute_adb")
def android_execute_adb(req: AndroidAdbCommandRequest):
    # Dummy response
    return {"output": f"Comando {req.command} ejecutado en {req.device_id} (dummy)."}

# --- ENDPOINT: Trigger Meta Ads para n8n ---
    # ...existing code...
@app.post("/metaads_trigger_n8n")
def metaads_trigger_n8n(payload: dict = Body(...)):
    # Dummy response
    return {"status": "ok", "msg": "Trigger recibido y procesado para automatización de campañas en redes sociales (dummy).", "payload": payload}

"""
API Backend Ejecutivo para gobierno total del sistema musical ML
"""
from fastapi import FastAPI, Body
from pydantic import BaseModel
from typing import Optional, Dict, Any, List

import logging
import sys
import os
# Comprobación e importación robusta de requirements
try:
    import requests
    import fastapi
    import pydantic
except ImportError as e:
    import subprocess
    print(f"Instalando dependencias faltantes: {e.name}")
    subprocess.run([sys.executable, "-m", "pip", "install", e.name])
    # Reintenta importación
    globals()[e.name] = __import__(e.name)
# Añadir el directorio 'src' al PYTHONPATH para encontrar los módulos
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

## Dummy mode: no external imports

app = FastAPI(title="Discográfica ML Executive API", description="Gobierna campañas, IA, Meta Ads, usuarios y más.")

import socket
# --- ENDPOINT: Input de información del canal principal ---
class MainChannelInputRequest(BaseModel):
    channel_id: str
    info: dict

main_channel_info = {}

# --- ENDPOINT: Información de red y puertos ---
@app.get("/network_info")
def network_info():
    """
    Devuelve información de red útil para despliegue y acceso externo.
    Incluye IPs locales, interfaces (simplificado), y puertos recomendados.
    """
    info = {}
    info["hostname"] = socket.gethostname()
    # Obtener IP local principal
    try:
        info["local_ip"] = socket.gethostbyname(socket.gethostname())
    except Exception:
        info["local_ip"] = "No disponible"
    info["recommended_ports"] = [80, 443, 8080, 8501]
    return info

@app.post("/main_channel_input")
def main_channel_input(req: MainChannelInputRequest):
    global main_channel_info
    main_channel_info[req.channel_id] = req.info
    return {"status": "ok", "msg": f"Información del canal {req.channel_id} registrada.", "data": req.info}

class SatelliteVideoRequest(BaseModel):
    api_keys: list
    main_channel_id: str
    video_metadata: dict
    video_file_path: str

class SatelliteMetricsRequest(BaseModel):
    api_keys: list
    main_channel_id: str

# --- ENDPOINT: Publicar video en cuentas satélite ---
    # ...existing code...
@app.post("/satellite_publish_video")
def satellite_publish_video(req: SatelliteVideoRequest):
    # Dummy response
    return {"result": [{"status": "ok", "videoId": "dummy_satellite_video"}]}

# --- ENDPOINT: Consultar métricas de cuentas satélite ---
    # ...existing code...
@app.post("/satellite_get_metrics")
def satellite_get_metrics(req: SatelliteMetricsRequest):
    # Dummy response
    return {"metrics": [{"account": "dummy_account", "views": 1000, "likes": 100, "comments": 10}]}

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CampaignLaunchRequest(BaseModel):
    track_name: str
    artist: str
    video_prompt: str
    platforms: List[str]
    budget_eur: float
    audience: Optional[str] = None
    hashtags: Optional[List[str]] = None

class ROIRequest(BaseModel):
    spend_eur: float
    revenue_eur: float
    clicks: int
    conversions: int
    impressions: int

class OpenAIChatRequest(BaseModel):
    prompt: str
    history: Optional[List[Dict[str, str]]] = None
    system_prompt: Optional[str] = "Eres el asistente ejecutivo de la discográfica. Responde como experto en IA, marketing musical, automatización y gestión empresarial."
    action: Optional[str] = None  # Para comandos especiales: lanzar campaña, consultar ROI, etc.
    params: Optional[Dict[str, Any]] = None
    openai_api_key: Optional[str] = None
    model: Optional[str] = None

@app.get("/status")
def status():
    """Estado básico del sistema."""
    return {"status": "ok", "orchestrator": True}

@app.post("/launch_campaign")
def launch_campaign(req: CampaignLaunchRequest):
    # Dummy response
    return {"result": "ok", "msg": f"Campaña lanzada en {', '.join(req.platforms)} (dummy)"}

@app.post("/calculate_roi")
def calculate_roi(req: ROIRequest):
    # Dummy response
    return {"roi": 1.5, "metrics": {"spend_eur": req.spend_eur, "revenue_eur": req.revenue_eur, "clicks": req.clicks, "conversions": req.conversions, "impressions": req.impressions}}

@app.get("/meta_ads_status")
def meta_ads_status():
    # Dummy response
    return {"status": "ok", "msg": "Meta Ads integración dummy"}

@app.get("/performance_report")
def performance_report(days: int = 30):
    # Dummy response
    return {"days": days, "performance": "dummy_report"}

@app.post("/set_openai_key")
def set_openai_key(api_key: str = Body(...)): 
    # Dummy response
    return {"valid": True, "status": "dummy"}

@app.get("/get_openai_key_status")
def get_openai_key_status():
    # Dummy response
    return {"status": "dummy"}

@app.post("/openai_chat")
def openai_chat(req: OpenAIChatRequest):
    # Dummy response
    return {"response": "Respuesta dummy IA", "action_result": None}

def launch_campaign_api(params: dict):
    # Dummy response
    return {"result": "ok", "msg": f"Campaña lanzada: {params.get('track_name', 'N/A')} (dummy)"}

# --- ENDPOINT: Recibir vídeos largos (Longcat) ---
class LongcatUploadRequest(BaseModel):
    video_file_path: str
    channel_id: str
    metadata: dict = {}

@app.post("/longcat_upload")
def longcat_upload(req: LongcatUploadRequest):
    """
    Recibe un vídeo largo (longcat), lo analiza con Ultralytics y deja preparado el punto para integración con Runway.
    """
    # Dummy response
    return {
        "channel_id": req.channel_id,
        "video_file_path": req.video_file_path,
        "metadata": req.metadata,
        "yolo_analysis": "dummy_result",
        "runway_analysis": {"status": "pending", "msg": "Integración Runway dummy"},
        "msg": "Vídeo analizado y listo para distribución y procesamiento avanzado (dummy)."
    }
