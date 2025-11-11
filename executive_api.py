from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()
# --- ENDPOINT: Generación de estrategia y prompts creativos por IA ---
class IAPromptStrategyRequest(BaseModel):
    performance_data: dict
    total_budget: float
    youtube_channel_url: str
    creativity_level: str = "alto"
    model: str = "gpt-5"

@app.post("/ia_generate_strategy")
def ia_generate_strategy(req: IAPromptStrategyRequest):
    # Obtener informe procesado por Ultralytics
    from analytics_engine import get_youtube_performance_report
    performance_report = get_youtube_performance_report(days=30)
    # Prompt argumental avanzado para OpenAI
    system_prompt = (
        "Eres un estratega musical IA experto en campañas virales y creatividad avanzada. "
        "Analiza el siguiente informe de rendimiento y análisis visual para generar una estrategia argumental detallada, "
        "incluyendo: \n"
        "- Acciones concretas para mejorar el rendimiento del canal\n"
        "- 3 prompts creativos para videos virales\n"
        "- Propuesta de distribución de presupuesto\n"
        "- Recomendaciones de contenido viral y colaboraciones\n"
        "- Sugerencias de plataformas y horarios óptimos\n"
        f"Nivel de creatividad: {req.creativity_level}."
    )
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"Informe completo: {performance_report}"}
    ]
    try:
        model = getattr(req, "model", "gpt-5")
        response = orchestrator.client.chat.completions.create(
            model=model,
            messages=messages,
            max_tokens=1500
        )
        # Espera una respuesta estructurada en JSON
        import json
        try:
            strategy = json.loads(response.choices[0].message.content)
        except Exception:
            strategy = {"raw": response.choices[0].message.content}
    except Exception as e:
        strategy = {"error": f"[Error IA]: {e}"}
    return {"strategy": strategy}
# --- ENDPOINT: Campaña 1 a 1 directa en cuentas satélite ---
class DirectSatelliteCampaignRequest(BaseModel):
    api_keys: list
    channel_id: str
    video_metadata: dict
    video_file_path: str

@app.post("/direct_satellite_campaign")
def direct_satellite_campaign(req: DirectSatelliteCampaignRequest):
    """
    Orquesta la publicación de vídeos en cuentas satélite de YouTube.
    Optimizado para feedback detallado y control de errores por cuenta.
    """
    from discografica_automator.services.orchestrator import orchestrator
    from ml_engine.vision.yolo_analyzer import YOLOAnalyzer
    results = []
    # Analizar el video y canal principal para obtener estilo y elementos virales
    analyzer = YOLOAnalyzer(use_coco=True)
    analysis = analyzer.analyze_video(req.video_file_path, use_coco=True)
    channel_info = {"id": req.channel_id}
    # Generar prompt y metadatos personalizados para cada cuenta satélite
    gen_result = orchestrator.generate_satellite_video_prompt(req.video_file_path, channel_info, use_coco=True)
    metadatos = gen_result.get("metadatos", {})
    for idx, api_key in enumerate(req.api_keys):
        try:
            # Aquí iría la llamada real al uploader con api_key, channel_id, metadatos, video_file_path
            video_id = f"video_{idx+1}_dummy"
            results.append({
                "status": "ok",
                "videoId": video_id,
                "account": api_key,
                "analysis": analysis,
                "metadatos": metadatos,
                "prompt": gen_result.get("prompt", "")
            })
        except Exception as e:
            results.append({
                "status": "error",
                "error": str(e),
                "account": api_key
            })
    return {"result": results}
# --- ENDPOINT: Automatización completa bajo trigger Meta Ads ---
class MetaTriggerSatelliteRequest(BaseModel):
    channel_id: str
    api_keys: list
    total_budget: float
    youtube_channel_url: str
    days: int = 30

@app.post("/meta_trigger_youtube_satellite")
def meta_trigger_youtube_satellite(payload: dict):
    """
    Recibe triggers de n8n o Meta Ads para lanzar campañas y recoger analítica.
    Estructura esperada del payload:
    {
        "campaign_id": str,
        "action": str,  # "launch" | "analyze"
        "meta_ads_data": dict,  # Opcional
        "youtube_channel_id": str,
        "video_metadata": dict,  # Opcional
    }
    """
    try:
        # Simulación de orquestación (reemplazar por lógica real)
        result = {
            "status": "ok",
            "msg": f"Trigger recibido para campaña {payload.get('campaign_id')} con acción {payload.get('action')}"
        }
    except Exception as e:
        result = {
            "status": "error",
            "error": str(e)
        }
    return result

