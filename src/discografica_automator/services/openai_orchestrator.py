"""
OpenAI Orchestrator - Integración REAL con o1 y GPT-4
"""
import os
import json
from openai import OpenAI
from typing import Dict, List, Optional

class OpenAIOrchestrator:
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY no configurada")
        
        self.client = OpenAI(api_key=self.api_key)
        self.model = "gpt-4-turbo-preview"  # Usar GPT-4 Turbo (o1 cuando esté disponible)
    
    def generate_campaign_strategy(self, artist: str, track: str, genre: str = "trap") -> Dict:
        """Generar estrategia de campaña completa con IA"""
        
        prompt = f"""
Eres un experto en marketing viral de música urbana. 

Artista: {artist}
Track: {track}
Género: {genre}

Genera una estrategia de campaña viral completa que incluya:

1. CONCEPTO CREATIVO:
   - Idea visual principal
   - Mood y estética
   - Referencias culturales relevantes

2. ESTRATEGIA DE CONTENIDO:
   - 5 ideas de videos cortos para TikTok/Reels
   - Hashtags específicos (#trap, #urban, etc)
   - Momentos clave del track para clips

3. TIMING Y PLATAFORMAS:
   - Mejor hora para publicar
   - Orden de plataformas (TikTok primero, etc)
   - Frecuencia de posts

4. ENGAGEMENT TACTICS:
   - Challenges potenciales
   - Collaboraciones recomendadas
   - Call-to-actions específicos

Responde en formato JSON estructurado.
"""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "Eres un experto en marketing viral musical."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.8,
                response_format={"type": "json_object"}
            )
            
            strategy = json.loads(response.choices[0].message.content)
            
            return {
                "status": "success",
                "artist": artist,
                "track": track,
                "strategy": strategy,
                "model_used": self.model
            }
        
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "fallback": self._get_fallback_strategy(artist, track, genre)
            }
    
    def generate_video_description(self, track_info: Dict) -> str:
        """Generar descripción para video viral"""
        
        prompt = f"""
Genera una descripción viral para TikTok/Instagram de:

Artista: {track_info.get('artist', 'Unknown')}
Track: {track_info.get('track', 'Unknown')}
Género: {track_info.get('genre', 'trap')}

La descripción debe:
- Ser corta (máx 150 caracteres)
- Incluir 3-5 hashtags relevantes
- Tener un hook que genere engagement
- Incluir call-to-action

Responde SOLO con la descripción, sin explicaciones.
"""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.9,
                max_tokens=100
            )
            
            return response.choices[0].message.content.strip()
        
        except Exception as e:
            return f"🔥 {track_info.get('track')} - {track_info.get('artist')} 🎵 #trap #music #viral"
    
    def analyze_content_performance(self, metrics: Dict) -> Dict:
        """Analizar rendimiento y dar recomendaciones con IA"""
        
        prompt = f"""
Analiza estas métricas de una campaña musical:

Views: {metrics.get('views', 0)}
Likes: {metrics.get('likes', 0)}
Shares: {metrics.get('shares', 0)}
Comments: {metrics.get('comments', 0)}
Watch time avg: {metrics.get('watch_time', 0)} segundos

Da:
1. Diagnóstico del rendimiento (bueno/regular/malo)
2. 3 recomendaciones específicas para mejorar
3. Predicción de potencial viral (1-10)

Responde en JSON con: diagnosis, recommendations[], viral_potential
"""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                response_format={"type": "json_object"}
            )
            
            analysis = json.loads(response.choices[0].message.content)
            return analysis
        
        except Exception as e:
            return {
                "diagnosis": "Error en análisis",
                "error": str(e),
                "recommendations": ["Revisar métricas", "Intentar nuevo contenido"]
            }
    
    def _get_fallback_strategy(self, artist: str, track: str, genre: str) -> Dict:
        """Estrategia de respaldo si falla la API"""
        return {
            "concepto_creativo": {
                "idea_visual": f"Video estilo urbano para {track}",
                "mood": "energético y nocturno",
                "referencias": ["videos de trap exitosos", "estética neón"]
            },
            "estrategia_contenido": {
                "ideas_videos": [
                    "Clip del hook principal",
                    "Behind the scenes en estudio",
                    "Lyric video animado",
                    "Challenge con el beat",
                    "Reacción de fans"
                ],
                "hashtags": [f"#{track.lower()}", "#trap", "#music", "#viral", f"#{artist.lower()}"]
            },
            "timing": {
                "mejor_hora": "18:00-22:00",
                "plataformas_orden": ["TikTok", "Instagram", "YouTube"],
                "frecuencia": "2-3 posts por día"
            }
        }

# Instancia global
openai_orchestrator = OpenAIOrchestrator()
