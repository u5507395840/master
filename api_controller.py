"""
API Controller para gobernar el sistema de campañas y la IA.
"""
import sys
import os
# Añadir el directorio 'src' al PYTHONPATH para encontrar los módulos
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

from fastapi import FastAPI, Body
from pydantic import BaseModel
from typing import Optional, Dict, Any
import logging
from discografica_automator.services.orchestrator import orchestrator
from analytics_engine import get_youtube_performance_report

app = FastAPI(title="Viral Marketing AI Automator API", description="Gobierna el sistema y la IA desde endpoints seguros.")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class StrategyRequest(BaseModel):
    total_budget: float
    youtube_channel_url: str
    performance_days: Optional[int] = 30
    performance_data: Optional[Dict[str, Any]] = None

@app.get("/status")
def status():
    """Estado básico del sistema."""
    return {"status": "ok", "orchestrator": True}

@app.post("/strategy")
def generate_strategy(req: StrategyRequest):
    """
    Genera una estrategia de campañas satélite usando OpenAI (o fallback).
    Puedes enviar performance_data personalizado o dejar que el sistema lo simule.
    """
    if req.performance_data:
        performance_data = req.performance_data
    else:
        performance_data = get_youtube_performance_report(days=req.performance_days)
    plan = orchestrator.decide_meta_ads_strategy(
        performance_data=performance_data,
        total_budget=req.total_budget,
        youtube_channel_url=req.youtube_channel_url
    )
    return plan

@app.get("/performance_report")
def performance_report(days: int = 30):
    """
    Obtiene un informe de rendimiento simulado para pruebas.
    """
    return get_youtube_performance_report(days=days)

# Puedes añadir más endpoints para lanzar campañas, consultar logs, etc.

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api_controller:app", host="0.0.0.0", port=8000, reload=True)