from tools.gologin_android_manager import GoLoginManager, AndroidSimulatorManager
app = FastAPI(title="Discográfica ML Executive API", description="Gobierna campañas, IA, Meta Ads, usuarios y más.")

# --- ENDPOINT: Crear perfil GoLogin ---
class GoLoginProfileRequest(BaseModel):
    api_token: str
    name: str
    os_type: str = "android"

@app.post("/gologin_create_profile")
def gologin_create_profile(req: GoLoginProfileRequest):
    manager = GoLoginManager(req.api_token)
    result = manager.create_profile(req.name, req.os_type)
    return {"result": result}

# --- ENDPOINT: Lanzar perfil GoLogin ---
class GoLoginStartProfileRequest(BaseModel):
    api_token: str
    profile_id: str

@app.post("/gologin_start_profile")
def gologin_start_profile(req: GoLoginStartProfileRequest):
    manager = GoLoginManager(req.api_token)
    result = manager.start_profile(req.profile_id)
    return {"result": result}

# --- ENDPOINT: Parar perfil GoLogin ---
class GoLoginStopProfileRequest(BaseModel):
    api_token: str
    profile_id: str

@app.post("/gologin_stop_profile")
def gologin_stop_profile(req: GoLoginStopProfileRequest):
    manager = GoLoginManager(req.api_token)
    result = manager.stop_profile(req.profile_id)
    return {"result": result}

# --- ENDPOINT: Automatización Android (Appium/ADB) ---
class AndroidEmulatorRequest(BaseModel):
    avd_name: str

@app.post("/android_start_emulator")
def android_start_emulator(req: AndroidEmulatorRequest):
    manager = AndroidSimulatorManager()
    manager.start_emulator(req.avd_name)
    return {"status": "ok", "msg": f"Emulador {req.avd_name} lanzado."}

class AndroidInstallApkRequest(BaseModel):
    apk_path: str
    device_id: str = "emulator-5554"

@app.post("/android_install_apk")
def android_install_apk(req: AndroidInstallApkRequest):
    manager = AndroidSimulatorManager()
    manager.install_apk(req.apk_path, req.device_id)
    return {"status": "ok", "msg": f"APK {req.apk_path} instalado en {req.device_id}."}

class AndroidAppiumRequest(BaseModel):
    device_id: str = "emulator-5554"
    port: int = 4723

@app.post("/android_run_appium")
def android_run_appium(req: AndroidAppiumRequest):
    manager = AndroidSimulatorManager()
    manager.run_appium(req.device_id, req.port)
    return {"status": "ok", "msg": f"Appium lanzado en {req.device_id}:{req.port}."}

class AndroidAdbCommandRequest(BaseModel):
    command: list
    device_id: str = "emulator-5554"

@app.post("/android_execute_adb")
def android_execute_adb(req: AndroidAdbCommandRequest):
    manager = AndroidSimulatorManager()
    output = manager.execute_adb_command(req.command, req.device_id)
    return {"output": output}

# --- ENDPOINT: Trigger Meta Ads para n8n ---
@app.post("/metaads_trigger_n8n")
def metaads_trigger_n8n(payload: dict = Body(...)):
    # Aquí puedes integrar el trigger con n8n vía webhook o lógica interna
    # Por ejemplo, lanzar campañas en redes sociales usando los endpoints anteriores
    # payload puede incluir info de campaña, cuentas, creatividades, etc.
    # Simulación de respuesta
    return {"status": "ok", "msg": "Trigger recibido y procesado para automatización de campañas en redes sociales.", "payload": payload}

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

from discografica_automator.services.orchestrator import orchestrator
from uploaders.youtube_satellite_manager import YouTubeSatelliteManager
from analytics_engine import get_youtube_performance_report

app = FastAPI(title="Discográfica ML Executive API", description="Gobierna campañas, IA, Meta Ads, usuarios y más.")

# --- ENDPOINT: Input de información del canal principal ---
class MainChannelInputRequest(BaseModel):
    channel_id: str
    info: dict

main_channel_info = {}

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
@app.post("/satellite_publish_video")
def satellite_publish_video(req: SatelliteVideoRequest):
    manager = YouTubeSatelliteManager(req.api_keys, req.main_channel_id)
    result = manager.publish_video(req.video_metadata, req.video_file_path)
    return {"result": result}

