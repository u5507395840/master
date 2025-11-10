"""
🧠 ORCHESTRATOR ML - Cerebro Central con OpenAI
"""
import os
import json
import logging
from openai import OpenAI

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MLOrchestrator:
    """Orquestador central con OpenAI"""
    
    MAX_BUDGET_EUR = 50.0
    
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            logger.warning("⚠️ OPENAI_API_KEY not set - modo fallback")
            self.client = None
        else:
            self.client = OpenAI(api_key=api_key)
        
        self.current_spend = 0.0
    
    def analyze_system(self, data: dict) -> dict:
        """Análisis del sistema con OpenAI"""
        if not self.client or self.current_spend >= self.MAX_BUDGET_EUR:
            return self._fallback_analysis(data)
        
        try:
            prompt = f"Analiza este sistema de automatización musical: {json.dumps(data)}"
            
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=500
            )
            
            # Track spend
            tokens = response.usage.total_tokens
            cost = (tokens * 0.0001) * 0.92  # Estimación EUR
            self.current_spend += cost
            
            logger.info(f"💰 OpenAI cost: €{cost:.4f} (total: €{self.current_spend:.2f})")
            
            return {
                "status": "ok",
                "analysis": response.choices[0].message.content,
                "cost_eur": cost,
                "tokens": tokens
            }
            
        except Exception as e:
            logger.error(f"Error OpenAI: {e}")
            return self._fallback_analysis(data)
    
    def _fallback_analysis(self, data: dict) -> dict:
        """Análisis sin OpenAI"""
        return {
            "status": "ok",
            "analysis": "Sistema funcionando - análisis básico",
            "fallback": True
        }
    
    def decide_meta_ads_strategy(self, performance_data: dict, total_budget: float, youtube_channel_url: str) -> dict:
        """
        Decide una estrategia de Meta Ads basada en el rendimiento y un presupuesto.
        Utiliza OpenAI para distribuir el presupuesto en 5 campañas satélite.
        """
        if not self.client:
            logger.warning("Cliente OpenAI no disponible. Usando estrategia de fallback.")
            return self._fallback_strategy(total_budget)

        prompt = f"""
        Eres un estratega experto en marketing musical para Meta Ads. Tu objetivo es maximizar el tráfico de calidad a un canal de YouTube principal.

        Canal de YouTube a promocionar: {youtube_channel_url}

        Datos de rendimiento de campañas anteriores:
        {json.dumps(performance_data, indent=2)}

        Presupuesto total para esta nueva fase: {total_budget} EUR.

        Tu tarea es diseñar un plan de acción para 5 campañas "satélite" en Meta Ads. Distribuye el presupuesto total entre estas 5 campañas basándote en los datos de rendimiento. Prioriza las audiencias y tipos de contenido que han demostrado un mejor 'coste por clic' (CPC) y 'tasa de clics' (CTR).

        Define para cada campaña:
        1. 'campaign_name': Un nombre descriptivo (ej. "Satélite 1 - Fans de Artistas Similares").
        2. 'target_audience': Una descripción de la audiencia a la que se dirige.
        3. 'ad_creative_prompt': Un prompt para generar el texto e imagen del anuncio (ej. "Anuncio enfocado en el videoclip, con un gancho sobre la producción...").
        4. 'budget_eur': La cantidad del presupuesto asignada a esta campaña.

        La suma de los presupuestos de las 5 campañas debe ser igual al presupuesto total.

        Devuelve el resultado únicamente en formato JSON, como una lista de 5 objetos, dentro de una clave "campaign_plan".
        Ejemplo de formato:
        {{
          "campaign_plan": [
            {{
              "campaign_name": "...",
              "target_audience": "...",
              "ad_creative_prompt": "...",
              "budget_eur": ...
            }}
          ]
        }}
        """

        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                response_format={"type": "json_object"},
                messages=[
                    {"role": "system", "content": "Eres un estratega de marketing que siempre devuelve JSON con el plan de campaña solicitado."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1500,
                temperature=0.7
            )

            strategy_plan = json.loads(response.choices[0].message.content)
            
            # Track spend
            tokens = response.usage.total_tokens
            cost = (tokens * 0.0001) * 0.92  # Estimación EUR
            self.current_spend += cost
            logger.info(f"💰 OpenAI cost for strategy: €{cost:.4f} (total spend: €{self.current_spend:.2f})")

            return strategy_plan

        except Exception as e:
            logger.error(f"Error al decidir la estrategia con OpenAI: {e}")
            return self._fallback_strategy(total_budget)

    def _fallback_strategy(self, total_budget: float) -> dict:
        """Estrategia de fallback si OpenAI falla."""
        budget_per_campaign = total_budget / 5
        return {
            "campaign_plan": [
                {
                    "campaign_name": f"Satélite {i+1} - Fallback",
                    "target_audience": "Audiencia general interesada en música",
                    "ad_creative_prompt": "Anuncio genérico promocionando el nuevo video musical.",
                    "budget_eur": budget_per_campaign
                } for i in range(5)
            ]
        }

# Instancia global
orchestrator = MLOrchestrator()

def get_system_status():
    return {
        "orchestrator": True,
        "video_gen": True,
        "campaigns": True,
        "clips": True
    }
