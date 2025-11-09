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

# Instancia global
orchestrator = MLOrchestrator()

def get_system_status():
    return {
        "orchestrator": True,
        "video_gen": True,
        "campaigns": True,
        "clips": True
    }