# --- ENDPOINT: Consultar métricas de cuentas satélite ---
@app.post("/satellite_get_metrics")
def satellite_get_metrics(req: SatelliteMetricsRequest):
    manager = YouTubeSatelliteManager(req.api_keys, req.main_channel_id)
    result = manager.get_metrics()
    return {"metrics": result}

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
    """
    Lanza una campaña real (simulada) en las plataformas seleccionadas.
    """
    # Aquí iría la lógica real de integración con N8N y los posters
    logger.info(f"Lanzando campaña: {req.track_name} - {req.artist} en {req.platforms}")
    return {"result": "ok", "msg": f"Campaña lanzada en {', '.join(req.platforms)}"}

@app.post("/calculate_roi")
def calculate_roi(req: ROIRequest):
    """
    Calcula el ROI y métricas clave de una campaña Meta Ads.
    """
    result = orchestrator.calculate_roi(req.dict())
    return result

@app.get("/meta_ads_status")
def meta_ads_status():
    """
    Devuelve el estado actual de la integración Meta Ads (tokens/configuración).
    """
    return orchestrator.get_meta_ads_status()

@app.get("/performance_report")
def performance_report(days: int = 30):
    """
    Obtiene un informe de rendimiento simulado para pruebas.
    """
    return get_youtube_performance_report(days=days)

@app.post("/set_openai_key")
def set_openai_key(api_key: str = Body(...)): 
    """
    Configura y valida la OpenAI API Key.
    """
    ok = orchestrator.set_api_key(api_key)
    return {"valid": ok, "status": orchestrator.get_api_key_status()}

@app.get("/get_openai_key_status")
def get_openai_key_status():
    """
    Devuelve el estado actual de la OpenAI API Key.
    """
    return {"status": orchestrator.get_api_key_status()}

@app.post("/openai_chat")
def openai_chat(req: OpenAIChatRequest):
    """
    Chat central: responde preguntas, ejecuta acciones, integra automatización y control.
    """
    # Construir historial para chat-completions
    messages = []
    if req.system_prompt:
        messages.append({"role": "system", "content": req.system_prompt})
    if req.history:
        messages.extend(req.history)
    messages.append({"role": "user", "content": req.prompt})
    try:
        model = getattr(req, "model", None) or "gpt-3.5-turbo"
        # Si se recibe una API Key, usarla para la llamada
        if req.openai_api_key:
            from openai import OpenAI
            client = OpenAI(api_key=req.openai_api_key)
            response = client.chat.completions.create(
                model=model,
                messages=messages,
                max_tokens=700
            )
        else:
            response = orchestrator.client.chat.completions.create(
                model=model,
                messages=messages,
                max_tokens=700
            )
        ai_reply = response.choices[0].message.content
    except Exception as e:
        ai_reply = f"[Error IA]: {e}"
    # Ejecutar acciones especiales si se solicita
    action_result = None
    if req.action:
        if req.action == "launch_campaign" and req.params:
            # Lógica para lanzar campaña real
            action_result = launch_campaign_api(req.params)
        elif req.action == "calculate_roi" and req.params:
            action_result = orchestrator.calculate_roi(req.params)
        # Puedes añadir más acciones: consultar tokens, modo dummy, etc.
    return {"response": ai_reply, "action_result": action_result}

def launch_campaign_api(params: dict):
    # Simulación de lanzamiento de campaña (puedes conectar con n8n aquí)
    return {"result": "ok", "msg": f"Campaña lanzada: {params.get('track_name', 'N/A')}"}

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
    from ml_engine.vision.yolo_analyzer import yolo_analyzer
    yolo_result = yolo_analyzer.analyze_video(req.video_file_path)
    # --- INTEGRACIÓN RUNWAY ---
    # TODO: Aquí puedes conectar con la API de Runway para procesar el vídeo/audio
    # Ejemplo:
    # runway_result = runway_client.process_video(req.video_file_path)
    runway_result = {"status": "pending", "msg": "Integración Runway aquí"}
    return {
        "channel_id": req.channel_id,
        "video_file_path": req.video_file_path,
        "metadata": req.metadata,
        "yolo_analysis": yolo_result,
        "runway_analysis": runway_result,
        "msg": "Vídeo analizado y listo para distribución y procesamiento avanzado."
    }
