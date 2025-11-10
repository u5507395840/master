"""
🤖 OPENAI CLIENT - Control de coste
"""
import os
import logging
from datetime import datetime
from openai import OpenAI

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class OpenAIManager:
    MAX_BUDGET_EUR = 50.0
    MAX_REQUESTS_DAY = 100
    
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            logger.warning("⚠️ OPENAI_API_KEY not set")
            self.client = None
        else:
            self.client = OpenAI(api_key=api_key)
        
        self.current_spend = 0.0
        self.requests_today = 0
    
    def ask(self, prompt: str, model: str = "gpt-4o-mini") -> str:
        if not self.client:
            return "OpenAI no configurado"
        
        if self.current_spend >= self.MAX_BUDGET_EUR:
            return "Budget alcanzado"
        
        if self.requests_today >= self.MAX_REQUESTS_DAY:
            return "Límite diario alcanzado"
        
        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=300
            )
            
            self.requests_today += 1
            
            # Estimar coste
            tokens = response.usage.total_tokens
            cost = (tokens * 0.0001) * 0.92
            self.current_spend += cost
            
            logger.info(f"Request #{self.requests_today}: €{cost:.6f}")
            
            return response.choices[0].message.content
            
        except Exception as e:
            logger.error(f"Error: {e}")
            return f"Error: {str(e)}"

openai_manager = OpenAIManager()
