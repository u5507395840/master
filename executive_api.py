"""
API Backend Ejecutivo para gobierno total del sistema musical ML
"""
from fastapi import FastAPI, Body
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
import logging
import sys
import os
# Añadir el directorio 'src' al PYTHONPATH para encontrar los módulos
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))
from discografica_automator.services.orchestrator import orchestrator
from analytics_engine import get_youtube_performance_report

app = FastAPI(title="Discográfica ML Executive API", description="Gobierna campañas, IA, Meta Ads, usuarios y más.")

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
        response = orchestrator.client.chat.completions.create(
            model="gpt-4o-mini",
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
