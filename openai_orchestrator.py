"""
🎵 OPENAI ORCHESTRATOR - CEREBRO CENTRAL DEL SISTEMA
Controla toda la automatización con inteligencia artificial
"""
import os
import json
import logging
from datetime import datetime
from typing import Dict, List, Optional
from openai import OpenAI

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class OpenAIOrchestrator:
    """Cerebro central que usa OpenAI para decisiones estratégicas"""
    
    def __init__(self):
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            logger.warning("OPENAI_API_KEY no configurada - modo simulación")
            self.client = None
        else:
            self.client = OpenAI(api_key=api_key)
    
    def generate_campaign_strategy(self, track_info: Dict) -> Dict:
        """Genera estrategia completa de campaña usando GPT-4"""
        if not self.client:
            return self._dummy_strategy(track_info)
        
        try:
            prompt = f"""
Eres un experto en marketing musical y campañas virales.

INFORMACIÓN DEL TRACK:
- Artista: {track_info.get('artist', 'Unknown')}
- Título: {track_info.get('title', 'Unknown')}
- Género: {track_info.get('genre', 'Unknown')}
- Duración: {track_info.get('duration', 'Unknown')}
- Descripción: {track_info.get('description', '')}

GENERA UNA ESTRATEGIA COMPLETA EN JSON con:
1. video_prompts: Lista de 3 prompts para generar videos virales
2. posting_schedule: Mejor momento para publicar (día y hora)
3. hashtags: 10 hashtags optimizados
4. caption: Caption viral para redes sociales
5. platforms: Prioridad de plataformas (TikTok, Instagram, YouTube)
6. budget_allocation: Distribución de presupuesto por plataforma
7. target_audience: Descripción de audiencia objetivo
8. engagement_strategy: Tácticas de engagement

Responde SOLO con JSON válido, sin markdown.
"""
            
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "Eres un experto en marketing musical. Respondes solo con JSON válido."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.8
            )
            
            strategy = json.loads(response.choices[0].message.content)
            logger.info(f"✅ Estrategia generada para: {track_info.get('title')}")
            return strategy
            
        except Exception as e:
            logger.error(f"Error generando estrategia: {e}")
            return self._dummy_strategy(track_info)
    
    def generate_video_prompt(self, track_info: Dict, style: str = "viral") -> str:
        """Genera prompt optimizado para generación de video"""
        if not self.client:
            return f"Music video for {track_info.get('genre', 'music')} track with neon lights"
        
        try:
            prompt = f"""
Genera un prompt detallado para crear un video musical viral.

TRACK INFO:
- Género: {track_info.get('genre', 'Unknown')}
- Mood: {track_info.get('mood', 'energetic')}
- Target: {track_info.get('target_audience', 'Gen Z')}

El prompt debe ser:
- Visual y cinematográfico
- Optimizado para engagement en redes sociales
- Estilo: {style}
- Máximo 500 caracteres

Responde SOLO con el prompt, sin explicaciones.
"""
            
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.9,
                max_tokens=200
            )
            
            video_prompt = response.choices[0].message.content.strip()
            logger.info(f"✅ Video prompt generado: {video_prompt[:50]}...")
            return video_prompt
            
        except Exception as e:
            logger.error(f"Error generando video prompt: {e}")
            return f"Cinematic music video, {track_info.get('genre')} style, neon lights, urban setting"
    
    def analyze_metrics(self, metrics: Dict) -> Dict:
        """Analiza métricas y genera recomendaciones con IA"""
        if not self.client:
            return {"recommendation": "Continuar estrategia actual", "confidence": 0.7}
        
        try:
            prompt = f"""
Analiza estas métricas de campaña musical y da recomendaciones:

MÉTRICAS:
{json.dumps(metrics, indent=2)}

Proporciona en JSON:
1. recommendation: Recomendación principal
2. confidence: Nivel de confianza (0-1)
3. actions: Lista de 3 acciones concretas
4. risks: Riesgos identificados
5. opportunities: Oportunidades detectadas

Responde SOLO con JSON válido.
"""
            
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.5
            )
            
            analysis = json.loads(response.choices[0].message.content)
            return analysis
            
        except Exception as e:
            logger.error(f"Error analizando métricas: {e}")
            return {"recommendation": "Error en análisis", "confidence": 0}
    
    def generate_community_response(self, comment: str, context: str = "") -> str:
        """Genera respuesta inteligente para community management"""
        if not self.client:
            return "¡Gracias por tu apoyo! 🎵🔥"
        
        try:
            prompt = f"""
Eres el community manager de un artista musical urbano.

COMENTARIO: "{comment}"
CONTEXTO: {context}

Genera una respuesta:
- Auténtica y cercana
- Con emojis apropiados
- Que fomente engagement
- Máximo 280 caracteres

Responde SOLO con el texto, sin comillas.
"""
            
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.8,
                max_tokens=100
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            logger.error(f"Error generando respuesta: {e}")
            return "¡Gracias por tu apoyo! 🎵🔥"
    
    def _dummy_strategy(self, track_info: Dict) -> Dict:
        """Estrategia de respaldo cuando no hay OpenAI"""
        return {
            "video_prompts": [
                f"{track_info.get('genre', 'music')} artist performing with neon lights",
                f"Urban night scene with {track_info.get('genre', 'music')} vibes",
                f"Studio session, cinematic, {track_info.get('genre', 'music')} style"
            ],
            "posting_schedule": {
                "day": "Friday",
                "time": "18:00",
                "timezone": "EST"
            },
            "hashtags": [
                f"#{track_info.get('genre', 'music')}",
                "#newmusic", "#viral", "#trending",
                "#musicvideo", "#artist", "#song",
                "#music", "#trap", "#hiphop"
            ],
            "caption": f"🔥 Nuevo track disponible! {track_info.get('title', 'Track')} 🎵",
            "platforms": ["TikTok", "Instagram", "YouTube"],
            "budget_allocation": {
                "TikTok": 0.4,
                "Instagram": 0.35,
                "YouTube": 0.25
            },
            "target_audience": "Gen Z, 16-24, urban music fans",
            "engagement_strategy": [
                "Post stories diarios",
                "Responder comentarios en 2 horas",
                "Crear challenges en TikTok"
            ]
        }


# Singleton global
_orchestrator = None

def get_orchestrator() -> OpenAIOrchestrator:
    """Obtiene instancia única del orchestrator"""
    global _orchestrator
    if _orchestrator is None:
        _orchestrator = OpenAIOrchestrator()
    return _orchestrator
